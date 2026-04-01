# Tooltip Compliance Report — Lane Design Docs

**Date:** 2026-04-01 11:38 CET
**Reviewer:** Background subagent (bg-tooltip-review)
**Scope:** All 8 lane design files in `docs/design/lanes/` against standards S01–S05

---

## Summary

| Standard | Issues Found | Severity |
|----------|-------------|----------|
| S01 (Numbers in tooltips) | 6 | Medium |
| S02 (Variable tracking) | 3 | High |
| S03 (Prerequisite tooltips) | 5 | High |
| S04 (Cross-references) | 1 | Low |
| S05 (Terminology) | 2 | Low |
| **Total** | **17** | |

**Most common issue type:** S03 — Prerequisite tooltips (5 issues)
**Top 3 files needing work:** lane4-trade (4 issues), lane8-faith (4 issues), lane5-redcourt (4 issues)

---

## Detailed Findings

### S01: Numbers in Tooltips (6 issues)

#### S01-1. lane1-court — `verne_silver_oaths_modifier_desc`
- **Text:** "The Silver Oaths grant Verne enhanced diplomatic standing and vassal loyalty."
- **Issue:** Uses vague "enhanced" instead of stating the actual values.
- **Fix:** "The Silver Oaths grant Verne +1 diplomatic reputation and +5% vassal income."

#### S01-2. lane8-faith — `verne_corinite_stewardship_modifier_desc`
- **Text:** "Verne's stewardship of the Corinite faith grants enhanced missionary capability."
- **Issue:** Uses "enhanced" instead of stating +1 missionary and -33% enforce religion cost.
- **Fix:** "Verne's stewardship of the Corinite faith grants +1 missionary and -33% enforce religion cost."

#### S01-3. lane8-faith — `verne_world_faith_emperor_modifier_desc`
- **Text:** "The World Faith Emperor's authority extends Verne's influence through faith."
- **Issue:** No numbers at all. Doesn't mention +1 free leader or +1 merchant.
- **Fix:** "The World Faith Emperor grants +1 free leader and +1 merchant, extending Verne's influence through faith."

#### S01-4. lane1-court — `verne_court_of_oaths_modifier_desc`
- **Text:** "The Court of Oaths streamlines the annexation of willing subjects."
- **Issue:** "Streamlines" is vague. Doesn't mention -10% diplo-annex, +10% vassal FL, or +1 relation.
- **Fix:** "The Court of Oaths reduces diplomatic annexation cost by 10%, increases vassal force limit contribution by 10%, and grants +1 diplomatic relation."

#### S01-5. lane3-dynastic — `verne_noble_charter_modifier_desc`
- **Text:** "The Noble Charter binds the aristocracy to the crown through shared interests."
- **Issue:** No mention of +5% manpower or +10% nobles loyalty.
- **Fix:** "The Noble Charter grants +5% manpower and +10% nobles loyalty, binding the aristocracy to the crown."

#### S01-6. lane5-redcourt — `verne_battle_mage_collegium_modifier_desc`
- **Text:** "The Battle Mage Collegium gives Verne's armies a devastating arcane edge."
- **Issue:** "Devastating arcane edge" doesn't mention +5% morale of armies.
- **Fix:** "The Battle Mage Collegium grants +5% morale of armies, giving Verne's forces a devastating arcane edge."

---

### S02: Variable Tracking (3 issues)

#### S02-1. lane4-trade — `A33_charter_overseas_companies`
- **Text:** `change_variable = { name = verne_overseas_projection add = 1 }` in effects block
- **Issue:** Variable `verne_overseas_projection` is changed without a `custom_tooltip` explaining this to the player. Also uses a tracking modifier `verne_overseas_projection_add_1` that has no localisation.
- **Fix:** Add `custom_tooltip = verne_overhaul_tt_overseas_projection_gain` and add localisation for the tracking modifier.

#### S02-2. lane4-trade — `A33_distant_horizons_expansion`
- **Text:** `change_variable = { name = verne_overseas_projection add = 1 }` and `change_variable = { name = verne_world_network add = 1 }` in effects block
- **Issue:** Both `verne_overseas_projection` AND `verne_world_network` are changed without any `custom_tooltip`.
- **Fix:** Add `custom_tooltip = verne_overhaul_tt_overseas_projection_gain` and `custom_tooltip = verne_overhaul_tt_world_network_gain`.

