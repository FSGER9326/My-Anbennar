#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_ROOT}"

PYTHON_BIN="${PYTHON_BIN:-python3}"
if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  PYTHON_BIN="python"
fi

fail_with_next() {
  local message="$1"
  local next_cmd="$2"
  echo "ERROR: ${message}"
  echo "Next command:"
  echo "${next_cmd}"
  exit 1
}

BRANCH="$(git branch --show-current)"

echo "[STEP 1/7] Verify clean working tree"
if [[ -n "$(git status --porcelain)" ]]; then
  fail_with_next "Working tree is not clean." "git status --short"
fi

echo "[STEP 2/7] Fetch latest origin"
if ! git fetch origin; then
  fail_with_next "Could not fetch from origin." "git fetch origin"
fi

echo "[STEP 3/7] Run auto_sync_pr_with_main (bash)"
SYNC_LOG="$(mktemp)"
set +e
bash "${SCRIPT_DIR}/auto_sync_pr_with_main.sh" >"${SYNC_LOG}" 2>&1
SYNC_EXIT=$?
set -e
if [[ ${SYNC_EXIT} -eq 0 ]]; then
  echo "auto_sync_pr_with_main completed."
fi

echo "[STEP 4/7] Resolve unresolved merge conflicts (docs hotspots only, when needed)"
if [[ -n "$(git diff --name-only --diff-filter=U)" ]]; then
  set +e
  "${PYTHON_BIN}" "${SCRIPT_DIR}/resolve_docs_conflicts.py"
  RESOLVE_EXIT=$?
  set -e

  if [[ ${RESOLVE_EXIT} -ne 0 ]]; then
    rm -f "${SYNC_LOG}"
    fail_with_next "Automatic docs conflict resolution failed." "${PYTHON_BIN} scripts/resolve_docs_conflicts.py"
  fi
fi

if [[ -n "$(git diff --name-only --diff-filter=U)" ]]; then
  rm -f "${SYNC_LOG}"
  fail_with_next "Unresolved merge conflicts remain." "${PYTHON_BIN} scripts/resolve_docs_conflicts.py"
fi

if [[ ${SYNC_EXIT} -ne 0 ]]; then
  rm -f "${SYNC_LOG}"
  fail_with_next "auto_sync_pr_with_main.sh failed." "bash scripts/auto_sync_pr_with_main.sh"
fi

echo "[STEP 5/7] Run docs_conflict_guard"
if ! "${PYTHON_BIN}" "${SCRIPT_DIR}/docs_conflict_guard.py"; then
  rm -f "${SYNC_LOG}"
  fail_with_next "docs_conflict_guard failed." "${PYTHON_BIN} scripts/docs_conflict_guard.py"
fi

echo "[STEP 6/7] Run verne_smoke_checks"
if ! bash "${SCRIPT_DIR}/verne_smoke_checks.sh"; then
  rm -f "${SYNC_LOG}"
  fail_with_next "verne_smoke_checks failed." "bash scripts/verne_smoke_checks.sh"
fi

rm -f "${SYNC_LOG}"

echo "[STEP 7/7] Done"
echo "Habit reminder: sync first, then push."
UPSTREAM="$(git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null || true)"
if [[ -n "${UPSTREAM}" ]]; then
  echo "Success. Push with:"
  echo "git push"
else
  echo "Success. Push with:"
  echo "git push --set-upstream origin ${BRANCH}"
fi
