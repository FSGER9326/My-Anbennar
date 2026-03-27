#!/usr/bin/env python3
"""Report common local repo health issues for beginner-friendly workflows."""
from __future__ import annotations

from pathlib import Path
import argparse
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def run_git(*args: str) -> tuple[int, str]:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    text = "\n".join(part for part in (result.stdout.strip(), result.stderr.strip()) if part)
    return result.returncode, text


def status_line(level: str, label: str, message: str) -> str:
    return f"[{level}] {label}: {message}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true", help="Return non-zero when warnings/errors are found.")
    args = parser.parse_args()

    issues = 0
    warnings = 0
    lines: list[str] = []

    if shutil.which("git"):
        lines.append(status_line("OK", "git", "git is available"))
    else:
        lines.append(status_line("ERR", "git", "git is not on PATH"))
        issues += 1

    for tool in ("powershell", "python", "python3", "bash"):
        found = shutil.which(tool)
        if found:
            lines.append(status_line("OK", tool, found))
        else:
            lines.append(status_line("WARN", tool, "not found on PATH"))
            warnings += 1

    code, branch = run_git("branch", "--show-current")
    if code == 0 and branch:
        lines.append(status_line("OK", "branch", branch))
    else:
        lines.append(status_line("ERR", "branch", "could not determine current branch"))
        issues += 1
        branch = ""

    code, dirty = run_git("status", "--porcelain")
    if code == 0 and not dirty:
        lines.append(status_line("OK", "working-tree", "clean"))
    elif code == 0:
        lines.append(status_line("WARN", "working-tree", "has uncommitted changes"))
        warnings += 1
    else:
        lines.append(status_line("ERR", "working-tree", "could not inspect working tree"))
        issues += 1

    code, upstream = run_git("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}")
    if code == 0 and upstream:
        lines.append(status_line("OK", "upstream", upstream))
        c2, counts = run_git("rev-list", "--left-right", "--count", f"HEAD...{upstream}")
        if c2 == 0 and counts:
            behind, ahead = [int(part) for part in counts.split()]
            if ahead == 0 and behind == 0:
                lines.append(status_line("OK", "sync", "local branch matches upstream"))
            else:
                lines.append(status_line("WARN", "sync", f"ahead {ahead}, behind {behind}"))
                warnings += 1
    else:
        lines.append(status_line("WARN", "upstream", "no upstream branch configured"))
        warnings += 1

    git_dir = ROOT / ".git"
    if (git_dir / "MERGE_HEAD").exists():
        lines.append(status_line("WARN", "merge-state", "merge in progress"))
        warnings += 1
    else:
        lines.append(status_line("OK", "merge-state", "no merge in progress"))

    if (git_dir / "rebase-apply").exists() or (git_dir / "rebase-merge").exists():
        lines.append(status_line("WARN", "rebase-state", "rebase in progress"))
        warnings += 1
    else:
        lines.append(status_line("OK", "rebase-state", "no rebase in progress"))

    code, hooks_path = run_git("config", "--get", "core.hooksPath")
    if code == 0 and hooks_path.strip() == ".githooks":
        lines.append(status_line("OK", "hooks-path", ".githooks installed"))
    elif code == 0 and hooks_path.strip():
        lines.append(status_line("WARN", "hooks-path", f"custom hooksPath is '{hooks_path.strip()}'"))
        warnings += 1
    else:
        lines.append(status_line("WARN", "hooks-path", "hooks not installed (run install_git_hooks)"))
        warnings += 1

    for rel in (
        ".githooks/pre-commit",
        ".githooks/pre-push",
        "scripts/verne_smoke_checks.ps1",
        "scripts/smart_smoke_router.ps1",
        "scripts/repo_doctor.ps1",
    ):
        path = ROOT / rel
        if path.exists():
            lines.append(status_line("OK", rel, "present"))
        else:
            lines.append(status_line("WARN", rel, "missing"))
            warnings += 1

    print("Repo doctor report")
    print("==================")
    for line in lines:
        print(line)

    if warnings or issues:
        print()
        print("Recommended next actions:")
        if branch == "main":
            print("- Stay on small commits and run verne_smoke_checks before push.")
        if code != 0 or not upstream:
            print("- Set or confirm upstream tracking for your active branch.")
        print("- Install Git hooks if you want automatic checks before commit/push.")
        print("- Run text_hygiene_guard if docs or localisation text starts looking strange.")

    if args.strict and (issues or warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
