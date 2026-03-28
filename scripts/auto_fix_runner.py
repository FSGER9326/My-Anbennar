#!/usr/bin/env python3
"""Apply allowlisted fixes from validation_report.json until clean or max iterations."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import shlex
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT_PATH = ROOT / "validation_report.json"
DEFAULT_POLICY_PATH = ROOT / "scripts" / "auto_fix_policy.yaml"
DEFAULT_LOG_PATH = ROOT / "artifacts" / "auto_fix_log.json"

CONFLICT_START = "<<<<<<<"
CONFLICT_SPLIT = "======="
CONFLICT_END = ">>>>>>>"

ALLOWLISTED_ACTIONS = {
    "normalize_line_endings",
    "remove_conflict_markers_hotspot",
    "enforce_heading_singleton",
    "replace_placeholder_keys",
}


@dataclass
class Issue:
    code: str
    path: Path
    raw: dict[str, Any]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Read validation_report.json, apply allowlisted fixes, rerun validations after "
            "each batch, and stop when clean or max-iterations is reached."
        )
    )
    parser.add_argument(
        "--report",
        default=str(DEFAULT_REPORT_PATH),
        help="Path to validation report JSON (default: %(default)s).",
    )
    parser.add_argument(
        "--policy",
        default=str(DEFAULT_POLICY_PATH),
        help="Path to allowlist policy YAML/JSON (default: %(default)s).",
    )
    parser.add_argument(
        "--log",
        default=str(DEFAULT_LOG_PATH),
        help="Path to fix log JSON (default: %(default)s).",
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=5,
        help="Maximum fix iterations (default: %(default)s).",
    )
    parser.add_argument(
        "--validation-cmd",
        action="append",
        default=[],
        help=(
            "Validation command to run after each batch (repeatable). "
            "If omitted, reads report.validation_commands."
        ),
    )
    parser.add_argument(
        "--allow-write-fixes",
        action="store_true",
        help="Required flag to actually mutate files.",
    )
    return parser.parse_args()


def read_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"ERROR: report not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"ERROR: invalid JSON in {path}: {exc}") from exc


def read_policy(path: Path) -> dict[str, Any]:
    # YAML is a superset of JSON. Keep parser dependency-free by expecting JSON-compatible YAML.
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise SystemExit(f"ERROR: policy not found: {path}") from exc

    try:
        policy = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(
            "ERROR: policy parser requires JSON-compatible YAML. "
            f"Could not parse {path}: {exc}"
        ) from exc

    issue_code_map = policy.get("issue_code_map")
    if not isinstance(issue_code_map, dict):
        raise SystemExit("ERROR: policy.issue_code_map must be an object")

    for code, rule in issue_code_map.items():
        if not isinstance(rule, dict):
            raise SystemExit(f"ERROR: policy rule for {code!r} must be an object")
        action = rule.get("action")
        if action not in ALLOWLISTED_ACTIONS:
            raise SystemExit(
                f"ERROR: policy rule for {code!r} uses non-allowlisted action {action!r}"
            )
    return policy


def normalize_issue(raw_issue: dict[str, Any]) -> Issue | None:
    code = str(raw_issue.get("code") or "").strip()
    path_raw = raw_issue.get("path") or raw_issue.get("file") or raw_issue.get("target")
    if not code or not path_raw:
        return None

    path = Path(str(path_raw))
    if path.is_absolute():
        try:
            path = path.relative_to(ROOT)
        except ValueError:
            return None
    return Issue(code=code, path=path, raw=raw_issue)


def collect_issues(report: dict[str, Any]) -> list[Issue]:
    issues_blob = report.get("issues")
    if not isinstance(issues_blob, list):
        return []

    issues: list[Issue] = []
    for item in issues_blob:
        if not isinstance(item, dict):
            continue
        issue = normalize_issue(item)
        if issue is None:
            continue
        issues.append(issue)
    return issues


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_conflict_markers(text: str) -> str:
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    i = 0
    changed = False
    while i < len(lines):
        if not lines[i].startswith(CONFLICT_START):
            out.append(lines[i])
            i += 1
            continue

        changed = True
        i += 1
        ours: list[str] = []
        while i < len(lines) and not lines[i].startswith(CONFLICT_SPLIT):
            ours.append(lines[i])
            i += 1
        if i < len(lines):
            i += 1
        while i < len(lines) and not lines[i].startswith(CONFLICT_END):
            i += 1
        if i < len(lines):
            i += 1

        out.extend(ours)

    if not changed:
        return text
    return "".join(out)


def enforce_single_heading(text: str, heading: str) -> str:
    lines = text.splitlines(keepends=True)
    matches = [idx for idx, line in enumerate(lines) if line.strip() == heading]
    if len(matches) <= 1:
        return text

    first = matches[0]
    kept = []
    for idx, line in enumerate(lines):
        if idx != first and line.strip() == heading:
            continue
        kept.append(line)
    return "".join(kept)


def replace_placeholders(text: str, replacements: dict[str, str]) -> str:
    updated = text
    for old, new in replacements.items():
        updated = updated.replace(old, new)
    return updated


def should_apply_hotspot(path: Path, hotspots: list[str]) -> bool:
    path_text = path.as_posix()
    return any(path_text.startswith(prefix) for prefix in hotspots)


def apply_issue_fix(issue: Issue, rule: dict[str, Any], *, write_enabled: bool) -> dict[str, Any] | None:
    action = rule["action"]
    abs_path = ROOT / issue.path
    if not abs_path.exists() or not abs_path.is_file():
        return None

    before_bytes = abs_path.read_bytes()
    before_hash = hashlib.sha256(before_bytes).hexdigest()
    before_text = before_bytes.decode("utf-8", errors="surrogateescape")
    after_text = before_text

    if action == "normalize_line_endings":
        after_text = before_text.replace("\r\n", "\n").replace("\r", "\n")
    elif action == "remove_conflict_markers_hotspot":
        hotspots = rule.get("hotspots") or []
        if not isinstance(hotspots, list) or not all(isinstance(x, str) for x in hotspots):
            return None
        if should_apply_hotspot(issue.path, hotspots):
            after_text = replace_conflict_markers(before_text)
    elif action == "enforce_heading_singleton":
        heading = str(rule.get("heading") or "").strip()
        if not heading:
            return None
        after_text = enforce_single_heading(before_text, heading)
    elif action == "replace_placeholder_keys":
        replacements = rule.get("replacements")
        if not isinstance(replacements, dict):
            return None
        string_replacements = {str(k): str(v) for k, v in replacements.items()}
        after_text = replace_placeholders(before_text, string_replacements)

    if after_text == before_text:
        return None

    after_bytes = after_text.encode("utf-8", errors="surrogateescape")
    after_hash = hashlib.sha256(after_bytes).hexdigest()

    if write_enabled:
        abs_path.write_bytes(after_bytes)

    return {
        "timestamp_utc": utc_now_iso(),
        "path": issue.path.as_posix(),
        "code": issue.code,
        "action": action,
        "before_sha256": before_hash,
        "after_sha256": after_hash,
        "changed": before_hash != after_hash,
        "issue": copy.deepcopy(issue.raw),
    }


def append_log(log_path: Path, entries: list[dict[str, Any]]) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    if log_path.exists():
        try:
            payload = json.loads(log_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            payload = {}
    else:
        payload = {}

    existing = payload.get("applied_fixes")
    if not isinstance(existing, list):
        existing = []

    existing.extend(entries)
    payload["applied_fixes"] = existing
    payload["updated_at_utc"] = utc_now_iso()
    log_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def resolve_validation_commands(args: argparse.Namespace, report: dict[str, Any]) -> list[str]:
    commands = [cmd for cmd in args.validation_cmd if cmd.strip()]
    if commands:
        return commands

    report_cmds = report.get("validation_commands")
    if isinstance(report_cmds, list) and all(isinstance(x, str) for x in report_cmds):
        return [x for x in report_cmds if x.strip()]

    return []


def run_validation_commands(commands: list[str]) -> int:
    if not commands:
        return 0

    for command in commands:
        print(f"[validate] {command}")
        result = subprocess.run(
            shlex.split(command),
            cwd=ROOT,
            check=False,
        )
        if result.returncode != 0:
            return result.returncode
    return 0


def main() -> int:
    args = parse_args()
    report_path = Path(args.report)
    policy_path = Path(args.policy)
    log_path = Path(args.log)

    report = read_json(report_path)
    policy = read_policy(policy_path)
    issue_code_map = policy["issue_code_map"]

    validation_commands = resolve_validation_commands(args, report)
    if not args.allow_write_fixes:
        print(
            "Analysis-only mode: no files will be modified. "
            "Use --allow-write-fixes to enable mutations."
        )

    iterations = 0
    total_applied = 0

    while iterations < args.max_iterations:
        iterations += 1
        issues = collect_issues(report)
        if not issues:
            print(f"No issues found in {report_path}. Done.")
            break

        batch_entries: list[dict[str, Any]] = []
        for issue in issues:
            rule = issue_code_map.get(issue.code)
            if not isinstance(rule, dict):
                continue
            entry = apply_issue_fix(issue, rule, write_enabled=args.allow_write_fixes)
            if entry is None:
                continue
            batch_entries.append(entry)

        if batch_entries:
            append_log(log_path, batch_entries)
            total_applied += len(batch_entries)
            print(f"Iteration {iterations}: applied {len(batch_entries)} fix(es).")
        else:
            print(f"Iteration {iterations}: no allowlisted fixes were applicable.")
            break

        if not args.allow_write_fixes:
            print("Stopping after dry-run batch because writes are disabled.")
            break

        if validation_commands:
            status = run_validation_commands(validation_commands)
            if status != 0:
                print(f"Validation command failed with exit code {status}.")
                return status

        report = read_json(report_path)
        if not collect_issues(report):
            print("Validation report is clean after fixes.")
            break
    else:
        print(f"Reached max iterations ({args.max_iterations}).")

    print(f"Total fixes recorded: {total_applied}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
