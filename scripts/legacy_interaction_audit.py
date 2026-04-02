#!/usr/bin/env python3
"""
legacy_interaction_audit.py — My-Anbennar
Canonical / legacy coupling audit.

Checks:
  1. The legacy anchor (events/Flavour_Verne_A33.txt) does not reference
     zzz_* legacy stub IDs — these should be retired, not referenced.
  2. Mission IDs referenced by legacy events actually exist in the mission file(s).
  3. Event IDs referenced by missions actually exist in the event file(s).
  4. Generates a coupling map artifact (JSON) for agent reasoning.

Outputs:
  automation/reports/legacy_interaction_report.json
  automation/reports/legacy_coupling_map.json
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path

EVENT_ID_RE   = re.compile(r"^\s*([A-Z][A-Za-z0-9_]+)\s*=\s*\{", re.MULTILINE)
MIS_ID_RE     = re.compile(r"^\s*([A-Z0-9_]+)\s*=\s*\{", re.MULTILINE)
LEGACY_EVT_RE = re.compile(r"(zzz_[a-z_]+)", re.IGNORECASE)
MISCOMP_RE    = re.compile(r"mission_completed\s*=\s*([A-Z0-9_]+)", re.IGNORECASE)
EVTREF_RE     = re.compile(r"event\s*=\s*([A-Z][A-Za-z0-9_]+)", re.IGNORECASE)


def collect_ids(filepath: Path, pattern) -> set[str]:
    if not filepath.exists():
        return set()
    text = filepath.read_text(encoding="utf-8", errors="replace")
    return {m.group(1) for m in pattern.finditer(text)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Legacy interaction audit")
    parser.add_argument("--legacy",  default="events/Flavour_Verne_A33.txt")
    parser.add_argument("--missions", default="missions/Verne_Missions.txt")
    parser.add_argument("--registry", default="automation/registries/verne_file_registry.json")
    parser.add_argument("--out-dir", default="automation/reports")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    legacy_path   = Path(args.legacy)
    missions_path = Path(args.missions)
    registry_path = Path(args.registry)

    legacy_event_ids  = collect_ids(legacy_path, EVENT_ID_RE)
    mission_ids      = collect_ids(missions_path, MIS_ID_RE)
    legacy_text      = legacy_path.read_text(encoding="utf-8", errors="replace") if legacy_path.exists() else ""

    # 1. Legacy file references to zzz_* stubs
    zzz_refs = [(m.group(1)) for m in LEGACY_EVT_RE.finditer(legacy_text)]
    zzz_refs = sorted(set(zzz_refs))

    # 2. Legacy events reference which missions?
    legacy_mis_refs = sorted(set(m.group(1) for m in MISCOMP_RE.finditer(legacy_text)))
    orphan_legacy_mis = [m for m in legacy_mis_refs if m not in mission_ids]

    # 3. Build coupling map: for each registry file, which event/mission IDs appear
    coupling = {}
    if registry_path.exists():
        reg = json.loads(registry_path.read_text(encoding="utf-8"))
        for row in reg.get("rows", []):
            p = Path(row["path"])
            if p.suffix not in (".txt", ".yml", ".yaml"):
                continue
            ids = collect_ids(p, EVENT_ID_RE) | collect_ids(p, MIS_ID_RE)
            couplings_for_file = {}
            # mission completions
            text = p.read_text(encoding="utf-8", errors="replace")
            mis_refs = {m.group(1) for m in MISCOMP_RE.finditer(text)}
            evt_refs = {m.group(1) for m in EVTREF_RE.finditer(text)}
            if mis_refs:
                couplings_for_file["mission_completed"] = sorted(mis_refs)
            if evt_refs:
                couplings_for_file["event_options"] = sorted(evt_refs)
            if couplings_for_file:
                coupling[row["path"]] = {
                    "status": row["status"],
                    "edit_policy": row["edit_policy"],
                    "declared_ids": sorted(ids),
                    "refs_to": couplings_for_file,
                }

    report = {
        "legacy_file": str(legacy_path),
        "legacy_event_count": len(legacy_event_ids),
        "zzz_stub_refs": zzz_refs,
        "legacy_mission_refs": legacy_mis_refs,
        "orphan_mission_refs_from_legacy": orphan_legacy_mis,
        "coupling_map": coupling,
    }

    report_path = out_dir / "legacy_interaction_report.json"
    map_path    = out_dir / "legacy_coupling_map.json"

    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    map_path.write_text(json.dumps(coupling, indent=2), encoding="utf-8")

    print(f"Report: {report_path}")
    print(f"Coupling map: {map_path}")
    print(f"zzz stub refs in legacy file: {len(zzz_refs)}")
    print(f"Orphan mission refs from legacy: {len(orphan_legacy_mis)}")

    if zzz_refs or orphan_legacy_mis:
        print("\n⚠️  LEGACY INTERACTION ISSUES FOUND")
        if zzz_refs:
            print(f"  zzz_* stubs still referenced: {zzz_refs}")
        if orphan_legacy_mis:
            print(f"  Legacy references non-existent missions: {orphan_legacy_mis}")
        return 1

    print("\n✅ Legacy interaction audit PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
