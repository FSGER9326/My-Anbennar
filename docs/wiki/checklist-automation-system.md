# Checklist Automation System

Goal: make the repo safer to update without needing to remember a pile of manual steps.

> [!IMPORTANT]
> ## You only need this command
> `bash scripts/noob_autopilot.sh`
>
> Run this before pushing. It performs branch sync/merge handling, conflict guarding, and the full smoke bundle.

## What this system covers

- smoke checks for the active Verne implementation layer
- checklist manifest audits for repo-map tracking
- markdown link audits for internal docs
- conflict-marker detection in docs, scripts, workflows, and `.gitattributes`
- feature-branch sync helpers for updating an open PR branch with `main`
- theorycraft scaffold generation for future country projects

## Automation commands

## Default command (noob-safe)

If you only run one thing before pushing docs or Verne changes, run:

- `bash scripts/noob_autopilot.sh`

This handles sync/merge + conflict flow and then runs the full validation chain, including the Verne smoke bundle.

## Advanced/manual fallback commands

Use this section only when you need manual control, troubleshooting, or platform-specific alternatives.

## Automation commands

### CI trigger note

Localisation-only edits now trigger the `verne-validation` workflow automatically on both pushes and pull requests to `main`.

On pull requests, `verne-validation` gate 3 also runs the overlap planner (`scripts/pr_conflict_churn_plan.py`) with `--focus-branch` + `--fail-on-block`, and publishes both JSON + markdown overlap summaries in job artifacts and step summary.

### Verne smoke checks

- PowerShell: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verne_smoke_checks.ps1`
- Bash: `bash scripts/verne_smoke_checks.sh`

Use this for the normal “did I break the tracked Verne layer?” check.

### Generic country smoke profile

- PowerShell: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\country_smoke_runner.ps1 -Profile automation/country_profiles/verne.json`
- Python: `python scripts/country_smoke_runner.py --profile automation/country_profiles/verne.json`

Use this when you want to run a specific profile directly instead of the full Verne smoke bundle.

Profile rule types (important for noobs):

- `require_patterns`: **any-one** check. Each item has a single regex `pattern`; it passes if that regex appears in at least one listed file path.
- `require_all_patterns`: **all-of** check. Each item has a regex list `patterns`; every entry in that list must match at least one listed file path.
- `forbid_patterns`: negative check. The regex must not appear in any listed file path.

Use `require_all_patterns` whenever you are tracking multiple helper names and you want to fail if even one helper disappears.

#### Verne phase-0 foundation guarantees

The Verne profile now also enforces a phase-0 foundation layer: it requires baseline objects in `common/event_modifiers/verne_overhaul_modifiers.txt` and `localisation/verne_overhaul_l_english.yml`, and blocks common anti-patterns there (merge markers, placeholder TODO keys, and inconsistent Verne prefix typos).

It now also gates new doctrine/reform foundation files:

- `common/ideas/verne_doctrine_groups.txt` must contain at least one `verne_... = {` object.
- `common/government_reforms/verne_overhaul_reforms.txt` must contain at least one `verne_... = {` object.
- Both files must include explicit sentinel IDs (`verne_doctrine_silver_wake` and `verne_court_of_silver_oaths_reform`) so empty stubs fail CI.
- Both files forbid placeholder keys such as `TODO...` and `replace_me...`.

#### Overhaul-required checks

The Verne smoke profile now has an explicit **overhaul-required checks** layer for these files:

- `common/ideas/verne_doctrine_groups.txt`
- `common/government_reforms/verne_overhaul_reforms.txt`
- `events/verne_overhaul_dynasty_events.txt`
- `common/on_actions/verne_overhaul_on_actions.txt`

For those files, CI now enforces both:

1. **Structure sentinels** (object/header shape + named sentinels)
   - doctrine object + `verne_doctrine_silver_wake`
   - reform object + `verne_court_of_silver_oaths_reform`
   - dynasty event object + namespace + `id = verne_overhaul_dynasty.1`
   - on_actions hook object + `on_new_heir`
2. **Safety forbids**
   - unresolved merge markers (`<<<<<<<`, `=======`, `>>>>>>>`)
   - placeholder key prefixes (`TODO...`, `placeholder...`, `replace_me...`, `verne_todo...`, `verne_overhaul_todo...`)

Legacy helper-layer smoke checks are still retained, but now explicitly labelled as **legacy compatibility** in the profile descriptions so it is easier to distinguish old-guard checks from overhaul-required gates.

#### What now fails automatically

The default Verne smoke flow now blocks PRs when any of these tracked files are missing their baseline structure checks or still contain scaffolding/conflict leftovers:

- `common/ideas/verne_doctrine_groups.txt`
- `common/government_reforms/verne_overhaul_reforms.txt`
- `events/verne_overhaul_dynasty_events.txt`
- `common/on_actions/verne_overhaul_on_actions.txt`

Specifically, CI now fails on unresolved merge markers (`<<<<<<<`, `=======`, `>>>>>>>`) and placeholder TODO-style keys (`TODO...`, `placeholder...`, `replace_me...`, `verne_todo...`, `verne_overhaul_todo...`) in those files.

