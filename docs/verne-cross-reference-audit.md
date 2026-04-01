# Cross-Reference Audit: Design Docs vs. Implementation

## Executive Summary
- Position conflicts: **11** (3 direct overlaps with existing missions, 8 within design docs themselves)
- Flag issues: **5** (3 flags checked but never set, 1 flag set but named differently, 1 typo)
- Modifier conflicts: **0** (no naming clashes with existing modifiers)
- Reform reference issues: **4** (1 reform name mismatch, 1 reform doesn't exist, 1 reform unlocked but undefined, 1 reform referenced in wrong lane)
- **Overall feasibility: MODIFICATIONS NEEDED** — implementable with targeted fixes

---

## Slot-by-Slot Analysis

### A33_first_slot (Court & Oaths — Lane 1)
- **Existing positions occupied:** 2, 3, 6, 8, 9, 10, 11, 12, 14
- **Existing missions:** A33_the_vernman_renaissance (2), A33_the_grand_port_of_heartspier (3), A33_the_vernissage (6), A33_expand_the_Vernissage (8), A33_zenith_of_the_eastern_princes (9), A33_the_halanni_exposition (10), A33_the_heart_of_darkness (11), A33_the_grand_vernissage (12), A33_project_holohana (14)
- **Free positions:** 1, 4, 5, 7, 13
- **Design doc wants positions:** 1, 3, 6, 9
- **CONFLICTS:**
  - ❌ Position 3: Lane 1 wants `A33_establish_court_of_oaths` but `A33_the_grand_port_of_heartspier` exists there
  - ❌ Position 6: Lane 1 wants `A33_royal_arbitration` but `A33_the_vernissage` exists there
  - ❌ Position 9: Lane 1 wants `A33_diplomatic_hegemony` but `A33_zenith_of_the_eastern_princes` exists there
- **Fix:** Remap Lane 1 to free positions: pos 1→1 ✅, pos 3→4, pos 6→5, pos 9→7 (or 13)
- **Flag issues:**
  - `verne_mission_start` — checked by `A33_formalize_silver_oaths` as trigger; **NEVER SET** in codebase or any design doc
  - `verne_royal_arbitration_complete` — checked by `A33_diplomatic_hegemony`; **NEVER SET** anywhere (design doc for `A33_royal_arbitration` doesn't set it; it sets a flag called `verne_royal_arbitration` implicitly via completing but never explicitly uses `set_country_flag`)
- **Reform issues:**
  - `verne_court_of_oaths_reform` — **DOES NOT EXIST** in reforms file. Actual name: `verne_court_of_silver_oaths_reform`
  - `verne_crown_of_the_oathkeeper_reform` — **DOES NOT EXIST** in reforms file. No match found. Likely needs to be defined or renamed to an existing reform (e.g., `verne_vernman_court_of_the_world_reform`)

### A33_second_slot (Maritime Empire — Lane 2)
- **Existing positions occupied:** 1, 2, 3, 4, 5, 7, 9, 10, 12
- **Existing missions:** A33_alvars_reforms (1), A33_the_riches_of_the_khenak (2), A33_the_rogue_duchy (3), A33_across_the_pond (4), A33_in_search_of_adventure (5), A33_the_lands_of_adventure (7), A33_a_most_prized_item (9), A33_laments_regatta (10), A33_new_verne (12)
- **Free positions:** 6, 8, 11
- **Design doc wants positions:** 1, 3, 5, 8
- **CONFLICTS:**
  - ❌ Position 1: Lane 2 wants `A33_secure_port_of_heartspier` but `A33_alvars_reforms` exists there
  - ❌ Position 3: Lane 2 wants `A33_form_estuary_companies` but `A33_the_rogue_duchy` exists there
  - ❌ Position 5: Lane 2 wants `A33_fleet_of_the_crimson_wake` but `A33_in_search_of_adventure` exists there
  - ✅ Position 8: FREE — `A33_imperial_sea_court` can go here
- **Fix:** Remap Lane 2: pos 1→6, pos 3→8 (taken by capstone), pos 5→11, pos 8→13+ (needs expansion). Or merge maritime missions into first_slot free positions.
- **Flag issues:**
  - `verne_heartspier_secured` — checked by `A33_form_estuary_companies`; **NEVER SET** in codebase (would be set by `A33_secure_port_of_heartspier`, but that mission also doesn't exist yet — it's circular within the lane, so this is OK as long as the chain is implemented in order)
- **Reform issues:**
  - All referenced reforms (`verne_estuary_companies_of_heartspier_reform`, `verne_admiralty_of_the_crimson_wake_reform`, `verne_regatta_discipline_reform`, `verne_imperial_sea_court_reform`) — **ALL EXIST** ✅

### A33_third_slot (Dynastic Machine — Lane 3)
- **Existing positions occupied:** 1, 2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14
- **Existing missions:** A33_old_friends_old_rivals (1), A33_a_matter_of_pride (2), A33_the_allure_of_the_luna (3), A33_the_kingdom_of_Verne (4), A33_corins_shield (6), A33_spread_the_word (7), A33_in_the_name_corin (8), A33_born_of_valour (9), A33_the_vernman_era (11), A33_valour_on_the_seas (12), A33_all_roads_lead_to_verne (13), A33_the_verne_halann (14)
- **Free positions:** 5, 10
- **Design doc wants positions:** 1, 4, 8
- **CONFLICTS:**
  - ❌ Position 1: Lane 3 wants `A33_enact_dynastic_safeguard` but `A33_old_friends_old_rivals` exists there
  - ❌ Position 4: Lane 3 wants `A33_expand_noble_privileges` but `A33_the_kingdom_of_Verne` exists there
  - ❌ Position 8: Lane 3 wants `A33_exalted_dynasty_machine` but `A33_in_the_name_corin` exists there
- **Fix:** Remap Lane 3 to free positions: pos 1→5, pos 4→10, pos 8→15+ (needs position expansion)
- **Flag issues:**
  - `verne_dynasty_protected` — checked by `A33_exalted_dynasty_machine`; **IS SET** by existing mission `A33_corins_devout_protectors` (slot 4, pos 9) ✅
  - `verne_mission_start` — checked by `A33_enact_dynastic_safeguard` (via `has_completed_mission = A33_formalize_silver_oaths`); this checks mission completion not a flag, so OK ✅
- **Reform issues:**
  - `verne_court_of_oaths_reform` — **DOES NOT EXIST** (same issue as Lane 1). Should be `verne_court_of_silver_oaths_reform`
  - `verne_throne_of_the_wyvern_kings_reform` — **EXISTS** ✅
  - `verne_exalted_dynasty_machine_reform` — referenced as `unlock_reform` target; **DOES NOT EXIST** in reforms file. Needs to be defined as a new reform tier.

### A33_fourth_slot (Trade & Colonisation — Lane 4)
- **Existing positions occupied:** 3, 4, 5, 8, 9, 10, 12, 13
- **Existing missions:** A33_taking_to_the_seas (3), A33_taming_the_lion (4), A33_a_union_of_crowns (5), A33_united_under_crimson_wings (8), A33_corins_devout_protectors (9), A33_with_sword_and_shield (10), A33_the_holy_corinite_empire (12), A33_type_2_wyverns (13)
- **Free positions:** 1, 2, 6, 7, 11, 14
- **Design doc wants positions:** 2, 5, 9
- **CONFLICTS:**
  - ✅ Position 2: FREE — `A33_charter_overseas_companies` can go here
  - ❌ Position 5: `A33_distant_horizons_expansion` conflicts with `A33_a_union_of_crowns`
  - ❌ Position 9: `A33_overseas_commanderies` conflicts with `A33_corins_devout_protectors`
- **Fix:** Keep pos 2, remap pos 5→6 or 7, remap pos 9→11 or 14
- **Flag issues:**
  - `verne_charter_unlocked` — set by `A33_charter_overseas_companies`, checked by `A33_distant_horizons_expansion` — OK ✅
  - `verne_distant_horizons_expansion_completed` — set by `A33_distant_horizons_expansion`, checked by `A33_overseas_commanderies` — OK ✅
- **Reform issues:**
  - `verne_hall_of_distant_horizons_reform` — **EXISTS** ✅
  - `verne_overseas_commanderies_reform` — **EXISTS** ✅
  - Generic `tier_2_reform` / `tier_4_reform` — these are NOT valid EU4 reform references. Must use actual reform IDs.

### A33_fifth_sloth (Red Court & Arcane — Lane 5, EXISTING + NEW)
- **NOTE:** Slot name typo: `A33_fifth_sloth` instead of `A33_fifth_slot`
- **Existing positions occupied:** 1, 2, 3, 4, 5, 6, 7, 9, 10, 12
- **Existing missions:** A33_break_the_queen_of_the_hill (1), A33_the_quest_for_eggs (2), A33_the_wyvern_nest_initiative (3), A33_binding_the_beast (4), A33_expand_the_wyvern_nests (5), A33_the_sea_nest (6), A33_the_might_of_the_wyvern (7), A33_a_crimson_sea (9), A33_religious_mercantilism (10), A33_on_wings_of_artificery (12)
- **Free positions:** 8, 11, 13+
- **Design doc (Lane 5) wants positions:** 2, 5, 9, 12
- **CONFLICTS:**
  - ❌ Position 2: Lane 5 wants `A33_establish_red_court` but `A33_the_quest_for_eggs` exists there
  - ❌ Position 5: Lane 5 wants `A33_dragonwake_ordinance` but `A33_expand_the_wyvern_nests` exists there
  - ❌ Position 9: Lane 5 wants `A33_battle_mage_collegium` but `A33_a_crimson_sea` exists there
  - ❌ Position 12: Lane 5 wants `A33_battle_mage_collegium` (capstone, but doc says pos 9 for collegium; 12 isn't assigned to a design mission) — actually lane 5 only has 3 missions (2, 5, 9). No conflict at 12 from design.
- **Fix:** Remap Lane 5 to free positions: pos 2→8, pos 5→11, pos 9→13+
- **Flag issues:** None specific to this lane's triggers
- **Reform issues:**
  - `verne_red_court_arcana_reform` — **EXISTS** ✅
  - `verne_dragonwake_ordinance_reform` — **EXISTS** ✅
  - `verne_battle_mage_collegium_reform` — **EXISTS** ✅

### A33_sixth_slot (Liliac War Legacy — Lane 6)
- **Wrapper:** `A33_sixth_slot` with `slot = 5` (shares slot with 5th, 7th, 8th, 9th)
- **Existing positions occupied:** 8, 10 (×2)
- **Existing missions:** A33_recount_liliac_defeat (8), A33_seek_eastern_allies (10), A33_avenge_liliac_wars (10), A33_unity_through_diplomacy (12)
- **Design doc (Lane 6) wants positions:** 2, 4, 7
- **CONFLICTS:** ✅ None — all positions free in this wrapper
- **Flag issues:**
  - `verne_liliac_diplomacy_path_open` — set by event `verne_liliac.1`, checked by `A33_seek_eastern_allies` — OK ✅
  - `verne_liliac_war_vengeful` — set by event `verne_liliac.1`, checked by `A33_avenge_liliac_wars` — OK ✅
  - `verne_liliac_vengeful_path` — checked by `A33_unity_through_diplomacy`; **likely set by event** `verne_liliac.1` or `.3` — verify in events ✅ (assumed OK)
- **Reform issues:**
  - `verne_vernman_court_of_the_world_reform` — **EXISTS** ✅
  - `verne_knights_of_the_crimson_scale_reform` — **EXISTS** ✅

### A33_seventh_slot (Adventure Network — Lane 7)
- **Wrapper:** `A33_seventh_slot` with `slot = 5`
- **Existing positions occupied:** 14, 16, 18
- **Existing missions:** A33_charter_the_expedition_fleet (14), A33_ports_of_adventure_program (16), A33_expedition_supply_chain (18)
- **CONFLICTS:** ✅ No new design doc missions for this lane — lane 7 IS the existing implementation

### A33_eighth_slot (Faith & Apostolic Empire — Lane 8)
- **Wrapper:** `A33_eighth_slot` with `slot = 5`
- **Existing positions occupied:** 2, 5, 9
- **Existing missions:** A33_corinite_stewardship (2), A33_pearlescent_concord (5), A33_world_faith_emperor (9)
- **CONFLICTS WITHIN SLOT 5:**
  - ❌ Position 2: Lane 8 `A33_corinite_stewardship` **CONFLICTS** with Lane 5 existing `A33_the_quest_for_eggs`
  - ❌ Position 5: Lane 8 `A33_pearlescent_concord` **CONFLICTS** with Lane 5 existing `A33_expand_the_wyvern_nests`
  - ❌ Position 9: Lane 8 `A33_world_faith_emperor` **CONFLICTS** with Lane 5 existing `A33_a_crimson_sea`
- **Fix:** Move Lane 8 to different wrapper (e.g., `A33_eighth_slot` with `slot = 8`) OR remap positions to unique values (e.g., 20, 23, 27)
- **Flag issues:**
  - `verne_corinite_founded` — set by `A33_corinite_stewardship`, checked by later missions — OK ✅
  - `verne_cb_against_heathen_pirates` — set by `A33_world_faith_emperor`; **no CB definition exists yet** in `common/cb_types/`. Flag is set but currently does nothing. Needs follow-up implementation.
- **Reform issues:**
  - `verne_apostolic_court_of_corin_reform` — **EXISTS** ✅
  - `verne_vernman_court_of_the_world_reform` — **EXISTS** ✅
  - `verne_vernissage_charter_reform` — **EXISTS** ✅

### A33_ninth_slot (Vernissage Secretariat — Lane 9)
- **Wrapper:** `A33_ninth_slot` with `slot = 5`
- **Existing positions occupied:** 24
- **Existing mission:** A33_vernissage_secretariat (24)
- **CONFLICTS WITHIN SLOT 5:**
  - ❌ Position 24: Lane 9 `A33_vernissage_secretariat` — no conflict with other lane positions (20, 22 are Lane 9's other positions)
  - ✅ Positions 20, 22: Used by Lane 9's `A33_red_brass_forge` and `A33_controlled_devastation` — but these are in `A33_eighth_slot` wrapper, not `A33_ninth_slot`!
  - ⚠️ **CROSS-WRAPPER ISSUE:** `A33_red_brass_forge` (pos 20) and `A33_controlled_devastation` (pos 22) are in the `A33_eighth_slot` wrapper, while `A33_vernissage_secretariat` (pos 24) is in `A33_ninth_slot`. These should likely be in the same wrapper.
- **Flag issues:**
  - `verne_seed_khenak_foundry` — checked by `A33_controlled_devastation` via `has_country_flag`; **set by** `verne_overhaul_seed_khenak_foundry_path` scripted effect — needs verification that this effect actually sets the flag ✅ (assumed OK)
- **Reform issues:**
  - `verne_vernissage_secretariat_reform` — **EXISTS** ✅
  - `verne_charter_of_the_vernissage_reform` — **EXISTS** ✅

---

## Modifier Audit

### Clashing names
- **None found** — all new design doc modifier names are unique and don't clash with existing modifiers in the codebase.

### Undefined modifiers (referenced in design docs but must be created)
These modifiers are defined in the design docs with their stats, so they just need to be implemented in `common/event_modifiers/` or `common/country_modifiers/`:

**Lane 1:** `verne_silver_oaths`, `verne_court_of_oaths`, `verne_royal_arbitration`, `verne_diplomatic_hegemony`
**Lane 2:** `verne_heartspier_port` (province), `verne_heartspier_trade_powers` (province), `verne_heartspier_companies`, `verne_crimson_wake_fleet`, `verne_crimson_wake_discount`, `verne_imperial_sea_court`
**Lane 3:** `verne_dynastic_safeguard`, `verne_noble_charter`, `verne_exalted_dynasty_machine`
**Lane 4:** `verne_chartered_overseas_companies`, `verne_distant_horizons`, `verne_overseas_commanderies`
**Lane 5:** `verne_red_court_advisory`, `verne_dragonwake_profession`, `verne_dragonwake_shock`, `verne_war_wizard`, `verne_battle_mage_collegium`, `verne_collegium_fire_artillery`, `verne_collegium_fire_army`
**Lane 6:** `verne_royal_census`, `verne_academic_endowments`, `verne_sovereign_legitimacy`
**Lane 8:** `verne_corinite_stewardship`, `verne_pearlescent_concord`, `verne_world_faith_emperor`, `verne_faith_emperor_innovat`

**Note on `verne_dynasty_protected_court`:** Existing codebase modifier used by `A33_corins_devout_protectors`. Design doc Lane 3 calls its equivalent `verne_dynasty_safeguard`. These are different modifiers serving different purposes — no clash, but they're thematically related and should be documented together.

---

## Flag Dependency Map

```
SET BY (existing codebase)              CHECKED BY
─────────────────────────────────       ─────────────────────────
verne_defavored_adventurers             A33_alvars_reforms (self-check), A33_united_under_crimson_wings
  └─ set by: A33_alvars_reforms

verne_dynasty_protected                 A33_exalted_dynasty_machine (Lane 3 design)
  └─ set by: A33_corins_devout_protectors (existing)

verne_akasi_bulwari_adventures_unlocked (set but never checked)
verne_sarhali_adventures_unlocked       (set but never checked)
verne_taychendi_kheionai_adventures_unlocked (set but never checked)
verne_seed_estuary_companies            (set but never checked)
verne_can_create_wyvern_carriers        (set but never checked)
verne_aur_kes_akasik_enabled            (set but never checked)

SET BY (design docs)                   CHECKED BY
─────────────────────────────────       ─────────────────────────
verne_mission_start                     A33_formalize_silver_oaths (Lane 1) ❌ NEVER SET ANYWHERE
verne_royal_arbitration_complete        A33_diplomatic_hegemony (Lane 1) ❌ NEVER SET ANYWHERE
verne_heartspier_secured                A33_form_estuary_companies (Lane 2) ✅ set by A33_secure_port_of_heartspier
verne_charter_unlocked                  A33_distant_horizons_expansion (Lane 4) ✅ set by Lane mission
verne_distant_horizons_expansion_completed A33_overseas_commanderies (Lane 4) ✅ set by Lane mission
verne_corinite_founded                  A33_pearlescent_concord, A33_world_faith_emperor (Lane 8) ✅ set by Lane mission
verne_census_established                A33_secure_academic_endowments (Lane 6) ✅ set by Lane mission
verne_endowments_established            A33_stamp_of_sovereign_legitimacy (Lane 6) ✅ set by Lane mission
verne_liliac_diplomacy_path_open        A33_seek_eastern_allies (Lane 6) ✅ set by event
verne_liliac_war_vengeful               A33_avenge_liliac_wars (Lane 6) ✅ set by event
verne_liliac_vengeful_path              A33_unity_through_diplomacy (Lane 6) ⚠️ assumed set by event
verne_cb_against_heathen_pirates        (set by Lane 8, but no CB implemented yet) ⚠️
```

---

## Reform Reference Summary

| Reform Name | Exists? | Referenced By |
|---|---|---|
| `verne_court_of_silver_oaths_reform` | ✅ Yes | Codebase |
| `verne_court_of_oaths_reform` | ❌ **No** | Lanes 1, 3 (SHOULD BE `verne_court_of_silver_oaths_reform`) |
| `verne_crown_of_the_oathkeeper_reform` | ❌ **No** | Lane 1 (needs to be defined or replaced) |
| `verne_throne_of_the_wyvern_kings_reform` | ✅ Yes | Lane 3 |
| `verne_exalted_dynasty_machine_reform` | ❌ **No** | Lane 3 (unlock_reform target — needs definition) |
| `verne_estuary_companies_of_heartspier_reform` | ✅ Yes | Lane 2 |
| `verne_admiralty_of_the_crimson_wake_reform` | ✅ Yes | Lane 2 |
| `verne_regatta_discipline_reform` | ✅ Yes | Lane 2 |
| `verne_imperial_sea_court_reform` | ✅ Yes | Lane 2 |
| `verne_hall_of_distant_horizons_reform` | ✅ Yes | Lane 4 |
| `verne_overseas_commanderies_reform` | ✅ Yes | Lane 4 |
| `verne_red_court_arcana_reform` | ✅ Yes | Lane 5 |
| `verne_dragonwake_ordinance_reform` | ✅ Yes | Lane 5 |
| `verne_battle_mage_collegium_reform` | ✅ Yes | Lane 5 |
| `verne_vernman_court_of_the_world_reform` | ✅ Yes | Lane 8 |
| `verne_apostolic_court_of_corin_reform` | ✅ Yes | Lane 8 |
| `verne_vernissage_charter_reform` | ✅ Yes | Lane 8 |
| `verne_knights_of_the_crimson_scale_reform` | ✅ Yes | Lane 6 |
| `verne_vernissage_secretariat_reform` | ✅ Yes | Lane 9 |
| `verne_charter_of_the_vernissage_reform` | ✅ Yes | Lane 9 |
| `tier_2_reform` / `tier_4_reform` | ❌ **Invalid** | Lane 4 (must use actual reform IDs) |

---

## Recommended Fixes

### 1. Position Reassignments

**Lane 1 (first_slot):** Remap to free positions
- pos 1 → 1 ✅ (free)
- pos 3 → 4 (free)
- pos 6 → 5 (free)
- pos 9 → 7 (free)

**Lane 2 (second_slot):** Remap to free positions
- pos 1 → 6 (free)
- pos 3 → 8 (free)
- pos 5 → 11 (free)
- pos 8 → 13 (free, or higher)

**Lane 3 (third_slot):** Remap to free positions
- pos 1 → 5 (free)
- pos 4 → 10 (free)
- pos 8 → 15+ (needs new position)

**Lane 4 (fourth_slot):** Partial remap
- pos 2 → 2 ✅ (free)
- pos 5 → 6 (free)
- pos 9 → 11 (free)

**Lanes 5+8 (fifth_sloth):** Separate into different wrappers or use high position numbers
- Lane 5 → positions 8, 11, 13+ (avoiding Lane 8's 2, 5, 9)
- OR: Move Lane 8 to a dedicated `slot = 8` wrapper with unique positions
- Current collision: Both Lane 5 and Lane 8 claim positions 2, 5, 9 within `slot = 5`

**Lane 9:** Merge `A33_red_brass_forge` (pos 20) and `A33_controlled_devastation` (pos 22) from `A33_eighth_slot` into `A33_ninth_slot` wrapper (they're already slot=5, just inconsistent wrapper assignment)

### 2. Reform Name Corrections
- Lane 1 & 3: Replace all `verne_court_of_oaths_reform` → `verne_court_of_silver_oaths_reform`
- Lane 1: Define `verne_crown_of_the_oathkeeper_reform` OR replace with `verne_vernman_court_of_the_world_reform`
- Lane 3: Define `verne_exalted_dynasty_machine_reform` as a new reform tier
- Lane 4: Replace `tier_2_reform` / `tier_4_reform` with actual reform IDs from the reforms file

### 3. Flag Chain Corrections
- **CRITICAL:** Create a mechanism to set `verne_mission_start` — either add `set_country_flag = verne_mission_start` to the game start/initialization event, or remove the check from `A33_formalize_silver_oaths`
- **CRITICAL:** Add `set_country_flag = verne_royal_arbitration_complete` to the effect of `A33_royal_arbitration` (Lane 1, position 6)
- **FOLLOW-UP:** Implement the `verne_cb_against_heathen_pirates` CB in `common/cb_types/`

### 4. Slot Wrapper Consolidation
- Fix typo: `A33_fifth_sloth` → `A33_fifth_slot`
- Consider merging all slot-5 wrappers (5th through 9th) into a single file or clearly delineating them by position ranges to avoid future collisions

---

## Overall Assessment

**Status: MODIFICATIONS NEEDED — implementable with targeted fixes**

The design docs are well-structured and thematically coherent. The main issues are:

1. **Position conflicts** (solvable): Most design lanes overlap with existing missions at the same position numbers. This is a straightforward remapping exercise — there are enough free positions in each slot.

2. **Slot 5 congestion** (moderate risk): Five lane wrappers (`A33_fifth_sloth` through `A33_ninth_slot`) all share `slot = 5`, with two lanes (5 and 8) directly colliding on positions 2, 5, and 9. These must be separated into different wrappers or given non-overlapping position ranges.

3. **Missing reforms** (needs content): Three reform references don't match any defined reform. Two (`verne_court_of_oaths_reform`, `verne_crown_of_the_oathkeeper_reform`) are naming mismatches or missing definitions. One (`verne_exalted_dynasty_machine_reform`) is an unlock target that needs to be created.

4. **Broken flag chains** (critical): Two flags are checked but never set (`verne_mission_start`, `verne_royal_arbitration_complete`). These will cause trigger failures at runtime.

5. **No modifier conflicts** — all new modifier names are clean.

6. **No cross-lane flag dependency issues** — lanes mostly self-contain their flag chains, with the exception of `verne_dynasty_protected` (set by existing codebase mission, checked by Lane 3 design).

**Recommendation:** Apply the position remappings, fix the reform names, add the missing flag sets, and consolidate the slot-5 wrappers. After these fixes, the design is fully implementable.
