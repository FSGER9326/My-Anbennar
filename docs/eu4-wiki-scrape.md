# EU4 Modding Wiki Scrape

*Scraped from eu4.paradoxwikis.com on 2026-03-31*

---

## Effects

Effects are used in order to affect the game dynamically from within a specific scope.

### Dual scope

These effects can be used in either country or province scope.

- **set_global_flag** `<flag>` — Defines a global flag. Flags can be appended with scopes or event targets.
- **clr_global_flag** `<flag>` — Clears a defined global flag.
- **custom_tooltip** `<string>` — Displays a localized key in the effect tooltip.
- **log** `<string>` — Displays a string in the game.log when executed. Accepts all localization commands.
- **save_event_target_as** `<string>` — Saves the current scope as a key. Is cleared once execution ends.
- **save_global_event_target_as** `<string>` — Saves the current scope as a key. Persists after execution until cleared.
- **clear_global_event_target** `<string>` — Clears a specific global event target.
- **clear_global_event_targets** `yes` — Clears all global event targets.
- **show_ambient_object** `<string>` — Displays a hidden ambient object.
- **hide_ambient_object** `<string>` — Hides a visible ambient object.
- **enable_council** `yes` — Starts the Council of Trent.
- **finish_council** `yes` — Ends the Council of Trent.

### Country scope — General

- **country_event** — Fires a country event. Parameters: `id`, `days`, `random`, `tooltip`.
- **add_country_modifier** — Adds an event modifier. Parameters: `name`, `duration` (-1 = forever), `hidden`, `desc`.
- **extend_country_modifier** — Extends an existing event modifier for specified duration.
- **remove_country_modifier** `<modifier>` — Removes an already assigned country modifier.
- **set_country_flag** `<flag>` / **clr_country_flag** `<flag>` — Define/clear country flags.
- **change_tag** `<scope>` — Changes current scope to a tag.
- **switch_tag** `<scope>` — Switches player view to a tag. Original country becomes AI-controlled.
- **change_graphical_culture** `<gfxculture>` — Changes graphical culture.
- **override_country_name** `<string>` — Changes country name.
- **restore_country_name** `yes` — Restores original country name.
- **change_country_color** — Changes country color. Parameters: `color = { R G B }` or `country = <scope>`.
- **restore_country_color** `yes` — Restores original country color.
- **add_adm_power** `<int>` — Adds administrative power.
- **add_dip_power** `<int>` — Adds diplomatic power.
- **add_mil_power** `<int>` — Adds military power.
- **set_saved_name** — Saves a name for use in other effects. Parameters: `key`, `type`, `name`, `scope`.
- **clear_saved_name** `<key>` — Clears a saved name key.
- **change_innovativeness** `<int>` — Adds innovativeness. Range [0, 100].
- **complete_mission** `<key>` — Marks a mission as completed (no rewards given).
- **swap_non_generic_missions** `yes` — Reloads the mission tree.
- **adm_power_cost** / **dip_power_cost** / **mil_power_cost** `<int>` — Scales with power cost modifier, then subtracts.
- **remove_country** `yes` — Removes the current country from existence.
- **play_sound** `<identifier>` — Plays a sound file.

### Country scope — Economy

- **add_years_of_income** `<float>` — Adds ducats equal to years of income.
- **add_treasury** `<int>` — Adds ducats directly.
- **add_inflation** `<float>` — Adds inflation.
- **add_mercantilism** `<int>` — Adds mercantilism.
- **add_owned_provinces_development_ducats** — Adds money scaling with province development. Parameters: `multiplier`, `age_multiplier`, `trigger`, `custom_tooltip`.
- **add_owned_provinces_development_manpower** — Same as above but for manpower.
- **add_tariff_value** `<float>` — Adds tariff value (ducat flow from subjects).
- **loan_size** `<unsigned char>` — Changes the loan size.
- **change_price** — Changes the price of a trade good globally. Parameters: `trade_goods`, `key`, `value`, `duration`.
- **add_loan** — Takes a loan. Parameters: `interest_modifier`, `fixed_interest`, `duration`.
- **raise_war_taxes** `yes` — Raises war taxes without spending military power.
- **add_years_of_owned_provinces_production_income** — Adds production income scaling with provinces.

---

## Triggers

Triggers are used in order to execute effects only when certain conditions are true. The AND operator is the default.

### Base value/identifier triggers