### Checklist manifest audit

- PowerShell: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verne_checklist_audit.ps1`
- Python: `python scripts/verne_checklist_audit.py`

Generic version:

- PowerShell: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\checklist_manifest_audit.ps1 -Manifest <path>`
- Python: `python scripts/checklist_manifest_audit.py --manifest <path>`
- Python (override index files): `python scripts/checklist_manifest_audit.py --manifest <path> --index-file <index-a> --index-file <index-b>`
- Python (explicitly force built-in defaults): `python scripts/checklist_manifest_audit.py --manifest <path> --use-default-index-files`

Python index-file behavior:

- If you pass one or more `--index-file` values, only those files are used.
- If you pass no `--index-file`, the legacy built-in default index list is used for compatibility.
- `--use-default-index-files` is optional explicitness for scripts/wrappers that want to force legacy defaults.

### What manifest coverage now means

Manifest coverage now tracks **roadmap file-family progress**, not just helper-layer success.

- The manifest includes first-wave helper families (`modifiers`, `triggers`, `effects`, and overhaul localisation).
- It also includes first-wave doctrine files, reform files, and integration files (`decisions`, `events`, `on_actions`) pulled from `docs/first-wave-backlog.md`.
- `status` is intentional:
  - `draft` = planned backlog target file not created yet.
  - `active` = current implementation file that already exists and is part of the live tracked layer.
- `scanned` / `mapped` / `verified` should be set conservatively. For newly-added planned targets, start these as `false` until real grounding passes are done.

### Markdown link audit

- PowerShell: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\checklist_link_audit.ps1`
- Python: `python scripts/checklist_link_audit.py`

### Conflict guard

- PowerShell: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\docs_conflict_guard.ps1`
- Python: `python scripts/docs_conflict_guard.py`

This now checks more than docs. It scans:

- `docs/**/*.md`
- `scripts/*.py`
- `scripts/*.ps1`
- `scripts/*.sh`
- `.github/workflows/*`
- `.gitattributes`

It also checks that key docs hub headings only appear once in hotspot files.

### Localisation audit

- PowerShell: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\localisation_audit.ps1 -File localisation/Flavour_Verne_A33_l_english.yml`
- Python: `python scripts/localisation_audit.py --file localisation/Flavour_Verne_A33_l_english.yml`

Checks for beginner mistakes in localisation files:

- missing UTF-8 BOM
- missing/invalid `l_english:`-style header
- duplicate localisation keys across scanned files

### Event ID audit

- PowerShell: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\event_id_audit.ps1 -File events/Flavour_Verne_A33.txt -File events/verne_overhaul_dynasty_events.txt`
- Python: `python scripts/event_id_audit.py --file events/Flavour_Verne_A33.txt --file events/verne_overhaul_dynasty_events.txt`

Checks for common event scripting mistakes:

- event IDs in files that forgot `namespace = ...`
- event IDs that use a namespace not declared in the same file
- duplicate event IDs across scanned files

Coverage note: the default Verne smoke/CI audit now checks both `events/Flavour_Verne_A33.txt` and `events/verne_overhaul_dynasty_events.txt`, and the Verne smoke profile includes an explicit namespace sentinel for the dynasty file so namespace regressions fail fast.

### New country scaffold

