#!/usr/bin/env python3
"""Auto-resolve common docs conflict hotspots by combining ours+theirs text.

This is intentionally limited to known markdown hotspot files.
"""

from pathlib import Path
import subprocess
import sys

HOTSPOTS = {
    "docs/README.md",
    "docs/implementation-crosswalk.md",
    "docs/references/README.md",
    "docs/references/reference-index.md",
    "docs/repo-maps/README.md",
    "docs/repo-maps/anbennar-systems-master-index.md",
    "docs/repo-maps/anbennar-systems-scan-roadmap.md",
}


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, check=False, text=True, capture_output=True)


def get_unmerged() -> list[str]:
    proc = run(["git", "diff", "--name-only", "--diff-filter=U"])
    if proc.returncode != 0:
        print(proc.stderr, file=sys.stderr)
        return []
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def read_stage(path: str, stage: int) -> str:
    proc = run(["git", "show", f":{stage}:{path}"])
    if proc.returncode != 0:
        return ""
    return proc.stdout


def dedupe_lines(text: str) -> str:
    out: list[str] = []
    for line in text.splitlines():
        if out and out[-1] == line:
            continue
        out.append(line)
    # normalize trailing whitespace and ensure newline at EOF
    return "\n".join(out).rstrip() + "\n"


def resolve_file(path: str) -> bool:
    ours = read_stage(path, 2)
    theirs = read_stage(path, 3)
    if not ours and not theirs:
        return False

    merged = dedupe_lines(ours.rstrip("\n") + "\n\n" + theirs.rstrip("\n") + "\n")
    Path(path).write_text(merged, encoding="utf-8")

    add_proc = run(["git", "add", path])
    return add_proc.returncode == 0


def main() -> int:
    unmerged = get_unmerged()
    if not unmerged:
        print("No unmerged files found.")
        return 0

    target = [f for f in unmerged if f in HOTSPOTS]
    skipped = [f for f in unmerged if f not in HOTSPOTS]

    if skipped:
        print("Skipped non-hotspot conflicts (manual resolution required):")
        for f in skipped:
            print(f"- {f}")

    resolved = []
    for path in target:
        if resolve_file(path):
            resolved.append(path)

    if resolved:
        print("Auto-resolved hotspot files:")
        for f in resolved:
            print(f"- {f}")

    remaining = get_unmerged()
    if remaining:
        print("Remaining unresolved files:")
        for f in remaining:
            print(f"- {f}")
        return 1

    print("All conflicts resolved.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
