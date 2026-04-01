# EU4 Anbennar Modding Reference

Project-specific knowledge base for Verne overhaul modding.
Maintained by the self-improving-agent skill — promote learnings here when patterns recur 3+ times.

Last updated: 2026-03-31

---

## Table of Contents
- [File Structure](#file-structure)
- [Mission Scripting](#mission-scripting)
- [Event Scripting](#event-scripting)
- [Modifier Reference](#modifier-reference)
- [Government Reforms](#government-reforms)
- [Localisation](#localisation)
- [Decisions](#decisions)
- [Common Pitfalls](#common-pitfalls)
- [Anbennar-Specific Conventions](#anbennar-specific-conventions)
- [Verne Overhaul Architecture](#verne-overhaul-architecture)

---

## File Structure

### Standard Anbennar Mod Layout
```
My-Anbennar/
├── common/
│   ├── event_modifiers/       # Modifier definitions (add_country_modifier, etc.)
│   ├── government_reforms/    # Reform definitions (verne_overhaul_reforms.txt)
│   ├── governments/           # Government type definitions
│   ├── cb_types/              # Casus belli definitions
│   ├── estates/               # Estate definitions
│   ├── buildings/             # Building definitions
│   └── policies/              # Policy definitions
├── events/                    # Event files (namespace = verne)
│   ├── Flavour_Verne_A33.txt  # Main flavour events
│   ├── verne_overhaul_*.txt   # Overhaul event chains
│   └── zzz_verne_*.txt        # Late-loading events (zzz prefix)
├── missions/                  # Mission tree files
│   └── Verne_Missions.txt     # All Verne missions (A33_first_slot through A33_eighth_slot)
├── decisions/                 # Decision files
├── history/                   # Province/country history
├── localisation/              # Localisation files (l_english.yml)
│   ├── Flavour_Verne_A33_l_english.yml
│   └── verne_overhaul_*_l_english.yml
└── gfx/interface/             # Icons (ideas_EU4 folder)
```

### File Naming Conventions
- Verne overhaul files: `verne_overhaul_<topic>_events.txt`
- Localisation: `verne_overhaul_<topic>_l_english.yml`
- Late-loading: prefix with `zzz_` (e.g., `zzz_verne_overhaul_dynasty_events.txt`)
- Event modifiers: `verne_overhaul_modifiers.txt` (single file for all modifiers)

---

## Mission Scripting

### Mission Slot Structure
```pdx
A33_first_slot = {
    slot = 1                    # Tree slot (1-9)
    generic = no
    ai = yes
    has_country_shield = yes
    potential = { tag = A33 }   # Only visible for Verne

    A33_mission_id = {
        icon = mission_icon_name
        position = 2            # Position within the slot (1-9)
        provinces_to_highlight = { }  # Provinces to highlight on map

        trigger = {
            # Conditions that must be met
        }

        effect = {
            # Rewards when completed
        }
    }
}
```

### Key Rules
- Each slot is a separate wrapper: `A33_first_slot`, `A33_second_slot`, etc.
- `position = N` controls column position within the slot
- Missions can chain via `required_missions = { previous_mission }`
- `has_country_shield = yes` makes it show in the mission tab
- AI can complete missions automatically with `ai = yes`

### Common Trigger Patterns
```pdx
# Tag check
tag = A33
is_or_was_tag = { tag = A33 }

# Province checks
owns = 288                          # Own specific province
num_of_provinces = { value = 5 }    # Province count
any_owned_province = { has_building = university }

# Reform checks
has_reform = verne_court_of_oaths_reform
has_reform = verne_red_court_arcana_reform

# Mission completion
has_completed_mission = A33_formalize_silver_oaths
has_country_flag = verne_census_established

# Institution checks
has_institution = renaissance

# Religion checks
religion = corinite
OR = { has_personal_deasy = corin religion = corinite }
```

### Common Effect Patterns
```pdx
# Modifiers (timed)
add_country_modifier = { name = verne_my_modifier duration = -1 }  # Permanent
add_country_modifier = { name = verne_my_modifier duration = 7300 } # 20 years
add_province_modifier = { name = verne_heartspier_port duration = 3650 } # 10 years

# Flags (for cross-mission/lanes gating)
set_country_flag = verne_my_flag
clr_country_flag = verne_my_flag   # Clear flag
has_country_flag = verne_my_flag   # Check flag

# Variables
change_variable = { name = verne_overseas_projection add = 1 }

# Events
country_event = { id = verne_overhaul_oaths.1 }
country_event = { id = verne.200 }  # Main namespace

# Power/Stats
add_legitimacy = 10
add_prestige = 15
add_diplo_power = 50
add_adm_power = 25
add_navy_tradition = 10
add_sailors = 1000
add_stability = 1
add_innovativeness = 1
add_mercantilism = 2

# Province-specific (in province scope)
288 = { add_province_modifier = { name = verne_center duration = 3650 } }
```

---

## Event Scripting

### Event Structure
```pdx
namespace = verne    # Namespace for ID resolution: verne.X.t = text

country_event = {
    id = verne.12            # namespace.number format
    title = verne.12.t       # Localisation key: <namespace>.<id>.t
    desc = verne.12.d        # Localisation key: <namespace>.<id>.d
    picture = RELIGION_eventPicture  # Event art

    fire_only_once = yes     # One-time event
    is_triggered_only = yes  # Only fires when called by another event/script

    trigger = {
        # Conditions for the event to be eligible
    }

    immediate = {
        hidden_effect = {
            # Runs before options, not shown to player
        }
    }

    option = {
        name = verne.12.a       # Localisation key
        ai_chance = { factor = 1 }  # AI weighting
        # Effects when player picks this option
    }
}
```

### Event Picture Constants
- `RELIGION_eventPicture` — religious events
- `DIPLOMACY_eventPicture` — diplomatic events
- `ECONOMY_eventPicture` — economic events
- `MILITARY_eventPicture` — military events
- `ESTATE_eventPicture` — estate events
- `EXPLORATION_eventPicture` — exploration events

### Event Types
| Type | Description |
|------|-------------|
| `country_event = { ... }` | Fires for a specific country |
| `province_event = { ... }` | Fires for a specific province |
| `is_triggered_only = yes` | Only fires via explicit trigger |
| `fire_only_once = yes` | Fires at most once per game |
| `hidden = yes` | Not shown to player (effect-only) |

### Pulse Events (for recurring random events)
```pdx
# Yearly pulse: each_year = { random_events = { ... } }
# 2-year pulse: every_24_months = { ... }
# Monthly pulse: each_month = { ... }  (mod-only, vanilla unused)
```

### MTTH (Mean Time to Happen)
```pdx
mean_time_to_happen = {
    months = 120           # Base: 10 years
    modifier = {
        factor = 0.5       # Halve if condition met
        has_country_modifier = some_modifier
    }
}
```

---

## Modifier Reference

### Modifier Types
| Type | File Location | How Applied | Duration |
|------|--------------|-------------|----------|
| Static | `common/static_modifiers/` | Internal engine | Varies |
| Event (country/province) | `common/event_modifiers/` | `add_country_modifier` / `add_province_modifier` | Set by `duration` |
| Triggered | `common/triggered_modifiers/` | Auto when conditions met | While conditions hold |
| Province Triggered | `common/province_triggered_modifiers/` | `add_province_triggered_modifier` | While conditions hold |
| Opinion | `common/opinion_modifiers/` | `add_opinion` | Set by `months` |

### Event Modifier Format (most common for mods)
```pdx
verne_my_modifier = {
    # Country modifiers
    diplomatic_reputation = 1
    trade_efficiency = 0.05
    governing_capacity = 10
    governing_capacity_modifier = 0.10   # percentage
    
    # Province modifiers (in province scope)
    local_tax_modifier = 0.20
    local_trade_power = 5
    local_development_cost = -0.10
    
    # Optional
    picture = "trade_efficiency"    # Icon override
    # Description: desc_verne_my_modifier: "Text here"
}
```

### Duration Values
- `-1` = permanent (never expires)
- `3650` = 10 years (365 days × 10)
- `5475` = 15 years
- `7300` = 20 years
- `9125` = 25 years

### Common Modifier Keys
| Key | Effect | Type |
|-----|--------|------|
| `diplomatic_reputation` | +N dip rep | Country |
| `trade_efficiency` | ±N% trade income | Country |
| `governing_capacity` | +N flat gov cap | Country |
| `governing_capacity_modifier` | ±N% gov cap | Country |
| `diplomatic_annexation_cost` | ±N% annex cost | Country |
| `liberty_desire` | ±N lib desire (subjects) | Country |
| `legitimacy` | ±N yearly legitimacy | Country |
| `prestige` | ±N/year prestige | Country |
| `land_morale` | ±N% army morale | Country |
| `morale_of_navies` | ±N% navy morale | Country |
| `colonial_range` | ±N% colonial range | Country |
| `global_tariffs` | ±N% tariffs | Country |
| `settler_growth` | ±N% settler growth | Country |
| `naval_forcelimit_modifier` | ±N% naval FL | Country |
| `tariffs` | ±N% tariffs | Country |
| `trade_range_modifier` | ±N% trade range | Country |
| `advisor_pool` | +N advisor slots | Country |
| `reform_progress_growth` | ±N/year reform progress | Country |
| `army_tradition` | ±N/year army tradition | Country |
| `navy_tradition` | ±N/year navy tradition | Country |
| `innovativeness` | ±N/year innovativeness | Country |
| `institution_spread` | ±N% institution spread | Country |
| `local_sailors_modifier` | ±N% local sailors | Province |
| `local_development_cost` | ±N% local dev cost | Province |
| `province_trade_power_value` | +N trade power | Province |
| `local_tax_modifier` | ±N% local tax | Province |
| `local_missionary_strength` | ±N% missionary strength | Province |
| `institution_spread` | ±N% inst spread | Province |

### ⚠️ Common Modifier Mistakes
- `governing_capacity = 10` → flat bonus. Use `governing_capacity_modifier = 0.10` for percentage.
- Duration `-1` = permanent. Duration `0` = temporary (removed on next tick).
- Modifier name must match exactly in definition and `add_country_modifier` call.
- Don't forget localisation for modifier names and descriptions.

---

## Government Reforms

### Reform Structure
```pdx
# In common/government_reforms/verne_overhaul_reforms.txt
verne_my_reform = {
    icon = "some_icon_gfx"
    allow_normal_conversion = yes
    potential = { tag = A33 }
    trigger = { tag = A33 }
    
    modifiers = {
        diplomatic_reputation = 1
        trade_efficiency = 0.05
    }
    
    effect = {
        # Fires when reform is enacted
    }
}
```

### Reform Tiers
Verne uses multiple reform tiers. Key reform names from the codebase:
- Tier 1: Starting government
- Tier 2: `verne_court_of_oaths_reform`, `verne_estuary_companies_of_heartspier_reform`
- Tier 4: `verne_hall_of_distant_horizons_reform`
- Tier 6: `verne_overseas_commanderies_reform`, `verne_imperial_sea_court_reform`
- Tier 7: `verne_apostolic_court_of_corin_reform`, `verne_vernman_court_of_the_world_reform`
- Tier 8: `verne_crown_of_the_oathkeeper_reform`, `verne_throne_of_the_wyvern_kings_reform`, `verne_exalted_dynasty_machine_reform`

### Cross-lane Gating
Many missions require specific reforms. Reform chains must be compatible:
- Court lane → Oathkeeper tier 8
- Dynastic lane → Wyvern Kings tier 8
- Red Court → Collegium tier 7+
- Maritime lane → Sea Court tier 6
- Faith lane → World Faith Emperor tier 7

---

## Localisation

### Format
```yaml
l_english:
 verne_my_mission_title:0 "Formalize the Silver Oaths"
 verne_my_mission_desc:0 "Establish the ancient Silver Oaths as a formal system."
 verne_my_modifier_modifier_desc:0 "The Silver Oaths grant enhanced diplomatic standing."
 verne_my_tt:0 "Verne's system allows binding diplomatic contracts."
```

### Key Naming Convention
| Key Pattern | Used For |
|-------------|----------|
| `A33_<mission_id>_title` | Mission name |
| `A33_<mission_id>_desc` | Mission description |
| `<modifier_name>_modifier_desc` | Modifier tooltip |
| `verne_<lane>_<concept>_tt` | Custom tooltips |
| `verne.<event_id>.t` | Event title |
| `verne.<event_id>.d` | Event description |
| `verne.<event_id>.a` | Event option |

### Rules
- Format: `key:0 "text"` (the `:0` is version tag, always include)
- YAML requires proper indentation (spaces, no tabs)
- Special chars in text: use `\"` for quotes inside text
- Multi-line: use `desc:0 "Line1 $BR$ Line2"` or separate keys
- **Always create localisation for every new key** — game shows raw keys without it

---

## Decisions

### Decision Structure
```pdx
verne_my_decision = {
    major = yes              # Shows as major decision
    potential = { tag = A33 } # Who can see it
    allow = { ... }          # Conditions to enact
    effect = { ... }         # What happens
    ai_will_do = { factor = 1 }  # AI likelihood
}
```

### Decision as Unlock from Mission
Missions can unlock decisions via flags:
```pdx
# In mission effect:
set_country_flag = verne_charter_unlocked

# In decision file:
verne_charter_overseas_decision = {
    potential = { has_country_flag = verne_charter_unlocked }
    allow = { ... }
    effect = { ... }
}
```

---

## Common Pitfalls

### Syntax Errors
1. **Mismatched braces** — every `{` needs a `}`
2. **Missing equals signs** — `trigger = { ... }` not `trigger { ... }`
3. **Tabs vs spaces** — EU4 uses tabs for indentation (Paradox format)
4. **Semicolons** — NOT used in Paradox script (unlike C-family languages)
5. **Comment syntax** — `# comment` only, not `//` or `/* */`

### Logic Errors
1. **Missing localisation** — game shows raw keys like `MISSING_KEY_title`
2. **Flag not set** — if mission sets `set_country_flag`, next mission must check `has_country_flag`
3. **Modifier duration** — `-1` = permanent, `0` = one-month temporary. Not the same!
4. **Province scope vs country scope** — `owns = 288` (country scope) vs `288 = { ... }` (province scope)
5. **Event id collision** — namespace must be unique; don't reuse id numbers

### Anbennar-Specific
1. **Tag = A33** is Verne's tag in Anbennar
2. **Province 288** = Heartspier (Verne's capital)
3. **Province 291** = Calasandur
4. **Corinite** = Verne's canonical religion (reformation era)
5. **Province names** vs IDs — always use province IDs for scripts
6. **is_or_was_tag = { tag = A33 }** for events that should fire even after tag change
7. **"sloth" typo** in `A33_fifth_sloth` — preserve, it's referenced in existing code

### Cross-file Dependencies
| File type | Depends on |
|-----------|-----------|
| Missions | Event modifiers (common/event_modifiers/) |
| Events | Localisation (localisation/) |
| Decisions | Flags set by missions/events |
| Modifiers | Icon files (gfx/interface/) |
| All player-facing | Localisation YAML |

---

## Anbennar-Specific Conventions

### Estate Integration
- Verne uses estates: `estate_adventurers`, `estate_nobles`, etc.
- Estate influence affects event triggers and mission conditions
- `estate_influence = { estate = estate_nobles influence = 80 }` — threshold check
- `has_estate_privilege = estate_nobles_ducal_muster` — privilege check
- `change_estate_land_share = { estate = estate_nobles share = -5 }` — land share

### Anbennar Religion System
- Corinite is the reformed religion (parallel to Protestantism)
- `is_religion_enabled = corinite` — check if reformation has started
- `change_religion = corinite` — convert provinces
- `has_personal_deity = corin` — Corinite deity mechanic

### Anbennar Institution System
- Standard EU4 institutions + Anbennar-specific ones
- `has_institution = renaissance` — standard check
- `add_institution_embracement = { which = renaissance value = 25 }` — province embracement
- `is_institution_enabled = renaissance` — check if institution is active

### Province ID Reference (Verne)
| ID | Province | Notes |
|----|----------|-------|
| 288 | Heartspier | Verne capital, port city |
| 291 | Calasandur | Secondary Verne province |

---

## Verne Overhaul Architecture

### Lane System
The Verne overhaul uses 8 mission lanes, each in a separate slot:
| Slot | Lane | Missions | Theme |
|------|------|----------|-------|
| 1 | Court & Oaths | 4 | Diplomatic/vassal system |
| 2 | Maritime Empire | 4 | Naval/trade |
| 3 | Dynastic Machine | 3 | Legitimacy/nobility |
| 4 | Trade & Colonisation | 3 | Overseas expansion |
| 5 | Red Court & Arcane | 3 | Magic/military |
| 6 | Legitimacy & Recognition | 3 | Institutional authority |
| 8 | Faith & Apostolic Empire | 3 | Religious diplomacy |

### Cross-Lane Gates
Missions reference flags from other lanes:
- `fleet_crimson_wake_complete` (Lane 2 → other lanes)
- `verne_dynasty_protected` (Lane 3 → Lane 6)
- `verne_census_established` (Lane 6 internal)
- `verne_corinite_founded` (Lane 8 internal)
- `verne_charter_unlocked` (Lane 4 internal)

### Event Namespaces
| Namespace | Purpose |
|-----------|---------|
| `verne` | Main flavour events (verne.1, verne.12, etc.) |
| `verne_overhaul_oaths` | Silver Oaths event chain |
| `verne_overhaul_dynasty` | Dynastic Safeguard event |
| `verne_overhaul_advisor` | Mage advisor recruitment |
| `verne_overhaul_crisis` | Crisis events |

### Modifier File
All custom modifiers defined in: `common/event_modifiers/verne_overhaul_modifiers.txt`
Naming convention: `verne_<lane>_<concept>` (e.g., `verne_dynasty_protected_court`)

---

## Tooltip Best Practices (Verne Mod)

### Rule #1: Show Numbers, Not Vague Words
❌ BAD: "Improves trade capabilities"
✅ GOOD: "+5% trade efficiency, +1 merchant"

❌ BAD: "Enhanced military power"
✅ GOOD: "+10% land morale, +0.5 army tradition/year"

### Rule #2: Track Hidden Variables
Verne uses several hidden tracking variables. ALWAYS expose them in tooltips:

```pdx
# In mission effect:
custom_tooltip = verne_overseas_proj_add_1_tt

# In localisation:
verne_overseas_proj_add_1_tt:0 "Overseas Projection: +1"
verne_overseas_proj_current_tt:0 "Current Overseas Projection: [See variable]"
verne_overseas_proj_tooltip_tt:0 "Gained through colonial missions and trade reforms. Unlocks bonuses at 3, 6, and 10."
```

### Rule #3: Explain Prerequisites Clearly
❌ BAD: "Locked" or "Requires previous mission"
✅ GOOD: "Requires: Reform X + 5 settled colonial provinces + Completion of Distant Horizons"

### Rule #4: Cross-Reference Systems
For complex mechanics, link to related content:
```
"This modifier is part of the Court & Oaths lane. See also: Formalize Silver Oaths, Royal Arbitration."
```

### Rule #5: Consistent Terminology
Pick ONE term per concept:
- "Overseas Projection" (not "colonial progress," "expansion reach," etc.)
- "Silver Oaths" (not "diplomatic pacts," "binding agreements")
- "Crimson Wake" (not "red fleet," "verne navy")

### Verne Tracking Variables (must always be visible)
| Variable | Where Set | Tooltip Location |
|----------|-----------|------------------|
| verne_overseas_projection | Lane 4 missions | Mission reward + decision tooltips |
| verne_world_network | Lane 4 mission 2 | Mission reward tooltip |
| verne_dynastic_magic_machine | Lane 3 mission 2 | Mission reward tooltip |

---

## Useful CLI Commands

```bash
# Check memory/index status
openclaw memory status

# Search modding knowledge
openclaw memory search "EU4 event syntax"

# Rebuild memory index after changes
openclaw memory index --force

# Git status in Anbennar repo
cd C:\Users\User\Documents\GitHub\My-Anbennar; git status

# Check subagent tasks
openclaw tasks list
openclaw tasks audit

# List hooks
openclaw hooks list
```

---

*This reference is a living document. The self-improving-agent promotes learnings here when patterns recur 3+ times.*
