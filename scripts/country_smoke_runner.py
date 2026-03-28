#!/usr/bin/env python3
"""Run profile-based smoke checks for a country/workstream."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _strip_comment(line: str) -> str:
    in_quote = False
    out: list[str] = []
    i = 0
    while i < len(line):
        ch = line[i]
        if ch == '"':
            in_quote = not in_quote
            out.append(ch)
            i += 1
            continue
        if ch == "#" and not in_quote:
            break
        out.append(ch)
        i += 1
    return "".join(out)


def _is_dangerous_for_top_level_duplicates(path: Path) -> bool:
    rel = path.as_posix()
    dangerous_roots = (
        "common/scripted_effects/",
        "common/scripted_triggers/",
        "common/decisions/",
        "common/modifiers/",
    )
    return rel.endswith(".txt") and any(root in rel for root in dangerous_roots)


def structural_errors(path: Path) -> list[str]:
    rel = path.relative_to(ROOT)
    lines = text(path).splitlines()
    errors: list[str] = []

    depth = 0
    top_level_keys: dict[str, int] = {}
    check_duplicates = _is_dangerous_for_top_level_duplicates(path)

    for line_number, raw_line in enumerate(lines, start=1):
        if raw_line.startswith(("<<<<<<<", "=======", ">>>>>>>")):
            errors.append(
                f"In {rel} around line {line_number}: found a git merge conflict marker "
                "(<<<<<<<, =======, or >>>>>>>). Please resolve the conflict and remove markers."
            )

        line = _strip_comment(raw_line)
        opens = line.count("{")
        closes = line.count("}")

        if check_duplicates and depth == 0:
            match = re.match(r"^\s*([A-Za-z0-9_.:\-]+)\s*=\s*\{", line)
            if match:
                key = match.group(1)
                first_seen = top_level_keys.get(key)
                if first_seen is None:
                    top_level_keys[key] = line_number
                else:
                    errors.append(
                        f"In {rel} around line {line_number}: duplicate top-level key '{key}'. "
                        f"It was first defined around line {first_seen}. "
                        "This can silently overwrite logic in scripted files."
                    )

        depth += opens - closes
        if depth < 0:
            errors.append(
                f"In {rel} around line {line_number}: found '}}' without matching '{{' earlier in the file."
            )
            depth = 0

    if depth != 0:
        errors.append(
            f"In {rel}: braces look unbalanced (net open braces: {depth}). "
            "Check for a missing '{' or '}' near the end of the file."
        )

    return errors


def run_profile(profile_path: Path) -> int:
    data = json.loads(profile_path.read_text(encoding="utf-8"))
    name = data.get("name", profile_path.stem)
    require = data.get("require_patterns", [])
    require_all = data.get("require_all_patterns", [])
    forbid = data.get("forbid_patterns", [])
    structural_checks = data.get("structural_checks", [])

    print(f"Running smoke profile: {name}")
    errors: list[str] = []

    step = 0
    for item in require:
        step += 1
        desc = item["description"]
        pattern_raw = item["pattern"]
        try:
            pattern = re.compile(pattern_raw, re.MULTILINE)
        except re.error as ex:
            errors.append(
                f"profile '{name}' ({profile_path.relative_to(ROOT)}), section 'require', "
                f"item '{desc}': invalid regex {ex}; pattern={pattern_raw!r}"
            )
            continue
        paths = [ROOT / p for p in item["paths"]]
        print(f"[{step}] require: {desc}")
        matched = False
        for p in paths:
            if not p.exists():
                errors.append(f"require '{desc}': missing file {p.relative_to(ROOT)}")
                continue
            if pattern.search(text(p)):
                matched = True
        if not matched:
            errors.append(f"require '{desc}': pattern not found in any listed file")

    for item in require_all:
        step += 1
        desc = item["description"]
        pattern_list = item["patterns"]
        paths = [ROOT / p for p in item["paths"]]
        print(f"[{step}] require_all: {desc}")
        existing_paths: list[Path] = []
        for p in paths:
            if not p.exists():
                errors.append(f"require_all '{desc}': missing file {p.relative_to(ROOT)}")
                continue
            existing_paths.append(p)

        for sub_idx, pattern_raw in enumerate(pattern_list, start=1):
            try:
                pattern = re.compile(pattern_raw, re.MULTILINE)
            except re.error as ex:
                errors.append(
                    f"profile '{name}' ({profile_path.relative_to(ROOT)}), section 'require_all', "
                    f"item '{desc}', subpattern #{sub_idx}: invalid regex {ex}; pattern={pattern_raw!r}"
                )
                continue

            matched = False
            for p in existing_paths:
                if pattern.search(text(p)):
                    matched = True
            if not matched:
                errors.append(
                    f"require_all '{desc}': subpattern #{sub_idx} not found in any listed file; "
                    f"pattern={pattern_raw!r}"
                )

    for item in forbid:
        step += 1
        desc = item["description"]
        pattern_raw = item["pattern"]
        try:
            pattern = re.compile(pattern_raw, re.MULTILINE)
        except re.error as ex:
            errors.append(
                f"profile '{name}' ({profile_path.relative_to(ROOT)}), section 'forbid', "
                f"item '{desc}': invalid regex {ex}; pattern={pattern_raw!r}"
            )
            continue
        paths = [ROOT / p for p in item["paths"]]
        print(f"[{step}] forbid: {desc}")
        for p in paths:
            if not p.exists():
                errors.append(f"forbid '{desc}': missing file {p.relative_to(ROOT)}")
                continue
            if pattern.search(text(p)):
                errors.append(f"forbid '{desc}': forbidden pattern found in {p.relative_to(ROOT)}")

    if structural_checks:
        step += 1
        print(f"[{step}] structural: lightweight scripted-file checks")
        for rel_path in structural_checks:
            p = ROOT / rel_path
            if not p.exists():
                errors.append(f"structural check: missing file {p.relative_to(ROOT)}")
                continue
            errors.extend(structural_errors(p))

    if errors:
        print("Smoke profile failed:")
        for e in errors:
            print(f" - {e}")
        return 1

    print("Smoke profile passed.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", required=True, help="Path to JSON smoke profile")
    args = ap.parse_args()
    return run_profile(ROOT / args.profile)


if __name__ == "__main__":
    sys.exit(main())
