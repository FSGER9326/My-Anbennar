# eu4_events_decisions_missions

## Purpose
Teach event, decision, and mission generation patterns — namespaces, ID allocation, file layout, scope correctness, and when to prefer each mechanism.

## Events

### Namespace Rule (Mandatory)
Every event file MUST use a namespace. This prevents ID collisions and makes events easier to maintain.

```bash
namespace = verne_overhaul_dynasty
```

Event IDs then use the namespace prefix:
```bash
verne_overhaul_dynasty.1 = {
    # ...
}
verne_overhaul_dynasty.2 = {
    # ...
}
```

### Event File Structure
```bash
namespace = my_namespace

# Single event
my_namespace.1 = {
    title = "my_event_title"           # loc key (no .yml needed)
    desc = "my_event_desc"              # loc key
    picture = "event_art_storytelling"  # art asset name
    
    is_triggered_only = yes             # or is_triggered_only / mean_time_to_happen
    mean_time_to_happen = { months = 6 }
    
    trigger = {
        tag = VRN                       # condition to even be possible
    }
    
    immediate = {
        # fires at event start, before showing to player
    }
    
    option = {
        name = "my_event_option_1"
        trigger = {
            # option-specific condition
        }
        effect = {
            # what happens
        }
    }
}
```

### Key Event Fields

| Field | Required | Notes |
|---|---|---|
| `title` | Yes | Loc key, no spaces in key name |
| `desc` | Yes | Loc key |
| `picture` | Recommended | Art asset from `gfx/event_pictures/` |
| `is_triggered_only` | Yes | For events that fire via effects, not random |
| `mean_time_to_happen` | Sometimes | Use for random events; omit if `is_triggered_only = yes` |
| `trigger` | Yes | Condition the event can fire |
| `immediate` | Sometimes | Runs before options display |
| `option` | Yes | At least one option required |

### Event Scope

Inside `option = { effect = { } }`, you are in **country scope** by default. Province-level effects need ` province_scope = { }`.

### Verne Event Namespaces (from registry)
```
verne_overhaul_advisor
verne_overhaul_crisis
verne_overhaul_dynasty
verne_liliac
```

### Testing Events
```bash
# In EU4 console — fires event immediately for a country
event verne_overhaul_dynasty.1 VRN
```

### Event Chaining
```bash
# In option effect:
country_scope = {
    hidden_effect = {
        set_country_flag = my_chain_flag
    }
    # Then chain event fires in next month:
    trigger_event = {
        id = my_namespace.2
        days = 30
    }
}
```

## Decisions

### Required Fields (Minimum Schema)

Every decision MUST have all four:

```bash
vn_establish_colony = {
    name = "Establish a Colony"         # Display name (loc key or string)
    potential = {
        tag = VRN                        # Who can see this decision
        NOT = { has_country_flag = colony_established }
    }
    allow = {
        gold = 100                       # Cost / conditions to ACTIVATE
        num_of_ports = 2
    }
    effect = {
        # What happens when taken
        add_gold = -100
        province_scope = {
            add_base_production = 1
        }
    }
}
```

### Decision Types
- **country_decisions** — appear in decisions panel, cost something to activate
- **mission** — appears in mission tree, auto-triggers on prerequisites
- **formable_decisions** — special formation decisions (e.g., forming a nation)

### Verne Decision IDs (from registry)
```
verne_launch_adventure
verne_can_send_expedition
verne_overhaul_formalize_silver_oaths
verne_overhaul_seed_silver_oaths_path
verne_overhaul_open_marriage_court
verne_overhaul_activate_marriage_court
verne_enforce_dynastic_safeguard
verne_overhaul_activate_dynasty_protection
verne_proclaim_exalted_lineage
verne_overhaul_appoint_court_advisor
```

### Formable Decisions
Anbennar has many formable nations. Before creating a new formable:
1. Check gameplay wiki for existing formables
2. Check `decisions/` for existing patterns
3. Common prerequisites: specific culture, religion, government reform, flag set

## Missions

### Mission File Location
- Path: `missions/{Tag}_Missions.txt` or `missions/{ModName}_Missions.txt`
- Verne: `missions/Verne_Missions.txt`

### Mission Slot Structure
```bash
verne_mission_slot_1 = {
    potential = {
        tag = VRN                        # Only for Verne
        NOT = { has_country_flag = verne_mission_1_completed }
    }
    verne_mission_1 = {                  # Actual mission ID
        name = "verne_mission_1_name"    # Loc key
        desc = "verne_mission_1_desc"    # Loc key
        
        trigger = {
            # Prerequisites — what must be true to SEE this mission
            treasury = 500
            num_of_ports = 3
        }
        
        effect = {
            # What happens on completion
            add_treasury = 500
            set_country_flag = verne_mission_1_completed
        }
        
        ai_will_do = {
            factor = 1
            modifier = {
                factor = 2
                treasury = 1000
            }
        }
    }
}
```

### Mission Slot Layout (Verne 10-lane)
```
Lane 1: verne_mission_slot_1 — Court & Oaths
Lane 2: verne_mission_slot_2 — Adventure Network
Lane 3: verne_mission_slot_3 — Maritime Empire
Lane 4: verne_mission_slot_4 — Dynastic Machine
Lane 5: verne_mission_slot_5 — Trade & Colonisation
Lane 6: verne_mission_slot_6 — Red Court & Arcane
Lane 7: verne_mission_slot_7 — Military Orders
Lane 8: verne_mission_slot_8 — Faith & Apostolic Empire
Lane 9: verne_mission_slot_9 — Industrial Foundries
Lane 10: Liliac War flag-gated missions (no verne_mission_slot_X reference)
```

### Verne Variable Tracking Patterns
Many missions use hidden variable tracking:
```bash
hidden_effect = {
    change_variable = { which = verne_world_network value = 1 }
}
set_country_flag = verne_world_network_gained
```
Always pair `change_variable` + `set_country_flag`.

### Testing Missions
```bash
# Fire a mission directly
event verne_mission_1 VRN
```

### Mission Tooltip Localisation
When missions track variables, add `custom_tooltip`:
```bash
custom_tooltip = verne_world_network_tt
# Then in localisation:
verne_world_network_tt:0 "£verne_world_network£ / 10 networks established"
```

## Choosing Between Events, Decisions, and Missions

| Use | Mechanism | Why |
|---|---|---|
| One-time story beat | Event chain | Player doesn't choose, fires on trigger |
| Player choice with cost | Decision | Player activates, pays price |
| Goal with prerequisites | Mission tree | Visible progression, completion effects |
| Reactive to game state | Event | Fires when condition becomes true |
| Long-term project | Mission | Visible in UI, multiple steps |

## Common Scope Mistakes

```bash
# WRONG — province trigger in country effect
effect = {
    is_adjacent_to_bay = yes  # Province trigger!
}

# RIGHT — province scope wrapper
effect = {
    123 = {  # province scope
        is_adjacent_to_bay = yes
    }
}

# WRONG — country trigger in province effect
province_scope = {
    add_casus_belli = {   # Country effect!
        target = VRN
    }
}

# RIGHT
country_scope = {
    add_casus_belli = {
        target = FROM
    }
}
```
