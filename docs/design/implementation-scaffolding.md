# Implementation Scaffolding

This file preserves the engineering-heavy sections from the restructured master plan that were not fully carried into the first draft design docs.

Use it together with:

- [README.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/README.md)
- [open-questions-and-design-lab.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/design/open-questions-and-design-lab.md)
- [docs/codex-grounding-checklist.md](/C:/Users/User/Documents/GitHub/My-Anbennar/docs/codex-grounding-checklist.md)

This file is not a promise that every item is immediately safe to code. It is a preserved implementation blueprint.

## Source note
Primary source for this file:

- [verne_overhaul_restructured_master_plan.md](/C:/Users/User/Downloads/verne_overhaul_restructured_master_plan.md)

## Immediate Next Engineering Slice

The first implementation wave should proceed in this order:

1. Build the first-wave doctrine files with their exact internal 7-idea entries.
2. Build the early precursor-flag layer so first missions do not rely on unavailable idea groups.
3. Implement the Tier 1-3 reform triplets as the minimum viable constitutional package.
4. Implement the dynasty-preservation layer with `define_heir` events and the `on_new_heir` safeguard.
5. Implement the advisor-generation layer for Red Court, Admiralty, and Vernissage archetypes.
6. Implement the Corinite center-of-reformation preserve-and-upgrade event chain.
7. Build the Chapterhouse and the three first-wave order companies, including manpower costs in the founding decisions.
8. Rewrite the first 10 Verne missions around the corrected early/mid/late reward logic.
9. Add the first-wave anti-corruption decisions, pressure modifiers, and the four disaster scaffolds.
10. Add the first-wave exact policy set.
11. Only after that, expand to the remaining reforms, policies, doctrine followups, and advanced artificery hooks.

## File Map

### Core files to create

#### Ideas and policies
- `common/ideas/verne_country_ideas_overhaul.txt`
  Purpose: keyed replacement for `A33_ideas`
- `common/ideas/verne_doctrine_groups.txt`
  Purpose: 21 Verne-exclusive doctrine groups
- `common/policies/verne_doctrine_policies.txt`
  Purpose: Verne doctrine policy definitions

#### Triggers and effects
- `common/scripted_triggers/verne_overhaul_triggers.txt`
  Purpose: doctrine-availability checks, dynasty-state checks, projection-score threshold checks, order-founding legality checks
- `common/scripted_effects/verne_overhaul_effects.txt`
  Purpose: score increments, mission reward bundles, order founding effects, dynastic correction helpers, advisor spawn helpers

#### Reforms, monuments, mercs, disasters
- `common/government_reforms/verne_overhaul_reforms.txt`
  Purpose: Verne reform triplets
- `common/great_projects/verne_overhaul_monuments.txt`
  Purpose: Chapterhouse and any new Verne monuments not patched into existing files
- `common/mercenary_companies/verne_overhaul_orders.txt`
  Purpose: Crimson Wake Lances, Heartspier Skyguard, Khenak Talons, and later variants
- `common/disasters/verne_overhaul_disasters.txt`
  Purpose: the four Verne-specific disasters

#### Events and decisions
- `events/verne_overhaul_dynasty_events.txt`
  Purpose: same-dynasty heir handling, marriage-court events, lineage exaltation events
- `events/verne_overhaul_magic_events.txt`
  Purpose: Red Court, paragonhood, infamy-control, battle-mage events
- `events/verne_overhaul_advisor_events.txt`
  Purpose: `define_advisor` helper events and court specialist arrivals
- `events/verne_overhaul_disaster_events.txt`
  Purpose: disaster start, pulse, and resolution events
- `decisions/verne_overhaul_decisions.txt`
  Purpose: heir training, Red Court, anti-corruption, order founding, advisor patronage

#### On-actions and modifiers
- `common/on_actions/zz_verne_overhaul_on_actions.txt`
  Purpose: `on_new_heir` hook plus optional ruler, marriage, or disaster support hooks
- `common/event_modifiers/verne_overhaul_modifiers.txt`
  Purpose: permanent and timed country/province modifiers used by the overhaul

#### Missions and localisation
- `missions/Verne_Missions.txt`
  Purpose: same-name override for the mission tree rewrite
- `localisation/verne_overhaul_l_english.yml`
  Purpose: all new loc for ideas, reforms, policies, decisions, modifiers, events, merc companies, and disasters

### Files likely to patch carefully

