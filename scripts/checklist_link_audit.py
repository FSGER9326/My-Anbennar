#!/usr/bin/env python3
"""Check local markdown links in checklist/workflow docs."""
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
TARGET_DIRS = [ROOT / "docs/repo-maps", ROOT / "docs/wiki", ROOT / "docs/theorycrafting"]
LINK_RE = re.compile(r"\[[^\]]+\]\((\.?\.?/[^)#]+\.md(?:#[^)]+)?)\)")


def slugify_heading(heading: str) -> str:
    """Create a markdown heading slug for basic anchor validation."""
    text = heading.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def heading_slugs(markdown_file: Path) -> set[str]:
    """Collect slugs for ATX-style headings in the given markdown file."""
    slugs: set[str] = set()
    text = markdown_file.read_text(encoding="utf-8")
    for line in text.splitlines():
        match = re.match(r"^#{1,6}\s+(.*?)\s*#*\s*$", line)
        if not match:
            continue
        slug = slugify_heading(match.group(1))
        if slug:
            slugs.add(slug)
    return slugs


def main() -> int:
    errors: list[str] = []
    checked = 0
    slug_cache: dict[Path, set[str]] = {}

    for base in TARGET_DIRS:
        for md in base.rglob("*.md"):
            text = md.read_text(encoding="utf-8")
            for rel in LINK_RE.findall(text):
                checked += 1
                path_part, _, anchor_part = rel.partition("#")
                target = (md.parent / path_part).resolve()
                if not target.exists():
                    errors.append(f"{md.relative_to(ROOT)} -> missing file target: {rel}")
                    continue

                if anchor_part:
                    slugs = slug_cache.get(target)
                    if slugs is None:
                        slugs = heading_slugs(target)
                        slug_cache[target] = slugs
                    if anchor_part not in slugs:
                        errors.append(
                            f"{md.relative_to(ROOT)} -> missing anchor in existing file: {rel}"
                        )

    if errors:
        print("Checklist link audit failed:")
        for e in errors:
            print(f" - {e}")
        return 1

    print(f"Checklist link audit passed: {checked} local markdown links checked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
