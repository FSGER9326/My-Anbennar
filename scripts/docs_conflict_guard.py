#!/usr/bin/env python3
"""Guardrails to reduce/spot common docs merge conflicts early."""
from pathlib import Path
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
import re
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]

HOTSPOT_FILES = [
    Path("docs/README.md"),
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
    Path("docs/start-here.md"),
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
    Path("docs/implementation-crosswalk.md"),
    Path("docs/references/README.md"),
    Path("docs/references/reference-index.md"),
    Path("docs/repo-maps/README.md"),
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
    Path("docs/repo-maps/anbennar-vs-eu4-mechanics-gap-register.md"),
    Path("docs/repo-maps/anbennar-systems-master-index.md"),
    Path("docs/repo-maps/anbennar-systems-scan-roadmap.md"),
    Path("docs/wiki/checklist-automation-system.md"),
=======
    Path("docs/repo-maps/anbennar-systems-master-index.md"),
    Path("docs/repo-maps/anbennar-systems-scan-roadmap.md"),
>>>>>>> theirs
=======
    Path("docs/repo-maps/anbennar-systems-master-index.md"),
    Path("docs/repo-maps/anbennar-systems-scan-roadmap.md"),
>>>>>>> theirs
=======
    Path("docs/repo-maps/anbennar-systems-master-index.md"),
    Path("docs/repo-maps/anbennar-systems-scan-roadmap.md"),
>>>>>>> theirs
=======
    Path("docs/repo-maps/anbennar-systems-master-index.md"),
    Path("docs/repo-maps/anbennar-systems-scan-roadmap.md"),
>>>>>>> theirs
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
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
    Path("docs/start-here.md"): [
        "## Tiny glossary (modding terms, not GitHub terms)",
        "## What should we do right now? (Decision guide)",
    ],
    Path("docs/repo-maps/anbennar-vs-eu4-mechanics-gap-register.md"): [
        "## High-value gap queue",
    ],
    Path("docs/wiki/checklist-automation-system.md"): [
        "## Automation commands",
        "## Merge-conflict prevention (docs hotspots)",
    ],
}

CONFLICT_MARKERS = ("<<<<<<<", "=======", ">>>>>>>")
CONFLICT_MARKER_REGEX = re.compile(r"(?m)^(<<<<<<<|=======|>>>>>>>)")
=======
}

CONFLICT_MARKERS = ("<<<<<<<", "=======", ">>>>>>>")
>>>>>>> theirs
=======
}

CONFLICT_MARKERS = ("<<<<<<<", "=======", ">>>>>>>")
>>>>>>> theirs
=======
}

CONFLICT_MARKERS = ("<<<<<<<", "=======", ">>>>>>>")
>>>>>>> theirs
=======
}

CONFLICT_MARKERS = ("<<<<<<<", "=======", ">>>>>>>")
>>>>>>> theirs


def fail(msg: str) -> None:
    print(f"ERROR: {msg}")


def main() -> int:
    failed = False

<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
    docs_root = REPO_ROOT / "docs"
    for path in sorted(docs_root.rglob("*.md")):
        rel_path = path.relative_to(REPO_ROOT)
        text = path.read_text(encoding="utf-8", errors="ignore")

        for match in CONFLICT_MARKER_REGEX.finditer(text):
            marker = match.group(1)
            fail(f"merge conflict marker '{marker}' found in {rel_path}")
            failed = True

=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
    for rel_path in HOTSPOT_FILES:
        path = REPO_ROOT / rel_path
        if not path.exists():
            fail(f"missing hotspot file: {rel_path}")
            failed = True
            continue

        text = path.read_text(encoding="utf-8", errors="ignore")

<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
=======
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
        for marker in CONFLICT_MARKERS:
            if marker in text:
                fail(f"merge conflict marker '{marker}' found in {rel_path}")
                failed = True

<<<<<<< ours
<<<<<<< ours
<<<<<<< ours
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs
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
