# Network of Adventure System

This article documents the "Network of Adventure" subsystem used by Verne in Anbennar.

It focuses on the progression layer built around Ports of Adventure and the resulting country modifiers.

Related articles:

- [port-of-adventure-system.md](./port-of-adventure-system.md)
- [verne-launch-adventure-system.md](./verne-launch-adventure-system.md)

## Overview

Network of Adventure is the stateful reward layer behind Verne's port-building system.

It is built from:

- a hidden variable
- a province-level port marker
- a mission unlock
- a province UI button
- a scripted effect that increments the hidden counter
- a tiered country-modifier ladder
- mission thresholds that read the counter later

This is the part of the Verne overseas system that turns individual ports into long-term national power.

## Core Files

| Area | File | What it does |
|---|---|---|
| Variable init | [events/Flavour_Verne_A33.txt](../../events/Flavour_Verne_A33.txt) | Initializes `verne_network_of_adventure` and `verne_number_of_adventures_completed` on province `292`. |
| Unlock mission | [missions/Verne_Missions.txt](../../missions/Verne_Missions.txt) | Unlocks the button, gives tier 1, and seeds an initial port. |
| Port creation effect | [common/scripted_effects/anb_scripted_effects_for_verne.txt](../../common/scripted_effects/anb_scripted_effects_for_verne.txt) | Defines `create_port_of_adventure`. |
| Network increment and tier logic | [common/scripted_effects/anb_scripted_effects_for_verne.txt](../../common/scripted_effects/anb_scripted_effects_for_verne.txt) | Defines `increase_size_network_of_adventure`. |
| Province button logic | [common/custom_gui/provinceview.txt](../../common/custom_gui/provinceview.txt) | Lets the player create more ports through the province interface. |
| Tier modifiers | [common/event_modifiers/anb_mission_modifiers.txt](../../common/event_modifiers/anb_mission_modifiers.txt) | Defines tier 1 through tier 5 country modifiers. |
| Mission checks | [missions/Verne_Missions.txt](../../missions/Verne_Missions.txt) | Checks the current network size for later milestones. |
| Localization | [localisation/Flavour_Verne_A33_l_english.yml](../../localisation/Flavour_Verne_A33_l_english.yml) | Names the modifiers and describes the thresholds and button behavior. |

## Main Objects

| Object | Type | Purpose |
|---|---|---|
| `verne_network_of_adventure` | variable | Hidden size counter for the network |
| `verne_port_of_adventure` | province modifier | Marks an established Port of Adventure |
| `verne_unlock_port_of_adventure_button` | country flag | Enables the province UI button |
| `create_port_of_adventure` | scripted effect | Adds a port marker and increments the network |
| `increase_size_network_of_adventure` | scripted effect | Changes the variable and upgrades the tier modifiers |
| `verne_network_of_adventure_tier_1` ... `_tier_5` | country modifiers | Reward ladder tied to network growth |

## Initialization

The variables are explicitly initialized in Verne flavor content:

