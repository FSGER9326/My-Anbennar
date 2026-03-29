# Checklist Automation System

Goal: one short index for the checklist automation stack, with a command matrix and deep-dive links.

> [!IMPORTANT]
> ## Default command
> `bash scripts/noob_autopilot.sh`
>
> Run this before pushing; it performs branch sync + conflict guard + smoke checks in one flow.

## Scope covered by this automation stack

- Verne smoke/profile checks
- Checklist manifest audit
- Markdown link audit
- Conflict marker and hotspot heading guard
- Localisation and event ID audits
- Branch sync wrappers for PR branches

## Command matrix

| Task | Bash / Python | PowerShell |
| --- | --- | --- |
| Full default flow (recommended) | `bash scripts/noob_autopilot.sh` | `powershell -NoProfile -ExecutionPolicy Bypass -File .\\scripts\\noob_autopilot.ps1` |
| Verne smoke checks | `bash scripts/verne_smoke_checks.sh` | `powershell -NoProfile -ExecutionPolicy Bypass -File .\\scripts\\verne_smoke_checks.ps1` |
| Country profile smoke runner | `python scripts/country_smoke_runner.py --profile automation/country_profiles/verne.json` | `powershell -NoProfile -ExecutionPolicy Bypass -File .\\scripts\\country_smoke_runner.ps1 -Profile automation/country_profiles/verne.json` |
| Checklist manifest audit | `python scripts/verne_checklist_audit.py` | `powershell -NoProfile -ExecutionPolicy Bypass -File .\\scripts\\verne_checklist_audit.ps1` |
| Markdown link audit | `python scripts/checklist_link_audit.py` | `powershell -NoProfile -ExecutionPolicy Bypass -File .\\scripts\\checklist_link_audit.ps1` |
| Conflict guard | `python scripts/docs_conflict_guard.py` | `powershell -NoProfile -ExecutionPolicy Bypass -File .\\scripts\\docs_conflict_guard.ps1` |
| Localisation audit | `python scripts/localisation_audit.py --file localisation/Flavour_Verne_A33_l_english.yml` | `powershell -NoProfile -ExecutionPolicy Bypass -File .\\scripts\\localisation_audit.ps1 -File localisation/Flavour_Verne_A33_l_english.yml` |
| Event ID audit | `python scripts/event_id_audit.py --file events/Flavour_Verne_A33.txt --file events/verne_overhaul_dynasty_events.txt` | `powershell -NoProfile -ExecutionPolicy Bypass -File .\\scripts\\event_id_audit.ps1 -File events/Flavour_Verne_A33.txt -File events/verne_overhaul_dynasty_events.txt` |
| Feature branch sync helper | `bash scripts/auto_sync_pr_with_main.sh` / `python scripts/auto_sync_pr_with_main.py` | `powershell -NoProfile -ExecutionPolicy Bypass -File .\\scripts\\auto_sync_pr_with_main.ps1` |
| Hotspot overlap planning | `python scripts/validate_conflict_hotspots.py` + `python scripts/pr_conflict_churn_plan.py --base main --json --focus-branch <your-branch> --fail-on-block` | (same Python commands) |

## Deep dives (read when needed)

- Merge conflict prevention and decision flow: [merge-conflict-prevention-playbook.md](./merge-conflict-prevention-playbook.md)
- Automation blindspots and historical fixes: [checklist-automation-blindspots-changelog.md](./checklist-automation-blindspots-changelog.md)
- New contributor onboarding flow and noob-safe commit shaping: [../start-here.md](../start-here.md)

## Safe checkpoint commit rule

Before implementation-heavy pushes, follow the Start Here checkpoint slicing guidance:

- [Safe checkpoint commit rule (Start Here)](../start-here.md#safe-checkpoint-commit-rule)
