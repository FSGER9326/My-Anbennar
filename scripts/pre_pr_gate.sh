#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${REPO_ROOT}"

PYTHON_BIN="${PYTHON_BIN:-python3}"
if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  PYTHON_BIN="python"
fi

VALIDATION_REPORT="${VALIDATION_REPORT:-automation/reports/validation_report.json}"
PR_DRAFT_OUTPUT="${PR_DRAFT_OUTPUT:-automation/pr/PR_DRAFT.md}"
mkdir -p "$(dirname "${VALIDATION_REPORT}")" "$(dirname "${PR_DRAFT_OUTPUT}")"

run_step() {
  local label="$1"
  local cmd="$2"

  echo "${label}"
  if ! eval "${cmd}"; then
    echo
    echo "Pre-PR gate failed."
    echo "Next command: ${cmd}"
    echo "Fix the issue shown above, then re-run: bash scripts/pre_pr_gate.sh"
    exit 1
  fi
}

run_step "[1/5] Docs conflict guard" "${PYTHON_BIN} scripts/docs_conflict_guard.py"
run_step "[2/5] Checklist link audit" "${PYTHON_BIN} scripts/checklist_link_audit.py"
run_step "[3/5] Verne checklist audit" "${PYTHON_BIN} scripts/verne_checklist_audit.py"
run_step "[4/5] Verne country smoke runner" "${PYTHON_BIN} scripts/country_smoke_runner.py --profile automation/country_profiles/verne.json"

cat > "${VALIDATION_REPORT}" <<JSON
{
  "generated_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "overall_status": "pass",
  "checks": [
    {"name":"docs_conflict_guard","command":"${PYTHON_BIN} scripts/docs_conflict_guard.py","status":"pass","severity":"high"},
    {"name":"checklist_link_audit","command":"${PYTHON_BIN} scripts/checklist_link_audit.py","status":"pass","severity":"high"},
    {"name":"verne_checklist_audit","command":"${PYTHON_BIN} scripts/verne_checklist_audit.py","status":"pass","severity":"high"},
    {"name":"country_smoke_runner","command":"${PYTHON_BIN} scripts/country_smoke_runner.py --profile automation/country_profiles/verne.json","status":"pass","severity":"high"}
  ],
  "unresolved_issues": [],
  "artifacts": [
    {"name":"validation-report","path":"${VALIDATION_REPORT}"},
    {"name":"pr-draft","path":"${PR_DRAFT_OUTPUT}"}
  ]
}
JSON

run_step "[5/5] Generate PR draft" "${PYTHON_BIN} scripts/pr_prep.py --validation-report ${VALIDATION_REPORT} --output ${PR_DRAFT_OUTPUT}"

echo "Pre-PR gate passed. Safe to open a PR."
echo "Generated artifacts:"
echo "- Validation report: ${VALIDATION_REPORT}"
echo "- PR draft: ${PR_DRAFT_OUTPUT}"
