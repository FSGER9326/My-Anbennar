# Mission Dependency Graph Audit — 2026-04-02

## Method
- `mission_dep_graph.py` — state-machine extractor for `required_missions` edges
- Source: `missions/Verne_Missions.txt` (5,200+ lines, 58 missions)
- Slot mapping: inferred from block names (file bug: slots 6-10 all say `slot = 5`)

## Overall Verdict
**STRUCTURALLY SOUND** — 58 missions, 80 edges, 0 orphan edges, 0 cycles.

The graph is a valid DAG. No mission requires a non-existent mission.
No circular dependencies.

---

## Key Finding: Cross-Slot Dependencies Are Intentional

41 of 80 edges are cross-slot. This is **not a bug** — it's the design:
the 10-column lane map intentionally connects lanes (e.g. "take the seas" in
lane 3 unlocks a naval mission in lane 4). The lanes are parallel tracks
with deliberate interconnections, not isolated columns.

The critical UI bug remains: **all slots 6-10 report `slot = 5`** in the
file. Once `max_slots_horizontal = 10` is set, these cross-slot edges
will render correctly as diagonal connectors between columns 6-10.

---

## 6 Root Missions (Entry Points)
No prerequisites — available from game start.

| Mission | Slot | Theme |
|---------|------|-------|
| A33_the_vernman_renaissance | 1 | Court & Oaths — Vernman heritage |
| A33_alvars_reforms | 2 | Adventure Network — Alvar's reform era |
| A33_old_friends_old_rivals | 3 | Maritime Empire — old rivalries |
| A33_corins_shield | 3 | Faith — Corinite foundation |
| A33_break_the_queen_of_the_hill | 5 | Red Court & Arcane — queen of the hill crisis |
| A33_recount_liliac_defeat | 6 | Diplomacy / Liliac War legacy |

**Assessment:** Appropriate entry points. The tree has multiple starting
frontiers rather than a single linear start — fits Verne's "silver-court
naval monarchy" identity with multiple thematic axes.

---

## 7 Terminal Missions (End States)
Nothing depends on these — final nodes of their chains.

| Mission | Slot | Theme |
|---------|------|-------|
| A33_project_holohana | 1 | ??? (Hawaiian name — possible lore mismatch?) |
| A33_the_verne_halann | 3 | Maritime — Verne's control of Halann |
| A33_ports_of_adventure_program | 7 | Military Orders — expeditionary program |
| A33_expedition_supply_chain | 7 | Military Orders — expedition logistics |
| A33_controlled_devastation | 8 | Faith — controlled devastation doctrine |
| A33_vernissage_secretariat | 9 | Industrial — Vernissage governance |
| A33_unity_through_diplomacy | 6 | Diplomacy — unity through diplomacy |

**Assessment:** `A33_project_holohana` — "Holohana" is a Hawaiian term. This
may be a placeholder or wrong name. Needs review against Verne lore.

---

## Notable Cross-Slot Dependencies

### High-Connectivity Hub: `A33_the_vernman_era` (Slot 3)
```
Requires (incoming):         A33_new_verne [2], A33_the_kingdom_of_Verne [3]
Required (outgoing):          A33_laments_regatta [2], A33_religious_mercantilism [5],
                              A33_the_halanni_exposition [1], A33_with_sword_and_shield [4]
```
This mission is a **major junction point** connecting slots 1, 2, 3, 4, 5.
It's the narrative core of the "Vernman era" — the golden age of the
Verne dynasty. The wide connectivity is likely intentional.

### High-Connectivity Hub: `A33_all_roads_lead_to_verne` (Slot 3)
```
Required by:                  A33_project_holohana [1], A33_the_grand_vernissage [1]
Required (outgoing):          A33_new_verne [2], A33_the_holy_corinite_empire [4]
```
Central trade/infrastructure hub connecting lanes 1, 2, 3, 4.

---

## Outstanding File Bug
**Slots 6-10 all say `slot = 5`** — the GUI reads this field, so in-game
only 5 columns would render (even after `max_slots_horizontal = 10` is set).

Must be fixed in `Verne_Missions.txt`:
```
A33_sixth_slot     → slot = 6   (currently says slot = 5)
A33_seventh_slot   → slot = 7   (currently says slot = 5)
A33_eighth_slot    → slot = 8   (currently says slot = 5)
A33_ninth_slot     → slot = 9   (currently says slot = 5)
A33_tenth_slot     → slot = 10  (currently says slot = 5)
```
Also: `A33_fifth_sloth` → should be `A33_fifth_slot` (typo).

---

## Audit Script
`scripts/mission_dep_graph.py` — saved to `automation/reports/mission_dep_graph.json`
