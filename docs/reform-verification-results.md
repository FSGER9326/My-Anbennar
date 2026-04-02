# Reform Verification Results

**Generated:** 2026-04-01  
**Task:** Verify all government reform references in lane design docs exist in codebase

## Summary

| Category | Count |
|----------|-------|
| Reforms in both design docs AND codebase ✅ | 15 |
| Reforms in docs but NOT in codebase ❌ | 2 |
| Reforms in codebase but NOT referenced in docs 🆕 | 8 |

---

## ✅ Reforms Found in Both Design Docs and Codebase (15)

| Reform ID | Lane / Doc |
|-----------|------------|
| `verne_admiralty_of_the_crimson_wake_reform` | lane2-maritime.txt |
| `verne_apostolic_court_of_corin_reform` | lane8-faith.txt |
| `verne_battle_mage_collegium_reform` | lane5-redcourt-arcane.txt |
| `verne_charter_of_great_captains_reform` | lane1-court-oaths.txt |
| `verne_charter_of_the_vernissage_reform` | lane8-faith.txt |
| `verne_court_of_silver_oaths_reform` | lane1-court-oaths.txt |
| `verne_dragonwake_ordinance_reform` | lane5-redcourt-arcane.txt |
| `verne_estuary_companies_of_heartspier_reform` | lane4-trade-colonisation.txt |
| `verne_hall_of_distant_horizons_reform` | lane4-trade-colonisation.txt |
| `verne_imperial_sea_court_reform` | lane2-maritime.txt |
| `verne_overseas_commanderies_reform` | lane4-trade-colonisation.txt |
| `verne_red_court_arcana_reform` | lane5-redcourt-arcane.txt |
| `verne_regatta_discipline_reform` | lane2-maritime.txt |
| `verne_throne_of_the_wyvern_kings_reform` | lane3-dynastic.txt |
| `verne_vernman_court_of_the_world_reform` | lane8-faith.txt |

## ❌ Reforms Referenced in Docs but NOT Defined in Codebase (2)

| Reform ID | Referenced In | Status |
|-----------|--------------|--------|
| `verne_overhaul_reform` | lane2-maritime.txt, verne-10-lane-blueprint.md, implementation-audit-current-repo.md, implementation-scaffolding.md | **MISSING** — likely a placeholder or renamed; needs definition or removal |
| `verne_exalted_dynasty_machine_reform` | lane3-dynastic.txt | **MISSING** — referenced in dynastic lane but no definition exists |

## 🆕 Reforms Defined in Codebase but NOT Referenced in Any Design Doc (8)

| Reform ID | File | Notes |
|-----------|------|-------|
| `verne_crimson_eyrie_commandery_reform` | verne_overhaul_reforms.txt | Not in any lane doc |
| `verne_ducal_muster_of_armoc_reform` | verne_overhaul_reforms.txt | Not in any lane doc |
| `verne_knights_of_the_crimson_scale_reform` | verne_overhaul_reforms.txt | Not in any lane doc |
| `verne_sea_nest_ascendancy_reform` | verne_overhaul_reforms.txt | Not in any lane doc |
| `verne_secretariat_of_the_grand_regatta_reform` | verne_overhaul_reforms.txt | Not in any lane doc |
| `verne_storm_crowned_hegemony_reform` | verne_overhaul_reforms.txt | Not in any lane doc |
| `verne_the_crimson_world_order_reform` | verne_overhaul_reforms.txt | Not in any lane doc |
| `verne_vernissage_secretariat_reform` | verne_overhaul_reforms.txt | Not in any lane doc |

---

## Action Items

1. **`verne_overhaul_reform`** — Referenced in 4 docs but never defined. Either:
   - It's a placeholder/alias that should be defined in `verne_overhaul_reforms.txt`, or
   - It was renamed and all references should be updated, or
   - References should be removed if the concept was dropped.

2. **`verne_exalted_dynasty_machine_reform`** — Referenced in lane3-dynastic.txt but no definition exists. Needs to be created or the lane doc updated to use an existing reform.

3. **8 orphaned reforms** — Defined in code but not referenced in any design doc. Consider:
   - Adding them to appropriate lane docs (e.g., maritime reforms to lane2, court reforms to lane1, etc.), or
   - Documenting why they exist independently (standalone reforms not tied to lanes).
