#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${REPO_ROOT}"

BASE_REF="${1:-origin/main}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  PYTHON_BIN="python"
fi

if [[ -n "$(git status --porcelain)" ]]; then
  echo "ERROR: Working tree is dirty. Commit/stash first."
  exit 1
fi

BRANCH="$(git branch --show-current)"
if [[ -z "${BRANCH}" || "${BRANCH}" == "main" ]]; then
  echo "ERROR: Run this from a non-main feature branch."
  exit 1
fi

if git rev-parse --verify "${BASE_REF}" >/dev/null 2>&1; then
  :
elif git remote get-url origin >/dev/null 2>&1; then
  echo "Fetching origin before conflict resolution..."
  git fetch origin
fi

if ! git rev-parse --verify "${BASE_REF}" >/dev/null 2>&1; then
  echo "ERROR: Base ref '${BASE_REF}' is unavailable."
  echo "Tip: pass an explicit base (for example: upstream/main)."
  exit 1
fi

echo "Merging ${BASE_REF} into ${BRANCH} (no auto-commit yet)..."
set +e
git merge --no-ff --no-commit "${BASE_REF}"
MERGE_CODE=$?
set -e

if [[ ${MERGE_CODE} -eq 0 ]]; then
  if [[ -n "$(git diff --cached --name-only)" ]]; then
    git commit -m "Merge ${BASE_REF} into ${BRANCH}"
    echo "Merge completed with commit."
  else
    echo "Already up to date; no merge commit needed."
    git merge --abort >/dev/null 2>&1 || true
  fi
  exit 0
fi

echo "Merge reported conflicts. Running auto-resolvers..."
"${PYTHON_BIN}" scripts/resolve_docs_conflicts.py || true
"${PYTHON_BIN}" scripts/resolve_content_conflicts.py || true

UNMERGED="$(git diff --name-only --diff-filter=U || true)"
if [[ -n "${UNMERGED}" ]]; then
  echo "ERROR: Unresolved conflicts remain:"
  echo "${UNMERGED}"
  echo "Resolve manually, then: git add <files> && git commit"
  exit 1
fi

git commit -m "Merge ${BASE_REF} into ${BRANCH} (auto-resolved hotspots)"
echo "Merge conflicts resolved and merge commit created."