- PowerShell: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\new_country_scaffold.ps1 -Slug <country-slug> -Tag <TAG>`
- Bash: `bash scripts/new_country_scaffold.sh <country-slug> <TAG>`

Use this to start a new theorycrafting folder without rebuilding the checklist structure by hand.

## Safe checkpoint commit rule

Before implementation-heavy pushes, follow the noob-safe checkpoint slicing rule from the Start Here guide:

- [Safe checkpoint commit rule (Start Here)](../start-here.md#safe-checkpoint-commit-rule)

Use that section as the default commit-shaping guard so each commit stays one system slice with helper->object->loc->smoke sentinel->ledger structure.

It also documents fast-path exceptions so this rule improves safety without blocking tightly-coupled work.

## Advanced/manual fallback (continued)

### Pre-coding overlap planning check (prevention-only)

Run this before implementation when branch/PR context is available:

- `python scripts/validate_conflict_hotspots.py`
- `python scripts/pr_conflict_churn_plan.py --base main --json --focus-branch <your-branch> --fail-on-block`

Result meaning:

- `block`: overlap on a **true single-writer surface** from `automation/conflict_hotspots.yaml`; stop and coordinate.
- `warn`: overlap on an advisory hotspot; proceed only with explicit coordination and a narrow scope.

Boundary policy (narrowed on purpose):

- Broad trees such as `scripts/`, `docs/wiki/`, and `automation/` are now advisory by default so parallel cleanup/docs work does not hard-block each other.
- `block` severity is reserved for small, high-churn coordination surfaces (for example workflow files and explicit orchestrator entrypoints such as `pre_pr_gate` / `noob_autopilot` wrappers).
- If a path starts generating repeated hard conflicts, promote that exact file (or a small prefix) to single-writer instead of re-expanding whole directory trees.

Required action for `block` overlaps:

1. stack onto the existing branch touching that hotspot, **or**
2. pick a different task outside the hotspot, **or**
3. mark current task blocked/waiting.

`pre_pr_gate` now validates `automation/conflict_hotspots.yaml` first, then runs the overlap planning check (bash + PowerShell variants) when on a feature branch with authenticated `gh`, and exits early on `block` overlaps.

If `gh` is unavailable (or not authenticated), run the overlap planner manually with explicit branch names:

- `python scripts/pr_conflict_churn_plan.py --base main --json --branches <your-branch> <other-branch> --fail-on-block`

Use this fallback to keep overlap planning prevention-oriented without requiring `gh` installation/authentication.

This is intentionally prevention-only: no merge-resolution automation behavior was changed.

## Merge-conflict prevention

The repo now uses a few layers together:

1. `.gitattributes` uses `merge=union` for shared docs hub files that are prone to concurrent edits.
2. `resolve_docs_conflicts.*` can auto-resolve a small hotspot list when you merge `main` into a PR branch.
3. `docs_conflict_guard.*` catches leftover conflict markers and duplicate hotspot headings before you push.
4. `verne_smoke_checks.*` runs the guard automatically as part of the normal smoke flow.

Important limitation:

- auto-resolution is only meant for known docs hotspots and `.gitattributes`
- real content conflicts in gameplay files still need a human decision

### What to do next when conflicts remain (missions/events/localisation)

Use this decision order (only supported helper commands):

1. Run `python scripts/resolve_docs_conflicts.py` **when unresolved files are only docs hotspots / `.gitattributes`**.
2. Run `bash scripts/noob_autopilot.sh --prefer-main` (PowerShell: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\noob_autopilot.ps1 -ResolutionStrategy prefer-main`) **when upstream `main` is the authoritative baseline**.
3. Run `bash scripts/noob_autopilot.sh --prefer-branch` (PowerShell: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\noob_autopilot.ps1 -ResolutionStrategy prefer-branch`) **when your branch holds the intended in-progress feature slice**.
4. Stop and manually inspect each conflict block **when both sides changed behavior or meaning** (mission requirements, event outcomes, localisation phrasing tied to keys).

Concrete file examples:

- `missions/Verne_Missions.txt`: conflicting edits to the same mission `trigger`/`effect` block should be reviewed line-by-line before choosing a side.
- `events/Flavour_Verne_A33.txt`: simultaneous changes to option effects and event IDs should be merged manually to preserve both correctness and flow.
- `localisation/Flavour_Verne_A33_l_english.yml`: conflicting text for the same key should be manually reconciled to match the final scripted behavior.

Final verification command:

- `python scripts/docs_conflict_guard.py`

## Feature-branch sync

Use this when GitHub says your open PR branch is behind `main` or has merge conflicts.

- PowerShell: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\auto_sync_pr_with_main.ps1`
- Python: `python scripts/auto_sync_pr_with_main.py`
- Bash: `bash scripts/auto_sync_pr_with_main.sh`
- Noob autopilot (default): `bash scripts/noob_autopilot.sh`

Noob autopilot fallback flags for stubborn conflicts:

- Prefer main side for unresolved files: `bash scripts/noob_autopilot.sh --prefer-main`
- Prefer branch side for unresolved files: `bash scripts/noob_autopilot.sh --prefer-branch`
- PowerShell equivalents:
  - `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\noob_autopilot.ps1 -ResolutionStrategy prefer-main`
  - `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\noob_autopilot.ps1 -ResolutionStrategy prefer-branch`

### Optional power-user shortcuts (mode scripts)

These are optional convenience wrappers for manual daily use:

- Implementation shortcut:
  - bash: `bash scripts/verne_mode_impl.sh`
  - PowerShell: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verne_mode_impl.ps1`
- Docs shortcut:
  - bash: `bash scripts/verne_mode_docs.sh`
  - PowerShell: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verne_mode_docs.ps1`

What the sync helper does:

1. refuses to run if your working tree is dirty
2. refuses to run on `main`
3. fetches `origin`
4. merges `origin/main` into your current feature branch without auto-committing first
5. tries hotspot auto-resolution if the merge conflicts
6. runs the guard + smoke checks
7. creates the merge commit if there is actually something to commit

### Main branch note

Do **not** use the PR sync helpers while already on `main`.

On `main`, use the simpler flow:

1. `git pull`
2. run the smoke checks
3. `git push`

## Obvious blindspots this fixes

These were the easiest ways the old automation could still fail:

- broken Python helper files passing unnoticed because the guard only scanned docs
- workflow paths pointing at `My-Anbennar/...` even though the repo root is already `My-Anbennar`
- shell scripts depending on executable bits instead of calling `python`/`bash` explicitly
- missing Windows-native scaffold/profile entrypoints
- sync helpers trying to create a merge commit even when already up to date
- duplicated smoke logic drifting across multiple scripts instead of using the JSON profile as the source of truth
