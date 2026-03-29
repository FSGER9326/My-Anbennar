# First-Wave Backlog

## Why this file exists
This file turns the theorycraft into small Codex-sized work items.

Each task should be possible to complete in one focused session. Early tasks should touch a small number of files and prefer helper layers over giant rewrites.

Run [`docs/codex-grounding-checklist.md`](./codex-grounding-checklist.md) before starting any backlog item that edits code.

## Current implementation status (2026-03-29)
- **Helpers:** live (`common/event_modifiers/verne_overhaul_modifiers.txt`, `common/scripted_triggers/verne_overhaul_triggers.txt`, `common/scripted_effects/verne_overhaul_effects.txt`).
- **Doctrine groups:** partial (single group live: `verne_doctrine_silver_wake` in [`common/ideas/verne_doctrine_groups.txt`](../common/ideas/verne_doctrine_groups.txt)).
- **Reforms:** partial (tier-1 triplet live in [`common/government_reforms/verne_overhaul_reforms.txt`](../common/government_reforms/verne_overhaul_reforms.txt)).
- **Policies/decisions:** scaffold-only until gameplay lane lands (`verne_placeholder_doctrine_policy` in [`common/policies/verne_doctrine_policies.txt`](../common/policies/verne_doctrine_policies.txt); `verne_placeholder_overhaul_decision` in [`decisions/verne_overhaul_decisions.txt`](../decisions/verne_overhaul_decisions.txt)).
- **Planning rule:** do not mark first-wave as complete while policies/decisions remain scaffold-only.

## Current live surface (implemented objects only)
- Doctrine: [`common/ideas/verne_doctrine_groups.txt`](../common/ideas/verne_doctrine_groups.txt) → `verne_doctrine_silver_wake`.
- Reforms: [`common/government_reforms/verne_overhaul_reforms.txt`](../common/government_reforms/verne_overhaul_reforms.txt) → `verne_court_of_silver_oaths_reform`, `verne_charter_of_great_captains_reform`, `verne_ducal_muster_of_armoc_reform`.
- Dynasty on_action dispatch: [`common/on_actions/verne_overhaul_on_actions.txt`](../common/on_actions/verne_overhaul_on_actions.txt) → `on_new_heir` -> `verne_overhaul_dynasty.1`.
- Dynasty event: [`events/verne_overhaul_dynasty_events.txt`](../events/verne_overhaul_dynasty_events.txt) → `verne_overhaul_dynasty.1`.

## Working rules
- Prefer 1 to 3 files per task when possible.
- Finish localization stubs in the same task as the new objects.
- Do not rewrite early missions before the helper layer and reform/precursor flags exist.
- Preserve working Verne content where possible instead of replacing it blindly.
- Treat shared multi-country files as normal for Verne work. Do not assume the real source lives in a tidy Verne-only file.
- Tooltip/custom-tooltip mission keys for overhaul helpers are standardized to the `verne_overhaul_tt_*` namespace; avoid introducing new `verne_unlock_*` keys.

## Known unresolved debt (tooltip prefix mismatch)
- Rule target remains `verne_overhaul_tt_*`, but current ownership is still split.
- Overhaul mission flow currently references `verne_overhaul_tt_*` keys in [`missions/Verne_Missions.txt`](../missions/Verne_Missions.txt).
- Legacy flavor localization still defines `verne_unlock_*` tooltip keys in [`localisation/Flavour_Verne_A33_l_english.yml`](../localisation/Flavour_Verne_A33_l_english.yml).
- Keep this as tracked debt; do not fold key-renaming churn into unrelated gameplay tasks.

## v0.1 Beginner-Safe Slice (Execute First)

This is the first implementation scope. Do **only** this thin slice before broader system work.

Target files for v0.1:
- [`common/ideas/verne_doctrine_groups.txt`](../common/ideas/verne_doctrine_groups.txt) — add one doctrine group prototype (single group only).
- [`common/government_reforms/verne_overhaul_reforms.txt`](../common/government_reforms/verne_overhaul_reforms.txt) — add one initial reform entry (single reform only).
- [`localisation/verne_overhaul_l_english.yml`](../localisation/verne_overhaul_l_english.yml) — add matching localization for the prototype IDs.

Scope guardrails:
- Keep this v0.1 pass to **~3 touched gameplay files + 1 localization file maximum** for beginner-safe iteration.
- Do not expand into mission-tree rewrites during this pass.
- Do not add deferred helper-heavy systems during this pass.

