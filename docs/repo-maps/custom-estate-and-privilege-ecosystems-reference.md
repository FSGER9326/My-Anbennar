# Custom Estate and Privilege Ecosystems Reference

This article documents how Anbennar uses estates as **full subsystem containers** rather than just passive modifiers.

## Quick Verdict

Major Anbennar estates (Mages, Artificers, Vampires, Adventurers, Commands, castes, etc.) are built as ecosystems:

- custom estate definitions
- large privilege libraries
- scripted helper effects/triggers
- event namespaces and mission consumers
- cross-estate coupling and lockout logic

For Verne adaptation, copying an ecosystem pattern is safer than inventing single isolated privileges.

---

## What the system does

- Governs political actors with loyalty/influence and state-specific privilege trees.
- Encodes special organizations (not just generic privileges).
- Connects estate choices to hidden progression, project pacing, and narrative event trees.
- Enables race/religion/tag-local naming and behavior branches.

---

## Core files

| Area | File | Why it matters |
|---|---|---|
| Mages estate | `common/estates/97_mages.txt` | Shows magic-specific trigger gating, infamy coupling, and dynamic naming. |
| Mages privileges | `common/estate_privileges/estate_mages_privileges.txt` | Large organization framework with swap costs and influence-scaled conditional modifiers. |
| Artificers estate | `common/estates/99_artificers.txt` | Artificery unlock and mixed-mode gating; production-oriented influence logic. |
| Artificers privileges | `common/estate_privileges/estate_artifice_privileges.txt` | Organization trees tied to research pacing flags and costed swaps. |
| Vampires estate | `common/estates/100_vampire.txt` | Full law/organization/action ecosystem with masquerade/open-rule branches. |
| Vampires privileges | `common/estate_privileges/estate_vampires_privileges.txt` | Demonstrates mutually exclusive law-state sets and on_granted/on_invalid cleanup. |
| Estate event consumers | `events/estate_mages.txt`, `events/estate_artificers.txt`, `events/VampireRuler.txt`, etc. | Runtime behavior and escalation consequences. |

---

## Main objects and state

| Object | Examples |
|---|---|
| Estate trigger gating | `has_not_banned_magic_artificery`, `artificery_unlocked`, `has_vampires_estate`. |
| Organization privileges | `estate_mages_organization_*`, `estate_artificers_organization_*`, `estate_vampires_law_*`. |
| Swap-cost helpers | `can_pay_for_organization_swap`, `pay_for_organization_swap`, `clear_*_organization_effect`. |
| Cross-system flags/modifiers | `artifice_research_fast`, infamy trigger tiers, `pursuing_lichdom`, masquerade opinion effects. |
| Dynamic naming | culture/tag/flag-based `custom_name` and `custom_desc` blocks in estate definitions. |

---

## Step-by-step implementation model

### 1) Estate existence is itself conditional

Estate files gate availability by country flags, reforms, magic/artifice mode, race, or government attributes.

### 2) Organization privileges define long-term posture

Instead of only one-off bonuses, organization privileges encode strategic lanes with costs and lockouts.

### 3) Grant/revoke/invalid hooks run cleanup and migration

`on_granted`, `on_revoked`, and `on_invalid` blocks handle state repair, removing stale modifiers/flags/opinions.

### 4) Influence/loyalty scaling modifies subsystem outputs

Influence-scaled conditional modifiers are used to model "estate competence" and pressure at different loyalty bands.

### 5) Events and missions consume estate state

Content files read privileges/flags/triggers to branch events and mission outcomes.

---

## Real code examples

### Example A: Mages estate coupled to magical infamy tiers

From `common/estates/97_mages.txt`:

```txt
influence_modifier = {
	desc = EST_VAL_INFAMY_DENOUNCED
	trigger = { type_has_infamy_denounced = { type = country } }
	influence = 60
}

influence_modifier = {
	desc = EST_VAL_INFAMY_WITCH_KING
	trigger = { estate_has_infamy_witch_king = yes }
	influence = 80
}
```

Why it matters: this estate is directly bound to high-magic reputation state.

### Example B: Mages organization swap with helper payment + scaling tooltips

From `common/estate_privileges/estate_mages_privileges.txt`:

```txt
can_select = { can_pay_for_organization_swap = { estate = mages } }
...
on_granted = {
	pay_for_organization_swap = { organization = state }
	scaling_with_influence_privilege_tooltip = {
		estate_privilege = estate_mages_organization_state
	}
}
```

Why it matters: organization transitions are formalized, not ad-hoc modifier toggles.

### Example C: Artificers organization affects research pace flags

From `common/estate_privileges/estate_artifice_privileges.txt`:

```txt
on_granted = {
	...
	hidden_effect = {
		set_country_flag = artifice_research_fast
	}
}
```

Why it matters: estate posture controls downstream research system behavior.

### Example D: Vampire law privilege cleanup discipline

From `common/estate_privileges/estate_vampires_privileges.txt`:

```txt
on_granted = {
	clear_vampire_law = yes
	set_vampire_masquerade_opinion = yes
}
on_invalid = {
	clear_vampire_masquerade_opinion = yes
}
```

Why it matters: the privilege layer includes explicit invalid-state recovery.

---

## Vanilla vs Anbennar difference notes

- Vanilla estates are broad and mostly generic; Anbennar estates are often bespoke subsystems.
- Organization trees and law-state structures are much deeper than common vanilla privilege sets.
- Cross-linking with magic/artificery/vampire frameworks is extensive and often hidden-state heavy.

---

## Safe adaptation notes

- Reuse an existing organization privilege pattern before inventing custom swap mechanics.
- Include `on_invalid` cleanup for any privilege that sets broad opinion/modifier/flag state.
- Keep estate trigger gating explicit; avoid granting estates unconditionally if mode flags are required.
- If Verne needs a court estate lane, scaffold from mages/artificers organization structures.

---

## Suggested reuse cases

- Verne court faction organizations (state/guild/religious style branches).
- Wyvern order institutional lane with privilege-based progression.
- Corinite political integration privileges with explicit invalid cleanup.
- Overseas charter houses as a privilege ecosystem, not one-off mission rewards.

---

## Related systems

- [adventurer-systems-and-estate-patterns-reference.md](./adventurer-systems-and-estate-patterns-reference.md)
- [artificery-research-and-inventions-reference.md](./artificery-research-and-inventions-reference.md)
- [witch-king-lichdom-war-wizard-infamy-reference.md](./witch-king-lichdom-war-wizard-infamy-reference.md)
- [custom-government-mechanics-and-gui-patterns-reference.md](./custom-government-mechanics-and-gui-patterns-reference.md)

Cross-layer links:

- Design: [../design/dynasty-and-court.md](../design/dynasty-and-court.md)
- Design: [../design/orders-monuments-and-mercs.md](../design/orders-monuments-and-mercs.md)
- Crosswalk: [../implementation-crosswalk.md](../implementation-crosswalk.md)
