# Anbennar Magic Systems Reference

This article documents the main Anbennar magic systems as they are implemented in the repository.

It is a repo-grounding reference article, not a redesign.

## Quick Verdict

Anbennar magic is not one mechanic.

It is a full system family built from:

- custom GUI windows and buttons
- scripted triggers for legal access
- scripted effects that centralize magic state changes
- country flags, ruler flags, ruler modifiers, country modifiers, and variables
- study and maintenance events
- ruler and heir generation hooks
- unique projects
- war wizard conversion
- witch-king and lich content
- duel logic
- race-aware and artificery-aware branches

This is exactly the kind of content the normal EU4 wiki does not cover well, because the implementation is mostly Anbennar-side structure and conventions rather than vanilla engine syntax alone.

## Core Files

| Area | File | What it does |
|---|---|---|
| Access and school triggers | [common/scripted_triggers/anb_scripted_triggers_magic.txt](../../common/scripted_triggers/anb_scripted_triggers_magic.txt) | Defines `can_use_magic`, banned-magic checks, and school-level triggers. |
| Menu state, mana, XP, and helper math | [common/scripted_effects/anb_scripted_effects_for_magic_system.txt](../../common/scripted_effects/anb_scripted_effects_for_magic_system.txt) | Central helper file for UI flags, mana changes, XP calculations, and study previews. |
| Patrons and other spell-side helpers | [common/scripted_effects/anb_scripted_effects_for_magic_spells.txt](../../common/scripted_effects/anb_scripted_effects_for_magic_spells.txt) | Handles patron setup, save/restore, and patron approval state. |
| Unique project effects | [common/scripted_effects/anb_scripted_effects_for_magic_project.txt](../../common/scripted_effects/anb_scripted_effects_for_magic_project.txt) | Project progression helpers and project outcome logic. |
| Duel stat setup | [common/scripted_effects/anb_scripted_effects_magic_duel.txt](../../common/scripted_effects/anb_scripted_effects_magic_duel.txt) | Initializes duel stats with race, age, and school-aware logic. |
| Main magic UI | [common/custom_gui/magic_menu.txt](../../common/custom_gui/magic_menu.txt) | Defines main windows, state flags, and button behavior for the magic interface. |
| Custom spell lists | [common/custom_gui/magic_spell_lists.txt](../../common/custom_gui/magic_spell_lists.txt) | Template and examples for tag/race/custom spellbook branches. |
| Unique projects UI | [common/custom_gui/magic_unique_projects.txt](../../common/custom_gui/magic_unique_projects.txt) | Template and real windows for regional and tag-specific projects. |
| Decision entry points | [decisions/MagicDecisions.txt](../../decisions/MagicDecisions.txt) | War wizard, patron, theatre, recruit mage, lichdom, and estate-linked decisions. |
| System events | [events/Magic_System_Events.txt](../../events/Magic_System_Events.txt) | Hidden handlers, UI refreshes, war wizard confirmation, automatic powerful mage logic. |
| Study events | [events/Magic_Study_Events.txt](../../events/Magic_Study_Events.txt) | Study progress pulses, aid events, resource events, and dangerous research branches. |
| Ruler magic events | [events/Magic_Ruler_Events.txt](../../events/Magic_Ruler_Events.txt) | Powerful mage heirs, bastard heir swaps, and succession-side magic events. |
| Duel events | [events/MagicDuel.txt](../../events/MagicDuel.txt) | Full duel minigame flow. |
| Diplomatic duel hook | [common/new_diplomatic_actions/zz_magic_duel.txt](../../common/new_diplomatic_actions/zz_magic_duel.txt) | Contains the dormant diplomatic-action pattern for magic duels. |
| Modifiers | [common/event_modifiers/anb_magic_modifiers.txt](../../common/event_modifiers/anb_magic_modifiers.txt) | Mana, infrastructure, mage estate, war wizard, witch-king, and related magic modifiers. |
| Mage estate content | [events/estate_mages.txt](../../events/estate_mages.txt) | Estate events that push magic politics and interact with magical systems. |
| Magic localisation | [localisation/anb_magic_system_l_english.yml](../../localisation/anb_magic_system_l_english.yml) | System labels, schools, levels, menu text, and many trigger names. |
| Ruler-side magic localisation | [localisation/anb_magic_ruler_l_english.yml](../../localisation/anb_magic_ruler_l_english.yml) | Powerful mage, war wizard, witch-king, and heir/ruler loc. |

