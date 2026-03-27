#!/usr/bin/env python3
"""Cross-platform PR sync helper.

Usage:
  python scripts/auto_sync_pr_with_main.py [base_ref]
Default base_ref: origin/main
"""

from __future__ import annotations

import shutil
import subprocess
import sys


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(cmd, text=True, capture_output=True)
    if check and proc.returncode != 0:
        if proc.stdout:
            print(proc.stdout)
        if proc.stderr:
            print(proc.stderr, file=sys.stderr)
        raise SystemExit(proc.returncode)
    return proc


def has_uncommitted_changes() -> bool:
    proc = run(["git", "status", "--porcelain"], check=True)
    return bool(proc.stdout.strip())


def unresolved_files() -> list[str]:
    proc = run(["git", "diff", "--name-only", "--diff-filter=U"], check=True)
    return [x for x in proc.stdout.splitlines() if x.strip()]


def run_smoke_checks() -> None:
    print("Running docs conflict guard...")
    run([sys.executable, "scripts/docs_conflict_guard.py"], check=True)

    bash = shutil.which("bash")
    if bash:
        print("Running full Verne smoke checks via bash...")
        run([bash, "scripts/verne_smoke_checks.sh"], check=True)
        return

    print("WARNING: bash not found; running reduced Python checks only.")
    run([sys.executable, "scripts/verne_checklist_audit.py"], check=True)
    run([sys.executable, "scripts/checklist_link_audit.py"], check=True)
    print("Reduced checks passed. Install bash to run full Verne smoke suite.")


def main() -> int:
    base_ref = sys.argv[1] if len(sys.argv) > 1 else "origin/main"

    if has_uncommitted_changes():
        print("ERROR: Working tree is not clean. Commit or stash first.")
        return 1

<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
    branch = run(["git", "branch", "--show-current"], check=True).stdout.strip()
    if branch == "main":
        print("ERROR: Current branch is 'main'.")
        print("This sync helper is for feature/PR branches only.")
        print("If you are already on main, run a normal pull/check flow instead.")
        return 1

=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
    print("Fetching latest refs...")
    run(["git", "fetch", "origin"], check=True)

    print(f"Merging {base_ref} into current branch (no auto-commit)...")
    merge_proc = run(["git", "merge", "--no-commit", "--no-ff", base_ref], check=False)
    if merge_proc.returncode != 0:
        print("Merge reported conflicts. Attempting docs hotspot auto-resolution...")
        run([sys.executable, "scripts/resolve_docs_conflicts.py"], check=False)

    remaining = unresolved_files()
    if remaining:
        print("ERROR: Some conflicts remain. Resolve manually, then run:")
        print(f"  {sys.executable} scripts/docs_conflict_guard.py")
        print("  bash scripts/verne_smoke_checks.sh   # or Git Bash equivalent")
        return 1

    run_smoke_checks()

<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
=======
    branch = run(["git", "branch", "--show-current"], check=True).stdout.strip()
>>>>>>> theirs
=======
    branch = run(["git", "branch", "--show-current"], check=True).stdout.strip()
>>>>>>> theirs
=======
    branch = run(["git", "branch", "--show-current"], check=True).stdout.strip()
>>>>>>> theirs
=======
    branch = run(["git", "branch", "--show-current"], check=True).stdout.strip()
>>>>>>> theirs
    msg = f"Merge {base_ref} into {branch} with docs guard automation"
    print("Creating merge commit...")
    run(["git", "commit", "-m", msg], check=True)

    print("Done. Push your branch to update the existing PR.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
