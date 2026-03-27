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
2. `./scripts/verne_checklist_audit.py`
   - validates manifest structure + file existence + index consistency
3. `./scripts/checklist_manifest_audit.py --manifest <path>`
   - generic audit command for non-Verne country manifests
4. `./scripts/checklist_link_audit.py`
   - verifies local markdown checklist/workflow links are not broken
5. `./scripts/auto_sync_pr_with_main.sh`
   - fetches `origin/main`, attempts conflict-safe merge, auto-resolves docs hotspots, then runs guards

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

This does **not** remove all conflicts, but it catches common failure cases before PR merge.

### Fastest conflict-safe update flow (existing PR)

Use this when GitHub shows merge conflicts on your open PR:

1. `./scripts/auto_sync_pr_with_main.sh`
2. if it reports remaining manual conflicts, resolve only those files and rerun:
   - `./scripts/docs_conflict_guard.py`
   - `./scripts/verne_smoke_checks.sh`
3. `git push`

You do **not** need a new PR if you are pushing to the same branch.