- **`<advisor>`** `<int>` — Country has hired an advisor of specified type with at least level X.
- **`<building>`** `<int>` — Country has at least X buildings of specified type.
- **`<idea group>`** `<int>` — Country has at least X ideas from specified idea group.
- **`<institution>`** `<int>` — Province has at least X support for specified institution.
- **`<religion>`** `<int>` — Country has tolerance of at least X for specified religion.
- **`<subject_type>`** `<int>` — Country has at least X subjects of given type.
- **`<trade good>`** `<int>` — Country has at least X provinces producing specified trade good.

### Key triggers

- **absolutism** `<int>` — Country has at least X absolutism.
- **accepted_culture** `<identifier>` — Country accepts specified culture.
- **adm** `<int>` — Ruler has admin skill of at least X.
- **adm_power** `<int>` — Country has at least X admin power.
- **adm_tech** `<int>` — Country has admin tech of at least X.
- **advisor** `<identifier>` — Country has an advisor of specified type.
- **advisor_exists** `<id>` — Advisor X exists.
- **ai** `yes/no` — Country is AI-controlled.
- **ai_attitude** — Country has specified attitude towards another country.
- **all_regiments_morale_percent** `<float>` — All regiments have morale ≥ X%.
- **alliance_with** `<tag>` — Country has alliance with X.
- **allows_female_emperor** `yes/no` — Females can become emperor.
- **always** `yes/no` — Always true or always false.
- **area** `<identifier>` — Province is part of area X.
- **army_size** `<int>` — Country has army of at least X k soldiers.
- **army_size_percentage** `<float>` — Army size ≥ X% of land force limit.
- **army_strength** — Country's army strength is at least X times that of another country.
- **army_professionalism** `<float>` — Army professionalism ≥ X.
- **army_tradition** `<int>` — Army tradition ≥ X.
- **artillery_fraction** `<float>` — Ratio of artillery to army size ≥ X.
- **artillery_in_province** `<int>` — At least X artillery units in province.
- **at_war_with_religious_enemy** `yes/no` — At war with different-religion country.
- **authority** `<int>` — Inti country has at least X authority.
- **average_autonomy** `<int>` — Average autonomy ≥ X.
- **average_unrest** `<int>` — Average unrest ≥ X.
- **base_manpower** / **base_production** / **base_tax** `<int>` — Province dev component ≥ X.
- **blockade** `<float>` — Blockade penalty ≥ X%.
- **border_distance** — Distance between borders ≥ X.
- **calc_true_if** — Returns true if at least N sub-triggers are true.
- **can_be_overlord** — Country meets conditions for subject type's is_potential_overlord.
- **can_build** `<identifier>` — Specified building can be built in province.
- **can_create_vassals** `yes` — Country can create a vassal.
- **can_spawn_rebels** `<identifier>` — Rebel faction is valid for province.
- **capital** `<province_id>` — Country's capital is province X.
- **capital_distance** — Distance between capitals ≥ X.
- **cavalry_fraction** `<float>` — Cavalry fraction ratio ≥ X.
- **province_has_center_of_trade_of_level** `<int>` — Province has CoT ≥ level X.
- **check_variable** — Variable ≥ value X.
- **church_power** `<int>` — Church power ≥ X.
- **coalition_target** `<tag>` — Country is target of coalition.
- **colonial_region** `<identifier>` — Province is in colonial region X.
- **colony** `<int>` — Country has at least X colonial subjects.
- **colonysize** `<int>` — Colony is at least size X.
- **consort_adm/dip/mil** `<int>` — Consort skill ≥ X.
- **consort_age** `<int>` — Consort age ≥ X.
- **consort_culture/religion** — Consort has specified culture/religion.
- **consort_has_personality** `<id>` — Consort has specified personality.
- **construction_progress** `<float>` — Construction progress ≥ X%.
- **continent** `<identifier>` — Province is on continent X.
- **controlled_by** `<tag>` — Province controlled by X.
- **controls** `<province_id>` — Country controls province X.
- **claim** `<tag>` — Country has claim on province.

---

## Modifier list

A modifier is a value that affects various attributes of a country or province. All modifiers are sorted into country or province scope. All modifiers stack additively.

### Military — Country modifiers

