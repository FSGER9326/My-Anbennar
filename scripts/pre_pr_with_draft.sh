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

echo "[1/3] Run pre-PR gate"
bash scripts/pre_pr_gate.sh

echo "[2/3] Write machine-readable validation report"
"${PYTHON_BIN}" scripts/write_validation_report.py \
  --output "${VALIDATION_REPORT}" \
  --overall-status "pass" \
  --check "docs_conflict_guard|${PYTHON_BIN} scripts/docs_conflict_guard.py|pass|high" \
  --check "checklist_link_audit|${PYTHON_BIN} scripts/checklist_link_audit.py|pass|high" \
  --check "verne_checklist_audit|${PYTHON_BIN} scripts/verne_checklist_audit.py|pass|high" \
  --check "country_smoke_runner|${PYTHON_BIN} scripts/country_smoke_runner.py --profile automation/country_profiles/verne.json|pass|high" \
  --artifact "validation-report|${VALIDATION_REPORT}" \
  --artifact "pr-draft|${PR_DRAFT_OUTPUT}"

echo "[3/3] Generate PR draft"
"${PYTHON_BIN}" scripts/pr_prep.py --validation-report "${VALIDATION_REPORT}" --output "${PR_DRAFT_OUTPUT}"

echo "Pre-PR + draft flow passed."
echo "- Validation report: ${VALIDATION_REPORT}"
echo "- PR draft: ${PR_DRAFT_OUTPUT}"
