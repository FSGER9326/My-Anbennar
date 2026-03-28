#!/usr/bin/env python3
"""Audit EU4 event IDs for common beginner mistakes."""
from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FILES = ["events/Flavour_Verne_A33.txt", "events/verne_overhaul_dynasty_events.txt"]
NAMESPACE_RE = re.compile(r"(?m)^\s*namespace\s*=\s*([A-Za-z0-9_.-]+)\s*$")
EVENT_ASSIGN_RE = re.compile(r"^\s*(country_event|province_event|character_event|triggered_only_event)\s*=\s*(.*)$")
EVENT_ID_RE = re.compile(r"^\s*id\s*=\s*([A-Za-z0-9_.-]+\.\d+)\s*$")
CHECK_NAME = "event_id_audit"


def extract_event_ids(text: str) -> list[tuple[str, int]]:
    ids: list[tuple[str, int]] = []
    depth = 0
    in_event = False
    waiting_for_event_open = False
    event_depth = -1

    for line_no, line in enumerate(text.splitlines(), start=1):
        line_no_comment = line.split("#", 1)[0]
        if not in_event and waiting_for_event_open:
            if "{" in line_no_comment:
                in_event = True
                waiting_for_event_open = False
                event_depth = depth + 1
            elif line_no_comment.strip():
                waiting_for_event_open = False

        if not in_event and not waiting_for_event_open:
            assign_match = EVENT_ASSIGN_RE.match(line_no_comment)
            if assign_match:
                waiting_for_event_open = True
                if "{" in assign_match.group(2):
                    in_event = True
                    waiting_for_event_open = False
                    event_depth = depth + 1

        if in_event:
            match = EVENT_ID_RE.match(line_no_comment)
            if match:
                ids.append((match.group(1), line_no))

        depth += line.count("{")
        depth -= line.count("}")
        if in_event and depth < event_depth:
            in_event = False
            event_depth = -1
    return ids


def _issue(file: str, line: int | None, code: str, message: str, suggested_fix_command: str, severity: str = "error") -> dict[str, object]:
    return {"check": CHECK_NAME, "severity": severity, "file": file, "line": line, "code": code, "message": message, "suggested_fix_command": suggested_fix_command}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", action="append", dest="files", help="Event script path relative to repo root (repeatable).")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()

    file_list = args.files if args.files else DEFAULT_FILES
    targets = [ROOT / p for p in file_list]

    issues: list[dict[str, object]] = []
    seen_ids: dict[str, list[tuple[str, int]]] = defaultdict(list)

    for path in targets:
        rel = path.relative_to(ROOT).as_posix()
        if not path.exists():
            issues.append(_issue(rel, None, "MISSING_EVENT_FILE", "event script file is missing", f"git restore --source=HEAD -- {rel}"))
            continue

        text = path.read_text(encoding="utf-8", errors="replace")
        namespaces = set(NAMESPACE_RE.findall(text))
        ids = extract_event_ids(text)

        if ids and not namespaces:
            issues.append(_issue(rel, ids[0][1], "MISSING_NAMESPACE", "contains event ids but no namespace declaration", f"sed -i '1inamespace = your_namespace' {rel}"))

        for event_id, line_no in ids:
            ns = event_id.split(".", 1)[0]
            if namespaces and ns not in namespaces:
                issues.append(_issue(rel, line_no, "UNDECLARED_NAMESPACE_IN_ID", f"id '{event_id}' uses namespace '{ns}' not declared in file", "Update id namespace or add matching namespace declaration"))
            seen_ids[event_id].append((rel, line_no))

    for event_id, where in sorted(seen_ids.items()):
        files = sorted({f for f, _ in where})
        if len(files) > 1:
            first_file, first_line = where[0]
            issues.append(_issue(first_file, first_line, "DUPLICATE_EVENT_ID", f"duplicate event id '{event_id}' found across files: {', '.join(files)}", "Rename one of the duplicated event IDs to a unique numeric suffix"))

    if args.format == "json":
        print(json.dumps({"check": CHECK_NAME, "status": "failed" if issues else "passed", "scanned_files": len(targets), "checked_ids": len(seen_ids), "issues": issues}, indent=2))
        return 1 if issues else 0

    if issues:
        print("Event ID audit failed:")
        for e in issues:
            where = f"{e['file']}:{e['line']}" if e["line"] else e["file"]
            print(f" - [{e['code']}] {where} - {e['message']}")
        return 1

    print(f"Event ID audit passed: {len(targets)} file(s) scanned, {len(seen_ids)} ids checked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
