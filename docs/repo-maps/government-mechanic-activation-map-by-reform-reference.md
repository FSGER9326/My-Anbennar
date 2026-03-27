# Government Mechanic Activation Map by Reform (Anbennar vs Vanilla Baseline)

## Quick verdict

Anbennar uses vanilla-capable government-mechanic scripting, but at much higher scale and with far deeper nation-specific branching.

The key non-vanilla difference is not engine syntax; it is **content architecture density**:

- many custom mechanics are activated through custom reforms
- a single mechanic may be reused across multiple government types
- mechanics often cross-link to magic, estates, and bespoke GUI/event layers

Status: **IMPLEMENTATION_READY** as an implementation pattern map.

## What the system does

This map documents how government mechanics are attached through `government_abilities` in reform files and then implemented in `common/government_mechanics/*.txt`.

It is designed to answer:

1. where activation happens
2. where mechanic logic lives
3. which mechanics are reused vs one-off
4. what is Anbennar-specific versus vanilla baseline behavior

## Core files

| Area | File | Role |
|---|---|---|
| Engine contract and syntax comments | `common/government_mechanics/readme.txt` | Canonical key list for `powers`, `interactions`, growth, and modifiers. |
| Reform activation layer (monarchies) | `common/government_reforms/01_government_reforms_monarchies.txt` | Activates mechanics like `floodborn_council_mechanic`, `konolkhatep_mechanic`, etc. |
| Reform activation layer (republics) | `common/government_reforms/02_government_reforms_republics.txt` | Activates mechanics like `allclan_pandemonium_mechanic`, `anb_medasi_power_share`, etc. |
| Reform activation layer (theocracies) | `common/government_reforms/03_government_reforms_theocracies.txt` | Activates mechanics like `anb_adventurer_unity`, `corinsfield_paranoia_mechanic`, `silk_order_mechanic`. |
| Mechanic definitions | `common/government_mechanics/*.txt` | Actual power bars, interactions, triggers, costs, and scaling. |
| GUI layer | `interface/government_mechanics/*.gui` and `*.gfx` | Custom presentation for many mechanics. |

## Main objects / state

| Object | Meaning |
|---|---|
| `government_abilities = { <mechanic_id> }` | Reform-level activation point. |
| `<mechanic_id> = { powers = {...} interactions = {...} }` | Mechanic definition object. |
| `add_government_power` / `has_government_power` | Runtime effects/triggers used by mechanics and downstream events. |
| `scaled_modifier` / `range_modifier` / `reverse_scaled_modifier` | Core state-to-modifier conversion pattern. |
| `available = { ... }` | Additional gating inside mechanic definition (not just reform gating). |

## Implementation flow

### 1) Reform enables mechanic by ID

Reform files define `government_abilities` and reference one or more mechanic IDs.

### 2) Mechanic definition provides runtime behavior

Mechanic file defines power ranges, monthly growth behavior, and interaction buttons.

### 3) GUI and icon assets expose mechanic to players

`gui = ...` keys in mechanic powers/interactions map to interface definitions.

### 4) Event/mission content can consume or modify mechanic state

Mechanic state is integrated via `add_government_power`/`has_government_power` checks.

## Activation map (sample set)

| Mechanic ID | Reform file anchors | Mechanic file |
|---|---|---|
| `anb_adventurer_unity` | `03_government_reforms_theocracies.txt` (multiple adventurer reforms) | `common/government_mechanics/anb_adventurer_unity.txt` |
| `corinsfield_paranoia_mechanic` | `03_government_reforms_theocracies.txt` (`peasants_theocracy_reform`) | `common/government_mechanics/anb_corinsfield_paranoia.txt` |
| `allclan_pandemonium_mechanic` | `02_government_reforms_republics.txt` (`pentapandemonium_reform` path) | `common/government_mechanics/anb_allclan_pandemonium.txt` |
| `floodborn_council_mechanic` | `01_government_reforms_monarchies.txt`, `02_government_reforms_republics.txt`, `03_government_reforms_theocracies.txt` | `common/government_mechanics/anb_floodborn_council.txt` |
| `silk_order_mechanic` | `03_government_reforms_theocracies.txt` | `common/government_mechanics/anb_silk_order.txt` |
| `rezankand_exemplar_mechanic` | `03_government_reforms_theocracies.txt` | `common/government_mechanics/anb_rezankand_exemplar.txt` |
| `anb_medasi_power_share` | `02_government_reforms_republics.txt` | `common/government_mechanics/anb_medasi_power_share.txt` |
| `vic_league_mechanic` | `01/02/03 government_reforms` (multiple lines) | `common/government_mechanics/anb_vic_league.txt` |

## Code examples

### Example A: Reform-level activation

From `common/government_reforms/03_government_reforms_theocracies.txt`:

```txt
government_abilities = {
	anb_adventurer_unity
}
```

And for Corinsfield:

```txt
government_abilities = {
	corinsfield_paranoia_mechanic
}
```

### Example B: Mechanic-level power definition

From `common/government_mechanics/anb_adventurer_unity.txt`:

```txt
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
```

### Example C: Cross-system coupling in mechanic logic

From `common/government_mechanics/anb_floodborn_council.txt`:

```txt
range_modifier = {
	trigger = {
		ruler_is_powerful_mage = yes
		ruler_is_witch_king = yes
	}
	modifier = {
		monthly_bloodbrand_power = 0.50
	}
}
```

This is a direct example of a government mechanic depending on the magic/infamy framework.

## Vanilla vs Anbennar differences

- Vanilla baseline supports mechanic scripting, but Anbennar uses a much larger number of bespoke mechanic IDs attached to custom reforms.
- Anbennar mechanics routinely include cross-links to custom estates, magic triggers, and tag-specific event systems.
- Reform activation in Anbennar is often part of nation-specific progression pipelines rather than broad generic government families.

## Safe adaptation notes

- For Verne, prefer activating a reused mechanic via reforms first, then adding light mission/event integration, instead of building a fresh mechanic stack.
- If creating a new mechanic, copy from a closest existing complexity tier (e.g., `anb_adventurer_unity` for simple; `corinsfield_paranoia_mechanic` for medium; `floodborn_council_mechanic` for heavy cross-system logic).
- Validate GUI hook names and icon assets early to avoid orphaned mechanics.

## Related systems

- [custom-government-mechanics-and-gui-patterns-reference.md](./custom-government-mechanics-and-gui-patterns-reference.md)
- [adventurer-systems-and-estate-patterns-reference.md](./adventurer-systems-and-estate-patterns-reference.md)
- [witch-king-lichdom-war-wizard-infamy-reference.md](./witch-king-lichdom-war-wizard-infamy-reference.md)
- [../references/eu4-baseline-vs-anbennar-comparison-notes.md](../references/eu4-baseline-vs-anbennar-comparison-notes.md)
- [../implementation-crosswalk.md](../implementation-crosswalk.md)

## Open verification points

- NEEDS_REPO_CHECK: complete line-by-line activation matrix for every custom mechanic ID across all reform files (this article includes representative high-value mechanics, not exhaustive full corpus).
- NEEDS_REPO_CHECK: confirm edge-case mechanics activated indirectly by event-swapped reforms or hidden reform transitions.
