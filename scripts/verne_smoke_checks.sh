#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-python3}"

if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  PYTHON_BIN="python"
fi

echo "[1/4] Run Verne smoke profile"
"${PYTHON_BIN}" scripts/country_smoke_runner.py --profile automation/country_profiles/verne.json

echo "[2/4] Run checklist status audit"
"${PYTHON_BIN}" scripts/verne_checklist_audit.py

echo "[3/4] Run checklist markdown link audit"
"${PYTHON_BIN}" scripts/checklist_link_audit.py

echo "[4/4] Run docs + automation conflict guard"
"${PYTHON_BIN}" scripts/docs_conflict_guard.py

echo "All Verne smoke checks passed."