| Modifier | Example | Description | Effect type |
|---|---|---|---|
| army_tradition | 1 | Rate of army tradition gain per year | Additive |
| army_tradition_decay | -0.01 | Decay rate of army tradition | Additive |
| army_tradition_from_battle | 0.01 | Tradition bonus from battles | Multiplicative |
| yearly_army_professionalism | 0.01 | Rate of professionalism gain per year | Multiplicative |
| drill_gain_modifier | 0.10 | Army drill gains while drilling | Multiplicative |
| drill_decay_modifier | -0.10 | Army drill decay rate per year | Multiplicative |
| infantry_cost | -0.10 | Base cost of infantry | Multiplicative |
| infantry_power | 0.10 | Power infantry gain from unit pips | Multiplicative |
| infantry_fire | 1 | Infantry fire phase damage multiplier | Additive |
| infantry_shock | 1 | Infantry shock phase damage multiplier | Additive |
| cavalry_cost | -0.10 | Base cost of cavalry | Multiplicative |
| cavalry_power | 0.10 | Power cavalry gain from unit pips | Multiplicative |
| cavalry_fire | 1 | Cavalry fire phase damage multiplier | Additive |
| cavalry_shock | 1 | Cavalry shock phase damage multiplier | Additive |
| artillery_cost | -0.10 | Base cost of artillery | Multiplicative |
| artillery_power | 0.10 | Power artillery gain from unit pips | Multiplicative |
| artillery_fire | 1 | Artillery fire phase damage multiplier | Additive |
| artillery_shock | 1 | Artillery shock phase damage multiplier | Additive |
| cav_to_inf_ratio | 0.10 | Ratio for insufficient support penalty | Additive |
| cavalry_flanking | 0.10 | Cavalry flanking effectiveness | Multiplicative |
| artillery_levels_available_vs_fort | 1 | Max artillery levels on siege | Additive |
| artillery_level_modifier | 1 | How much artillery contributes to siege | Multiplicative |
| backrow_artillery_damage | 0.10 | Bonus backrow artillery damage | Multiplicative |
| discipline | 0.01 | Land unit discipline | Multiplicative |
| land_morale | 0.10 | Land unit morale | Multiplicative |
| land_morale_constant | 0.1 | Land unit morale (additive) | Additive |
| movement_speed | 0.10 | Base movement speed for land units | Multiplicative |
| fire_damage | 0.10 | Fire damage done | Multiplicative |
| fire_damage_received | -0.10 | Fire damage taken | Multiplicative |
| shock_damage | 0.10 | Shock damage done | Multiplicative |
| shock_damage_received | -0.10 | Shock damage taken | Multiplicative |
| morale_damage | 0.025 | Morale damage done | Multiplicative |
| morale_damage_received | -0.025 | Morale damage taken | Multiplicative |
| recover_army_morale_speed | 0.10 | Army morale recovery speed | Multiplicative |
| reserves_organisation | 0.10 | Morale damage by reserves | Multiplicative |
| land_attrition | -0.10 | Land unit attrition | Multiplicative |
| reinforce_cost_modifier | -0.10 | Cost of reinforcements | Multiplicative |
| no_cost_for_reinforcing | yes | Free reinforcement | Constant |
| reinforce_speed | 0.10 | Reinforcement rate | Multiplicative |
| manpower_recovery_speed | 0.10 | Manpower recovery rate | Multiplicative |
| global_manpower | 1 | Adds to total manpower pool (1=1000) | Additive |
| global_manpower_modifier | 0.10 | Modifies total manpower pool | Multiplicative |
| global_regiment_cost | -0.10 | Base unit cost for all land units | Multiplicative |
| global_regiment_recruit_speed | -0.10 | Land unit recruitment speed | Multiplicative |
| global_supply_limit_modifier | 0.10 | Supply limit of provinces | Additive |
| land_forcelimit | 1 | Adds to force limit | Additive |
| land_forcelimit_modifier | 0.10 | Modifies force limit | Multiplicative |
| land_maintenance_modifier | -0.10 | Maintenance cost of land units | Multiplicative |
| possible_condottieri | 1 | Base condottieri limit | Multiplicative |
| hostile_attrition | 1 | Attrition enemies take in provinces | Additive |
| max_hostile_attrition | 3 | Max attrition for enemies | Additive |
| siege_ability | 0.10 | Siege phase length (inverse of defensiveness) | Multiplicative |
| artillery_barrage_cost | -0.25 | Cost for Artillery Barrage | Multiplicative |
| assault_fort_cost_modifier | -0.25 | Military cost to assault forts | Multiplicative |
| assault_fort_ability | 0.25 | Damage to garrison when assaulting | Multiplicative |
| defensiveness | 0.10 | Siege defensiveness | Multiplicative |
| garrison_size | 0.10 | Base garrison size | Multiplicative |
| global_garrison_growth | 0.10 | Base garrison growth | Multiplicative |
| garrison_damage | 0.5 | Damage garrison deals on assault/sortie | Multiplicative |
| fort_maintenance_modifier | -0.10 | Base fort maintenance | Multiplicative |
| rival_border_fort_maintenance | -0.10 | Fort maintenance bordering rivals | Multiplicative |
| war_exhaustion | -0.10 | Monthly war exhaustion rate | Additive |
| war_exhaustion_cost | -0.10 | Dip power cost to reduce war exhaustion | Multiplicative |
| leader_land_fire | 1 | Min fire pips for generated leaders | Additive |
| leader_land_manuever | 1 | Min maneuver pips for leaders | Additive |
| leader_land_shock | 1 | Min shock pips for leaders | Additive |
| leader_siege | 1 | Min siege pips for leaders | Additive |
| max_general_fire/shock/maneuver/siege | 1 | Max pips for leaders | Additive |
| general_cost | -0.10 | Mil power cost for generals | Multiplicative |
| free_leader_pool | 1 | Max free leaders (land+navy) | Additive |
| free_land_leader_pool | 1 | Max free land leaders | Additive |
| free_navy_leader_pool | 1 | Max free navy leaders | Additive |
| raze_power_gain | 0.10 | Monarch power from razing | Multiplicative |
| loot_amount | 0.10 | Loot taken during looting | Multiplicative |
| available_province_loot | 0.10 | Loot available in province | Multiplicative |
| prestige_from_land | 0.10 | Prestige from combat | Multiplicative |
| war_taxes_cost_modifier | -0.10 | Mil power cost for war taxes | Multiplicative |
| leader_cost | -0.10 | Mil power cost for hiring leaders | Multiplicative |
| may_recruit_female_generals | yes | Allows female generals | Constant |
| manpower_in_true_faith_provinces | 0.10 | Manpower from true faith provinces | Multiplicative |
| regiment_manpower_usage | -0.1 | Manpower usage by regiments | Multiplicative |
| military_tactics | 0.25 | Military tactics (damage reduction) | Additive |
| capped_by_forcelimit | yes | Forbids going over forcelimit | Constant |
| global_attacker_dice_roll_bonus | 1 | Global attacker dice bonus | Additive |
| global_defender_dice_roll_bonus | 1 | Global defender dice bonus | Additive |
| own_territory_dice_roll_bonus | 1 | Dice roll bonus for territory owner | Additive |
| manpower_in_accepted_culture_provinces | 0.10 | Manpower in accepted culture provinces | Multiplicative |
| manpower_in_culture_group_provinces | 0.1 | Manpower in culture group provinces | Multiplicative |
| manpower_in_own_culture_provinces | 0.10 | Manpower in own culture provinces | Multiplicative |
| may_build_supply_depot | yes | Allows supply depots | Constant |
| may_refill_garrison | yes | Allows refilling garrisons | Constant |
| may_return_manpower_on_disband | yes | Manpower returned on disband | Constant |

