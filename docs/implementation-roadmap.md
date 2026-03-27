# Verne Overhaul - Implementation Roadmap

## Goal of this roadmap
Turn the long theorycraft into a build order that is safe for beginner-guided Codex sessions.

Each milestone should leave the repo in a better, still-loadable state. Early work should favor helper files, exact object names, and a narrow first-wave doctrine slice over giant all-at-once rewrites.

Use [`docs/codex-grounding-checklist.md`](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/codex-grounding-checklist.md) at the start of every coding milestone.

## Safety gate before every coding milestone
Before editing files, the session should confirm four things:

1. Which exact repo files were read first.
2. Which existing implementation pattern will be mirrored.
3. Which touched files are shared multi-country files versus safe Verne-only files.
4. Which generic EU4 or Anbennar systems may still depend on vanilla/basic idea-group checks.

If those four points are not known yet, the session is still in grounding mode and should not start coding.

## Milestone 0: Foundation and Grounding Layer
Build the helper layer and naming spine before rewriting big mission or event chains, and document the shared-file anchors that the overhaul must respect.

### Outcomes
- map where Verne already exists in shared idea, localization, monument, mercenary, mission, and on_action files
- create a Verne-specific modifier file
- create a Verne-specific scripted trigger file
- create a Verne-specific scripted effect file
- reserve the first-wave flags and variables
- establish first-wave localization stubs

### Files to create early
- [`common/event_modifiers/verne_overhaul_modifiers.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/common/event_modifiers/verne_overhaul_modifiers.txt)
- [`common/scripted_triggers/verne_overhaul_triggers.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/common/scripted_triggers/verne_overhaul_triggers.txt)
- [`common/scripted_effects/verne_overhaul_effects.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/common/scripted_effects/verne_overhaul_effects.txt)
- [`localisation/verne_overhaul_l_english.yml`](/C:/Users/User/Documents/GitHub/My-Anbennar/localisation/verne_overhaul_l_english.yml)

### Files to inspect early
- [`common/ideas/anb_country_ideas.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/common/ideas/anb_country_ideas.txt)
- [`localisation/anb_powers_and_ideas_l_english.yml`](/C:/Users/User/Documents/GitHub/My-Anbennar/localisation/anb_powers_and_ideas_l_english.yml)
- [`common/ideas/00_basic_ideas.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/common/ideas/00_basic_ideas.txt)
- [`common/great_projects/anb_monuments_missions.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/common/great_projects/anb_monuments_missions.txt)
- [`common/mercenary_companies/0_anb_elite_mercenaries.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/common/mercenary_companies/0_anb_elite_mercenaries.txt)
- [`events/Flavour_Verne_A33.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/events/Flavour_Verne_A33.txt)
- [`common/on_actions/00_on_actions.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/common/on_actions/00_on_actions.txt)

### Done condition
First-wave missions, reforms, dynasty events, and decisions can call shared Verne helpers instead of inlining repeated logic, and the roadmap records which existing shared files must be patched carefully instead of ignored.

## Milestone 1: First-Wave Doctrine Slice
Ship the first seven doctrine groups exactly as named in the theorycraft.

### Doctrine targets
- Silver Oaths Ideas
- Vernissage Ideas
- Dragonwake Ideas
- Imperial Sea Court Ideas
- Red Court Ideas
- Crimson Wake Order Ideas
- Estuary Companies Ideas

### Main files
- [`common/ideas/anb_country_ideas.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/common/ideas/anb_country_ideas.txt)
- [`localisation/anb_powers_and_ideas_l_english.yml`](/C:/Users/User/Documents/GitHub/My-Anbennar/localisation/anb_powers_and_ideas_l_english.yml)
- [`common/ideas/verne_country_ideas_overhaul.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/common/ideas/verne_country_ideas_overhaul.txt)
- [`common/ideas/verne_doctrine_groups.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/common/ideas/verne_doctrine_groups.txt)
- [`common/policies/verne_doctrine_policies.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/common/policies/verne_doctrine_policies.txt)

### Safety checks
- confirm whether `A33_ideas` is safest to patch in place or via a keyed override
- confirm whether the Verne doctrine menu needs shared-file support in [`common/ideas/00_basic_ideas.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/common/ideas/00_basic_ideas.txt)
- audit generic `has_idea_group` consumers in shared policies, reforms, agendas, and decisions before declaring the menu replacement safe

### Done condition
Verne has a usable first-wave doctrine menu, completion bonuses work, first-wave policy pairings exist, and the replacement does not blindly strand Verne outside shared generic systems.

## Milestone 2: First Constitutional Slice
Implement the reform package that makes Verne feel different before the late game.

### Reform targets
- Tier 1 triplet: Court of Silver Oaths / Charter of Great Captains / Ducal Muster of Armoc
- Tier 2 triplet: Admiralty of the Crimson Wake / Estuary Companies of Heartspier / Regatta Discipline
- Tier 3 triplet: Red Court Arcana / Dragonwake Ordinance / Battle-Mage Collegium

