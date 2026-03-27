#!/usr/bin/env bash
set -euo pipefail

BASE_REF="${1:-origin/main}"

if [[ -n "$(git status --porcelain)" ]]; then
  echo "ERROR: Working tree is not clean. Commit or stash first."
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
  ./scripts/resolve_docs_conflicts.py || true
fi

if [[ -n "$(git diff --name-only --diff-filter=U)" ]]; then
  echo "ERROR: Some conflicts remain. Resolve manually, then run:"
  echo "  ./scripts/docs_conflict_guard.py"
  echo "  ./scripts/verne_smoke_checks.sh"
  exit 1
fi

echo "Running conflict guard and smoke checks..."
./scripts/docs_conflict_guard.py
./scripts/verne_smoke_checks.sh

echo "Creating merge commit..."
git commit -m "Merge ${BASE_REF} into $(git branch --show-current) with docs guard automation"

echo "Done. Push your branch to update the existing PR."
