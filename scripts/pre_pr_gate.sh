#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${REPO_ROOT}"

PYTHON_BIN="${PYTHON_BIN:-python3}"
if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  PYTHON_BIN="python"
fi

ARTIFACT_DIR="artifacts/validation"
mkdir -p "${ARTIFACT_DIR}"

run_audit_json() {
  local label="$1"
  local cmd="$2"
  local out_json="$3"

  echo "${label}"
  set +e
  eval "${cmd} --format json > '${out_json}'"
  local code=$?
  set -e
  return ${code}
}

attempt_safe_remediation() {
  local report_json="$1"
  local cmd
  cmd="$(${PYTHON_BIN} - <<'PY' "${report_json}"
import json, sys
report = json.load(open(sys.argv[1], encoding='utf-8'))
SAFE_CODES = {"MERGE_CONFLICT_MARKER", "HEADING_SINGLETON_VIOLATION", "MISSING_UTF8_BOM"}
for issue in report.get("issues", []):
    code = issue.get("code")
    fix = (issue.get("suggested_fix_command") or "").strip()
    if code in SAFE_CODES and fix:
        print(fix)
        break
PY
)"

  if [[ -n "${cmd}" ]]; then
    echo "Auto-remediation selected (safe): ${cmd}"
    eval "${cmd}" || true
  fi
}

run_audit_json "[1/5] Docs conflict guard" "${PYTHON_BIN} scripts/docs_conflict_guard.py" "${ARTIFACT_DIR}/docs_conflict_guard.json" || true
run_audit_json "[2/5] Checklist link audit" "${PYTHON_BIN} scripts/checklist_link_audit.py" "${ARTIFACT_DIR}/checklist_link_audit.json" || true
run_audit_json "[3/5] Verne checklist audit" "${PYTHON_BIN} scripts/verne_checklist_audit.py" "${ARTIFACT_DIR}/checklist_manifest_audit.json" || true
run_audit_json "[4/5] Verne country smoke runner" "${PYTHON_BIN} scripts/country_smoke_runner.py --profile automation/country_profiles/verne.json" "${ARTIFACT_DIR}/country_smoke_runner.json" || true
run_audit_json "[5/5] Localisation + Event audits" "${PYTHON_BIN} scripts/localisation_audit.py --file localisation/Flavour_Verne_A33_l_english.yml" "${ARTIFACT_DIR}/localisation_audit.json" || true
"${PYTHON_BIN}" scripts/event_id_audit.py --file events/Flavour_Verne_A33.txt --file events/verne_overhaul_dynasty_events.txt --format json > "${ARTIFACT_DIR}/event_id_audit.json" || true

"${PYTHON_BIN}" scripts/validation_aggregate.py \
  --input "${ARTIFACT_DIR}/docs_conflict_guard.json" \
  --input "${ARTIFACT_DIR}/checklist_link_audit.json" \
  --input "${ARTIFACT_DIR}/checklist_manifest_audit.json" \
  --input "${ARTIFACT_DIR}/country_smoke_runner.json" \
  --input "${ARTIFACT_DIR}/localisation_audit.json" \
  --input "${ARTIFACT_DIR}/event_id_audit.json" \
  --out-json artifacts/validation_report.json \
  --out-md artifacts/validation_report.md || true

attempt_safe_remediation "artifacts/validation_report.json"

if "${PYTHON_BIN}" scripts/validation_aggregate.py \
  --input "${ARTIFACT_DIR}/docs_conflict_guard.json" \
  --input "${ARTIFACT_DIR}/checklist_link_audit.json" \
  --input "${ARTIFACT_DIR}/checklist_manifest_audit.json" \
  --input "${ARTIFACT_DIR}/country_smoke_runner.json" \
  --input "${ARTIFACT_DIR}/localisation_audit.json" \
  --input "${ARTIFACT_DIR}/event_id_audit.json" \
  --out-json artifacts/validation_report.json \
  --out-md artifacts/validation_report.md; then
  echo "Pre-PR gate passed. Safe to open a PR."
  exit 0
fi

echo
echo "Pre-PR gate failed. See artifacts/validation_report.md for prioritized issues."
echo "Attempted one safe auto-remediation when available."
exit 1
