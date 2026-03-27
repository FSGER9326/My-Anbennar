# Witch-King, Lichdom, War Wizard, and Magical Infamy Reference

This article documents the **implementation reality** of Anbennar's high-risk magical ruler pipeline.

It focuses on reusable mechanics and state handling, not on balance recommendations.

## Quick Verdict

This is a layered system, not a single event chain:

1. infamy state is tracked through variables and helper triggers
2. threshold helpers apply/remove modifiers and trigger witch-king transitions
3. lichdom and war wizard progression piggyback on the same ruler-magic framework
4. UI and decision entry points expose only part of the real logic

The safest adaptation pattern is to reuse helper effects/triggers, then attach tag content around them.

---

## What the system does

- Tracks ruler/heir/consort/country magical infamy levels.
- Converts threshold crossings into status bands (paragon/respected/suspicious/denounced/witch-king).
- Applies infamy modifiers and witch-king conversion effects.
- Supports war wizard conversion for ruler/heir and generated war wizards.
- Connects with lichdom pursuit state (`pursuing_lichdom`) and project/event content.

---

## Core files

| Area | File | Why it matters |
|---|---|---|
| Infamy + witch-king trigger layer | `common/scripted_triggers/anb_scripted_triggers_magic.txt` | Contains `type_has_infamy_*` thresholds and pseudonym trigger wrappers. |
| Conversion + infamy effect layer | `common/scripted_effects/anb_scripted_effects_for_magic_system.txt` | Contains `become_a_witch_king_effect`, infamy calculation helpers, and war wizard/infamy constructors. |
| Modifiers | `common/event_modifiers/anb_magic_modifiers.txt` | Defines infamy modifiers and war wizard stat packages. |
| Decision entry points | `decisions/MagicDecisions.txt` | Player-facing conversion and lichdom pursuit decisions. |
| Military custom GUI entry points | `common/custom_gui/countrymilitaryview.txt` | GUI button wrappers for ruler/heir war wizard conversion. |
| Magic menu infamy readout | `common/custom_gui/magic_menu.txt` + `interface/topbar.gui` | UI hooks for infamy labels/tooltips and witch-king visual assets. |
| Mission/event consumers | `missions/Black_Herd_Missions.txt`, `missions/Wyvernheart_Missions.txt`, `events/estate_mages.txt` (and others) | Concrete examples of consuming infamy/witch-king/lich checks in content branches. |

---

## Main objects and state

| Object type | Examples |
|---|---|
| Variables | `ruler_witch_king_points` and type-specific equivalents used by `type_has_infamy_*` checks. |
| Flags | `is_infamous_$type$`, plus project/nation flow flags. |
| Ruler modifier | `pursuing_lichdom` from `common/event_modifiers/anb_magic_modifiers.txt` and decision hooks. |
| Country/ruler modifiers | `infamy_respected_modifier`, `infamy_suspicious_modifier`, `infamy_denounced_modifier`; `ruler_war_wizard_*_mod`; `war_wizard_*_mod`. |
| Trigger wrappers | `ruler_has_infamy_denounced_or_worse`, `ruler_is_witch_king`, `ruler_is_lich`, `has_war_wizard`. |

---

## Step-by-step implementation model

### 1) Content calls helper effects rather than setting raw state ad hoc

Examples:

- Mission/decision/event content calls `increase_ruler_witch_king_points`, `become_a_witch_king_effect`, or war wizard conversion helpers.
- The helper layer in `anb_scripted_effects_for_magic_system.txt` performs canonical cleanup + recalculation.

### 2) Threshold checks are centralized in scripted triggers

`anb_scripted_triggers_magic.txt` defines:

- `type_has_infamy_witch_king`
- `type_has_infamy_denounced`
- `type_has_infamy_suspicious`
- `type_has_infamy_respected`
- `type_has_infamy_paragon`

Then wraps those into ruler/heir/consort/estate aliases.

### 3) Modifier and role transitions are recalculated

`calculate_magical_infamy_modifier`:

