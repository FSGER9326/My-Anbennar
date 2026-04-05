"""Check mission dependency integrity: broken refs and cycles."""
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
        missions[key] = {'reqs': [], 'required_by': []}
        in_mission = True
        depth = 1
        continue
    if in_mission:
        depth += stripped.count('{') - stripped.count('}')
        if depth <= 0:
            in_mission = False

# Extract required_missions
for i, line in enumerate(lines):
    stripped = line.strip()
    raw_indent = len(line) - len(line.lstrip())
    if raw_indent == 1 and stripped.startswith('A33_') and stripped.endswith(' = {'):
        key = stripped.split(' = ')[0].strip()
        block = '\n'.join(lines[i:i+60])
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
    # Extract position
    idx = lines.index(next(l for l in lines if l.strip().startswith(k + ' = {')))
    block = '\n'.join(lines[idx:idx+60])
    pos = re.findall(r'position\s*=\s*(\d+)', block)
    p = int(pos[0]) if pos else -1
    if p not in positions:
        positions[p] = []
    positions[p].append(k)

for p in sorted(positions.keys()):
    print(f'  pos {p}: {len(positions[p])} missions')
    for m in sorted(positions[p]):
        print(f'    - {m}')
