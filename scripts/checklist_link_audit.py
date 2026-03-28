#!/usr/bin/env python3
"""Check local markdown links in checklist/workflow docs."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
TARGET_DIRS = [ROOT / "docs/repo-maps", ROOT / "docs/wiki", ROOT / "docs/theorycrafting"]
CHECK_NAME = "checklist_link_audit"
LINK_RE = re.compile(
    r"\[[^\]]+\]\(("
    r"(?![a-zA-Z][a-zA-Z0-9+.-]*:)"
    r"(?:\./|\.\./)*"
    r"[^)#/]+(?:/[^)#/]+)*\.md"
    r"(?:#[^)]+)?"
    r")\)"
)


def slugify_heading(heading: str) -> str:
    text = heading.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def heading_slugs(markdown_file: Path) -> set[str]:
    slugs: set[str] = set()
    text = markdown_file.read_text(encoding="utf-8")
    for line in text.splitlines():
        match = re.match(r"^#{1,6}\s+(.*?)\s*#*\s*$", line)
        if match:
            slug = slugify_heading(match.group(1))
            if slug:
                slugs.add(slug)
    return slugs


def _issue(*, file: str, line: int | None, code: str, message: str, suggested_fix_command: str) -> dict[str, object]:
    return {
        "check": CHECK_NAME,
        "severity": "error",
        "file": file,
        "line": line,
        "code": code,
        "message": message,
        "suggested_fix_command": suggested_fix_command,
    }


def run_self_test() -> int:
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
    for fixture, expected in cases:
        if LINK_RE.findall(fixture) != expected:
            print("Checklist link audit self-test failed")
            return 1
    print(f"Checklist link audit self-test passed ({len(cases)} fixtures).")
    return 0


def run_audit() -> tuple[list[dict[str, object]], int]:
    issues: list[dict[str, object]] = []
    checked = 0
    slug_cache: dict[Path, set[str]] = {}

    for base in TARGET_DIRS:
        if not base.exists():
            continue
        for md in base.rglob("*.md"):
            text = md.read_text(encoding="utf-8")
            lines = text.splitlines()
            for ln, line in enumerate(lines, start=1):
                for rel in LINK_RE.findall(line):
                    checked += 1
                    path_part, _, anchor_part = rel.partition("#")
                    target = (md.parent / path_part).resolve()
                    rel_md = md.relative_to(ROOT).as_posix()
                    if not target.exists():
                        issues.append(
                            _issue(
                                file=rel_md,
                                line=ln,
                                code="MISSING_LINK_TARGET",
                                message=f"missing file target: {rel}",
                                suggested_fix_command=f"python3 scripts/checklist_link_audit.py --format text",
                            )
                        )
                        continue
                    if anchor_part:
                        slugs = slug_cache.get(target)
                        if slugs is None:
                            slugs = heading_slugs(target)
                            slug_cache[target] = slugs
                        if anchor_part not in slugs:
                            issues.append(
                                _issue(
                                    file=rel_md,
                                    line=ln,
                                    code="MISSING_LINK_ANCHOR",
                                    message=f"missing anchor in existing file: {rel}",
                                    suggested_fix_command=f"python3 scripts/checklist_link_audit.py --format text",
                                )
                            )
    return issues, checked


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()

    if args.self_test:
        return run_self_test()

    issues, checked = run_audit()
    if args.format == "json":
        print(json.dumps({"check": CHECK_NAME, "status": "failed" if issues else "passed", "checked": checked, "issues": issues}, indent=2))
        return 1 if issues else 0

    if issues:
        print("Checklist link audit failed:")
        for e in issues:
            print(f" - [{e['code']}] {e['file']}:{e['line']} - {e['message']}")
        return 1

    print(f"Checklist link audit passed: {checked} local markdown links checked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
