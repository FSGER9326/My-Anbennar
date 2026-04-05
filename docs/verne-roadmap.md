# Verne Roadmap

## Status: 10-Lane Blueprint — Design Phase COMPLETE

All 10 lane design docs written and committed (2026-04-01).

### Lane Overview

| # | Lane | File | Status |
|---|------|------|--------|
| 1 | Court & Oaths | `lane1-court-oaths.txt` | ✅ IMPLEMENTED (9 missions) |
| 2 | Adventure Network | `lane2-adventure-network.txt` | ✅ IMPLEMENTED (6 missions) |
| 3 | Maritime Empire | `lane3-maritime-empire.txt` | ✅ IMPLEMENTED (8 missions) |
| 4 | Dynastic Machine | `lane4-dynastic-machine.txt` | ✅ IMPLEMENTED (8 missions) |
| 5 | Trade & Colonisation | `lane4-trade-colonisation.txt` | 🔶 PARTIAL (8 of 10 missions, wyvern+trade) |
| 6 | Red Court & Arcane | `lane5-redcourt-arcane.txt` | 🔶 PARTIAL (3 new + 2 gates in slot 5) |
| 7 | Military Orders | `lane7-military-orders.txt` | 🔶 PARTIAL (scattered across slots 3-5) |
| 8 | Faith & Apostolic Empire | `lane8-faith.txt` | 🔶 PARTIAL (6 missions across slots 3-5) |
| 9 | Industrial Foundries | `lane9-industrial-foundries.txt` | 🔶 PARTIAL (3 missions, Khenak chain) |
| 10 | Diplomacy & Liliac War | `lane10-diplomacy-liliac.txt` | ✅ IMPLEMENTED (4 missions, branch design) |

### Implementation Notes

- **Design-implementation reconciliation:** ✅ DONE — all lanes mapped to actual codebase missions
- **Lane 5 file naming:** `lane4-trade-colonisation.txt` reused (old file overwritten) to match slot numbering from blueprint
- **Parallel content:** Lanes 5 & 6 share slot 5 (A33_fifth_sloth); position interleaving documented
- **Scattered missions:** Lanes 7 & 8 have missions across slots 3-5; no dedicated slot blocks yet

## Recent Fixes & Findings

- **2026-04-05 — CRITICAL: 6 undefined scripted triggers found** — mission blockers. EU4 treats undefined scripted triggers as always `false`. All 6 must be defined in `common/scripted_triggers/verne_overhaul_triggers.txt`:
  - `verne_overhaul_akasik_access_ready`
  - `verne_overhaul_laments_regatta_anchor_state_ready`
  - `verne_overhaul_in_search_expedition_capacity`
  - `verne_overhaul_in_search_network_or_monument_route`
  - `verne_overhaul_in_search_subject_projection_route`
  - `verne_overhaul_early_akasik_access_route`
  - Also: `verne_wyvern_nest_initialized` flag never set → `A33_might_of_the_wyvern` permanently unavailable
  - Fix: create `common/scripted_triggers/verne_overhaul_triggers.txt` with trigger definitions; set flag in wyvern nest event
  - See `docs/verne-audit/2026-04-05-deep-audit.md` and `docs/inspiration-bank.md` (Scripted Triggers section)

- **2026-04-01 — 10-lane design docs complete:** All 6 remaining lanes (5-10) rewritten/created with actual mission IDs, modifiers, reform gates, and cross-lane dependencies.
- **2026-04-01 — Reform verification pass:** Cross-checked all 17 government reform IDs referenced in lane design docs against `common/government_reforms/` definitions.
  - ✅ 15 reforms exist in both docs and codebase
  - ❌ 2 reforms referenced but missing: `verne_overhaul_reform` (used in lane2 + 3 other docs), `verne_exalted_dynasty_machine_reform` (used in lane3)
  - 🆕 8 codebase reforms not referenced in any design doc (e.g., `verne_crimson_eyrie_commandery_reform`, `verne_knights_of_the_crimson_scale_reform`, etc.)
  - See `reform-verification-results.md` for full details.

## Needs Human Input

- [ ] Authoritative design intent: what should `verne_overhaul_in_search_expedition_capacity` actually check? (colonists? treasury? custom variable?)
- [ ] Authoritative design intent: what should `verne_overhaul_laments_regatta_anchor_state_ready` represent? (coastal dev threshold? specific port building?)
- [ ] Which wyvern nest event should set `verne_wyvern_nest_initialized`? Existing Verne event ID or new one?

## Planned

### Implementation gaps (missions in design docs but NOT in codebase):
- Lane 5: `A33_establish_trade_network`, `A33_vernman_merchant_marine`, `A33_spice_route_monopoly`
- Lane 7: `A33_found_the_crimson_scale_order` (gates existing reform), military order slot block
- Lane 8: `A33_corinite_stewardship`, `A33_pearlescent_concord`, `A33_world_faith_emperor`
- Lane 9: `A33_expand_the_foundry_complex`, `A33_khenak_steel_program`

### Architecture decisions needed:
- Dedicated slot blocks for Lanes 7-9 (currently share slots 3-5)
- Lane 5/6 interleaving — consider splitting slot 5 into separate blocks
- Verne.200 event — referenced by Battle Mage Collegium but not verified in events/
