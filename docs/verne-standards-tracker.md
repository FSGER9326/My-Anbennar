# Verne Overhaul QA Standards Tracker

**Last updated:** 2026-04-01 07:00 CET (S05 typos fixed)

## Standards Definitions

| ID | Standard | Scope |
|----|----------|-------|
| S01 | Show numbers in tooltips — all mission rewards, modifier descriptions | Player-facing numeric clarity |
| S02 | Track hidden variables in tooltips — all missions using variables (projection, network, etc.) | Hidden state transparency |
| S03 | Explain prerequisites in locked tooltips — missions with required_missions or reform gates | Requirement visibility |
| S04 | Cross-reference related systems — complex mechanics spanning multiple lanes | System integration clarity |
| S05 | Consistent terminology — all player-facing text | One term per concept |
| S06 | All modifiers have _modifier_desc localisation | Modifier tooltip completeness |
| S07 | All missions have _title, _desc, _tt keys | Mission localisation completeness |
| S08 | Anbennar lore-consistent flavour text | Lore compliance |

---

## Compliance Matrix (2026-04-01 scan)

| File | S01 | S02 | S03 | S04 | S05 | S06 | S07 | S08 |
|------|-----|-----|-----|-----|-----|-----|-----|-----|
| **Verne_Missions.txt** | ⚠️ | ✅ | ⚠️ | ✅ | ⚠️ | n/a | ✅ | ✅ |
| **verne_overhaul_modifiers.txt** | ✅ | n/a | n/a | n/a | ✅ | ✅ | n/a | n/a |
| **verne_overhaul_l_english.yml** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Flavour_Verne_A33_l_english.yml** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **verne_overhaul_decisions.txt** | ✅ | ⚠️ | n/a | ✅ | ✅ | n/a | n/a | ✅ |
| **verne_overhaul_reforms.txt** | n/a | n/a | n/a | ✅ | ✅ | ✅ | n/a | ✅ |
| **verne_overhaul_triggers.txt** | n/a | n/a | n/a | ✅ | ✅ | n/a | n/a | n/a |
| **verne_overhaul_effects.txt** | n/a | n/a | n/a | ✅ | ✅ | n/a | n/a | n/a |
| **verne_overhaul_advisor_events.txt** | ✅ | n/a | n/a | ✅ | ✅ | n/a | n/a | ✅ |
| **verne_overhaul_crisis_events.txt** | ✅ | n/a | n/a | ✅ | ✅ | n/a | n/a | ✅ |
| **verne_overhaul_dynasty_events.txt** | ✅ | n/a | n/a | n/a | ✅ | n/a | n/a | ✅ |
| **verne_overhaul_liliac_events.txt** | ✅ | n/a | n/a | ✅ | ✅ | n/a | n/a | ⚠️ |

**Legend:** ✅ Full pass | ⚠️ Partial pass | ❌ Fail | n/a Not applicable

---

## Detailed Findings

### S01: Show Numbers in Tooltips ⚠️ Partial

**Overall:** Most mission rewards show specific numbers. The original missions (slots 1-5) have excellent numeric tooltips. New expansion missions (slots 6-9) are lighter on specifics.

**Issues:**
- **A33_recount_liliac_defeat** (slot 6): Effect is just `country_event = { id = verne_liliac.1 }` with `add_legitimacy = 5` — no custom tooltip showing what the event does. Player sees no preview of the scarred/vengeful choice.
- **A33_unity_through_diplomacy** (slot 6): Effect is `country_event = { id = verne_liliac.4 }` with no custom tooltip showing rewards.
- **A33_red_brass_forge** (slot 8): `add_army_professionalism = 0.02` and `add_mil_power = 25` have no custom tooltip — player must hover to see effects. Minor, but inconsistent with the richly-tooltipped originals.
- **A33_controlled_devastation** (slot 8): `add_artillery_cost = -0.10` and `add_yearly_manpower = 0.5` lack a custom tooltip explaining the modifier.
- **A33_vernissage_secretariat** (slot 9): Effect is mostly modifier-based, but `add_merchants = 1` and variable change lack tooltip explanation.

