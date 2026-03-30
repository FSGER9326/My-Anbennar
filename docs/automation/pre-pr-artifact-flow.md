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
- `scripts/write_validation_report.py` is the shared report writer for both shell families and CI, so the JSON shape stays consistent.
- `scripts/pr_prep.py` will block PR draft generation if the validation report includes unresolved **high-severity** issues.
- You can provide extra artifact URLs for the PR draft by setting `PR_PREP_ARTIFACT_URLS` (comma-separated).
- GitHub Actions now uploads both generated artifacts and links the workflow run back into the validation report for easier PR handoff.

## CI behavior

The workflow `.github/workflows/verne-validation.yml` now:

1. runs the pre-PR validation wrapper on Ubuntu,
2. writes a machine-readable validation report,
3. generates `automation/pr/PR_DRAFT.md`,
4. uploads both files as workflow artifacts,
5. writes a short job summary for quick triage in the Actions UI, and
6. runs a separate CWTools EU4 validation job with `output.json` uploaded as its own artifact.

That means local and CI flows now share the same artifact format instead of maintaining separate report logic, while Clausewitz-native validation now runs alongside the repo’s custom smoke checks rather than replacing them.
