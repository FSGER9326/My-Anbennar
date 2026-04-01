# Government Reform Verification Report

**Date:** 2026-04-01 03:05 CET  
**Source:** `common/government_reforms/verne_overhaul_reforms.txt` (24 reforms defined)  
**Cross-referenced against:** `docs/design/lanes/*.txt` (16 unique reform refs) + `docs/verne-roadmap.md` (14 reforms listed)

---

## Roadmap Reforms (Priority 8 — verified)

| # | Reform (Roadmap) | Status | Codebase Location |
|---|---|---|---|
| 1 | `verne_court_of_oaths_reform` | ⚠️ **NAME MISMATCH** | Line 9 — actual name: `verne_court_of_silver_oaths_reform` |
| 2 | `verne_crown_of_the_oathkeeper_reform` | ❌ **MISSING** | Not found anywhere in repo |
| 3 | `verne_estuary_companies_of_heartspier_reform` | ✅ Exists | `verne_overhaul_reforms.txt` line 73 |
| 4 | `verne_admiralty_of_the_crimson_wake_reform` | ✅ Exists | `verne_overhaul_reforms.txt` line 58 |
| 5 | `verne_imperial_sea_court_reform` | ✅ Exists | `verne_overhaul_reforms.txt` line 264 |
| 6 | `verne_throne_of_the_wyvern_kings_reform` | ✅ Exists | `verne_overhaul_reforms.txt` line 345 |
| 7 | `verne_exalted_dynasty_machine_reform` | ❌ **MISSING** | Not found anywhere in repo |
| 8 | `verne_hall_of_distant_horizons_reform` | ✅ Exists | `verne_overhaul_reforms.txt` line 169 |
| 9 | `verne_overseas_commanderies_reform` | ✅ Exists | `verne_overhaul_reforms.txt` line 279 |
| 10 | `verne_red_court_arcana_reform` | ✅ Exists | `verne_overhaul_reforms.txt` line 108 |
| 11 | `verne_dragonwake_ordinance_reform` | ✅ Exists | `verne_overhaul_reforms.txt` line 122 |
| 12 | `verne_battle_mage_collegium_reform` | ✅ Exists | `verne_overhaul_reforms.txt` line 136 |
| 13 | `verne_apostolic_court_of_corin_reform` | ✅ Exists | `verne_overhaul_reforms.txt` line 297 |
| 14 | `verne_vernman_court_of_the_world_reform` | ✅ Exists | `verne_overhaul_reforms.txt` line 312 |

**Score: 11/14 ✅ | 2 ❌ MISSING | 1 ⚠️ NAME MISMATCH**

---

## Reforms Referenced in Lane Design Docs (extra checks)

All 16 unique reform references from lane design files:

| Reform | Lane(s) | In Codebase? |
|---|---|---|
| `verne_court_of_silver_oaths_reform` | Lane 1 | ✅ Line 9 |
| `verne_throne_of_the_wyvern_kings_reform` | Lane 1, 3, 6 | ✅ Line 345 |
| `verne_estuary_companies_of_heartspier_reform` | Lane 2 | ✅ Line 73 |
| `verne_admiralty_of_the_crimson_wake_reform` | Lane 2, 4 | ✅ Line 58 |
| `verne_regatta_discipline_reform` | Lane 2 | ✅ Line 89 |
| `verne_imperial_sea_court_reform` | Lane 2 | ✅ Line 264 |
| `verne_exalted_dynasty_machine_reform` | Lane 3 | ❌ **MISSING** |
| `verne_hall_of_distant_horizons_reform` | Lane 4 | ✅ Line 169 |
| `verne_overseas_commanderies_reform` | Lane 4 | ✅ Line 279 |
| `verne_red_court_arcana_reform` | Lane 5 | ✅ Line 108 |
| `verne_dragonwake_ordinance_reform` | Lane 5 | ✅ Line 122 |
| `verne_battle_mage_collegium_reform` | Lane 5 | ✅ Line 136 |
| `verne_crown_of_the_oathkeeper_reform` | Lane 6 | ❌ **MISSING** |
| `verne_apostolic_court_of_corin_reform` | Lane 8 | ✅ Line 297 |
| `verne_vernissage_charter_reform` | Lane 8 | ✅ Line 154 |
| `verne_vernman_court_of_the_world_reform` | Lane 8 | ✅ Line 312 |

**Lane doc score: 14/16 ✅ | 2 ❌ MISSING**

---

## Reforms in Codebase NOT Referenced in Any Lane Design Doc

These 10 reforms exist in `verne_overhaul_reforms.txt` but are never referenced in `docs/design/lanes/`:

| Reform | Line | Notes |
|---|---|---|
| `verne_charter_of_great_captains_reform` | 24 | No lane doc reference |
| `verne_ducal_muster_of_armoc_reform` | 39 | No lane doc reference |
| `verne_wyvern_marshalate_reform` | 202 | No lane doc reference |
| `verne_crimson_eyrie_commandery_reform` | 217 | No lane doc reference |
| `verne_sea_nest_ascendancy_reform` | 231 | No lane doc reference |
| `verne_secretariat_of_the_grand_regatta_reform` | 249 | No lane doc reference |
| `verne_vernissage_secretariat_reform` | 184 | No lane doc reference |
| `verne_knights_of_the_crimson_scale_reform` | 327 | No lane doc reference |
| `verne_the_crimson_world_order_reform` | 359 | No lane doc reference |
| `verne_storm_crowned_hegemony_reform` | 374 | No lane doc reference |

---

## Name Mismatches Detail

| Roadmap Name | Actual Codebase Name | Delta |
|---|---|---|
| `verne_court_of_oaths_reform` | `verne_court_of_silver_oaths_reform` | Missing "silver" in roadmap |
| *(lane 8 doc)* `verne_charter_of_the_vernissage_reform` | `verne_charter_of_the_vernissage_reform` | ✅ Matches |

---

## Missing Reforms — Investigation

### `verne_crown_of_the_oathkeeper_reform` (Lane 6)
- Referenced in `lane6-legitimacy.txt` line 82
- No matching reform definition anywhere in the repo
- **Possible alternatives in codebase:** `verne_charter_of_great_captains_reform`, `verne_storm_crowned_hegemony_reform`
- **Status:** Design doc only — never implemented

### `verne_exalted_dynasty_machine_reform` (Lane 3)
- Referenced in `lane3-dynastic.txt` line 83 as `unlock_reform = verne_exalted_dynasty_machine_reform`
- No matching reform definition anywhere in the repo
- **Possible alternatives in codebase:** `verne_ducal_muster_of_armoc_reform`, `verne_wyvern_marshalate_reform`
- **Status:** Design doc only — never implemented

---

## Summary

| Category | Count |
|---|---|
| Roadmap reforms verified ✅ | 11 |
| Roadmap reforms missing ❌ | 2 |
| Roadmap reform name mismatch ⚠️ | 1 |
| Lane doc reforms verified ✅ | 14 |
| Lane doc reforms missing ❌ | 2 |
| Codebase-only reforms (no lane doc) | 10 |
| Total reforms in codebase | 24 |

**Conclusion:** 2 of the 14 roadmap reforms (`crown_of_the_oathkeeper`, `exalted_dynasty_machine`) were never implemented in the codebase. The roadmap should be updated: `verne_court_of_oaths_reform` → `verne_court_of_silver_oaths_reform`. 10 additional reforms exist in codebase that aren't in any lane design doc, suggesting organic expansion beyond the original blueprint.
