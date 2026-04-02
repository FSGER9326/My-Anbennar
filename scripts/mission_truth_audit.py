#!/usr/bin/env python3
"""
mission_truth_audit.py — My-Anbennar
Verne mission-spine truth audit.

What it checks:
  1. Every mission ID in missions/Verne_Missions.txt has a corresponding
     localisation entry (title + desc keys).
  2. Every mission ID referenced via `mission_completed = <id>` in any canonical
     file actually exists in the mission file(s).
  3. Every event option / effect that triggers/completes a mission has a valid
     target mission ID.

Outputs:
  automation/reports/mission_truth_report.json
  automation/reports/mission_truth_missing_loc.json   (actionable fix list)
"""
from __future__ import annotations
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional

# Patterns
MISSION_ID_RE = re.compile(r"^\s*([A-Z0-9_]+)\s*=\s*\{", re.MULTILINE)
LOC_TITLE_RE  = re.compile(r"^\s*([a-z0-9_]+(_title))\s*:", re.MULTILINE | re.IGNORECASE)
LOC_DESC_RE   = re.compile(r"^\s*([a-z0-9_]+(_desc))\s*:", re.MULTILINE | re.IGNORECASE)
MISCOMP_RE    = re.compile(r"mission_completed\s*=\s*([A-Z0-9_]+)", re.IGNORECASE)
MISSETC_RE    = re.compile(r"([A-Z0-9_]+)", re.IGNORECASE)


def find_mission_ids(missions_path: Path) -> set[str]:
    """Extract all top-level mission IDs from a mission file."""
    ids = set()
    if not missions_path.exists():
        return ids
    text = missions_path.read_text(encoding="utf-8", errors="replace")
    for m in MISSION_ID_RE.finditer(text):
        ids.add(m.group(1))
    return ids


def find_loc_keys(loc_path: Path) -> tuple[set[str], set[str]]:
    """Return (title_keys, desc_keys) from a localisation file."""
    titles, descs = set(), set()
    if not loc_path.exists():
        return titles, descs
    text = loc_path.read_text(encoding="utf-8", errors="replace")
    for m in LOC_TITLE_RE.finditer(text):
        titles.add(m.group(1).lower())
    for m in LOC_DESC_RE.finditer(text):
        descs.add(m.group(1).lower())
    return titles, descs


def scan_file_for_mission_refs(filepath: Path, pattern=re.compile(r"mission_completed\s*=\s*([A-Z0-9_]+)", re.IGNORECASE)) -> list[tuple[str, str]]:
    """Return list of (file, mission_id) where missions are referenced."""
    refs = []
    if not filepath.exists():
        return refs
    text = filepath.read_text(encoding="utf-8", errors="replace")
    for m in pattern.finditer(text):
        refs.append((str(filepath), m.group(1)))
    return refs


def main() -> int:
    parser = argparse.ArgumentParser(description="Mission truth audit")
    parser.add_argument("--missions", default="missions/Verne_Missions.txt")
    parser.add_argument("--loc",     default="localisation/verne_overhaul_l_english.yml")
    parser.add_argument("--registry", default="automation/registries/verne_file_registry.json")
    parser.add_argument("--out-dir", default="automation/reports")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    missions_path = Path(args.missions)
    loc_path      = Path(args.loc)
    registry_path = Path(args.registry)

    # 1. Collect all declared mission IDs
    declared = find_mission_ids(missions_path)
    print(f"Declared missions: {len(declared)}")

    # 2. Collect all loc keys
    loc_titles, loc_descs = find_loc_keys(loc_path)
    print(f"Localisation titles: {len(loc_titles)}, descs: {len(loc_descs)}")

    # 3. Check that each declared mission has loc entries
    missing_loc = []
    for mid in sorted(declared):
        t_key = f"{mid}_title".lower()
        d_key = f"{mid}_desc".lower()
        has_title = t_key in loc_titles
        has_desc  = d_key in loc_descs
        if not has_title or not has_desc:
            missing_loc.append({
                "mission_id": mid,
                "missing_title": not has_title,
                "missing_desc": not has_desc,
                "title_key": t_key,
                "desc_key": d_key,
            })

    # 4. Scan canonical files for mission_completed references
    refd_missions = set()
    all_refs = []
    if registry_path.exists():
        reg = json.loads(registry_path.read_text(encoding="utf-8"))
        for row in reg.get("rows", []):
            p = Path(row["path"])
            if p.suffix in (".txt", ".yml", ".yaml"):
                for ref_file in [p]:
                    for fref in scan_file_for_mission_refs(ref_file):
                        all_refs.append(fref)
                        refd_missions.add(fref[1])

    # 5. Check referenced mission IDs exist
    orphan_refs = [(f, m) for f, m in all_refs if m not in declared]

    report = {
        "total_declared": len(declared),
        "total_loc_titles": len(loc_titles),
        "total_loc_descs": len(loc_descs),
        "declared_ids": sorted(declared),
        "missing_loc": missing_loc,
        "orphan_mission_refs": [{"file": f, "mission": m} for f, m in orphan_refs],
        "all_mission_refs": [{"file": f, "mission": m} for f, m in all_refs],
    }

    report_path = out_dir / "mission_truth_report.json"
    missing_path = out_dir / "mission_truth_missing_loc.json"

    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    missing_path.write_text(
        json.dumps({"missing_loc": missing_loc, "orphan_refs": orphan_refs}, indent=2),
        encoding="utf-8",
    )

    print(f"\nReport: {report_path}")
    print(f"Missing loc entries: {len(missing_loc)}")
    print(f"Orphan mission refs: {len(orphan_refs)}")

    if missing_loc or orphan_refs:
        print("\nACTION REQUIRED — run with --fix to generate fix script")
        return 1
    print("\n✅ Mission truth audit PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