- [events/Flavour_Verne_A33.txt:441](../../events/Flavour_Verne_A33.txt#L441)

```txt
292 = {
	set_variable = {
		which = verne_network_of_adventure
		value = 0
	}
	set_variable = {
		which = verne_number_of_adventures_completed
		value = 0
	}
}
```

Important implementation detail:

- the network counter is anchored on province `292`
- it is not stored as a straightforward country-only variable

That makes this system more bespoke than a simpler EU4 mission reward ladder.

## Unlock Flow

The major unlock point is:

- [missions/Verne_Missions.txt:1493](../../missions/Verne_Missions.txt#L1493)

The mission `A33_in_search_of_adventure` does several things at once:

- unlocks the province UI button
- gives the first network tier modifier
- unlocks Sarhali adventures
- seeds an initial Port of Adventure

Relevant reward block:

```txt
custom_tooltip = verne_unlock_network_of_adventure
set_country_flag = verne_unlock_port_of_adventure_button
add_country_modifier = {
	name = "verne_network_of_adventure_tier_1"
	duration = -1
}
set_country_flag = verne_sarhali_adventures_unlocked
402 = { create_port_of_adventure = yes }
```

This is a good example of a single mission unlocking both UI and progression state.

## Port Creation Effect

The central reusable effect is:

- [common/scripted_effects/anb_scripted_effects_for_verne.txt:102](../../common/scripted_effects/anb_scripted_effects_for_verne.txt#L102)

```txt
create_port_of_adventure = {
	add_permanent_province_modifier = {
		name = verne_port_of_adventure
		duration = -1
	}
	increase_size_network_of_adventure = yes
}
```

Why this matters:

- port creation is centralized
- every mission, event, or button call feeds the same network logic
- the repo avoids duplicating province-modifier and counter code inline

## Network Increment Logic

The core logic is:

- [common/scripted_effects/anb_scripted_effects_for_verne.txt:2](../../common/scripted_effects/anb_scripted_effects_for_verne.txt#L2)

The effect does three jobs:

1. increments the hidden variable on province `292`
2. swaps out the country tier modifier when thresholds are crossed
3. prints tooltips about current size and the next tier upgrade

Core structure:

```txt
292 = {
	change_variable = {
		which = verne_network_of_adventure
		value = 1
	}
	owner = {
		if = {
			limit = { mission_completed = A33_in_search_of_adventure }
			...
		}
	}
}
custom_tooltip = verne_current_number_of_ports
```

This is a classic Anbennar helper-layer pattern:

- hidden state update first
- country reward update second
- player-facing tooltip explanation last

## Province Button Integration

The custom button lives in:

- [common/custom_gui/provinceview.txt:1621](../../common/custom_gui/provinceview.txt#L1621)

The player can only use it if:

- the button unlock flag exists
- the province is coastal
- the province is in the allowed continents or region
- the province is a level 2 center of trade
- Verne has enough infantry present
- the province does not already have the port modifier

The key effect block is:

```txt
effect = {
	kill_units = { who = FROM type = infantry amount = 5 }
	create_port_of_adventure = yes
	if = {
		limit = {
			region_for_scope_province = {
				is_empty = yes
				has_port = yes
			}
		}
		custom_tooltip = verne_port_of_adventure_button_effect_tt
		hidden_effect = {
			region = {
				limit = {
					is_empty = yes
					has_port = yes
				}
				type = random
				amount = 1
				add_siberian_construction = 100
			}
		}
	}
}
```

So building a new port can also seed frontier growth in a random coastal province in the same region.

## Tier Modifier Ladder

The reward ladder lives in:

- [common/event_modifiers/anb_mission_modifiers.txt:3904](../../common/event_modifiers/anb_mission_modifiers.txt#L3904)

The five tiers are:

- `verne_network_of_adventure_tier_1`
- `verne_network_of_adventure_tier_2`
- `verne_network_of_adventure_tier_3`
- `verne_network_of_adventure_tier_4`
- `verne_network_of_adventure_tier_5`

### Example: tier 1

```txt
verne_network_of_adventure_tier_1 = {
	range = 0.05
	prestige = 0.50
	colonist_placement_chance = 0.05
}
```

### Example: tier 3

```txt
verne_network_of_adventure_tier_3 = {
	range = 0.25
	prestige = 1.00
	colonists = 1
	manpower_recovery_speed = 0.05
	general_cost = -0.25
	mercenary_cost = -0.05
	adventurers_loyalty_modifier = 0.10
	adventurers_influence_modifier = 0.10
	cb_on_overseas = yes
}
```

### Example: tier 5

```txt
verne_network_of_adventure_tier_5 = {
	range = 0.50
	prestige = 1.50
	colonists = 1
	manpower_recovery_speed = 0.15
	general_cost = -0.25
	mercenary_cost = -0.15
	adventurers_loyalty_modifier = 0.20
	adventurers_influence_modifier = 0.20
}
```

This is not a flat bonus system. It is a full state ladder.

## Threshold Messaging

Localization makes the intended thresholds visible to the player:

- [localisation/Flavour_Verne_A33_l_english.yml:107](../../localisation/Flavour_Verne_A33_l_english.yml#L107)
- [localisation/Flavour_Verne_A33_l_english.yml:108](../../localisation/Flavour_Verne_A33_l_english.yml#L108)
- [localisation/Flavour_Verne_A33_l_english.yml:113](../../localisation/Flavour_Verne_A33_l_english.yml#L113)

Examples:

- current network size tooltip
- preview text for tier upgrades
- mission threshold tooltips for 6, 11, and 20 ports

This is another sign that the system is meant to be a persistent tracked mechanic, not just a hidden bonus.

## Mission Hooks

The network is read directly by later missions.

### Unlock mission

- [missions/Verne_Missions.txt:1493](../../missions/Verne_Missions.txt#L1493)

### Six-port threshold

- [missions/Verne_Missions.txt:1630](../../missions/Verne_Missions.txt#L1630)

```txt
custom_trigger_tooltip = {
	tooltip = verne_needs_6_ports_of_adventure_tt
	292 = {
		check_variable = {
			which = verne_network_of_adventure
			value = 6
		}
	}
}
```

### Eleven-port threshold

- [missions/Verne_Missions.txt:2651](../../missions/Verne_Missions.txt#L2651)

### Twenty-port threshold

- [missions/Verne_Missions.txt:2820](../../missions/Verne_Missions.txt#L2820)

This means mission progression is tightly coupled to the hidden network variable.

## Multiple Port Creation Sources

The system is fed from more than one content layer.

### Missions

- [missions/Verne_Missions.txt:204](../../missions/Verne_Missions.txt#L204)
- [missions/Verne_Missions.txt:205](../../missions/Verne_Missions.txt#L205)
- [missions/Verne_Missions.txt:1588](../../missions/Verne_Missions.txt#L1588)
- [missions/Verne_Missions.txt:2621](../../missions/Verne_Missions.txt#L2621)
- [missions/Verne_Missions.txt:2736](../../missions/Verne_Missions.txt#L2736)
- [missions/Verne_Missions.txt:2761](../../missions/Verne_Missions.txt#L2761)

### Events

- [events/Flavour_Verne_A33.txt:965](../../events/Flavour_Verne_A33.txt#L965)
- [events/Flavour_Verne_A33.txt:1106](../../events/Flavour_Verne_A33.txt#L1106)

### Province button

- [common/custom_gui/provinceview.txt:1650](../../common/custom_gui/provinceview.txt#L1650)

This is an important repo pattern:

- all of these sources converge on the same scripted effect

## How It Differs From A Simpler Vanilla-Style Pattern

Compared with a simpler vanilla-style EU4 implementation, Network of Adventure is more elaborate:

1. it uses a hidden variable instead of only static mission completion state
2. it uses a province-anchored state container on province `292`
3. it uses a custom GUI button as an ongoing expansion tool
4. it upgrades through a ladder of permanent country modifiers
5. it is checked repeatedly by later missions
6. it shares infrastructure with the broader Port of Adventure system

In short:

- vanilla-style: mission rewards a permanent modifier
- this system: mission unlocks a growth mechanic, later inputs increase hidden state, and later missions read that state for new thresholds

## Editing Cautions

If this system is changed later:

1. preserve the province `292` variable anchor unless you intentionally migrate the state model
2. preserve the central `create_port_of_adventure` effect instead of duplicating logic
3. keep mission thresholds aligned with the modifier tier expectations
4. remember that the button, the scripted effect, the mission checks, and the localization all have to agree
5. do not assume changing the province modifier alone changes the whole system

## Grounding Verdict

Network of Adventure is the hidden-state reward ladder behind Verne's Ports of Adventure.

The most important anchor files are:

1. [common/scripted_effects/anb_scripted_effects_for_verne.txt](../../common/scripted_effects/anb_scripted_effects_for_verne.txt)
2. [common/event_modifiers/anb_mission_modifiers.txt](../../common/event_modifiers/anb_mission_modifiers.txt)
3. [missions/Verne_Missions.txt](../../missions/Verne_Missions.txt)
4. [common/custom_gui/provinceview.txt](../../common/custom_gui/provinceview.txt)
5. [localisation/Flavour_Verne_A33_l_english.yml](../../localisation/Flavour_Verne_A33_l_english.yml)