#### Existing Verne systems to preserve and patch
- `decisions/VerneDecisions.txt`
  Reason: reuse or expansion of `verne_launch_adventure`
- `common/scripted_effects/anb_scripted_effects_for_verne.txt`
  Reason: extend the Port of Adventure reward chain if possible
- `events/Flavour_Verne_A33.txt`
  Reason: preserve and patch existing event chains where that is cleaner than fully parallel events

#### Existing shared hooks to touch only if needed
- `common/custom_gui/provinceview.txt`
- `interface/provinceview.gui`

Only touch the GUI files if the Port of Adventure button itself is expanded, not merely reused.

## Object Naming Plan

### Doctrine groups
- `verne_silver_oaths_ideas`
- `verne_red_court_ideas`
- `verne_estuary_companies_ideas`
- `verne_khenak_foundry_ideas`
- `verne_vernissage_patronage_ideas`
- `verne_corinite_stewardship_ideas`
- `verne_imperial_chancery_ideas`
- `verne_vernissage_ideas`
- `verne_imperial_sea_court_ideas`
- `verne_grand_regatta_ideas`
- `verne_overseas_commandery_ideas`
- `verne_eastern_correspondence_ideas`
- `verne_apostolic_sea_lanes_ideas`
- `verne_pearlescent_concord_ideas`
- `verne_dragonwake_ideas`
- `verne_crimson_wake_order_ideas`
- `verne_battle_evocation_ideas`
- `verne_red_brass_ideas`
- `verne_sea_lance_doctrine_ideas`
- `verne_apostolic_valour_ideas`
- `verne_silver_banner_ideas`

### Reforms
Prefix all custom reforms with `verne_`.

Examples:
- `verne_court_of_silver_oaths`
- `verne_charter_of_great_captains`
- `verne_ducal_muster_of_armoc`
- `verne_red_court_arcana`
- `verne_battle_mage_collegium`

### Orders / mercenary companies
- `merc_verne_crimson_wake_lances`
- `merc_verne_heartspier_skyguard`
- `merc_verne_khenak_talons`

Upgraded variants should use suffixes like:
- `_veteran`
- `_royal`
- `_high_eyries`

### Disasters
- `verne_shattering_of_silver_oaths`
- `verne_scandal_of_the_red_court`
- `verne_chapterhouse_feud`
- `verne_overseas_overstretch`

### Decisions
- `verne_train_heir_red_court`
- `verne_induct_heir_dragonwake`
- `verne_present_heir_vernissage`
- `verne_drill_battle_mage_court`
- `verne_elevate_storm_crowned_prince`
- `verne_purge_admiralty_ledgers`
- `verne_muster_ducal_auditors`
- `verne_red_court_inquest`
- `verne_found_crimson_wake_lances`
- `verne_charter_heartspier_skyguard`
- `verne_raise_khenak_talons`

### Flags and variables
Keep all custom flags and variables under a strict `verne_` prefix.

## First Code Slice Dependency Order

1. `verne_overhaul_modifiers.txt`
2. `verne_overhaul_triggers.txt`
3. `verne_overhaul_effects.txt`
4. `verne_country_ideas_overhaul.txt`
5. `verne_doctrine_groups.txt`
6. `verne_overhaul_reforms.txt`
7. `verne_overhaul_orders.txt`
8. `verne_overhaul_decisions.txt`
9. `verne_overhaul_dynasty_events.txt`
10. `zz_verne_overhaul_on_actions.txt`
11. `Verne_Missions.txt`
12. localization file

## Scripted Trigger Catalog

### Doctrine and precursor triggers
- `is_verne_overhaul_country_trigger`
- `has_verne_early_court_path_trigger`
- `has_verne_early_captains_path_trigger`
- `has_verne_early_muster_path_trigger`
- `has_verne_early_maritime_path_trigger`
- `has_verne_early_estuary_path_trigger`
- `has_verne_early_regatta_path_trigger`

### Dynastic-state triggers
- `has_verne_dynasty_protected_trigger`
- `has_verne_dynasty_exalted_trigger`
- `has_verne_marriage_court_active_trigger`
- `verne_heir_is_not_sil_verne_trigger`
- `verne_should_correct_dynasty_trigger`

### Projection-score triggers
- `verne_has_projection_3_trigger`
- `verne_has_projection_4_trigger`
- `verne_has_projection_6_trigger`
- `verne_has_world_network_5_trigger`
- `verne_has_world_network_8_trigger`
- `verne_has_dynastic_magic_5_trigger`

