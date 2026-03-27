# Powerful Mage and Succession Reference

This article maps how Anbennar handles powerful mage rulers, heirs, consorts, and succession maintenance in the live repo.

It is a repo-grounding document, not a redesign.

## Quick Verdict

Anbennar does not treat powerful mage succession as a single personality roll.

The real pattern is:

1. a central scripted effect creates or upgrades a mage ruler, heir, or consort
2. hidden helper events call that effect in a normalized way
3. nation-, government-, and reform-specific content injects direct mage-heir generation
4. `on_new_heir` maintenance events repair or preserve magical inheritance after normal succession logic fires

That means the safest way to build "special heir" systems is usually to adapt the existing `define_powerful_mage` plus delayed heir-maintenance pattern rather than inventing a new one from scratch.

## Core Files

| File | Role |
|---|---|
| [common/scripted_effects/anb_scripted_effects_for_magic_system.txt](../../common/scripted_effects/anb_scripted_effects_for_magic_system.txt) | Central `define_powerful_mage` helper and related mage state logic |
| [events/Magic_System_Events.txt](../../events/Magic_System_Events.txt) | Hidden helper events, inheritance maintenance, and succession cleanup |
| [events/Magic_Ruler_Events.txt](../../events/Magic_Ruler_Events.txt) | Generated heir/ruler mage event branches and upgrades |
| [common/on_actions/00_on_actions.txt](../../common/on_actions/00_on_actions.txt) | Delayed `on_new_heir` hook into mage inheritance maintenance |
| [events/Theocracies.txt](../../events/Theocracies.txt) | Government-specific mage-heir odds and explicit "promising young mage" options |
| [events/RintaSeekerEvents.txt](../../events/RintaSeekerEvents.txt) | Tag-specific direct ruler/heir mage setup examples |

## Main Objects And State

| Object | Type | Purpose |
|---|---|---|
| `define_powerful_mage` | scripted effect | Central creator/upgrader for ruler, heir, and consort mages |
| `magic_system.10` / `.11` / `.12` | events | Hidden wrappers that normalize ruler, heir, and consort mage definition |
| `magic_system.19` | event | Delayed heir maintenance and inheritance repair |
| `always_mage` | trigger/branch concept | Forces magical continuity in succession flows |
| `inherits_magic` | trigger/branch concept | Preserves school levels and magical inheritance |
| `theocracy_magical_odds_boosted` | government attribute | Raises chance of mage heirs in specific theocratic systems |

## Main Implementation Model

### 1. The central helper defines the mage object

The core entry point is `define_powerful_mage`.

It supports:

- `type = ruler`
- `type = heir`
- `type = consort`
- explicit school levels
- random levels
- `saved_levels = inherits`
- `save_levels = inherits`
- `war_wizard = yes`
- `starting_infamy = <value>`
- optional `witch_king = yes`
- optional `lich = yes`

Representative shape:

```txt
define_powerful_mage = {
    type = heir
    saved_levels = inherits
    save_levels = inherits
}
```

Repo anchor:

