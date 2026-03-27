# Magic Projects Reference

This article maps the Anbennar magic project framework as it exists in the repo.

It is a repo-grounding article, not a proposal for new projects.

## Quick Verdict

Magic projects are not individual one-off events.

They are a reusable framework built from:

1. a project-start helper
2. shared advancement state
3. per-project flags and level variables
4. a central dispatcher event
5. per-project handler namespaces
6. optional milestone branches at specific progress percentages
7. cleanup helpers that reset or abort the shared advancement state

That makes magic projects one of the clearest reusable "button plus variable plus event family" systems in Anbennar.

## Core Files

| File | Role |
|---|---|
| [common/scripted_effects/anb_scripted_effects_for_magic_system.txt](../../common/scripted_effects/anb_scripted_effects_for_magic_system.txt) | Shared start, progress, completion, and cleanup helpers |
| [common/scripted_effects/anb_scripted_effects_for_magic_project.txt](../../common/scripted_effects/anb_scripted_effects_for_magic_project.txt) | Project-specific helper support |
| [events/Magic_System_Events.txt](../../events/Magic_System_Events.txt) | Shared dispatcher and level-up routing |
| [events/Magic_Project_Events.txt](../../events/Magic_Project_Events.txt) | Main project namespaces and per-project handlers |
| [common/custom_gui/magic_unique_projects.txt](../../common/custom_gui/magic_unique_projects.txt) | UI side of the project system |
| [common/on_actions/00_on_actions.txt](../../common/on_actions/00_on_actions.txt) | Project progress trackers tied to combat and other world actions |

## Main Objects And State

| Object | Type | Purpose |
|---|---|---|
| `start_magic_project` | scripted effect | Starts a project and seeds its state |
| `magic_project_level_up` | scripted effect | Advances project level and fires the project handler |
| `magic_advancement_abort_all_effect` | scripted effect | Clears shared advancement state on cancel or completion |
| `magic_system.100` | event | Central dispatcher for project progress |
| `magic_project_<project>.0` | event convention | Project-specific main handler |
| `magic_project` | flag | Shared "currently in project mode" marker |
| `<project>_project` | flag | Active project selector |
| `<project>_level` | variable | Tracks project level |
| `current_experience_percent` | variable | Shared milestone/progress tracking |

## Main Implementation Model

### 1. Projects are started by a shared helper

`start_magic_project` centralizes the project start flow.

It typically:

- sets the shared `magic_project` flag
- sets the specific `<project>_project` flag
- resets or initializes advancement state
- can seed school advancement data
- can fire optional entry events
- sets experience targets for the project

Representative shape:

```txt
start_magic_project = {
    project = orb_of_omniscience
}
```

Repo anchor:

- [anb_scripted_effects_for_magic_system.txt:632](../../common/scripted_effects/anb_scripted_effects_for_magic_system.txt#L632)

### 2. Progress is dispatched through a central event

Project advancement is not hardwired separately for every project.

Instead, `magic_system.100` checks the active project flag and routes advancement through a shared helper:

```txt
magic_project_level_up = {
    project = orb_of_omniscience
}
```

Repo anchor:

- [Magic_System_Events.txt:675](../../events/Magic_System_Events.txt#L675)

### 3. Completion and milestone logic live in project namespaces

Each project family uses a naming convention:

- `namespace = magic_project_<project_key>`
- handler event `magic_project_<project_key>.0`

Those handlers are responsible for:

- final completion outcomes
- 33% / 67% or other milestone branches
- project-specific side effects

Repo anchor:

- [Magic_Project_Events.txt](../../events/Magic_Project_Events.txt)

### 4. Cleanup is centralized

Shared project state is cleaned up by `magic_advancement_abort_all_effect`.

This is important because the system uses a lot of shared state, not only project-local state.

The helper is used on:

- cancellation
- abort
- completion

Repo anchor:

- [anb_scripted_effects_for_magic_system.txt:392](../../common/scripted_effects/anb_scripted_effects_for_magic_system.txt#L392)

## Real Code Examples

### Example 1. Orb of Omniscience project

This is one of the clearest full project examples.

It uses:

- the shared project framework
- a project namespace
- milestone branches at `33` and `67`
- a final completion branch

Project namespace anchor:

- [Magic_Project_Events.txt:2069](../../events/Magic_Project_Events.txt#L2069)

### Example 2. Battlemage Academy project

This project also uses the standard handler shape with:

- shared routing
- project-local namespace
- milestone branches
- a completion result

Repo anchor:

- [Magic_Project_Events.txt:3063](../../events/Magic_Project_Events.txt#L3063)

### Example 3. Non-standard milestone projects

Not every project is locked to the same exact threshold pattern.

Examples:

- Great Storm uses milestone values such as `25` and `50`
- Black Herd lichdom content mixes `33`, `50`, and `67`

Repo anchors:

- [Magic_Project_Events.txt:9439](../../events/Magic_Project_Events.txt#L9439)
- [Magic_Project_Events.txt:9451](../../events/Magic_Project_Events.txt#L9451)
- [Magic_Project_Events.txt:9612](../../events/Magic_Project_Events.txt#L9612)
- [Magic_Project_Events.txt:9617](../../events/Magic_Project_Events.txt#L9617)
- [Magic_Project_Events.txt:9623](../../events/Magic_Project_Events.txt#L9623)

### Example 4. On-action progress trackers

Some projects gain progress through world actions instead of only direct menu use.

Example:

- `orb_of_omniscience_progress_tracker` is tied to battle kill/loss hooks

Repo anchor:

- [00_on_actions.txt:3475](../../common/on_actions/00_on_actions.txt#L3475)

## Useful Framework Notes From The Repo

The project event file itself documents the intended framework:

- project systems are built as button plus variable plus event chain
- each project should have its own namespace
- `magic_system.100` is the dispatcher to extend
- cleanup must be mirrored in the shared abort helper

Repo anchor:

- [Magic_Project_Events.txt](../../events/Magic_Project_Events.txt)

## How This Differs From A Simpler Vanilla-Style Pattern

Vanilla-style expectation:

- click decision
- fire event
- receive reward

Anbennar project pattern:

- project start is centralized
- shared progress state is tracked with variables and flags
- advancement is routed by a dispatcher
- completion logic lives in project families
- milestones can fire partial outcomes
- progress can come from menu actions, passive systems, or on-actions

## Safe Adaptation Notes

If you want to build or adapt a project:

1. start from the existing project framework rather than inventing a bespoke chain
2. add the project flag and level routing to the shared dispatcher
3. create a `magic_project_<project>.0` namespace handler
4. add cleanup support to the abort helper if the project adds shared state
5. use on-actions only when the project fantasy really depends on world-action progress

## Best Places To Reuse This

- Verne magical institutions or Red Court arcana projects
- staged ruler/heir magical training tracks
- monument- or reform-linked magical unlock projects
- long-form artifact or relic progression systems