### Order and monument triggers
- `verne_can_build_chapterhouse_trigger`
- `verne_can_found_crimson_wake_lances_trigger`
- `verne_can_found_heartspier_skyguard_trigger`
- `verne_can_found_khenak_talons_trigger`
- `verne_has_order_state_path_trigger`

### Pressure-state triggers
- `verne_low_legitimacy_pressure_trigger`
- `verne_low_prestige_pressure_trigger`
- `verne_low_power_projection_pressure_trigger`
- `verne_red_court_scandal_pressure_trigger`

## Scripted Effect Catalog

### Score and flag effects
- `verne_add_overseas_projection_1_effect`
- `verne_add_world_network_1_effect`
- `verne_add_dynastic_magic_1_effect`
- `verne_set_early_court_path_effect`
- `verne_set_early_captains_path_effect`
- `verne_set_early_muster_path_effect`
- `verne_set_early_maritime_path_effect`
- `verne_set_early_estuary_path_effect`
- `verne_set_early_regatta_path_effect`

### Dynastic effects
- `verne_define_sil_verne_heir_effect`
- `verne_correct_to_sil_verne_heir_effect`
- `verne_apply_dynasty_protected_effect`
- `verne_apply_dynasty_exalted_effect`
- `verne_apply_marriage_court_effect`

### Advisor effects
- `verne_spawn_red_court_magister_effect`
- `verne_spawn_grand_admiral_effect`
- `verne_spawn_vernissage_curator_effect`
- `verne_spawn_khenak_founder_effect`

### Order effects
- `verne_found_crimson_wake_lances_effect`
- `verne_found_heartspier_skyguard_effect`
- `verne_found_khenak_talons_effect`
- `verne_pay_order_manpower_cost_effect`
- `verne_unlock_order_variant_effect`

### Pressure and cleanup effects
- `verne_apply_tarnished_courtly_reputation_effect`
- `verne_apply_fading_ducal_authority_effect`
- `verne_apply_empty_boasts_of_the_wake_effect`
- `verne_reduce_minor_corruption_effect`
- `verne_reduce_magic_infamy_small_effect`

### Mission reward bundle effects
- `verne_reward_old_friends_old_rivals_effect`
- `verne_reward_alvars_reform_effect`
- `verne_reward_grand_port_effect`
- `verne_reward_vernissage_effect`
- `verne_reward_binding_the_beast_effect`

### Design rule
All first-wave missions, decisions, and dynasty events should call helper effects instead of inlining huge logic blocks.

## Event Namespaces and Core Objects

### Dynasty events
- `namespace = verne_overhaul_dynasty`
- `verne_overhaul_dynasty.1`
  Purpose: `on_new_heir` dynasty safeguard checker
- `verne_overhaul_dynasty.2`
  Purpose: replace incorrect heir with defined sil Verne heir
- `verne_overhaul_dynasty.3`
  Purpose: marriage-court prestige event
- `verne_overhaul_dynasty.4`
  Purpose: exalted lineage accession event

### Advisor events
- `namespace = verne_overhaul_advisors`
- `verne_overhaul_advisors.1`
  Purpose: invite a Magister of the Red Court
- `verne_overhaul_advisors.2`
  Purpose: commission a Grand Admiral of the Wake
- `verne_overhaul_advisors.3`
  Purpose: patronize a Curator of the Vernissage
- `verne_overhaul_advisors.4`
  Purpose: recruit a Khenak Master Founder

### Magic and pressure events
- `namespace = verne_overhaul_magic`
- `verne_overhaul_magic.1`
  Purpose: controlled evocation success
- `verne_overhaul_magic.2`
  Purpose: Red Court backlash
- `verne_overhaul_magic.3`
  Purpose: paragon-support event
- `verne_overhaul_magic.4`
  Purpose: witch-king temptation event

### Anti-corruption events
- `namespace = verne_overhaul_cleansing`
- `verne_overhaul_cleansing.1`
  Purpose: Purge the Admiralty Ledgers outcome
- `verne_overhaul_cleansing.2`
  Purpose: Muster the Ducal Auditors outcome
- `verne_overhaul_cleansing.3`
  Purpose: Red Court Inquest outcome

### Order-founding events
- `namespace = verne_overhaul_orders`
- `verne_overhaul_orders.1`
  Purpose: found Crimson Wake Lances
- `verne_overhaul_orders.2`
  Purpose: found Heartspier Skyguard
- `verne_overhaul_orders.3`
  Purpose: found Khenak Talons