Post-v0.1 (explicitly deferred):
- Broad mission rewrites and mission reward rebalance.
- Cross-system doctrine integration passes (global compat rewiring, policy web expansion, and wide event coupling).
- Additional reform tiers/chains beyond the first single reform prototype.

Done when (v0.1 checks):
- Doctrine prototype ID exists in `common/ideas/verne_doctrine_groups.txt`.
- Initial reform ID exists in `common/government_reforms/verne_overhaul_reforms.txt`.
- Matching localization keys exist in `localisation/verne_overhaul_l_english.yml` for every new v0.1 ID.
- No duplicate key names are introduced across newly added v0.1 entries.
- Helper naming parity is consistent (`verne_` prefix and shared suffix patterns where applicable).

## Phase 0: Grounding Audit

### V-00 Map shared touchpoints and compatibility risks
Target files:
- [`common/ideas/anb_country_ideas.txt`](../common/ideas/anb_country_ideas.txt)
- [`localisation/anb_powers_and_ideas_l_english.yml`](../localisation/anb_powers_and_ideas_l_english.yml)
- [`common/ideas/00_basic_ideas.txt`](../common/ideas/00_basic_ideas.txt)
- [`common/great_projects/anb_monuments_missions.txt`](../common/great_projects/anb_monuments_missions.txt)
- [`common/mercenary_companies/0_anb_elite_mercenaries.txt`](../common/mercenary_companies/0_anb_elite_mercenaries.txt)
- [`events/Flavour_Verne_A33.txt`](../events/Flavour_Verne_A33.txt)
- [`common/on_actions/00_on_actions.txt`](../common/on_actions/00_on_actions.txt)
- [`docs/mod-spec.md`](./mod-spec.md)

Done when:
- we know where Verne national ideas, idea localization, monuments, mercs, dynasty handling, and advisor spawning already live
- we have written down which files are shared multi-country files
- we have listed the first generic `has_idea_group` compatibility risks for doctrine replacement

## Phase A: Helper Layer

### V-01 Create the Verne modifier file
Target files:
- [`common/event_modifiers/verne_overhaul_modifiers.txt`](../common/event_modifiers/verne_overhaul_modifiers.txt)
- [`localisation/verne_overhaul_l_english.yml`](../localisation/verne_overhaul_l_english.yml)

Done when:
- first-wave pressure modifiers exist
- first-wave mission reward modifiers exist
- first-wave dynasty and court modifiers have named homes

### V-02 Create the Verne trigger file
Target files:
- [`common/scripted_triggers/verne_overhaul_triggers.txt`](../common/scripted_triggers/verne_overhaul_triggers.txt)

Done when:
- doctrine precursor triggers exist
- dynasty-state triggers exist
- projection-score triggers exist
- Chapterhouse and order legality triggers exist
- pressure-state triggers exist

### V-03 Create the Verne effect file
Target files:
- [`common/scripted_effects/verne_overhaul_effects.txt`](../common/scripted_effects/verne_overhaul_effects.txt)

Done when:
- projection score increments exist
- early-path flag setters exist
- dynasty correction helpers exist
- advisor spawn helpers exist
- order founding helpers exist
- shared mission reward bundle effects exist

### V-04 Reserve first-wave flags, variables, and loc stubs
Target files:
- [`localisation/verne_overhaul_l_english.yml`](../localisation/verne_overhaul_l_english.yml)
- [`docs/mod-spec.md`](./mod-spec.md)

Done when:
- the first-wave variables are fixed and named
- the early path and dynasty flags are fixed and named
- new object naming follows the `verne_` prefix rule consistently

## Phase B: Doctrine Slice

### Doctrine safety gate
Before V-05 through V-13, confirm all of the following:

- where `A33_ideas` currently lives
- where Verne idea localization currently lives
- whether the doctrine-menu replacement needs support in [`common/ideas/00_basic_ideas.txt`](../common/ideas/00_basic_ideas.txt)
- which shared systems still expect vanilla/basic idea groups and therefore need alternate handling or a deferred compatibility note

### V-05 Replace Verne national ideas cleanly
Target files:
- [`common/ideas/anb_country_ideas.txt`](../common/ideas/anb_country_ideas.txt)
- [`localisation/anb_powers_and_ideas_l_english.yml`](../localisation/anb_powers_and_ideas_l_english.yml)
- [`common/ideas/verne_country_ideas_overhaul.txt`](../common/ideas/verne_country_ideas_overhaul.txt)
- [`localisation/verne_overhaul_l_english.yml`](../localisation/verne_overhaul_l_english.yml)

