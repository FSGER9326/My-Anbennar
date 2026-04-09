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
        print(f"SLOT HEADER at line {i+1}: {stripped[:60]}")
        continue
    if raw_indent == 1 and stripped.startswith('A33_') and stripped.endswith(' = {'):
        key = stripped.split(' = ')[0].strip()
        missions[key] = {'reqs': [], 'required_by': [], 'line': i+1}
        in_mission = True
        depth = 1
        print(f"  MISSION at line {i+1}: {key}")
        continue
    if in_mission:
        depth += stripped.count('{') - stripped.count('}')
        if depth <= 0:
            in_mission = False

print(f"\nTotal missions found: {len(missions)}")
key1 = 'A33_might_of_the_wyvern'
key2 = 'A33_might_of_wyvern'
print(f"{key1}: {'FOUND at line '+str(missions[key1]['line']) if key1 in missions else 'NOT FOUND'}")
print(f"{key2}: {'FOUND at line '+str(missions[key2]['line']) if key2 in missions else 'NOT FOUND'}")
