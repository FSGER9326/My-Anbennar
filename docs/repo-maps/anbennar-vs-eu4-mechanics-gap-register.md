# Anbennar vs EU4 Mechanics Gap Register

Purpose: keep a running list of major mechanics that still need a clean "base EU4 vs Anbennar implementation" comparison.
Purpose: keep a running list of major mechanics that still need a clean “base EU4 vs Anbennar implementation” comparison.

Use this as the queue for future repo-map deep scans.

## Status key

- `NOT_STARTED`: no dedicated comparison article yet
- `IN_PROGRESS`: anchors collected, article not complete
- `DONE`: dedicated comparison article exists

## High-value gap queue

| Mechanic family | Why it matters | Current evidence | Status | Next action |
|---|---|---|---|---|
| Custom estates beyond current deep docs | Many Verne systems interact with estates and privileges | Dedicated comparison article now exists: `custom-estates-family-and-privilege-framework-base-vs-anbennar-reference.md` | DONE | Keep article current during estate-related implementation commits |
| Custom government mechanics library | Reforms and government powers are core to overhaul design | Dedicated comparison article: `government-mechanics-library-base-vs-anbennar-reference.md` | DONE | Keep matrix current when adding new mechanic IDs |
| Special diplomacy actions | Can silently change war/peace and AI behavior expectations | Dedicated comparison article: `diplomatic-actions-layer-base-vs-anbennar-reference.md` | DONE | Revalidate action IDs during upstream merges |
| Custom peace treaty layer | High-risk during upstream updates and balance passes | Dedicated comparison article: `peace-treaty-layer-base-vs-anbennar-reference.md` | DONE | Revalidate key custom peace options after upstream updates |
| Rebel system deltas | Impacts disasters, unrest, and mission fail states | Dedicated comparison article: `rebel-system-deltas-base-vs-anbennar-reference.md` | DONE | Revalidate rebel IDs used by disasters/events |
| Unit/system deltas | Hidden balancing differences from vanilla expectations | Dedicated comparison article: `unit-system-deltas-base-vs-anbennar-reference.md` | DONE | Re-check unit families when upstream changes military progression |
| Religion behavior deltas used by Verne content | Needed for Corinite/disaster pressure design validation | Dedicated comparison article: `religion-behavior-deltas-for-verne-reference.md` | DONE | Keep aligned with Corinite/Regent Court event flow updates |

## Per-gap mini template

### Gap ID: `ANB-GAP-XXXX`

- **Mechanic family:**
- **Vanilla baseline summary:**
- **Anbennar deltas observed:**
- **Primary repo anchors:**
- **Risk if ignored:**
- **Suggested adaptation pattern:**
- **Status:**
