"""Mission integrity audit: flags, modifiers, triggers, loc."""
import re
import os

MISSIONS = r"C:\Users\User\Documents\GitHub\My-Anbennar\missions\Verne_Missions.txt"
TRIGGERS = r"C:\Users\User\Documents\GitHub\My-Anbennar\common\scripted_triggers\verne_overhaul_triggers.txt"
EFFECTS  = r"C:\Users\User\Documents\GitHub\My-Anbennar\common\scripted_effects\verne_overhaul_effects.txt"
MODS     = r"C:\Users\User\Documents\GitHub\My-Anbennar\common\event_modifiers\verne_overhaul_modifiers.txt"
LOC      = r"C:\Users\User\Documents\GitHub\My-Anbennar\localisation\verne_overhaul_l_english.yml"

def read(path):
    with open(path, 'rb') as f:
        return f.read().decode('utf-8-sig').replace('\r', '')

def get_namespaced(path, prefix):
    text = read(path)
    return {m.group(1).lower() for m in re.finditer(rf'^\s*({re.escape(prefix)}\S+)\s*=', text, re.MULTILINE)}

def get_flags_set_in_missions():
    text = read(MISSIONS)
    # set_country_flag = flagname, set_global_flag = flagname
    flags = set()
    for m in re.finditer(r'set_(?:country|global)_flag\s*=\s*(\w+)', text):
        flags.add(m.group(1).lower())
    return flags

def get_flags_checked_in_missions():
    text = read(MISSIONS)
    # has_country_flag = flagname, has_global_flag = flagname
    flags = set()
    for m in re.finditer(r'has_(?:country|global)_flag\s*=\s*(\w+)', text):
        flags.add(m.group(1).lower())
    return flags

def get_modifiers_used_in_missions():
    text = read(MISSIONS)
    mods = set()
    for m in re.finditer(r'add_(?:country|province)_modifier\s*=\s*\{\s*name\s*=\s*"(\w+)"', text):
        mods.add(m.group(1).lower())
    return mods

def get_modifiers_defined():
    text = read(MODS)
    mods = set()
    for m in re.finditer(r'^\s*(\w+)\s*=\s*\{', text, re.MULTILINE):
        mods.add(m.group(1).lower())
    return mods

def get_trigger_names():
    text = read(TRIGGERS)
    names = set()
    for m in re.finditer(r'^\s*(verne_\w+)\s*=\s*\{', text, re.MULTILINE):
        names.add(m.group(1).lower())
    return names

def get_effect_names():
    text = read(EFFECTS)
    names = set()
    for m in re.finditer(r'^\s*(verne_\w+)\s*=\s*\{', text, re.MULTILINE):
        names.add(m.group(1).lower())
    return names

def get_mission_ids():
    text = read(MISSIONS)
    ids = set()
    # Real missions have indent=1 inside slot blocks (not slot declarations)
    in_slot = False
    for line in text.split('\n'):
        stripped = line.strip()
        if stripped.startswith('A33_') and '=' in stripped and '{' in stripped:
            if not in_slot:
                ids.add(stripped.split('=')[0].strip().lower())
            else:
                if 'slot' in stripped or stripped.startswith('#'):
                    continue
                ids.add(stripped.split('=')[0].strip().lower())
        if 'slot' in stripped and '=' in stripped:
            in_slot = True
        if stripped == '}':
            if in_slot:
                depth = len(line) - len(line.lstrip('\t'))
                if depth == 0:
                    in_slot = False
    return ids

def get_loc_keys():
    text = read(LOC)
    titles = set()
    descs = set()
    for m in re.finditer(r'^\s*([a-z0-9_]+)(_title)\s*:', text, re.MULTILINE | re.IGNORECASE):
        titles.add(m.group(1).lower())
    for m in re.finditer(r'^\s*([a-z0-9_]+)(_desc)\s*:', text, re.MULTILINE | re.IGNORECASE):
        descs.add(m.group(1).lower())
    return titles, descs

def mission_id_to_loc_key(mid):
    return mid.replace('a33_', 'a33_')

flags_set = get_flags_set_in_missions()
flags_checked = get_flags_checked_in_missions()
triggers = get_trigger_names()
effects = get_effect_names()
mods_used = get_modifiers_used_in_missions()
mods_defined = get_modifiers_defined()
loc_titles, loc_descs = get_loc_keys()

# Filter to A33 missions only
a33_flags_set = {f for f in flags_set if f.startswith('verne_') or f.startswith('a33_')}
a33_flags_checked = {f for f in flags_checked if f.startswith('verne_') or f.startswith('a33_')}

flags_set_not_ref = a33_flags_set - triggers
flags_check_not_set = a33_flags_checked - flags_set - triggers
mods_not_defined = {m for m in mods_used if m.startswith('verne_') and m not in mods_defined}

# Get all A33 mission IDs from missions file
mission_ids = get_mission_ids()
real_missions = {m for m in mission_ids if m.startswith('a33_')}

# Check loc coverage
missing_titles = []
missing_descs = []
for mid in sorted(real_missions):
    key = mid.replace('a33_', 'a33_')
    if key + '_title' not in loc_titles:
        missing_titles.append(mid)
    if key + '_desc' not in loc_descs:
        missing_descs.append(mid)

print("=" * 60)
print("MISSION INTEGRITY AUDIT")
print("=" * 60)
print()

print(f"Real A33 missions: {len(real_missions)}")
print(f"Flags SET (verne_/a33_): {len(a33_flags_set)}")
print(f"Flags CHECKED (verne_/a33_): {len(a33_flags_checked)}")
print(f"Trigger defs (verne_*): {len(triggers)}")
print(f"Effect defs (verne_*): {len(effects)}")
print(f"Modifiers used in missions: {len(mods_used)}")
print(f"Modifiers defined in modifiers file: {len(mods_defined)}")
print(f"Loc title keys: {len(loc_titles)}")
print(f"Loc desc keys: {len(loc_descs)}")
print()

print("=" * 60)
print("FLAGS: set but not in triggers file")
print("=" * 60)
for f in sorted(flags_set_not_ref):
    print(f"  {f}")
print()

print("=" * 60)
print("FLAGS: checked but never set and not a trigger")
print("=" * 60)
for f in sorted(flags_check_not_set):
    print(f"  {f}")
print()

print("=" * 60)
print("MODIFIERS: used in missions but not defined")
print("=" * 60)
for m in sorted(mods_not_defined):
    print(f"  {m}")
print()

print("=" * 60)
print("LOC: missing _title entries")
print("=" * 60)
print(f"  Count: {len(missing_titles)}")
for m in missing_titles[:10]:
    print(f"  {m}")
if len(missing_titles) > 10:
    print(f"  ... and {len(missing_titles)-10} more")
print()

print("=" * 60)
print("LOC: missing _desc entries")
print("=" * 60)
print(f"  Count: {len(missing_descs)}")
for m in missing_descs[:10]:
    print(f"  {m}")
if len(missing_descs) > 10:
    print(f"  ... and {len(missing_descs)-10} more")
