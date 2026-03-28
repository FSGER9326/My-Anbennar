#!/usr/bin/env python3
"""Prepare a PR draft from local repo state and validation outputs."""

from __future__ import annotations

import argparse
import os
import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


DOMAIN_ORDER = ["automation", "docs", "gameplay", "events", "loc", "other"]


def run_git(args: list[str]) -> str:
    result = subprocess.run(
        ["git", *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.rstrip("\n")


def classify_domain(path: str) -> str:
    if path.startswith(("automation/", "scripts/", ".github/")):
        return "automation"
    if path.startswith("docs/"):
        return "docs"
    if path.startswith("events/"):
        return "events"
    if path.startswith("localisation/"):
        return "loc"
    if path.startswith(("common/", "decisions/", "missions/")):
        return "gameplay"
    return "other"


def load_validation_report(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Validation report is not valid JSON: {path} ({exc})") from exc


def has_unresolved_high(validation_report: dict[str, Any]) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    issues = list(validation_report.get("unresolved_issues", []))
    issues.extend(validation_report.get("issues", []))
    issues.extend(validation_report.get("findings", []))
    for issue in issues:
        if str(issue.get("severity", "")).lower() == "high" and not issue.get("resolved", False):
            reasons.append(issue.get("title", "unresolved high-severity issue"))
    for check in validation_report.get("checks", []):
        if str(check.get("severity", "")).lower() == "high" and str(check.get("status", "")).lower() != "pass":
            reasons.append(check.get("name", "high-severity validation check failure"))
    return bool(reasons), reasons


def collect_changed_files() -> list[str]:
    # Includes tracked and untracked files, excluding deletes for draft readability.
    output = run_git(["status", "--porcelain"])
    changed: list[str] = []
    ignored_prefixes = ("automation/reports/", "scripts/__pycache__/")
    for line in output.splitlines():
        if not line:
            continue
        status = line[:2]
        path = line[3:]
        if status.endswith("D") or status.startswith("D"):
            continue
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        if path.endswith("/"):
            continue
        if path.startswith(ignored_prefixes):
            continue
        changed.append(path)
    return sorted(set(changed))


def build_domain_groups(changed_files: list[str]) -> dict[str, list[str]]:
    grouped: dict[str, list[str]] = defaultdict(list)
    for path in changed_files:
        grouped[classify_domain(path)].append(path)
    return grouped


def suggest_slicing(groups: dict[str, list[str]]) -> list[str]:
    suggestions: list[str] = []
    for domain in DOMAIN_ORDER:
        files = groups.get(domain, [])
        if not files:
            continue
        quoted_files = " ".join(f'"{f}"' for f in files)
        suggestions.append(
            f"- {domain}: git add {quoted_files} && git commit -m \"slice({domain}): checkpoint\""
        )
    return suggestions


def perform_commit_slicing(groups: dict[str, list[str]], message_prefix: str) -> list[str]:
    created: list[str] = []
    staged_check = run_git(["diff", "--cached", "--name-only"])
    if staged_check:
        raise SystemExit("Cannot auto-slice commits with pre-staged files. Run `git reset` first.")
    for domain in DOMAIN_ORDER:
        files = groups.get(domain, [])
        if not files:
            continue
        subprocess.run(["git", "add", "--", *files], check=True)
        if not run_git(["diff", "--cached", "--name-only"]).strip():
            continue
        msg = f"{message_prefix} {domain} slice"
        subprocess.run(["git", "commit", "-m", msg], check=True)
        created.append(msg)
    return created


def validation_lines(validation_report: dict[str, Any]) -> list[str]:
    checks = validation_report.get("checks", [])
    if not checks:
        return ["- No machine-readable validation report was found."]
    out: list[str] = []
    for check in checks:
        status = str(check.get("status", "unknown")).upper()
        name = check.get("name", "unnamed-check")
        command = check.get("command", "")
        out.append(f"- `{name}`: **{status}**" + (f" (`{command}`)" if command else ""))
    return out


def risk_lines(groups: dict[str, list[str]]) -> list[str]:
    risks: list[str] = []
    if groups.get("gameplay") or groups.get("events"):
        risks.append("- Gameplay/event behavior changed; verify save compatibility and trigger scopes.")
    if groups.get("loc"):
        risks.append("- Localisation touched; verify keys and in-game text rendering.")
    if groups.get("automation") or groups.get("docs"):
        risks.append("- Tooling/docs updates could alter contributor workflow expectations.")
    if groups.get("other"):
        risks.append("- Unclassified files were changed; do a manual sanity pass before merge.")
    return risks or ["- Low risk: no high-impact gameplay paths modified."]


def write_pr_draft(
    output_path: Path,
    groups: dict[str, list[str]],
    why: str,
    validation_report: dict[str, Any],
    artifact_urls: list[str],
) -> None:
    changed_total = sum(len(v) for v in groups.values())
    lines: list[str] = [
        "# PR Draft",
        "",
        "## What changed",
        f"- Total changed files: **{changed_total}**",
    ]
    for domain in DOMAIN_ORDER:
        files = groups.get(domain, [])
        if not files:
            continue
        lines.append(f"- **{domain}** ({len(files)} files)")
        for file_path in files:
            lines.append(f"  - `{file_path}`")

    lines.extend(
        [
            "",
            "## Why",
            f"- {why}",
            "",
            "## Validation evidence",
            *validation_lines(validation_report),
            "",
            "## Risk notes",
            *risk_lines(groups),
            "",
            "## Rollback notes",
            "- Revert the PR merge commit if production behavior regresses.",
            "- If slices were used, revert only the offending slice commit(s) and keep safe slices.",
            "",
            "## Artifact links",
        ]
    )

    report_artifacts = validation_report.get("artifacts", [])
    for artifact in report_artifacts:
        name = artifact.get("name", "artifact")
        url = artifact.get("url") or artifact.get("path")
        if url:
            lines.append(f"- [{name}]({url})")
    for url in artifact_urls:
        lines.append(f"- [external-artifact]({url})")
    if lines[-1] == "## Artifact links":
        lines.append("- No artifact links were provided yet.")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def infer_ci_artifact_urls() -> list[str]:
    urls: list[str] = []
    github_server = os.getenv("GITHUB_SERVER_URL", "").strip()
    github_repo = os.getenv("GITHUB_REPOSITORY", "").strip()
    github_run_id = os.getenv("GITHUB_RUN_ID", "").strip()
    if github_server and github_repo and github_run_id:
        urls.append(f"{github_server}/{github_repo}/actions/runs/{github_run_id}")
    extra = os.getenv("PR_PREP_ARTIFACT_URLS", "").strip()
    if extra:
        urls.extend([part.strip() for part in extra.split(",") if part.strip()])
    return urls


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare PR draft markdown from repo state.")
    parser.add_argument(
        "--validation-report",
        default="automation/reports/validation_report.json",
        help="Machine-readable validation report path (JSON).",
    )
    parser.add_argument(
        "--output",
        default="automation/pr/PR_DRAFT.md",
        help="Path to write generated draft markdown.",
    )
    parser.add_argument(
        "--why",
        default="Improve PR quality with structured summaries and safer commit slicing.",
        help="One-line rationale section text for the PR draft.",
    )
    parser.add_argument(
        "--artifact-url",
        action="append",
        default=[],
        help="Additional artifact URL to include (repeatable).",
    )
    parser.add_argument(
        "--slice-commits",
        action="store_true",
        help="Perform commit slicing by domain after suggesting slices.",
    )
    parser.add_argument(
        "--slice-message-prefix",
        default="chore(pr-prep):",
        help="Prefix for generated slice commit messages.",
    )
    args = parser.parse_args()

    report_path = Path(args.validation_report)
    validation_report = load_validation_report(report_path)
    has_high, reasons = has_unresolved_high(validation_report)
    if has_high:
        print("PR prep blocked: unresolved high-severity validation issues detected.", file=sys.stderr)
        for reason in reasons:
            print(f" - {reason}", file=sys.stderr)
        return 2

    changed = collect_changed_files()
    groups = build_domain_groups(changed)
    suggestions = suggest_slicing(groups)

    print("Commit slicing suggestions:")
    if suggestions:
        for suggestion in suggestions:
            print(suggestion)
    else:
        print("- No changed files detected.")

    if args.slice_commits and changed:
        created = perform_commit_slicing(groups, args.slice_message_prefix)
        print("Created slice commits:")
        for msg in created:
            print(f"- {msg}")

    output_path = Path(args.output)
    artifact_urls = list(args.artifact_url)
    artifact_urls.extend(infer_ci_artifact_urls())
    write_pr_draft(output_path, groups, args.why, validation_report, artifact_urls)
    print(f"PR draft written: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
