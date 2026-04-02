import re
import os

VERNE_PATH = r"C:\Users\User\Documents\GitHub\My-Anbennar"

# Only Verne-specific files
files_to_check = [
    os.path.join(VERNE_PATH, "missions", "Verne_Missions.txt"),
    os.path.join(VERNE_PATH, "events", "Flavour_Verne_A33.txt"),
    os.path.join(VERNE_PATH, "decisions", "verne_overhaul_decisions.txt"),
    os.path.join(VERNE_PATH, "common", "scripted_triggers", "verne_overhaul_triggers.txt"),
    os.path.join(VERNE_PATH, "common", "scripted_effects", "verne_overhaul_effects.txt"),
    os.path.join(VERNE_PATH, "common", "event_modifiers", "verne_overhaul_modifiers.txt"),
    os.path.join(VERNE_PATH, "events", "verne_overhaul_crisis_events.txt"),
    os.path.join(VERNE_PATH, "events", "verne_overhaul_liliac_events.txt"),
    os.path.join(VERNE_PATH, "events", "verne_overhaul_dynasty_events.txt"),
    os.path.join(VERNE_PATH, "events", "verne_overhaul_advisor_events.txt"),
]

flags_to_verify = [
    'verne_seed_khenak_foundry',
    'verne_won_support_full',
    'verne_won_support_partial',
    'verne_liliac_diplomacy_path_open',
    'verne_liliac_vengeful_path',
    'verne_liliac_war_vengeful',
    'verne_attacked',
    'verne_backed_down',
    'verne_blue_house_adventure_completed',
    'verne_refunding_holy_order_15',
    'verne_can_create_wyvern_carriers',
]

results = {}
for flag in flags_to_verify:
    results[flag] = {'set': [], 'checked': []}
    pattern_set = re.compile(r'set_country_flag\s*=\s*' + re.escape(flag), re.IGNORECASE)
    pattern_chk = re.compile(r'has_country_flag\s*=\s*' + re.escape(flag), re.IGNORECASE)
    for fp in files_to_check:
        if not os.path.exists(fp):
            continue
        try:
            with open(fp, 'r', encoding='utf-8-sig', errors='ignore') as f:
                content = f.read()
        except:
            continue
        for m in pattern_set.finditer(content):
            rel = fp.replace(VERNE_PATH, '').lstrip('\\')
            results[flag]['set'].append(rel)
        for m in pattern_chk.finditer(content):
            rel = fp.replace(VERNE_PATH, '').lstrip('\\')
            results[flag]['checked'].append(rel)

print("=== FLAG TRACE RESULTS ===\n")
for flag, data in results.items():
    status = "*** NEVER SET ***" if not data['set'] else ""
    print(f"{flag} {status}")
    print(f"  SET in ({len(data['set'])}): {', '.join(data['set']) or 'NONE'}")
    print(f"  CHECKED in ({len(data['checked'])}): {', '.join(data['checked']) or 'NONE'}")
    print()
