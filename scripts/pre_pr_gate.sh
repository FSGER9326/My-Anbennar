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

declare -a CHECK_RECORDS=()

record_check() {
  local name="$1"
  local command="$2"
  local status="$3"
  local severity="$4"
  CHECK_RECORDS+=("{\"name\":\"${name}\",\"command\":\"${command}\",\"status\":\"${status}\",\"severity\":\"${severity}\"}")
}

write_validation_report() {
  local overall_status="$1"
  local unresolved_issues_json="$2"
  {
    echo "{"
    echo "  \"generated_at\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\","
    echo "  \"overall_status\": \"${overall_status}\","
    echo "  \"checks\": ["
    local idx=0
    for rec in "${CHECK_RECORDS[@]}"; do
      if [[ ${idx} -gt 0 ]]; then
        echo ","
      fi
      printf "    %s" "${rec}"
      idx=$((idx + 1))
    done
    echo
    echo "  ],"
    echo "  \"unresolved_issues\": ${unresolved_issues_json},"
    echo "  \"artifacts\": ["
    echo "    {\"name\":\"validation-report\",\"path\":\"${VALIDATION_REPORT}\"},"
    echo "    {\"name\":\"pr-draft\",\"path\":\"${PR_DRAFT_OUTPUT}\"}"
    echo "  ]"
    echo "}"
  } > "${VALIDATION_REPORT}"
}

run_step() {
  local label="$1"
  local name="$2"
  local cmd="$3"
  local severity="${4:-high}"

  echo "${label}"
  if ! eval "${cmd}"; then
    record_check "${name}" "${cmd}" "fail" "${severity}"
    write_validation_report "fail" "[{\"title\":\"${name} failed\",\"severity\":\"${severity}\",\"resolved\":false}]"
    echo
    echo "Pre-PR gate failed."
    echo "Next command: ${cmd}"
    echo "Fix the issue shown above, then re-run: bash scripts/pre_pr_gate.sh"
    exit 1
  fi
  record_check "${name}" "${cmd}" "pass" "${severity}"
}

run_step "[1/5] Docs conflict guard" "docs_conflict_guard" "${PYTHON_BIN} scripts/docs_conflict_guard.py"
run_step "[2/5] Checklist link audit" "checklist_link_audit" "${PYTHON_BIN} scripts/checklist_link_audit.py"
run_step "[3/5] Verne checklist audit" "verne_checklist_audit" "${PYTHON_BIN} scripts/verne_checklist_audit.py"
run_step "[4/5] Verne country smoke runner" "country_smoke_runner" "${PYTHON_BIN} scripts/country_smoke_runner.py --profile automation/country_profiles/verne.json"
write_validation_report "pass" "[]"
run_step "[5/5] Generate PR draft" "pr_prep" "${PYTHON_BIN} scripts/pr_prep.py --validation-report ${VALIDATION_REPORT} --output ${PR_DRAFT_OUTPUT}" "medium"
write_validation_report "pass" "[]"

echo "Pre-PR gate passed. Safe to open a PR."
echo "Generated artifacts:"
echo "- Validation report: ${VALIDATION_REPORT}"
echo "- PR draft: ${PR_DRAFT_OUTPUT}"
