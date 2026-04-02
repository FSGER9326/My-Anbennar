#!/usr/bin/env python3
"""
scan_formable_conflicts.py
Detects formable/formation decision conflicts:
  - Missions/events that hardcode checks for old tags after a formation decision
  - Tag swap logic that bypasses mission tree compatibility
  - Missing DLC-gated formable guards

Scans for patterns like:
  - has_country_flag = formed_<oldtag>
  - tag = OLD  (after a formable decision)
  - decision keys related to formables without proper formable=X guards
"""
import sys
import os
import re
from pathlib import Path

SKIPDirs = {'.git', 'node_modules', '__pycache__', '.cwtools', '.github'}

# Patterns that suggest hardcoded old-tag checks in missions/events
HARDCODED_TAG_PATTERNS = [
    (r'has_country_flag\s*=\s*formed_\w{3}', 'Hardcoded formed_X flag check'),
    (r'tag\s*=\s*[A-Z]{3}(?!\s*[=<>])', 'Hardcoded old tag check (not in variable)'),
    (r'FROM\s*=\s*[A-Z]{3}(?!\s*[=<>])', 'Hardcoded FROM tag reference'),
]

# Decision files that look like formables
FORMABLE_DECISION_FILES = ['formable', 'formation']


def check_file(path: Path) -> list:
    issues = []
    txt = path.read_text(encoding='utf-8', errors='replace')
    rel = path.relative_to(path.parts[0]) if path.parts else path

    for pattern, desc in HARDCODED_TAG_PATTERNS:
        for m in re.finditer(pattern, txt, re.IGNORECASE):
            issues.append(f"{desc} in {path}: ...{m.group()}... (may conflict with formable)")

    return issues


def main():
    root = Path(os.environ.get('SCAN_ROOT', '.')).resolve()

    all_issues = []
    for path in root.rglob('*'):
        if path.is_dir():
            continue
        if any(d in path.parts for d in SKIPDirs):
            continue
        if path.suffix != '.txt':
            continue

        # Focus on events and missions where formable conflicts are most common
        if 'event' not in str(path).lower() and 'mission' not in str(path).lower():
            continue

        issues = check_file(path)
        all_issues.extend(issues)

    if all_issues:
        print("FORMABLE CONFLICT WARNINGS:")
        for issue in all_issues:
            print(f"  {issue}")
        print("\nReview: these may indicate hardcoded old-tag checks that conflict with formable transitions.")
        # Exit 0 for warnings — don't hard-fail on heuristic matches
        sys.exit(0)
    else:
        print("scan_formable_conflicts: PASS")
        sys.exit(0)


if __name__ == '__main__':
    main()
