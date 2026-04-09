# Verne Loc Completeness Audit — 2026-04-05

**Scope**: `verne_overhaul_l_english.yml`, `verne_overhaul_dynasty_l_english.yml`, `verne_overhaul_policy_split_l_english.yml`, `Flavour_Verne_A33_l_english.yml` (vanilla, read-only)  
**Game files cross-referenced**: `missions/Verne_Missions.txt`, `events/verne_overhaul_*.txt`, `decisions/verne_overhaul_decisions.txt`

---

## Summary

| Check | Result |
|---|---|
| Duplicate keys (verne_overhaul ∩ vanilla) | **53** — all resolved correctly |
| Vanilla-overwrites-overhaul precedence bug | **0** — none found |
| Empty/null values in verne_overhaul loc | **0** — none found |
| Event scope tag mismatches | **0** — none found |
| Decision scope tag mismatches | **13 missing title keys** (see below) |
| Keys referenced in game files but absent from all loc | **13** (see below) |
| Keys referenced in game files but only in vanilla (not overhaul) | **115** (vanilla fallback) |

---

## 1. Duplicate Key Detection

**53 keys** appear in both `verne_overhaul` loc files and `Flavour_Verne_A33_l_english.yml`.

### Load Order (alphabetical)
Files load in this order; later files overwrite earlier ones:

1. `F` — `Flavour_Verne_A33_l_english.yml` *(vanilla, read-only)*
2. `v` — `verne_overhaul_dynasty_l_english.yml`
3. `v` — `verne_overhaul_l_english.yml`
4. `v` — `verne_overhaul_policy_split_l_english.yml`

**Result**: `verne_overhaul_l_english.yml` loads after `Flavour_Verne_A33_l_english.yml`, so all 53 duplicate keys use **verne_overhaul values**. No vanilla-overwrites-overhaul precedence bug exists.

### Duplicate Key List
```
a33_a_crimson_sea_title
a33_a_matter_of_pride_title
a33_a_most_prized_item_title
a33_a_union_of_crowns_title
a33_across_the_pond_title
a33_all_roads_lead_to_verne_title
a33_alvars_reforms_title
a33_binding_the_beast_title
a33_born_of_valour_title
a33_break_the_queen_of_the_hill_title
a33_corins_devout_protectors_title
a33_corins_shield_title
a33_expand_the_vernissage_title
a33_expand_the_wyvern_nests_title
a33_in_search_of_adventure_title
a33_in_the_name_corin_title
a33_laments_regatta_title
a33_new_verne_title
a33_old_friends_old_rivals_title
a33_on_wings_of_artificery_title
a33_project_holohana_title
a33_religious_mercantilism_title
a33_spread_the_word_title
a33_taking_to_the_seas_title
a33_taming_the_lion_title
a33_the_allure_of_the_luna_title
a33_the_grand_port_of_heartspier_title
a33_the_grand_vernissage_title
a33_the_halanni_exposition_title
a33_the_heart_of_darkness_title
a33_the_holy_corinite_empire_title
a33_the_kingdom_of_verne_title
a33_the_lands_of_adventure_title
a33_the_might_of_the_wyvern_title
a33_the_quest_for_eggs_title
a33_the_riches_of_the_khenak_title
a33_the_rogue_duchy_title
a33_the_sea_nest_title
a33_the_verne_halann_title
a33_the_vernissage_title
a33_the_vernman_era_title
a33_the_vernman_renaissance_title
a33_the_wyvern_nest_initiative_title
a33_type_2_wyverns_title
a33_united_under_crimson_wings_title
a33_valour_on_the_seas_title
a33_with_sword_and_shield_title
a33_zenith_of_the_eastern_princes_title
NEW_VERNE
verne.200.a
verne.200.d
verne.200.t
verne_might_of_the_wyvern
```

---

## 2. Missing Key Audit

### 2a. Keys Referenced in Game Files — In Vanilla, Not in Verne Overhaul

**115 keys** referenced in mission/event/decision files exist in `Flavour_Verne_A33` loc but are absent from `verne_overhaul` loc. These fall back to vanilla values (acceptable for vanilla-patched content).

Selected notable entries (representing ~115 total):
```
verne_A1_tt_1yes / verne_A1_tt_1no
verne_A1_tt_2yes / verne_A1_tt_2no
verne_A8_effect_tt_1 through _6
verne_A10_effect_tt_1 through _6
verne_alvar_IV_condition_yes / verne_alvar_IV_condition_no
verne_B4_trigger_tt1yes/no through _tt3yes/no
verne_new_armada
verne_the_wyverns_gulf
verne_wyvern_nest / verne_wyvern_nest_expanded / verne_wyvern_nest_grand
verne_vernman_era
verne_corinite_halann
verne_liliac_avenge_tt / verne_liliac_seek_eastern_tt / verne_liliac_unity_tt
verne_tourism_economy
verne_wingspan
... (115 total)
```

**Action recommended**: Audit each to determine whether the vanilla loc value is appropriate for overhaul gameplay or whether an overhaul-specific value is needed. This is not a bug — it is expected behaviour when preserving vanilla mission/toolkit content.

### 2b. Keys Truly Missing (Not in Vanilla, Not in Verne Overhaul)

**13 keys** referenced in game files that exist in **neither** `Flavour_Verne_A33` nor `verne_overhaul` loc. These will fall back to the game default (raw key as display string) in-game.

