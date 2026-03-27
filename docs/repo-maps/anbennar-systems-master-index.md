# Anbennar Systems Master Index

This article is the starting point for documenting Anbennar systems that go beyond normal EU4 wiki coverage.

It is a repo-grounding document, not a design proposal.

Use it when you want:

- a fast map of which Anbennar systems are custom rather than vanilla-style
- examples of where to look before inventing a new mechanic from scratch
- a shortlist of systems that may already solve part of a new design problem
- a reminder that many Anbennar features are implemented across multiple files at once

## Quick Verdict

Anbennar does not usually implement its unique mechanics as single isolated files.

The common pattern is:

1. a visible player entry point such as a decision, estate action, government interaction, or custom GUI button
2. scripted triggers that decide whether the feature is legal
3. scripted effects that do the real work
4. event modifiers, variables, flags, and personalities that hold state
5. event chains that deliver outcomes or maintenance pulses
6. localisation and GUI support layered on top

That means the safest way to extend Anbennar is usually to adapt an existing multi-file pattern rather than copy a single effect line.

## Core Reusable Categories

| Category | Why it matters | Main repo areas | Current doc status |
|---|---|---|---|
| Magic framework | Full custom system for magic access, schools, mana, study, patrons, projects, duels, lichdom, witch-kings, and war wizards | `common/custom_gui`, `common/scripted_effects`, `common/scripted_triggers`, `common/event_modifiers`, `events`, `decisions`, `localisation` | Detailed |
| Powerful mage and succession handling | Reusable heir, ruler, consort, and inheritance patterns for magical continuity | `common/scripted_effects`, `events/Magic_*.txt`, `common/on_actions` | Detailed |
| Magic projects | Shared project framework with dispatcher events, milestone handlers, and progress hooks | `common/scripted_effects`, `events/Magic_*.txt`, `common/custom_gui`, `common/on_actions` | Detailed |
| Verne overseas systems | Example of mission plus GUI plus scripted helper plus variable tracking | `missions`, `events`, `common/scripted_effects`, `common/custom_gui`, `interface` | Detailed |
| Verne wyvern orders and monument coupling | Nation-specific mercenary/order/monument bundle with mission and event wiring | `missions/Verne_Missions.txt`, `events/Flavour_Verne_A33.txt`, `common/mercenary_companies`, `common/great_projects` | Detailed |
| Verne wyvernrider estate ecosystem | Mutual-exclusion estate lanes with shared action wrapper and compatibility guards | `common/estate_privileges`, `decisions/VerneDecisions.txt`, `events/Flavour_Verne_A33.txt` | Detailed |
| Racial population and military systems | Population tolerance, racial administration, racial military tech and UI sorting systems | `events/anb_racial_*`, `common/scripted_effects`, `common/scripted_triggers`, `common/custom_gui`, `localisation` | Detailed |
| Artificery | Custom research and invention layer with its own estate, points, and interface hooks | `events/Artifice*.txt`, `common/scripted_effects`, `common/scripted_triggers`, `common/estate_privileges`, `common/estates` | Detailed |
| Adventurer systems | Adventurer estate plus government mechanic plus spawnable/event content | `common/government_mechanics`, `events/estate_adventurers.txt`, `events/AdventurerSpawnables.txt` | Detailed |
| Witch-king, lichdom, war wizard, magical infamy | High-risk ruler-magic state machine with infamy tiers and conversion helpers | `common/scripted_effects`, `common/scripted_triggers`, `events`, `decisions`, `common/event_modifiers`, `common/custom_gui` | Detailed |
| Government mechanics + GUI wiring | Reusable government power bars/interactions with custom interfaces | `common/government_mechanics`, `interface/government_mechanics` | Detailed |
| Government mechanic activation map | How `government_abilities` in reforms wire mechanics into live gameplay | `common/government_reforms/*.txt`, `common/government_mechanics/*.txt` | Detailed |
| Custom estate ecosystems | Organization/law privilege trees wired to larger systems | `common/estates`, `common/estate_privileges`, `events/estate_*.txt` | Detailed |
| Custom estates | Mages, Adventurers, Artificers, Vampires, Commands, castes, and other non-vanilla estates | `common/estates`, `common/estate_privileges`, `events/estate_*.txt` | Overview |
| Custom government mechanics | Large library of tag- and region-specific government power systems | `common/government_mechanics`, `interface/government_mechanics` | Overview |
| Custom GUI infrastructure | Shared pattern used by magic, province systems, racial UI, and other non-vanilla layers | `common/custom_gui`, `interface/*.gui`, `interface/*.gfx` | Overview |
| Special diplomacy, peace, rebels, units | Extra support layers for non-vanilla content | `common/new_diplomatic_actions`, `common/peace_treaties`, `common/rebel_types`, `common/units` | Index only |

