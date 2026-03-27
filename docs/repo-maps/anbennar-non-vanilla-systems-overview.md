# Anbennar Non-Vanilla Systems Overview

This article gives a repo-grounded overview of major Anbennar systems that are not well covered by the normal EU4 modding wiki.

It focuses on reusable implementation patterns rather than lore.

## Quick Verdict

Outside the magic layer, Anbennar still relies heavily on custom architecture.

The most important non-vanilla families are:

- racial population and military systems
- artificery
- adventurer systems
- expanded estates
- custom government mechanics
- custom GUI-backed subsystems

If a planned mechanic sounds too specific for vanilla EU4, there is a good chance Anbennar already solves something similar somewhere in one of those families.

## Shared Architecture Pattern

Across these systems, the repo repeatedly uses the same structure:

1. state is stored in flags, modifiers, and variables
2. scripted effects are used as the real implementation layer
3. events drive outcomes and pulses
4. custom GUI is used where vanilla interfaces are too limited
5. nation- or race-specific variants branch from the same shared helper layer

That is why repo scans matter so much here.

## 1. Racial Population and Military Systems

### What makes it non-vanilla

Vanilla EU4 does not have Anbennar's racial population management, tolerance, racial administration, or racial military switching system.

### Core files

| Area | File | What it does |
|---|---|---|
| Main race event namespace | [events/RacialPopEvents.txt](../../events/RacialPopEvents.txt) | Shared racial population event layer |
| Racial admin and military namespace | [events/anb_racial_admin_mil.txt](../../events/anb_racial_admin_mil.txt) | Administration and military switching logic |
| Population setup and calc | [events/anb_racial_pop_calculations.txt](../../events/anb_racial_pop_calculations.txt) | Setup and recalculation layer |
| Race misc | [events/anb_RacialMiscEvents.txt](../../events/anb_RacialMiscEvents.txt) | Miscellaneous support events |
| Race-specific population branches | [events/anb_racial_pop_events_elven.txt](../../events/anb_racial_pop_events_elven.txt) and related files | Per-race event variations |
| Tolerance and military helpers | [common/scripted_effects/anb_scripted_effects_for_racial_tolerances.txt](../../common/scripted_effects/anb_scripted_effects_for_racial_tolerances.txt) | Main scripted effect helper layer |
| Main triggers | [common/scripted_triggers/anb_scripted_triggers_racial.txt](../../common/scripted_triggers/anb_scripted_triggers_racial.txt) | Race and administration legality triggers |
| Custom UI | [common/custom_gui/customgui_racial_interface.txt](../../common/custom_gui/customgui_racial_interface.txt) | Race management window and sorting controls |

### Representative implementation pattern

The racial system does not just apply flavor modifiers.

It can change the country's military tech family through helper effects such as:

- [common/scripted_effects/anb_scripted_effects_for_racial_tolerances.txt:11](../../common/scripted_effects/anb_scripted_effects_for_racial_tolerances.txt#L11) `reset_racial_military_via_administration`

Representative excerpt:

```txt
if = {
	limit = { has_country_modifier = orcish_administration }
	add_country_modifier = {
		name = orcish_military
		duration = -1
		hidden = yes
	}
	...
	change_unit_type = tech_orcish
}
```

That means Anbennar can use race-linked administration as the trigger for unit-tech swaps and broader military identity.

### UI pattern

The racial interface uses custom GUI windows and button sorting, for example:

- [common/custom_gui/customgui_racial_interface.txt](../../common/custom_gui/customgui_racial_interface.txt)

Representative pattern:

```txt
custom_button = {
	name = racial_pop_menu_open_button
	effect = {
		clr_country_flag = racial_military_menu_opened
		set_country_flag = racial_pop_menu_opened
	}
}
```

This is another example of the Anbennar window-state-via-country-flags approach.

### Reuse lesson

If you need a system that:

- tracks multiple demographic groups
- changes admin or military identity
- exposes a sortable management UI

then the racial framework is one of the best places to look.

## 2. Artificery

### What makes it non-vanilla

Artificery is a large custom layer for magical industry, inventions, and research progression.

It is not a normal vanilla estate-only mechanic.

### Core files

| Area | File | What it does |
|---|---|---|
| Research namespace | [events/ArtificeResearch.txt](../../events/ArtificeResearch.txt) | Research progression |
| Inventions namespace | [events/ArtificeInventions.txt](../../events/ArtificeInventions.txt) | Invention outcomes and follow-up |
| Estate namespace | [events/estate_artificers.txt](../../events/estate_artificers.txt) | Estate-facing artificer events |
| Scripted effects | [common/scripted_effects/artifice_scripted_effects.txt](../../common/scripted_effects/artifice_scripted_effects.txt) | Core point and capacity helpers |
| Scripted triggers | [common/scripted_triggers/anb_scripted_triggers_artifice.txt](../../common/scripted_triggers/anb_scripted_triggers_artifice.txt) | Artificery legality and thresholds |
| Estate definition | [common/estates/99_artificers.txt](../../common/estates/99_artificers.txt) | Custom artificers estate |
| Privileges | [common/estate_privileges/estate_artifice_privileges.txt](../../common/estate_privileges/estate_artifice_privileges.txt) | Artificery privileges |

### Representative implementation pattern

The helper file includes its own mini checklist in the comments:

- [common/scripted_effects/artifice_scripted_effects.txt](../../common/scripted_effects/artifice_scripted_effects.txt)

That comment is useful because it explicitly names the cross-file update path needed when adding inventions.

The main points updater starts at:

- [common/scripted_effects/artifice_scripted_effects.txt:21](../../common/scripted_effects/artifice_scripted_effects.txt#L21)

Representative excerpt:

```txt
update_artifice_points = {
	if = {
		limit = {
			OR = {
				has_country_flag = magic_artificery_mixed
				has_country_flag = magic_artificery_artificery_only
			}
		}
		hidden_effect = {
			set_variable = { which = MaxArtificePoints value = 0 }
			...
			change_variable = {
				which = MaxArtificePoints
				which = ResearchArtificePoints
			}
		}
	}
}
```

Important takeaways:

- artificery uses a variable-driven capacity model
- it already has explicit mixed-mode and artificery-only flags
- trade goods such as precursor relics and damestear feed the system directly

### Reuse lesson

If you need a system based on:

- research capacity
- invention slots
- resource-sensitive progression
- magic-versus-tech branching

then artificery is one of the best existing anchors.

## 3. Adventurer Systems

### What makes it non-vanilla

Anbennar treats adventurers as both:

- an estate or political group
- a government mechanic in some tags
- a content family with special spawning and event behavior

### Core files

| Area | File | What it does |
|---|---|---|
| Government mechanic | [common/government_mechanics/anb_adventurer_unity.txt](../../common/government_mechanics/anb_adventurer_unity.txt) | Defines custom adventurer unity power |
| Estate events | [events/estate_adventurers.txt](../../events/estate_adventurers.txt) | Adventurer estate interactions |
| Spawnables | [events/AdventurerSpawnables.txt](../../events/AdventurerSpawnables.txt) | Adventurer spawning content |
| Estate definition | [common/estates/98_adventurers.txt](../../common/estates/98_adventurers.txt) | Adventurers estate |

### Representative implementation pattern

The government mechanic itself starts at:

- [common/government_mechanics/anb_adventurer_unity.txt:1](../../common/government_mechanics/anb_adventurer_unity.txt#L1)

Representative excerpt:

```txt
anb_adventurer_unity = {
	powers = {
		adventurer_unity = {
			max = 100
			reset_on_new_ruler = no
			...
		}
	}
}
```

And it includes an interaction that spends MIL to raise unity.

That is useful because it shows how Anbennar sometimes builds a bespoke government meter when vanilla reform or estate tools are not enough.

### Reuse lesson

If you want a campaign momentum or state coherence mechanic that is not tied to mana or reform progress, the adventurer unity model is worth studying.

## 4. Expanded Estate Layer

### What makes it non-vanilla

Anbennar adds many new estates and estate families beyond vanilla.

Especially important custom estates:

- [common/estates/97_mages.txt](../../common/estates/97_mages.txt)
- [common/estates/98_adventurers.txt](../../common/estates/98_adventurers.txt)
- [common/estates/99_artificers.txt](../../common/estates/99_artificers.txt)
- [common/estates/100_vampire.txt](../../common/estates/100_vampire.txt)
- multiple command, caste, and regional estate files

Relevant privilege layer examples:

- [common/estate_privileges/estate_mages_privileges.txt](../../common/estate_privileges/estate_mages_privileges.txt)
- [common/estate_privileges/estate_artifice_privileges.txt](../../common/estate_privileges/estate_artifice_privileges.txt)
- [common/estate_privileges/estate_shirgrii_privileges.txt](../../common/estate_privileges/estate_shirgrii_privileges.txt)
- [common/estate_privileges/estate_vampires_privileges.txt](../../common/estate_privileges/estate_vampires_privileges.txt)

### Reuse lesson

If a mechanic sounds like it should belong to a political group rather than a permanent national modifier, check whether an existing custom estate already models that fantasy.

## 5. Custom Government Mechanics

### What makes it non-vanilla

Anbennar contains a large library of special government mechanics under:

- [common/government_mechanics](../../common/government_mechanics)

Representative custom files include:

- [common/government_mechanics/anb_adventurer_unity.txt](../../common/government_mechanics/anb_adventurer_unity.txt)
- [common/government_mechanics/anb_allclan_pandemonium.txt](../../common/government_mechanics/anb_allclan_pandemonium.txt)
- [common/government_mechanics/anb_harpylen_queendom.txt](../../common/government_mechanics/anb_harpylen_queendom.txt)
- [common/government_mechanics/anb_rezankand_exemplar.txt](../../common/government_mechanics/anb_rezankand_exemplar.txt)

### Reuse lesson

If a system is meant to be:

- tag-defining
- persistent
- visible in the government screen

then a government mechanic may be a better home than a mission reward chain or estate privilege pile.

## 6. Custom GUI as a First-Class Tool

### What makes it non-vanilla

Anbennar uses `common/custom_gui` far more aggressively than a normal vanilla-like submod.

Current standout files include:

- [common/custom_gui/magic_menu.txt](../../common/custom_gui/magic_menu.txt)
- [common/custom_gui/magic_spell_lists.txt](../../common/custom_gui/magic_spell_lists.txt)
- [common/custom_gui/magic_unique_projects.txt](../../common/custom_gui/magic_unique_projects.txt)
- [common/custom_gui/customgui_racial_interface.txt](../../common/custom_gui/customgui_racial_interface.txt)
- [common/custom_gui/provinceview.txt](../../common/custom_gui/provinceview.txt)
- [common/custom_gui/countrymilitaryview.txt](../../common/custom_gui/countrymilitaryview.txt)

### Reuse lesson

Before assuming a mechanic must be a decision, check whether Anbennar already exposes something similar as:

- a custom province button
- a custom country panel button
- a custom menu window

## 7. Special Content Layers

The repo also contains other special content families worth keeping in mind:

- [common/new_diplomatic_actions](../../common/new_diplomatic_actions)
- [common/peace_treaties](../../common/peace_treaties)
- [common/rebel_types](../../common/rebel_types)
- [common/units](../../common/units)

Examples already seen in this scan:

- `zz_magic_duel.txt` in diplomatic actions
- race-specific peace options
- magical abomination rebels
- special magic battlemage units

These are important because they show how Anbennar sometimes extends the rules of interaction, not just the flavor text.

## Best Reuse Candidates For Future Verne Work

The strongest non-magic reuse targets for a future Verne overhaul are:

- racial UI and sorting patterns if you need a state-management screen
- artificery capacity logic if you need research-slot or invention-slot style progression
- adventurer unity if you need a national momentum meter
- expanded estate structures if you want systems expressed as institutions instead of flat modifiers
- custom GUI button patterns if you want a feature to live in province or country view instead of decisions

## Best Next Articles To Add

The next high-value docs after this overview are:

- racial population and military system reference
- artificery research and inventions reference
- adventurer unity and adventurer estate reference
- custom government mechanics index
