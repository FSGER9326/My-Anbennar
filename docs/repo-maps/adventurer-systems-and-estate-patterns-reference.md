# Adventurer Systems And Estate Patterns Reference

This article maps the Anbennar adventurer framework, especially adventurer unity, the adventurer estate, and how adventurer governments transition into longer-lived state content.

It is a repo-grounding article, not a redesign.

## Quick Verdict

Adventurer content in Anbennar is not just an estate or just a government mechanic.

The main pattern is:

1. an adventurer estate exists with loyalty, influence, and estate actions
2. some governments use a dedicated `adventurer_unity` mechanic
3. events deliver estate conflicts, growth, and expedition flavor
4. formable and transition content preserves adventurer legacy with scripted effects

This makes the adventurer family a strong example of how Anbennar combines estate, mechanic, event, and transition logic into a single gameplay identity.

## Core Files

| File | Role |
|---|---|
| [common/government_mechanics/anb_adventurer_unity.txt](../../common/government_mechanics/anb_adventurer_unity.txt) | Dedicated government power mechanic for adventurer unity |
| [common/estates/98_adventurers.txt](../../common/estates/98_adventurers.txt) | Adventurer estate definition |
| [decisions/EstateActionsAdventurers.txt](../../decisions/EstateActionsAdventurers.txt) | Decision wrappers for adventurer estate actions |
| [events/estate_adventurers.txt](../../events/estate_adventurers.txt) | Main adventurer estate event family |
| [events/Escann_Adventurers_Intro.txt](../../events/Escann_Adventurers_Intro.txt) | Early Escann adventurer-unity setup and conversion examples |
| [common/scripted_effects/anb_scripted_effects.txt](../../common/scripted_effects/anb_scripted_effects.txt) | Shared legacy helper used when countries outgrow adventurer origin |
| [decisions/EscannFormables.txt](../../decisions/EscannFormables.txt) | Transition/formable logic for adventurer-derived states |

## Main Objects And State

| Object | Type | Purpose |
|---|---|---|
| `anb_adventurer_unity` | government mechanic | Main custom unity resource |
| `adventurer_unity` | mechanic power | Value tracked from `0` to `100` |
| `promote_adventurer_unity` | interaction | MIL-for-unity government interaction |
| `adventurer_derived_government` | flag | Tracks post-adventurer legacy states |
| `adventurer_legacy_effect` | scripted effect | Applies legacy support during transition or formation |

## Main Implementation Model

### 1. Adventurer unity is a real government mechanic

The unity system is defined in `common/government_mechanics`.

It includes:

- `adventurer_unity` with max `100`
- `reset_on_new_ruler = no`
- scaled modifiers by unity level
- a direct interaction, `promote_adventurer_unity`

Representative interaction:

```txt
promote_adventurer_unity = {
    monarch_power = MIL
    cost = 50
    add_government_power = {
        mechanic_type = anb_adventurer_unity
        power_type = adventurer_unity
        value = 10
    }
}
```

Repo anchor:

- [anb_adventurer_unity.txt](../../common/government_mechanics/anb_adventurer_unity.txt)

### 2. The estate is broader than the mechanic

The adventurer estate exists even outside the narrow unity mechanic definition.

The estate file includes:

- custom trigger logic excluding many governments and tags
- happiness-based modifiers
- influence logic for adventurer-derived governments

Repo anchor:

- [98_adventurers.txt](../../common/estates/98_adventurers.txt)

### 3. Estate actions use the normal wrapper pattern

Adventurer estate actions are exposed through standard decision wrappers that check:

- `has_enabled_estate_action`
- cooldowns
- estate loyalty/influence conditions
- then use `estate_action = { ... }`

Repo anchor:

- [EstateActionsAdventurers.txt](../../decisions/EstateActionsAdventurers.txt)

### 4. Legacy is preserved through a shared effect

Anbennar does not simply forget adventurer origin after nation transitions.

`adventurer_legacy_effect` applies long-tail support for countries that came from adventurer roots.

Repo anchor:

- [anb_scripted_effects.txt:2605](../../common/scripted_effects/anb_scripted_effects.txt#L2605)

## Real Code Examples

### Example 1. Adventurer unity government interaction

The unity mechanic file is the best example of a compact but real Anbennar-specific government power system.

It contains:

- a custom power
- scaling effects
- a direct spend-MIL-for-unity interaction

Repo anchor:

- [anb_adventurer_unity.txt](../../common/government_mechanics/anb_adventurer_unity.txt)

### Example 2. Adventurer estate conflicts

`estate_adventurers.txt` contains repeated conflict and flavor patterns such as:

- adventurers vs nobles
- merchants refusing to pay adventurers
- artifact conflicts with artificers

Repo anchor:

- [estate_adventurers.txt](../../events/estate_adventurers.txt)

### Example 3. Early Escann unity support

Escann adventurer intro content directly adds government power through the custom mechanic:

```txt
add_government_power = {
    mechanic_type = anb_adventurer_unity
    power_type = adventurer_unity
    value = 10
}
```

Repo anchor:

- [Escann_Adventurers_Intro.txt](../../events/Escann_Adventurers_Intro.txt)

### Example 4. Formable transition into legacy state

Escann formable decisions repeatedly preserve adventurer origin by checking adventurer government state and applying:

```txt
adventurer_legacy_effect = yes
```

They also set:

- `adventurer_derived_government`

Repo anchor:

- [EscannFormables.txt](../../decisions/EscannFormables.txt)

## Estate Pattern Lessons

The adventurer family shows several reusable estate patterns:

1. define the estate in `common/estates`
2. expose active actions through decision wrappers
3. drive narrative and tension in `events/estate_<estate>.txt`
4. let formables or reform transitions preserve the estate's legacy through a helper effect or flag

## How This Differs From A Simpler Vanilla-Style Pattern

Vanilla-style expectation:

- estate exists
- give privileges
- maybe get a generic event

Anbennar adventurer pattern:

- estate plus custom mechanic can coexist
- region-specific intro content feeds the mechanic
- estate action wrappers behave like a mini-interface
- event families create internal political identity
- formables can preserve the system's legacy instead of deleting it

## Safe Adaptation Notes

If you want to adapt adventurer-style systems:

1. decide whether you need only an estate, only a government mechanic, or both
2. copy estate action wrappers if the player should actively push the system
3. use a shared legacy effect if the system should matter after regime transition
4. check event families for estate-vs-estate conflict patterns before inventing new political events
5. use direct `add_government_power` hooks when missions or intros should feed the custom mechanic

## Best Places To Reuse This

- custom order, expedition, or prestige corps systems
- Verne court or chapterhouse content with estate plus institution overlap
- transition mechanics where an early-game identity should remain relevant later
- any new custom estate that should feel alive rather than only modifier-driven
