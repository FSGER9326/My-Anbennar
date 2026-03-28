#!/usr/bin/env python3
"""Generic checklist manifest audit."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

DEFAULT_STATUS = {"active", "draft", "archived", "needs_revalidation"}
REQUIRED_FIELDS = ("id", "path", "category", "scanned", "mapped", "verified", "automation", "status")
DEFAULT_INDEX_FILES = [
    "docs/repo-maps/README.md",
    "docs/repo-maps/anbennar-systems-master-index.md",
    "docs/repo-maps/anbennar-systems-scan-roadmap.md",
]
CHECK_NAME = "checklist_manifest_audit"


def issue(file: str, line: int | None, code: str, message: str, suggested_fix_command: str, severity: str = "error") -> dict[str, object]:
    return {
        "check": CHECK_NAME,
        "severity": severity,
        "file": file,
        "line": line,
        "code": code,
        "message": message,
        "suggested_fix_command": suggested_fix_command,
    }


def run_audit(root: Path, manifest: Path, index_files: list[Path], allowed_status: set[str], require_smoke_text: bool) -> tuple[list[dict[str, object]], dict[str, int]]:
    issues: list[dict[str, object]] = []

    if not manifest.exists():
        rel = manifest.relative_to(root).as_posix()
        return [issue(rel, None, "MISSING_MANIFEST", "manifest file is missing", f"git restore --source=HEAD -- {rel}")], {}

    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        rel = manifest.relative_to(root).as_posix()
        return [issue(rel, exc.lineno, "INVALID_JSON", f"invalid JSON: {exc.msg}", f"python3 -m json.tool {rel} > /dev/null")], {}

    if not isinstance(data, dict):
        rel = manifest.relative_to(root).as_posix()
        return [issue(rel, 1, "INVALID_MANIFEST_ROOT", "manifest root must be a JSON object", "Edit manifest root to be a JSON object")], {}

    items = data.get("items", [])
    if not isinstance(items, list):
        rel = manifest.relative_to(root).as_posix()
        return [issue(rel, 1, "INVALID_ITEMS_TYPE", "manifest field 'items' must be a list", "Set manifest.items to a JSON array")], {}
    if not items:
        rel = manifest.relative_to(root).as_posix()
        return [issue(rel, 1, "EMPTY_ITEMS", "manifest has no items", "Populate manifest.items with checklist entries")], {}

    index_texts: list[str] = []
    for index_file in index_files:
        rel = index_file.relative_to(root).as_posix()
        if not index_file.exists():
            issues.append(issue(rel, None, "MISSING_INDEX_FILE", "missing index file", f"git restore --source=HEAD -- {rel}"))
            continue
        try:
            index_texts.append(index_file.read_text(encoding="utf-8"))
        except OSError as exc:
            issues.append(issue(rel, None, "UNREADABLE_INDEX_FILE", f"unable to read index file: {exc}", f"chmod +r {rel}"))

    rel_manifest = manifest.relative_to(root).as_posix()
    for idx, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            issues.append(issue(rel_manifest, idx, "ITEM_NOT_OBJECT", f"item must be object, got {type(item).__name__}", "Replace non-object list item with an object"))
            continue

        item_id = str(item.get("id", f"item#{idx}"))
        path = item.get("path")
        status = item.get("status")

        for field in REQUIRED_FIELDS:
            if field not in item:
                issues.append(issue(rel_manifest, idx, "MISSING_REQUIRED_FIELD", f"{item_id}: missing field '{field}'", f"Add field '{field}' to manifest item '{item_id}'"))

        if status not in allowed_status:
            issues.append(issue(rel_manifest, idx, "INVALID_STATUS", f"{item_id}: invalid status '{status}'", f"Set status to one of: {', '.join(sorted(allowed_status))}"))

        if not isinstance(item.get("scanned"), bool) or not isinstance(item.get("mapped"), bool) or not isinstance(item.get("verified"), bool):
            issues.append(issue(rel_manifest, idx, "INVALID_BOOLEAN_FIELDS", f"{item_id}: scanned/mapped/verified must be booleans", "Set scanned/mapped/verified to true/false"))

        if not path:
            continue

        abs_path = root / path
        if not abs_path.exists():
            if status != "draft":
                issues.append(issue(rel_manifest, idx, "MISSING_ITEM_FILE", f"{item_id}: missing file '{path}'", f"Create {path} or set status to 'draft'"))
            continue

        if item.get("category") == "repo_map":
            filename = Path(path).name
            for idx_file, idx_text in zip(index_files, index_texts):
                if filename not in idx_text:
                    issues.append(issue(rel_manifest, idx, "UNINDEXED_REPO_MAP", f"{item_id}: '{filename}' not found in {idx_file.relative_to(root)}", f"Add '{filename}' to {idx_file.relative_to(root)}"))

        if require_smoke_text and item.get("category") == "repo_map" and item.get("verified") is True and abs_path.suffix == ".md":
            text = abs_path.read_text(encoding="utf-8")
            has_smoke = any(x in text for x in ("Smoke-check", "smoke-check", "Smoke check", "Smoke-test", "smoke-test", "Smoke test"))
            if not has_smoke:
                issues.append(issue(rel_manifest, idx, "MISSING_SMOKE_SECTION", f"{item_id}: verified repo-map missing smoke-check section", f"Add a Smoke-check section to {path}"))

    stats = {
        "total_items": len(items),
        "active_items": sum(1 for i in items if isinstance(i, dict) and i.get("status") == "active"),
        "verified_items": sum(1 for i in items if isinstance(i, dict) and i.get("verified") is True),
    }
    return issues, stats


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default="docs/repo-maps/checklist-status-manifest.json")
    parser.add_argument("--index-file", action="append", default=None)
    parser.add_argument("--use-default-index-files", action="store_true")
    parser.add_argument("--allow-status", action="append", default=list(DEFAULT_STATUS))
    parser.add_argument("--no-smoke-text-required", action="store_true")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    manifest = root / args.manifest
    selected_index_files = DEFAULT_INDEX_FILES if (args.use_default_index_files or not args.index_file) else args.index_file
    index_files = [root / p for p in selected_index_files]

    issues, stats = run_audit(root, manifest, index_files, set(args.allow_status), not args.no_smoke_text_required)
    if args.format == "json":
        print(json.dumps({"check": CHECK_NAME, "status": "failed" if issues else "passed", "stats": stats, "issues": issues}, indent=2))
        return 1 if issues else 0

    if issues:
        print("Checklist audit failed:")
        for e in issues:
            where = f"{e['file']}:{e['line']}" if e["line"] else e["file"]
            print(f" - [{e['code']}] {where} - {e['message']}")
        return 1

    print(f"Checklist audit passed: {stats['total_items']} items, {stats['active_items']} active, {stats['verified_items']} verified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
