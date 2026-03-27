# Verne Overhaul - Working Spec

## Source of truth
This repo summary is the condensed build version of `Verne Overhaul Master Plan (2.1)`.

The long-form theorycraft remains the design source of truth. This file exists to answer a simpler question:

What are we actually trying to ship in the first playable overhaul slice?

## Core fantasy
Verne should feel like a silver-tongued, red-sailed, wyvern-crowned, evocation-blooded imperial court.

It is not meant to be a generic strong country. Its identity is built from:

- courtly diplomacy
- sea-trade projection
- mage-dynasty shaping
- wyvern-knightly warfare
- adventurous overseas reach

## Campaign shapes the overhaul must support
The overhaul should support multiple valid Verne campaigns instead of forcing one narrow opener.

- empire-first Verne
- sea-trade Verne
- mage-court Verne
- wyvern-order Verne
- delayed-colonizer Verne
- Corinite imperial Verne
- industrial red-brass Verne

## Hard implementation principles
- Use real EU4 and Anbennar systems wherever possible.
- Prefer country flags, country variables, mission completion, reforms, decisions, merc companies, monuments, ruler personalities, heir logic, and existing Anbennar magic systems.
- Avoid fake province-292-only pseudo-state logic unless there is no cleaner option.
- Preserve and patch working Verne content before inventing replacements.
- Keep the overhaul modular and submod-friendly.

## Structural corrections from the theorycraft
The overhaul is meant to correct four problems in the current planning state:

1. The country identity was compressed into vague buckets instead of executable work.
2. The doctrine menu was still too partial and did not clearly support different campaign shapes.
3. Early missions were at risk of checking doctrine groups before doctrine groups could legally exist.
4. The dynasty, order, and pressure systems were described in theory but not yet translated into build order.

## First playable overhaul slice
The first playable slice is not the whole project. It is the minimum version that proves the overhaul works.

### Pillar 1: First-wave doctrine menu
Ship the first seven doctrine groups with their exact internal entries:

- Silver Oaths Ideas
- Vernissage Ideas
- Dragonwake Ideas
- Imperial Sea Court Ideas
- Red Court Ideas
- Crimson Wake Order Ideas
- Estuary Companies Ideas

### Pillar 2: First-wave constitutional reform slice
Ship the first three reform triplets:

- Tier 1: Foundations of the Vernman State
- Tier 2: Sea State Formation
- Tier 3: Red Court Transformation

### Pillar 3: Mission flexibility rewrite
Rewrite the first ten missions that establish the new doctrine state:

- Old Friends, Old Rivals
- Alvar's Reform
- The Grand Port of Heartspier
- The Riches of the Khenak
- The Vernissage
- Across the Pond
- In Search of Adventure
- Binding the Beast
- Expand the Wyvern Nests
- The Lament's Regatta

### Pillar 4: Dynasty preservation
Ship the silver Verne dynasty package:

- heir-training decisions
- same-dynasty continuity support
- `on_new_heir` safeguard
- marriage-court progression

### Pillar 5: Order state
Ship the Chapterhouse and first three order companies:

- The Crimson Wake Lances
- The Heartspier Skyguard
- The Khenak Talons

### Pillar 6: Pressure and failure states
Ship the first maintenance and punishment layer:

- anti-corruption decisions
- pressure modifiers
- four Verne-specific disasters

## Key systems that should be preserved and upgraded
- existing Verne mission tree structure in [`missions/Verne_Missions.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/missions/Verne_Missions.txt)
- existing adventure decision structure in [`decisions/VerneDecisions.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/decisions/VerneDecisions.txt)
- existing Port of Adventure logic in [`common/scripted_effects/anb_scripted_effects_for_verne.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/common/scripted_effects/anb_scripted_effects_for_verne.txt)
- existing Verne flavor chains in [`events/Flavour_Verne_A33.txt`](/C:/Users/User/Documents/GitHub/My-Anbennar/events/Flavour_Verne_A33.txt)
- existing Corinite conversion pattern already present for Verne

## First-wave variables and flags
The first engineering slice should establish these as shared planning anchors:

### Country variables
- `verne_overseas_projection`
- `verne_world_network`
- `verne_dynastic_magic_machine`

### Early path and state flags
- `verne_unlock_silver_oaths_ideas`
- `verne_unlock_vernissage_ideas`
- `verne_unlock_dragonwake_ideas`
- `verne_unlock_chapterhouse`
- `verne_unlock_tier1_reforms`
- `verne_unlock_tier3_reforms`
- `verne_unlock_tier6_reforms`
- `verne_seed_silver_oaths`
- `verne_seed_estuary_companies`
- `verne_seed_dragonwake`
- `verne_seed_khenak_foundry`
- `verne_seed_chapterhouse_orders`
- `verne_dynasty_protected`
- `verne_dynasty_exalted`
- `verne_marriage_court_active`

## Definition of done for v0.1 alpha
- Verne has a real first-wave doctrine menu instead of vague placeholders.
- Early missions use precursor flags, reform choices, and country-state checks instead of impossible early doctrine checks.
- Overseas missions accept multiple route families instead of a single colonizer script.
- Dynasty continuity is supported proactively, not only reactively.
- Orders, court, and pressure systems all exist as real gameplay objects.
- New content is grouped under consistent `verne_` names and dedicated files.
- All new objects have localization.
- No touched files produce startup script errors.

## Not in the first playable slice
- all 21 doctrine groups
- full doctrine policy matrix
- full reform ladder beyond the first three triplets
- large anti-Corinite alternate route
- full artificery route
- broad GUI rewrites

## Working rule for future sessions
If a task cannot be described as a concrete file change with named objects and a clear done condition, it is still theorycraft and must be broken down further before coding starts.
