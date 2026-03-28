#!/usr/bin/env bash
set -euo pipefail

BASE_REF="${1:-origin/main}"

if [[ -n "$(git status --porcelain)" ]]; then
  echo "ERROR: Working tree is dirty. Commit or stash first."
  exit 1
fi

BRANCH="$(git branch --show-current)"
if [[ -z "${BRANCH}" || "${BRANCH}" == "main" ]]; then
  echo "ERROR: Checkout your PR branch first."
  exit 1
fi

if ! git remote get-url origin >/dev/null 2>&1; then
  echo "ERROR: Missing 'origin' remote."
  exit 1
fi

git fetch origin
set +e
git rebase "${BASE_REF}"
REB_EXIT=$?
set -e

if [[ ${REB_EXIT} -ne 0 ]]; then
  echo "Rebase stopped on conflicts."
  echo "Resolve files, then run:"
  echo "  git add <resolved-files>"
  echo "  git rebase --continue"
  echo "After completion, push:"
  echo "  git push --force-with-lease"
  exit 2
fi

git push --force-with-lease
echo "Done. Refresh PR status on GitHub."
