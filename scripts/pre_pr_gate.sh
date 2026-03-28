#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${REPO_ROOT}"

PYTHON_BIN="${PYTHON_BIN:-python3}"
if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  PYTHON_BIN="python"
fi

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

run_step "[1/4] Docs conflict guard" "${PYTHON_BIN} scripts/docs_conflict_guard.py"
run_step "[2/4] Checklist link audit" "${PYTHON_BIN} scripts/checklist_link_audit.py"
run_step "[3/4] Verne checklist audit" "${PYTHON_BIN} scripts/verne_checklist_audit.py"
run_step "[4/4] Verne country smoke runner" "${PYTHON_BIN} scripts/country_smoke_runner.py --profile automation/country_profiles/verne.json"

echo "Pre-PR gate passed. Safe to open a PR."
