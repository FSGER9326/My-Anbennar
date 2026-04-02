import re

loc = r'C:\Users\User\Documents\GitHub\My-Anbennar\localisation\verne_overhaul_l_english.yml'
text = open(loc, 'rb').read().decode('utf-8-sig').replace('\r', '')

# Count desc keys (same logic as audit)
descs = set()
for m in re.finditer(r"^\s*([a-z0-9_]+)(_desc)\s*:", text, re.MULTILINE | re.IGNORECASE):
    key = m.group(1).lower()
    descs.add(key)

print(f"Total desc keys found: {len(descs)}")
print()

# Check specific keys
test_keys = ['a33_the_vernman_renaissance', 'a33_avenge_liliac_wars', 'a33_controlled_devastation']
for k in test_keys:
    status = 'FOUND' if k in descs else 'MISSING'
    print(f"  {k}: {status}")

print()
# Show the last 5 desc keys found
sorted_keys = sorted(descs)
print("Last 10 desc keys:", sorted_keys[-10:])
