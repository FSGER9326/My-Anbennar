# Checklist Automation System

Goal: make the repo safer to update without needing to remember a pile of manual steps.

## What this system covers

- smoke checks for the active Verne implementation layer
- checklist manifest audits for repo-map tracking
- markdown link audits for internal docs
- conflict-marker detection in docs, scripts, workflows, and `.gitattributes`
- feature-branch sync helpers for updating an open PR branch with `main`
- theorycraft scaffold generation for future country projects

## Safest everyday command

If you only run one thing before pushing docs or Verne changes, run:

- PowerShell: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verne_smoke_checks.ps1`
- Bash: `bash scripts/verne_smoke_checks.sh`

This now runs:

1. the Verne JSON smoke profile
2. the checklist status audit
3. the markdown link audit
4. the docs + automation conflict guard
5. the Verne localisation audit
6. the Verne event ID audit

## Automation commands

### Verne smoke checks

- PowerShell: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verne_smoke_checks.ps1`
- Bash: `bash scripts/verne_smoke_checks.sh`

Use this for the normal “did I break the tracked Verne layer?” check.

### Generic country smoke profile

- PowerShell: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\country_smoke_runner.ps1 -Profile automation/country_profiles/verne.json`
- Python: `python scripts/country_smoke_runner.py --profile automation/country_profiles/verne.json`

Use this when you want to run a specific profile directly instead of the full Verne smoke bundle.

### Checklist manifest audit

- PowerShell: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verne_checklist_audit.ps1`
- Python: `python scripts/verne_checklist_audit.py`

Generic version:

- PowerShell: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\checklist_manifest_audit.ps1 -Manifest <path>`
- Python: `python scripts/checklist_manifest_audit.py --manifest <path>`

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

- PowerShell: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\event_id_audit.ps1 -File events/Flavour_Verne_A33.txt`
- Python: `python scripts/event_id_audit.py --file events/Flavour_Verne_A33.txt`

Checks for common event scripting mistakes:

- event IDs in files that forgot `namespace = ...`
- event IDs that use a namespace not declared in the same file
- duplicate event IDs across scanned files

### New country scaffold

- PowerShell: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\new_country_scaffold.ps1 -Slug <country-slug> -Tag <TAG>`
- Bash: `bash scripts/new_country_scaffold.sh <country-slug> <TAG>`

Use this to start a new theorycrafting folder without rebuilding the checklist structure by hand.

## Merge-conflict prevention

The repo now uses a few layers together:

1. `.gitattributes` uses `merge=union` for shared docs hub files that are prone to concurrent edits.
2. `resolve_docs_conflicts.*` can auto-resolve a small hotspot list when you merge `main` into a PR branch.
3. `docs_conflict_guard.*` catches leftover conflict markers and duplicate hotspot headings before you push.
4. `verne_smoke_checks.*` runs the guard automatically as part of the normal smoke flow.

Important limitation:

- auto-resolution is only meant for known docs hotspots and `.gitattributes`
- real content conflicts in gameplay files still need a human decision

## Feature-branch sync

Use this when GitHub says your open PR branch is behind `main` or has merge conflicts.

- PowerShell: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\auto_sync_pr_with_main.ps1`
- Python: `python scripts/auto_sync_pr_with_main.py`
- Bash: `bash scripts/auto_sync_pr_with_main.sh`

What the sync helper does:

1. refuses to run if your working tree is dirty
2. refuses to run on `main`
3. fetches `origin`
4. merges `origin/main` into your current feature branch without auto-committing first
5. tries hotspot auto-resolution if the merge conflicts
6. runs the guard + smoke checks
7. creates the merge commit if there is actually something to commit

## Main branch note

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
