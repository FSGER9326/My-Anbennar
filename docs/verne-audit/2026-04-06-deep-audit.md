# Verne Deep Audit — 2026-04-06

**Scope:** missions/Verne_Missions.txt, events/verne_overhaul_*.txt, common/scripted_effects/verne_overhaul_effects.txt, common/event_modifiers/verne_overhaul*.txt, common/on_actions/verne_overhaul_on_actions.txt
**Severity:** [CRITICAL] = game-breaking, [HIGH] = broken logic, [MED] = warning, [LOW] = cosmetic/dead code

---

## 1. FLAG PROPAGATION AUDIT

### [CRITICAL] Flags SET but never CHECKED (broken state — dead flags)

These flags are set in mission effects or event `immediate` blocks but have no corresponding `has_country_flag = <flag>` check anywhere in Verne:

| Flag | Set By | Checked By |
|------|--------|------------|
| `verne_seed_estuary_companies` | A33_the_grand_port_of_heartspier effect | **NONE** — only referenced in `custom_tooltip = verne_overhaul_tt_seed_estuary_companies` (tooltip string, not a flag check) |
| `verne_can_create_wyvern_carriers` | A33_the_sea_nest effect | **NONE** — only appears in `custom_tooltip = verne_E6_effect_tt` |
| `verne_aur_kes_akasik_enabled` | A33_a_crimson_sea effect | **NONE** — only referenced in tooltip |
| `verne_sarhali_adventures_unlocked` | A33_in_search_of_adventure effect | **NONE** |
| `verne_taychendi_kheionai_adventures_unlocked` | A33_the_lands_of_adventure effect | **NONE** |
| `verne_akasi_bulwari_adventures_unlocked` | A33_across_the_pond effect | **NONE** |
| `verne_unlocked_adventure_system` | A33_across_the_pond AND A33_charter_the_expedition_fleet | **NONE** — despite being set twice |
| `verne_liliac_war_recounted` | `immediate = {}` in verne_liliac.1 | **NONE** |
| `verne_liliac_diplomacy_path_open` | `immediate = {}` in verne_liliac.1 | **NONE** — only option-selected path (verne_liliac.2) checks `has_country_flag` |
| `verne_liliac_vengeful_path` | Option B of verne_liliac.1 | **NONE** — A33_avenge_liliac_wars checks the same flag but the event that sets it is never triggered before the mission |

**Impact:** State set in mission/event never gates downstream content. Dead code that consumes flag namespace.

---

### [HIGH] Flags SET by scripted helpers but never verified via `has_country_flag`

| Helper Effect | Flags Set | Verified via `has_country_flag`? |
|--------------|-----------|----------------------------------|
| `verne_overhaul_seed_khenak_foundry_path` | `verne_seed_khenak_foundry` | **NO** — only `verne_overhaul_has_khenak_foundry_seeded` (custom scripted trigger, not a flag check) |
| `verne_overhaul_seed_dragonwake_path` | `verne_seed_dragonwake` | **NO** — only `verne_overhaul_has_dragonwake_path_seeded` (custom scripted trigger) |

**Impact:** If these scripted triggers ever change, the flag-based state is orphaned with no fallback flag check.

---

### [HIGH] Flags CHECKED but never SET

| Flag | Checked In | Likely Source |
|------|------------|--------------|
| `verne_blue_house_adventure_completed` | A33_a_most_prized_item trigger | **NOT FOUND** — no mission or event sets this flag |

**Impact:** A33_a_most_prized_item will never complete via the `verne_blue_house_adventure_completed` path.

---

### [MED] `verne_seed_estuary_companies` — tooltip vs. flag confusion

A33_the_grand_port_of_heartspier sets `verne_seed_estuary_companies` but the comment references `verne_overhaul_tt_seed_estuary_companies` as if it gates downstream content. This tooltip key may have been intended as a `custom_trigger_tooltip` that checks the flag, but currently it is only a plain `custom_tooltip` (no flag condition).

**Recommended fix:** If downstream content should be gated by this flag, convert `custom_tooltip` to `custom_trigger_tooltip` with a `has_country_flag = verne_seed_estuary_companies` check, OR remove the flag if truly unused.

---

### [MED] Liliac event immediate block state leakage

`verne_liliac.1` sets flags in `immediate = {}` (runs before option choice):
- `verne_liliac_war_recounted`
- `verne_liliac_diplomacy_path_open`

Then option B additionally sets `verne_liliac_vengeful_path`.

Problem: `immediate` flags are set regardless of which option the player picks. If the player picks Option A, `verne_liliac_diplomacy_path_open` is set but never used (option A fires verne_liliac.2, which checks `has_country_flag = verne_liliac_diplomacy_path_open` — so this works). But `verne_liliac_war_recounted` is set and **never checked anywhere**.

