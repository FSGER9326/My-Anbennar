#!/usr/bin/env bash
set -euo pipefail

if current="$(git config --get core.hooksPath 2>/dev/null)" && [[ "${current}" == ".githooks" ]]; then
  git config --unset core.hooksPath
  echo "Removed repo hooksPath (.githooks)."
  echo "Manual fallback:"
  echo " - powershell -NoProfile -ExecutionPolicy Bypass -File .\\scripts\\smart_smoke_router.ps1"
  echo " - powershell -NoProfile -ExecutionPolicy Bypass -File .\\scripts\\verne_smoke_checks.ps1"
  exit 0
fi

echo "No repo hooksPath override was set."
