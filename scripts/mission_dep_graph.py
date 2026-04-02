#!/usr/bin/env python3
"""
mission_dep_graph.py — My-Anbennar
Verne mission dependency graph audit.
"""
from __future__ import annotations
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

RESERVED = {
    "OR", "AND", "NOT", "IF", "ELSE", "LIMIT",
    "FROM", "THIS", "PREV", "ROOT", "OWNER", "ANY", "ALL",
    # DLC names (frequently appear inside has_dlc checks caught by mission-ID regex)
    "Leviathan", "Rights_of_Man", "Mandate_of_Heaven", "Mandate",
    "Commonwealth", "Third_Nation", "Embers_of_Eastern_Flames",
    "Embers", "Cradle_of_Civilization", "Cradle", "Art_of_War",
    "Art", "Rule_Britannia", "Rule", "Bronze_Age", "Wealth_of_Nations",
    "Wealth", "Northern_Throne", "Golden_Century", "Golden",
    "Origins", "Origins", "Plymouth", "Leviathan",
}

MISSIONS = Path(r"C:\Users\User\Documents\GitHub\My-Anbennar\missions\Verne_Missions.txt")


def _read(path: Path) -> str:
    return path.read_bytes().decode("utf-8-sig").replace("\r", "")


def find_missions_with_slot(lines: list[str]) -> dict[str, int]:
    """Return {mission_id: slot_number} for every real mission.

    NOTE: Slots 6-10 all incorrectly say slot=5 in the file.
    We infer the real slot from the block name.
    """
    ids = {}
    current_slot = None
    current_slot_name = None
    i = 0
    while i < len(lines):
        raw = lines[i]
        line = raw.strip()
        if not line or line.startswith("#"):
            i += 1
            continue
        # Top-level slot block declaration (no indent)
        slot_block_m = re.match(r"^(A33_\w+)\s*=\s*\{", line)
        if slot_block_m:
            top_indent = len(raw) - len(raw.lstrip("\t "))
            if top_indent == 0:
                current_slot = None
                current_slot_name = slot_block_m.group(1)
                name_lower = current_slot_name.lower()
                SLOT_NAME_MAP = {
                    "first": 1, "second": 2, "third": 3, "fourth": 4,
                    "fifth": 5, "sixth": 6, "seventh": 7, "eighth": 8,
                    "ninth": 9, "tenth": 10,
                }
                for kw, num in SLOT_NAME_MAP.items():
                    if kw in name_lower:
                        current_slot = num
                        break
                # Fallback: look for slot = N in the block
                if current_slot is None:
                    for j in range(i + 1, min(i + 10, len(lines))):
                        inner = lines[j].strip()
                        slot_n_m = re.match(r"^slot\s*=\s*(\d+)", inner)
                        if slot_n_m:
                            current_slot = int(slot_n_m.group(1))
                            break
        # Tab-indented mission id inside a slot block
        top_indent = len(raw) - len(raw.lstrip("\t "))
        if top_indent == 1 and line and not line.startswith("#"):
            m = re.match(r"^([A-Z][A-Za-z0-9_]+)\s*=\s*\{", line)
            if m and m.group(1) not in RESERVED:
                mission_id = m.group(1)
                if current_slot is not None:
                    ids[mission_id] = current_slot
                else:
                    print(f"  WARNING: {mission_id} found outside any slot block")
        i += 1
    return ids


def extract_edges(text: str) -> list[tuple[str, str]]:
    """Extract (mission_id, required_mission_id) edges using state machine."""
    edges = []
    lines = text.split("\n")
    i = 0
    current_mission = None

    while i < len(lines):
        raw = lines[i]
        line = raw.strip()

        # Skip blanks and comments
        if not line or line.startswith("#"):
            i += 1
            continue

        # Detect current mission id (tab-indented inside slot)
        top_indent = len(raw) - len(raw.lstrip("\t "))
        if top_indent == 1:
            m = re.match(r"^([A-Z][A-Za-z0-9_]+)\s*=\s*\{", line)
            if m and m.group(1) not in RESERVED:
                current_mission = m.group(1)

        # Detect required_missions block start
        if "required_missions" in line and current_mission:
            # Collect all mission IDs from this block
            # State: inside required_missions block until brace depth goes negative
            brace_depth = 0
            in_block = False
            j = i
            while j < len(lines):
                block_line = lines[j].strip()
                if "required_missions" in block_line:
                    in_block = True
                    brace_depth += block_line.count("{")
                    brace_depth -= block_line.count("}")
                    # Extract IDs from same line (e.g. "required_missions = { A33_x }")
                    for mid in re.findall(r'\b([A-Z][A-Za-z0-9_]+)\b', block_line):
                        if mid not in RESERVED and mid != current_mission:
                            edges.append((current_mission, mid))
                elif in_block:
                    brace_depth += block_line.count("{")
                    brace_depth -= block_line.count("}")
                    if brace_depth <= 0:
                        break
                    for mid in re.findall(r'\b([A-Z][A-Za-z0-9_]+)\b', block_line):
                        if mid not in RESERVED and mid != current_mission:
                            edges.append((current_mission, mid))
                j += 1
            i = j
            continue
        i += 1
    return edges


