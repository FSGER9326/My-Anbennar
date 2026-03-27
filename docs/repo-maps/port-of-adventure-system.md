# Port of Adventure System Map

This file maps the existing Port of Adventure system as implemented in the Anbennar repo.

It is a repo-grounding document, not a redesign.

Related articles:

- [verne-launch-adventure-system.md](./verne-launch-adventure-system.md)
- [network-of-adventure-system.md](./network-of-adventure-system.md)

## Quick Verdict

Port of Adventure is not a single file feature.

It is a small multi-file subsystem built from:

- mission unlocks
- a custom province UI button
- a Verne-specific scripted effect
- a permanent province modifier
- country-level variable tracking
- country modifiers for network tiers
- event and decision content that interacts with the same progression

## What It Is

At a high level, the system lets Verne establish special overseas harbor provinces called Ports of Adventure.

Those ports then feed a larger "Network of Adventure" progression layer, which is tracked with variables and country modifiers and later checked by missions.

There is also a related but separate expedition/adventure decision system that shares the same broader overseas fantasy and increments the number of adventures completed.

## Core Files Involved

| Area | File | What it does |
|---|---|---|
| Decision entry point | [decisions/VerneDecisions.txt](../../decisions/VerneDecisions.txt) | Defines `verne_launch_adventure`, the expedition-style decision system. |
| Mission unlocks and checks | [missions/Verne_Missions.txt](../../missions/Verne_Missions.txt) | Unlocks the button, seeds ports, checks port presence, and checks network size. |
| Verne events | [events/Flavour_Verne_A33.txt](../../events/Flavour_Verne_A33.txt) | Some event rewards also create ports or increment adventure progress. |
| Shared exploration event | [events/ExplorationEvents.txt](../../events/ExplorationEvents.txt) | Circumnavigation gives Verne another adventure completion increment. |
| Scripted effects | [common/scripted_effects/anb_scripted_effects_for_verne.txt](../../common/scripted_effects/anb_scripted_effects_for_verne.txt) | Defines `create_port_of_adventure`, `increase_size_network_of_adventure`, and `increase_number_of_adventures_completed`. |
| Scripted trigger | [common/scripted_triggers/anb_scripted_triggers_missions.txt](../../common/scripted_triggers/anb_scripted_triggers_missions.txt) | Defines `verne_can_send_expedition`. |
| Province button logic | [common/custom_gui/provinceview.txt](../../common/custom_gui/provinceview.txt) | Defines the scripted custom button behavior and province conditions. |
| Province button placements | [interface/provinceview.gui](../../interface/provinceview.gui) | Places the button in multiple province UI layouts. |
| Province button art | [interface/provinceview.gfx](../../interface/provinceview.gfx) | Defines the `port_of_adventure_button` sprite. |
| Province modifier | [common/event_modifiers/anb_mission_modifiers.txt](../../common/event_modifiers/anb_mission_modifiers.txt) | Defines the permanent `verne_port_of_adventure` modifier. |
| Localization | [localisation/Flavour_Verne_A33_l_english.yml](../../localisation/Flavour_Verne_A33_l_english.yml) | Names, tooltips, network tier text, and mission threshold tooltips. |

## System Flow

## 1. The broader Verne adventure layer is unlocked by missions

The expedition decision system is first unlocked by mission rewards, not by default startup state.

Relevant examples:

