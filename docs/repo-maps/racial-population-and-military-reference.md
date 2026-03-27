# Racial Population And Military Reference

This article maps the Anbennar racial population, racial administration, and racial military systems in the live repo.

It is a repo-grounding article, not a redesign.

## Quick Verdict

Anbennar racial systems are not a single racial modifier layer.

They are a multi-part family built from:

1. custom GUI entry points
2. menu-opening decision or button logic
3. hidden state flags for which racial menu is open
4. scripted effects that reset and rebuild racial military state
5. race-specific event families
6. province-level tolerance updates
7. mismatch-repair events that keep military tech and racial unit states aligned

That means any attempt to adapt racial systems safely needs to account for UI, events, scripted effects, and repair logic together.

## Core Files

| File | Role |
|---|---|
| [decisions/Racial.txt](../../decisions/Racial.txt) | Menu-opening decision wrappers and AI access |
| [common/custom_gui/customgui_racial_interface.txt](../../common/custom_gui/customgui_racial_interface.txt) | Racial menu windows and button logic |
| [common/scripted_effects/anb_scripted_effects_for_racial_tolerances.txt](../../common/scripted_effects/anb_scripted_effects_for_racial_tolerances.txt) | Central racial administration and military reset helpers |
| [common/scripted_triggers/anb_scripted_triggers_racial.txt](../../common/scripted_triggers/anb_scripted_triggers_racial.txt) | Tolerance and racial-state checks |
| [events/anb_racial_pop_misc.txt](../../events/anb_racial_pop_misc.txt) | Menu routing and miscellaneous population handling |
| [events/anb_racial_admin_mil.txt](../../events/anb_racial_admin_mil.txt) | Administration and military switching events |

## Main Objects And State

| Object | Type | Purpose |
|---|---|---|
| `racial_pop_menu_opened` | flag | Tracks whether racial population menu is open |
| `racial_military_menu_opened` | flag | Tracks whether military menu is open |
| `racial_root_menu_opened` | flag | Tracks main racial interface state |
| `clear_racial_military` | scripted effect | Clears old racial military state before rebuild |
| `reset_racial_military_via_administration` | scripted effect | Rebuilds military state from racial administration choice |
| `update_racial_province_modifier_tolerance` | scripted effect | Refreshes province tolerance state |
| `update_unit_sprites_for_racial_mil` | scripted effect | Updates unit appearance after military changes |
| `has_unmatching_military_to_unit` | scripted trigger | Detects mismatch between racial military and unit tech state |

## Main Implementation Model

### 1. The player-facing interface is a custom GUI system

The racial layer is not just a decision list.

It uses custom GUI windows keyed by flags such as:

- `racial_root_menu_opened`
- `racial_pop_menu_opened`
- `racial_military_menu_opened`

Repo anchor:

- [customgui_racial_interface.txt](../../common/custom_gui/customgui_racial_interface.txt)

That is why the decision file itself comments that players use the button while AI uses menu-routing logic.

### 2. The decision layer mainly opens the menu

The `racial_pop_menu` decision acts as a wrapper:

- AI can use it
- it sets `racial_pop_menu_opened`
- it fires a menu event

Representative shape:

```txt
racial_pop_menu = {
    effect = {
        set_country_flag = racial_pop_menu_opened
        country_event = { id = racial_pop_misc.1 }
    }
}
```

Repo anchor:

- [Racial.txt](../../decisions/Racial.txt)

### 3. Racial military is reset and rebuilt through scripted effects

The system does not trust ad hoc military changes.

Instead, it uses central helpers like:

- `clear_racial_military`
- `reset_racial_military_via_administration`

The scripted effects file explicitly warns that multiple mirror points must stay aligned, including:

- `racial_mil_military_change_tech`
- `racial_modifiers.6`
- `has_unmatching_military_to_unit`

Repo anchors:

- [anb_scripted_effects_for_racial_tolerances.txt:11](../../common/scripted_effects/anb_scripted_effects_for_racial_tolerances.txt#L11)
- [anb_scripted_effects_for_racial_tolerances.txt:1004](../../common/scripted_effects/anb_scripted_effects_for_racial_tolerances.txt#L1004)
- [anb_scripted_effects_for_racial_tolerances.txt:1077](../../common/scripted_effects/anb_scripted_effects_for_racial_tolerances.txt#L1077)

## Real Code Examples

### Example 1. Menu routing and race-variable seeding

`racial_pop_misc.1` is a good example of how the racial menu layer works.

It:

- handles the menu back/close logic
- applies AI cooldowns
- routes into race-specific branches
- seeds variables like `nbCentaurDev`

Repo anchor:

- [anb_racial_pop_misc.txt](../../events/anb_racial_pop_misc.txt)

### Example 2. Military reset and rebuild via administration

In `anb_racial_admin_mil.txt`, racial military branches clear the old system and rebuild from the current administration choice.

Representative shape:

```txt
clear_racial_military = yes
reset_racial_military_via_administration = yes
```

Repo anchor:

- [anb_racial_admin_mil.txt](../../events/anb_racial_admin_mil.txt)

### Example 3. Province and sprite refresh after military change

After racial military changes, the repo updates both province tolerance state and unit visuals:

```txt
every_owned_province = {
    update_racial_province_modifier_tolerance = yes
}
update_unit_sprites_for_racial_mil = yes
```

Repo anchor:

- [anb_racial_admin_mil.txt:1156](../../events/anb_racial_admin_mil.txt#L1156)

### Example 4. Mismatch repair event

`racial_modifiers.6` exists specifically to repair states where racial military choice and actual unit tech do not match.

The file also contains race-specific recovery branches such as an orcish branch setting:

- `change_technology_group = tech_black_orcish`

Repo anchor:

- [anb_racial_admin_mil.txt](../../events/anb_racial_admin_mil.txt)

## How This Differs From A Simpler Vanilla-Style Pattern

Vanilla-style expectation:

- race does not exist as a full administrative system
- unit tech is a national tech question
- population is mostly static

Anbennar pattern:

- racial population has menu routing, variables, and race branches
- racial administration and military are explicit state machines
- military changes require reset, rebuild, and repair logic
- province tolerance and unit visuals are updated as part of the system

## Safe Adaptation Notes

If you want to adapt or extend a racial system:

1. do not patch only one event branch; check the scripted effects and repair triggers too
2. if military tech changes, verify `has_unmatching_military_to_unit` and the repair event still make sense
3. if tolerance logic changes, make sure province update helpers still run
4. if the player should see or control the system, check `common/custom_gui` before touching only decisions
5. prefer copying a full race branch rather than inventing a partial mini-system

## Best Places To Reuse This

- race-specific military or administration choices for custom content
- large population-management interfaces
- systems where a visible menu must coordinate with hidden repair logic
- any nation-specific content that needs race-aware military state
