"""Check for out-of-order mission prerequisites."""
import re

with open('missions/Verne_Missions.txt', 'r', encoding='utf-8') as f:
    content = f.read()
lines = content.split('\n')

missions = {}
in_mission = False
depth = 0

for i, line in enumerate(lines):
    stripped = line.strip()
    raw_indent = len(line) - len(line.lstrip())
    if raw_indent == 0 and stripped.startswith('A33_') and 'slot' in stripped and '=' in stripped:
        in_mission = True
        depth = 1
        continue
    if raw_indent == 1 and stripped.startswith('A33_') and stripped.endswith(' = {'):
        key = stripped.split(' = ')[0].strip()
        block = '\n'.join(lines[i:i+60])
        reqs = re.findall(r'required_missions\s*=\s*\{([^}]+)\}', block)
        req_list = re.findall(r'A33_[A-Za-z_0-9]+', reqs[0]) if reqs else []
        pos = re.findall(r'position\s*=\s*(\d+)', block)
        p = int(pos[0]) if pos else -1
        missions[key] = {'pos': p, 'reqs': req_list}
        in_mission = True
        depth = 1
        continue
    if in_mission:
        depth += stripped.count('{') - stripped.count('}')
        if depth <= 0:
            in_mission = False

out_of_order = []
for k, v in missions.items():
    for r in v['reqs']:
        if r in missions:
            req_pos = missions[r]['pos']
            if req_pos >= v['pos']:
                out_of_order.append((k, v['pos'], r, req_pos))

if out_of_order:
    print('OUT OF ORDER REQUISITES:')
    for row in sorted(out_of_order):
        print(f'  {row[0]}(pos={row[1]}) requires {row[2]}(pos={row[3]})')
else:
    print('No out-of-order prerequisites')