- strips old infamy modifiers
- reapplies modifier tier based on current thresholds
- escalates into `become_a_witch_king_effect` once witch-king threshold is reached

### 4) War wizard conversion uses effect constructors with stat tiers

The same helper file defines:

- `define_type_to_war_wizard_effect`
- `define_ruler_to_war_wizard`
- `define_heir_to_war_wizard`
- `create_war_wizard`
- `define_war_wizard`

This ensures consistent stat-package assignment via hidden country modifiers.

### 5) Lichdom pursuit starts as explicit state

`MagicDecisions.txt` adds ruler modifier `pursuing_lichdom` and hands off to the broader magic project/event layer.

---

## Real code examples

### Example A: Infamy threshold trigger family

From `common/scripted_triggers/anb_scripted_triggers_magic.txt`:

```txt
type_has_infamy_witch_king = { #16+ witch-king points = witch-king
	type_has_variable = {
		which = $type$_witch_king_points
		value = 16
	}
}

ruler_has_infamy_denounced_or_worse = { type_has_infamy_denounced_or_worse = { type = ruler } }
```

Why it matters: content files can stay readable by using alias triggers instead of repeating variable logic.

### Example B: Centralized infamy-to-status recalculation

From `common/scripted_effects/anb_scripted_effects_for_magic_system.txt`:

```txt
calculate_magical_infamy_modifier = {
	hidden_effect = {
		remove_country_modifier = infamy_denounced_modifier
		remove_country_modifier = infamy_suspicious_modifier
		remove_country_modifier = infamy_respected_modifier
	}
	if = {
		limit = { type_has_infamy_witch_king = { type = ruler } }
		become_a_witch_king_effect = yes
	}
}
```

Why it matters: this is the canonical "repair/rebuild" pass for visible status.

### Example C: Decision -> state handoff for lichdom pursuit

From `decisions/MagicDecisions.txt`:

```txt
NOT = { has_ruler_modifier = pursuing_lichdom }
...
add_ruler_modifier = { name = pursuing_lichdom duration = -1 desc = until_advancement_concludes }
```

Why it matters: lichdom isn't just a one-click reward; it starts a tracked progression state.

---

## Vanilla vs Anbennar difference notes

- Vanilla has no native "magical infamy" tier framework for rulers/heirs/consorts.
- Vanilla war wizard equivalents are far simpler; Anbennar uses custom constructors and stat packages.
- Witch-king and lichdom progression are integrated with scripted helper layers and mission/event consumers, not isolated per-tag events.

---

## Safe adaptation notes

- Prefer calling helper effects (`increase_*_witch_king_points`, `calculate_magical_infamy_modifier`, `define_*_to_war_wizard`) over direct variable editing.
- Use trigger aliases (`ruler_has_infamy_*`) in missions/events for readability and future compatibility.
- If adding a new high-magic path, verify infamy threshold assumptions with `type_has_infamy_*` first.
- Keep UI labels/tooltips synchronized if new infamy states are added (`magic_menu.txt`, `topbar.gui`, localisation).

---

## Suggested reuse cases

- Verne "court scandal" escalation tied to mage abuse risk.
- Dynastic magical legitimacy tracks that branch on infamy tiers.
- Alternative war wizard recruitment paths for doctrine/reform branches.
- Disaster pressure systems that read existing infamy/witch-king state instead of duplicating values.

---

## Related systems

- [magic-systems-reference.md](./magic-systems-reference.md)
- [powerful-mage-and-succession-reference.md](./powerful-mage-and-succession-reference.md)
- [magic-projects-reference.md](./magic-projects-reference.md)
- [artificery-research-and-inventions-reference.md](./artificery-research-and-inventions-reference.md)

Cross-layer links:

- Design: [../design/pressure-disasters-and-corinite.md](../design/pressure-disasters-and-corinite.md)
- Design: [../design/dynasty-and-court.md](../design/dynasty-and-court.md)
- Crosswalk: [../implementation-crosswalk.md](../implementation-crosswalk.md)