def build_graph(mission_ids: set[str], edges: list[tuple[str, str]]):
    out_edges = defaultdict(list)
    in_edges = defaultdict(list)
    orphans = []
    for src, dst in edges:
        if dst not in mission_ids:
            orphans.append((src, dst))
        else:
            out_edges[src].append(dst)
            in_edges[dst].append(src)
    return out_edges, in_edges, orphans


def find_cycles(out_edges, mission_ids):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {m: WHITE for m in mission_ids}
    cycles = []

    def dfs(node, path):
        color[node] = GRAY
        path.append(node)
        for neigh in out_edges.get(node, []):
            if color[neigh] == GRAY:
                cycle_start = path.index(neigh)
                cycles.append(path[cycle_start:] + [neigh])
            elif color[neigh] == WHITE:
                dfs(neigh, path)
        path.pop()
        color[node] = BLACK

    for m in mission_ids:
        if color[m] == WHITE:
            dfs(m, [])
    return cycles


def main():
    text = _read(MISSIONS)
    lines = text.split("\n")
    mission_slot = find_missions_with_slot(lines)
    mission_ids = set(mission_slot.keys())
    edges = extract_edges(text)

    print(f"Missions found: {len(mission_ids)}")
    print(f"required_missions edges: {len(edges)}")

    out_edges, in_edges, orphans = build_graph(mission_ids, edges)

    if orphans:
        print(f"\n[HIGH] ORPHAN edges (target doesn't exist): {len(orphans)}")
        for src, dst in orphans:
            print(f"  {src} -> {dst}  [ORPHAN]")
    else:
        print("\n[OK] No orphan edges")

    cycles = find_cycles(out_edges, mission_ids)
    if cycles:
        print(f"\n[HIGH] CYCLE DETECTED — {len(cycles)} cycles:")
        for cyc in cycles:
            print(f"  {' -> '.join(cyc)}")
    else:
        print("[OK] No cycles (DAG valid)")

    roots = [m for m in mission_ids if not out_edges.get(m)]
    terminals = [m for m in mission_ids if not in_edges.get(m)]
    print(f"\nRoot missions (no prerequisites): {len(roots)}")
    for m in sorted(roots):
        print(f"  [{mission_slot[m]}] {m}")

    print(f"\nTerminal missions (nothing depends on them): {len(terminals)}")
    for m in sorted(terminals):
        print(f"  [{mission_slot[m]}] {m}")

    # Cross-slot dependencies
    cross_slot = []
    for src, reqs in out_edges.items():
        src_slot = mission_slot.get(src, 0)
        for req in reqs:
            req_slot = mission_slot.get(req, 0)
            if req_slot and req_slot != src_slot:
                cross_slot.append((src, src_slot, req, req_slot))
    if cross_slot:
        print(f"\n[MEDIUM] Cross-slot dependencies: {len(cross_slot)}")
        for src, s_slot, req, r_slot in sorted(cross_slot):
            print(f"  [{s_slot}] {src} -> [{r_slot}] {req}")
    else:
        print("\n[OK] No cross-slot dependencies")

    # Save full graph
    report = {
        "mission_count": len(mission_ids),
        "edge_count": len(edges),
        "orphans": orphans,
        "cycles": cycles,
        "roots": sorted(roots),
        "terminals": sorted(terminals),
        "cross_slot": cross_slot,
        "mission_slot": {m: mission_slot[m] for m in sorted(mission_slot)},
        "out_edges": {m: out_edges[m] for m in sorted(out_edges)},
    }
    out = Path("C:/Users/User/.openclaw/workspace/automation/reports/mission_dep_graph.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2))
    print(f"\nFull graph saved to {out}")


if __name__ == "__main__":
    main()