Done when:
- Verne traditions, seven national ideas, and ambition match the theorycraft summary
- the national ideas are clearly separated from the doctrine menu
- the task states whether the final implementation patches `A33_ideas` in place or overrides it from a Verne-specific file

### V-06 Add Silver Oaths Ideas
Target files:
- [`common/ideas/verne_doctrine_groups.txt`](../common/ideas/verne_doctrine_groups.txt)
- [`localisation/verne_overhaul_l_english.yml`](../localisation/verne_overhaul_l_english.yml)

Done when:
- the full seven internal idea entries exist
- the completion bonus exists
- names and modifiers match the first-wave theorycraft package

### V-07 Add Vernissage Ideas
Target files:
- [`common/ideas/verne_doctrine_groups.txt`](../common/ideas/verne_doctrine_groups.txt)
- [`localisation/verne_overhaul_l_english.yml`](../localisation/verne_overhaul_l_english.yml)

Done when:
- the full seven internal idea entries exist
- the completion bonus exists
- the group supports expedition and world-network play

### V-08 Add Dragonwake Ideas
Target files:
- [`common/ideas/verne_doctrine_groups.txt`](../common/ideas/verne_doctrine_groups.txt)
- [`localisation/verne_overhaul_l_english.yml`](../localisation/verne_overhaul_l_english.yml)

Done when:
- the full seven internal idea entries exist
- the completion bonus exists
- the group supports noble-rider and martial-heir play

### V-09 Add Imperial Sea Court Ideas
Target files:
- [`common/ideas/verne_doctrine_groups.txt`](../common/ideas/verne_doctrine_groups.txt)
- [`localisation/verne_overhaul_l_english.yml`](../localisation/verne_overhaul_l_english.yml)

Done when:
- the full seven internal idea entries exist
- the completion bonus exists
- the group supports fleet-backed diplomacy

### V-10 Add Red Court Ideas
Target files:
- [`common/ideas/verne_doctrine_groups.txt`](../common/ideas/verne_doctrine_groups.txt)
- [`localisation/verne_overhaul_l_english.yml`](../localisation/verne_overhaul_l_english.yml)

Done when:
- the full seven internal idea entries exist
- the completion bonus exists
- the group supports mage-state and heir-shaping play

### V-11 Add Crimson Wake Order Ideas
Target files:
- [`common/ideas/verne_doctrine_groups.txt`](../common/ideas/verne_doctrine_groups.txt)
- [`localisation/verne_overhaul_l_english.yml`](../localisation/verne_overhaul_l_english.yml)

Done when:
- the full seven internal idea entries exist
- the completion bonus exists
- the group supports state-backed elite order play

### V-12 Add Estuary Companies Ideas
Target files:
- [`common/ideas/verne_doctrine_groups.txt`](../common/ideas/verne_doctrine_groups.txt)
- [`localisation/verne_overhaul_l_english.yml`](../localisation/verne_overhaul_l_english.yml)

Done when:
- the full seven internal idea entries exist
- the completion bonus exists
- the group supports port-finance and audited trade-state play

### V-13 Add the first-wave policy layer
Target files:
- [`common/policies/verne_doctrine_policies.txt`](../common/policies/verne_doctrine_policies.txt)
- [`localisation/verne_overhaul_l_english.yml`](../localisation/verne_overhaul_l_english.yml)

Done when:
- the first-wave exact policy packages exist
- names follow the Verne flavor families from the theorycraft
- the policy layer feels like a real system, not filler
- status is no longer scaffold-only (`verne_placeholder_doctrine_policy` removed/replaced by non-placeholder policy objects)

## Phase C: Reform Slice

### V-14 Add Tier 1 reform triplet
Target files:
- [`common/government_reforms/verne_overhaul_reforms.txt`](../common/government_reforms/verne_overhaul_reforms.txt)
- [`localisation/verne_overhaul_l_english.yml`](../localisation/verne_overhaul_l_english.yml)

Done when:
- Court of Silver Oaths exists
- Charter of Great Captains exists
- Ducal Muster of Armoc exists
- Default/safest pick for first tests: Court of Silver Oaths (most stable general-purpose governance baseline).

### V-15 Add Tier 2 reform triplet
Target files:
- [`common/government_reforms/verne_overhaul_reforms.txt`](../common/government_reforms/verne_overhaul_reforms.txt)
- [`localisation/verne_overhaul_l_english.yml`](../localisation/verne_overhaul_l_english.yml)

