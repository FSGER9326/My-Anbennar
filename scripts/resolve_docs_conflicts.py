#!/usr/bin/env python3
"""Auto-resolve known docs hotspot conflicts during PR branch sync."""
from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

HOTSPOTS = [
    ".gitattributes",
    "docs/README.md",
    "docs/start-here.md",
    "docs/implementation-crosswalk.md",
    "docs/references/README.md",
    "docs/references/reference-index.md",
    "docs/repo-maps/README.md",
    "docs/repo-maps/anbennar-vs-eu4-mechanics-gap-register.md",
    "docs/repo-maps/anbennar-systems-master-index.md",
    "docs/repo-maps/anbennar-systems-scan-roadmap.md",
    "docs/wiki/checklist-automation-system.md",
]

CANONICAL_GITATTRIBUTES = """# Normalize repository text files consistently.
* text=auto

# Keep docs, automation, and workflow files on LF so merges stay predictable
# across desktop Codex, cloud Codex, GitHub, and local Windows tooling.
.gitattributes text eol=lf
automation/** text eol=lf
docs/** text eol=lf
scripts/** text eol=lf
.github/workflows/** text eol=lf

# Prefer additive auto-merge in documentation hotspot files to reduce manual
# conflict resolution in shared indexes and hub docs.
docs/README.md merge=union
docs/start-here.md merge=union
docs/implementation-crosswalk.md merge=union
docs/references/README.md merge=union
docs/references/reference-index.md merge=union
docs/repo-maps/README.md merge=union
docs/repo-maps/anbennar-vs-eu4-mechanics-gap-register.md merge=union
docs/repo-maps/anbennar-systems-master-index.md merge=union
docs/repo-maps/anbennar-systems-scan-roadmap.md merge=union
docs/wiki/checklist-automation-system.md merge=union
"""


def run_git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def unmerged_files() -> list[str]:
    result = run_git("diff", "--name-only", "--diff-filter=U")
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def stage_text(path: str, stage: int) -> str:
    result = run_git("show", f":{stage}:{path}")
    if result.returncode != 0:
        return ""
    return result.stdout


def dedupe_consecutive_lines(text: str) -> str:
    out: list[str] = []
    for line in text.splitlines():
        if out and out[-1] == line:
            continue
        out.append(line)
    return "\n".join(out).rstrip("\n") + "\n"


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8", newline="\n")


def resolve_file(path: str) -> bool:
    target = ROOT / path

    if path == ".gitattributes":
        write_text(target, CANONICAL_GITATTRIBUTES)
        return run_git("add", path).returncode == 0

    ours = stage_text(path, 2)
    theirs = stage_text(path, 3)
    if not ours and not theirs:
        return False

    merged = dedupe_consecutive_lines(f"{ours.rstrip()}\n\n{theirs.rstrip()}\n")
    write_text(target, merged)
    return run_git("add", path).returncode == 0


def main() -> int:
    unmerged = unmerged_files()
    if not unmerged:
        print("No unmerged files found.")
        return 0

    target = [path for path in unmerged if path in HOTSPOTS]
    skipped = [path for path in unmerged if path not in HOTSPOTS]

    if skipped:
        print("Skipped non-hotspot conflicts (manual resolution required):")
        for path in skipped:
            print(f" - {path}")

    resolved: list[str] = []
    for path in target:
        if resolve_file(path):
            resolved.append(path)

    if resolved:
        print("Auto-resolved hotspot files:")
        for path in resolved:
            print(f" - {path}")

    remaining = unmerged_files()
    if remaining:
        print("Remaining unresolved files:")
        for path in remaining:
            print(f" - {path}")
        return 1

    print("All hotspot conflicts resolved.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