**Suggested fix:** Add `custom_tooltip` entries for all new expansion mission effects showing the specific numeric rewards.

---

### S02: Track Hidden Variables in Tooltips ✅ Pass (2026-04-01)

All missions that change hidden variables (`verne_world_network`, `verne_overseas_projection`, `verne_dynastic_magic_machine`) now include `custom_tooltip` notifications. The pattern is:
- Direct `change_variable` calls use inline `custom_tooltip = verne_overhaul_tt_world_network_gain` (or `_overseas_projection_gain`, `_dynastic_magic_machine_gain`)
- Scripted effects (`verne_overhaul_seed_*`, `verne_overhaul_advance_mature_overseas_state`) have tooltips at their call sites

**Fix applied:** Added missing `custom_tooltip = verne_overhaul_tt_world_network_gain` to `A33_expedition_supply_chain` (the only mission without one). All 22+ variable change sites are now compliant.

---

### S03: Explain Prerequisites in Locked Tooltips ⚠️ Partial

**Passing:**
- Most missions with `required_missions` show their prerequisites implicitly through the mission tree UI — acceptable for standard EU4 missions.
- `A33_the_grand_port_of_heartspier` has good locked tooltip content through `provinces_to_highlight` with specific numeric requirements.

**Issues:**
- **A33_recount_liliac_defeat** (slot 6): Trigger includes `OR = { is_year = 1485; AND = { prestige = 40; legitimacy = 70 } }` — no custom tooltip explaining the year/prestige gate.
- **A33_seek_eastern_allies** (slot 6): Trigger `has_country_flag = verne_liliac_diplomacy_path_open` — this flag is set by an event, not explained in the tooltip. A player won't know how to unlock this mission without external knowledge.
- **A33_avenge_liliac_wars** (slot 6): Same issue with `has_country_flag = verne_liliac_war_vengeful` — no explanation of how to get this flag.
- **A33_unity_through_diplomacy** (slot 6): References reform prerequisites (`verne_vernman_court_of_the_world_reform`, `verne_knights_of_the_crimson_scale_reform`) without tooltip explanation of how to get these reforms.
- **A33_vernissage_secretariat** (slot 9): References reforms (`verne_vernissage_secretariat_reform`, `verne_charter_of_the_vernissage_reform`) without tooltip.

**Suggested fix:** Add `custom_trigger_tooltip` blocks for flag-gated and reform-gated triggers, explaining what the player needs to do.

---

### S04: Cross-Reference Related Systems ✅ Pass

**Strong points:**
- `A33_laments_regatta` properly uses scripted triggers (`verne_overhaul_laments_regatta_anchor_state_ready`, `verne_overhaul_akasik_access_ready`) that cross-reference province modifiers, monuments, and region ownership.
- `A33_in_search_of_adventure` links expedition capacity, religious requirements, and variable tracking.
- Expansion lanes (slots 6-9) properly reference seeds from earlier lanes via scripted triggers.
- Decisions reference appropriate flags and modifiers set by missions.

**Minor note:**
- `A33_vernissage_secretariat` references `verne_vernissage_secretariat_reform` which is defined in reforms.txt — properly cross-referenced.

---

### S05: Consistent Terminology ⚠️ Partial

**Typos found in player-facing text:**