Done when:
- Admiralty of the Crimson Wake exists
- Estuary Companies of Heartspier exists
- Regatta Discipline exists

### V-16 Add Tier 3 reform triplet
Target files:
- [`common/government_reforms/verne_overhaul_reforms.txt`](../common/government_reforms/verne_overhaul_reforms.txt)
- [`localisation/verne_overhaul_l_english.yml`](../localisation/verne_overhaul_l_english.yml)

Done when:
- Red Court Arcana exists
- Dragonwake Ordinance exists
- Battle-Mage Collegium exists

## Phase D: Dynasty and Court

### V-17 Add the dynasty safeguard chain
Target files:
- [`events/verne_overhaul_dynasty_events.txt`](../events/verne_overhaul_dynasty_events.txt)
- [`common/on_actions/verne_overhaul_on_actions.txt`](../common/on_actions/verne_overhaul_on_actions.txt)
- [`common/scripted_triggers/verne_overhaul_triggers.txt`](../common/scripted_triggers/verne_overhaul_triggers.txt)

Done when:
- a Verne-specific `on_new_heir` safeguard exists
- incorrect heirs can be corrected into the silver Verne line
- the logic uses the repo's existing heir-handling patterns cleanly
- the event chain mirrors existing `define_heir` usage instead of inventing a new heir-definition style

### V-18 Add the five core dynastic decisions
Target files:
- [`decisions/verne_overhaul_decisions.txt`](../decisions/verne_overhaul_decisions.txt)
- [`events/verne_overhaul_dynasty_events.txt`](../events/verne_overhaul_dynasty_events.txt)
- [`localisation/verne_overhaul_l_english.yml`](../localisation/verne_overhaul_l_english.yml)

Done when:
- Train the Heir in the Red Court exists
- Induct the Heir into the Dragonwake exists
- Present the Heir at the Vernissage exists
- Drill the Battle-Mage Court exists
- Elevate a Storm-Crowned Prince exists
- status is no longer scaffold-only (`verne_placeholder_overhaul_decision` removed/replaced by non-placeholder decision objects)

### V-19 Add the first advisor archetype package
Target files:
- [`events/verne_overhaul_advisor_events.txt`](../events/verne_overhaul_advisor_events.txt)
- [`decisions/verne_overhaul_decisions.txt`](../decisions/verne_overhaul_decisions.txt)
- [`localisation/verne_overhaul_l_english.yml`](../localisation/verne_overhaul_l_english.yml)

Done when:
- Red Court Magister exists
- Grand Admiral of the Wake exists
- Vernissage Curator exists
- Khenak Master Founder exists

## Phase E: Mission Rewrite Slice

### V-20 Rewrite `Old Friends, Old Rivals`
Target files:
- [`missions/Verne_Missions.txt`](../missions/Verne_Missions.txt)
- supporting helper files as needed

Done when:
- the mission opens diplomacy and marriage-court play
- it no longer checks unavailable idea groups
- it sets early precursor state cleanly

### V-21 Rewrite `Alvar's Reform`
Target files:
- [`missions/Verne_Missions.txt`](../missions/Verne_Missions.txt)

Done when:
- the mission acts as state-foundation content
- it unlocks the Tier 1 reform slice cleanly
- it seeds the correct early doctrine lanes

### V-22 Rewrite `The Grand Port of Heartspier`
Target files:
- [`missions/Verne_Missions.txt`](../missions/Verne_Missions.txt)

Done when:
- the mission becomes the first true sea-state mission
- it unlocks Twin Harbours and flagship stage 1 logic cleanly

### V-23 Rewrite `The Riches of the Khenak`
Target files:
- [`missions/Verne_Missions.txt`](../missions/Verne_Missions.txt)

Done when:
- the mission becomes the industrial foundation mission
- it seeds Khenak Foundry logic cleanly

### V-24 Rewrite `The Vernissage`
Target files:
- [`missions/Verne_Missions.txt`](../missions/Verne_Missions.txt)

Done when:
- the mission unlocks cultural and international prestige systems
- it seeds Vernissage and Grand Galerie progression

### V-25 Rewrite `Across the Pond`
Target files:
- [`missions/Verne_Missions.txt`](../missions/Verne_Missions.txt)

Done when:
- the mission can be completed through multiple overseas route families
- it uses `verne_overseas_projection` logic instead of narrow colonizer checks