*(Note: Full modifier list includes many more country and province modifiers — economy, diplomacy, religion, etc. See wiki for complete list.)*

---

## Scopes

A scope is the context that triggers and effects are used in. All script scopes operate on either country or province internal scope.

### Dynamic scopes

| Scope | Description |
|---|---|
| ROOT | The base scope (e.g., country that event fires for) |
| FROM | The calling scope (e.g., ROOT of event that called this one) |
| PREV | The previous scope (one level up) |
| THIS | The current scope (only works as effect target) |

### Logic scopes

- **AND** — Groups triggers; returns true if ALL nested triggers return true. Default scope, usually implicit.
- **OR** — Returns true if ANY nested trigger returns true.
- **NOT** — Inverts truth value. Multiple conditions in one NOT = multiple NOTs combined with AND.
- **implication** — No direct scope. Encode as `NOT P OR Q` with OR and NOT.

### Subscope prefixes

| Prefix | Type | Description |
|---|---|---|
| `all_<scope>` | Trigger | Requires valid trigger for ALL subscopes |
| `any_<scope>` | Trigger | Requires valid trigger for ONE subscope |
| `every_<scope>` | Effect | Applies effects to ALL subscopes |
| `random_<scope>` | Effect | Applies effects to ONE random subscope |

All effect scopes can nest `limit = { }` to filter subscopes.

### Country and Province scopes

