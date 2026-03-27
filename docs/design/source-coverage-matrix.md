# Source Coverage Matrix

This file maps the original restructured master plan into the current `docs/design/` set.

Purpose:

- show where each major source domain currently lives
- show which areas are already preserved well
- show which areas still need a deeper reconciliation pass
- reduce the risk of losing information during later cleanup

Primary source:

- [verne_overhaul_restructured_master_plan.md](/C:/Users/User/Downloads/verne_overhaul_restructured_master_plan.md)

Important rule:

- if this matrix says a section is only partially reconciled, the original master plan still remains the authoritative preservation source for that area

## Coverage Status Key

- **Well preserved**: the current `docs/design/` file set appears to carry the section's main content in a usable form
- **Partially reconciled**: the section is represented, but still needs a tighter pass against the original source
- **Needs deeper reconciliation**: the section exists in some form, but important detail is still likely trapped mainly in the original master plan

## Part I - Strategic vision and design rules

| Original section | Current home | Coverage | Notes |
|---|---|---|---|
| Executive snapshot | [README.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/README.md), [open-questions-and-design-lab.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/open-questions-and-design-lab.md) | Partially reconciled | High-level project identity is preserved, but the original master plan still carries the richest phrasing. |
| Hard implementation principles | [README.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/README.md), [implementation-scaffolding.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/implementation-scaffolding.md), [preserved-notes-and-edge-cases.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/preserved-notes-and-edge-cases.md) | Partially reconciled | Core rules like no fake mechanics and no casual province-state logic are preserved, but should still be rechecked during implementation. |
| Implementation model | [implementation-scaffolding.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/implementation-scaffolding.md), [open-questions-and-design-lab.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/open-questions-and-design-lab.md) | Well preserved | File-map and phased engineering order are now carried directly. |
| Verne-exclusive ruler personality | [dynasty-and-court.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/dynasty-and-court.md) | Partially reconciled | The concept is represented, but should be checked against the original exact effect package and acquisition sources. |

## Part II - National identity, doctrine, and policies

| Original section | Current home | Coverage | Notes |
|---|---|---|---|
| National ideas redesign | [doctrine-bible.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/doctrine-bible.md) | Well preserved | This is one of the stronger imported areas. |
| Full Verne-exclusive doctrine menu | [doctrine-bible.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/doctrine-bible.md) | Well preserved | First-wave and second-wave doctrine groups are represented there. |
| Policy architecture and first-wave policy matrix | [doctrine-bible.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/doctrine-bible.md), [preserved-notes-and-edge-cases.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/preserved-notes-and-edge-cases.md) | Partially reconciled | First-wave policy logic is preserved, but the full matrix and role-generation rule still deserve a stricter pass. |
| Exact doctrine internal packages (16A.1-16A.21) | [doctrine-bible.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/doctrine-bible.md) | Partially reconciled | Largely present, but worth auditing line by line against the master plan before coding. |
| Advanced systems integration (16A.22) | [preserved-notes-and-edge-cases.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/preserved-notes-and-edge-cases.md), [open-questions-and-design-lab.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/open-questions-and-design-lab.md) | Needs deeper reconciliation | This is one of the biggest remaining gaps from the imported draft set. |

## Part III - Mission architecture and government structure

| Original section | Current home | Coverage | Notes |
|---|---|---|---|
| Mission flexibility overhaul | [mission-rewrite-spec.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/mission-rewrite-spec.md) | Well preserved | Route families, projection scores, and threshold logic are represented. |
| Mission tree structure and reward rules | [mission-rewrite-spec.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/mission-rewrite-spec.md), [implementation-scaffolding.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/implementation-scaffolding.md) | Partially reconciled | Reward logic and coding rules are preserved, but full-mission coverage is still first-wave heavy. |
| Government reform matrix | [reform-bible.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/reform-bible.md) | Well preserved | The imported reform doc is structurally strong. |
| Reform unlock matrix and doctrine logic | [reform-bible.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/reform-bible.md), [open-questions-and-design-lab.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/open-questions-and-design-lab.md) | Partially reconciled | Design is present, but still needs repo-aware validation before coding. |
| Maritime commerce correction | [reform-bible.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/reform-bible.md), [preserved-notes-and-edge-cases.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/preserved-notes-and-edge-cases.md) | Partially reconciled | Light-ship and mercantilism support is preserved, but spread across files. |

## Part IV - Institutions, decisions, estates, religion, and pressure systems

