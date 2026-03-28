#!/usr/bin/env bash
set -euo pipefail

BASE_REF="origin/main"
SYNC_MODE="merge"
AUTO_PUSH="false"
DEBUG_ONLY="false"
PYTHON_BIN="${PYTHON_BIN:-python3}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --base)
      BASE_REF="$2"
      shift 2
      ;;
    --mode)
      SYNC_MODE="$2"
      shift 2
      ;;
    --push)
      AUTO_PUSH="true"
      shift
      ;;
    --debug)
      DEBUG_ONLY="true"
      shift
      ;;
    *)
      # Backward compatibility for old positional usage: first arg = base ref.
      if [[ "$BASE_REF" == "origin/main" ]]; then
        BASE_REF="$1"
        shift
      else
        echo "ERROR: Unknown argument: $1"
        echo "Usage: bash scripts/auto_sync_pr_with_main.sh [--base origin/main] [--mode merge|rebase] [--push] [--debug]"
        exit 1
      fi
      ;;
  esac
done

if [[ "$SYNC_MODE" != "merge" && "$SYNC_MODE" != "rebase" ]]; then
  echo "ERROR: --mode must be 'merge' or 'rebase'."
  exit 1
fi

if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  PYTHON_BIN="python"
fi

if [[ -n "$(git status --porcelain)" ]]; then
  echo "ERROR: Working tree is not clean. Commit or stash first."
  exit 1
fi

BRANCH="$(git branch --show-current)"
if [[ "${BRANCH}" == "main" ]]; then
  echo "ERROR: Current branch is 'main'."
  echo "This sync helper is for feature/PR branches only."
  echo "If you are already on main, run a normal pull/check flow instead."
  exit 1
fi

echo "Fetching latest refs..."
git fetch origin

if [[ "$DEBUG_ONLY" == "true" ]]; then
  echo "=== PR Sync Debug Info ==="
  echo "Current branch: ${BRANCH}"
  echo "Base ref: ${BASE_REF}"
  MERGE_BASE="$(git merge-base HEAD "${BASE_REF}")"
  echo "Merge base: ${MERGE_BASE}"
  COUNTS="$(git rev-list --left-right --count HEAD..."${BASE_REF}")"
  AHEAD="$(echo "${COUNTS}" | awk '{print $1}')"
  BEHIND="$(echo "${COUNTS}" | awk '{print $2}')"
  echo "Ahead/Behind vs ${BASE_REF}: ahead=${AHEAD}, behind=${BEHIND}"
  echo
  echo "Potential conflict files (merge-tree preview):"
  set +e
  git merge-tree "${MERGE_BASE}" HEAD "${BASE_REF}" | grep '^<<<<<<< ' | sed 's/^<<<<<<< //' | sort -u
  MERGE_TREE_EXIT=$?
  set -e
  if [[ ${MERGE_TREE_EXIT} -ne 0 ]]; then
    echo "  (No conflict markers found in merge-tree preview.)"
  fi
  echo
  echo "Suggested next command:"
  echo "  bash scripts/auto_sync_pr_with_main.sh --mode rebase --push"
  exit 0
fi

if [[ "$SYNC_MODE" == "merge" ]]; then
  echo "Merging ${BASE_REF} into current branch (no auto-commit)..."
  set +e
  git merge --no-commit --no-ff "${BASE_REF}"
  SYNC_EXIT=$?
  set -e
else
  echo "Rebasing current branch onto ${BASE_REF}..."
  set +e
  git rebase "${BASE_REF}"
  SYNC_EXIT=$?
  set -e
fi

if [[ ${SYNC_EXIT} -ne 0 ]]; then
  echo "Sync reported conflicts. Attempting docs hotspot auto-resolution..."
  "${PYTHON_BIN}" scripts/resolve_docs_conflicts.py || true
  "${PYTHON_BIN}" scripts/resolve_content_conflicts.py --union-docs-only || true
fi

if [[ -n "$(git diff --name-only --diff-filter=U)" ]]; then
  echo "ERROR: Some conflicts remain."
  echo "Resolve manually, then run:"
  if [[ "$SYNC_MODE" == "rebase" ]]; then
    echo "  git add <resolved-files>"
    echo "  git rebase --continue"
  else
    echo "  git add <resolved-files>"
    echo "  git commit"
  fi
  echo "Then run:"
  echo "  ${PYTHON_BIN} scripts/docs_conflict_guard.py"
  echo "  bash scripts/verne_smoke_checks.sh"
  echo "If GitHub still shows 'This branch has conflicts', push your branch again:"
  echo "  git push --force-with-lease"
  exit 1
fi

echo "Running conflict guard and smoke checks..."
"${PYTHON_BIN}" scripts/docs_conflict_guard.py
bash scripts/verne_smoke_checks.sh

if [[ "$SYNC_MODE" == "merge" ]]; then
  if ! git rev-parse -q --verify MERGE_HEAD >/dev/null 2>&1; then
    echo "Already up to date. No merge commit needed."
    exit 0
  fi

  echo "Creating merge commit..."
  git commit -m "Merge ${BASE_REF} into ${BRANCH} with docs guard automation"
fi

if [[ "$AUTO_PUSH" == "true" ]]; then
  echo "Pushing branch updates..."
  if [[ "$SYNC_MODE" == "rebase" ]]; then
    git push --force-with-lease
  else
    git push
  fi
fi

echo "Done. Push your branch to update the existing PR status on GitHub."
