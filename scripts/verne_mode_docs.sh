#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-python3}"

if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  PYTHON_BIN="python"
fi

echo "When to use this mode: docs/checklist-only edits before commit/push."

echo "[1/3] Run checklist manifest audit"
"${PYTHON_BIN}" scripts/checklist_manifest_audit.py

echo "[2/3] Run markdown link audit"
"${PYTHON_BIN}" scripts/checklist_link_audit.py

echo "[3/3] Run conflict guard"
"${PYTHON_BIN}" scripts/docs_conflict_guard.py

echo "Verne docs mode checks passed."
