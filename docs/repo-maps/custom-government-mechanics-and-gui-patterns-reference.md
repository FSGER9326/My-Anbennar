# Custom Government Mechanics and GUI Patterns Reference

This article maps reusable Anbennar patterns for **government mechanics that require custom GUI wiring**.

## Quick Verdict

Anbennar's government mechanics are a major reusable architecture family:

- mechanics are declared in `common/government_mechanics/*.txt`
- UI surfaces are declared in `interface/government_mechanics/*.gui` plus sprite sheets in `*.gfx`
- government reforms/missions/events activate or consume those mechanics

Treat each mechanic as a three-part bundle: **mechanic definition + GUI view + content hooks**.

---

## What the system does

- Defines custom power bars and interactions beyond vanilla defaults.
- Applies scaled/range modifiers based on power values.
- Exposes click interactions with costs, triggers, cooldowns, and effects.
- Enables tag-specific minigame systems without hardcoding everything into one event file.

---

## Core files

| Area | File | Why it matters |
|---|---|---|
| Syntax and engine contract | `common/government_mechanics/readme.txt` | Documents available keys (`powers`, `interactions`, `scaled_modifier`, etc.). |
| Example mechanic (simple reusable baseline) | `common/government_mechanics/anb_adventurer_unity.txt` | One-power + one-interaction implementation with custom GUI. |
| Example GUI for baseline | `interface/government_mechanics/adventurer_unity.gui` | Shows minimal custom interaction window and power bar. |
| Example mechanic (complex range/scaling) | `common/government_mechanics/anb_corinsfield_paranoia.txt` | Multi-range growth logic + interaction suite + event handoff. |
| Example GUI for complex case | `interface/government_mechanics/corinsfield_paranoia.gui` | Multiple button widgets and custom bar assets. |
| Shared icon atlas | `interface/government_mechanics/anb_government_mechanics.gfx` | Sprite binding for interaction icons and bars. |
| Activation consumers | `common/government_reforms/*.txt`, missions/events using mechanic triggers/effects | Attach mechanics to governments and narrative content. |

---

## Main objects and state

| Object | Notes |
|---|---|
| Mechanic ID | e.g. `anb_adventurer_unity`, `corinsfield_paranoia_mechanic`. |
| Power type ID | e.g. `adventurer_unity`, `corinsfield_paranoia_power`. |
| Interaction IDs | e.g. `promote_adventurer_unity`, `trust_no_one`, `commence_witch_trial`. |
| Power state | Handled via `has_government_power`, `add_government_power`, `set_government_power`. |
| UI link | `gui = <window_name>` on power or interaction, resolved in `interface/government_mechanics/*.gui`. |

---

## Step-by-step implementation model

### 1) Define mechanic contract

In `common/government_mechanics/<file>.txt`:

- create mechanic ID
- define `powers` with max/min/growth and scaling modifiers
- define `interactions` with costs/triggers/effects

### 2) Bind GUI windows

- For bars: set `gui` on power or rely on shared power display.
- For interactions: set `gui` per interaction when custom layout is needed.

### 3) Provide art/sprite wiring

- Register icons/sprites in `interface/government_mechanics/*.gfx`.
- Reference those `GFX_` names from interaction definitions.

### 4) Attach mechanic to governments/reforms/content

- Use government reform hooks and/or mission/event flow to ensure tags actually get and use the mechanic.

### 5) Add event handoff for complex interactions

- For nontrivial outcomes, interaction effects trigger events (example: Corinsfield witch trial event handoff).

---

## Real code examples

### Example A: Generic mechanic schema (engine-level)

From `common/government_mechanics/readme.txt`:

```txt
<government_mechanic_id> = {
	powers = {
		<government_power_type_id> = {
			max = <int>
			base_monthly_growth = <float>
			scaled_modifier = { ... }
		}
	}
	interactions = {
		<government_power_interaction_id> = {
			cost_type = <progress_type_id>
			effect = { ... }
		}
	}
}
```

Why it matters: this defines what is possible and should be treated as the contract layer.

### Example B: Adventurer unity as compact reusable pattern

From `common/government_mechanics/anb_adventurer_unity.txt`:

```txt
anb_adventurer_unity = {
	powers = {
		adventurer_unity = {
			max = 100
			reset_on_new_ruler = no
			scaled_modifier = {
				modifier = {
					global_tax_income = 27
					manpower_recovery_speed = 0.20
					land_maintenance_modifier = -0.20
				}
			}
		}
	}
}
```

Why it matters: demonstrates a low-complexity "single meter drives bonuses" model.

### Example C: Corinsfield paranoia with interaction -> event handoff

From `common/government_mechanics/anb_corinsfield_paranoia.txt`:

```txt
commence_witch_trial = {
	gui = corinsfield_paranoia_button
	trigger = {
		custom_trigger_tooltip = {
			tooltip = h35_paranoia_too_low
			has_government_power = {
				mechanic_type = corinsfield_paranoia_mechanic
				power_type = corinsfield_paranoia_power
				value = 20
			}
		}
	}
	effect = {
		add_adm_power = -20
		country_event = { id = flavour_corinsfield.36 }
	}
}
```

Why it matters: mechanics often dispatch into bespoke narrative systems instead of keeping all logic inline.

---

## Vanilla vs Anbennar difference notes

- Vanilla mechanics exist, but Anbennar massively expands count and specificity of government mechanics.
- Many Anbennar mechanics use custom GUI windows/assets instead of stock templates.
- Tag-specific political systems frequently use range/scaled modifier math plus custom interactions.

---

## Safe adaptation notes

- Start from an existing mechanic closest in complexity (adventurer unity for simple; paranoia for complex).
- Reuse existing trigger/effect primitives (`has_government_power`, `add_government_power`) rather than event-only pseudo systems.
- Keep GUI naming synchronized between mechanic definitions and `interface/government_mechanics/*.gui`.
- If adding a new Verne meter, prototype with one power + one interaction first, then expand.

---

## Suggested reuse cases

- Verne court authority/legitimacy pressure meter.
- Overseas expedition tempo meter.
- Corinite imperial integration pressure/actions.
- Wyvern command doctrine stance switching.

---

## Related systems

- [adventurer-systems-and-estate-patterns-reference.md](./adventurer-systems-and-estate-patterns-reference.md)
- [custom-estate-and-privilege-ecosystems-reference.md](./custom-estate-and-privilege-ecosystems-reference.md)
- [anbennar-systems-master-index.md](./anbennar-systems-master-index.md)

Cross-layer links:

- Design: [../design/reform-bible.md](../design/reform-bible.md)
- Design: [../design/pressure-disasters-and-corinite.md](../design/pressure-disasters-and-corinite.md)
- Crosswalk: [../implementation-crosswalk.md](../implementation-crosswalk.md)