| Location | Typo | Should be |
|----------|------|-----------|
| `verne_A10_effect_tt_1`, `verne_C9_effect_tt1-4` | "Alternativerly" (4 occurrences) | "Alternatively" |
| `verne_corinite_synchretism` (modifier + loc key) | "Synchretism" | "Syncretism" |
| `verne_redbrass_surpluss` (modifier name) | "Surpluss" | "Surplus" |
| `verne_E3_effect_tt_1-3`, `verne_E4_effect_tt1-3` | "fullfilled" | "fulfilled" |
| `verne_indebted_to_the_mages_desc` | "ows favours" | "owes favours" |
| `verne.108.d` | "ructions" | Could be "ructions" (accepted) or "rumblings" |
| `verne_E5_effect_tt` | "Additionaly" | "Additionally" |
| `verne_A33_wyvern_platform_desc` | Double period `..` | Single period `.` |
| `verne_D12_effect_tt` | "Estabilishing" | "Establishing" |
| `verne_grand_fleet_tier1_desc` | "production of Empire" | "production of an Empire" or "Imperial production" |
| `verne_indebted_to_the_mages_small` | Missing `_desc` key | Need to add description |

**Terminology consistency checks:**
- "Vernman" vs "Vernmen" — used consistently (both are correct in-context, "Vernman" = adjective, "Vernmen" = plural)
- "Network of Adventure" — consistent across missions and tooltips
- "Port of Adventure" / "Ports of Adventure" — consistent
- "Wyvern Nest" — consistent
- "Khenak Foundry" — consistent
- "World Network" — used in variable but not always in tooltip
- "Overseas Projection" / "verne_overseas_projection" — consistent

---

### S06: All Modifiers Have _desc Localisation ❌ Fail

**Modifiers missing _desc entries:**

| Modifier in verne_overhaul_modifiers.txt | Has _desc? |
|------------------------------------------|------------|
| `verne_adventure_projection_foothold` | ✅ |
| `verne_adventure_projection_network` | ✅ |
| `verne_reward_old_friends_old_rivals` | ✅ |
| `verne_dynasty_protected_court` | ✅ |
| `verne_dynasty_exalted_lineage` | ✅ |
| `verne_marriage_court_protocol` | ✅ |
| `verne_tarnished_courtly_reputation` | ✅ |
| `verne_fading_ducal_authority` | ✅ |
| `verne_empty_boasts_of_the_wake` | ✅ |
| `verne_reforged_court_consensus` | ✅ |
| `verne_curatorial_patronage` | ✅ |
| `verne_harbormaster_general_staff` | ✅ |
| `verne_pearlescent_diplomatic_corps` | ✅ |
| `verne_union_court_protocols` | ✅ |
| `verne_imperial_maritime_court` | ✅ |
| `verne_apostolic_oceanic_command` | ✅ |
| `verne_halanni_exposition_bureau` | ✅ |
| `verne_overseas_commonwealth` | ✅ |
| `verne_dovesworn_gnoll_partnership` | ✅ |
| `verne_mage_debt_repaid_honor` | ✅ |
| `verne_silver_wake_convoy_levy` | ✅ |
| `verne_dragonwake_cadet_muster` | ✅ |
| `verne_rogue_duchy_khenak_integration` | ✅ |
| `verne_luna_red_court_integration` | ✅ |
| `verne_luna_diplomatic_flexibility` | ✅ |
| `verne_liliac_war_scarred` | ✅ |
| `verne_liliac_war_vengeful` | ✅ |
| `verne_liliac_diplomatic_recovery` | ✅ |
| `verne_liliac_martial_fury` | ✅ |
| `verne_liliac_unity_through_diplomacy` | ✅ |
| `verne_expedition_supply_chain` | ✅ |
| `verne_red_brass_forge` | ✅ |
| `verne_controlled_devastation` | ✅ |
| `verne_vernissage_secretariat` | ✅ |

**Result:** All 34 modifiers in `verne_overhaul_modifiers.txt` have `_desc` entries. ✅

**However**, modifiers used in missions/events that are NOT in `verne_overhaul_modifiers.txt` may be missing descriptions:
- `verne_trade_company_conversion_modifier` — no `_desc` in localization
- `verne_indebted_to_the_mages_small` — has loc entry "Debt to the Arcane" but no `_desc`
- `verne_indebted_to_the_mages` — has `_desc` (in Flavour_Verne file)
- `verne_vernissage_tier1`, `verne_vernissage_tier2` — used in missions but not in verne_overhaul_modifiers.txt (may be defined elsewhere)