| Scope | Example | Changes to | Multiple? |
|---|---|---|---|
| `<province id>` | `110 = { }` | Province | No |
| `<tag>` | `FRA = { }` | Country | No |
| `<area>` | `western_mediterrenean_area = { }` | Province | Yes |
| `<region>` | `france_region = { }` | Province | Yes |
| `<superregion>` | `india_superregion = { }` | Province | Yes |
| `<continent>` | `europe = { }` | Province | Yes |
| `<trade_company>` | `trade_company_west_africa = { }` | Province | Yes |
| `<colonial_region>` | `colonial_alaska = { }` | Province | Yes |
| `<event_target>` | `event_target:name = { }` | Any | Yes |
| `emperor` | `emperor = { }` | Country | No |
| `revolution_target` | `revolution_target = { }` | Country | No |
| `crusade_target` | `crusade_target = { }` | Country | No |
| `papal_controller` | `papal_controller = { }` | Country | No |

### Country scopes

| Scope | Changes to |
|---|---|
| `colonial_parent` | Country |
| `overlord` | Country |
| `capital_scope` | Province |

### Province scopes

| Scope | Changes to |
|---|---|
| `owner` | Country |
| `controller` | Country |
| `sea_zone` | Province |
| `tribal_owner` | Country |

### Trade node scopes

| Scope | Description |
|---|---|
| `most_province_trade_power` | Country with most provincial trade power |
| `strongest_trade_power` | Country with most total trade power |

### Effect scopes (country)

| Scope | Description | Multiple? |
|---|---|---|
| `every_ally` | All allies | Yes |
| `every_coalition_member` | All coalition members | Yes |
| `every_country` | All countries in the world | Yes |
| `every_country_including_inactive` | All tags, even inactive | Yes |
| `every_elector` | All HRE electors | Yes |
| `every_enemy_country` | All countries that rivaled this one | Yes |
| `every_known_country` | All discovered countries | Yes |
| `every_neighbor_country` | All land/strait border neighbors | Yes |
| `every_rival_country` | All rivaled countries | Yes |
| `every_subject_country` | All subjects | Yes |
| `every_war_enemy_country` | All war enemies | Yes |
| `every_federation_member` | All federation members | Yes |
| `random_ally` | One random ally | No |
| `random_country` | One random country | No |
| `random_elector` | One random elector | No |
| `random_enemy_country` | One random enemy | No |

*(Plus many more random_* variants matching every_* equivalents)*

---

## Variables

Variables (in EU4) are persistent values associated with a specific country or province. They are fixed-point decimals (precise to nearest thousandth). Max value before overflow: ~2,147,484.

### Setup

```pdl
set_variable = {
    which = myCountingVariable
    value = 0
}
```

### Operations

| Effect | Description |
|---|---|
| `change_variable` | Add |
| `subtract_variable` | Subtract |
| `divide_variable` | Divide |
| `multiply_variable` | Multiply |
| `round_variable` | Round (value < 0 down, = 0 round, > 0 up) |
| `sqrt_variable` | Square root |
| `random_variable` | Random float between 0 and value |
| `modulo_variable` | Remainder |
| `export_to_variable` | Export game value to variable |
| `set_variable` | Set (also copies from another var with `which`) |

### Triggers

```pdl
check_variable = {
    which = myVar
    value = 5        # myVar >= 5
    # or
    which = otherVar  # myVar >= otherVar
}

is_variable_equal = {
    which = var1
    which = var2
}
```

### Export to variable

```pdl
export_to_variable = {
    which = moneyToGive
    value = monthly_income
    who = ROOT
}

# Export trigger values:
export_to_variable = {
    variable_name = my_age
    value = trigger_value:ruler_age
}
```

### Variable arithmetic trigger

Used within trigger scopes to compare exported values:

```pdl
variable_arithmetic_trigger = {
    custom_tooltip = <string>
    export_to_variable = { variable_name = my_age value = trigger_value:ruler_age }
    export_to_variable = { variable_name = their_age value = trigger_value:heir_age who = FROM }
    check_variable = { which = my_age which = their_age }
}
```

### Event scope values

Variables exported for culture/religion become index values. Use `variable:` syntax:

```pdl
set_heir_culture = variable:myVarName
any_owned_province = { culture = variable:From::myVarName }
religion_group = new_variable:ruler_religion
```

Supported effects: `change_religion`, `change_culture`, `change_primary_culture`, `set_ruler_culture`, `set_ruler_religion`, `set_consort_culture`, `set_consort_religion`, `set_heir_culture`, `set_heir_religion`

