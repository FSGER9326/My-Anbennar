#!/usr/bin/env bash
set -euo pipefail

BASE_REF="origin/main"
DRY_RUN="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --base)
      BASE_REF="$2"
      shift 2
      ;;
    --dry-run)
      DRY_RUN="true"
      shift
      ;;
    *)
      echo "ERROR: Unknown argument: $1"
      echo "Usage: bash scripts/resolve_pr_merge_conflicts.sh [--base origin/main] [--dry-run]"
      exit 1
      ;;
  esac
done

CURRENT_BRANCH="$(git branch --show-current)"
if [[ -z "${CURRENT_BRANCH}" ]]; then
  echo "ERROR: Not on a branch."
  exit 1
fi
if [[ "${CURRENT_BRANCH}" == "main" ]]; then
  echo "ERROR: You are on main. Checkout your PR branch first."
  exit 1
fi
if [[ -n "$(git status --porcelain)" ]]; then
  echo "ERROR: Working tree is dirty. Commit/stash first."
  exit 1
fi

echo "Fetching latest refs..."
git fetch origin

if [[ "${DRY_RUN}" == "true" ]]; then
  echo "Dry run mode."
  echo "Would run:"
  echo "  git rebase ${BASE_REF}"
  echo "  git push --force-with-lease"
  exit 0
fi

echo "Rebasing ${CURRENT_BRANCH} onto ${BASE_REF}..."
set +e
git rebase "${BASE_REF}"
REB_EXIT=$?
set -e

if [[ ${REB_EXIT} -ne 0 ]]; then
  echo
  echo "Rebase stopped due to conflicts."
  echo "Resolve files, then run:"
  echo "  git add <resolved-files>"
  echo "  git rebase --continue"
  echo
  echo "After rebase finishes, push:"
  echo "  git push --force-with-lease"
  exit 2
fi

echo "Rebase completed. Updating PR branch on GitHub..."
git push --force-with-lease
echo "Done. Refresh your PR page."
