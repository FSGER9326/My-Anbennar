# Checklist Automation System

Goal: make the repo safer to update without needing to remember a pile of manual steps.

## What this system covers

- smoke checks for the active Verne implementation layer
- checklist manifest audits for repo-map tracking
- markdown link audits for internal docs
- text-hygiene checks for docs and localisation
- conflict-marker detection in docs, scripts, workflows, and `.gitattributes`
- feature-branch sync helpers for updating an open PR branch with `main`
- smart routing so the repo can choose checks based on changed files
- theorycraft scaffold generation for future country projects
- repo-local Git hooks for automatic pre-commit and pre-push checks

## Safest everyday commands

If you only run one thing before pushing Verne work, run:

- PowerShell: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verne_smoke_checks.ps1`
- Bash: `bash scripts/verne_smoke_checks.sh`

If you feel lost before you even start, run:

- PowerShell: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\repo_doctor.ps1`
- Python: `python scripts/repo_doctor.py`

## Automation commands

### Verne smoke checks

- PowerShell: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verne_smoke_checks.ps1`
- Bash: `bash scripts/verne_smoke_checks.sh`

This is the normal "did I break the tracked Verne layer?" check.

It runs:

1. the Verne JSON smoke profile
2. the checklist status audit
3. the markdown link audit
4. the docs + automation conflict guard

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

This checks:

- `docs/**/*.md`
- `scripts/*.py`
- `scripts/*.ps1`
- `scripts/*.sh`
- `.github/workflows/*`
- `.gitattributes`

It also checks that key docs hub headings only appear once in hotspot files.

### Text hygiene guard

- PowerShell: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\text_hygiene_guard.ps1`
- Python: `python scripts/text_hygiene_guard.py`

This catches:

- common mojibake and encoding damage
- replacement characters
- near-duplicate consecutive lines in docs and localisation files

### Repo doctor

- PowerShell: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\repo_doctor.ps1`
- Python: `python scripts/repo_doctor.py`

This is the beginner-friendly repo health summary. It reports:

- branch
- ahead/behind state
- dirty working tree
- merge/rebase state
- tool availability
- whether hooks are installed

### Smart smoke router

- PowerShell: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\smart_smoke_router.ps1`
- Bash: `bash scripts/smart_smoke_router.sh`

This decides which checks to run based on which files changed, so you do not have to remember the right command every time.

### New country scaffold

- PowerShell: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\new_country_scaffold.ps1 -Slug <country-slug> -Tag <TAG>`
- Bash: `bash scripts/new_country_scaffold.sh <country-slug> <TAG>`

Use this to start a new theorycrafting folder without rebuilding the checklist structure by hand.

### Install Git hooks

- PowerShell: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install_git_hooks.ps1`
- Bash: `bash scripts/install_git_hooks.sh`

This installs repo-local hooks from `.githooks/` so checks run automatically before commit and push.

Important Windows note:

- if Git commit or push starts failing with a Git shell / `signal pipe` error, disable hooks again and use the manual commands instead

Disable hooks:

- PowerShell: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\uninstall_git_hooks.ps1`
- Bash: `bash scripts/uninstall_git_hooks.sh`

Manual fallback:

- PowerShell: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\smart_smoke_router.ps1`
- PowerShell: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verne_smoke_checks.ps1`

## Merge-conflict prevention

The repo now uses a few layers together:

1. `.gitattributes` uses `merge=union` for shared docs hub files that are prone to concurrent edits.
2. `resolve_docs_conflicts.*` can auto-resolve a small hotspot list when you merge `main` into a PR branch.
3. `docs_conflict_guard.*` catches leftover conflict markers and duplicate hotspot headings before you push.
4. `verne_smoke_checks.*` runs the guard automatically as part of the normal smoke flow.
5. `.githooks/pre-commit` and `.githooks/pre-push` can run the smart router automatically once installed.

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
2. run `repo_doctor`
3. run the smoke checks
4. `git push`

## Obvious blindspots this fixes

These were the easiest ways the old automation could still fail:

- broken helper files passing unnoticed because the guard only scanned docs
- workflow paths pointing at `My-Anbennar/...` even though the repo root is already `My-Anbennar`
- shell scripts depending on executable bits instead of calling `python` or `bash` explicitly
- missing Windows-native scaffold and profile entrypoints
- sync helpers trying to create a merge commit even when already up to date
- duplicated smoke logic drifting across multiple scripts instead of using the JSON profile as the source of truth
- docs or localisation quietly accumulating mojibake and duplicate lines
- no local hook installation path, so checks were easy to forget
- GitHub PRs having no built-in checklist or risk prompt
