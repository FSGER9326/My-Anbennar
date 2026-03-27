# Verne Overhaul Design Documentation

This directory contains the structured working design for the Verne overhaul (EU4/Anbennar).

It is derived from:

- the original restructured master plan in [verne_overhaul_restructured_master_plan.md](/C:/Users/User/Downloads/verne_overhaul_restructured_master_plan.md)
- an imported draft markdown set that was then patched inside the repo

Important rule:

- the original restructured master plan is still the deepest preservation source
- this `docs/design/` folder is the GitHub-friendly working design layer
- if a detail exists in the original source but not here yet, the original source wins until reconciliation is complete

## File Overview

| File | Content |
|------|---------|
| [doctrine-bible.md](./doctrine-bible.md) | All Verne doctrine groups, national ideas, policies, roles, and numeric packages. |
| [reform-bible.md](./reform-bible.md) | Government reforms: tiers, triplets, unlock logic, exact modifiers, and thematic role. |
| [mission-rewrite-spec.md](./mission-rewrite-spec.md) | Mission tree rewrite: mission identity, completion logic, route flexibility, rewards, and doctrine sensitivity. |
| [dynasty-and-court.md](./dynasty-and-court.md) | Dynastic continuity, heir shaping, marriage court, advisor archetypes, and related decisions/events. |
| [orders-monuments-and-mercs.md](./orders-monuments-and-mercs.md) | The Chapterhouse monument, wyvern order companies, unlock flow, costs, and upgrade paths. |
| [pressure-disasters-and-corinite.md](./pressure-disasters-and-corinite.md) | Pressure systems, anti-corruption tools, disasters, Corinite integration, and alternative paths. |
| [open-questions-and-design-lab.md](./open-questions-and-design-lab.md) | Unresolved design questions, conflicts, and items needing repo verification. |
| [preserved-notes-and-edge-cases.md](./preserved-notes-and-edge-cases.md) | Stray notes, edge cases, variant concepts, and preserved fragments that did not fit elsewhere. |
| [implementation-scaffolding.md](./implementation-scaffolding.md) | File map, naming plan, scripted trigger/effect catalog, event namespaces, constants, code-shaped skeletons, and repo-verified implementation anchors. |

## Status Labels

Each major mechanic is tagged with one of these statuses:

- **CANONICAL**: settled design, preserved as the current intended version.
- **IMPLEMENTATION_READY**: design is specific enough to implement after a normal grounding pass.
- **NEEDS_DESIGN**: incomplete and still needs theorycraft.
- **NEEDS_REPO_CHECK**: design exists but must be verified against the actual Anbennar repository before coding.
- **CONFLICT_NEEDS_DECISION**: multiple incompatible versions exist and a decision is still required.

## How to Use These Documents

- **For theorycraft**: refer to canonical entries and open questions. `preserved-notes-and-edge-cases.md` keeps alternative ideas and loose fragments alive.
- **For implementation**: use `IMPLEMENTATION_READY` items as design-ready specs, then ground them against the repo and the local EU4 wiki references before coding.
- **For engineering-heavy work**: consult `implementation-scaffolding.md`, because that is where the trigger/effect catalogs, namespaces, naming plan, and repo-anchor notes are preserved.
- **For maintenance**: prefer updating these files rather than creating new scattered design notes.

## Quick Index of Major Systems

- Doctrine groups: 7 ADM, 7 DIP, 7 MIL plus policies ([doctrine-bible.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/doctrine-bible.md))
- National ideas: traditions, 7 ideas, ambition ([doctrine-bible.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/doctrine-bible.md))
- Reforms: 8 tiers, each with 3 choices ([reform-bible.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/reform-bible.md))
- Missions: route families, projection scores, and first-wave rewrite specs ([mission-rewrite-spec.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/mission-rewrite-spec.md))
- Dynasty: heir correction, marriage court, training decisions, and advisors ([dynasty-and-court.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/dynasty-and-court.md))
- Orders: Chapterhouse, order companies, and upgrade direction ([orders-monuments-and-mercs.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/orders-monuments-and-mercs.md))
- Disasters and pressure: maintenance mechanics and failure states ([pressure-disasters-and-corinite.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/pressure-disasters-and-corinite.md))
- Engineering scaffolding: file map, helper catalogs, event namespaces, naming plan, and repo anchors ([implementation-scaffolding.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/implementation-scaffolding.md))
