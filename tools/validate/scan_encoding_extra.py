#!/usr/bin/env python3
"""
scan_encoding_extra.py — Encoding scanner for folders that upstream
checkEncoding.sh does NOT cover:
  common/, history/, interface/, customizable_localization/, map text/CSV assets

Run AFTER tools/upstream/checkEncoding.sh (which handles localisation, events,
missions, decisions).
"""
import sys
import os
from pathlib import Path

# Folders upstream checkEncoding.sh covers: localisation, events, missions, decisions
# This script covers everything else.
UPSTREAM_COVERED = {'localisation', 'events', 'missions', 'decisions'}

# Files that MUST have UTF-8 BOM
UTF8_BOM_FILES = {'.yml', '.yaml'}

# Files that must NOT have UTF-8 BOM
NO_BOM_FILES = {'.txt', '.gui'}

BOM = b'\xef\xbb\xbf'
SKIPDirs = {'.git', 'node_modules', '__pycache__', '.cwtools'}


def check_file(path: Path) -> list:
    issues = []
    try:
        raw = path.read_bytes()
    except Exception:
        return issues

    is_utf8_bom_file = path.suffix in UTF8_BOM_FILES
    is_no_bom_file = path.suffix in NO_BOM_FILES

    has_bom = raw.startswith(BOM)

    if is_utf8_bom_file and not has_bom:
        issues.append(f"Missing UTF-8 BOM: {path} (required for {path.suffix} files)")
    elif is_no_bom_file and has_bom:
        issues.append(f"Unexpected UTF-8 BOM: {path} (script files must be CP-1252)")

    return issues


def main():
    root = Path(os.environ.get('SCAN_ROOT', '.')).resolve()

    all_issues = []
    for path in root.rglob('*'):
        if path.is_dir():
            continue
        if any(d in path.parts for d in SKIPDirs):
            continue

        # Skip folders already covered by upstream checkEncoding.sh
        rel = path.relative_to(root)
        parts = set(rel.parts)
        if parts & UPSTREAM_COVERED:
            continue

        # Only scan relevant file types
        if path.suffix in {'.txt', '.gui', '.yml', '.yaml'}:
            issues = check_file(path)
            all_issues.extend(issues)

    if all_issues:
        print("ENCODING ISSUES FOUND:")
        for issue in all_issues:
            print(f"  {issue}")
        sys.exit(1)
    else:
        print("scan_encoding_extra: PASS")
        sys.exit(0)


if __name__ == '__main__':
    main()