- [missions/Verne_Missions.txt:1482](../../missions/Verne_Missions.txt#L1482) sets `verne_akasi_bulwari_adventures_unlocked`
- [missions/Verne_Missions.txt:1483](../../missions/Verne_Missions.txt#L1483) sets `verne_unlocked_adventure_system`
- [missions/Verne_Missions.txt:1580](../../missions/Verne_Missions.txt#L1580) sets `verne_sarhali_adventures_unlocked`
- [missions/Verne_Missions.txt:1659](../../missions/Verne_Missions.txt#L1659) sets `verne_taychendi_kheionai_adventures_unlocked`
- [events/Flavour_Verne_A33.txt:978](../../events/Flavour_Verne_A33.txt#L978) sets `verne_halessi_adventures_unlocked`

This means the player-facing overseas system is phased in by Verne-specific content.

## 2. Port of Adventure itself is created through one reusable scripted effect

The central effect is:

- [common/scripted_effects/anb_scripted_effects_for_verne.txt:102](../../common/scripted_effects/anb_scripted_effects_for_verne.txt#L102)

It does two things:

1. adds the permanent province modifier `verne_port_of_adventure`
2. calls `increase_size_network_of_adventure = yes`

This is important because it means every place that creates a port feeds the same network progression.

## 3. Network size is tracked through a province-anchored variable

The network-size logic lives in:

- [common/scripted_effects/anb_scripted_effects_for_verne.txt:2](../../common/scripted_effects/anb_scripted_effects_for_verne.txt#L2)

The effect increments `verne_network_of_adventure` on province `292`, then upgrades country modifiers once the relevant mission is completed.

This is one of the most important implementation details:

- the system is not stored as a clean country-scoped custom mechanic
- it uses province `292` as a state anchor for variables

That is a very Anbennar-specific practical implementation choice, and it is exactly the kind of thing that can be missed if someone only reads the design summary instead of the code.

## 4. Network tiers are real country modifiers, not just variable thresholds

The tier modifiers are defined at:

- [common/event_modifiers/anb_mission_modifiers.txt:3904](../../common/event_modifiers/anb_mission_modifiers.txt#L3904)
- [common/event_modifiers/anb_mission_modifiers.txt:3909](../../common/event_modifiers/anb_mission_modifiers.txt#L3909)
- [common/event_modifiers/anb_mission_modifiers.txt:3917](../../common/event_modifiers/anb_mission_modifiers.txt#L3917)
- [common/event_modifiers/anb_mission_modifiers.txt:3928](../../common/event_modifiers/anb_mission_modifiers.txt#L3928)
- [common/event_modifiers/anb_mission_modifiers.txt:3940](../../common/event_modifiers/anb_mission_modifiers.txt#L3940)

So the variable is only part of the system. The actual player reward layer is expressed through permanent country modifiers such as:

- `verne_network_of_adventure_tier_1`
- `verne_network_of_adventure_tier_2`
- `verne_network_of_adventure_tier_3`
- `verne_network_of_adventure_tier_4`
- `verne_network_of_adventure_tier_5`

## 5. The province UI button is a real scripted custom GUI button

The button logic is defined here:

- [common/custom_gui/provinceview.txt:1621](../../common/custom_gui/provinceview.txt#L1621)

Important gating rules in the button logic:

- owner or overlord must have `verne_unlock_port_of_adventure_button`
- province must be held by the country or subject chain
- province must be in Africa, North America, South America, or `ringlet_isles_region`
- province must have a port
- province must be a level 2 center of trade
- province must have at least 5 infantry from the acting country
- province must not already have `verne_port_of_adventure`

On use, it:

- kills 5 infantry
- runs `create_port_of_adventure = yes`
- can fire a merfolk opinion effect
- can add `100` siberian construction in a random empty coastal province in the same region

This is much more bespoke than a normal vanilla decision or mission reward.

## 6. The province button exists in multiple GUI layouts

The button is placed multiple times in `interface/provinceview.gui`:

- [interface/provinceview.gui:2859](../../interface/provinceview.gui#L2859)
- [interface/provinceview.gui:3403](../../interface/provinceview.gui#L3403)
- [interface/provinceview.gui:3642](../../interface/provinceview.gui#L3642)

This is a good example of how Anbennar custom buttons are often implemented:

- logic lives in `common/custom_gui/...`
- visible button placement lives in `interface/...gui`
- art lives in `interface/...gfx`

The sprite is defined at:

- [interface/provinceview.gfx:1886](../../interface/provinceview.gfx#L1886)

## 7. Missions both seed ports and check for them later

This is one of the most important patterns in the system.

Missions do not only unlock the system. They also:

- directly create ports in specific provinces
- later require ported provinces as mission conditions
- later require total network size thresholds

### Examples of direct port creation in mission effects

- [missions/Verne_Missions.txt:204](../../missions/Verne_Missions.txt#L204) and [missions/Verne_Missions.txt:205](../../missions/Verne_Missions.txt#L205)
- [missions/Verne_Missions.txt:1588](../../missions/Verne_Missions.txt#L1588)
- [missions/Verne_Missions.txt:2621](../../missions/Verne_Missions.txt#L2621)
- [missions/Verne_Missions.txt:2736](../../missions/Verne_Missions.txt#L2736)
- [missions/Verne_Missions.txt:2761](../../missions/Verne_Missions.txt#L2761)

### Examples of mission checks that require a specific port province

- [missions/Verne_Missions.txt:532](../../missions/Verne_Missions.txt#L532) and [missions/Verne_Missions.txt:549](../../missions/Verne_Missions.txt#L549)
- [missions/Verne_Missions.txt:1739](../../missions/Verne_Missions.txt#L1739) and [missions/Verne_Missions.txt:1757](../../missions/Verne_Missions.txt#L1757)

### Examples of mission checks that require total network size

- [missions/Verne_Missions.txt:1630](../../missions/Verne_Missions.txt#L1630)
- [missions/Verne_Missions.txt:2651](../../missions/Verne_Missions.txt#L2651)
- [missions/Verne_Missions.txt:2820](../../missions/Verne_Missions.txt#L2820)

## 8. Events can also create ports directly

Port creation is not limited to missions or the UI button.

Examples:

- [events/Flavour_Verne_A33.txt:965](../../events/Flavour_Verne_A33.txt#L965) creates a port in province `4963`
- [events/Flavour_Verne_A33.txt:1106](../../events/Flavour_Verne_A33.txt#L1106) creates a port in the capital scope

This shows the same effect being reused in another content layer instead of copying modifier logic inline.

## 9. The adventure-completion counter is separate from the port counter

This is easy to mix up, but the code keeps them separate:

- `verne_network_of_adventure`
- `verne_number_of_adventures_completed`

The second one is incremented by:

- [common/scripted_effects/anb_scripted_effects_for_verne.txt:110](../../common/scripted_effects/anb_scripted_effects_for_verne.txt#L110)

And it is reused in many event rewards, for example:

- [events/Flavour_Verne_A33.txt:1082](../../events/Flavour_Verne_A33.txt#L1082)
- [events/Flavour_Verne_A33.txt:1613](../../events/Flavour_Verne_A33.txt#L1613)
- [events/ExplorationEvents.txt:692](../../events/ExplorationEvents.txt#L692)

This means the broader Verne adventure system has at least two overlapping progression tracks:

1. Ports / network size
2. Adventures completed

## 10. The expedition decision is related, but not identical, to the port button

The main decision is:

- [decisions/VerneDecisions.txt:43](../../decisions/VerneDecisions.txt#L43)

What it does:

- highlights specific target provinces
- checks region-specific unlock flags
- uses `verne_can_send_expedition`
- dispatches different Verne event chains depending on which valid target exists

The expedition trigger it relies on is defined here:

- [common/scripted_triggers/anb_scripted_triggers_missions.txt:2450](../../common/scripted_triggers/anb_scripted_triggers_missions.txt#L2450)

So "Port of Adventure" is not the whole adventure system.
It is one major branch of a broader Verne overseas package.

## Concrete Coding Examples

## Example A - scripted effect used as a shared system entry point

Instead of copying the same modifier logic in every mission and event, Anbennar centralizes it:

- `create_port_of_adventure = { ... }`

Defined at:

- [common/scripted_effects/anb_scripted_effects_for_verne.txt:102](../../common/scripted_effects/anb_scripted_effects_for_verne.txt#L102)

That effect is then called from:

- mission rewards
- event rewards
- the custom province button

This is a strong repo pattern to reuse later.

## Example B - custom province UI button instead of a normal decision

The custom button is implemented through:

- logic in [common/custom_gui/provinceview.txt:1621](../../common/custom_gui/provinceview.txt#L1621)
- placements in [interface/provinceview.gui:2859](../../interface/provinceview.gui#L2859), [interface/provinceview.gui:3403](../../interface/provinceview.gui#L3403), and [interface/provinceview.gui:3642](../../interface/provinceview.gui#L3642)
- art in [interface/provinceview.gfx:1886](../../interface/provinceview.gfx#L1886)

This is more complex than a normal vanilla mission or decision pattern.

## Example C - province modifier plus country variable plus country modifier

Port of Adventure uses three layers at once:

1. province-level marker:
   - `verne_port_of_adventure`
   - [common/event_modifiers/anb_mission_modifiers.txt:3672](../../common/event_modifiers/anb_mission_modifiers.txt#L3672)
2. state counter:
   - `verne_network_of_adventure`
   - [common/scripted_effects/anb_scripted_effects_for_verne.txt:2](../../common/scripted_effects/anb_scripted_effects_for_verne.txt#L2)
3. country reward tiers:
   - `verne_network_of_adventure_tier_1` through `_tier_5`
   - [common/event_modifiers/anb_mission_modifiers.txt:3904](../../common/event_modifiers/anb_mission_modifiers.txt#L3904)

That layered design is more elaborate than a simple single-mission permanent modifier.

## How It Differs From A Simpler Vanilla-Style EU4 Pattern

Port of Adventure differs from a simpler vanilla-style implementation in several ways:

1. it uses a custom province UI button instead of only decisions and missions
2. it relies on a bespoke scripted effect and Verne-specific helper logic
3. it tracks progression with province-anchored variables on province `292`
4. it upgrades through permanent country modifiers rather than one flat reward
5. it mixes province conditions, region filters, mission unlock flags, event rewards, and subject-aware ownership logic
6. it is tightly woven into Verne mission progression instead of being a generic reusable vanilla mechanic

In short:

- vanilla-style content is often "mission or decision gives modifier"
- this Anbennar system is "mission unlocks UI + effect creates province marker + effect increments hidden network counter + missions and events read those values later"

## Practical Takeaways For Future Verne Overhaul Work

If this system is ever changed, the safe lesson from the repo is:

1. do not treat Port of Adventure as a single decision or single modifier
2. preserve the button path unless there is a strong reason to rewrite GUI
3. preserve the shared scripted effect pattern instead of duplicating logic
4. check all three state layers:
   - province modifier
   - network variable
   - country tier modifier
5. remember that the broader adventure system also uses separate expedition and adventure-completion plumbing

## Grounding Verdict

Port of Adventure is a Verne-specific Anbennar subsystem built from real repo patterns in multiple layers.

The most important anchor files for any future modification are:

1. [common/scripted_effects/anb_scripted_effects_for_verne.txt](../../common/scripted_effects/anb_scripted_effects_for_verne.txt)
2. [common/custom_gui/provinceview.txt](../../common/custom_gui/provinceview.txt)
3. [missions/Verne_Missions.txt](../../missions/Verne_Missions.txt)
4. [events/Flavour_Verne_A33.txt](../../events/Flavour_Verne_A33.txt)
5. [common/event_modifiers/anb_mission_modifiers.txt](../../common/event_modifiers/anb_mission_modifiers.txt)
