#!/usr/bin/env python3
"""Generic checklist manifest audit.

Default behavior is compatible with the current Verne setup, but the script can
be reused for other country projects by passing a different manifest and index files.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

DEFAULT_STATUS = {"active", "draft", "archived", "needs_revalidation"}
REQUIRED_FIELDS = ("id", "path", "category", "scanned", "mapped", "verified", "automation", "status")


def run_audit(root: Path, manifest: Path, index_files: list[Path], allowed_status: set[str], require_smoke_text: bool) -> tuple[int, str]:
    errors: list[str] = []

    if not manifest.exists():
        return 1, f"ERROR: missing manifest: {manifest}"

    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return (
            1,
            (
                f"ERROR: invalid JSON in manifest {manifest} "
                f"(line {exc.lineno}, column {exc.colno}): {exc.msg}"
            ),
        )

    if not isinstance(data, dict):
        return 1, f"ERROR: manifest root must be a JSON object: {manifest}"

    items = data.get("items", [])
    if not items:
        return 1, "ERROR: manifest has no items"
    if not isinstance(items, list):
        return 1, "ERROR: manifest field 'items' must be a list"

    index_texts: list[str] = []
    for index_file in index_files:
        if not index_file.exists():
            rel = index_file.relative_to(root) if index_file.is_relative_to(root) else index_file
            return 1, f"ERROR: missing index file: {rel}"

        try:
            index_texts.append(index_file.read_text(encoding="utf-8"))
        except OSError as exc:
            rel = index_file.relative_to(root) if index_file.is_relative_to(root) else index_file
            return 1, f"ERROR: unable to read index file {rel}: {exc}"

    for item in items:
        if not isinstance(item, dict):
            errors.append(f"<non-object-item>: item must be an object, got {type(item).__name__}")
            continue

        item_id = item.get("id", "<missing-id>")
        path = item.get("path")
        status = item.get("status")

        for field in REQUIRED_FIELDS:
            if field not in item:
                errors.append(f"{item_id}: missing field '{field}'")

        if status not in allowed_status:
            errors.append(f"{item_id}: invalid status '{status}'")

        if not isinstance(item.get("scanned"), bool) or not isinstance(item.get("mapped"), bool) or not isinstance(item.get("verified"), bool):
            errors.append(f"{item_id}: scanned/mapped/verified must be booleans")

        if not path:
            continue

        abs_path = root / path
        if not abs_path.exists():
            if status == "draft":
                # draft items may point to planned files that do not exist yet
                continue
            errors.append(f"{item_id}: missing file '{path}'")
            continue

        if item.get("category") == "repo_map":
            filename = Path(path).name
            for idx_file, idx_text in zip(index_files, index_texts):
                if filename not in idx_text:
                    errors.append(f"{item_id}: '{filename}' not found in {idx_file.relative_to(root)}")

        if require_smoke_text and item.get("category") == "repo_map" and item.get("verified") is True and abs_path.suffix == ".md":
            text = abs_path.read_text(encoding="utf-8")
            has_smoke = any(x in text for x in ("Smoke-check", "smoke-check", "Smoke check", "Smoke-test", "smoke-test", "Smoke test"))
            if not has_smoke:
                errors.append(f"{item_id}: verified repo-map missing smoke-check section")

    if errors:
        lines = ["Checklist audit failed:"] + [f" - {e}" for e in errors]
        return 1, "\n".join(lines)

    active = sum(1 for i in items if i.get("status") == "active")
    verified = sum(1 for i in items if i.get("verified") is True)
    return 0, f"Checklist audit passed: {len(items)} items, {active} active, {verified} verified."


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default="docs/repo-maps/checklist-status-manifest.json")
    parser.add_argument(
        "--index-file",
        action="append",
        default=[
            "docs/repo-maps/README.md",
            "docs/repo-maps/anbennar-systems-master-index.md",
            "docs/repo-maps/anbennar-systems-scan-roadmap.md",
        ],
        help="Repeatable. Files where repo-map entries must be indexed.",
    )
    parser.add_argument("--allow-status", action="append", default=list(DEFAULT_STATUS))
    parser.add_argument("--no-smoke-text-required", action="store_true")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    manifest = root / args.manifest
    index_files = [root / p for p in args.index_file]

    code, msg = run_audit(root, manifest, index_files, set(args.allow_status), not args.no_smoke_text_required)
    print(msg)
    return code


if __name__ == "__main__":
    sys.exit(main())
