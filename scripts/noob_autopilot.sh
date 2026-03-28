#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_ROOT}"

PYTHON_BIN="${PYTHON_BIN:-python3}"
if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  PYTHON_BIN="python"
fi

RESOLUTION_STRATEGY="manual"
BASE_REF="origin/main"
EXIT_NEEDS_MANUAL_CONFLICT=20
EXIT_GUARD_FAILED=21
EXIT_SMOKE_FAILED=22

usage() {
  cat <<USAGE
Usage: bash scripts/noob_autopilot.sh [--base-ref <ref>] [--prefer-main|--prefer-branch]

Options:
  --base-ref <ref>     Merge source (default: origin/main)
  --prefer-main        If unresolved conflicts remain, auto-resolve using main's side
  --prefer-branch      If unresolved conflicts remain, auto-resolve using your branch side

Default mode is manual-safe: unresolved conflicts stop with a clear next command.
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --base-ref)
      BASE_REF="${2:-}"
      shift 2
      ;;
    --prefer-main)
      RESOLUTION_STRATEGY="prefer-main"
      shift
      ;;
    --prefer-branch)
      RESOLUTION_STRATEGY="prefer-branch"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "ERROR: unknown argument: $1"
      usage
      exit 1
      ;;
  esac
done

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
if [[ -n "$(git status --porcelain)" && -z "$(git diff --name-only --diff-filter=U)" ]]; then
  fail_with_next "Working tree is not clean." "git status --short"
fi

echo "[STEP 2/7] Fetch latest origin"
if [[ -z "$(git diff --name-only --diff-filter=U)" ]] && ! git fetch origin; then
  fail_with_next "Could not fetch from origin." "git fetch origin"
fi

echo "[STEP 3/7] Run auto_sync_pr_with_main (bash)"
SYNC_LOG="$(mktemp)"
if [[ -n "$(git diff --name-only --diff-filter=U)" ]]; then
  echo "Existing unresolved merge conflicts detected; skipping merge step." >"${SYNC_LOG}"
  echo "EXIT_MODE=needs_manual_conflict" >>"${SYNC_LOG}"
  SYNC_EXIT=${EXIT_NEEDS_MANUAL_CONFLICT}
else
  set +e
  bash "${SCRIPT_DIR}/auto_sync_pr_with_main.sh" "${BASE_REF}" >"${SYNC_LOG}" 2>&1
  SYNC_EXIT=$?
  set -e
fi
cat "${SYNC_LOG}"

echo "[STEP 4/7] Handle sync result"
if [[ ${SYNC_EXIT} -eq 0 ]]; then
  echo "auto_sync_pr_with_main completed."
elif [[ ${SYNC_EXIT} -eq ${EXIT_NEEDS_MANUAL_CONFLICT} ]]; then
  if [[ "${RESOLUTION_STRATEGY}" == "manual" ]]; then
    rm -f "${SYNC_LOG}"
    fail_with_next "Sync paused: unresolved conflicts need manual attention." "bash scripts/noob_autopilot.sh --prefer-main"
  fi
  echo "Sync mode: needs_manual_conflict. Applying ${RESOLUTION_STRATEGY} strategy..."
  while IFS= read -r f; do
    [[ -z "${f}" ]] && continue
    if [[ "${RESOLUTION_STRATEGY}" == "prefer-main" ]]; then
      git checkout --theirs -- "${f}"
    else
      git checkout --ours -- "${f}"
    fi
    git add -- "${f}"
  done < <(git diff --name-only --diff-filter=U)
elif [[ ${SYNC_EXIT} -eq ${EXIT_GUARD_FAILED} ]]; then
  rm -f "${SYNC_LOG}"
  fail_with_next "Sync mode: guard_failed (docs conflict guard did not pass)." "${PYTHON_BIN} scripts/docs_conflict_guard.py"
elif [[ ${SYNC_EXIT} -eq ${EXIT_SMOKE_FAILED} ]]; then
  rm -f "${SYNC_LOG}"
  fail_with_next "Sync mode: smoke_failed (smoke checks did not pass)." "bash scripts/verne_smoke_checks.sh"
else
  rm -f "${SYNC_LOG}"
  fail_with_next "auto_sync_pr_with_main.sh failed unexpectedly (exit ${SYNC_EXIT})." "bash scripts/auto_sync_pr_with_main.sh ${BASE_REF}"
fi

echo "[STEP 5/7] Run docs_conflict_guard (post-sync confirmation)"
if ! "${PYTHON_BIN}" "${SCRIPT_DIR}/docs_conflict_guard.py"; then
  rm -f "${SYNC_LOG}"
  fail_with_next "docs_conflict_guard failed." "${PYTHON_BIN} scripts/docs_conflict_guard.py"
fi

echo "[STEP 6/7] Run verne_smoke_checks (post-sync confirmation)"
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
