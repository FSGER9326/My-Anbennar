# Checklist Automation System

Goal: provide the **system overview** and a compact **operational command index** for checklist automation.

> [!IMPORTANT]
> **Default operation command:**
> `bash scripts/noob_autopilot.sh`

## System overview

The automation stack coordinates:

- branch sync wrappers for active PR branches,
- overlap-planning checks for conflict-prone hotspots,
- Verne smoke/profile checks,
- checklist manifest and markdown link audits,
- conflict marker and hotspot heading guards,
- localisation and event ID audits.

## Operational command index

### Primary entrypoint

- `bash scripts/noob_autopilot.sh`
- `powershell -NoProfile -ExecutionPolicy Bypass -File .\\scripts\\noob_autopilot.ps1`

### Focused operations

- Verne smoke checks:
  - `bash scripts/verne_smoke_checks.sh`
  - `powershell -NoProfile -ExecutionPolicy Bypass -File .\\scripts\\verne_smoke_checks.ps1`
- Country profile smoke runner:
  - `python scripts/country_smoke_runner.py --profile automation/country_profiles/verne.json`
  - `powershell -NoProfile -ExecutionPolicy Bypass -File .\\scripts\\country_smoke_runner.ps1 -Profile automation/country_profiles/verne.json`
- Checklist manifest audit:
  - `python scripts/verne_checklist_audit.py`
  - `powershell -NoProfile -ExecutionPolicy Bypass -File .\\scripts\\verne_checklist_audit.ps1`
- Markdown link audit:
  - `python scripts/checklist_link_audit.py`
  - `powershell -NoProfile -ExecutionPolicy Bypass -File .\\scripts\\checklist_link_audit.ps1`
- Conflict guard:
  - `python scripts/docs_conflict_guard.py`
  - `powershell -NoProfile -ExecutionPolicy Bypass -File .\\scripts\\docs_conflict_guard.ps1`
- Localisation audit:
  - `python scripts/localisation_audit.py --file localisation/Flavour_Verne_A33_l_english.yml`
  - `powershell -NoProfile -ExecutionPolicy Bypass -File .\\scripts\\localisation_audit.ps1 -File localisation/Flavour_Verne_A33_l_english.yml`
- Event ID audit:
  - `python scripts/event_id_audit.py --file events/Flavour_Verne_A33.txt --file events/verne_overhaul_dynasty_events.txt`
  - `powershell -NoProfile -ExecutionPolicy Bypass -File .\\scripts\\event_id_audit.ps1 -File events/Flavour_Verne_A33.txt -File events/verne_overhaul_dynasty_events.txt`
- Feature-branch sync helper:
  - `bash scripts/auto_sync_pr_with_main.sh`
  - `python scripts/auto_sync_pr_with_main.py`
  - `powershell -NoProfile -ExecutionPolicy Bypass -File .\\scripts\\auto_sync_pr_with_main.ps1`
- Overlap planning:
  - `python scripts/validate_conflict_hotspots.py`
  - `python scripts/pr_conflict_churn_plan.py --base main --json --focus-branch <your-branch> --fail-on-block`

## Related references

- Minimal newcomer flow (no extra workflow prose): [../start-here.md](../start-here.md)
- Conflict decision playbook: [merge-conflict-prevention-playbook.md](./merge-conflict-prevention-playbook.md)
- Parallel lane model (safe task splitting): [parallelization-lanes-playbook.md](./parallelization-lanes-playbook.md)
- Automation blindspots history: [checklist-automation-blindspots-changelog.md](./checklist-automation-blindspots-changelog.md)