- [anb_scripted_effects_for_magic_system.txt:1961](../../common/scripted_effects/anb_scripted_effects_for_magic_system.txt#L1961)

### 2. Hidden helper events call the same effect

The magic system also exposes hidden wrapper events so content can fire an event and let the event apply the correct helper.

The main wrappers are:

- `magic_system.10` for rulers
- `magic_system.11` for heirs
- `magic_system.12` for consorts

Repo anchor:

- [Magic_System_Events.txt](../../events/Magic_System_Events.txt)

### 3. Succession is repaired after normal heir generation

Anbennar does not assume all special heir conditions can be resolved at heir creation time.

Instead, it uses a delayed `on_new_heir` maintenance pass to preserve magical inheritance after vanilla-like succession logic finishes.

The hook schedules:

```txt
country_event = { id = magic_system.19 days = 3 }
```

Repo anchor:

- [00_on_actions.txt:6242](../../common/on_actions/00_on_actions.txt#L6242)

Then `magic_system.19` checks inheritance conditions such as `always_mage` and `inherits_magic` and repairs the heir if needed.

Representative logic:

```txt
if = {
    limit = {
        has_heir = yes
        inherits_magic = yes
    }
    define_powerful_mage = {
        type = heir
        saved_levels = inherits
        save_levels = inherits
    }
}
```

Repo anchor:

- [Magic_System_Events.txt:297](../../events/Magic_System_Events.txt#L297)

## Real Code Examples

### Example 1. Heir inheritance repair in the generic magic system

This is the cleanest "do not trust raw succession, repair it later" pattern in the repo.

Core behavior:

- wait for heir creation
- check if magical inheritance rules apply
- redefine the heir as a powerful mage
- preserve inherited school data where appropriate

Key anchors:

- [00_on_actions.txt:6242](../../common/on_actions/00_on_actions.txt#L6242)
- [Magic_System_Events.txt:297](../../events/Magic_System_Events.txt#L297)

### Example 2. Direct heir creation in mage-ruler content

Some event chains bypass ordinary inheritance and directly create a new mage heir.

In `magic_ruler.103`, `magic_ruler.104`, and `magic_ruler.105`, the flow is:

1. create or replace the heir
2. immediately call `define_powerful_mage = { type = heir }`

Representative shape:

```txt
define_heir = {
    dynasty = ROOT
}
define_powerful_mage = {
    type = heir
}
```

Repo anchors:

- [Magic_Ruler_Events.txt:56](../../events/Magic_Ruler_Events.txt#L56)
- [Magic_Ruler_Events.txt:132](../../events/Magic_Ruler_Events.txt#L132)
- [Magic_Ruler_Events.txt:236](../../events/Magic_Ruler_Events.txt#L236)

### Example 3. Theocracy-specific mage-heir support

Theocracies repeatedly inject mage odds into their own succession and event branches with:

- `has_government_attribute = theocracy_magical_odds_boosted`
- weighted `random_list` chances
- direct "promising young mage" options

Representative branch shape:

```txt
if = {
    limit = { has_government_attribute = theocracy_magical_odds_boosted }
    random_list = {
        10 = { define_powerful_mage = { type = heir } }
        90 = { }
    }
}
```

Repo anchors:

- [Theocracies.txt:1255](../../events/Theocracies.txt#L1255)
- [Theocracies.txt](../../events/Theocracies.txt)

### Example 4. Tag-specific ruler and heir setup

Rinta Seeker content shows the nation-script version of the same pattern:

- direct `define_heir`
- immediate `define_powerful_mage`
- optional explicit school values for rulers

Repo anchors:

- [RintaSeekerEvents.txt](../../events/RintaSeekerEvents.txt)

## How This Differs From A Simpler Vanilla-Style Pattern

Vanilla-style expectation:

- heir exists
- trait or event modifier decides quality
- done

Anbennar pattern:

- heir may be created normally, by event, or by government content
- magical capability is separately imposed or repaired
- inheritance can preserve school data
- multiple systems can hook the same mage-definition helper
- succession maintenance happens through delayed cleanup, not only immediate generation

## Safe Adaptation Notes

If you want to build a special heir or succession system:

1. prefer calling `define_powerful_mage` instead of manually rebuilding mage state
2. use a delayed repair event if the heir can be created by multiple routes
3. treat `on_new_heir` as the safest repair point for succession-specific guarantees
4. copy government- or tag-specific injection patterns when you want weighted magical odds
5. preserve inheritance branches like `saved_levels = inherits` when continuity matters

## Best Places To Reuse This

- Verne heir-shaping and Red Court succession systems
- nation-specific "always magical dynasty" content
- special consort mage or heir-mage reform rewards
- controlled magical inheritance without rewriting the entire succession system
