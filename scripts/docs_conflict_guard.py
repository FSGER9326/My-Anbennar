#!/usr/bin/env python3
"""Guard against leftover merge conflicts in docs and automation hotspots."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MARKERS = ("<<<<<<<", "=======", ">>>>>>>")
CHECK_NAME = "docs_conflict_guard"

HOTSPOT_FILES = [
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

HEADING_SINGLETON_RULES: dict[str, list[str]] = {
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
}


def iter_guard_files() -> list[Path]:
    files: dict[Path, None] = {}
    for doc in (ROOT / "docs").rglob("*.md"):
        files[doc] = None
    for pattern in ("*.py", "*.ps1", "*.sh"):
        for script in (ROOT / "scripts").glob(pattern):
            files[script] = None
    workflow_root = ROOT / ".github" / "workflows"
    if workflow_root.exists():
        for pattern in ("*.yml", "*.yaml"):
            for workflow in workflow_root.glob(pattern):
                files[workflow] = None
    files[ROOT / ".gitattributes"] = None
    return sorted(files)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _line_for_pattern(text: str, pattern: str) -> int | None:
    for idx, line in enumerate(text.splitlines(), start=1):
        if line.startswith(pattern):
            return idx
    return None


def _issue(*, severity: str, file: str, line: int | None, code: str, message: str, suggested_fix_command: str) -> dict[str, object]:
    return {
        "check": CHECK_NAME,
        "severity": severity,
        "file": file,
        "line": line,
        "code": code,
        "message": message,
        "suggested_fix_command": suggested_fix_command,
    }


def run_audit() -> list[dict[str, object]]:
    issues: list[dict[str, object]] = []
    for path in iter_guard_files():
        if not path.exists():
            continue
        rel = path.relative_to(ROOT).as_posix()
        text = read_text(path)
        for marker in MARKERS:
            line_no = _line_for_pattern(text, marker)
            if line_no is not None:
                issues.append(
                    _issue(
                        severity="error",
                        file=rel,
                        line=line_no,
                        code="MERGE_CONFLICT_MARKER",
                        message=f"merge conflict marker '{marker}' found",
                        suggested_fix_command=f"python3 scripts/resolve_docs_conflicts.py --paths {rel}",
                    )
                )

    for rel_path in HOTSPOT_FILES:
        path = ROOT / rel_path
        if not path.exists():
            issues.append(
                _issue(
                    severity="error",
                    file=rel_path,
                    line=None,
                    code="MISSING_HOTSPOT_FILE",
                    message="required hotspot file is missing",
                    suggested_fix_command=f"git restore --source=HEAD -- {rel_path}",
                )
            )
            continue

        text = read_text(path)
        for heading in HEADING_SINGLETON_RULES.get(rel_path, []):
            count = text.count(heading)
            if count != 1:
                issues.append(
                    _issue(
                        severity="error",
                        file=rel_path,
                        line=_line_for_pattern(text, heading),
                        code="HEADING_SINGLETON_VIOLATION",
                        message=f"heading '{heading}' appears {count} times (expected exactly 1)",
                        suggested_fix_command=f"python3 scripts/resolve_docs_conflicts.py --paths {rel_path}",
                    )
                )
    return issues


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()

    issues = run_audit()
    if args.format == "json":
        print(json.dumps({"check": CHECK_NAME, "status": "failed" if issues else "passed", "issues": issues}, indent=2))
        return 1 if issues else 0

    if issues:
        print("Docs/automation conflict guard failed:")
        for issue in issues:
            where = f"{issue['file']}:{issue['line']}" if issue["line"] else issue["file"]
            print(f" - [{issue['code']}] {where} - {issue['message']}")
        return 1

    print("Docs/automation conflict guard passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