**Verdict:** `verne_liliac_war_recounted` is dead code.

---

### [LOW] `verne_seed_silver_oaths` — correctly propagated

`verne_seed_silver_oaths` is set by `verne_overhaul_seed_silver_oaths_path` and correctly checked in `verne_overhaul_advisor.1` ai_chance. ✓

---

### [LOW] `verne_overhaul_advisor.1` ai_chance flag dependencies

Options in `verne_overhaul_advisor.1` use `ai_chance` modifiers keyed to flags:
- `verne_seed_silver_oaths` → checked ✓
- `verne_seed_khenak_foundry` → dead flag (no check elsewhere, but ai_chance still sees it) ⚠
- `verne_seed_dragonwake` → dead flag ⚠
- `verne_overhaul_has_adventure_network_started` → custom scripted trigger
- `verne_overhaul_dynasty_machine_started` → custom scripted trigger
- `verne_overhaul_has_dragonwake_path_seeded` → custom scripted trigger

---

## 2. MISSION CHAIN INTEGRITY

### All `required_missions` reference valid mission keys ✓

Every `required_missions = { ... }` block in Verne_Missions.txt references mission keys that exist in the same file. No broken `required_missions` references detected.

### Flag-gated mission trigger validation

| Mission | Flag Required | Flag Source | Status |
|---------|---------------|-------------|--------|
| A33_might_of_the_wyvern | `verne_wyvern_nest_initialized` | A33_expand_the_wyvern_nests | ✓ Chain works |
| A33_avenge_liliac_wars | `verne_liliac_vengeful_path` | verne_liliac.1 option B | ⚠ Flag never set before mission is available |
| A33_seek_eastern_allies | `verne_liliac_diplomacy_path_open` | verne_liliac.1 immediate | ✓ Works |
| A33_a_most_prized_item | `verne_blue_house_adventure_completed` | NOT FOUND | [CRITICAL] Broken |

### No circular dependencies detected ✓

The mission tree flows in one direction with no circular `required_missions` loops.

---

## 3. MODIFIER AUDIT

**File checked:** `common/event_modifiers/verne_overhaul_modifiers.txt` and `verne_overhaul_flavour_modifiers.txt`

### Country modifiers from mission rewards — ALL DEFINED ✓

40+ country modifiers referenced in mission effects all have definitions in the modifier files. Notable verified mappings:

| Mission | Modifier | Status |
|---------|----------|--------|
| A33_the_grand_port_of_heartspier | `verne_new_armada`, `verne_the_wyverns_gulf` | ✓ Defined |
| A33_expand_the_Vernissage | `verne_vernissage_tier2` | ✓ Defined |
| A33_zenith_of_the_eastern_princes | `verne_restoring_the_borders` | ✓ Defined |
| A33_born_of_valour | `verne_half_ruinborn_small_modifier` | ✓ Defined |
| A33_expand_the_wyvern_nests | `verne_wyvern_nest_expanded` | ✓ Defined |
| A33_united_under_crimson_wings | `verne_wyvern_nest_grand` / `verne_wyvern_nest_no_dlc` | ✓ Defined |
| A33_religious_mercantilism | `verne_grand_fleet_tier1` | ✓ Defined |
| A33_all_roads_lead_to_verne | `verne_grand_fleet_tier2` | ✓ Defined |
| A33_world_faith_emperor | `verne_world_faith_emperor` + `verne_faith_emperor_innovat` | ✓ Both defined (distinct) |

### Province modifiers — NOT AUDITED

Province modifiers (e.g., `verne_port_of_adventure`, `verne_khenak_excavations`, `verne_vernissage_tier1`) were not audited against definitions. Recommend separate province-modifier audit.

### Special flags not expected to be modifiers

| Flag | Type | Expected | Status |
|------|------|----------|--------|
| `verne_special_cb_enabled` | Country flag | Unlocks special CB | ✓ Not a modifier (correctly used) |
| `can_use_propagate_religion` | Country flag | Gate propagate religion | ✓ Not a modifier (correctly used) |
| `verne_trade_company_conversion` | Country flag | Gate trade company conversion | ✓ Not a modifier (correctly used) |

---

## 4. EVENT HOOK AUDIT

### on_action hooks — MINIMAL but FUNCTIONAL ✓

**File:** `common/on_actions/verne_overhaul_on_actions.txt`

```plaintext
on_new_heir = {
    country_event = { id = verne_overhaul_dynasty.1 days = 1 }
}

on_yearly_pulse = {
    events = {
        verne_overhaul_advisor.5
    }
}
```

