# Verne Wyvernrider Estate Ecosystem Reference

## Quick verdict

This is a **strongly grounded implementation family** for Verne.

Status: **IMPLEMENTATION_READY** for adaptation patterns, with some broader chain verification still pending.

## What the system does

The wyvernrider institutional loop is implemented as a **mutually exclusive estate lane**:

1. one of two Verne-specific privileges becomes active
2. privilege grants enable the same estate action (`VERNE_WYVERNRIDER_RECRUIT`)
3. decision wrapper executes the action and routes counters to the active estate
4. companion modifiers and cross-privilege cleanup preserve consistent state
5. mission/event progression gates and flips which lane is active

## Core files

| Area | File | Notes |
|---|---|---|
| Verne estate action decision wrapper | `decisions/VerneDecisions.txt` | `estate_verne_recruit_wyvernrider` with cooldown, MIL cost, estate counter routing. |
| Verne-specific privileges (primary) | `common/estate_privileges/anb_privileges.txt` | `estate_adventurers_ride_of_the_worthy` and `estate_nobles_noble_wyvernriders`. |
| Noble privilege compatibility guard | `common/estate_privileges/02_noble_privileges.txt` | `estate_nobles_noble_officer_right` blocks conflicts with wyvernrider privileges for A33. |
| Verne flavor event lane toggles | `events/Flavour_Verne_A33.txt` | Event outcomes set relevant privileges/flags and support order effects. |
| Estate framework context | `common/estates/98_adventurers.txt`, `common/estates/02_nobility.txt` | Estates containing the Verne privilege entries. |

## Main objects / state

| Object | Type | Role |
|---|---|---|
| `estate_adventurers_ride_of_the_worthy` | estate privilege | Verne adventurer-side wyvernrider lane. |
| `estate_nobles_noble_wyvernriders` | estate privilege | Verne noble-side wyvernrider lane. |
| `VERNE_WYVERNRIDER_RECRUIT` | estate action | Shared action enabled by either privilege. |
| `estate_verne_recruit_wyvernrider` | decision | Player-facing execution wrapper for estate action. |
| `verne_adventurer_wyvernriders` / `verne_noble_wyvernriders` | country modifiers | Lane-specific persistent state markers. |
| `increase_estate_action_counter` | effect use | Routes usage tracking to active estate branch. |

## Implementation flow

### 1) Privileges are mission-gated and tag-gated

Both core privileges require Verne (`A33`) and mission completion (`A33_binding_the_beast`).

### 2) Granting one lane auto-cleans the other lane

Each privilege `on_granted` removes the opposite privilege, applies lane modifier, and charges switch cost (`add_mil_power = -100`) when switching.

### 3) Both lanes expose the same estate action surface

Both privileges enable `VERNE_WYVERNRIDER_RECRUIT`, creating one player-facing action path with branch-specific backend accounting.

### 4) Decision wrapper handles action cooldown and accounting

`estate_verne_recruit_wyvernrider` checks action availability/cooldown and calls the estate action. It then increments action counters for Adventurers or Nobles based on active privilege.

### 5) Compatibility guardrails exist in broader noble privilege ecosystem

`estate_nobles_noble_officer_right` explicitly blocks selection for A33 while either wyvernrider privilege is present.

## Code examples

### Example A: Adventurer wyvernrider privilege grant behavior

From `common/estate_privileges/anb_privileges.txt`:

```txt
estate_adventurers_ride_of_the_worthy = {
	is_valid = {
		is_or_was_tag = { tag = A33 }
		mission_completed = A33_binding_the_beast
	}
	on_granted = {
		enable_estate_action = { estate_action = VERNE_WYVERNRIDER_RECRUIT }
		add_country_modifier = { name = verne_adventurer_wyvernriders duration = -1 }
		if = {
			limit = { has_estate_privilege = estate_nobles_noble_wyvernriders }
			remove_estate_privilege = estate_nobles_noble_wyvernriders
			add_mil_power = -100
		}
	}
}
```

### Example B: Shared decision wrapper with branch-specific counter routing

From `decisions/VerneDecisions.txt`:

```txt
estate_verne_recruit_wyvernrider = {
	allow = {
		mil_power = 100
		estate_action_off_cooldown = {
			estate_action = VERNE_WYVERNRIDER_RECRUIT
			days = 3650
		}
	}
	effect = {
		estate_action = { estate_action = VERNE_WYVERNRIDER_RECRUIT }
		if = {
			limit = { has_estate_privilege = estate_adventurers_ride_of_the_worthy }
			increase_estate_action_counter = { estate = estate_adventurers }
		}
		else = {
			increase_estate_action_counter = { estate = estate_nobles }
		}
	}
}
```

### Example C: Compatibility guard in noble officer-right privilege

From `common/estate_privileges/02_noble_privileges.txt`:

```txt
if = {
	limit = { is_or_was_tag = { tag = A33 } }
	NOT = {
		has_estate_privilege = estate_adventurers_ride_of_the_worthy
		has_estate_privilege = estate_nobles_noble_wyvernriders
	}
}
```

## Vanilla vs Anbennar differences

- Vanilla does not typically implement this level of tag-specific mutual exclusivity between estate lanes and action wrappers.
- Verne uses estate privileges as institutional state toggles, not just passive modifiers.
- Branch switching has explicit cleanup and cost semantics, making it closer to a custom subsystem than ordinary privilege picks.

## Safe adaptation notes

- Reuse this exact mutual-exclusion pattern for future Verne court/order lanes.
- Keep one shared action ID if branches should diverge only in accounting/effects, not UX.
- Preserve cleanup logic in `on_granted` when adding additional lanes.
- Add explicit compatibility checks in other privileges/reforms to prevent hidden conflicts.

## Related systems

- [custom-estate-and-privilege-ecosystems-reference.md](./custom-estate-and-privilege-ecosystems-reference.md)
- [adventurer-systems-and-estate-patterns-reference.md](./adventurer-systems-and-estate-patterns-reference.md)
- [verne-wyvern-orders-mercs-and-monuments-reference.md](./verne-wyvern-orders-mercs-and-monuments-reference.md)
- [../design/orders-monuments-and-mercs.md](../design/orders-monuments-and-mercs.md)
- [../implementation-crosswalk.md](../implementation-crosswalk.md)

## Open verification points

- NEEDS_REPO_CHECK: full event-map of every source that can set/remove the two wyvernrider privileges.
- NEEDS_REPO_CHECK: full localization and estate-action scripting bundle for `VERNE_WYVERNRIDER_RECRUIT` to ensure no hidden branch behavior is missed.
