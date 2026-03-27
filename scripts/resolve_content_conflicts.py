#!/usr/bin/env python3
"""Conservative assisted merge resolution for Anbennar content hotspots."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import argparse
import re
import subprocess
import sys
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
TARGET_PREFIXES = ("missions/", "events/", "localisation/")
KEY_PATTERN = re.compile(r"^\s*([A-Za-z0-9_.-]+):")


@dataclass
class ConflictBlock:
    start_line: int
    ours: list[str]
    theirs: list[str]


@dataclass
class ResolveResult:
    resolved_path: str | None
    unresolved_hints: list[str]


@dataclass
class ParsedConflicts:
    conflicts: list[ConflictBlock]


def run_git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def unmerged_files() -> list[str]:
    result = run_git("diff", "--name-only", "--diff-filter=U")
    if result.returncode != 0:
        return []
    files = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    return [path for path in files if path.startswith(TARGET_PREFIXES)]


def parse_conflicts(path: Path) -> ParsedConflicts:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    conflicts: list[ConflictBlock] = []

    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.startswith("<<<<<<<"):
            i += 1
            continue

        start_line = i + 1
        i += 1
        ours: list[str] = []
        while i < len(lines) and not lines[i].startswith("======="):
            ours.append(lines[i])
            i += 1

        if i >= len(lines):
            break

        i += 1  # skip =======
        theirs: list[str] = []
        while i < len(lines) and not lines[i].startswith(">>>>>>>"):
            theirs.append(lines[i])
            i += 1

        if i < len(lines):
            i += 1  # skip >>>>>>>

        conflicts.append(ConflictBlock(start_line=start_line, ours=ours, theirs=theirs))

    return ParsedConflicts(conflicts=conflicts)


def extract_localisation_keys(lines: list[str]) -> set[str]:
    keys: set[str] = set()
    for line in lines:
        match = KEY_PATTERN.match(line)
        if match:
            keys.add(match.group(1))
    return keys


def merge_localisation_block(block: ConflictBlock) -> list[str] | None:
    ours_keys = extract_localisation_keys(block.ours)
    theirs_keys = extract_localisation_keys(block.theirs)

    if ours_keys & theirs_keys:
        return None

    merged: list[str] = []
    merged.extend(block.ours)

    if merged and not merged[-1].endswith("\n"):
        merged[-1] = merged[-1] + "\n"

    if block.ours and block.theirs:
        if merged and merged[-1].strip():
            merged.append("\n")

    merged.extend(block.theirs)
    return merged


def write_resolved(path: Path, parsed: ParsedConflicts, blocks: list[list[str]]) -> None:
    source_lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    output: list[str] = []

    source_idx = 0
    block_idx = 0
    while source_idx < len(source_lines):
        if source_lines[source_idx].startswith("<<<<<<<"):
            # Skip original block in source.
            source_idx += 1
            while source_idx < len(source_lines) and not source_lines[source_idx].startswith("======="):
                source_idx += 1
            source_idx += 1
            while source_idx < len(source_lines) and not source_lines[source_idx].startswith(">>>>>>>"):
                source_idx += 1
            source_idx += 1

            output.extend(blocks[block_idx])
            block_idx += 1
            continue

        output.append(source_lines[source_idx])
        source_idx += 1

    path.write_text("".join(output), encoding="utf-8", newline="")


def classify(path: str) -> str:
    if path.startswith("missions/"):
        return "missions"
    if path.startswith("events/"):
        return "events"
    if path.startswith("localisation/"):
        return "localisation"
    return "other"


def resolve_path(path: str, args: argparse.Namespace) -> ResolveResult:
    target = ROOT / path
    parsed = parse_conflicts(target)
    if not parsed.conflicts:
        return ResolveResult(resolved_path=None, unresolved_hints=[])

    resolved_blocks: list[list[str]] = []
    unresolved_hints: list[str] = []

    for block in parsed.conflicts:
        if args.prefer_main:
            resolved_blocks.append(block.theirs)
            continue
        if args.prefer_branch:
            resolved_blocks.append(block.ours)
            continue

        path_type = classify(path)
        if path_type == "localisation":
            merged = merge_localisation_block(block)
            if merged is not None:
                resolved_blocks.append(merged)
                continue

        unresolved_hints.append(f"{path}:{block.start_line}")
        resolved_blocks.append([
            "<<<<<<< HEAD\n",
            *block.ours,
            "=======\n",
            *block.theirs,
            ">>>>>>> MERGE_HEAD\n",
        ])

    if unresolved_hints:
        return ResolveResult(resolved_path=None, unresolved_hints=unresolved_hints)

    write_resolved(target, parsed, resolved_blocks)
    if run_git("add", path).returncode != 0:
        return ResolveResult(resolved_path=None, unresolved_hints=[f"{path}:git-add-failed"])
    return ResolveResult(resolved_path=path, unresolved_hints=[])


def print_unresolved_summary(unresolved_by_type: dict[str, list[str]]) -> None:
    print("Unresolved conflict summary (manual review required):")
    for file_type in ("missions", "events", "localisation", "other"):
        entries = unresolved_by_type.get(file_type, [])
        if not entries:
            continue
        print(f"- {file_type} ({len(entries)}):")
        for hint in entries:
            print(f"  - {hint}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Assist with conflict resolution for missions/, events/, and localisation/ files "
            "using conservative policies."
        )
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--prefer-main",
        action="store_true",
        help="Resolve each target conflict block by taking upstream/main (theirs).",
    )
    mode.add_argument(
        "--prefer-branch",
        action="store_true",
        help="Resolve each target conflict block by taking current branch (ours).",
    )
    parser.add_argument(
        "--union-docs-only",
        action="store_true",
        help=(
            "Safety guard for future union strategies: never union gameplay scripts. "
            "Default conservative mode already avoids gameplay unions."
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    unresolved = unmerged_files()
    if not unresolved:
        print("No unresolved content conflicts found in missions/, events/, or localisation/.")
        return 0

    resolved: list[str] = []
    unresolved_by_type: dict[str, list[str]] = defaultdict(list)

    for path in unresolved:
        result = resolve_path(path, args)
        if result.resolved_path:
            resolved.append(result.resolved_path)
        for hint in result.unresolved_hints:
            unresolved_by_type[classify(path)].append(hint)

    if resolved:
        print("Auto-resolved content files:")
        for path in resolved:
            print(f" - {path}")

    remaining = run_git("diff", "--name-only", "--diff-filter=U")
    if remaining.returncode == 0 and remaining.stdout.strip():
        # Ensure grouped unresolved hints are visible even if another unresolved file type exists.
        if unresolved_by_type:
            print_unresolved_summary(unresolved_by_type)
        else:
            print("Unresolved conflicts remain outside assisted content paths.")
        return 1

    if unresolved_by_type:
        print_unresolved_summary(unresolved_by_type)
        return 1

    print("All targeted content conflicts resolved.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
