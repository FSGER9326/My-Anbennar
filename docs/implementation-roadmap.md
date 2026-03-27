# Verne Overhaul - Implementation Roadmap

## Goal of this roadmap
Turn the long theorycraft into a build order that is safe for beginner-guided Codex sessions.

Each milestone should leave the repo in a better, still-loadable state. Early work should favor helper files, exact object names, and a narrow first-wave doctrine slice over giant all-at-once rewrites.

## Milestone 0: Foundation Layer
Build the helper layer and naming spine before rewriting big mission or event chains.

### Outcomes
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

### Done condition
First-wave missions, reforms, dynasty events, and decisions can call shared Verne helpers instead of inlining repeated logic.

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
- [`common/ideas/verne_country_ideas_overhaul.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/common/ideas/verne_country_ideas_overhaul.txt)
- [`common/ideas/verne_doctrine_groups.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/common/ideas/verne_doctrine_groups.txt)
- [`common/policies/verne_doctrine_policies.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/common/policies/verne_doctrine_policies.txt)

### Done condition
Verne has a usable first-wave doctrine menu, completion bonuses work, and first-wave policy pairings exist.

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
- [`common/great_projects/verne_overhaul_monuments.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/common/great_projects/verne_overhaul_monuments.txt)
- [`common/mercenary_companies/verne_overhaul_orders.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/common/mercenary_companies/verne_overhaul_orders.txt)
- [`common/disasters/verne_overhaul_disasters.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/common/disasters/verne_overhaul_disasters.txt)
- [`events/verne_overhaul_disaster_events.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/events/verne_overhaul_disaster_events.txt)

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

1. helper layer
2. first-wave doctrine files
3. first three reform triplets
4. dynasty safeguard
5. then mission rewrites
