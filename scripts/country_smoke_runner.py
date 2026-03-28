#!/usr/bin/env python3
"""Run profile-based smoke checks for a country/workstream."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
CHECK_NAME = "country_smoke_runner"


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _issue(file: str, line: int | None, code: str, message: str, suggested_fix_command: str, severity: str = "error") -> dict[str, object]:
    return {"check": CHECK_NAME, "severity": severity, "file": file, "line": line, "code": code, "message": message, "suggested_fix_command": suggested_fix_command}


def _strip_comment(line: str) -> str:
    in_quote = False
    out: list[str] = []
    for ch in line:
        if ch == '"':
            in_quote = not in_quote
            out.append(ch)
            continue
        if ch == "#" and not in_quote:
            break
        out.append(ch)
    return "".join(out)


def _is_dangerous_for_top_level_duplicates(path: Path) -> bool:
    rel = path.as_posix()
    dangerous_roots = ("common/scripted_effects/", "common/scripted_triggers/", "common/decisions/", "common/modifiers/")
    return rel.endswith(".txt") and any(root in rel for root in dangerous_roots)


def structural_errors(path: Path) -> list[dict[str, object]]:
    rel = path.relative_to(ROOT).as_posix()
    lines = text(path).splitlines()
    issues: list[dict[str, object]] = []
    depth = 0
    top_level_keys: dict[str, int] = {}
    check_duplicates = _is_dangerous_for_top_level_duplicates(path)

    for line_number, raw_line in enumerate(lines, start=1):
        if raw_line.startswith(("<<<<<<<", "=======", ">>>>>>>")):
            issues.append(_issue(rel, line_number, "MERGE_CONFLICT_MARKER", "found git merge conflict marker", f"python3 scripts/resolve_content_conflicts.py --file {rel}"))

        line = _strip_comment(raw_line)
        if check_duplicates and depth == 0:
            match = re.match(r"^\s*([A-Za-z0-9_.:\-]+)\s*=\s*\{", line)
            if match:
                key = match.group(1)
                first_seen = top_level_keys.get(key)
                if first_seen is None:
                    top_level_keys[key] = line_number
                else:
                    issues.append(_issue(rel, line_number, "DUPLICATE_TOP_LEVEL_KEY", f"duplicate top-level key '{key}' (first seen near line {first_seen})", f"Edit {rel} and keep only one '{key} = {{ ... }}' block"))

        depth += line.count("{") - line.count("}")
        if depth < 0:
            issues.append(_issue(rel, line_number, "UNBALANCED_BRACES_CLOSE", "found '}' without matching '{' earlier in file", f"Edit {rel} around line {line_number} to balance braces"))
            depth = 0

    if depth != 0:
        issues.append(_issue(rel, None, "UNBALANCED_BRACES_NET", f"braces look unbalanced (net open braces: {depth})", f"Edit {rel} and balance opening/closing braces"))

    return issues


def run_profile(profile_path: Path) -> tuple[int, list[dict[str, object]], str]:
    data = json.loads(profile_path.read_text(encoding="utf-8"))
    name = data.get("name", profile_path.stem)
    require = data.get("require_patterns", [])
    require_all = data.get("require_all_patterns", [])
    forbid = data.get("forbid_patterns", [])
    structural_checks = data.get("structural_checks", [])

    issues: list[dict[str, object]] = []

    for item in require:
        desc = item["description"]
        pattern_raw = item["pattern"]
        try:
            pattern = re.compile(pattern_raw, re.MULTILINE)
        except re.error as ex:
            issues.append(_issue(profile_path.relative_to(ROOT).as_posix(), None, "INVALID_REQUIRE_REGEX", f"require '{desc}' has invalid regex: {ex}", "Fix regex in smoke profile JSON"))
            continue
        paths = [ROOT / p for p in item["paths"]]
        matched = False
        for p in paths:
            if not p.exists():
                issues.append(_issue(p.relative_to(ROOT).as_posix(), None, "MISSING_REQUIRED_FILE", f"require '{desc}': missing file", f"Create {p.relative_to(ROOT).as_posix()} or remove it from profile"))
                continue
            if pattern.search(text(p)):
                matched = True
        if not matched:
            target = item["paths"][0] if item.get("paths") else profile_path.relative_to(ROOT).as_posix()
            issues.append(_issue(str(target), None, "REQUIRED_PATTERN_NOT_FOUND", f"require '{desc}': pattern not found in listed files", "Implement required content or adjust smoke profile"))

    for item in require_all:
        desc = item["description"]
        pattern_list = item["patterns"]
        paths = [ROOT / p for p in item["paths"]]
        existing_paths = [p for p in paths if p.exists()]
        for p in paths:
            if not p.exists():
                issues.append(_issue(p.relative_to(ROOT).as_posix(), None, "MISSING_REQUIRE_ALL_FILE", f"require_all '{desc}': missing file", f"Create {p.relative_to(ROOT).as_posix()} or remove it from profile"))
        for sub_idx, pattern_raw in enumerate(pattern_list, start=1):
            try:
                pattern = re.compile(pattern_raw, re.MULTILINE)
            except re.error as ex:
                issues.append(_issue(profile_path.relative_to(ROOT).as_posix(), None, "INVALID_REQUIRE_ALL_REGEX", f"require_all '{desc}' subpattern #{sub_idx} invalid regex: {ex}", "Fix regex in smoke profile JSON"))
                continue
            if not any(pattern.search(text(p)) for p in existing_paths):
                target = item["paths"][0] if item.get("paths") else profile_path.relative_to(ROOT).as_posix()
                issues.append(_issue(str(target), None, "REQUIRE_ALL_SUBPATTERN_NOT_FOUND", f"require_all '{desc}': subpattern #{sub_idx} not found", "Implement required content or adjust smoke profile"))

    for item in forbid:
        desc = item["description"]
        pattern_raw = item["pattern"]
        try:
            pattern = re.compile(pattern_raw, re.MULTILINE)
        except re.error as ex:
            issues.append(_issue(profile_path.relative_to(ROOT).as_posix(), None, "INVALID_FORBID_REGEX", f"forbid '{desc}' has invalid regex: {ex}", "Fix regex in smoke profile JSON"))
            continue
        for rel in item["paths"]:
            p = ROOT / rel
            if not p.exists():
                issues.append(_issue(rel, None, "MISSING_FORBID_FILE", f"forbid '{desc}': missing file", f"Create {rel} or remove it from profile"))
                continue
            if pattern.search(text(p)):
                issues.append(_issue(rel, None, "FORBIDDEN_PATTERN_FOUND", f"forbid '{desc}': forbidden pattern found", f"Remove forbidden pattern from {rel}"))

    for rel_path in structural_checks:
        p = ROOT / rel_path
        if not p.exists():
            issues.append(_issue(rel_path, None, "MISSING_STRUCTURAL_FILE", "structural check target file is missing", f"Create {rel_path} or remove it from profile"))
            continue
        issues.extend(structural_errors(p))

    return (1 if issues else 0), issues, name


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", required=True, help="Path to JSON smoke profile")
    ap.add_argument("--format", choices=("text", "json"), default="text")
    args = ap.parse_args()

    code, issues, name = run_profile(ROOT / args.profile)
    if args.format == "json":
        print(json.dumps({"check": CHECK_NAME, "profile": name, "status": "failed" if issues else "passed", "issues": issues}, indent=2))
        return code

    print(f"Running smoke profile: {name}")
    if issues:
        print("Smoke profile failed:")
        for e in issues:
            where = f"{e['file']}:{e['line']}" if e["line"] else e["file"]
            print(f" - [{e['code']}] {where} - {e['message']}")
        return 1

    print("Smoke profile passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
