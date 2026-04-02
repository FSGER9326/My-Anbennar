#!/usr/bin/env python3
"""
scan_country_tag_pairs.py
For every country tag in common/country_tags/, verify that the corresponding
files exist:
  - common/countries/<Name>.txt
  - history/countries/<TAG>.txt  OR  history/countries/<TAG> - <Name>.txt
  - gfx/flags/<TAG>.tga
  - localisation entries (optional scan)

Missing any pair = game crash risk at launch.
"""
import sys
import os
import re
from pathlib import Path

SKIPDirs = {'.git', 'node_modules', '__pycache__', '.cwtools', '.github'}


def parse_tag_file(path: Path) -> list:
    """Extract tag entries from a country_tags/*.txt file."""
    tags = []
    try:
        txt = path.read_text(encoding='utf-8', errors='replace')
    except Exception:
        return tags
    for m in re.finditer(r'^\s*(\w{3})\s*=\s*"([^"]+)"', txt, re.MULTILINE):
        tags.append((m.group(1), m.group(2)))
    return tags


def check_tag(tag: str, country_file_path: str, root: Path) -> list:
    issues = []
    country_file = root / country_file_path
    if not country_file.exists():
        issues.append(f"Tag {tag}: missing country file: {country_file_path}")

    # History file: try both naming conventions
    hist_a = root / 'history' / 'countries' / f'{tag}.txt'
    hist_b = root / 'history' / 'countries' / f'{tag} - {Path(country_file_path).stem}.txt'
    if not hist_a.exists() and not hist_b.exists():
        issues.append(f"Tag {tag}: missing history file (tried {tag}.txt and 'tag - name.txt')")

    # Flag file
    flag = root / 'gfx' / 'flags' / f'{tag}.tga'
    if not flag.exists():
        issues.append(f"Tag {tag}: missing flag: gfx/flags/{tag}.tga")

    return issues


def main():
    root = Path(os.environ.get('SCAN_ROOT', '.')).resolve()
    tag_dir = root / 'common' / 'country_tags'
    if not tag_dir.exists():
        print("scan_country_tag_pairs: SKIP — no common/country_tags/")
        sys.exit(0)

    all_issues = []
    for tag_file in sorted(tag_dir.glob('*.txt')):
        if any(d in tag_file.parts for d in SKIPDirs):
            continue
        tags = parse_tag_file(tag_file)
        for tag, country_path in tags:
            issues = check_tag(tag, country_path, root)
            all_issues.extend(issues)

    if all_issues:
        print("COUNTRY TAG PAIR ISSUES:")
        for issue in all_issues:
            print(f"  {issue}")
        sys.exit(1)
    else:
        print("scan_country_tag_pairs: PASS")
        sys.exit(0)


if __name__ == '__main__':
    main()
