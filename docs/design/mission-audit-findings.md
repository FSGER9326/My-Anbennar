# Mission Integration Audit — 2026-04-02

**Scope:** `missions/Verne_Missions.txt` vs live helper layer  
**Reference files:**
- `common/scripted_triggers/verne_overhaul_triggers.txt` (23 triggers)
- `common/scripted_effects/verne_overhaul_effects.txt` (10 effects)
- `common/event_modifiers/verne_overhaul_modifiers.txt` (65 modifiers)
- `localisation/verne_overhaul_l_english.yml` (81 title keys, 361 desc keys)

---

## CRITICAL: 28 modifiers used in missions but not defined

These modifiers are referenced in `add_country_modifier` / `add_province_modifier` blocks but have no definition in `verne_overhaul_modifiers.txt`. They will be silently ignored by the game.

| Missing Modifier | Likely Source |
|---|---|
| `verne_all_roads_lead_to_verne` | Province modifier |
| `verne_apostles_of_corin` | Mission reward |
| `verne_corinite_halann` | Mission reward |
| `verne_exaltation_of_adventurers` | Mission reward |
| `verne_foreign_doctrines` | Mission reward |
| `verne_grand_fleet_tier1` | Province modifier |
| `verne_grand_fleet_tier2` | Province modifier |
| `verne_impecable_groundwork` | Province modifier |
| `verne_impressment_drive` | Province modifier |
| `verne_indebted_to_the_mages_small` | Country modifier |
| `verne_international_investment` | Province modifier |
| `verne_might_of_the_wyvern` | Province modifier |
| `verne_new_armada` | Province modifier |
| `verne_new_world_monopolies` | Province modifier |
| `verne_off_to_adventure` | Province modifier |
| `verne_redbrass_surplus` | Province modifier |
| `verne_restoring_the_borders` | Province modifier |
| `verne_the_wyvern_king` | Province modifier |
| `verne_the_wyverns_gulf` | Province modifier (Wyvern Gulf, prov 376 area) |
| `verne_tourism_economy` | Province modifier |
| `verne_trade_company_conversion_modifier` | Country modifier |
| `verne_vernissage_tier2` | Province modifier |
| `verne_vernman_era` | Province modifier |
| `verne_wingspan` | Province modifier |
| `verne_wyvern_nest` | Province modifier |
| `verne_wyvern_nest_expanded` | Province modifier |
| `verne_wyvern_nest_grand` | Province modifier |
| `verne_wyvern_nest_no_dlc` | Province modifier (no-DLC fallback) |
| `verne_wyvern_stride` | Province modifier |

**Action:** These need definitions added to `verne_overhaul_modifiers.txt`. Priority order: top 10 most-visible (Wyvern nests, Vernissage tiers, fleet tiers) should be V-01 priority before testing.

---

## CRITICAL: 9 flags checked but never SET anywhere

These `has_country_flag` checks exist in mission triggers but no mission, event, or decision sets these flags.

| Flag | Note |
|---|---|
| `verne_attacked` | Liliac War path — may be set by event |
| `verne_backed_down` | Liliac War path |
| `verne_blue_house_adventure_completed` | Adventure network |
| `verne_liliac_diplomacy_path_open` | Liliac War diplomacy |
| `verne_liliac_vengeful_path` | Liliac War vengeful branch |
| `verne_seed_khenak_foundry` | Should be set by mission or decision |
| `verne_won_support_full` | Expedition/supply chain |
| `verne_won_support_partial` | Expedition/supply chain |

**Action:** Check if these are set by events/decisions. If not, they are broken mission-gate conditions. `verne_seed_khenak_foundry` in particular — this is referenced in the triggers file (`verne_overhaul_has_khenak_foundry_seeded`) so it SHOULD be set somewhere.

---

## WARNINGS: 15 flags set but not referenced in triggers file

These flags are set by missions but the triggers file doesn't check them. Most are likely fine (one-shot event/decision flags), but could indicate orphaned state.

Notable potentially-meaningful flags:
- `verne_dynasty_protected` — dynasty safeguard (referenced elsewhere)
- `verne_seed_estuary_companies` — used in mission effects
- `verne_can_create_wyvern_carriers` — unlock flag
- `verne_unlocked_adventure_system` — adventure network gate

These are likely OK but should be confirmed against the triggers file scope (the triggers file only covers ~20 of the most-reused helper triggers).

---

## LOC: 48 title entries still missing

Status: placeholder `0 "Title"` stubs were added 2026-04-02. These need human-authored titles.

The missions still needing real titles are listed in `automation/reports/mission_truth_report.json`.

---

## What is actually working well

- **58 real missions** correctly parsed with proper slot placement
- **65 modifiers defined** in the modifiers file — broad coverage
- **23 scripted triggers** — meaningful doctrine/path detection logic
- **10 scripted effects** — shared mission reward bundles
- **361 desc loc keys** — all missions have descriptions
- **Zero orphan mission refs** — no broken mission→mission dependencies
- **Zero broken scripted effect calls** — effects referenced do exist

---

## Recommended Priority Fix Order

1. **V-M1:** ✅ DONE — all 31 missing modifier definitions added to `verne_overhaul_modifiers.txt` (commit d88c74208a)
2. **V-M2:** Trace `verne_seed_khenak_foundry` — where is it supposed to be set? Add to the mission or decision that seeds the Khenak path
3. **V-M3:** Audit Liliac War flags (`verne_attacked`, `verne_liliac_*`) — are they set by the Liliac War event chain?
4. **V-M4:** Get human titles for the 48 placeholder missions (ChatGPT or Falk)
