#!/usr/bin/env bash
set -euo pipefail

echo "[0/2] Run noob doctor preflight"
bash scripts/noob_doctor.sh

echo "[1/2] Run automation smoke checks"
bash scripts/verne_smoke_checks.sh
