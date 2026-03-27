# Verne Wyvern Orders, Mercenaries, and Monument Coupling Reference

## Quick verdict

This system is **partially grounded and partially unresolved**.

Grounded now:

- Verne has real mercenary company implementations (`merc_vernmen_adventurers`, `merc_verne_exploration_team_1/2`).
- Verne has order-adjacent event hooks and mission flags (`verne.902`, `verne.903`, `verne_refunding_holy_order_15`).
- Verne has a real monument relocation chain (`kazakesh` to `kazakesh_stingport`) with mission/event coupling.

Still unresolved:

- direct repo evidence for the design-named "Chapterhouse of the Crimson Wake" object and the three design-named wyvern order companies.

Status for full ORD blueprint: **NEEDS_REPO_CHECK**.

## What the system does

At implementation level, this is a **bundle of linked systems**:

1. mercenary company templates
2. mission progression and flags
3. order-related triggered events
4. monument state transitions via events
5. wyvern military unlock hooks (mythical cavalry, estate-action rider loops)

## Core files

| Area | File | Notes |
|---|---|---|
| Baseline Verne mercenary company | `common/mercenary_companies/00_mercenaries.txt` | Contains `merc_vernmen_adventurers`. |
| Verne special expedition teams | `common/mercenary_companies/0_anb_elite_mercenaries.txt` | Contains `merc_verne_exploration_team_1` and `_2`. |
| Verne mission progression | `missions/Verne_Missions.txt` | Holds wyvern nest chain, unlock flags, and mount unlock. |
| Verne decisions | `decisions/VerneDecisions.txt` | Contains estate-driven wyvernrider recruitment decision and adventure launcher. |
| Verne flavor events | `events/Flavour_Verne_A33.txt` | Includes order events `verne.902`/`verne.903` and monument move event `verne.126`. |
| Monument definition (moved variant) | `common/great_projects/anb_monuments_missions.txt` | Defines `kazakesh_stingport`. |
| Monument definition (original) | `common/great_projects/anb_monuments_sarhal.txt` | Defines `kazakesh` and move-prevention flag checks. |
| Verne helper effects | `common/scripted_effects/anb_scripted_effects_for_verne.txt` | Includes wyvernrider creation helpers used by Verne systems. |

## Main objects / state

| Object | Type | Role |
|---|---|---|
| `merc_vernmen_adventurers` | merc company template | Core Verne-linked company in generic merc pool layer. |
| `merc_verne_exploration_team_1/2` | merc company templates | Flag-gated non-AI expedition teams. |
| `verne_refunding_holy_order_15` | country flag | Enables additional MIL refund in order events. |
| `verne_has_discounted_wyvernrider` | country flag | Set by order event branch (`verne.903`). |
| `kazakesh` / `kazakesh_stingport` | great projects | Monument path that is physically moved in Verne event chain. |
| `verne_moved_spire` / `verne_moved_this_spire` | country/province flags | Prevents duplicate monument state and gates build behavior. |
| `enable_mythical_cavalry = { mount = wyvern }` | mission effect | Explicit wyvern military capability unlock in mission flow. |

## Implementation flow

### 1) Mission chain pushes Verne into wyvern institutional progression

`missions/Verne_Missions.txt` includes the wyvern nest sequence and later unlock hooks including mythical cavalry.

### 2) Event layer handles order outcomes and refunds

`verne.902` and `verne.903` are hidden order events; `verne.903` sets long-lived discount flag state.

### 3) Monument transformation is handled by events, not passive modifier swaps

`verne.126` destroys `kazakesh` at province `5763`, then adds `kazakesh_stingport` at province `376`, setting movement flags.

### 4) Merc companies exist in at least two Verne-linked families

- baseline adventurer company in `00_mercenaries.txt`
- specialized expedition teams in `0_anb_elite_mercenaries.txt`

### 5) Estate and decision systems tie back into wyvern force identity

`estate_verne_recruit_wyvernrider` exists as a player-facing decision wrapper and consumes estate-action machinery.

## Code examples

### Example A: Verne baseline mercenary company

From `common/mercenary_companies/00_mercenaries.txt`:

```txt
merc_vernmen_adventurers = {
    regiments_per_development = 0.025
	cavalry_weight = 0.3
	cavalry_cap = 5
	...
	cost_modifier = 0.75
	modifier = {
		discipline = -0.05
	}
}
```

### Example B: Verne special expedition teams

From `common/mercenary_companies/0_anb_elite_mercenaries.txt`:

```txt
merc_verne_exploration_team_1 = {
    regiments_per_development = 0
    cost_modifier = 0
	counts_towards_force_limit = no
	trigger = {
        has_country_flag = verne_vernissage_expedition_teams_unlocked
		hidden_trigger = { ai = no }
    }
}
```

### Example C: Hidden order event state changes

From `events/Flavour_Verne_A33.txt`:

```txt
country_event = {
	id = verne.903
	...
	option = {
		name = verne.903.a
		set_country_flag = verne_has_discounted_wyvernrider
		change_variable = {
			which = verne_wywvernrider_discount_count
			value = 1
		}
	}
}
```

### Example D: Monument relocation event

From `events/Flavour_Verne_A33.txt`:

```txt
5763 = {
	destroy_great_project = { type = kazakesh }
	set_province_flag = verne_moved_this_spire
}
set_country_flag = verne_moved_spire
376 = {
	add_great_project = {
		type = kazakesh_stingport
		instant = yes
	}
}
```

## Vanilla vs Anbennar differences

- Vanilla merc systems rarely chain this tightly into bespoke nation event + monument relocation logic.
- Verne implementation mixes merc templates, mission flags, hidden order events, estate actions, and monument replacement.
- This is significantly more "institutional state machine" than vanilla's ordinary merc hiring flow.

## Safe adaptation notes

- Reuse existing mission-flag/event pattern for any new Verne order branch before adding new standalone frameworks.
- Prefer adding new Verne companies as template families gated by explicit flags, matching current pattern.
- Keep monument transitions event-driven when physical relocation/swap semantics are required.
- Do not assume design names map 1:1 to existing implementation IDs without direct verification.

## Related systems

- [verne-wyvernrider-estate-ecosystem-reference.md](./verne-wyvernrider-estate-ecosystem-reference.md)
- [verne-launch-adventure-system.md](./verne-launch-adventure-system.md)
- [custom-estate-and-privilege-ecosystems-reference.md](./custom-estate-and-privilege-ecosystems-reference.md)
- [../design/orders-monuments-and-mercs.md](../design/orders-monuments-and-mercs.md)
- [../implementation-crosswalk.md](../implementation-crosswalk.md)

## Open verification points

- NEEDS_REPO_CHECK: identify whether "Chapterhouse of the Crimson Wake" has a direct monument ID currently present in repo.
- NEEDS_REPO_CHECK: identify whether design-named companies (Crimson Wake Lances / Heartspier Skyguard / Khenak Talons) already exist under different IDs.
- NEEDS_REPO_CHECK: complete map of holy-order interaction points beyond `verne.902`/`verne.903` and mission refund flag usage.
