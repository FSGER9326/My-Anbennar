# Verne Lore-Mechanics Bridge Notes

**Status:** WORKING_LORE

This file translates Verne lore identity into implementation-facing guidance without changing script truth.

Use this when writing missions, events, privileges, reforms, modifiers, or localization so mechanics and narrative stay synchronized.

## Canon policy for this bridge

Each bridge note carries a canon marker:

- **OFFICIAL_CANON**: directly grounded in base Anbennar content present in this repo (history setup, existing missions/events, established names).
- **INFERRED_CANON**: high-confidence interpretation from multiple in-repo signals.
- **PROJECT_CANON**: deliberate submod direction that extends or re-weights existing signals.

If a mechanic choice depends on PROJECT_CANON, mark it in the implementation doc or PR description before scripting.

## Bridge matrix (lore role -> mechanic expression)

| Bridge ID | Lore role | Mechanic expression | Canon marker | Primary anchors |
|---|---|---|---|---|
| VERNE-BRIDGE-COURT-001 | Verne is a ceremonial maritime court-state, not a generic conquest monarchy. | Prefer legitimacy/prestige/statecraft reward loops (reforms, court-flavored events, court-vs-expedition choices) over flat conquest-only pacing. | INFERRED_CANON | `history/countries/A33 - Verne.txt`, `missions/Verne_Missions.txt`, `docs/design/dynasty-and-court.md` |
| VERNE-BRIDGE-WYVERN-001 | Wyverns are institutional military identity, not only aesthetic flavor. | Gate elite military rewards behind order/estate/state-investment milestones, with upkeep/tradeoff choices that signal discipline. | INFERRED_CANON | `missions/Verne_Missions.txt`, `docs/repo-maps/verne-wyvern-orders-mercs-and-monuments-reference.md`, `docs/repo-maps/verne-wyvernrider-estate-ecosystem-reference.md` |
| VERNE-BRIDGE-OVERSEAS-001 | Overseas expansion fantasy is curated expeditionary statecraft. | Use route-building, staging, and network progression (adventure systems, ports, mission flags) rather than purely random colony throughput language. | OFFICIAL_CANON | `missions/Verne_Missions.txt`, `docs/repo-maps/verne-launch-adventure-system.md`, `docs/repo-maps/network-of-adventure-system.md` |
| VERNE-BRIDGE-FAITH-001 | Religious posture evolves from pragmatic court management toward stronger Corinite-imperial framing. | Stage religious text and triggers by era/progression; avoid early hard-lock flavor that erases transitional play. | INFERRED_CANON | `history/countries/A33 - Verne.txt`, `docs/design/pressure-disasters-and-corinite.md`, `docs/design/reform-bible.md` |
| VERNE-BRIDGE-RIVALRY-001 | Rivals/friends are prestige-political mirrors for Verne court identity. | Frame diplomatic events and mission text around sea-lane prestige, protocol insult, and court influence, not only border friction. | OFFICIAL_CANON | `history/countries/A33 - Verne.txt`, `docs/lore/verne-religion-rivals-and-overseas-imaginary.md` |
| VERNE-BRIDGE-ALT-001 | Submod may push stronger doctrine integration than base patterns. | If introducing new doctrine meters/pressures, classify as PROJECT_CANON and cross-link implementation rationale so future regions can reuse the pattern safely. | PROJECT_CANON | `docs/design/doctrine-bible.md`, `docs/implementation-crosswalk.md` |

## Authoring rules for bridge-safe content

1. **Mechanics stay authoritative in implementation files.**
   - This document explains meaning and intent; it does not supersede scripted triggers/effects.
2. **Keep one source of truth for behavior.**
   - If a lore statement conflicts with script, update this file (or mark gap) instead of duplicating script logic here.
3. **Name by role, not only by effect.**
   - Event/mission prose should communicate what institution or doctrine is being reinforced.
4. **Expose transitional arcs explicitly.**
   - Court -> expedition, pragmatism -> Corinite framing, and rider prestige -> administrative cost should be visible in text and option structure.

## Merge-safe placement policy

To reduce hotspot overlap, add Verne bridge expansions here first under `docs/lore/`.

Defer broad hub and index aggregation (for example repo-wide docs hubs) to later stacked PRs unless the current implementation task requires immediate discoverability updates.

## Current open gaps (target future stacked PRs)

- Add a reusable template for other nations (`<nation>-lore-mechanics-bridge.md`) once Verne bridge sections stabilize.
- Add a lightweight docs hub link sweep after concurrent documentation PRs settle, to avoid cross-branch conflicts.
- Add optional validation checklist references for bridge-sensitive systems (missions/events/estates/reforms) in a dedicated non-hotspot location.

## Related docs

- [./verne-identity-and-court-culture.md](./verne-identity-and-court-culture.md)
- [./verne-religion-rivals-and-overseas-imaginary.md](./verne-religion-rivals-and-overseas-imaginary.md)
- [../implementation-crosswalk.md](../implementation-crosswalk.md)
- [../design/dynasty-and-court.md](../design/dynasty-and-court.md)
- [../design/pressure-disasters-and-corinite.md](../design/pressure-disasters-and-corinite.md)
- [../repo-maps/verne-launch-adventure-system.md](../repo-maps/verne-launch-adventure-system.md)
