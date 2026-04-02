#!/usr/bin/env python3
"""
anbennar_hotspot_explainer.py — My-Anbennar
Given a list of changed file paths, report which (if any) intersect
conflict-hotspot single-writer or advisory scopes.

Usage:
  python scripts/anbennar_hotspot_explainer.py --files file1.txt file2.txt
  python scripts/anbennar_hotspot_explainer.py  (reads from git diff --name-only)
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

def load_hotspots(path: str = "automation/conflict_hotspots.yaml") -> dict:
    # Minimal YAML-like parser for conflict_hotspots.yaml
    # The file uses: file: <path>, type: single-writer|advisory
    hotspots = {"single_writer": [], "advisory": []}
    p = Path(path)
    if not p.exists():
        return hotspots
    content = p.read_text(encoding="utf-8", errors="replace")
    current_entry = {}
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("-"):
            if current_entry.get("file") and current_entry.get("type"):
                if current_entry["type"] == "single-writer":
                    hotspots["single_writer"].append(current_entry["file"])
                else:
                    hotspots["advisory"].append(current_entry["file"])
            current_entry = {}
            line = line.lstrip("- ").strip()
        if ":" in line:
            k, v = line.split(":", 1)
            current_entry[k.strip()] = v.strip()
    if current_entry.get("file") and current_entry.get("type"):
        if current_entry["type"] == "single-writer":
            hotspots["single_writer"].append(current_entry["file"])
        else:
            hotspots["advisory"].append(current_entry["file"])
    return hotspots


def explain_changed(files: list[str], hotspots: dict) -> str:
    sw_hits   = [f for f in files if any(f == h or f.endswith("/" + h) or h in f for h in hotspots["single_writer"])]
    adv_hits  = [f for f in files if any(f == h or f.endswith("/" + h) or h in f for h in hotspots["advisory"])]

    lines = []
    if not files:
        lines.append("No changed files.")
    else:
        lines.append(f"Changed files ({len(files)}):")
        for f in files:
            lines.append(f"  {f}")
    if sw_hits:
        lines.append(f"\n🚨 SINGLE-WRITER HOTSPOT HIT ({len(sw_hits)}):")
        for f in sw_hits:
            lines.append(f"  🚨 {f}  ← SERIALIZE, do not parallelize")
        lines.append("\n  → Run: anbennar.validate_all before proceeding")
    if adv_hits:
        lines.append(f"\n⚠️  ADVISORY HOTSPOT HIT ({len(adv_hits)}):")
        for f in adv_hits:
            lines.append(f"  ⚠️  {f}")
    if not sw_hits and not adv_hits:
        lines.append("\n✅ No hotspot intersections — clear to proceed.")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Anbennar hotspot explainer")
    parser.add_argument("--files", nargs="*", help="Changed file paths")
    args = parser.parse_args()

    if not args.files:
        import subprocess
        try:
            out = subprocess.check_output(["git", "diff", "--name-only"], text=True).strip()
            files = [x for x in out.splitlines() if x]
        except subprocess.CalledProcessError:
            files = []
    else:
        files = args.files

    hotspots = load_hotspots()
    report = explain_changed(files, hotspots)
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
