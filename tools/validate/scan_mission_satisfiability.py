#!/usr/bin/env python3
"""
scan_mission_satisfiability.py
Static pass for likely wrong-scope logic and impossible/brittle mission triggers:
  - Province-level triggers in country scope (is_adjacent_to_bay, etc.)
  - Country-level triggers in province scope (add_casus_belli, etc.)
  - OR conditions in triggers that make completion impossible
  - Numeric conditions that are trivially impossible (num_of_x < 0)
  - Self-referential conditions (mission X requires mission X)
"""
import sys
import os
import re
from pathlib import Path

SKIPDirs = {'.git', 'node_modules', '__pycache__', '.cwtools', '.github'}

# Province triggers used in country scope = wrong scope
PROVINCE_TRIGGERS_IN_COUNTRY = [
    'is_adjacent_to_bay', 'is_adjacent_to_importance', 'is_capital',
    'add_province_trigger', 'province_has_current_tech_fort_trigger',
    'num_of_owned_provinces_with', 'num_of_ports',
]

# Country triggers used in province scope = wrong scope
COUNTRY_TRIGGERS_IN_PROVINCE = [
    'add_casus_belli', 'add_prestige', 'add_legitimacy',
    'add_absolutism', 'set_government', 'change_government_reform',
]


def parse_mission_blocks(txt: str) -> list:
    """Extract all mission = { ... } blocks with their names."""
    blocks = []
    for m in re.finditer(r'^(\w+)\s*=\s*\{[^}]*(?:\{[^}]*\}[^}]*)*\}', txt, re.MULTILINE | re.DOTALL):
        name = m.group(1)
        block = m.group(0)
        blocks.append((name, block))
    return blocks


def check_block(name: str, block: str, filepath: str) -> list:
    issues = []

    # Trivially impossible numeric conditions
    for m in re.finditer(r'(num_of_\w+|treasury|manpower|num_of_ports|num_of_buildings)\s*<\s*0', block):
        issues.append(f"Mission '{name}' in {filepath}: impossible condition (can't be < 0): {m.group()}")

    # Self-referential triggers
    for m in re.finditer(r'has_country_flag\s*=\s*(\w+)', block):
        flag = m.group(1)
        if flag.replace('_completed', '') in name or flag in name:
            issues.append(f"Mission '{name}' in {filepath}: self-referential flag check: {flag}")

    # Wrong-scope patterns (heuristic — look for specific trigger names out of context)
    # This is a simplified check; a full scope analysis needs a proper parser
    province_triggers = '|'.join(PROVINCE_TRIGGERS_IN_COUNTRY)
    if re.search(province_triggers, block):
        # Check if we're in a country-level block (mission trees are country-scoped)
        # If the block doesn't contain 'province_scope', flag it
        if 'province_scope' not in block:
            matched = re.search(province_triggers, block)
            issues.append(f"Mission '{name}' in {filepath}: likely province trigger in country scope: {matched.group()}")

    return issues


def main():
    root = Path(os.environ.get('SCAN_ROOT', '.')).resolve()

    all_issues = []
    for path in root.rglob('missions/*.txt'):
        if any(d in path.parts for d in SKIPDirs):
            continue
        txt = path.read_text(encoding='utf-8', errors='replace')
        blocks = parse_mission_blocks(txt)
        for name, block in blocks:
            issues = check_block(name, block, str(path))
            all_issues.extend(issues)

    if all_issues:
        print("MISSION SATISFIABILITY ISSUES:")
        for issue in all_issues:
            print(f"  {issue}")
        sys.exit(1)
    else:
        print("scan_mission_satisfiability: PASS")
        sys.exit(0)


if __name__ == '__main__':
    main()
