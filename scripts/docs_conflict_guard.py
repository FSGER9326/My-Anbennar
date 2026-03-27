#!/usr/bin/env python3
"""Guardrails to reduce/spot common docs merge conflicts early."""
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]

HOTSPOT_FILES = [
    Path("docs/README.md"),
    Path("docs/implementation-crosswalk.md"),
    Path("docs/references/README.md"),
    Path("docs/references/reference-index.md"),
    Path("docs/repo-maps/README.md"),
    Path("docs/repo-maps/anbennar-systems-master-index.md"),
    Path("docs/repo-maps/anbennar-systems-scan-roadmap.md"),
]

HEADING_SINGLETON_RULES = {
    Path("docs/README.md"): [
        "### Repo grounding maps",
        "### Local references",
        "### Maintenance wiki",
    ],
    Path("docs/repo-maps/README.md"): [
        "Core indexes:",
    ],
}

CONFLICT_MARKERS = ("<<<<<<<", "=======", ">>>>>>>")


def fail(msg: str) -> None:
    print(f"ERROR: {msg}")


def main() -> int:
    failed = False

    for rel_path in HOTSPOT_FILES:
        path = REPO_ROOT / rel_path
        if not path.exists():
            fail(f"missing hotspot file: {rel_path}")
            failed = True
            continue

        text = path.read_text(encoding="utf-8", errors="ignore")

        for marker in CONFLICT_MARKERS:
            if marker in text:
                fail(f"merge conflict marker '{marker}' found in {rel_path}")
                failed = True

        for heading in HEADING_SINGLETON_RULES.get(rel_path, []):
            count = text.count(heading)
            if count != 1:
                fail(
                    f"heading '{heading}' appears {count} times in {rel_path} (expected exactly 1)"
                )
                failed = True

    if failed:
        print("\nHow to fix quickly:")
        print("1) Keep both sides only when both add unique content.")
        print("2) Remove duplicate repeated sections in docs index files.")
        print("3) Re-run: ./scripts/docs_conflict_guard.py")
        return 1

    print("Docs conflict guard passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