#### S02-3. lane4-trade — `A33_overseas_commanderies` (implicit)
- **Text:** Capstone mission — no variable changes shown, but if `verne_overseas_projection` advances further here, it needs a tooltip.
- **Issue:** Design doesn't show variable changes for this mission, but the tracking modifier `verne_overseas_projection_add_1` from mission 1 suggests a tracking system is intended but incomplete.
- **Fix:** Clarify whether this mission advances variables. If yes, add tooltips. Remove or localise the debug modifier.

---

### S03: Prerequisite Tooltips (5 issues)

#### S03-1. lane5-redcourt — `A33_establish_red_court`
- **Text (desc):** "Found Verne's arcane advisory council to study magical knowledge for statecraft."
- **Conditions:** `has_institution = renaissance`, `has_reform = verne_red_court_arcana_reform`, `any_owned_province = { has_building = university }`
- **Issue:** Description doesn't mention needing the Renaissance institution, a specific reform, or a university building. Player won't know prerequisites from the tooltip.
- **Fix:** Add `custom_trigger_tooltip` or revise desc: "With the Renaissance embraced, a university built, and the Red Court Arcana reform enacted, found Verne's arcane advisory council."

#### S03-2. lane5-redcourt — `A33_dragonwake_ordinance`
- **Text (desc):** "Formalize Verne's war magic doctrine based on ancient dragon resonance."
- **Conditions:** `has_reform = verne_dragonwake_ordinance_reform`
- **Issue:** Doesn't mention needing the Dragonwake Ordinance reform specifically.
- **Fix:** Revise desc: "Enact the Dragonwake Ordinance reform to formalize Verne's war magic doctrine."

#### S03-3. lane8-faith — `A33_corinite_stewardship`
- **Text (desc):** "Formalize Verne's role as guardian and patron of the Corinite faith."
- **Conditions:** `religion = corinite`, `OR = { has_reform = verne_apostolic_court_of_corin_reform; hasAdvisor = corinite_missionary }`
- **Issue:** Doesn't mention requiring Corinite religion specifically, nor the reform/advisor alternatives.
- **Fix:** Revise desc: "As a Corinite nation with the Apostolic Court reform or a Corinite missionary advisor, formalize Verne's role as faith guardian."

#### S03-4. lane8-faith — `A33_pearlescent_concord`
- **Text (desc):** "Unite Corinite nations under a shared religious diplomatic framework."
- **Conditions:** `has_country_flag = verne_corinite_founded`, `full_idea_group = verne_doctrine_pearlescent_concord`, `OR = { has_reform = verne_apostolic_court_of_corin_reform; has_reform = verne_vernissage_charter_reform; diplomatic_reputation = 3 }`
- **Issue:** Three critical prerequisites not mentioned: completing the Pearlescent Concord idea group, having a specific reform or 3+ diplo rep, and the Corinite Stewardship flag. Player sees only flavour text.
- **Fix:** Revise desc: "With the Pearlescent Concord idea group completed and either the Apostolic Court reform, Vernissage Charter, or 3+ diplomatic reputation, unite Corinite nations."

#### S03-5. lane5-redcourt — `A33_battle_mage_collegium`
- **Text (desc):** "Establish a permanent institution for training mage-soldiers."
- **Conditions:** `has_reform = verne_battle_mage_collegium_reform`, `province_id = 288`, `has_building = university`
- **Issue:** Doesn't mention needing a university specifically in Heartspier (province 288), nor the Collegium reform. Also, `province_id = 288` + `has_building = university` at country scope is incorrect scripting (should be inside a province scope or use `any_owned_province`).
- **Fix:** Revise desc: "With the Battle Mage Collegium reform enacted and a university in Heartspier, establish a permanent institution for training mage-soldiers." Fix scope: `any_owned_province = { province_id = 288 has_building = university }`.

---

### S04: Cross-References (1 issue)