## Registry maintenance rule

To reduce future merge conflicts in this index:

- append new article links at the end of the `Existing Reference Articles` list
- defer major reordering to dedicated cleanup commits

## Existing Reference Articles

- [port-of-adventure-system.md](./port-of-adventure-system.md)
- [verne-launch-adventure-system.md](./verne-launch-adventure-system.md)
- [network-of-adventure-system.md](./network-of-adventure-system.md)
- [magic-systems-reference.md](./magic-systems-reference.md)
- [powerful-mage-and-succession-reference.md](./powerful-mage-and-succession-reference.md)
- [magic-projects-reference.md](./magic-projects-reference.md)
- [racial-population-and-military-reference.md](./racial-population-and-military-reference.md)
- [artificery-research-and-inventions-reference.md](./artificery-research-and-inventions-reference.md)
- [adventurer-systems-and-estate-patterns-reference.md](./adventurer-systems-and-estate-patterns-reference.md)
- [anbennar-non-vanilla-systems-overview.md](./anbennar-non-vanilla-systems-overview.md)
- [anbennar-systems-scan-roadmap.md](./anbennar-systems-scan-roadmap.md)
- [witch-king-lichdom-war-wizard-infamy-reference.md](./witch-king-lichdom-war-wizard-infamy-reference.md)
- [custom-government-mechanics-and-gui-patterns-reference.md](./custom-government-mechanics-and-gui-patterns-reference.md)
- [government-mechanic-activation-map-by-reform-reference.md](./government-mechanic-activation-map-by-reform-reference.md)
- [custom-estate-and-privilege-ecosystems-reference.md](./custom-estate-and-privilege-ecosystems-reference.md)
- [verne-wyvern-orders-mercs-and-monuments-reference.md](./verne-wyvern-orders-mercs-and-monuments-reference.md)
- [verne-wyvernrider-estate-ecosystem-reference.md](./verne-wyvernrider-estate-ecosystem-reference.md)
- [anbennar-vs-eu4-mechanics-gap-register.md](./anbennar-vs-eu4-mechanics-gap-register.md)
- [custom-estates-family-and-privilege-framework-base-vs-anbennar-reference.md](./custom-estates-family-and-privilege-framework-base-vs-anbennar-reference.md)
- [religion-behavior-deltas-for-verne-reference.md](./religion-behavior-deltas-for-verne-reference.md)
- [unit-system-deltas-base-vs-anbennar-reference.md](./unit-system-deltas-base-vs-anbennar-reference.md)
- [rebel-system-deltas-base-vs-anbennar-reference.md](./rebel-system-deltas-base-vs-anbennar-reference.md)
- [peace-treaty-layer-base-vs-anbennar-reference.md](./peace-treaty-layer-base-vs-anbennar-reference.md)
- [diplomatic-actions-layer-base-vs-anbennar-reference.md](./diplomatic-actions-layer-base-vs-anbennar-reference.md)
- [government-mechanics-library-base-vs-anbennar-reference.md](./government-mechanics-library-base-vs-anbennar-reference.md)
- [automated-grep-checklists-by-mechanic-family.md](./automated-grep-checklists-by-mechanic-family.md)
- [verne-monument-object-id-parity-check-reference.md](./verne-monument-object-id-parity-check-reference.md)
- [verne-adventure-chain-mission-event-localization-parity-reference.md](./verne-adventure-chain-mission-event-localization-parity-reference.md)
- [verne-cross-nation-mission-interaction-watchlist.md](./verne-cross-nation-mission-interaction-watchlist.md)
- [repo-rescan-playbook.md](./repo-rescan-playbook.md)

