#!/usr/bin/env bash
set -euo pipefail

BASE_REF="origin/main"
MODE="rebase"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --base)
      BASE_REF="$2"
      shift 2
      ;;
    --mode)
      MODE="$2"
      shift 2
      ;;
    *)
      echo "ERROR: Unknown argument: $1"
      echo "Usage: bash scripts/fix_pr_merge_conflicts.sh [--base origin/main] [--mode rebase|merge]"
      exit 1
      ;;
  esac
done

if [[ "$MODE" != "rebase" && "$MODE" != "merge" ]]; then
  echo "ERROR: --mode must be rebase or merge."
  exit 1
fi

echo "=== PR Conflict Fix Helper ==="
echo "Base: ${BASE_REF}"
echo "Mode: ${MODE}"
echo
echo "Step 1/2: showing quick conflict diagnostics..."
bash scripts/auto_sync_pr_with_main.sh --base "${BASE_REF}" --debug
echo
echo "Step 2/2: syncing and pushing branch to update GitHub PR conflict status..."
bash scripts/auto_sync_pr_with_main.sh --base "${BASE_REF}" --mode "${MODE}" --push
echo
echo "Done. Refresh your PR page on GitHub."