Supported triggers: `ruler_culture`, `consort_culture`, `heir_culture`, `ruler_religion`, `consort_religion`, `heir_religion`, `culture`, `religion`

### Exportable values (country)

`prestige`, `war_exhaustion`, `corruption`, `stability`, `treasury`, `mercantilism`, `inflation`, `num_of_cities`, `num_of_ports`, `adm_tech`, `dip_tech`, `mil_tech`, `years_of_income`, `monthly_income`, `trade_income_percentage`, `states_development`, `total_development`, `average_autonomy`, `average_home_autonomy`, `manpower`, `manpower_percentage`, `max_manpower`, `land_forcelimit`, `naval_forcelimit`, `army_tradition`, `navy_tradition`, `army_size`, `navy_size`, `average_unrest`, `average_autonomy_above_min`, `average_effective_unrest`, `num_of_rebel_armies`, `num_of_rebel_controlled_provinces`, `overextension_percentage`, `ADM`, `DIP`, `MIL`, `consort_adm/dip/mil`, `heir_adm/dip/mil`, `monarch_age`, `consort_age`, `heir_age`, `patriarch_authority`, `piety`, `religious_unity`, `tolerance_to_this`, `religion`, `dominant_religion`, `secondary_religion`, `ruler_religion`, `heir_religion`, `consort_religion`

Also: `modifier:<country_modifier>` for any country modifier, `trigger_value:<trigger>` for integer/float/boolean triggers.

---

## Events

Events occur throughout gameplay. They take the form of pop-up notifications.

### Triggered-only events

Events that occur as a result of a nation's actions. Usually fired immediately or shortly after being triggered.

### Pulse events

Random events in regular intervals. Grouped into sets with weights. Higher weights = higher chance.

**Date calculations:**
- Yearly pulses: each year
- 2-year pulses: years divisible by 2
- 3-year pulses: years divisible by 3
- 4/5-year pulses: depend on tag order id

Pulse day formula: `(year + tag_order_id + pulse_offset) mod 365`

**Pulse offsets:**
| Pulse | Offset |
|---|---|
| yearly I | 0 |
| yearly II | 30 |
| yearly III | 60 |
| yearly IV | 90 |
| yearly V | 120 |
| 2yr I | 69 |
| 2yr II | 99 |
| 2yr III | 129 |
| 2yr IV | 159 |
| 2yr V | 189 |
| 3yr I | 94 |
| 3yr II | 124 |
| 3yr III | 154 |
| 3yr IV | 184 |
| 4yr I | 130 |
| 4yr II | 160 |
| 4yr III | 190 |
| 4yr IV | 220 |
| 5yr I | 167 |
| 5yr II | 197 |
| 5yr III | 227 |
| 5yr IV | 257 |

Monthly pulse (mods only): day = `(year * 12 + month + tag_order_id) mod days_in_month`

### Mean time to happen (MTTH)

Events with a chance of happening when conditions are met. MTTH is the median time (half-life), not the mean.

Probability per check (every 20 days): `1 - 2^(-t_c / t_half)`

Mean = median / ln(2) ≈ 1.44 × median

Ideal probability: `1 - 2^(-t / t_half)` or equivalently `1 - e^(-t / mean)`

---

## Localization

Localisation files link in-code names to display text. Format is YAML-like.

### File format

```yaml
l_english:
 MY_KEY:0 "Display text"
 ANOTHER_KEY:0 "Another text"
```

**Rules:**
- Files must be in `localisation/` folder (not `localization`)
- Override vanilla with files in `localisation/replace/`
- Filename must end with `_l_english.yml`
- File must be UTF-8 with BOM
- First line must be `l_english:`
- Key characters: A-Z, a-z, 0-9, `_`, `.`, `-`
- Format: `KEY:version "text"` (version is optional number, no functional meaning)
- Newlines in text: `\n`, backslashes: `\\`
- `#` outside quotes = comment

### Text formatting

Use `§` followed by formatting rules, end with `§!`

**Colors:** W=White, B=Blue, G=Green, R=Red, b=Black, g=Grey, Y=Yellow, M=Marine, T=Teal, O=Orange, l=Lime, J=Jade, P=Purple, V=Violet

