# Open Questions and Design Lab

This file tracks unresolved design issues, conflicts, and items requiring future decision or repo verification.

## Confirmed Canonical Decisions

The following systems appear stable as current design truth and are documented in the other files:

- National ideas and the doctrine structure
- Reform tiers and triplets
- Mission flexibility through route families and projection scores
- Dynastic continuity stages and heir-shaping decisions
- Wyvern order companies and the Chapterhouse concept
- Pressure systems and Verne-specific disasters
- Corinite conversion preservation as the mainline religious route

## Implementation-Ready Packages

These are the strongest design-ready packages, but they still require a grounding pass against the real Anbennar repo before coding:

- First-wave doctrine groups and their exact internal packages
- First-wave policies
- Reform triplets for the first implementation slice
- First 10 missions
- Dynastic decisions
- Anti-corruption decisions
- Wyvern order company definitions
- Verne-specific disasters
- Advisor archetypes
- Helper-layer trigger/effect/event scaffolding preserved in [implementation-scaffolding.md](./implementation-scaffolding.md)

## Needs Further Design

The following areas are mentioned but not fully detailed:

- **Full mission tree:** only the first 10 missions are specified; the remaining missions need the same level of treatment
- **Anti-Corinite / non-Corinite content:** concept exists, but not a fully specified branch
- **Full policy matrix:** the first-wave policies are set, but the full pair matrix is not finished
- **Artificery integration:** low priority and still incomplete
- **Advanced integration layer:** paragonhood, witch-king temptation, artifact/relic hooks, and Port of Adventure modernization need fuller reconciliation into the design docs

## Conflicts To Resolve

No major hard conflicts have been confirmed in the imported draft set, but this should not be treated as final proof that all source conflicts are resolved.

Known ambiguity:

- **Mercenary manpower cost:** the source mentions both direct manpower removal in founding decisions and possible `mercenary_manpower` support. The current intended mainline is direct founding-cost removal, with `mercenary_manpower` left as optional broader support.

## Needs Repo Verification Later

The following items should be checked against the actual Anbennar repository before implementation:

- **Port of Adventure system:** preserve the existing GUI and button path; extend rewards and country tracking instead of rewriting the GUI first
- **Mercenary company upgrade pattern:** mirror Marrhold's griffon upgrade flow
- **`define_heir = { dynasty = ROOT }` usage:** verify it is safe across Verne succession handling
- **`on_new_heir` event hook:** verify it can be added cleanly via a dedicated on_actions file
- **Corinite conversion event:** verify exact event ID and trigger conditions
- **Same-name core overrides:** verify where keyed override is safer and where a shared Verne anchor should be patched instead
- **Generic idea-group compatibility:** verify which shared systems still depend on vanilla/basic `has_idea_group` logic before doctrine replacement is treated as implementation-safe

## Deduplication Log

The imported draft merged a lot of repeated content successfully:

- National ideas consolidated from scattered summary layers
- Doctrine groups merged from names, totals, exact internal packages, and role notes
- Reforms merged from outline sections and later exact packages
- Missions merged from route logic, threshold logic, and rewrite specs
- Dynastic decisions merged from separate cadence and outcome sections
- Wyvern orders merged from role notes, stats, and founding-cost sections
- Disasters merged from trigger, effect, and scaling sections

Important note:

- the first imported draft did omit or only partially preserve some engineering-heavy material from the original master plan
- that material is now preserved separately in [implementation-scaffolding.md](./implementation-scaffolding.md)