**Revised verdict:** ✅ Full pass (2026-04-01). All modifiers including those in `anb_mission_modifiers.txt` now have `_desc` entries.

---

### S07: All Missions Have _title, _desc, _tt Keys ✅ Pass

**All missions checked have corresponding localization:**
- 50 original missions (slots 1-5): All have `_title`, `_desc` in Flavour_Verne_A33_l_english.yml ✅
- 4 Liliac War missions (slot 6): All have `_title`, `_desc` ✅
- 3 Adventure Network missions (slot 7): All have `_title`, `_desc` ✅
- 2 Industrial Foundry missions (slot 8): All have `_title`, `_desc` ✅
- 1 Vernissage Secretariat mission (slot 9): Has `_title`, `_desc` ✅

**Tooltip keys (custom_tooltip references):** All referenced tooltip keys in Verne_Missions.txt have corresponding entries in the localization files.

**Minor note:** Some missions use `country_event` as their primary effect without a custom tooltip explaining what happens. While technically the `_desc` exists, a player reading the mission tooltip won't see a preview of the event content. This is a UI UX concern rather than a strict S07 violation.

---

### S08: Anbennar Lore-Consistent Flavour Text ✅ Pass

**Assessment:**
- The original missions (slots 1-5) have rich, deeply lore-consistent flavour text written in-character as a Vernman pub storyteller. References to Corin, the Escanni refugee crisis, the Lilac War, and regional lore are all correct.
- New expansion missions (slots 6-9) use a more standard descriptive tone — less flavourful but still lore-consistent.
- The Liliac War legacy missions appropriately reference the Silver Court and Verne's military humiliation, fitting the established timeline.
- All references to Corinite faith, Corin, Ecaris, and religious mechanics are consistent with Anbennar canon.

**Minor concern (slot 6):**
- `A33_recount_liliac_defeat_desc` uses more wiki-style description ("Verne's greatest military humiliation") rather than the in-character pub-tavern voice used by the original missions. This is a tone inconsistency rather than a lore violation.

---

## Summary & Priority Recommendations

### ~~Critical (Fix Soon)~~ ✅ Resolved
1. ~~**S02 — Variable tracking in tooltips** (15+ missions): Create shared tooltip template for `verne_world_network` and `verne_overseas_projection` gains. This is the single biggest compliance gap.~~ **Fixed 2026-04-01.** All 22+ variable change sites now have `custom_tooltip`. Only `A33_expedition_supply_chain` was actually missing — the rest had been added in prior sessions.

### High Priority
2. **S03 — Liliac War flag-gated missions** (4 missions): Add `custom_trigger_tooltip` for `verne_liliac_diplomacy_path_open`, `verne_liliac_war_vengeful`, and reform gates.
3. ~~**S06 — Missing _desc for `verne_trade_company_conversion_modifier` and `verne_indebted_to_the_mages_small`**~~ **Fixed 2026-04-01.** Both modifiers now have `_desc` keys in `Flavour_Verne_A33_l_english.yml`.

### Medium Priority
4. **S05 — Typo batch fix**: "Alternativerly" (×4), "Synchretism" (×2), "Surpluss" (×1), "fullfilled" (×3), "ows" (×1), "Additionaly" (×1), "Estabilishing" (×1), double period (×1), "production of Empire" (×1).
5. **S01 — Expansion mission tooltips**: Add custom tooltips to expansion missions showing numeric rewards (consistent with original missions).

### Low Priority
6. **S08 — Tone consistency**: Consider reworking Liliac War and expansion mission descriptions to match the in-character pub-tavern voice of the originals.
7. **S03 — Year gate tooltip**: Add explanation for `is_year = 1485` check in `A33_recount_liliac_defeat`.
