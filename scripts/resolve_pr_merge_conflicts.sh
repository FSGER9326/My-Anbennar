#!/usr/bin/env bash
set -euo pipefail

BASE_REF="origin/main"
DRY_RUN="false"
NO_PUSH="false"

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
    --no-push)
      NO_PUSH="true"
      shift
      ;;
    *)
      echo "ERROR: Unknown argument: $1"
      echo "Usage: bash scripts/resolve_pr_merge_conflicts.sh [--base origin/main] [--dry-run] [--no-push]"
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
if ! git remote get-url origin >/dev/null 2>&1; then
  echo "ERROR: No 'origin' remote configured."
  echo "Add your GitHub remote first, then retry."
  echo "Example:"
  echo "  git remote add origin <your-repo-url>"
  exit 1
fi
if ! git fetch origin; then
  echo "ERROR: Failed to fetch from origin."
  echo "Check network/auth and retry."
  exit 1
fi

if [[ "${DRY_RUN}" == "true" ]]; then
  echo "Dry run mode."
  echo "Would run:"
  echo "  git rebase ${BASE_REF}"
  if [[ "${NO_PUSH}" == "true" ]]; then
    echo "  # push skipped (--no-push)"
  else
    echo "  git push --force-with-lease"
  fi
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

if [[ "${NO_PUSH}" == "true" ]]; then
  echo "Rebase completed. Push skipped (--no-push)."
  echo "When ready, run:"
  echo "  git push --force-with-lease"
  exit 0
fi

echo "Rebase completed. Updating PR branch on GitHub..."
git push --force-with-lease
echo "Done. Refresh your PR page."
