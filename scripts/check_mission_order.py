"""Check for out-of-order mission prerequisites.

NOTE: In EU4 mission trees, "position" is the visual slot number (left-to-right column
placement), NOT the completion order. A mission at pos=12 can legitimately require a
mission at pos=13 if the tree design calls for non-linear or parallel paths.
Only flag truly problematic backward chains where the prerequisite position implies
an impossible unlock order given the tree structure.
"""
import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MISSION_FILE = os.path.join(SCRIPT_DIR, '..', 'missions', 'Verne_Missions.txt')

with open(MISSION_FILE, 'r', encoding='utf-8') as f:
    content = f.read()
lines = content.split('\n')

missions = {}
in_block = False
brace_depth = 0

for i, line in enumerate(lines):
    raw_indent = len(line) - len(line.lstrip())
    stripped = line.strip()
    if raw_indent == 1 and stripped.startswith('A33_') and stripped.endswith(' = {'):
        key = stripped.split(' = ')[0].strip()
        block = '\n'.join(lines[i:i + 80])
        reqs = re.findall(r'required_missions\s*=\s*\{([^}]+)\}', block)
        req_list = re.findall(r'A33_[A-Za-z_0-9]+', reqs[0]) if reqs else []
        pos = re.findall(r'position\s*=\s*(\d+)', block)
        p = int(pos[0]) if pos else -1
        missions[key] = {'pos': p, 'reqs': req_list, 'line': i + 1}
        in_block = True
        brace_depth = 1
        continue
    if in_block:
        brace_depth += stripped.count('{') - stripped.count('}')
        if brace_depth <= 0:
            in_block = False
            brace_depth = 0

out_of_order = []
for k, v in missions.items():
    for r in v['reqs']:
        if r in missions:
            req_pos = missions[r]['pos']
            # Flag if required mission has same or higher position (implies equal-or-later slot)
            if req_pos >= v['pos']:
                out_of_order.append((k, v['pos'], r, req_pos))

if out_of_order:
    print('OUT OF ORDER REQUISITES (requires manual review):')
    for row in sorted(out_of_order):
        print(f'  {row[0]}(pos={row[1]}) requires {row[2]}(pos={row[3]})')
else:
    print('No out-of-order prerequisites')