### Main file
- [`common/government_reforms/verne_overhaul_reforms.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/common/government_reforms/verne_overhaul_reforms.txt)

### Done condition
Early and midgame Verne can diverge through real reform picks before late doctrine completion.

## Milestone 3: Mission Flexibility Rewrite
Rewrite the first ten priority missions so that overseas progress is no longer railroaded.

### Route logic to support
- classical colonizer route
- subject and ally projection route
- adventure network route
- monument and institution projection route
- doctrine-based overseas projection route

### Priority missions
1. Old Friends, Old Rivals
2. Alvar's Reform
3. The Grand Port of Heartspier
4. The Riches of the Khenak
5. The Vernissage
6. Across the Pond
7. In Search of Adventure
8. Binding the Beast
9. Expand the Wyvern Nests
10. The Lament's Regatta

### Main file
- [`missions/Verne_Missions.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/missions/Verne_Missions.txt)

### Supporting helpers
- use `verne_overseas_projection`
- use `verne_world_network`
- use early precursor flags instead of impossible early doctrine checks

### Done condition
Empire-first, delayed-colonizer, sea-trade, and expedition-heavy runs can all progress through the same mission spine.

## Milestone 4: Dynasty and Court Machine
Turn the dynastic fantasy into real scripted state support.

### Outcomes
- heir-training decision package
- same-dynasty continuity package
- `on_new_heir` safeguard
- exalted lineage and marriage-court progression
- first court advisor archetypes

### Main files
- [`events/verne_overhaul_dynasty_events.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/events/verne_overhaul_dynasty_events.txt)
- [`events/verne_overhaul_advisor_events.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/events/verne_overhaul_advisor_events.txt)
- [`decisions/verne_overhaul_decisions.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/decisions/verne_overhaul_decisions.txt)
- [`common/on_actions/zz_verne_overhaul_on_actions.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/common/on_actions/zz_verne_overhaul_on_actions.txt)

### Pattern anchors
- mirror `on_new_heir` hook style from [`common/on_actions/00_on_actions.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/common/on_actions/00_on_actions.txt)
- mirror Verne `define_heir` and `define_advisor` usage from [`events/Flavour_Verne_A33.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/events/Flavour_Verne_A33.txt)

### Done condition
The silver Verne dynasty is mechanically protected and cultivated instead of left to pure RNG.

## Milestone 5: Order State and Pressure Layer
Add the machinery that makes Verne powerful but demanding to maintain.

### Outcomes
- Chapterhouse monument
- first three order companies
- anti-corruption decisions
- pressure modifiers
- four Verne-specific disasters

### Main files
- [`common/great_projects/anb_monuments_missions.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/common/great_projects/anb_monuments_missions.txt)
- [`common/great_projects/verne_overhaul_monuments.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/common/great_projects/verne_overhaul_monuments.txt)
- [`common/mercenary_companies/0_anb_elite_mercenaries.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/common/mercenary_companies/0_anb_elite_mercenaries.txt)
- [`common/mercenary_companies/verne_overhaul_orders.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/common/mercenary_companies/verne_overhaul_orders.txt)
- [`common/disasters/verne_overhaul_disasters.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/common/disasters/verne_overhaul_disasters.txt)
- [`events/verne_overhaul_disaster_events.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/events/verne_overhaul_disaster_events.txt)

### Safety checks
- patch existing shared Verne monument and elite-merc anchors first where that is cleaner than inventing parallel content
- only move fully into standalone Verne files if keyed overrides or new objects are clearly safer than editing the shared anchor

### Done condition
Verne has thematic failure states tied to the same pillars that make it strong.

## Milestone 6: Expansion Wave
Only after the first playable slice is stable:

- remaining 14 doctrine groups
- full doctrine policy matrix
- later reform tiers
- additional orders and upgraded variants
- advanced magic-state hooks
- artificery integration
- broader artifact and exposition integration
- low-priority anti-Corinite branch

## Safest file dependency order
When in doubt, build in this order:

1. [`common/event_modifiers/verne_overhaul_modifiers.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/common/event_modifiers/verne_overhaul_modifiers.txt)
2. [`common/scripted_triggers/verne_overhaul_triggers.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/common/scripted_triggers/verne_overhaul_triggers.txt)
3. [`common/scripted_effects/verne_overhaul_effects.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/common/scripted_effects/verne_overhaul_effects.txt)
4. [`common/ideas/verne_country_ideas_overhaul.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/common/ideas/verne_country_ideas_overhaul.txt)
5. [`common/ideas/verne_doctrine_groups.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/common/ideas/verne_doctrine_groups.txt)
6. [`common/government_reforms/verne_overhaul_reforms.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/common/government_reforms/verne_overhaul_reforms.txt)
7. [`common/mercenary_companies/verne_overhaul_orders.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/common/mercenary_companies/verne_overhaul_orders.txt)
8. [`decisions/verne_overhaul_decisions.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/decisions/verne_overhaul_decisions.txt)
9. [`events/verne_overhaul_dynasty_events.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/events/verne_overhaul_dynasty_events.txt)
10. [`common/on_actions/zz_verne_overhaul_on_actions.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/common/on_actions/zz_verne_overhaul_on_actions.txt)
11. [`missions/Verne_Missions.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/missions/Verne_Missions.txt)
12. [`localisation/verne_overhaul_l_english.yml`](/C:/Users/User/Documents/GitHub/My-Anbennar/localisation/verne_overhaul_l_english.yml)

## Beginner-safe rule
Do not open with a giant mission rewrite.

The first productive sessions should be:

1. grounding audit plus helper layer
2. first-wave doctrine files
3. first three reform triplets
4. dynasty safeguard
5. then mission rewrites

Do not do blind same-name overrides on shared files without first naming the exact existing object being replaced and the reason that replacement is safe.