## Main Implementation Model

At a high level, the magic layer works like this:

1. a country must have access to magic
2. access is checked through scripted triggers
3. the player opens or interacts with custom GUI windows
4. the GUI sets and clears country flags to show different windows
5. helper effects calculate variables for tooltips and resource bars
6. studying, projects, rulers, heirs, spells, and patrons are all represented through flags, modifiers, and variables
7. decisions and events hook into the same helper layer instead of duplicating logic inline

This is a classic Anbennar helper-layer architecture.

## 1. Access Gate

The first major access trigger is:

- [common/scripted_triggers/anb_scripted_triggers_magic.txt:5](../../common/scripted_triggers/anb_scripted_triggers_magic.txt#L5)

```txt
can_use_magic = {
	custom_trigger_tooltip = {
		tooltip = can_use_magic
		NOT = { has_country_flag = J84_no_casting_spells_flag }
		OR = {
			AND = {
				has_magic_estate_or_equiv = yes
				NOT = { has_country_modifier = mages_strike }
			}
			has_ruler_flag = zokka_phoenix_flag
			AND = {
				ruler_is_powerful_mage = yes
				NOT = { has_country_flag = magic_artificery_artificery_only }
			}
		}
	}
}
```

Important points:

- magic access is not hardcoded to one source
- estate magic and ruler magic are both valid access routes
- the system already has explicit magic-versus-artificery compatibility rules
- special-case tags and flags exist inside the access layer

Related trigger:

- [common/scripted_triggers/anb_scripted_triggers_magic.txt:23](../../common/scripted_triggers/anb_scripted_triggers_magic.txt#L23) defines `has_magic_estate_or_equiv`

That trigger allows non-standard branches such as:

- countries with the Mages estate
- Azjakuma
- Command artificery privilege exceptions

## 2. Data Model: Flags, Modifiers, and Variables

The most important design note in the whole magic system is written directly into the helper file:

- [common/scripted_effects/anb_scripted_effects_for_magic_system.txt](../../common/scripted_effects/anb_scripted_effects_for_magic_system.txt)

The comments explain:

- ruler flags and country flags are separate
- ruler modifiers and country modifiers are not cleanly separate in the same way
- a ruler modifier is really a country modifier cleared on ruler death

Practical takeaway:

- use flags to distinguish ruler versus country school state
- be careful reusing the same modifier names across ruler and country layers
- do not assume vanilla-looking scope behavior without checking how Anbennar's helpers already use it

## 3. School Levels

Each school has multiple trigger families in:

- [common/scripted_triggers/anb_scripted_triggers_magic.txt](../../common/scripted_triggers/anb_scripted_triggers_magic.txt)

Examples:

- `is_overall_abjuration_level_0`
- `is_overall_abjuration_level_1`
- `is_overall_abjuration_level_2_minimum`
- `is_overall_abjuration_level_3`

This pattern is repeated for all eight schools:

- Abjuration
- Conjuration
- Divination
- Enchantment
- Evocation
- Illusion
- Necromancy
- Transmutation

The localisation file makes clear that the levels are treated as:

- Novice
- Proficient
- Renowned
- Legendary

See:

- [localisation/anb_magic_system_l_english.yml](../../localisation/anb_magic_system_l_english.yml)

## 4. Menu State and Custom GUI

The custom magic menu is driven by country flags.

Examples from:

- [common/custom_gui/magic_menu.txt](../../common/custom_gui/magic_menu.txt)

Main window flags:

- `magic_menu_main_flag`
- `magic_menu_advancement_flag`
- `magic_menu_spellbook_flag`
- `magic_menu_patron_flag`
- `magic_menu_study_flag`

The main custom windows are declared around:

- [common/custom_gui/magic_menu.txt:194](../../common/custom_gui/magic_menu.txt#L194)

The UI open button name appears at:

- [common/custom_gui/magic_menu.txt:46](../../common/custom_gui/magic_menu.txt#L46)
- [common/custom_gui/magic_menu.txt:322](../../common/custom_gui/magic_menu.txt#L322)

This means the visible menu is not a normal decision category or province interaction.

It is a custom GUI state machine controlled by country flags and hidden update events.

## 5. The UI Refresh Pattern

The UI refresh helper is:

- [common/scripted_effects/anb_scripted_effects_for_magic_system.txt](../../common/scripted_effects/anb_scripted_effects_for_magic_system.txt)

```txt
update_magic_menu_effect = {
	hidden_effect = { country_event = { id = magic_system.1 } }
}
```

And the matching event is:

- [events/Magic_System_Events.txt:9](../../events/Magic_System_Events.txt#L9)

```txt
country_event = {
	id = magic_system.1
	hidden = yes
	immediate = {
		update_magic_ui_experience_modifiers = yes
		update_mana_regen_vars = yes
		generic_calc_spell_levels = { type = ruler }
		generic_calc_spell_levels = { type = heir }
		generic_calc_spell_levels = { type = country }
		update_spell_tooltips = yes
	}
}
```

This is a strong pattern to copy:

- custom GUI button or state change
- one hidden maintenance event
- that event recomputes display variables

## 6. Mana and Experience

Mana is explicitly centralized in the helper layer.

Important warning:

- [common/scripted_effects/anb_scripted_effects_for_magic_system.txt:259](../../common/scripted_effects/anb_scripted_effects_for_magic_system.txt#L259)

```txt
change_mana = {
	[[amount] change_variable = { currentMana = $amount$ } ]
```

The file comment says there should be no direct mana editing outside this path.

That is a useful modification rule:

- if you are adding spell effects or nation-specific magic content, use the centralized mana helpers
- do not directly mutate `currentMana` unless you are intentionally stepping outside the system

Experience is similarly surfaced through the hidden UI events:

- [events/Magic_System_Events.txt:34](../../events/Magic_System_Events.txt#L34) for `magic_system.2`

That event:

- exports modifier values into variables
- combines school and source modifiers
- computes `last_months_xp_gain`
- computes `months_till_advancement_done`
- updates decimal display variables for localisation

## 7. Study Progress System

Study progress is handled by:

- [events/Magic_Study_Events.txt:1](../../events/Magic_Study_Events.txt#L1)

The handler event is:

- [events/Magic_Study_Events.txt:3](../../events/Magic_Study_Events.txt#L3) for `magic_study.0`

It acts as a progress pulse that:

- checks whether the cooldown modifier is absent
- sets advancement-specific flags
- fires one of many possible study subevents
- reapplies a randomized cooldown modifier

Study help sources documented directly in the event options include:

- Mage estate aid
- Court mage aid
- Library research
- Ancient tome
- Ancient relic
- Precursor knowledge
- Magisterium assistance
- Mana-fueled practice
- Unregulated research
- Unsafe experiments

This is a very flexible event-driven study framework, and it is a strong candidate for adaptation if you want disciplined magical progression instead of one-off event boosts.

## 8. Custom Spell Lists

Custom spell lists are documented like a mini developer framework in:

- [common/custom_gui/magic_spell_lists.txt](../../common/custom_gui/magic_spell_lists.txt)

The file itself explains how to add a custom list:

1. define a `custom_window`
2. copy a spell list template
3. wire each slot to `magical_tradition_spell_trigger`
4. cast via `magical_tradition_cast_spell`
5. run group cleanup or follow-up through `magical_tradition_on_spell_cast_effect`

The file already includes reusable examples:

- template default list
- tag-specific example list
- harpy list
- bulwar list

Key anchors:

- [common/custom_gui/magic_spell_lists.txt:123](../../common/custom_gui/magic_spell_lists.txt#L123) custom spell list selector button
- [common/custom_gui/magic_spell_lists.txt:177](../../common/custom_gui/magic_spell_lists.txt#L177) `magic_list_harpy_default`
- [common/custom_gui/magic_spell_lists.txt:189](../../common/custom_gui/magic_spell_lists.txt#L189) `magic_list_bulwar_default`

Representative button pattern:

```txt
custom_button = {
	name = magic_list_harpy_2_button_default
	trigger = {
		magical_tradition_spell_trigger = { group = harpy subgroup = default slot = 2 player = yes }
	}
	effect = {
		magical_tradition_cast_spell = { school = evocation level = 2 id = harpy_default_2 war = yes }
		magical_tradition_on_spell_cast_effect = { group = harpy }
	}
}
```

This is one of the most reusable Anbennar patterns in the repo if you want a nation-, race-, or doctrine-specific spellbook.

## 9. Patrons

Patrons are handled in:

- [common/scripted_effects/anb_scripted_effects_for_magic_spells.txt:1](../../common/scripted_effects/anb_scripted_effects_for_magic_spells.txt#L1)

Main helper:

```txt
set_magic_patron = {
	set_ruler_flag = $name_key$_patron
	hidden_effect = {
		set_$name_key$_patron_schools = yes
		[[initial_approval] set_variable = { PatronApproval = $initial_approval$ } ]
	}
}
```

The same file also defines:

- school bias setup for many patrons
- `clr_magic_patron`
- `change_patron_approval`
- `save_patron`
- `restore_patron`

Important implementation insight:

- patron choice is not just flavor text
- it is saved and restored across ruler persistence logic
- it uses a mix of ruler flags, saved country flags, variables, and school-favor modifiers

That makes it another good adaptation source for bonded magical affiliation systems.

## 10. Unique Magical Projects

The project UI template lives in:

- [common/custom_gui/magic_unique_projects.txt](../../common/custom_gui/magic_unique_projects.txt)

The helper logic lives in:

- [common/scripted_effects/anb_scripted_effects_for_magic_project.txt](../../common/scripted_effects/anb_scripted_effects_for_magic_project.txt)

The project UI file shows the generic pattern:

- a window per regional or tag-specific project set
- one button per project
- one progress bar per project
- school icons when relevant
- `can_upgrade_project` to gate the button
- `start_magic_project` as the normal button effect

The project helper file shows more advanced patterns such as:

- temporary or permanent bypass flags for magical infrastructure
- setback handling and bonus recovery
- project-specific variables
- project-specific cross-event branching
- project-specific sanity or consequence trackers
- transformation effects like lichdom

Example project-side effect:

```txt
theatre_of_simulacra_add_bonus = {
	if = {
		limit = {
			check_variable = {
				which = theatre_of_simulacra_bonuses
				which = theatre_of_simulacra_level
			}
		}
		custom_tooltip = no_theatre_of_simulacra_has_space_tt
	}
	else = {
		change_variable = { which = theatre_of_simulacra_bonuses value = 1 }
		add_country_modifier = { name = theatre_$bonus$_bonus duration = -1 hidden = yes }
		set_country_flag = new_theatre_bonus
	}
}
```

## 11. Project Effects Can Spill Into Unrelated Files

One of the most important implementation lessons is that high-level magic projects can modify behavior far outside the magic files themselves.

The strongest example is `orb_of_omniscience`.

Search results show checks for it in:

- [events/Dynastic.txt](../../events/Dynastic.txt)
- [events/estate_mages.txt](../../events/estate_mages.txt)
- [events/estate_burghers.txt](../../events/estate_burghers.txt)
- [events/estate_nobles.txt](../../events/estate_nobles.txt)
- many other estate and event files

Representative anchors:

- [events/Dynastic.txt:149](../../events/Dynastic.txt#L149)
- [events/Dynastic.txt:256](../../events/Dynastic.txt#L256)
- [events/estate_mages.txt:493](../../events/estate_mages.txt#L493)
- [events/estate_burghers.txt:701](../../events/estate_burghers.txt#L701)
- [events/estate_nobles.txt:401](../../events/estate_nobles.txt#L401)

This means some projects act as cross-cutting event prevention or event avoidance systems, not just local bonuses.

## 12. Powerful Mage Generation

Powerful mage generation is handled by both hidden helper events and ordinary MTTH ruler events.

System-side helper events:

- [events/Magic_System_Events.txt:144](../../events/Magic_System_Events.txt#L144) `magic_system.10`
- [events/Magic_System_Events.txt:161](../../events/Magic_System_Events.txt#L161) `magic_system.11`
- [events/Magic_System_Events.txt:178](../../events/Magic_System_Events.txt#L178) `magic_system.12`

These events call `define_powerful_mage` for:

- ruler
- heir
- consort

Meanwhile [events/Magic_Ruler_Events.txt](../../events/Magic_Ruler_Events.txt) contains the broader powerful-mage bloodline, succession, and emergence content.

Representative entries:

- [events/Magic_Ruler_Events.txt:9](../../events/Magic_Ruler_Events.txt#L9) `magic_ruler.103` Powerful Mage Heir
- [events/Magic_Ruler_Events.txt:80](../../events/Magic_Ruler_Events.txt#L80) `magic_ruler.104` Powerful Mage Bastard Child
- [events/Magic_Ruler_Events.txt:173](../../events/Magic_Ruler_Events.txt#L173) `magic_ruler.105` Young Heir is Magically Gifted

Important implementation pattern:

- the file uses `define_heir = { dynasty = ROOT ... }`
- then applies `define_powerful_mage = { type = heir }`

That is highly relevant to future Verne work because it shows Anbennar already using same-dynasty heir shaping plus magic shaping in event form.

## 13. War Wizard Entry Points

Key decisions:

- [decisions/MagicDecisions.txt:114](../../decisions/MagicDecisions.txt#L114) `make_ruler_war_wizard`
- [decisions/MagicDecisions.txt:172](../../decisions/MagicDecisions.txt#L172) `make_heir_war_wizard`
- [decisions/MagicDecisions.txt:457](../../decisions/MagicDecisions.txt#L457) `estate_mages_recruit_war_wizard_decision`

The pattern is:

- check that the character is already a powerful mage
- check general-leader legality
- check special attribute bans and edge cases
- set a temporary country flag
- call a confirmation event
- let the event invoke the real definition helper

Confirmation events:

- [events/Magic_System_Events.txt:195](../../events/Magic_System_Events.txt#L195) `magic_system.13`
- [events/Magic_System_Events.txt:239](../../events/Magic_System_Events.txt#L239) `magic_system.14`

This is a good example of Anbennar wrapping risky actions in confirmation events instead of making the decision effect do everything at once.

## 14. Witch-King Layer

The witch-king content sits across modifiers, ruler events, and other content.

Relevant modifier section:

- [common/event_modifiers/anb_magic_modifiers.txt](../../common/event_modifiers/anb_magic_modifiers.txt)

The localization anchors are especially useful for understanding the intended branches:

- [localisation/anb_magic_ruler_l_english.yml:167](../../localisation/anb_magic_ruler_l_english.yml#L167) `magic_ruler.66`
- [localisation/anb_magic_ruler_l_english.yml:173](../../localisation/anb_magic_ruler_l_english.yml#L173) `magic_ruler.67`
- [localisation/anb_magic_ruler_l_english.yml:177](../../localisation/anb_magic_ruler_l_english.yml#L177) `magic_ruler.68`
- [localisation/anb_magic_ruler_l_english.yml:204](../../localisation/anb_magic_ruler_l_english.yml#L204) `magic_ruler.77`

The witch-king framework is not just one flag.

It includes:

- reputation states
- branch modifiers
- death and reform outcomes
- imperial incident tie-ins
- infamy and pariah-state consequences

## 15. Lichdom

Key decision:

- [decisions/MagicDecisions.txt:557](../../decisions/MagicDecisions.txt#L557) `pursue_lichdom`

The actual transformation-side helper is in:

- [common/scripted_effects/anb_scripted_effects_for_magic_project.txt](../../common/scripted_effects/anb_scripted_effects_for_magic_project.txt)

`become_a_lich_effect` does much more than add one modifier.

It:

- sets `long_lived_ruler`
- sets `ruled_by_lich`
- applies ruler modifiers
- saves personalities
- saves ruler stats
- saves spell levels
- saves dynasty
- saves patron
- switches the country to magic-only mode through an artifice/magic compatibility helper
- chains into follow-up events

This is a very strong example of how Anbennar handles high-impact character transformations:

- save all critical character state first
- then apply the transformation
- then support revival or persistence logic later

## 16. Magic Duel System

The duel initialization helper is:

- [common/scripted_effects/anb_scripted_effects_magic_duel.txt:1](../../common/scripted_effects/anb_scripted_effects_magic_duel.txt#L1)

It initializes:

- HP
- Mana
- Power
- Shield
- Accuracy
- Evasion
- Resistance
- Damage over time
- Healing over time

The big surprise is that it also directly adjusts those values by:

- ruler ADM, DIP, and MIL
- ruler race
- ruler age
- ruler school flags

That makes the duel system a good example of a race-aware and character-aware subgame.

The duel event chain begins at:

- [events/MagicDuel.txt:27](../../events/MagicDuel.txt#L27) `magic_duel.0`
- [events/MagicDuel.txt:77](../../events/MagicDuel.txt#L77) `magic_duel.1`

The file comments also document the duel balance model directly:

- mana-to-damage value assumptions
- school efficiency differences
- spell-rank efficiency bonuses

That is unusually explicit for a gameplay file and makes this one of the better reference systems in the repo.

There is also a dormant or example-style diplomatic action file at:

- [common/new_diplomatic_actions/zz_magic_duel.txt](../../common/new_diplomatic_actions/zz_magic_duel.txt)

Even though it is commented out, it is useful as a pattern for how a duel could be exposed through diplomacy.

## 17. Race-Aware and Artifice-Aware Magic Branches

Two especially important cross-links:

1. magic access can be blocked by artificery-only mode
2. duel stats change by race

The race side is visible in:

- [common/scripted_effects/anb_scripted_effects_magic_duel.txt](../../common/scripted_effects/anb_scripted_effects_magic_duel.txt)

The artifice side is visible in:

- [common/scripted_triggers/anb_scripted_triggers_magic.txt](../../common/scripted_triggers/anb_scripted_triggers_magic.txt)
- [common/event_modifiers/anb_magic_modifiers.txt](../../common/event_modifiers/anb_magic_modifiers.txt)
- [common/scripted_effects/anb_scripted_effects_for_magic_project.txt](../../common/scripted_effects/anb_scripted_effects_for_magic_project.txt)

This matters because it means Anbennar already has patterns for:

- magic only
- artificery only
- mixed compromise

That is useful if a future system needs to prefer one branch without deleting the other.

## 18. How To Modify This Safely

If you want to adapt or extend Anbennar magic, the safest route is usually:

1. copy an existing trigger family instead of inventing a new access model
2. route new state changes through the helper effects
3. reuse existing country and ruler flag conventions
4. attach new decisions or UI buttons to hidden confirmation or update events
5. inspect localisation because it often reveals design intent and hidden branches
6. search for cross-file project or flag usage before changing a local magic feature

## Best Reuse Targets For Future Verne Work

The strongest existing patterns to borrow from are:

- Powerful mage heir generation in [events/Magic_Ruler_Events.txt](../../events/Magic_Ruler_Events.txt)
- War wizard conversion in [decisions/MagicDecisions.txt](../../decisions/MagicDecisions.txt) plus [events/Magic_System_Events.txt](../../events/Magic_System_Events.txt)
- Custom spell list framework in [common/custom_gui/magic_spell_lists.txt](../../common/custom_gui/magic_spell_lists.txt)
- Cross-cutting project logic in [common/scripted_effects/anb_scripted_effects_for_magic_project.txt](../../common/scripted_effects/anb_scripted_effects_for_magic_project.txt)
- Patron save and restore in [common/scripted_effects/anb_scripted_effects_for_magic_spells.txt](../../common/scripted_effects/anb_scripted_effects_for_magic_spells.txt)

## Next Magic Docs To Add Later

The next best standalone reference articles would be:

- Powerful Mage and succession handling
- Magic projects and project spillover patterns
- Mage estate integration
- War wizard generation patterns
- Witch-king escalation and containment paths
