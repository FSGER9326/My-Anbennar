#!/usr/bin/env python3
"""Audit EU4 localisation files for beginner mistakes."""
from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FILES = ["localisation/Flavour_Verne_A33_l_english.yml"]
HEADER_RE = re.compile(r"^\s*l_[a-z_]+:\s*$")
KEY_RE = re.compile(r'^\s*([^#\s][^:]*)\s*:\s*\d+\s+"')
CHECK_NAME = "localisation_audit"


def _issue(file: str, line: int | None, code: str, message: str, suggested_fix_command: str, severity: str = "error") -> dict[str, object]:
    return {
        "check": CHECK_NAME,
        "severity": severity,
        "file": file,
        "line": line,
        "code": code,
        "message": message,
        "suggested_fix_command": suggested_fix_command,
    }


def audit_file(root: Path, rel_path: Path, key_index: dict[str, list[tuple[str, int]]], issues: list[dict[str, object]]) -> None:
    path = root / rel_path
    data = path.read_bytes()
    rel = rel_path.as_posix()
    if not data.startswith(b"\xef\xbb\xbf"):
        issues.append(_issue(rel, 1, "MISSING_UTF8_BOM", "expected UTF-8 BOM (use UTF-8 with BOM)", f"python3 -c \"from pathlib import Path;p=Path('{rel}');t=p.read_text(encoding='utf-8',errors='replace');p.write_text(t,encoding='utf-8-sig')\""))

    text = data.decode("utf-8-sig", errors="replace")
    lines = text.splitlines()

    first_non_empty_line_no = None
    first_non_empty = ""
    for i, line in enumerate(lines, start=1):
        if line.strip():
            first_non_empty = line
            first_non_empty_line_no = i
            break

    if first_non_empty_line_no is None or not HEADER_RE.match(first_non_empty):
        issues.append(_issue(rel, first_non_empty_line_no or 1, "INVALID_LOCALISATION_HEADER", "missing/invalid localisation header (expected e.g. 'l_english:')", f"sed -i '1s/^/l_english:\\n/' {rel}"))

    for line_no, line in enumerate(lines, start=1):
        m = KEY_RE.match(line)
        if m:
            key = m.group(1).strip()
            key_index[key].append((rel, line_no))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", action="append", dest="files", help="Localisation file relative to repo root (repeatable).")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()

    file_list = args.files if args.files else DEFAULT_FILES
    targets = [ROOT / p for p in file_list]

    issues: list[dict[str, object]] = []
    key_index: dict[str, list[tuple[str, int]]] = defaultdict(list)

    for path in targets:
        rel = path.relative_to(ROOT).as_posix()
        if not path.exists():
            issues.append(_issue(rel, None, "MISSING_LOCALISATION_FILE", "localisation file is missing", f"git restore --source=HEAD -- {rel}"))
            continue
        if path.suffix.lower() != ".yml":
            issues.append(_issue(rel, None, "INVALID_LOCALISATION_EXTENSION", "expected .yml localisation file", "Rename file extension to .yml"))
            continue
        audit_file(ROOT, path.relative_to(ROOT), key_index, issues)

    for key, occurrences in sorted(key_index.items()):
        if len(occurrences) > 1:
            joined = ", ".join(f"{f}:{ln}" for f, ln in occurrences)
            first_file, first_line = occurrences[0]
            issues.append(_issue(first_file, first_line, "DUPLICATE_LOCALISATION_KEY", f"duplicate localisation key '{key}' found at: {joined}", "Rename duplicate key(s) so each key is globally unique"))

    if args.format == "json":
        print(json.dumps({"check": CHECK_NAME, "status": "failed" if issues else "passed", "scanned_files": len(targets), "indexed_keys": len(key_index), "issues": issues}, indent=2))
        return 1 if issues else 0

    if issues:
        print("Localisation audit failed:")
        for err in issues:
            where = f"{err['file']}:{err['line']}" if err["line"] else err["file"]
            print(f" - [{err['code']}] {where} - {err['message']}")
        return 1

    print(f"Localisation audit passed: {len(targets)} file(s) scanned, {len(key_index)} keys indexed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
