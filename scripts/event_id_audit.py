#!/usr/bin/env python3
"""Audit EU4 event IDs for common beginner mistakes.

Checks include duplicate event IDs both within a single file and across files.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FILES = [
    "events/Flavour_Verne_A33.txt",
]
NAMESPACE_RE = re.compile(r"(?m)^\s*namespace\s*=\s*([A-Za-z0-9_.-]+)\s*$")
EVENT_BLOCK_START_RE = re.compile(
    r"^\s*(country_event|province_event|character_event|triggered_only_event)\s*=\s*\{\s*$"
)
EVENT_ID_RE = re.compile(r"^\s*id\s*=\s*([A-Za-z0-9_.-]+\.\d+)\s*$")


def extract_event_ids_with_lines(text: str) -> list[tuple[str, int]]:
    ids: list[tuple[str, int]] = []
    depth = 0
    in_event = False
    event_depth = -1

    for line_no, line in enumerate(text.splitlines(), start=1):
        if EVENT_BLOCK_START_RE.match(line):
            in_event = True
            event_depth = depth + 1

        if in_event:
            match = EVENT_ID_RE.match(line)
            if match:
                ids.append((match.group(1), line_no))

        depth += line.count("{")
        depth -= line.count("}")

        if in_event and depth < event_depth:
            in_event = False
            event_depth = -1

    return ids


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file",
        action="append",
        dest="files",
        help="Event script path relative to repo root (repeatable).",
    )
    args = parser.parse_args()

    file_list = args.files if args.files else DEFAULT_FILES
    targets = [ROOT / p for p in file_list]

    errors: list[str] = []
    seen_ids: dict[str, list[str]] = defaultdict(list)

    for path in targets:
        if not path.exists():
            errors.append(f"missing file: {path.relative_to(ROOT)}")
            continue

        text = path.read_text(encoding="utf-8", errors="replace")
        namespaces = set(NAMESPACE_RE.findall(text))
        ids = extract_event_ids_with_lines(text)

        if ids and not namespaces:
            errors.append(f"{path.relative_to(ROOT)}: contains event ids but no namespace declaration")

        for event_id, line_no in ids:
            ns = event_id.split(".", 1)[0]
            if namespaces and ns not in namespaces:
                errors.append(
                    f"{path.relative_to(ROOT)}: id '{event_id}' uses namespace '{ns}' not declared in file"
                )
            seen_ids[event_id].append(f"{path.relative_to(ROOT)}:{line_no}")

    for event_id, locations in sorted(seen_ids.items()):
        if len(locations) > 1:
            errors.append(
                f"duplicate event id '{event_id}' found across files/lines: {', '.join(locations)}"
            )

    if errors:
        print("Event ID audit failed:")
        for error in errors:
            print(f" - {error}")
        return 1

    print(f"Event ID audit passed: {len(targets)} file(s) scanned, {len(seen_ids)} ids checked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