## Magic System Family

The magic family is one of the clearest examples of how Anbennar differs from vanilla EU4.

It includes:

- a topbar-style custom GUI menu
- eight tracked schools of magic
- powerful mage personality generation
- ruler, heir, and consort handling
- mana and experience variables
- study events and study progress pulses
- custom spell lists by group and subgroup
- patrons
- unique magical projects
- war wizard conversion
- lichdom
- witch-king progression
- magic duels
- cross-links to races and artificery

Core anchors:

- [common/custom_gui/magic_menu.txt](../../common/custom_gui/magic_menu.txt)
- [common/custom_gui/magic_spell_lists.txt](../../common/custom_gui/magic_spell_lists.txt)
- [common/custom_gui/magic_unique_projects.txt](../../common/custom_gui/magic_unique_projects.txt)
- [common/scripted_triggers/anb_scripted_triggers_magic.txt](../../common/scripted_triggers/anb_scripted_triggers_magic.txt)
- [common/scripted_effects/anb_scripted_effects_for_magic_system.txt](../../common/scripted_effects/anb_scripted_effects_for_magic_system.txt)
- [common/scripted_effects/anb_scripted_effects_for_magic_spells.txt](../../common/scripted_effects/anb_scripted_effects_for_magic_spells.txt)
- [common/scripted_effects/anb_scripted_effects_for_magic_project.txt](../../common/scripted_effects/anb_scripted_effects_for_magic_project.txt)
- [common/scripted_effects/anb_scripted_effects_magic_duel.txt](../../common/scripted_effects/anb_scripted_effects_magic_duel.txt)
- [events/Magic_System_Events.txt](../../events/Magic_System_Events.txt)
- [events/Magic_Study_Events.txt](../../events/Magic_Study_Events.txt)
- [events/Magic_Ruler_Events.txt](../../events/Magic_Ruler_Events.txt)
- [events/MagicDuel.txt](../../events/MagicDuel.txt)
- [decisions/MagicDecisions.txt](../../decisions/MagicDecisions.txt)
- [common/event_modifiers/anb_magic_modifiers.txt](../../common/event_modifiers/anb_magic_modifiers.txt)

Deep reference articles:

- [powerful-mage-and-succession-reference.md](./powerful-mage-and-succession-reference.md)
- [magic-projects-reference.md](./magic-projects-reference.md)

## Powerful Mage And Succession Family

This family is the cleanest reusable example of:

- powerful mage ruler, heir, and consort generation
- magical inheritance preservation
- delayed succession repair through `on_new_heir`
- government- and tag-specific mage-heir odds

Core anchors:

- [common/scripted_effects/anb_scripted_effects_for_magic_system.txt](../../common/scripted_effects/anb_scripted_effects_for_magic_system.txt)
- [events/Magic_System_Events.txt](../../events/Magic_System_Events.txt)
- [events/Magic_Ruler_Events.txt](../../events/Magic_Ruler_Events.txt)
- [common/on_actions/00_on_actions.txt](../../common/on_actions/00_on_actions.txt)
- [events/Theocracies.txt](../../events/Theocracies.txt)
- [events/RintaSeekerEvents.txt](../../events/RintaSeekerEvents.txt)

Deep reference article:

- [powerful-mage-and-succession-reference.md](./powerful-mage-and-succession-reference.md)

## Magic Projects Family

Magic projects are a reusable framework made from:

- a shared project-start helper
- project flags and variables
- a central dispatcher event
- per-project namespaces
- optional milestone branches
- cleanup helpers
- on-action progress trackers where needed

Core anchors:

- [common/scripted_effects/anb_scripted_effects_for_magic_system.txt](../../common/scripted_effects/anb_scripted_effects_for_magic_system.txt)
- [common/scripted_effects/anb_scripted_effects_for_magic_project.txt](../../common/scripted_effects/anb_scripted_effects_for_magic_project.txt)
- [events/Magic_System_Events.txt](../../events/Magic_System_Events.txt)
- [events/Magic_Project_Events.txt](../../events/Magic_Project_Events.txt)
- [common/custom_gui/magic_unique_projects.txt](../../common/custom_gui/magic_unique_projects.txt)
- [common/on_actions/00_on_actions.txt](../../common/on_actions/00_on_actions.txt)

Deep reference article:

- [magic-projects-reference.md](./magic-projects-reference.md)

## Racial System Family

The racial layer is another Anbennar-only system family that normal EU4 wiki articles will not explain.

It includes:

- racial population events by race
- racial tolerance and management logic
- racial administration switching
- racial military switching and unit tech changes
- custom racial GUI sorting and management buttons
- race-linked peace treaty options in some content areas

Core anchors:

- [events/RacialPopEvents.txt](../../events/RacialPopEvents.txt)
- [events/anb_racial_admin_mil.txt](../../events/anb_racial_admin_mil.txt)
- [events/anb_racial_pop_calculations.txt](../../events/anb_racial_pop_calculations.txt)
- [events/anb_RacialMiscEvents.txt](../../events/anb_RacialMiscEvents.txt)
- [common/custom_gui/customgui_racial_interface.txt](../../common/custom_gui/customgui_racial_interface.txt)
- [common/scripted_effects/anb_scripted_effects_for_racial_tolerances.txt](../../common/scripted_effects/anb_scripted_effects_for_racial_tolerances.txt)
- [common/scripted_triggers/anb_scripted_triggers_racial.txt](../../common/scripted_triggers/anb_scripted_triggers_racial.txt)
- [common/scripted_triggers/anb_scripted_triggers_racial_interface.txt](../../common/scripted_triggers/anb_scripted_triggers_racial_interface.txt)

Representative race-specific branches:

- [events/anb_racial_pop_events_elven.txt](../../events/anb_racial_pop_events_elven.txt)
- [events/anb_racial_pop_events_orcish.txt](../../events/anb_racial_pop_events_orcish.txt)
- [events/anb_racial_pop_events_harpy.txt](../../events/anb_racial_pop_events_harpy.txt)
- [events/anb_racial_pop_events_dwarven.txt](../../events/anb_racial_pop_events_dwarven.txt)

Deep reference article:

- [racial-population-and-military-reference.md](./racial-population-and-military-reference.md)

## Artificery Family

Artificery is not just "magic but science flavored."

It has its own estate, points system, inventions, research chain, and mixed-mode interaction with magic.

Core anchors:

- [events/ArtificeResearch.txt](../../events/ArtificeResearch.txt)
- [events/ArtificeInventions.txt](../../events/ArtificeInventions.txt)
- [events/estate_artificers.txt](../../events/estate_artificers.txt)
- [common/scripted_effects/artifice_scripted_effects.txt](../../common/scripted_effects/artifice_scripted_effects.txt)
- [common/scripted_triggers/anb_scripted_triggers_artifice.txt](../../common/scripted_triggers/anb_scripted_triggers_artifice.txt)
- [common/event_modifiers/artifice_modifiers.txt](../../common/event_modifiers/artifice_modifiers.txt)
- [common/estates/99_artificers.txt](../../common/estates/99_artificers.txt)
- [common/estate_privileges/estate_artifice_privileges.txt](../../common/estate_privileges/estate_artifice_privileges.txt)

Deep reference article:

- [artificery-research-and-inventions-reference.md](./artificery-research-and-inventions-reference.md)

## Adventurer Family

Anbennar has both generic adventurer content and more bespoke government and estate implementations.

Core anchors:

