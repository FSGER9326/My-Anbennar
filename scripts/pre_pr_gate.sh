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

BASE_REF="${BASE_REF:-origin/main}"

if [[ -n "$(git diff --name-only --diff-filter=U)" ]]; then
  echo "Pre-PR gate cannot run with unresolved git merge conflicts."
  echo "Try: python3 scripts/resolve_docs_conflicts.py"
  echo "Or:  python3 scripts/resolve_content_conflicts.py"
  exit 1
fi

attempt_branch_sync() {
  if ! git rev-parse --verify "${BASE_REF}" >/dev/null 2>&1; then
    echo "[sync] Skip: base ref '${BASE_REF}' is unavailable in this clone."
    return 0
  fi

  echo "[sync] Attempt merge sync from ${BASE_REF}"
  if ! bash scripts/auto_sync_pr_with_main.sh "${BASE_REF}"; then
    echo "[sync] Auto sync reported conflicts; attempting hotspot resolvers"
    python3 scripts/resolve_docs_conflicts.py || true
    python3 scripts/resolve_content_conflicts.py || true

    if [[ -n "$(git diff --name-only --diff-filter=U)" ]]; then
      echo "[sync] Unresolved conflicts remain after auto-resolvers."
      return 1
    fi
  fi

  return 0
}

run_audits() {
  echo "[1/6] Docs conflict guard"
  "${PYTHON_BIN}" scripts/docs_conflict_guard.py --format json > "${ARTIFACT_DIR}/docs_conflict_guard.json" || true

  echo "[2/6] Checklist link audit"
  "${PYTHON_BIN}" scripts/checklist_link_audit.py --format json > "${ARTIFACT_DIR}/checklist_link_audit.json" || true

  echo "[3/6] Verne checklist audit"
  "${PYTHON_BIN}" scripts/verne_checklist_audit.py --format json > "${ARTIFACT_DIR}/checklist_manifest_audit.json" || true

  echo "[4/6] Verne country smoke runner"
  "${PYTHON_BIN}" scripts/country_smoke_runner.py --profile automation/country_profiles/verne.json --format json > "${ARTIFACT_DIR}/country_smoke_runner.json" || true

  echo "[5/6] Localisation audit"
  "${PYTHON_BIN}" scripts/localisation_audit.py --file localisation/Flavour_Verne_A33_l_english.yml --format json > "${ARTIFACT_DIR}/localisation_audit.json" || true

  echo "[6/6] Event ID audit"
  "${PYTHON_BIN}" scripts/event_id_audit.py --file events/Flavour_Verne_A33.txt --file events/verne_overhaul_dynasty_events.txt --format json > "${ARTIFACT_DIR}/event_id_audit.json" || true
}

aggregate_reports() {
  "${PYTHON_BIN}" scripts/validation_aggregate.py \
    --input "${ARTIFACT_DIR}/docs_conflict_guard.json" \
    --input "${ARTIFACT_DIR}/checklist_link_audit.json" \
    --input "${ARTIFACT_DIR}/checklist_manifest_audit.json" \
    --input "${ARTIFACT_DIR}/country_smoke_runner.json" \
    --input "${ARTIFACT_DIR}/localisation_audit.json" \
    --input "${ARTIFACT_DIR}/event_id_audit.json" \
    --out-json artifacts/validation_report.json \
    --out-md artifacts/validation_report.md
}

run_safe_remediation() {
  local report_json="$1"
  "${PYTHON_BIN}" - <<'PY' "${report_json}" | while IFS= read -r cmd; do
import json
import sys

SAFE_CODES = {"MERGE_CONFLICT_MARKER", "HEADING_SINGLETON_VIOLATION", "MISSING_UTF8_BOM"}
MAX_FIXES = 3

with open(sys.argv[1], encoding="utf-8") as fh:
    report = json.load(fh)

seen = set()
fixes = 0
for issue in report.get("issues", []):
    code = issue.get("code")
    cmd = (issue.get("suggested_fix_command") or "").strip()
    if code not in SAFE_CODES or not cmd:
        continue
    if cmd in seen:
        continue
    print(cmd)
    seen.add(cmd)
    fixes += 1
    if fixes >= MAX_FIXES:
        break
PY
    if [[ -n "${cmd}" ]]; then
      echo "Auto-remediation selected (safe): ${cmd}"
      bash -lc "${cmd}" || true
    fi
  done
}

attempt_branch_sync || exit 1

run_audits
aggregate_reports || true
run_safe_remediation "artifacts/validation_report.json"
run_audits

if aggregate_reports; then
  echo "Pre-PR gate passed. Safe to open a PR."
  exit 0
fi

echo
echo "Pre-PR gate failed. See artifacts/validation_report.md for prioritized issues."
echo "Attempted safe auto-remediation where applicable; remaining issues need manual fixes."
exit 1
