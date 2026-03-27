#!/usr/bin/env python3
"""Check local markdown links in checklist/workflow docs."""
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
TARGET_DIRS = [ROOT / "docs/repo-maps", ROOT / "docs/wiki", ROOT / "docs/theorycrafting"]
LINK_RE = re.compile(r"\[[^\]]+\]\((\.?\.?/[^)]+\.md)\)")


def main() -> int:
    errors: list[str] = []
    checked = 0

    for base in TARGET_DIRS:
        for md in base.rglob("*.md"):
            text = md.read_text(encoding="utf-8")
            for rel in LINK_RE.findall(text):
                checked += 1
                target = (md.parent / rel).resolve()
                if not target.exists():
                    errors.append(f"{md.relative_to(ROOT)} -> missing link target: {rel}")

    if errors:
        print("Checklist link audit failed:")
        for e in errors:
            print(f" - {e}")
        return 1

    print(f"Checklist link audit passed: {checked} local markdown links checked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
