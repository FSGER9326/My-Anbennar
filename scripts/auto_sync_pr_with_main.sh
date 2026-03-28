#!/usr/bin/env bash
set -euo pipefail
# Flow parity contract: bash/python/powershell sync scripts share resolver order and exit modes (ok|needs_manual_conflict|guard_failed|smoke_failed).

EXIT_OK=0
EXIT_NEEDS_MANUAL_CONFLICT=20
EXIT_GUARD_FAILED=21
EXIT_SMOKE_FAILED=22

BASE_REF="${1:-origin/main}"
PYTHON_BIN="${PYTHON_BIN:-python3}"

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

echo "Merging ${BASE_REF} into current branch (no auto-commit)..."
set +e
git merge --no-commit --no-ff "${BASE_REF}"
MERGE_EXIT=$?
set -e

if [[ ${MERGE_EXIT} -ne 0 ]]; then
  echo "Merge reported conflicts. Attempting docs hotspot auto-resolution..."
  "${PYTHON_BIN}" scripts/resolve_docs_conflicts.py || true
  "${PYTHON_BIN}" scripts/resolve_content_conflicts.py --union-docs-only || true
fi

if [[ -n "$(git diff --name-only --diff-filter=U)" ]]; then
  echo "ERROR: Some conflicts remain. Resolve manually, then run:"
  echo "  ${PYTHON_BIN} scripts/docs_conflict_guard.py"
  echo "  bash scripts/verne_smoke_checks.sh"
  echo "EXIT_MODE=needs_manual_conflict"
  exit ${EXIT_NEEDS_MANUAL_CONFLICT}
fi

echo "Running conflict guard and smoke checks..."
if ! "${PYTHON_BIN}" scripts/docs_conflict_guard.py; then
  echo "EXIT_MODE=guard_failed"
  exit ${EXIT_GUARD_FAILED}
fi
if ! bash scripts/verne_smoke_checks.sh; then
  echo "EXIT_MODE=smoke_failed"
  exit ${EXIT_SMOKE_FAILED}
fi

if ! git rev-parse -q --verify MERGE_HEAD >/dev/null 2>&1; then
  echo "Already up to date. No merge commit needed."
  echo "EXIT_MODE=ok"
  exit ${EXIT_OK}
fi

echo "Creating merge commit..."
git commit -m "Merge ${BASE_REF} into ${BRANCH} with docs guard automation"

echo "Done. Push your branch to update the existing PR."
echo "EXIT_MODE=ok"
