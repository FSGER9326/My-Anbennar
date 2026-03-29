# Parallelization Lanes Playbook

Purpose: define safe, practical parallel work lanes that reduce merge conflicts while keeping delivery velocity high.

## Lane model (default)

Use at most one active task per lane unless there is explicit coordination.

### 1) Gameplay lane

Scope: gameplay implementation under `common/`, `events/`, `missions/`, `decisions/`, and `localisation/`.

Use this lane for mechanical behavior changes, scripted logic, and gameplay-facing content implementation.

### 2) Lore/docs lane

Scope: lore/design/explanatory docs (for example `docs/lore/`, `docs/design/`, dossiers, and template docs).

Use this lane for canon notes, design rationale, and player-facing explanation work. Avoid gameplay file edits unless explicitly approved for combined work.

### 3) Reference lane

Scope: repo maps and implementation references (for example `docs/repo-maps/` and `docs/implementation-crosswalk.md`).

Use this lane for mapping where systems live and how implementation ownership is structured.

### 4) Automation lane (mostly serial)

Scope: onboarding/workflow/hotspot/validation infrastructure (`docs/start-here.md`, `docs/wiki/checklist-automation-system.md`, `automation/`, `scripts/`, `.github/workflows/`).

This lane is mostly serial and should not be parallelized casually.

## Heavy automation posture (default direction)

Use lane planning to move toward automation-heavy modding support, not just manual prose updates.

Target outcomes:
- machine-checkable repo mapping for implementation ownership and helper reuse
- structured lore/system/playstyle mapping that can be transformed into implementation-ready specs
- guarded prose-to-modfile pipelines that generate draft content, then run audits before acceptance
- continuously expanding reference context so future modding becomes easier and lower-risk

Practical split for this posture:
- lore/docs lane produces structured source prose
- reference lane normalizes and maps that prose to canonical implementation anchors
- automation lane owns generation/validation workflow changes (serial)
- gameplay lane applies accepted generated drafts or mapped implementation slices

## Hard overlap rules for parallel tasks

Two parallel tasks must not touch the same:
- mission file
- helper file
- localisation file
- single-writer hotspot

Single-writer and hotspot policy is defined in `automation/conflict_hotspots.yaml`; treat it as the current source of truth.

## How to choose safe parallel tasks

1. Start with one task per lane.
2. Before work starts, compare touched-file lists for overlap in mission/helper/localisation files and single-writer hotspots.
3. If overlap is detected, stack on one branch or mark one task blocked/waiting.
4. Keep automation/onboarding/workflow updates in a dedicated serial slice.
5. Keep each PR narrow so lane ownership and conflict risk are obvious.
6. For automation-heavy expansion, change one pipeline layer at a time (mapping, generation, or validation), not all at once.

## Practical default split

- **Lane A (gameplay):** one focused implementation slice.
- **Lane B (lore/docs):** structured documentation updates that do not touch gameplay files.
- **Lane C (reference):** repo-map/crosswalk refresh aligned to current canonical ownership.
- **Automation lane:** separate serial task for script/workflow/onboarding changes.
