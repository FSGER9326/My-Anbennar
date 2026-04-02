#!/usr/bin/env python3
"""
scan_dlc_softlocks.py
Detects DLC-gated mission/decisions that lack a fallback path:
  - Mission triggers that require DLC-linked estate privileges
  - Decisions that assume DLC-gated mechanics are always available
  - Missing has_dlc guards around DLC-specific content

Flags as potential softlock risks.
"""
import sys
import os
import re
from pathlib import Path

SKIPDirs = {'.git', 'node_modules', '__pycache__', '.cwtools', '.github'}

# Known DLC-gated estate privileges, reforms, mechanics
DLC_ESTATE_PRIVILEGES = [
    r'estate_\w+_Privileges',  # estate privilege chains
    r'estate_privilege',
]

# Patterns that suggest DLC-dependent logic without guard
DLC_WITHOUT_GUARD = [
    (r'(?!has_dlc)', ''),  # placeholder — actual scan is below
]


def check_mission_file(path: Path) -> list:
    issues = []
    txt = path.read_text(encoding='utf-8', errors='replace')

    # Find mission blocks with potential/trigger sections
    # If a trigger references estate mechanics but has no has_dlc guard, flag it
    in_trigger = False
    trigger_depth = 0
    lines = txt.split('\n')

    for i, line in enumerate(lines):
        stripped = line.strip()
        if re.match(r'^\s*(potential|trigger|allow)\s*=', stripped):
            in_trigger = True
            trigger_depth = 0
            continue
        if in_trigger:
            if '{' in line:
                trigger_depth += line.count('{')
            if '}' in line:
                trigger_depth -= line.count('}')
            if trigger_depth <= 0:
                in_trigger = False
            # Check for estate references without has_dlc nearby
            if re.search(r'estate_(?!has_dlc)', stripped):
                # Look ahead for has_dlc within next 5 lines
                lookahead = '\n'.join(lines[i:i+6])
                if not re.search(r'has_dlc', lookahead):
                    issues.append(f"{path}:{i+1}: estate reference without has_dlc guard")

    return issues


def check_decision_file(path: Path) -> list:
    issues = []
    txt = path.read_text(encoding='utf-8', errors='replace')

    # Check if a decision has DLC-relevant effects (estate, government reforms)
    # but no has_dlc in potential/allow
    blocks = re.split(r'^(\w+)\s*=\s*\{', txt, flags=re.MULTILINE)
    for i in range(1, len(blocks), 2):
        dec_name = blocks[i].strip()
        block = blocks[i+1] if i+1 < len(blocks) else ''
        if re.search(r'estate_|government_reform', block):
            if not re.search(r'has_dlc', block[:500]):  # check potential/allow section
                issues.append(f"Decision '{dec_name}' in {path}: DLC/estate logic without has_dlc guard")

    return issues


def main():
    root = Path(os.environ.get('SCAN_ROOT', '.')).resolve()

    all_issues = []
    for path in root.rglob('missions/*.txt'):
        if any(d in path.parts for d in SKIPDirs):
            continue
        all_issues.extend(check_mission_file(path))

    for path in root.rglob('decisions/*.txt'):
        if any(d in path.parts for d in SKIPDirs):
            continue
        all_issues.extend(check_decision_file(path))

    if all_issues:
        print("DLC SOFTLOCK WARNINGS:")
        for issue in all_issues:
            print(f"  {issue}")
        print("\nReview: add has_dlc guards or fallback paths for DLC-gated content.")
        sys.exit(0)  # Warnings only
    else:
        print("scan_dlc_softlocks: PASS")
        sys.exit(0)


if __name__ == '__main__':
    main()
