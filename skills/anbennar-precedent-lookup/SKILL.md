# anbennar-precedent-lookup

## Purpose
Find similar existing implementations in the repo to use as precedent before generating new content. Repo precedent is the strongest form of validation — if a pattern exists in the repo, it is safe to replicate.

## How to Use This Skill

Before generating any EU4 content (missions, events, decisions, modifiers):
1. Search repo for similar existing content
2. Use that file's patterns as your template
3. Record the precedent in the mod-spec

## Search Strategy

### By Mechanic Family
```
missions/Verne_Missions.txt — search for "hidden_effect", "set_country_flag", "change_variable"
common/event_modifiers/verne_overhaul_modifiers.txt — search for modifier patterns
decisions/Verne*.txt — search for decision patterns
```

### By Tag
```
events/verne_overhaul_*.txt — tag-specific events
localisation/Flavour_Verne_A33_l_english.yml — tag-specific loc
```

### By Pattern Type
- **Mission chains** → search `missions/` for `verne_mission_slot` patterns
- **Modifier application** → search `missions/` for `add_permanent_flag` + `modifier` effects
- **Variable tracking** → search for `change_variable` + `set_country_flag` pairs
- **Event chains** → search `events/` for namespace + `.1`, `.2`, `.3` patterns

## Precedent Categories

### Mission Precedent
Look for:
- Slot usage (which `verne_mission_slot_X`)
- Trigger style (`is_actual_mission`, `has_mission`, `has_country_flag`)
- Effect patterns (`hidden_effect`, `ai_chance`, `effect`)
- Variable usage (`change_variable`, `set_country_flag`)
- Tooltip patterns (`custom_tooltip`, `tooltip`)

### Event Precedent
Look for:
- Namespace usage
- Trigger scope
- Mean time to happen (MTTH)
- Option structure
- Chain patterns (`.1`, `.2`, `.3`)

### Modifier Precedent
Look for:
- How modifiers are applied (`add_permanent_modifier`, `add_country_modifier`)
- Whether they're temporary or permanent
- Stacking rules
- Icon usage

## Repo Paths for Verne

```
VERNE_REPO = C:\Users\User\Documents\GitHub\My-Anbennar

missions/Verne_Missions.txt                      # ~117 missions, 9 slots
events/Flavour_Verne_A33.txt                     # Main events
events/verne_overhaul_*.txt                      # Overhaul event files
common/event_modifiers/verne_overhaul_modifiers.txt  # 34 modifiers
common/government_reforms/verne_overhaul_reforms.txt # 24 reforms
decisions/                                       # Verne decisions
localisation/Flavour_Verne_A33_l_english.yml    # Main loc (369KB)
```

## Precedent Recording Format

In mod-spec, record as:
```yaml
sources:
  repo_precedents:
    - path: "missions/Verne_Missions.txt"
      lines: "1200-1250"
      pattern: "verne_mission_slot_3 with hidden_effect + variable tracking"
      used_for: "Lane 3 mission structure template"
```

## Blast Radius Check

After finding precedent, classify blast radius:
- **Low** — single mission, single event, single modifier
- **Medium** — new event namespace, new modifier type
- **High** — new slot, new mechanic system, common/ override
- **Critical** — map/trade changes, government reform changes
