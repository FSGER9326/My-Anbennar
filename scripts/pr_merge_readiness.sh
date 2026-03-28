#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_ROOT}"

PYTHON_BIN="${PYTHON_BIN:-python3}"
if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  PYTHON_BIN="python"
fi

run_full_checks="false"
if [[ "${1:-}" == "--full-checks" ]]; then
  run_full_checks="true"
elif [[ -n "${1:-}" ]]; then
  echo "Usage: bash scripts/pr_merge_readiness.sh [--full-checks]"
  exit 1
fi

fail() {
  local message="$1"
  local next_cmd="$2"
  echo "❌ ${message}"
  echo "Next command: ${next_cmd}"
  exit 1
}

warn() {
  echo "⚠️  $1"
}

pass() {
  echo "✅ $1"
}

if ! git rev-parse --git-dir >/dev/null 2>&1; then
  fail "Not inside a git repository." "cd /path/to/repo"
fi

branch="$(git branch --show-current)"
if [[ -z "${branch}" ]]; then
  fail "Detached HEAD detected." "git switch <your-branch>"
fi
pass "Branch: ${branch}"

if [[ -n "$(git status --porcelain)" ]]; then
  fail "Working tree is not clean." "git status --short"
fi
pass "Working tree is clean"

pass "Fetching origin"
git fetch origin

if ! git rev-parse --verify origin/main >/dev/null 2>&1; then
  fail "origin/main not found after fetch." "git remote -v"
fi

upstream="$(git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null || true)"
if [[ -z "${upstream}" ]]; then
  warn "No upstream set for ${branch}."
  echo "Next command: git push --set-upstream origin ${branch}"
else
  pass "Upstream: ${upstream}"
fi

if git merge-base --is-ancestor origin/main HEAD; then
  pass "Branch already includes latest origin/main"
else
  warn "Branch does not include latest origin/main"
  echo "Next command: bash scripts/noob_autopilot.sh"
fi

if [[ -n "${upstream}" ]]; then
  ahead_behind="$(git rev-list --left-right --count "${upstream}...HEAD")"
  behind_count="${ahead_behind%% *}"
  ahead_count="${ahead_behind##* }"

  if [[ "${behind_count}" != "0" ]]; then
    warn "Your branch is behind upstream by ${behind_count} commit(s)."
    echo "Next command: git pull --rebase"
  else
    pass "Not behind upstream"
  fi

  if [[ "${ahead_count}" == "0" ]]; then
    warn "No local commits ahead of upstream."
  else
    pass "Ahead of upstream by ${ahead_count} commit(s)"
  fi
fi

# Dry-run merge in a temporary worktree so main tree stays untouched.
wt_dir="$(mktemp -d)"
cleanup() {
  git worktree remove --force "${wt_dir}" >/dev/null 2>&1 || true
  rm -rf "${wt_dir}" >/dev/null 2>&1 || true
}
trap cleanup EXIT

git worktree add --detach "${wt_dir}" HEAD >/dev/null 2>&1
merge_log="${wt_dir}/merge.log"
set +e
git -C "${wt_dir}" merge --no-commit --no-ff origin/main >"${merge_log}" 2>&1
merge_exit=$?
set -e

if [[ ${merge_exit} -eq 0 ]]; then
  pass "Merge simulation with origin/main: no conflicts"
  git -C "${wt_dir}" merge --abort >/dev/null 2>&1 || true
else
  if git -C "${wt_dir}" diff --name-only --diff-filter=U | grep -q .; then
    fail "Merge simulation found conflicts against origin/main." "bash scripts/noob_autopilot.sh --prefer-main"
  else
    fail "Merge simulation failed for a non-conflict reason." "cat ${merge_log}"
  fi
fi

if [[ "${run_full_checks}" == "true" ]]; then
  pass "Running pre-PR gate"
  bash "${SCRIPT_DIR}/pre_pr_gate.sh"
else
  warn "Skipped full checks (pass --full-checks to run pre_pr_gate.sh)."
  echo "Next command: bash scripts/pr_merge_readiness.sh --full-checks"
fi

pass "PR merge readiness checks completed"
