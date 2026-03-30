#!/usr/bin/env python3
"""Audit EU4 localisation files for beginner mistakes.

Checks implemented:
1. UTF-8 BOM on target files.
2. Presence of a language header (for example: l_english:).
3. Duplicate localisation keys across scanned files.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FILES = [
    "localisation/Flavour_Verne_A33_l_english.yml",
]
HEADER_RE = re.compile(r"^\s*l_[a-z_]+:\s*$")
KEY_RE = re.compile(r'^\s*([^#\s][^:]*)\s*:\s*\d+\s+"')


def audit_file(root: Path, rel_path: Path, key_index: dict[str, list[str]], errors: list[str]) -> None:
    path = root / rel_path
    data = path.read_bytes()
    if not data.startswith(b"\xef\xbb\xbf"):
        errors.append(f"{rel_path}: expected UTF-8 BOM (use UTF-8 with BOM)")

    text = data.decode("utf-8-sig", errors="replace")
    lines = text.splitlines()

    first_non_empty = next((line for line in lines if line.strip()), "")
    if not HEADER_RE.match(first_non_empty):
        errors.append(f"{rel_path}: missing/invalid localisation header (expected e.g. 'l_english:')")

    for line_no, line in enumerate(lines, start=1):
        m = KEY_RE.match(line)
        if not m:
            continue
        key = m.group(1).strip()
        key_index[key].append(f"{rel_path}:{line_no}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file",
        action="append",
        dest="files",
        help="Localisation file relative to repo root (repeatable).",
    )
    args = parser.parse_args()

    file_list = args.files if args.files else DEFAULT_FILES
    targets = [ROOT / p for p in file_list]

    errors: list[str] = []
    key_index: dict[str, list[str]] = defaultdict(list)

    for path in targets:
        if not path.exists():
            errors.append(f"missing file: {path.relative_to(ROOT)}")
            continue
        if path.suffix.lower() != ".yml":
            errors.append(f"{path.relative_to(ROOT)}: expected .yml localisation file")
            continue
        audit_file(ROOT, path.relative_to(ROOT), key_index, errors)

    for key, occurrences in sorted(key_index.items()):
        if len(occurrences) > 1:
            joined = ", ".join(occurrences)
            errors.append(f"duplicate localisation key '{key}' found at: {joined}")

    if errors:
        print("Localisation audit failed:")
        for error in errors:
            print(f" - {error}")
        return 1

    print(f"Localisation audit passed: {len(targets)} file(s) scanned, {len(key_index)} keys indexed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
