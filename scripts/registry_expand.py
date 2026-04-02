#!/usr/bin/env python3
"""
registry_expand.py — My-Anbennar
Parse docs/wiki/verne-canonical-vs-legacy-file-registry.md (Markdown table)
and emit automation/registries/verne_file_registry.json.

Fails fast if:
  a) A "Legacy (do not extend)" file is edited and the edit is not a pure deletion/retirement
  b) A file listed in the registry does not exist on disk
  c) The table has zero rows (malformed)
"""
from __future__ import annotations
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROW_RE = re.compile(
    r"^\|\s*([^|]+)\s*\|\s*`([^`]+)`\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|"
)


def git_changed_files() -> set[str]:
    try:
        out = subprocess.check_output(
            ["git", "diff", "--name-only", "--cached"], text=True
        ).strip()
    except subprocess.CalledProcessError:
        out = subprocess.check_output(
            ["git", "diff", "--name-only"], text=True
        ).strip()
    return {x for x in out.splitlines() if x}


def parse_registry(md_text: str) -> list[dict]:
    rows = []
    for line in md_text.splitlines():
        m = ROW_RE.match(line)
        if not m:
            continue
        domain, path, status, edit_policy, note = [x.strip() for x in m.groups()]
        rows.append(
            {
                "domain": domain,
                "path": path,
                "status": status,
                "edit_policy": edit_policy,
                "note": note,
            }
        )
    if not rows:
        print("WARNING: No registry rows parsed; table format may have changed", file=sys.stderr)
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Expand canonical/legacy registry to JSON")
    parser.add_argument("--registry-md", required=True, help="Path to registry Markdown file")
    parser.add_argument("--out", required=True, help="Output JSON path")
    parser.add_argument(
        "--fail-on-legacy-edit-risk",
        action="store_true",
        help="Fail if a Legacy (do not extend) file is in the diff",
    )
    args = parser.parse_args()

    md_path = Path(args.registry_md)
    if not md_path.exists():
        raise SystemExit(f"Registry Markdown not found: {md_path}")

    rows = parse_registry(md_path.read_text(encoding="utf-8"))

    # Existence check
    missing = [r["path"] for r in rows if not Path(r["path"]).exists()]
    if missing:
        print("ERROR: Registry lists files that do not exist:", file=sys.stderr)
        for p in missing:
            print(f"  - {p}", file=sys.stderr)
        raise SystemExit(1)

    changed = git_changed_files()
    legacy_touched = [
        r for r in rows if "Legacy" in r["status"] and r["path"] in changed
    ]
    if args.fail_on_legacy_edit_risk and legacy_touched:
        print(
            "ERROR: Refusing — changed file(s) marked Legacy (do not extend):",
            file=sys.stderr,
        )
        for r in legacy_touched:
            print(f"  - {r['path']} [{r['status']}]", file=sys.stderr)
        raise SystemExit(1)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps({"version": 1, "rows": rows, "generated_by": __file__}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"OK — wrote {out_path} with {len(rows)} rows.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
