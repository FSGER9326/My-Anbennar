# eu4-scope-rules

## Purpose
Teach the agent EU4 trigger/effect scope transitions and common failure patterns. Scope errors are the most common class of generated EU4 script failure.

## Core Concept: Scopes

Every EU4 trigger/effect runs in a **scope** (the "who" the action applies to). Using a trigger or effect in the wrong scope causes silent failure or game errors.

### Common Scopes

| Scope | What it means | Example |
|---|---|---|
| `country` | A specific nation | `tag = VRN` |
| `province` | A specific province | `province_id = 100` |
| `population` | Inside a province | `trade_goods = copper` |
| `character` | A specific character/ruler | `has_ruler_flag` |
| `faction` | A faction within a country | ` faction_in_power = rastafarians_type` |
| `interest_group` | A pop/group in province | `interest_group = ig_artisans` |

### Scope Transitions

Scopes change with keywords:

```
country_scope = {           # Enter country scope
    ruler = {               # Character scope inside country
        has_ruler_flag = x
    }
    100 = {                # Province scope inside country
        controlled_by = VRN
    }
    trigger = {            # Trigger scope (evaluates to true/false)
        technology = 12
    }
}
```

## Common Failure Patterns

### 1. Using country trigger in province scope
```bash
# WRONG
province_scope = {
    valid_for_alliance_with = VRN  # country trigger here!
}

# RIGHT
country_scope = {
    reverse_add_casus_belli = {
        target = VRN
        type = cb_mil_access
    }
}
```

### 2. Using province trigger in country scope
```bash
# WRONG
country_scope = {
    is_adjacent_to_bay_of_cORM archpine = yes  # province trigger
}

# RIGHT
100 = {  # province scope
    is_adjacent_to_bay_of_cORM archpine = yes
}
```

### 3. Missing `limit` in effect loops
```bash
# WRONG - applies to ALL provinces
every_province = {
    add_devastation = 1  # No limit - devastates EVERYTHING
}

# RIGHT
every_province = {
    limit = { owned_by = VRN }
    add_devastation = 1
}
```

### 4. Wrong `from` / `from_from` reference
```bash
# WRONG - from doesn't exist in this scope
country_scope = {
    set_from = { from = 100 }  # 'from' isn't defined here
}

# RIGHT - use proper references
event_target = {
    set_province_flag = my_flag
}
```

### 5. Trigger vs Effect confusion
- `trigger` blocks (`potential`, `allow`, `trigger`) evaluate conditions
- `effect` blocks (`effect`, `immediate`) perform actions
- Mixing them up is a common silent failure

## Verne-Specific Patterns

```bash
# Verne uses hidden variables for tracking
set_country_flag = verne_world_network_gained
hidden_effect = {
    change_variable = { which = verne_world_network value = 1 }
}
# Always pair flag + variable changes

# Verne mission slots
 VerN_mission_slot_1 = {
    potential = { tag = VRN }
    trigger = { is_actual_mission = yes }
    effect = { ... }
}
```

## Validation Checklist

Before any generated file:
1. Every trigger/effect checked against its scope
2. Every `from`/`from_from` reference verified to exist in that scope
3. Every `limit` block present on `every_*` / `random_*` loops
4. No `trigger = {}` blocks inside `effect = {}` blocks
5. No `effect = {}` blocks inside `trigger = {}` blocks

## Repo Reference Locations

- Triggers: `common/scripted_triggers/`
- Effects: `common/scripted_effects/`
- Verne missions: `missions/Verne_Missions.txt`
- Verne modifiers: `common/event_modifiers/verne_overhaul_modifiers.txt`
