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
  print_post_fail_summary
  echo "ERROR: ${message}"
  echo "Next command:"
  echo "${next_cmd}"
  exit 1
}

print_post_fail_summary() {
  local tmp_file
  local loc_rc=0
  local event_rc=0

  echo
  echo "Quick triage summary (priority order):"

  if [[ -n "$(git diff --name-only --diff-filter=U)" ]]; then
    echo "1) merge conflicts -> git diff --name-only --diff-filter=U ; Why first: unresolved merges can invalidate every later check."
  fi

  tmp_file="$(mktemp)"
  if ! "${PYTHON_BIN}" "${SCRIPT_DIR}/docs_conflict_guard.py" >"${tmp_file}" 2>&1; then
    echo "2) conflict markers -> ${PYTHON_BIN} scripts/docs_conflict_guard.py ; Why first: marker leftovers break parsing and hide real logic errors."
  fi

  if ! bash "${SCRIPT_DIR}/verne_smoke_checks.sh" >"${tmp_file}" 2>&1; then
    echo "3) syntax/structure checks -> bash scripts/verne_smoke_checks.sh ; Why first: structural failures must clear before deeper content audits."
  fi

  "${PYTHON_BIN}" "${SCRIPT_DIR}/localisation_audit.py" >"${tmp_file}" 2>&1 || loc_rc=$?
  "${PYTHON_BIN}" "${SCRIPT_DIR}/event_id_audit.py" >"${tmp_file}" 2>&1 || event_rc=$?
  if [[ ${loc_rc} -ne 0 ]]; then
    echo "4) localisation/event ID checks -> ${PYTHON_BIN} scripts/localisation_audit.py ; Why first: broken localisation keys block text integrity checks before ID cleanup."
  elif [[ ${event_rc} -ne 0 ]]; then
    echo "4) localisation/event ID checks -> ${PYTHON_BIN} scripts/event_id_audit.py ; Why first: duplicate/missing event IDs can break runtime event flow even after syntax passes."
  fi

  rm -f "${tmp_file}"
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
bash "${SCRIPT_DIR}/auto_sync_pr_with_main.sh" "${BASE_REF}" >"${SYNC_LOG}" 2>&1
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
  if [[ "${RESOLUTION_STRATEGY}" == "manual" ]]; then
    fail_with_next "Unresolved merge conflicts remain." "bash scripts/noob_autopilot.sh --prefer-main"
  fi
  echo "Applying ${RESOLUTION_STRATEGY} strategy to unresolved files..."
  while IFS= read -r f; do
    [[ -z "${f}" ]] && continue
    if [[ "${RESOLUTION_STRATEGY}" == "prefer-main" ]]; then
      git checkout --theirs -- "${f}"
    else
      git checkout --ours -- "${f}"
    fi
    git add -- "${f}"
  done < <(git diff --name-only --diff-filter=U)
fi

if [[ ${SYNC_EXIT} -ne 0 ]]; then
  rm -f "${SYNC_LOG}"
  fail_with_next "auto_sync_pr_with_main.sh failed." "bash scripts/noob_autopilot.sh --prefer-main"
fi

echo "[STEP 5/7] Run docs_conflict_guard"
if ! "${PYTHON_BIN}" "${SCRIPT_DIR}/docs_conflict_guard.py"; then
  rm -f "${SYNC_LOG}"
  fail_with_next "docs_conflict_guard failed." "${PYTHON_BIN} scripts/docs_conflict_guard.py"
fi

echo "[STEP 6/7] Run full smoke checks (verne_smoke_checks)"
if ! bash "${SCRIPT_DIR}/verne_smoke_checks.sh"; then
  rm -f "${SYNC_LOG}"
  fail_with_next "verne_smoke_checks failed." "bash scripts/verne_smoke_checks.sh"
fi

rm -f "${SYNC_LOG}"

echo "[STEP 7/7] Done"
echo "Habit reminder: sync first, then push."
echo "Final instruction: run the push command shown below."
UPSTREAM="$(git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null || true)"
if [[ -n "${UPSTREAM}" ]]; then
  echo "Success after sync/merge handling + conflict guard + full smoke checks."
  echo "Push with:"
  echo "git push"
else
  echo "Success after sync/merge handling + conflict guard + full smoke checks."
  echo "Push with:"
  echo "git push --set-upstream origin ${BRANCH}"
fi
