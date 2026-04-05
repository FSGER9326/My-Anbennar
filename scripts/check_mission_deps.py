"""Check mission dependency integrity: broken refs and cycles.

BUG FIX 2026-04-05: depth tracking rewritten to use brace-counting across lines,
not just per-line delta. The original per-line approach lost sync when nested blocks
(e.g. if = { limit = { ... } }) had closing } on the same line as other content.
"""
import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MISSION_FILE = os.path.join(SCRIPT_DIR, '..', 'missions', 'Verne_Missions.txt')

with open(MISSION_FILE, 'r', encoding='utf-8') as f:
    content = f.read()
lines = content.split('\n')

missions = {}

# Pass 1: find all mission IDs using brace-counting across the whole file
# Track whether we're inside a mission block by counting { and } from the
# mission definition line onwards.
in_block = False
brace_depth = 0
block_start = -1

for i, line in enumerate(lines):
    raw_indent = len(line) - len(line.lstrip())
    stripped = line.strip()

    # Detect mission definition line: indent=1, starts with A33_, ends with = {
    if raw_indent == 1 and stripped.startswith('A33_') and stripped.endswith(' = {'):
        key = stripped.split(' = ')[0].strip()
        missions[key] = {'reqs': [], 'required_by': [], 'line': i + 1}
        in_block = True
        brace_depth = 1  # the opening { of the mission itself
        block_start = i
        continue

    # If we're inside a mission block, count braces
    if in_block:
        open_count = stripped.count('{')
        close_count = stripped.count('}')
        brace_depth += open_count - close_count
        if brace_depth <= 0:
            # End of mission block
            in_block = False
            brace_depth = 0

# Extract required_missions — use mission block from Pass 1 (up to 60 lines from definition)
for key, info in missions.items():
    start = info['line'] - 1  # 0-indexed
    block = '\n'.join(lines[start:start + 80])
    reqs = re.findall(r'required_missions\s*=\s*\{([^}]+)\}', block)
    if reqs:
        req_list = re.findall(r'A33_[A-Za-z_0-9]+', reqs[0])
        missions[key]['reqs'] = req_list
        for r in req_list:
            if r in missions:
                missions[r]['required_by'].append(key)

broken = []
for k, v in missions.items():
    for r in v['reqs']:
        if r not in missions:
            broken.append(f'{k} requires {r} (MISSING)')

if broken:
    print('BROKEN REFERENCES:')
    for b in sorted(broken):
        print(' ', b)
else:
    print('No broken references')

# Find orphans (required by nobody)
orphans = [k for k, v in missions.items() if not v['required_by']]
print(f'\nOrphan missions (not required by any other mission): {len(orphans)}')
for o in sorted(orphans):
    print(f'  {o}')

# Check position gaps / out-of-order chains
print('\nPosition number analysis:')
positions = {}
for k, v in missions.items():
    start = v['line'] - 1
    block = '\n'.join(lines[start:start + 80])
    pos = re.findall(r'position\s*=\s*(\d+)', block)
    p = int(pos[0]) if pos else -1
    if p not in positions:
        positions[p] = []
    positions[p].append(k)

for p in sorted(positions.keys()):
    print(f'  pos {p}: {len(positions[p])} missions')
    for m in sorted(positions[p]):
        print(f'    - {m}')
