#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-python3}"
VERNE_SMOKE_PROFILE="${VERNE_SMOKE_PROFILE:-automation/country_profiles/verne.json}"

if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  PYTHON_BIN="python"
fi

echo "[1/6] Run Verne smoke profile"
"${PYTHON_BIN}" scripts/country_smoke_runner.py --profile "${VERNE_SMOKE_PROFILE}"

echo "[2/6] Run checklist status audit"
"${PYTHON_BIN}" scripts/verne_checklist_audit.py

echo "[3/6] Run checklist markdown link audit"
"${PYTHON_BIN}" scripts/checklist_link_audit.py

echo "[4/6] Run docs + automation conflict guard"
"${PYTHON_BIN}" scripts/docs_conflict_guard.py

echo "[5/6] Run Verne localisation audit"
"${PYTHON_BIN}" scripts/localisation_audit.py --file localisation/Flavour_Verne_A33_l_english.yml

echo "[6/6] Run Verne event ID audit"
"${PYTHON_BIN}" scripts/event_id_audit.py \
  --file events/Flavour_Verne_A33.txt \
  --file events/verne_overhaul_dynasty_events.txt

echo "All Verne smoke checks passed."
