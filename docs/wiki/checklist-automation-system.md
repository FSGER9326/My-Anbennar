# Checklist Automation System (Plain-Language)

Goal: make checklists executable, not just readable.

## What this system does

Instead of relying only on markdown instructions, we now keep a machine-readable manifest:

- `docs/repo-maps/checklist-status-manifest.json`

Each item records flags:

- `scanned`
- `mapped`
- `verified`
- plus `status` and automation mode.

## Automation commands

Run from repo root:

1. `./scripts/verne_smoke_checks.sh`
   - fast wiring/ID/index checks
   - PowerShell: `powershell -ExecutionPolicy Bypass -File .\scripts\verne_smoke_checks.ps1`
2. `./scripts/verne_checklist_audit.py`
   - validates manifest structure + file existence + index consistency
   - PowerShell: `powershell -ExecutionPolicy Bypass -File .\scripts\verne_checklist_audit.ps1`
3. `./scripts/checklist_manifest_audit.py --manifest <path>`
   - generic audit command for non-Verne country manifests
   - PowerShell: `powershell -ExecutionPolicy Bypass -File .\scripts\checklist_manifest_audit.ps1 -Manifest <path>`
4. `./scripts/checklist_link_audit.py`
   - verifies local markdown checklist/workflow links are not broken
   - PowerShell: `powershell -ExecutionPolicy Bypass -File .\scripts\checklist_link_audit.ps1`
5. PR/main sync helpers
   - Python: `python scripts/auto_sync_pr_with_main.py`
   - Bash: `./scripts/auto_sync_pr_with_main.sh`
   - PowerShell: `powershell -ExecutionPolicy Bypass -File .\scripts\auto_sync_pr_with_main.ps1`
   - purpose: fetch `origin/main`, attempt conflict-safe merge into the current feature branch, auto-resolve docs hotspots, then run guards/checks

`verne_smoke_checks.sh` now calls the checklist audit script automatically.
`verne_smoke_checks.ps1` does the same for the Windows/PowerShell workflow.
2. `./scripts/verne_checklist_audit.py`
   - validates manifest structure + file existence + index consistency
3. `./scripts/checklist_manifest_audit.py --manifest <path>`
   - generic audit command for non-Verne country manifests
4. `./scripts/checklist_link_audit.py`
   - verifies local markdown checklist/workflow links are not broken
5. `python scripts/auto_sync_pr_with_main.py`
   - cross-platform sync helper (Windows/macOS/Linux) for merging `origin/main`, auto-resolving docs hotspots, and running guards
6. `./scripts/auto_sync_pr_with_main.sh`
   - shell version of the same flow (useful in bash environments)

`verne_smoke_checks.sh` now calls the checklist audit script automatically.

## Why this helps

- prevents checklist drift,
- gives clear active/verified state per tracked item,
- makes AI/human sessions easier to hand off safely.

## Workflow rule

When adding a new Verne repo-map/checklist item:

1. add the markdown file,
2. register in the 3 repo-map index files,
3. add/update manifest entry with flags,
4. run `./scripts/verne_smoke_checks.sh`.


## Reuse for another country

Create a starter pack with:

- `./scripts/new_country_scaffold.sh <country-slug> <TAG>`

This creates a theorycrafting folder with plan + manifest templates so you can move from theorycrafting to implementation without rebuilding process from scratch.


## How "keep working" decides next task

When told to keep working by playbook:

1. run automation checks,
2. find the highest-priority item still incomplete (manifest/roadmap),
3. ship one safe slice,
4. rerun checks and report what changed + why it matters.

This keeps progress iterative (high quantity) while preserving safety (high quality).

## Merge-conflict prevention (docs hotspots)

To reduce repeated merge conflicts in docs index files:

1. `.gitattributes` uses `merge=union` for known hotspot files (docs hubs/indexes).
2. `./scripts/docs_conflict_guard.py` checks for leftover conflict markers and accidental duplicated section headings.
3. `./scripts/verne_smoke_checks.sh` runs this guard automatically.
4. `.\scripts\docs_conflict_guard.ps1` and `.\scripts\verne_smoke_checks.ps1` provide the same checks for Windows/PowerShell use.

This does **not** remove all conflicts, but it catches common failure cases before PR merge.

## Fastest conflict-safe update flow (existing PR branch)

Use this when GitHub shows merge conflicts on your open PR branch:

1. run one sync helper:
   - `python scripts/auto_sync_pr_with_main.py`
   - or `./scripts/auto_sync_pr_with_main.sh`
   - or `powershell -ExecutionPolicy Bypass -File .\scripts\auto_sync_pr_with_main.ps1`
2. if it reports remaining manual conflicts, resolve only those files and rerun:
   - `./scripts/docs_conflict_guard.py`
   - `./scripts/verne_smoke_checks.sh`
   - PowerShell:
     - `powershell -ExecutionPolicy Bypass -File .\scripts\docs_conflict_guard.ps1`
     - `powershell -ExecutionPolicy Bypass -File .\scripts\verne_smoke_checks.ps1`

This does **not** remove all conflicts, but it catches common failure cases before PR merge.

### Fastest conflict-safe update flow (existing PR)

Use this when GitHub shows merge conflicts on your open PR:

1. `python scripts/auto_sync_pr_with_main.py` (recommended cross-platform)
   - or `./scripts/auto_sync_pr_with_main.sh` in bash
2. if it reports remaining manual conflicts, resolve only those files and rerun:
   - `./scripts/docs_conflict_guard.py`
   - `./scripts/verne_smoke_checks.sh`
3. `git push`

You do **not** need a new PR if you are pushing to the same branch.

## Main branch note

- If you are already on `main`, do **not** use the PR sync helpers.
- On `main`, use a normal `git pull`, run checks, then `git push`.
- The PR sync helpers are only for feature branches that already have, or will have, a PR.

### PowerShell note (Windows)

If you are in PowerShell, `.sh` files are not executed directly.
Use `python scripts/auto_sync_pr_with_main.py` instead.
