# Artificery Research And Inventions Reference

This article maps the live Anbennar artificery framework: unlocking artificery, calculating capacity, researching inventions, and applying inventions through estate privileges.

It is a repo-grounding article, not a redesign.

## Quick Verdict

Artificery is a full system family, not just a list of inventions.

The implementation pattern is:

1. choose an artificery mode
2. unlock the system and its estate state
3. calculate artifice capacity and remaining points through a shared helper
4. open research chains through events
5. convert research state into unlocked invention flags
6. spend artifice points by granting estate privileges that represent active inventions

That means the real "invention" layer lives across events, triggers, scripted effects, privileges, and estate structure at once.

## Core Files

| File | Role |
|---|---|
| [common/scripted_effects/artifice_scripted_effects.txt](../../common/scripted_effects/artifice_scripted_effects.txt) | Capacity, point, and invention-use helpers |
| [events/MagicArtificerySetup.txt](../../events/MagicArtificerySetup.txt) | Unlock and mode-choice events |
| [events/ArtificeResearch.txt](../../events/ArtificeResearch.txt) | Research menus, category choices, and unlock pipeline |
| [events/ArtificeInventions.txt](../../events/ArtificeInventions.txt) | Invention-specific event outcomes |
| [common/scripted_triggers/anb_scripted_triggers_artifice.txt](../../common/scripted_triggers/anb_scripted_triggers_artifice.txt) | Point checks and discovery-state checks |
| [common/estate_privileges/estate_artifice_privileges.txt](../../common/estate_privileges/estate_artifice_privileges.txt) | Active invention privileges and organization modes |
| [common/estates/99_artificers.txt](../../common/estates/99_artificers.txt) | Artificers estate definition |

## Main Objects And State

| Object | Type | Purpose |
|---|---|---|
| `update_artifice_points` | scripted effect | Recalculates total and remaining artificery capacity |
| `StaticArtificePoints` | variable | Permanent point support granted by content |
| `RemainingArtificePoints` | variable | Unspent current capacity |
| `MaxArtificePoints` | variable | Total current capacity |
| `artificery_unlocked` | flag | Main unlock marker |
| `magic_artificery_mixed` | flag | Mixed magic-artificery mode |
| `magic_artificery_artificery_only` | flag | Pure artificery mode |
| `unlocked_artifice_invention_*` | flags | Discovery state for specific inventions |
| `artifice_invention_*` | estate privileges | Active inventions currently in use |

## Main Implementation Model

### 1. Capacity is centralized in a helper effect

The most important helper is `update_artifice_points`.

It:

- checks whether artificery mode is active
- calculates total capacity
- calculates remaining capacity
- updates overflow handling
- sets or clears modifiers like over-capacity penalties

Repo anchor:

- [artifice_scripted_effects.txt](../../common/scripted_effects/artifice_scripted_effects.txt)

### 2. Unlocking artificery is an event-mode choice

`magic_artificery_setup.1` and `.2` manage:

- mage-only vs mixed vs artificery-only mode
- special restrictions such as lich or witch-king incompatibilities
- immediate unlock setup

The unlock flow includes:

- `set_country_flag = artificery_unlocked`
- `artifice_inventions_give_basket = yes`
- `update_artifice_points = yes`
- organizational privilege setup

Repo anchor:

- [MagicArtificerySetup.txt](../../events/MagicArtificerySetup.txt)

### 3. Research and active use are separate layers

Research events unlock invention flags.

Active use is represented by estate privileges such as:

- `artifice_invention_portable_turrets`
- `artifice_invention_spell_in_a_box`
- `artifice_invention_commercial_sky_galleons`

That means "known" and "currently active" are intentionally separate states.

## Real Code Examples

### Example 1. Research menu entry and cost payment

`artifice_research.1` is a clear example of how research begins.

It:

- opens the research menu state
- updates research speed
- charges `-30` ADM, DIP, and MIL
- may route to the next research event

Repo anchor:

- [ArtificeResearch.txt](../../events/ArtificeResearch.txt)

### Example 2. Unlocking specific inventions through research branches

Research events in `ArtificeResearch.txt` eventually convert research state into unlocked invention flags.

Representative invention families include:

- spell in a box
- portable turrets
- commercial sky galleons

Repo anchor:

- [ArtificeResearch.txt](../../events/ArtificeResearch.txt)

### Example 3. Active invention privileges

The actual "equip/use this invention" layer lives in estate privileges.

Representative structure:

```txt
artifice_invention_portable_turrets = {
    is_valid = {
        has_country_flag = unlocked_artifice_invention_portable_turrets
    }
    can_select = {
        artifice_has_points_10 = yes
    }
    on_granted = {
        artifice_inventions_currently_used_increase = yes
    }
    on_revoked = {
        artifice_inventions_currently_used_decrease = yes
    }
}
```

Repo anchor:

- [estate_artifice_privileges.txt](../../common/estate_privileges/estate_artifice_privileges.txt)

### Example 4. Collection triggers

The artificery trigger file does not only check point costs.

It also includes collection-state helpers such as:

- `has_active_all_military_tier_1_inventions`
- `has_discovered_all_military_tier_1_inventions`

Repo anchor:

- [anb_scripted_triggers_artifice.txt](../../common/scripted_triggers/anb_scripted_triggers_artifice.txt)

## How This Differs From A Simpler Vanilla-Style Pattern

Vanilla-style expectation:

- unlock invention
- get permanent modifier

Anbennar artificery pattern:

- choose system mode
- unlock the system
- maintain capacity and overflow
- research discoveries
- store discoveries in flags
- activate a limited subset through estate privileges
- re-run capacity helpers whenever support changes

## Safe Adaptation Notes

If you want to adapt artificery:

1. use `update_artifice_points` whenever content changes capacity or support
2. separate discovery from activation
3. check both `unlocked_artifice_invention_*` and point-cost triggers when copying an invention pattern
4. if you add a new invention family, mirror the checklist comments in the research/effects files
5. remember artificery mode interacts with magic mode, lich, and witch-king branches

## Best Places To Reuse This

- Verne artifice or artificery-adjacent upgrades
- invention-like subsystems with limited active slots
- mixed-mode magic/technology content
- mission rewards that should support a technology layer without directly granting the whole payoff