#### S04-1. lane8-faith — `A33_pearlescent_concord`
- **Text (conditions):** `has_reform = verne_vernissage_charter_reform`
- **Issue:** References `verne_vernissage_charter_reform` but the design doc for Lane 0 (redesign-existing) also uses `verne_charter_of_the_vernissage_reform`. Two different names for the same reform — cross-referencing is ambiguous.
- **Fix:** Verify which reform ID is the correct one in the codebase. Standardise to one name across all lane docs. (Note: Lane 0's `verne_charter_of_the_vernissage_reform` may be the correct existing name.)

---

### S05: Terminology (2 issues)

#### S05-1. lane4-trade — `verne_overseas_projection_add_1`
- **Text:** Modifier name `verne_overseas_projection_add_1` used as a tracking/debug modifier
- **Issue:** This appears to be a debug modifier with no player-facing localisation. If it's meant to be visible to players, it needs a proper name and description. If it's debug-only, it shouldn't appear in the design doc as a mission effect.
- **Fix:** Either add proper localisation (`verne_overseas_projection_add_1: "Overseas Projection"`) or remove from the effects block and use only `change_variable` + `custom_tooltip`.

#### S05-2. lane5-redcourt — `A33_fifth_sloth` wrapper name
- **Text:** `Wrapper: A33_fifth_sloth` with note "(typo preserved from existing code)"
- **Issue:** The wrapper name contains "sloth" instead of "slot". While acknowledged as preserved, it will appear in any dev-facing documentation and could confuse future contributors. Not a player-facing typo but a dev-facing terminology issue.
- **Fix:** Add a prominent comment in the implementation code: `# NOTE: A33_fifth_sloth is intentional — typo from original Verne code. Do NOT "correct" to fifth_slot.`

---

## Lane-by-Lane Compliance Matrix

| Lane | S01 | S02 | S03 | S04 | S05 | Issues |
|------|-----|-----|-----|-----|-----|--------|
| lane0-redesign-existing | ✅ | ✅ | ✅ | ✅ | ✅ | 0 (design doc, not player-facing) |
| lane1-court | ❌ (2) | ✅ | ✅ | ✅ | ✅ | 2 |
| lane2-maritime | ✅ | ✅ | ✅ | ✅ | ✅ | 0 |
| lane3-dynastic | ❌ (1) | ✅ | ✅ | ✅ | ✅ | 1 |
| lane4-trade | ✅ | ❌ (3) | ✅ | ✅ | ❌ (1) | 4 |
| lane5-redcourt | ❌ (1) | ✅ | ❌ (3) | ✅ | ❌ (1) | 5 |
| lane6-legitimacy | ✅ | ✅ | ✅ | ✅ | ✅ | 0 |
| lane8-faith | ❌ (2) | ✅ | ❌ (2) | ❌ (1) | ✅ | 5 |

**Best lanes:** lane0, lane2, lane6 (0 issues each)
**Worst lanes:** lane5-redcourt, lane8-faith (5 issues each)

---

## Prioritised Fix List

### High Priority (affects player understanding)
1. **S02-1, S02-2** (lane4): Add `custom_tooltip` for `verne_overseas_projection` and `verne_world_network` variable changes — players currently get zero feedback when these hidden variables change.
2. **S03-1** (lane5): `A33_establish_red_court` prerequisites completely opaque — needs university, Renaissance, and reform listed.
3. **S03-4** (lane8): `A33_pearlescent_concord` has 3 hidden prerequisites — idea group, reform alternatives, and flag from prior mission.
4. **S03-3** (lane8): `A33_corinite_stewardship` doesn't mention Corinite religion requirement.

### Medium Priority (modifier clarity)
5. **S01-1 through S01-6**: All modifier descriptions using vague language instead of specific numbers. Fix in localisation file.

### Low Priority (clean-up)
6. **S04-1** (lane8): Resolve reform name inconsistency (`verne_vernissage_charter_reform` vs `verne_charter_of_the_vernissage_reform`).
7. **S05-1** (lane4): Clean up debug modifier `verne_overseas_projection_add_1`.
8. **S05-2** (lane5): Document the `fifth_sloth` typo preservation.

---

## Recommendations for Implementation

1. **Create shared tooltip keys** for S02 fixes: `verne_overhaul_tt_overseas_projection_gain` and `verne_overhaul_tt_world_network_gain` (may already exist from earlier S02 fix on existing missions — check `verne_overhaul_l_english.yml`).

2. **Batch localisation fixes** for S01: Update 6 `_modifier_desc` entries in the localisation file to include specific numbers. These are single-line edits.

3. **Add `custom_trigger_tooltip`** for S03: Use EU4's `custom_trigger_tooltip` feature in missions with hidden prerequisites to explain gates to players.

4. **Verify reform names** for S04: Check `common/government_reforms/verne_overhaul_reforms.txt` for the correct ID of the Vernissage Charter reform and update all references.

5. **Audit `A33_battle_mage_collegium`** scope (S03-5): The `province_id = 288 has_building = university` at country scope is a scripting bug. Must be wrapped in `any_owned_province = { ... }`.
