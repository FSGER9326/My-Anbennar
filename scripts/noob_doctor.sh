#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-python3}"
if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  if command -v python >/dev/null 2>&1; then
    PYTHON_BIN="python"
  elif command -v py >/dev/null 2>&1; then
    PYTHON_BIN="py -3"
  else
    echo "ERROR: Python is not installed or not on PATH."
    echo "fix: sudo apt-get update && sudo apt-get install -y python3"
    exit 1
  fi
fi

if [[ "${PYTHON_BIN}" == "py -3" ]]; then
  py -3 scripts/noob_doctor.py "$@"
else
  "${PYTHON_BIN}" scripts/noob_doctor.py "$@"
fi