- `verne_overhaul_orders.4`
  Purpose: unlock veteran, royal, or high-eyries variants

## First-Wave Implementation Constants

### Dynasty safeguard constants
- if dynasty-protected and heir is not sil Verne: `70%` correction weight
- if dynasty-exalted: `100%` correction weight
- if marriage-court is active and legitimacy is `75+`: prestige gain on corrected succession

### Order founding constants
| Order | Ducats | MIL | Manpower |
|---|---|---|---|
| Crimson Wake Lances | `250-300` | `50` | `3000` |
| Heartspier Skyguard | `225-275` | `40` | `3500` |
| Khenak Talons | `200-250` | `50` | `4500` |

### Anti-corruption constants
- each active purge decision reduces corruption by `1`
- cooldowns should be `10-12 years`
- no single button should zero out a corrupt state instantly

### Pressure-modifier constants
- Tarnished Courtly Reputation: `5-year` duration
- Fading Ducal Authority: `5-year` duration
- Empty Boasts of the Wake: `5-year` duration

## Mission Coding Rule

### Rule
For the first 10 rewritten Verne missions:
- early missions use precursor flags, marriage state, legitimacy, alliances, and reforms
- mid missions may use doctrine groups if legally available
- late missions may use doctrine groups and score thresholds heavily

### Hard ban
Do not let a mission both:
- unlock a doctrine group
- and immediately check progress inside that same doctrine group

Use latent-synergy flags and later followup events instead.

## Code-Shaped Helper Definitions

### Scripted trigger shapes

#### `is_verne_overhaul_country_trigger`
- Purpose: central country gate for all Verne-only systems
- Shape:
  - true if `tag = A33`
  - also true for formed Verne if the formation path changes tag later and the design still wants access preserved

#### `verne_should_correct_dynasty_trigger`
- Purpose: decide whether a newly generated heir should be replaced or corrected into the sil Verne line
- Shape:
  - country passes `is_verne_overhaul_country_trigger`
  - has `verne_dynasty_protected` or `verne_dynasty_exalted`
  - has an heir
  - heir dynasty is not the intended Verne line
  - not in a special edge case where succession should be allowed to drift intentionally

#### `verne_low_legitimacy_pressure_trigger`
- Purpose: shared disaster/event pressure gate
- Shape:
  - legitimacy below `50`
  - has at least one major dynastic-state flag or reform

#### `verne_can_found_crimson_wake_lances_trigger`
- Purpose: order-founding legality gate
- Shape:
  - Chapterhouse path active
  - Chapterhouse at required tier
  - company not already unlocked
  - enough money
  - enough manpower
  - enough MIL or other required resource

### Scripted effect shapes

#### `verne_define_sil_verne_heir_effect`
- Purpose: create a same-dynasty heir cleanly
- Shape:
  - `define_heir = { dynasty = ROOT ... }` or explicit dynasty text if safer
  - stat weighting based on current dynastic-state level
  - optional chance for Blood of the Wyvern-Kings
  - optional chance for mage support if Red Court infrastructure is active

#### `verne_pay_order_manpower_cost_effect`
- Purpose: centralize order-founding resource payment
- Shape:
  - subtract ducats
  - subtract manpower
  - subtract MIL if relevant
  - optionally apply small prestige or army-tradition rider

#### `verne_spawn_grand_admiral_effect`
- Purpose: create the maritime court advisor cleanly
- Shape:
  - `define_advisor = { type = naval_reformer ... }`
  - skill `2` or `3` depending on source
  - cost discount if created through a premium mission/decision

#### `verne_reduce_magic_infamy_small_effect`
- Purpose: central helper for disciplined-evocation containment
- Shape:
  - use the cleanest available Anbennar infamy reduction path
  - should never erase all pressure at once
  - intended as a small paragon-support lever

### First decision skeletons

#### `verne_train_heir_red_court`
- Potential:
  - Verne trigger
  - has heir
  - not on cooldown
  - has Red Court infrastructure or Mages support
- Allow:
  - enough ducats
  - enough ADM or MIL
  - Mages interaction threshold if used
- Effect:
  - resource payment
  - set cooldown flag
  - fire Verne dynasty training event

#### `verne_induct_heir_dragonwake`
- Potential:
  - Verne trigger
  - has heir
  - noble/wyvern path sufficiently advanced
- Allow:
  - ducats
  - MIL
  - maybe army tradition threshold
- Effect:
  - pay resources
  - set cooldown
  - fire martial-heir event