### V-26 Rewrite `In Search of Adventure`
Target files:
- [`missions/Verne_Missions.txt`](../missions/Verne_Missions.txt)

Done when:
- the mission supports colonizer and Vernissage/adventure-network routes
- it helps unlock adventure-state systems

### V-27 Rewrite `Binding the Beast`
Target files:
- [`missions/Verne_Missions.txt`](../missions/Verne_Missions.txt)

Done when:
- the mission becomes the wyvern-state founding mission
- it seeds Dragonwake and Chapterhouse order logic

### V-28 Rewrite `Expand the Wyvern Nests`
Target files:
- [`missions/Verne_Missions.txt`](../missions/Verne_Missions.txt)

Done when:
- the mission grows nest and rider infrastructure
- it feeds dynasty-magic and overseas-projection state where intended

### V-29 Rewrite `The Lament's Regatta`
Target files:
- [`missions/Verne_Missions.txt`](../missions/Verne_Missions.txt)

Done when:
- the mission becomes the true maritime-international prestige mission
- it feeds Tier 6 maritime reform logic

## Phase F: Order State and Pressure Layer

### Order-state safety gate
Before V-30 and V-31, confirm whether the cleanest first-wave implementation patches the existing shared Verne sections in:

- [`common/great_projects/anb_monuments_missions.txt`](../common/great_projects/anb_monuments_missions.txt)
- [`common/mercenary_companies/0_anb_elite_mercenaries.txt`](../common/mercenary_companies/0_anb_elite_mercenaries.txt)

Use standalone Verne files only if they are clearly safer than editing the existing anchors.

### V-30 Add the Chapterhouse monument
Target files:
- [`common/great_projects/anb_monuments_missions.txt`](../common/great_projects/anb_monuments_missions.txt)
- [`common/great_projects/verne_overhaul_monuments.txt`](../common/great_projects/verne_overhaul_monuments.txt)
- [`localisation/verne_overhaul_l_english.yml`](../localisation/verne_overhaul_l_english.yml)

Done when:
- the Chapterhouse unlock sequence is real
- monument tiers unlock order decisions progressively
- the task states whether the Chapterhouse was patched into the shared Verne monument anchor or implemented as a new keyed object on purpose

### V-31 Add the first three order companies
Target files:
- [`common/mercenary_companies/0_anb_elite_mercenaries.txt`](../common/mercenary_companies/0_anb_elite_mercenaries.txt)
- [`common/mercenary_companies/verne_overhaul_orders.txt`](../common/mercenary_companies/verne_overhaul_orders.txt)
- [`events/verne_overhaul_orders.txt`](../events/verne_overhaul_orders.txt)
- [`decisions/verne_overhaul_decisions.txt`](../decisions/verne_overhaul_decisions.txt)

Done when:
- Crimson Wake Lances exist
- Heartspier Skyguard exist
- Khenak Talons exist
- founding costs use money, manpower, and other required resources cleanly

### V-32 Add the anti-corruption decision package
Target files:
- [`decisions/verne_overhaul_decisions.txt`](../decisions/verne_overhaul_decisions.txt)
- [`events/verne_overhaul_cleansing_events.txt`](../events/verne_overhaul_cleansing_events.txt)

Done when:
- Purge the Admiralty Ledgers exists
- Muster the Ducal Auditors exists
- Red Court Inquest exists

### V-33 Add pressure modifiers and the four disaster scaffolds
Target files:
- [`common/disasters/verne_overhaul_disasters.txt`](../common/disasters/verne_overhaul_disasters.txt)
- [`events/verne_overhaul_disaster_events.txt`](../events/verne_overhaul_disaster_events.txt)
- [`common/event_modifiers/verne_overhaul_modifiers.txt`](../common/event_modifiers/verne_overhaul_modifiers.txt)

Done when:
- Shattering of Silver Oaths scaffold exists
- Scandal of the Red Court scaffold exists
- Chapterhouse Feud scaffold exists
- Overseas Overstretch of the Vernissage scaffold exists

## Recommended next task order
If we are picking one task at a time, the safest next order is:

1. V-00
2. V-01
3. V-02
4. V-03
5. V-05
6. V-06
7. V-07
8. V-08
9. V-09
10. V-10
11. V-11
12. V-12
13. V-13
14. V-14
15. V-15
16. V-16
17. V-17
18. V-20

That sequence gets us from vague theorycraft to a real first playable Verne slice without taking giant blind swings.