**Value formatting:**
| Code | Effect | Example |
|---|---|---|
| `%` | To percent | `$VAL\|%$!` → 0.5 → 50% |
| `*` | SI units | `$VAL\|*$!` → 1000 → 1K |
| `=` | Prepend +/- | `$VAL\|=$!` → 10 → +10 |
| `0-9` | Decimals | `$VAL\|3$!` → 10.12345 → 10.123 |
| `+` | Green/positive, yellow/zero, red/negative | `$VAL\|+$!` |
| `-` | Red/positive, yellow/zero, green/negative | `$VAL\|-$!` |

### Bracket commands (localisation scopes)

```
[Root.GetAdjective]          → Country adjective
[FRA.Monarch.GetTitle]       → Ruler title
[From.From.From.Owner.Monarch.GetHerHim]  → Stacked From scopes
```

**Key scopes:** Capital, ColonialParent, Culture, Dynasty, Emperor, From, Heir, Location, Monarch, Consort, Overlord, Owner, Religion, Root, This, Prev, TradeCompany, Dip_Advisor, Adm_Advisor, Mil_Advisor, `<event_target>`

**Key commands:** GetAreaName, GetRegionName, GetContinentName, GetSuperRegionName, GetAdjective, GetAdm/Dip/Mil, GetCapitalName, GetDate, GetFlagshipName, GetGroupName, GetHerHim/HerHis/HerselfHimself/SheHe (+Cap variants), GetSisterBrother, GetMonth, GetName, GetValue, GetTag, GetTitle, GetTradeGoodsName, GetWomanMan, GetYear, GovernmentName

**@TAG** — Displays country flag: `@[Root.GetTag]`

**Legacy keys:** `$COUNTRY$`, `$CAPITAL$`, `$MONARCH$`, `$HEIR$`, `$CULTURE$`, `$RELIGION$`, `$DYNASTY$`, `$DATE$`, `$OVERLORD$`, etc.

---

## Modifier modding

There are several types of modifiers, modded in different ways.

### Static modifiers
Applied when specific internally-coded events occur. Can't add new ones, only change their effects.
- Location: `/common/static_modifiers/*.txt`
- Example: `absolutism = { administrative_efficiency = 0.4 discipline = 0.05 }`

### Timed modifiers
Applied to subjects when specific actions are taken. Can't add new ones.
- Location: `/common/timed_modifiers/*.txt`
- Example: `place_relative_on_throne_not_regency = { liberty_desire = { value = 25 yearly_decay = 1 } }`

### Opinion modifiers
Define opinion changes (amount, duration, max). Applied internally or via `add_opinion`.
- Location: `/common/opinion_modifiers/*.txt`
- Parameters: `opinion`, `min`, `max`, `max_vassal`, `max_in_other_direction`, `yearly_decay`, `months`

### Event modifiers
Most widely used. Applied via `add_country_modifier` or `add_province_modifier`.
- Location: `/common/event_modifiers/*.txt`
- Can specify `picture = "icon_name"` for custom icon
- Description: `desc_<name>: "Description"`
- Icons in: `/gfx/interface/ideas_EU4/`

### Trade modifiers
Alter trade power in a specific trade node. Added with `add_trade_modifier` in trade node province scope.
- Parameters: `who`, `duration`, `power`, `key`

### Triggered modifiers
Dynamic modifiers that apply when trigger conditions are met. Evaluate for every country every monthly tick — use sparingly!
- Location: `/common/triggered_modifiers/*.txt`
- Structure:
```pdl
<name> = {
    potential = { <triggers> }  # visibility
    trigger = { <triggers> }    # activation
    <modifiers>                 # effects
}
```

### Province triggered modifiers
Operate directly with provinces. Applied with `add_province_triggered_modifier`.
- Location: `/common/province_triggered_modifiers/*.txt`
- Additional: `on_activation = { }`, `on_deactivation = { }`, `hidden = yes`

---

## Triggered modifiers

Triggered modifiers apply automatically whenever conditions are met. They are always active (unlike events) and don't require player action.

### Key triggered modifiers in vanilla:

- **East Indian Trade Route** — Non-Asian country with exploration ideas, ports, and trade presence in Indian Ocean nodes. +5% Trade efficiency.
- **Custodian of the Holy Cities** — Muslim country that owns Mecca and Medina. +0.5 yearly legitimacy, +1 missionary.
- **Subjugation of the Papacy** — Catholic overlord of Papal States. -2 diplomatic reputation.
- **Rapid Collapse of Society** — New World country without Feudalism hit by European diseases. +33% power costs, -10% discipline, -20% land morale.
- **Submission to the Emperor** — Latin culture in HRE after Shadow Kingdom (before 1550). +3 national unrest, +10% stab cost, -1 prestige.
- **Counter Revolution** — Monarchy near revolution target (not at war). -5 prestige, +30% stab cost, +5 unrest.
- **Reaction** — Monarchy at war with revolution target. +10 prestige, -10% stab cost, -10 unrest.
- **Crusade** — Catholic at war with crusade target controlling provinces. +30% manpower, +10% tax, +10% morale, +1 prestige, +1 papal influence.
- **Excommunication** — Excommunicated Catholic. -2 prestige, -10 papal influence, -5 devotion, -3 tolerance.
- **The Pentarchy** — Orthodox owning all 5 holy cities. +0.5 prestige, +1 missionary.
- **The Mandate of Heaven** — Celestial Empire with ≥20 cities, stability ≥0, legitimacy ≥60 (without DLC). -10% stab cost, -5 unrest.
- **The Mandate of Heaven Lost** — Celestial Empire failing conditions. -10% discipline, +50% stab cost, +10 unrest.
- **Catholic/Protestant/Reformed/Hussite Empire** — Correct faith dominant in HRE. +0.25 legitimacy, +1 tolerance, +1% missionary strength, +25% imperial authority.
- **The Golden Age of Piracy** — After Golden Age of Piracy event, with privateers in Caribbean. +20% privateer efficiency.
- **Pope of the Empire** — Papal State joined HRE, non-HRE Catholic. Various effects.
- **Robot Parts** — After defeating Synthetics. -25% technology cost.

---

## Static modifiers

Static modifiers are fixed modifiers used within the game (verified for version 1.37).

### Difficulty modifiers

**Player (Very Easy):** +50% manpower modifier/recovery/force limits, +50% production efficiency, +60 yearly tax, -33% regiment/ship cost, -0.05 inflation, -5 unrest, -0.05 war exhaustion, -25% core creation, +1 possible advisor/diplomatic relation/free leader, +2 dip rep, -2 interest, +10% improve relations, -33% AE, -1 corruption

**Player (Easy):** +50% manpower recovery, -5 unrest, -2 interest, -33% AE, -1 corruption

**Player (Hard):** *(Empty — no modifiers)*

**Player (Very Hard):** *(Empty — no modifiers)*

**AI (Very Hard):** +50% manpower/force limits/recovery, -33% regiment/ship cost, -0.05 inflation, -2 unrest, -0.05 war exhaustion, -25% core creation/idea cost, -1 interest, +50% improve relations, -20% dev cost, -25% construction cost, -33% AE, -30% missionary maintenance

**AI (Hard):** +50% manpower recovery, -1 unrest, -0.05 war exhaustion, -1 interest, -33% AE, -15% missionary maintenance

### Provincial static modifiers

- **City:** +25% local tax, +2 possible buildings, +25% local sailors, +5% garrison growth, +1 possible manufactory
- **State:** +10% institution spread
- **Capital State:** +5% institution spread, -50% state maintenance, -100% governing cost
- **Seat in Parliament:** +10% local manpower/sailors, +15% local tax, +10% local production efficiency
- **Coastal Sea:** -20% local naval engagement
- **Tropical:** -10 settler increase, -30% supply limit, +2 enemy attrition, +5% dev cost
- **Arctic:** -10 settler increase, -40% supply limit, +1 enemy attrition, -1 possible building, +50% dev cost
- **Arid:** -10 settler increase, -20% supply limit, +1 enemy attrition, +10% dev cost
- **Blockaded:** +20% recruitment/shipbuilding time, +0.25 monthly devastation, -100% local trade power
- **No Adjacent Controlled:** -5 local settler increase

### Per point of development

- **Tax:** -2% recruitment time, -1% great project upgrade time, -1% construction time, +2% institution spread
- **Manpower:** +1% garrison growth
- **General:** +0.1 possible buildings, +2% supply limit, -0.1% local missionary strength, +0.1 land/naval force limit, +60 sailors, +0.2 local trade power

### Development scaled

+3% local development cost per point above 19 (before modifiers).

### Capital City

+1 fort level

### Pasha (in state)

-20% governing cost, +20% minimum autonomy, -33% state maintenance, -0.1% monthly autonomy, +10 local heathen tolerance

---

*Note: All content was truncated to ~15,000 characters per page where applicable. For full details, see the original wiki pages at https://eu4.paradoxwikis.com/*