#### `verne_found_crimson_wake_lances`
- Potential:
  - Verne trigger
  - Chapterhouse active
  - not already founded
- Allow:
  - `verne_can_found_crimson_wake_lances_trigger`
- Effect:
  - `verne_pay_order_manpower_cost_effect`
  - `unlock_merc_company = { merc_company = merc_verne_crimson_wake_lances free_merc = yes }`
  - set permanent founding flag
  - small prestige/army-tradition gain

#### `verne_purge_admiralty_ledgers`
- Potential:
  - Verne trigger
  - corruption above a modest threshold or port-state infrastructure active
  - not on cooldown
- Allow:
  - ducats and ADM
- Effect:
  - reduce corruption
  - maybe add mercantilism for a harsher branch
  - maybe anger Burghers

### First event skeletons

#### `verne_overhaul_dynasty.1`
- Trigger context: `on_new_heir`
- Logic:
  - if `verne_should_correct_dynasty_trigger = yes`
  - after short delay call correction event

#### `verne_overhaul_dynasty.2`
- Logic:
  - remove or replace incorrect heir as needed
  - use `verne_define_sil_verne_heir_effect`
  - grant prestige if dynasty-exalted stage is active
  - if marriage-court is active and legitimacy is high, add extra legitimacy or prestige

#### `verne_overhaul_advisors.2`
- Logic:
  - `define_advisor = { type = naval_reformer skill = 3 cost_multiplier = 0.5 }`
  - optional culture assignment if appropriate
  - add small navy-tradition rider

#### `verne_overhaul_orders.1`
- Logic:
  - fires from founding decision
  - unlocks company
  - adds prestige
  - sets order-state flag
  - maybe increments `verne_overseas_projection` or army tradition slightly

## Repository-Verified Implementation Anchors

### `on_new_heir` pattern
The repo already uses `on_new_heir` as a bundle hook that fires delayed country events for heir correction, race correction, magical inheritance, and other succession cleanup.

Verne implication:
- do not solve dynasty preservation inline inside every heir-creation event
- use one small Verne `on_new_heir` hook in a dedicated on_actions file
- then call a delayed Verne dynasty event chain

### `define_heir` pattern
The repo contains many instances of `define_heir = { dynasty = ROOT ... }` in country flavor and succession events.

Verne implication:
- same-dynasty continuity for sil Verne should use this exact pattern
- this is cleaner than relying only on passive heir-chance modifiers

### `define_advisor` pattern
The repo repeatedly uses event-driven `define_advisor = { type = ... skill = ... culture = ... cost_multiplier = ... }`, often through `random_list` or mission/event options.

Verne implication:
- the specialized Verne court advisor system should use the same event-driven model
- spawn the advisor through an event or decision
- set skill and cost multiplier directly
- only then optionally support it with country modifiers

### Mercenary company upgrade pattern
The repo's Marrhold content is the best direct analogue for Verne's order companies. It uses:
- a first company unlock
- later mission-driven upgrade variants
- `clr_country_flag = unlocked_merc_*` on the old company
- then `unlock_merc_company = { merc_company = ... free_merc = yes }` on the upgraded company

Verne implication:
- the Chapterhouse path should follow this exact logic
- unlock first wyvern order, then replace it with stronger variants or unlock sister companies later
- do not try to live-edit a single company's manpower/cap profile mid-run

### Flying knight balance anchor
Marrhold griffon companies in `common/mercenary_companies/0_anb_elite_mercenaries.txt` provide the best balance anchor for Verne's wyvern orders.

Verne implication:
- stay inside that balance family
- elite
- movement-heavy
- cavalry-dominant
- not absurdly larger than existing griffon analogues

### Mission reward scripting pattern
The repo uses direct mission effects plus helper effects/modifiers rather than building all logic inline into one giant mission reward block.

Verne implication:
- keep mission bodies readable
- move repeated reward logic into scripted effects
- reserve large nested conditions for only the most complex rewards

### Shared-system caution
The current Verne Port of Adventure system already touches:
- missions
- scripted effects
- GUI/custom button infrastructure
- province modifiers

Verne implication:
- do not casually rewrite the GUI side first
- for v1, preserve the existing button and GUI path
- extend rewards and country tracking around it
- only touch `provinceview` / custom GUI files if absolutely necessary

### Build rule from the repo pass
The safest Verne overhaul path is:

1. preserve and patch existing Verne systems where possible
2. build new helper layers in parallel files
3. only override same-name core files where a full rewrite is actually needed
