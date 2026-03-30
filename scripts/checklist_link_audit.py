#!/usr/bin/env python3
"""Check local markdown links in checklist/workflow docs."""
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
TARGET_DIRS = [ROOT / "docs/repo-maps", ROOT / "docs/wiki", ROOT / "docs/theorycrafting"]
LINK_RE = re.compile(
    r"\[[^\]]+\]\(("
    r"(?![a-zA-Z][a-zA-Z0-9+.-]*:)"
    r"(?:\./|\.\./)*"
    r"[^)#/]+(?:/[^)#/]+)*\.md"
    r"(?:#[^)]+)?"
    r")\)"
)


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


def run_self_test() -> int:
    """Regression fixture for markdown link matching behavior."""
    cases = [
        ("[same dir](README.md)", ["README.md"]),
        ("[same dir anchor](README.md#overview)", ["README.md#overview"]),
        ("[same dir explicit](./README.md)", ["./README.md"]),
        ("[up one](../foo/README.md#intro)", ["../foo/README.md#intro"]),
        ("[up two](../../foo/README.md#heading-1)", ["../../foo/README.md#heading-1"]),
        ("[nested](guides/setup/README.md)", ["guides/setup/README.md"]),
        ("[nested up](../guides/setup/README.md)", ["../guides/setup/README.md"]),
        ("[non-markdown](README.txt)", []),
        ("[image](./img/logo.png)", []),
        ("[web](https://example.com/README.md)", []),
        ("[mail](mailto:test@example.com)", []),
    ]

    failures: list[tuple[str, list[str], list[str]]] = []
    for fixture, expected in cases:
        found = LINK_RE.findall(fixture)
        if found != expected:
            failures.append((fixture, expected, found))

    if failures:
        print("Checklist link audit self-test failed:")
        for fixture, expected, found in failures:
            print(f" - fixture:  {fixture}")
            print(f"   expected: {expected}")
            print(f"   found:    {found}")
        return 1

    print(f"Checklist link audit self-test passed ({len(cases)} fixtures).")
    return 0


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "--self-test":
        return run_self_test()

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
