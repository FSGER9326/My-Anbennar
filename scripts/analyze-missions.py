import re
from collections import defaultdict

with open(r'C:\Users\User\Documents\GitHub\My-Anbennar\missions\Verne_Missions.txt', 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

current_slot = None
current_mission = None
in_req = False
missions = {}

for i, line in enumerate(lines):
    raw = line.rstrip('\n')
    stripped = line.strip()
    
    # Slot container (no indent, e.g. 'A33_first_slot = {')
    if not line.startswith('\t') and not line.startswith(' ') and re.match(r'^\w+\s*=\s*\{\s*$', line):
        for j in range(i+1, min(i+10, len(lines))):
            if 'slot' in lines[j] and '=' in lines[j]:
                m = re.search(r'slot\s*=\s*(\d+)', lines[j])
                if m:
                    current_slot = int(m.group(1))
                break
    
    # Mission definition (one tab + name + = + {)
    mission_m = re.match(r'^\t(\w+)\s*=\s*\{\s*$', line)
    if mission_m:
        current_mission = mission_m.group(1)
        missions[current_mission] = {'slot': current_slot, 'requires': [], 'position': None}
        in_req = False
        continue
    
    # Position (two tabs) — use raw line for tab detection
    if current_mission and re.match(r'^\t\tposition\s*=', line):
        nums = re.findall(r'\d+', stripped)
        if len(nums) >= 2:
            missions[current_mission]['position'] = (int(nums[0]), int(nums[1]))
    
    # required_missions - could be single line or multi-line
    # Must use raw line (not stripped) because strip() removes tabs
    if current_mission and re.match(r'^\t\trequired_missions\s*=', line):
        # Check if it's single-line: required_missions = { A33_xxx }
        inline = re.findall(r'\{([^}]+)\}', stripped)
        if inline:
            ids = re.findall(r'(\w+)', inline[0])
            missions[current_mission]['requires'].extend(ids)
        else:
            in_req = True
        continue
    
    if in_req:
        ids = re.findall(r'\b(A33_\w+)\b', stripped)
        if ids:
            missions[current_mission]['requires'].extend(ids)
        if '}' in stripped:
            in_req = False

# Filter
skip = {'potential', 'generic', 'has_country_shield'}
missions = {k: v for k, v in missions.items() if k not in skip and len(k) > 3}

# Analysis
has_deps = set()
is_dep_of = set()
for name, data in missions.items():
    for r in data['requires']:
        if r in missions:
            has_deps.add(name)
            is_dep_of.add(r)

orphans = set(missions.keys()) - has_deps - is_dep_of

print(f'Total missions: {len(missions)}')
print(f'With prerequisites: {len(has_deps)}')
print(f'Entry points (no prereqs): {len(set(missions.keys()) - has_deps)}')
print(f'Leaf missions (not required by anything): {len(set(missions.keys()) - is_dep_of)}')
print()

# Print by slot
for slot in sorted(set(v['slot'] for v in missions.values() if v['slot'] is not None)):
    slot_ms = {k: v for k, v in missions.items() if v['slot'] == slot}
    print(f'=== SLOT {slot} ({len(slot_ms)} missions) ===')
    for name, data in sorted(slot_ms.items(), key=lambda x: (x[1]['position'][0] if x[1]['position'] else 999)):
        pos = data['position']
        reqs = data['requires']
        req_str = ' <-- [' + ', '.join(reqs) + ']' if reqs else ''
        print(f'  {name} (pos={pos}){req_str}')
    print()

# Cross-slot deps
print('=== CROSS-SLOT DEPENDENCIES ===')
cross = []
for name, data in missions.items():
    for r in data['requires']:
        if r in missions and missions[r]['slot'] != data['slot'] and data['slot'] is not None and missions[r]['slot'] is not None:
            cross.append((data['slot'], name, missions[r]['slot'], r))
for slot, name, req_slot, req in sorted(cross):
    print(f'  [{slot}] {name} <-- [{req_slot}] {req}')
print(f'Total cross-slot deps: {len(cross)}')
print()

# Dependency chains
def max_depth(m, visited=None):
    if visited is None: visited = set()
    if m in visited or m not in missions: return 0
    visited.add(m)
    if not missions[m]['requires']: return 0
    return 1 + max(max_depth(r, visited.copy()) for r in missions[m]['requires'])

depths = {m: max_depth(m) for m in missions}
print('=== TOP 15 LONGEST DEPENDENCY CHAINS ===')
for m, d in sorted(depths.items(), key=lambda x: -x[1])[:15]:
    chain = [m]
    current = m
    while missions.get(current, {}).get('requires'):
        current = missions[current]['requires'][0]
        chain.append(current)
        if len(chain) > 20: break
    print(f'  depth={d}: {" -> ".join(reversed(chain))}')
print(f'Max depth: {max(depths.values())}')
print()

# Lane connectivity
print('=== LANE CONNECTIVITY ===')
all_lanes = set(v['slot'] for v in missions.values() if v['slot'] is not None)
for slot in sorted(all_lanes):
    out_count = sum(1 for s, _, rs, _ in cross if rs == slot)
    in_count = sum(1 for s, _, rs, _ in cross if s == slot)
    status = []
    if out_count: status.append(f'exports {out_count}')
    if in_count: status.append(f'imports {in_count}')
    if not status: status.append('ISOLATED')
    slot_ms = [k for k, v in missions.items() if v['slot'] == slot]
    print(f'  Lane {slot} ({len(slot_ms)} missions): {", ".join(status)}')

# Missions referencing non-existent missions
print()
print('=== BROKEN REFERENCES ===')
all_ids = set(missions.keys())
for name, data in missions.items():
    for r in data['requires']:
        if r not in all_ids and r not in skip:
            print(f'  {name} requires {r} -- NOT FOUND in mission file')
