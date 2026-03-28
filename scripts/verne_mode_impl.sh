#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-python3}"

if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  PYTHON_BIN="python"
fi

echo "When to use this mode: implementation slices (script/event/loc edits) before commit/push."

echo "[1/4] Run country smoke profile"
"${PYTHON_BIN}" scripts/country_smoke_runner.py --profile automation/country_profiles/verne.json

echo "[2/4] Run localisation audit"
"${PYTHON_BIN}" scripts/localisation_audit.py --file localisation/Flavour_Verne_A33_l_english.yml

echo "[3/4] Run event ID audit"
"${PYTHON_BIN}" scripts/event_id_audit.py \
  --file events/Flavour_Verne_A33.txt \
  --file events/verne_overhaul_dynasty_events.txt

echo "[4/4] Run conflict guard"
"${PYTHON_BIN}" scripts/docs_conflict_guard.py

echo "Verne implementation mode checks passed."
