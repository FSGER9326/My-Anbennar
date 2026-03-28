#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${REPO_ROOT}"

PYTHON_BIN="${PYTHON_BIN:-python3}"
if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  PYTHON_BIN="python"
fi

print_post_fail_summary() {
  local tmp_file
  local loc_rc=0
  local event_rc=0

  echo "Quick triage summary (priority order):"

  if [[ -n "$(git diff --name-only --diff-filter=U)" ]]; then
    echo "1) merge conflicts -> git diff --name-only --diff-filter=U ; Why first: unresolved merges can invalidate every later check."
  fi

  tmp_file="$(mktemp)"
  if ! "${PYTHON_BIN}" scripts/docs_conflict_guard.py >"${tmp_file}" 2>&1; then
    echo "2) conflict markers -> ${PYTHON_BIN} scripts/docs_conflict_guard.py ; Why first: marker leftovers break parsing and hide real logic errors."
  fi

  if ! bash scripts/verne_smoke_checks.sh >"${tmp_file}" 2>&1; then
    echo "3) syntax/structure checks -> bash scripts/verne_smoke_checks.sh ; Why first: structural failures must clear before deeper content audits."
  fi

  "${PYTHON_BIN}" scripts/localisation_audit.py >"${tmp_file}" 2>&1 || loc_rc=$?
  "${PYTHON_BIN}" scripts/event_id_audit.py >"${tmp_file}" 2>&1 || event_rc=$?
  if [[ ${loc_rc} -ne 0 ]]; then
    echo "4) localisation/event ID checks -> ${PYTHON_BIN} scripts/localisation_audit.py ; Why first: broken localisation keys block text integrity checks before ID cleanup."
  elif [[ ${event_rc} -ne 0 ]]; then
    echo "4) localisation/event ID checks -> ${PYTHON_BIN} scripts/event_id_audit.py ; Why first: duplicate/missing event IDs can break runtime event flow even after syntax passes."
  fi

  rm -f "${tmp_file}"
}

run_step() {
  local label="$1"
  local cmd="$2"

  echo "${label}"
  if ! eval "${cmd}"; then
    echo
    echo "Pre-PR gate failed."
    print_post_fail_summary
    echo "Next command: ${cmd}"
    echo "Fix the issue shown above, then re-run: bash scripts/pre_pr_gate.sh"
    exit 1
  fi
}

run_step "[1/4] Docs conflict guard" "${PYTHON_BIN} scripts/docs_conflict_guard.py"
run_step "[2/4] Checklist link audit" "${PYTHON_BIN} scripts/checklist_link_audit.py"
run_step "[3/4] Verne checklist audit" "${PYTHON_BIN} scripts/verne_checklist_audit.py"
run_step "[4/4] Verne country smoke runner" "${PYTHON_BIN} scripts/country_smoke_runner.py --profile automation/country_profiles/verne.json"

echo "Pre-PR gate passed. Safe to open a PR."
