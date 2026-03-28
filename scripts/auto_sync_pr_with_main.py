#!/usr/bin/env python3
"""Sync a feature branch with main and run repository automation checks."""
# Flow parity contract: bash/python/powershell sync scripts share resolver order and exit modes (ok|needs_manual_conflict|guard_failed|smoke_failed).
from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
BASE_REF = sys.argv[1] if len(sys.argv) > 1 else "origin/main"
EXIT_OK = 0
EXIT_NEEDS_MANUAL_CONFLICT = 20
EXIT_GUARD_FAILED = 21
EXIT_SMOKE_FAILED = 22


def run(cmd: list[str], *, check: bool = False) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if check and result.returncode != 0:
        raise subprocess.CalledProcessError(
            result.returncode,
            cmd,
            output=result.stdout,
            stderr=result.stderr,
        )
    return result


def print_output(result: subprocess.CompletedProcess[str]) -> None:
    text = "\n".join(part for part in (result.stdout.strip(), result.stderr.strip()) if part)
    if text:
        print(text)


def current_branch() -> str:
    result = run(["git", "branch", "--show-current"], check=True)
    return result.stdout.strip()


def has_merge_head() -> bool:
    result = run(["git", "rev-parse", "-q", "--verify", "MERGE_HEAD"])
    return result.returncode == 0


def ensure_clean_worktree() -> None:
    result = run(["git", "status", "--porcelain"], check=True)
    if result.stdout.strip():
        print("ERROR: Working tree is not clean. Commit or stash first.")
        raise SystemExit(1)


def run_python_script(script: str, *args: str) -> int:
    result = run([sys.executable, str(ROOT / "scripts" / script), *args])
    print_output(result)
    return result.returncode


def run_shell_script(script: str, *args: str) -> int:
    result = run(["bash", str(ROOT / "scripts" / script), *args])
    print_output(result)
    return result.returncode


def main() -> int:
    ensure_clean_worktree()

    branch = current_branch()
    if branch == "main":
        print("ERROR: Current branch is 'main'.")
        print("This sync helper is for feature/PR branches only.")
        print("If you are already on main, run a normal pull/check flow instead.")
        return 1

    print("Fetching latest refs...")
    fetch = run(["git", "fetch", "origin"])
    print_output(fetch)
    if fetch.returncode != 0:
        return fetch.returncode

    print(f"Merging {BASE_REF} into current branch (no auto-commit)...")
    merge = run(["git", "merge", "--no-commit", "--no-ff", BASE_REF])
    print_output(merge)

    unresolved_now = run(["git", "diff", "--name-only", "--diff-filter=U"], check=True)
    has_unresolved_now = any(line.strip() for line in unresolved_now.stdout.splitlines())
    if merge.returncode != 0 or has_unresolved_now:
        print("Merge reported conflicts. Attempting docs hotspot auto-resolution...")
        run_python_script("resolve_docs_conflicts.py")
        run_python_script("resolve_content_conflicts.py", "--union-docs-only")

    remaining = run(["git", "diff", "--name-only", "--diff-filter=U"], check=True)
    unresolved = [line.strip() for line in remaining.stdout.splitlines() if line.strip()]
    if unresolved:
        print("ERROR: Some conflicts remain. Resolve manually, then run:")
        print(f"    {sys.executable} scripts/docs_conflict_guard.py")
        print("    bash scripts/verne_smoke_checks.sh")
        print("EXIT_MODE=needs_manual_conflict")
        return EXIT_NEEDS_MANUAL_CONFLICT

    print("Running conflict guard and smoke checks...")
    guard_rc = run_python_script("docs_conflict_guard.py")
    if guard_rc != 0:
        print("EXIT_MODE=guard_failed")
        return EXIT_GUARD_FAILED
    # Keep parity with shell + PowerShell sync entrypoints by delegating to the shared smoke bundle.
    smoke_rc = run_shell_script("verne_smoke_checks.sh")
    if smoke_rc != 0:
        print("EXIT_MODE=smoke_failed")
        return EXIT_SMOKE_FAILED

    if not has_merge_head():
        print("Already up to date. No merge commit needed.")
        print("EXIT_MODE=ok")
        return EXIT_OK

    print("Creating merge commit...")
    commit = run(
        ["git", "commit", "-m", f"Merge {BASE_REF} into {branch} with docs guard automation"]
    )
    print_output(commit)
    if commit.returncode != 0:
        return commit.returncode

    print("Done. Push your branch to update the existing PR.")
    print("EXIT_MODE=ok")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
