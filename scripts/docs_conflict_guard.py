#!/usr/bin/env python3
"""Guard against leftover merge conflicts in docs and automation hotspots."""
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MARKERS = ("<<<<<<<", "=======", ">>>>>>>")

HOTSPOT_FILES = [
    "README.md",
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
    "docs/wiki/current-work-queue.md",
]

HEADING_SINGLETON_RULES: dict[str, list[str]] = {
    "README.md": [
        "## Main areas",
        "## Current project docs",
    ],
    "docs/README.md": [
        "### Repo grounding maps",
        "### Local references",
        "### Maintenance wiki",
    ],
    "docs/repo-maps/README.md": [
        "Core indexes:",
    ],
    "docs/start-here.md": [
        "## Tiny glossary (modding terms, not GitHub terms)",
        "## What should we do right now? (Decision guide)",
    ],
    "docs/repo-maps/anbennar-vs-eu4-mechanics-gap-register.md": [
        "## High-value gap queue",
    ],
    "docs/wiki/checklist-automation-system.md": [
        "## Automation commands",
        "## Merge-conflict prevention",
        "## Feature-branch sync",
    ],
    "docs/wiki/current-work-queue.md": [
        "## Now (max 1 item)",
        "## Next (max 3 items)",
        "## Parked",
    ],
}


def iter_guard_files() -> list[Path]:
    files: dict[Path, None] = {}

    for doc in (ROOT / "docs").rglob("*.md"):
        files[doc] = None

    files[ROOT / "README.md"] = None

    for pattern in ("*.py", "*.ps1", "*.sh"):
        for script in (ROOT / "scripts").glob(pattern):
            files[script] = None

    for pattern in ("*.yml", "*.yaml"):
        workflow_root = ROOT / ".github" / "workflows"
        if workflow_root.exists():
            for workflow in workflow_root.glob(pattern):
                files[workflow] = None

    files[ROOT / ".gitattributes"] = None
    return sorted(files)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def main() -> int:
    errors: list[str] = []

    for path in iter_guard_files():
        if not path.exists():
            continue

        rel = path.relative_to(ROOT).as_posix()
        text = read_text(path)

        for marker in MARKERS:
            if re.search(rf"(?m)^{re.escape(marker)}", text):
                errors.append(f"merge conflict marker '{marker}' found in {rel}")

    for rel_path in HOTSPOT_FILES:
        path = ROOT / rel_path
        if not path.exists():
            errors.append(f"missing hotspot file: {rel_path}")
            continue

        text = read_text(path)
        for heading in HEADING_SINGLETON_RULES.get(rel_path, []):
            count = text.count(heading)
            if count != 1:
                errors.append(
                    f"heading '{heading}' appears {count} times in {rel_path} "
                    "(expected exactly 1)"
                )

    if errors:
        print("Docs/automation conflict guard failed:")
        for error in errors:
            print(f" - {error}")
        print()
        print("How to fix quickly:")
        print("1) Remove leftover conflict markers first.")
        print("2) Keep docs hub headings unique in hotspot files.")
        print("3) Re-run the guard after resolving conflicts.")
        return 1

    print("Docs/automation conflict guard passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