| Original section | Current home | Coverage | Notes |
|---|---|---|---|
| Monument architecture | [orders-monuments-and-mercs.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/orders-monuments-and-mercs.md) | Partially reconciled | Main monument identity is preserved, but some per-tier detail should still be compared against the source. |
| Wyvern orders and mercenary architecture | [orders-monuments-and-mercs.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/orders-monuments-and-mercs.md), [implementation-scaffolding.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/implementation-scaffolding.md) | Well preserved | Role identity, founding direction, and upgrade logic now have a better preservation layer. |
| Dynastic decision package | [dynasty-and-court.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/dynasty-and-court.md), [implementation-scaffolding.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/implementation-scaffolding.md) | Well preserved | Decisions plus first code-shaped skeletons are now both represented. |
| Balancing pressure package | [pressure-disasters-and-corinite.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/pressure-disasters-and-corinite.md) | Partially reconciled | Strong concept coverage, but worth checking exact trigger/effect wording against source before coding. |
| Estate package and advisor package | [dynasty-and-court.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/dynasty-and-court.md), [preserved-notes-and-edge-cases.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/preserved-notes-and-edge-cases.md) | Partially reconciled | Advisor archetypes seem preserved better than estate detail. |
| Country/area modifiers and provincial specialization | [preserved-notes-and-edge-cases.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/preserved-notes-and-edge-cases.md) | Needs deeper reconciliation | This is preserved more as notes than as a full canonical spec. |
| Anti-corruption package | [pressure-disasters-and-corinite.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/pressure-disasters-and-corinite.md), [implementation-scaffolding.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/implementation-scaffolding.md) | Well preserved | Decisions, event namespaces, constants, and warnings are now captured in multiple layers. |
| Corinite conversion and center of reformation | [pressure-disasters-and-corinite.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/pressure-disasters-and-corinite.md), [preserved-notes-and-edge-cases.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/preserved-notes-and-edge-cases.md) | Partially reconciled | Mainline route is preserved, but should still be repo-checked carefully. |
| Anti-Corinite / non-Corinite content | [pressure-disasters-and-corinite.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/pressure-disasters-and-corinite.md), [open-questions-and-design-lab.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/open-questions-and-design-lab.md) | Needs deeper reconciliation | Still mainly a lower-priority concept lane. |
| Verne-specific disasters and scaling hooks | [pressure-disasters-and-corinite.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/pressure-disasters-and-corinite.md), [implementation-scaffolding.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/implementation-scaffolding.md) | Well preserved | The pressure/disaster layer is now meaningfully better represented than in the imported draft alone. |

## Part V - Engineering roadmap and implementation scaffolding

| Original section | Current home | Coverage | Notes |
|---|---|---|---|
| Immediate next engineering slice | [implementation-scaffolding.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/implementation-scaffolding.md) | Well preserved | Preserved directly. |
| Exact submod file map and object naming plan | [implementation-scaffolding.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/implementation-scaffolding.md) | Well preserved | Preserved directly. |
| First code slice dependency order | [implementation-scaffolding.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/implementation-scaffolding.md) | Well preserved | Preserved directly. |
| Key repo hooks to reuse rather than reinvent | [implementation-scaffolding.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/implementation-scaffolding.md) | Well preserved | Preserved through repo-anchor notes and shared-system cautions. |
| Scripted trigger catalog | [implementation-scaffolding.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/implementation-scaffolding.md) | Well preserved | Preserved directly. |
| Scripted effect catalog | [implementation-scaffolding.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/implementation-scaffolding.md) | Well preserved | Preserved directly. |
| Event namespaces and core objects | [implementation-scaffolding.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/implementation-scaffolding.md) | Well preserved | Preserved directly. |
| First-wave implementation constants | [implementation-scaffolding.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/implementation-scaffolding.md) | Well preserved | Preserved directly. |
| Mission coding rule | [implementation-scaffolding.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/implementation-scaffolding.md), [mission-rewrite-spec.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/mission-rewrite-spec.md) | Well preserved | Preserved in both design and engineering layers. |
| Code-shaped helper definitions and skeletons | [implementation-scaffolding.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/implementation-scaffolding.md) | Well preserved | This was the biggest preservation gap from the imported draft; it is now carried over. |
| Repository-verified implementation anchors | [implementation-scaffolding.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/implementation-scaffolding.md), [docs/codex-grounding-checklist.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/codex-grounding-checklist.md) | Well preserved | Repo-anchor guidance is now present in both the design layer and the working checklist. |

## Remaining Priority Gaps

These areas are the best candidates for the next reconciliation pass:

1. advanced systems integration (`16A.22`)
2. provincial specialization and area/country modifier cleanup (`13` and `13.1`)
3. estate package detail outside the advisor archetype slice (`12`)
4. full policy generation rule and later-wave policy coverage (`5F.3`)
5. second-pass verification of exact doctrine internal packages against the original source

## Working Verdict

The current `docs/design/` folder is now materially safer than the imported draft set on its own because it includes:

- a design-layer README
- a more honest open-questions file
- a preserved-notes file that stops pretending everything was already fully carried over
- an implementation scaffolding file that captures the engineering-heavy sections from the original master plan

However:

- the original restructured master plan is still the deepest preservation source
- several design files are still imported-and-patched rather than fully re-authored from source
- a second reconciliation pass is still warranted before treating every section as equally mature
