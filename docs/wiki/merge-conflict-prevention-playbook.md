# Merge-Conflict Prevention Playbook

Purpose: keep merge conflicts rare by planning for overlap up front, then use a consistent resolution decision order when conflicts still happen.

## Prevention-first rules

1. Prefer one active PR per hotspot domain (`docs/wiki/*`, `docs/start-here.md`, `scripts/*`, `.github/workflows/*`, `automation/*`).
2. Before coding on a feature branch, run overlap planning:
   - `python scripts/validate_conflict_hotspots.py`
   - `python scripts/pr_conflict_churn_plan.py --base main --json --focus-branch <your-branch> --fail-on-block`
3. On `block` overlaps (single-writer surfaces), do one of:
   - stack on the existing branch,
   - pick a different non-overlapping task,
   - mark the task blocked/waiting.
4. Keep PRs narrow and single-topic where possible (docs vs automation vs gameplay content).

## Automation layers used by this repo

1. `.gitattributes` uses `merge=union` for selected shared docs hub files.
2. `resolve_docs_conflicts.*` auto-resolves a small docs hotspot set when merging `main` into a branch.
3. `docs_conflict_guard.*` detects leftover merge markers and duplicate hotspot headings.
4. `verne_smoke_checks.*` runs conflict guard automatically as part of the normal smoke flow.

Important limitation: docs auto-resolution is only for known docs hotspots and `.gitattributes`; gameplay conflicts still require human review.

## Conflict resolution decision order

### A) Docs hotspot only

Use this when unresolved files are only docs hotspots or `.gitattributes`:

- `python scripts/resolve_docs_conflicts.py`

Then run:

- `python scripts/docs_conflict_guard.py`

### B) Branch sync with preferred side

Use noob autopilot resolution flags when one side is clearly authoritative:

- Prefer `main` side baseline:
  - `bash scripts/noob_autopilot.sh --prefer-main`
  - `powershell -NoProfile -ExecutionPolicy Bypass -File .\\scripts\\noob_autopilot.ps1 -ResolutionStrategy prefer-main`
- Prefer feature branch in-progress slice:
  - `bash scripts/noob_autopilot.sh --prefer-branch`
  - `powershell -NoProfile -ExecutionPolicy Bypass -File .\\scripts\\noob_autopilot.ps1 -ResolutionStrategy prefer-branch`

### C) Manual review required

Stop and inspect conflict blocks line-by-line when both sides changed behavior/meaning, especially in:

- `missions/Verne_Missions.txt` (mission trigger/effect meaning)
- `events/Flavour_Verne_A33.txt` (event effects, options, and IDs)
- `localisation/Flavour_Verne_A33_l_english.yml` (same-key text reconciliation)

## Pre-PR and pre-push checklist

1. Sync with `main` (autopilot/default flow recommended).
2. Resolve any conflict markers.
3. Run smoke + docs guard + link audit.
4. Confirm no single-writer hotspot overlap was introduced while branch was in flight.

Minimum verification commands:

- `python scripts/docs_conflict_guard.py`
- `python scripts/checklist_link_audit.py`
- `bash scripts/verne_smoke_checks.sh`
