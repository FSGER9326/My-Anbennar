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


def run_profile(profile_path: Path) -> int:
    data = json.loads(profile_path.read_text(encoding="utf-8"))
    name = data.get("name", profile_path.stem)
    require = data.get("require_patterns", [])
    forbid = data.get("forbid_patterns", [])

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
