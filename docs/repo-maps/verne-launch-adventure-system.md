# Verne Launch Adventure System

This article documents the existing `verne_launch_adventure` system as implemented in the Anbennar repo.

It covers the decision-driven expedition framework, not the Port of Adventure button itself.

Related articles:

- [port-of-adventure-system.md](./port-of-adventure-system.md)
- [network-of-adventure-system.md](./network-of-adventure-system.md)

## Overview

`verne_launch_adventure` is a major Verne decision that dispatches bespoke overseas expedition event chains.

It is not a simple one-click reward button.

The live system combines:

- mission and event unlock flags
- a shared expedition-eligibility trigger
- one major decision
- region-specific target provinces
- one event chain per target
- branch-state flags inside each chain
- a country-wide mutex flag to stop multiple simultaneous expeditions
- a scripted cancel helper
- a shared "adventures completed" progression counter

## Core Files

| Area | File | What it does |
|---|---|---|
| Decision entry point | [decisions/VerneDecisions.txt](../../decisions/VerneDecisions.txt) | Defines `verne_launch_adventure` and dispatches the initial adventure events. |
| Shared expedition trigger | [common/scripted_triggers/anb_scripted_triggers_missions.txt](../../common/scripted_triggers/anb_scripted_triggers_missions.txt) | Defines `verne_can_send_expedition`. |
| Shared cancel helper | [common/scripted_effects/anb_scripted_effects_for_verne.txt](../../common/scripted_effects/anb_scripted_effects_for_verne.txt) | Defines `verne_cancel_expedition`. |
| Adventure event chains | [events/Flavour_Verne_A33.txt](../../events/Flavour_Verne_A33.txt) | Contains the actual expedition stories and rewards. |
| Unlock missions | [missions/Verne_Missions.txt](../../missions/Verne_Missions.txt) | Unlocks the adventure system and region families. |
| Decision loc and tooltips | [localisation/Flavour_Verne_A33_l_english.yml](../../localisation/Flavour_Verne_A33_l_english.yml) | Provides the decision title, description, and expedition tooltip text. |

## Main Objects

| Object | Type | Purpose |
|---|---|---|
| `verne_launch_adventure` | decision | Main player-facing expedition launcher |
| `verne_can_send_expedition` | scripted trigger | Checks whether the expedition can be sent from a target province |
| `verne_cancel_expedition` | scripted effect | Cancels an expedition cleanly without paying the troop-removal penalty |
| `verne_ongoing_adventure` | country flag | Prevents more than one live adventure chain at a time |
| `verne_unlocked_adventure_system` | country flag | Unlocks the decision itself |
| `verne_*_adventures_unlocked` | country flags | Unlock region families |
| `verne_*_adventure_completed` | country flags | Mark finished expedition chains |
| `verne_number_of_adventures_completed` | variable | Progress counter reused by missions and other Verne rewards |

## Region Families

The decision is split into four regional unlock families.

| Family | Unlock flag | Provinces | First event IDs | Completion flags |
|---|---|---|---|---|
| Akasi/Bulwari | `verne_akasi_bulwari_adventures_unlocked` | `383`, `555`, `6103` | `1009`, `1017`, `1013` | `verne_aur_kes_adventure_completed`, `verne_damerian_umbar_adventure_completed`, `verne_genie_palace_adventure_completed` |
| Taychendi/Kheionai | `verne_taychendi_kheionai_adventures_unlocked` | `2388`, `2495`, `2520`, `2745` | `1045`, `1049`, `1053`, `1057` | `verne_amadia_pearl_hunt_adventure_completed`, `verne_nanru_nakar_adventure_completed`, `verne_blue_house_adventure_completed`, `verne_lokemeion_adventure_completed` |
| Halessi | `verne_halessi_adventures_unlocked` | `4765`, `4955` | `1037`, `1041` | `verne_tlagapatung_adventure_completed`, `verne_chien_binhrung_adventure_completed` |
| Sarhal | `verne_sarhali_adventures_unlocked` | `5776`, `5863`, `6599`, `6584` | `1025`, `1021`, `1029`, `1033` | `verne_fangaulan_adventure_completed`, `verne_gamyi_adventure_completed`, `verne_fahvanosy_dive_adventure_completed`, `verne_ardimya_adventure_completed` |

## Unlock Flow

The decision is not available from game start.

Examples of unlock sources:

- [missions/Verne_Missions.txt:1482](../../missions/Verne_Missions.txt#L1482) sets `verne_akasi_bulwari_adventures_unlocked`
- [missions/Verne_Missions.txt:1483](../../missions/Verne_Missions.txt#L1483) sets `verne_unlocked_adventure_system`
- [missions/Verne_Missions.txt:1580](../../missions/Verne_Missions.txt#L1580) sets `verne_sarhali_adventures_unlocked`
- [missions/Verne_Missions.txt:1659](../../missions/Verne_Missions.txt#L1659) sets `verne_taychendi_kheionai_adventures_unlocked`
- [events/Flavour_Verne_A33.txt:978](../../events/Flavour_Verne_A33.txt#L978) sets `verne_halessi_adventures_unlocked`

So the decision is part of a phased Verne progression tree, not a generic reusable decision.

## Decision Structure

The decision itself starts at:

- [decisions/VerneDecisions.txt:43](../../decisions/VerneDecisions.txt#L43)

It does three major jobs:

1. decides whether the system is available at all
2. highlights currently valid target provinces
3. dispatches the first event in the next valid expedition chain

### Decision potential

The decision requires:

- Verne tag identity
- `verne_unlocked_adventure_system`
- at least one unfinished expedition target

### Shared lock

The decision `allow` block also requires:

- `NOT = { has_country_flag = verne_ongoing_adventure }`

That flag acts as a global expedition mutex.

## Shared Expedition Trigger

The eligibility helper lives here:

- [common/scripted_triggers/anb_scripted_triggers_missions.txt:2450](../../common/scripted_triggers/anb_scripted_triggers_missions.txt#L2450)

It is short but important:

```txt
verne_can_send_expedition = {
	custom_trigger_tooltip = {
		tooltip = verne_send_expe_generic2_tt
		OR = {
			AND = {
				country_or_non_sovereign_subject_holds = ROOT
				has_manpower_building_trigger = yes
			}
			num_of_units_in_province = {
				amount = 5
				who = ROOT
				type = infantry
			}
		}
	}
}
```

That means a target province is expedition-ready if it either:

- is held by Verne or its non-sovereign subjects and has the right manpower building
- or has 5 Verne infantry present

Tooltip localization:

- [localisation/Flavour_Verne_A33_l_english.yml:668](../../localisation/Flavour_Verne_A33_l_english.yml#L668)

## Shared Cancel Helper

This is one of the more elegant parts of the implementation.

The helper lives at:

- [common/scripted_effects/anb_scripted_effects_for_verne.txt:445](../../common/scripted_effects/anb_scripted_effects_for_verne.txt#L445)

```txt
verne_cancel_expedition = {
	hidden_effect = {
		add_country_modifier = {
			hidden = yes
			name = verne_no_delete_explo
			duration = 3
		}
		clr_country_flag = verne_ongoing_adventure
	}
}
```

Why it matters:

- many adventure entry events kill 5 infantry in an `after` block
- the cancel helper adds a short hidden modifier
- the `after` block checks for that modifier and skips troop deletion if cancellation was used

So the system has a reusable "abort cleanly" path rather than duplicating cancellation logic in every branch.

## Event Chain Pattern

Each expedition family follows the same broad pattern:

1. decision dispatches a first event
2. first event sets `verne_ongoing_adventure`
3. player choices set branch flags
4. follow-up events read those branch flags and continue the story
5. a completion event grants rewards
6. the completion event clears branch flags, sets the `*_adventure_completed` flag, and clears `verne_ongoing_adventure`

## Example Chain A - Aur-kes

Entry event:

- [events/Flavour_Verne_A33.txt:3216](../../events/Flavour_Verne_A33.txt#L3216)

The entry event immediately locks the adventure system:

```txt
immediate = {
	hidden_effect = {
		set_country_flag = verne_ongoing_adventure
		remove_country_modifier = verne_no_delete_explo
	}
}
```

It then sets one of several branch flags and schedules the next event:

```txt
option = {
	name = verne.1009.a
	add_treasury = -50
	add_dip_power = -25
	hidden_effect = {
		country_event = {
			id = verne.1010
			days = 182
		}
	}
	set_country_flag = verne_aur_kes_1_A
}
```

The completion event rewards the player and increments the shared adventure counter:

- [events/Flavour_Verne_A33.txt:3498](../../events/Flavour_Verne_A33.txt#L3498)

```txt
option = {
	name = verne.1012.a
	trigger = {
		OR = {
			has_country_flag = verne_aur_kes_3_C
			has_country_flag = verne_aur_kes_3_A
		}
	}
	increase_number_of_adventures_completed = yes
	custom_tooltip = verne_akasi_relic_effect_tt
	add_country_modifier = { hidden = yes name = vernissage_akasi_relic duration = -1 }
}
```

And the chain closes by cleaning its flags:

- [events/Flavour_Verne_A33.txt:3658](../../events/Flavour_Verne_A33.txt#L3658)

```txt
after = {
	clr_country_flag = verne_aur_kes_1_A
	clr_country_flag = verne_aur_kes_1_B
	clr_country_flag = verne_aur_kes_1_C
	clr_country_flag = verne_aur_kes_3_A
	clr_country_flag = verne_aur_kes_3_C
	clr_country_flag = verne_aur_kes_3_B
	set_country_flag = verne_aur_kes_adventure_completed
	clr_country_flag = verne_ongoing_adventure
}
```

## Example Chain B - Amadian Pearl Hunt

Entry event:

- [events/Flavour_Verne_A33.txt:6732](../../events/Flavour_Verne_A33.txt#L6732)

This chain shows a different kind of branching: race-tolerance-dependent options.

```txt
option = {
	name = verne.1045.a
	trigger = {
		OR = {
			high_tolerance_gnollish_race_trigger = yes
			medium_tolerance_gnollish_race_trigger = yes
		}
	}
	set_country_flag = verne_amadia_pearl_hunt_1_A
	medium_increase_of_gnollish_tolerance_effect = yes
	add_estate_loyalty = {
		estate = estate_adventurers
		loyalty = 5
	}
	hidden_effect = {
		country_event = {
			id = verne.1046
			days = 182
		}
	}
}
```

It also has low-tolerance refusal paths that cancel the expedition:

```txt
option = {
	name = verne.1045.a2
	trigger = {
		low_tolerance_gnollish_race_trigger = yes
	}
	verne_cancel_expedition = yes
}
```

This is a good example of the same framework being reused with different thematic gating.

## Example Chain C - Fangaulan Jungle

Entry event:

- [events/Flavour_Verne_A33.txt:4896](../../events/Flavour_Verne_A33.txt#L4896)

This one shows a diplomatic and devastation-focused branch structure rather than a tolerance-heavy one.

```txt
option = {
	name = verne.1025.b
	add_treasury = -100
	every_known_country = {
		limit = { capital_scope = { superregion = fangaula_superregion } has_country_modifier = human_administration }
		custom_tooltip = verne_1025_2_tt
		hidden_effect = {
			if = {
				limit = { capital_scope = { region = dao_nako_region } }
				add_opinion = {
					who = ROOT
					modifier = improved_relation
					multiplier = 50
				}
			}
		}
	}
	hidden_effect = {
		country_event = {
			id = verne.1026
			days = 182
		}
	}
}
```

So the underlying framework is shared, but each chain can swap in very different choice logic.

## Decision Dispatch Pattern

The decision does not randomly pick from all events at once.

It checks unlocked families in priority order and then dispatches the first valid unresolved target it finds.

Example from the Akasi family:

```txt
if = {
	limit = {
		NOT = { has_country_flag = verne_aur_kes_adventure_completed }
		383 = { verne_can_send_expedition = yes }
	}
	country_event = {
		id = verne.1009
	}
}
else_if = {
	limit = {
		NOT = { has_country_flag = verne_damerian_umbar_adventure_completed }
		555 = { verne_can_send_expedition = yes }
	}
	country_event = {
		id = verne.1017
	}
}
```

That means order matters in the decision logic.

## Interaction With Other Verne Systems

The expedition chains feed the shared counter:

- `verne_number_of_adventures_completed`

That counter is checked by missions and also incremented by other Verne content such as:

- [events/Flavour_Verne_A33.txt:1082](../../events/Flavour_Verne_A33.txt#L1082)
- [events/Flavour_Verne_A33.txt:1613](../../events/Flavour_Verne_A33.txt#L1613)
- [events/ExplorationEvents.txt:692](../../events/ExplorationEvents.txt#L692)

So expeditions are part of a wider Verne progression web, not an isolated minigame.

## How It Differs From A Simpler Vanilla-Style Pattern

Compared with a simpler vanilla-style EU4 setup, this system is more layered:

1. one decision can launch many different story chains
2. target availability depends on unlock flags plus province-specific expedition checks
3. the event chains keep internal state through multiple branch flags
4. the system uses a global mutex flag to prevent overlapping chains
5. cancellation is centralized through a scripted effect
6. rewards are often indirect and tied back into the broader Verne progression framework

In short:

- vanilla-style: one decision -> one reward block
- Verne adventure system: one decision -> many gated targets -> multi-step events -> branch cleanup -> shared progression counters

## Editing Cautions

If this system is modified later:

1. preserve `verne_ongoing_adventure` behavior unless deliberately redesigning concurrency
2. preserve `verne_cancel_expedition` or replace it with an equivalent safe cancel path
3. keep the unlock flags, target provinces, and completion flags aligned
4. check both the decision and the event-chain cleanup logic
5. remember that mission progression depends on `verne_number_of_adventures_completed`

## Grounding Verdict

`verne_launch_adventure` is a reusable expedition framework, not just a flavored Verne decision.

The most important anchor files are:

1. [decisions/VerneDecisions.txt](../../decisions/VerneDecisions.txt)
2. [common/scripted_triggers/anb_scripted_triggers_missions.txt](../../common/scripted_triggers/anb_scripted_triggers_missions.txt)
3. [common/scripted_effects/anb_scripted_effects_for_verne.txt](../../common/scripted_effects/anb_scripted_effects_for_verne.txt)
4. [events/Flavour_Verne_A33.txt](../../events/Flavour_Verne_A33.txt)
5. [missions/Verne_Missions.txt](../../missions/Verne_Missions.txt)
