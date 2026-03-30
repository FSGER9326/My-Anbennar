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

## Hard overlap rules for parallel tasks

Two parallel tasks must not touch the same:
- mission file
- helper file
- localisation file
- single-writer hotspot

Explicit single-writer helper rule for gameplay PRs:
- Allow only **one active gameplay PR touching helper surfaces** at a time for:
  - `common/scripted_triggers/verne_overhaul_triggers.txt`
  - `common/scripted_effects/verne_overhaul_effects.txt`
  - `localisation/verne_overhaul_l_english.yml`
- If a gameplay PR already owns any helper surface above, other gameplay PRs must either:
  - avoid these helper files entirely, or
  - stack on that same branch/PR instead of running in parallel.

Single-writer and hotspot policy is defined in `automation/conflict_hotspots.yaml`; treat it as the current source of truth.

## How to choose safe parallel tasks

1. Start with one task per lane.
2. Before work starts, compare touched-file lists for overlap in mission/helper/localisation files and single-writer hotspots.
3. If overlap is detected, stack on one branch or mark one task blocked/waiting.
4. Keep automation/onboarding/workflow updates in a dedicated serial slice.
5. Keep each PR narrow so lane ownership and conflict risk are obvious.

## Practical default split

- **Lane A (gameplay):** one focused implementation slice.
  - Keep helper-only or helper-heavy changes isolated where possible.
  - Avoid simultaneous helper + mission edits across parallel gameplay PRs; if helper files are touched, do not run another PR touching mission files in parallel unless intentionally stacked.
- **Lane B (lore/docs):** documentation updates that do not touch gameplay files.
- **Lane C (reference):** optional repo-map/crosswalk refresh.
- **Automation lane:** run as a separate serial task when needed.
