#!/usr/bin/env python3
"""Quick preflight checks for noob-friendly automation."""
from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


class CheckResult:
    def __init__(self, name: str, ok: bool, detail: str, fix: str, blocking: bool) -> None:
        self.name = name
        self.ok = ok
        self.detail = detail
        self.fix = fix
        self.blocking = blocking


def run_git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def check_python_executable() -> CheckResult:
    py = shutil.which("python3") or shutil.which("python")
    if py:
        return CheckResult(
            name="Python executable availability",
            ok=True,
            detail=f"found: {py}",
            fix="",
            blocking=False,
        )

    return CheckResult(
        name="Python executable availability",
        ok=False,
        detail="python3/python not found on PATH",
        fix="sudo apt-get update && sudo apt-get install -y python3",
        blocking=True,
    )


def check_git_repo() -> CheckResult:
    result = run_git("rev-parse", "--is-inside-work-tree")
    if result.returncode == 0 and result.stdout.strip() == "true":
        return CheckResult(
            name="git repo presence",
            ok=True,
            detail=str(ROOT),
            fix="",
            blocking=False,
        )

    return CheckResult(
        name="git repo presence",
        ok=False,
        detail="current folder is not a git work tree",
        fix="cd /workspace/My-Anbennar",
        blocking=True,
    )


def check_branch() -> CheckResult:
    result = run_git("branch", "--show-current")
    branch = result.stdout.strip()
    if result.returncode == 0 and branch:
        return CheckResult(
            name="current branch name",
            ok=True,
            detail=branch,
            fix="",
            blocking=False,
        )

    return CheckResult(
        name="current branch name",
        ok=False,
        detail="could not determine branch (detached HEAD or git issue)",
        fix="git switch -c my-feature-branch",
        blocking=True,
    )


def check_dirty_tree() -> CheckResult:
    result = run_git("status", "--porcelain")
    if result.returncode == 0 and not result.stdout.strip():
        return CheckResult(
            name="dirty working tree",
            ok=True,
            detail="clean",
            fix="",
            blocking=False,
        )

    if result.returncode == 0:
        return CheckResult(
            name="dirty working tree",
            ok=False,
            detail="uncommitted changes detected",
            fix='git add -A && git commit -m "WIP: save local changes before automation"',
            blocking=True,
        )

    return CheckResult(
        name="dirty working tree",
        ok=False,
        detail="unable to read git status",
        fix="git status",
        blocking=True,
    )


def check_origin_reachability() -> CheckResult:
    remote = run_git("remote", "get-url", "origin")
    if remote.returncode != 0:
        return CheckResult(
            name="remote origin reachability",
            ok=False,
            detail="origin remote is missing",
            fix="git remote add origin <your-repo-url>",
            blocking=True,
        )

    ls_remote = run_git("ls-remote", "--heads", "origin")
    if ls_remote.returncode == 0:
        return CheckResult(
            name="remote origin reachability",
            ok=True,
            detail=f"reachable: {remote.stdout.strip()}",
            fix="",
            blocking=False,
        )

    return CheckResult(
        name="remote origin reachability",
        ok=False,
        detail=(ls_remote.stderr or ls_remote.stdout).strip() or "cannot reach origin",
        fix="git fetch origin",
        blocking=True,
    )


def main() -> int:
    checks = [
        check_python_executable(),
        check_git_repo(),
    ]

    # Only run git-dependent checks if repo presence succeeded.
    if checks[-1].ok:
        checks.extend(
            [
                check_branch(),
                check_dirty_tree(),
                check_origin_reachability(),
            ]
        )

    print("noob_doctor preflight")
    print("====================")

    blocking = False
    for check in checks:
        icon = "PASS" if check.ok else "FAIL"
        print(f"- {check.name}: {icon} ({check.detail})")
        if not check.ok:
            print(f"  fix: {check.fix}")
        blocking = blocking or (check.blocking and not check.ok)

    if blocking:
        print("\nBlocking issues found. Fix them, then rerun noob_doctor.")
        return 1

    print("\nAll preflight checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