- `verne_overhaul_dynasty.1` → Defined in `verne_overhaul_dynasty_events.txt` ✓
- `verne_overhaul_advisor.5` → Defined in `verne_overhaul_advisor_events.txt` ✓

**No broken on_action references detected.**

---

### Event namespaces — ALL CORRECT ✓

| Namespace | File | Events |
|-----------|------|--------|
| `verne_liliac` | verne_overhaul_liliac_events.txt | .1, .2, .3, .4 |
| `verne_overhaul_crisis` | verne_overhaul_crisis_events.txt | .1-.9, .100 |
| `verne_overhaul_advisor` | verne_overhaul_advisor_events.txt | .1-.6 |
| `verne_overhaul_flavour` | verne_overhaul_flavour_events.txt | .1-.4 |
| `verne_overhaul_dynasty` | verne_overhaul_dynasty_events.txt | .1 |

All event IDs match their namespace. ✓

---

### Vanilla Anbennar event references — OUT OF SCOPE

Multiple missions reference vanilla Anbennar events (verne.100, verne.101, verne.102, etc.). These are base Anbennar events and were **not audited** — they belong to the Anbennar mod proper, not the Verne overhaul layer.

---

## 5. DECISION AUDIT

**Finding:** No `common/decisions/` directory exists in the repo. Decisions for Verne (if any) are either:
1. Part of base Anbennar
2. Not yet implemented
3. Embedded in events/scripted effects

**No decisions to audit.**

---

## 6. FILE PATH DISCREPANCIES (Audit Note)

The cron task specified these files that did NOT match repo structure:

| Specified Path | Actual Path |
|----------------|-------------|
| `events/verne_overhaul_events.txt` | `events/verne_overhaul_advisor_events.txt` (exists) |
| `common/on_actions/verne_on_actions.txt` | `common/on_actions/verne_overhaul_on_actions.txt` (exists) |

The actual Verne event content is split across 5 files:
1. `verne_overhaul_advisor_events.txt` — advisor recruitment
2. `verne_overhaul_crisis_events.txt` — Red Court crisis
3. `verne_overhaul_liliac_events.txt` — Liliac War legacy
4. `verne_overhaul_flavour_events.txt` — lightweight follow-through
5. `verne_overhaul_dynasty_events.txt` — dynasty safeguard

---

## SUMMARY OF FINDINGS

### [CRITICAL] (1)
- `verne_blue_house_adventure_completed` is checked in A33_a_most_prized_item but **never set** — the Blue House adventure completion path is unreachable

### [HIGH] (3)
- `verne_seed_estuary_companies` — set but never checked as a flag; tooltip reference only
- `verne_seed_khenak_foundry` — set via helper but no `has_country_flag` check exists
- `verne_seed_dragonwake` — set via helper but no `has_country_flag` check exists

### [MED] (4)
- `verne_can_create_wyvern_carriers` — dead flag, only in tooltip
- `verne_aur_kes_akasik_enabled` — dead flag, only in tooltip
- `verne_liliac_war_recounted` — dead flag from event immediate block
- `verne_unlocked_adventure_system` — set twice, never checked as flag

### [LOW] (6 dead flags)
- `verne_sarhali_adventures_unlocked`
- `verne_taychendi_kheionai_adventures_unlocked`
- `verne_akasi_bulwari_adventures_unlocked`
- `verne_liliac_vengeful_path` (event option sets it, but path logic may bypass event)

### [CLEAN] (4 areas)
- ✅ All `required_missions` reference valid keys
- ✅ All 40+ country modifiers have definitions
- ✅ Event namespaces match file namespaces
- ✅ on_action hooks reference valid events

---

## RECOMMENDED ACTIONS

1. **[CRITICAL]** Find where `verne_blue_house_adventure_completed` should be set and add the `set_country_flag` call, OR remove the flag check from A33_a_most_prized_item
2. **[HIGH]** Investigate whether `verne_seed_estuary_companies` was intended to gate downstream content; if not, remove the flag from the mission effect
3. **[HIGH]** Audit `verne_overhaul_has_khenak_foundry_seeded` and `verne_overhaul_has_dragonwake_path_seeded` scripted triggers to ensure they check equivalent state to the flags they parallel
4. **[MED]** Remove dead flags from mission effects to clean up namespace: `verne_can_create_wyvern_carriers`, `verne_aur_kes_akasik_enabled`, `verne_unlocked_adventure_system`, `verne_sarhali_adventures_unlocked`, `verne_taychendi_kheionai_adventures_unlocked`, `verne_akasi_bulwari_adventures_unlocked`
5. **[LOW]** Consider whether `verne_liliac_war_recounted` was intended to gate anything

---

*Audit generated: 2026-04-06 16:00 UTC*
*Next scheduled audit: 2026-04-06 22:00 UTC*