- [common/government_mechanics/anb_adventurer_unity.txt](../../common/government_mechanics/anb_adventurer_unity.txt)
- [events/estate_adventurers.txt](../../events/estate_adventurers.txt)
- [events/AdventurerSpawnables.txt](../../events/AdventurerSpawnables.txt)
- [events/adventurers.txt](../../events/adventurers.txt)
- [common/estates/98_adventurers.txt](../../common/estates/98_adventurers.txt)

Deep reference article:

- [adventurer-systems-and-estate-patterns-reference.md](./adventurer-systems-and-estate-patterns-reference.md)

## Custom Estate Layer

Anbennar has a much larger estate library than vanilla EU4 and many mechanics assume those estates exist.

Examples:

- [common/estates/97_mages.txt](../../common/estates/97_mages.txt)
- [common/estates/98_adventurers.txt](../../common/estates/98_adventurers.txt)
- [common/estates/99_artificers.txt](../../common/estates/99_artificers.txt)
- [common/estates/100_vampire.txt](../../common/estates/100_vampire.txt)
- [common/estate_privileges/estate_mages_privileges.txt](../../common/estate_privileges/estate_mages_privileges.txt)
- [common/estate_privileges/estate_artifice_privileges.txt](../../common/estate_privileges/estate_artifice_privileges.txt)

## Custom Government Mechanics Layer

There are currently many files in [common/government_mechanics](../../common/government_mechanics), including both vanilla carryovers and Anbennar-specific additions.

Representative Anbennar examples:

- [common/government_mechanics/anb_adventurer_unity.txt](../../common/government_mechanics/anb_adventurer_unity.txt)
- [common/government_mechanics/anb_allclan_pandemonium.txt](../../common/government_mechanics/anb_allclan_pandemonium.txt)
- [common/government_mechanics/anb_harpylen_queendom.txt](../../common/government_mechanics/anb_harpylen_queendom.txt)
- [common/government_mechanics/anb_rezankand_exemplar.txt](../../common/government_mechanics/anb_rezankand_exemplar.txt)

The common implementation pattern is:

- define a custom power in `common/government_mechanics`
- wire it into a GUI file under `interface/government_mechanics`
- use events, modifiers, missions, or decisions to manipulate it

## Custom GUI Layer

Many Anbennar-specific systems rely on `common/custom_gui` rather than only decisions or missions.

Current key files include:

- [common/custom_gui/magic_menu.txt](../../common/custom_gui/magic_menu.txt)
- [common/custom_gui/magic_spell_lists.txt](../../common/custom_gui/magic_spell_lists.txt)
- [common/custom_gui/magic_unique_projects.txt](../../common/custom_gui/magic_unique_projects.txt)
- [common/custom_gui/customgui_racial_interface.txt](../../common/custom_gui/customgui_racial_interface.txt)
- [common/custom_gui/provinceview.txt](../../common/custom_gui/provinceview.txt)
- [common/custom_gui/countrymilitaryview.txt](../../common/custom_gui/countrymilitaryview.txt)

This is one of the biggest differences from vanilla-style wiki expectations.

If a mechanic looks "missing" from decisions, missions, or events, check `common/custom_gui` and the matching `interface/*.gui` or `*.gfx` files before assuming it is hardcoded or absent.

## Reusable Modding Lessons

When adapting Anbennar systems for new content, start by asking:

1. Is there already a scripted effect that centralizes the state change?
2. Is there already a scripted trigger that gates legal usage?
3. Is the player entry point a decision, estate action, government interaction, or custom GUI button?
4. Is the system storing state in flags, modifiers, or variables rather than a dedicated mechanic object?
5. Does the same system already have nation-specific branches that can be copied instead of rewritten?

That is usually how you avoid reinventing the mechanic badly.

## Best Next Deep-Scan Targets

The strongest next documentation targets after this first pass are:

- Mage estate and magical politics as a standalone article
- Witch-king, lichdom, and magical infamy as a standalone article
- Government mechanics and custom GUI infrastructure as a standalone article
- Custom estate patterns beyond Adventurers and Artificers as a standalone article
- Artificery-magic crossover and nation-specific invention usage as a standalone article
