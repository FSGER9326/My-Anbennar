# Pre-PR Validation + Artifact Flow

Use this flow when you want one command that both:

1. runs the existing pre-PR validation gate, and
2. generates machine-readable PR artifacts.

## Commands

- **macOS/Linux (bash):** `bash scripts/pre_pr_with_draft.sh`
- **Windows PowerShell:** `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\pre_pr_with_draft.ps1`

## Generated artifacts

- `automation/reports/validation_report.json`
- `automation/pr/PR_DRAFT.md`

## Notes

- This wrapper composes the existing `scripts/pre_pr_gate.*` checks.
- `scripts/pr_prep.py` will block PR draft generation if the validation report includes unresolved **high-severity** issues.
- You can provide extra artifact URLs for the PR draft by setting `PR_PREP_ARTIFACT_URLS` (comma-separated).