| Missing Key | Likely Source | Impact |
|---|---|---|
| `verne_overhaul_flavour.1.t` | `events/verne_overhaul_flavour_events.txt` | Event title missing |
| `verne_overhaul_flavour.1.d` | `events/verne_overhaul_flavour_events.txt` | Event desc missing |
| `verne_corinite_stewardship_effect_tt` | `missions/Verne_Missions.txt` | Tooltip may show raw key |
| `verne_expand_foundry_tt` | `missions/Verne_Missions.txt` | Tooltip may show raw key |
| `verne_found_crimson_scale_order_tt` | `missions/Verne_Missions.txt` | Tooltip may show raw key |
| `verne_industrial_logistics_tt` | `missions/Verne_Missions.txt` | Tooltip may show raw key |
| `verne_khenak_steel_tt` | `missions/Verne_Missions.txt` | Tooltip may show raw key |
| `verne_spice_route_monopoly_tt` | `missions/Verne_Missions.txt` | Tooltip may show raw key |
| `verne_trade_network_tt` | `missions/Verne_Missions.txt` | Tooltip may show raw key |
| `verne_vernman_merchant_marine_tt` | `missions/Verne_Missions.txt` | Tooltip may show raw key |
| `verne_world_faith_emperor_tt` | `missions/Verne_Missions.txt` | Tooltip may show raw key |
| `abolished_slavery_act_tooltip` | `missions/Verne_Missions.txt` | Vanilla key, not Verne-specific |
| `empty_line_tt` | `missions/Verne_Missions.txt` | Likely intentional placeholder |

**Action recommended**: Add loc entries for the two `verne_overhaul_flavour.1.*` keys. For the tooltip keys, confirm whether they are intended to be implemented; if so, add loc entries.

---

## 3. Empty Value Check

**No empty values** were found in `verne_overhaul_l_english.yml`, `verne_overhaul_dynasty_l_english.yml`, or `verne_overhaul_policy_split_l_english.yml`. All key-value pairs have non-empty values.

---

## 4. Scope Tag Audit

### 4a. Event Loc Keys vs Event IDs

**Result: PASS** — No mismatches.

| Event File | Event IDs | Loc Keys Verified |
|---|---|---|
| `verne_overhaul_advisor_events.txt` | 1–6 | All present |
| `verne_overhaul_crisis_events.txt` | 1–9, 100 | All present |
| `verne_overhaul_dynasty_events.txt` | 1 | Present |
| `verne_overhaul_flavour_events.txt` | 1 | Present (`.t`/`.d` **missing** from loc — see §2b) |
| `verne_overhaul_liliac_events.txt` | 1–4 | All present |

### 4b. Decision Loc Keys vs Decision IDs

**15 decision IDs** found in `verne_overhaul_decisions.txt`. All have `*_desc` entries in verne_overhaul loc. However, **13 are missing `*_title` entries**:

```
verne_overhaul_appoint_court_advisor_title          ← MISSING
verne_overhaul_charter_khenak_talons_title          ← MISSING
verne_overhaul_codify_union_court_protocols_title   ← MISSING
verne_overhaul_consolidate_reforged_court_title     ← MISSING
verne_overhaul_enforce_dynastic_safeguard_title     ← MISSING (dynasty file has _title)
verne_overhaul_form_harbormaster_general_staff_title ← MISSING
verne_overhaul_formalize_dovesworn_partnership_title ← MISSING
verne_overhaul_formalize_silver_oaths_title         ← MISSING
verne_overhaul_levy_silver_wake_convoy_title        ← MISSING
verne_overhaul_muster_dragonwake_cadets_title       ← MISSING
verne_overhaul_open_marriage_court_title            ← MISSING
verne_overhaul_organize_pearlescent_diplomatic_corps_title ← MISSING
verne_overhaul_pay_off_mage_debt_title              ← MISSING
verne_overhaul_proclaim_exalted_lineage_title       ← MISSING (dynasty file has _title)
verne_overhaul_sponsor_curatorial_embassies_title    ← MISSING
```

Note: `verne_overhaul_enforce_dynastic_safeguard_title` and `verne_overhaul_proclaim_exalted_lineage_title` DO exist in `verne_overhaul_dynasty_l_english.yml`. The other 13 have no `*_title` entry anywhere in verne_overhaul loc.

In-game, the decision display name falls back to the decision ID when no loc key exists. This is a cosmetic issue (decision popup shows raw key name) — not a crash or gameplay break.

### 4c. Mission Title Keys vs Mission IDs

Mission title keys are not stored in verne_overhaul loc files — the vanilla `Flavour_Verne_A33_l_english.yml` carries `a33_*_title` keys for the Verne missions. The overhaul references the same vanilla mission IDs, so title loc is handled by vanilla.

---

## Key Counts

| File | Key Count |
|---|---|
| `verne_overhaul_l_english.yml` | 817 |
| `verne_overhaul_dynasty_l_english.yml` | 9 |
| `verne_overhaul_policy_split_l_english.yml` | 6 |
| `Flavour_Verne_A33_l_english.yml` (vanilla, read-only) | 1,197 |

---

## Findings Requiring Action

1. **`verne_overhaul_flavour.1.t` / `verne_overhaul_flavour.1.d`** — Event title and desc loc keys referenced in `verne_overhaul_flavour_events.txt` but not present in any verne_overhaul loc file. Add to `verne_overhaul_l_english.yml`.

2. **13 missing decision `*_title` keys** — Cosmetic (decision popup shows raw key). Consider adding for polish:
   - All 13 new-overhaul decisions missing `*_title` keys (the 2 in dynasty file are already covered)

3. **~115 vanilla-patch keys** — Not bugs; verify on a case-by-case basis whether vanilla loc values are appropriate for overhaul mission flows.
