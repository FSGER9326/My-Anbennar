#!/usr/bin/env python3
"""Plan low-conflict PR merge/rebase order and hotspot overlap risk."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

FALLBACK_USAGE = (
    "python scripts/pr_conflict_churn_plan.py --base main --branches branch-a branch-b"
)
DEFAULT_REGISTRY = "automation/conflict_hotspots.yaml"


@dataclass
class HotspotRegistry:
    single_writer_files: set[str]
    single_writer_prefixes: tuple[str, ...]
    advisory_hotspots: set[str]
    advisory_prefixes: tuple[str, ...]

    def classify_file(self, path: str) -> str:
        if path in self.single_writer_files or path.startswith(self.single_writer_prefixes):
            return "block"
        if path in self.advisory_hotspots or path.startswith(self.advisory_prefixes):
            return "warn"
        return "none"


@dataclass
class Candidate:
    name: str
    title: str
    base: str
    files: set[str] = field(default_factory=set)


@dataclass
class Overlap:
    left: str
    right: str
    block_files: list[str]
    warn_files: list[str]
    neutral_files: list[str]

    def severity(self) -> str:
        if self.block_files:
            return "block"
        if self.warn_files:
            return "warn"
        return "none"


def run_git(args: list[str]) -> str:
    result = subprocess.run(["git", *args], text=True, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout.strip()


def run_gh_open_prs(base: str | None) -> list[dict]:
    cmd = [
        "gh",
        "pr",
        "list",
        "--state",
        "open",
        "--json",
        "number,title,headRefName,baseRefName",
        "--limit",
        "200",
    ]
    if base:
        cmd += ["--base", base]

    try:
        result = subprocess.run(cmd, text=True, capture_output=True)
    except FileNotFoundError as exc:
        raise RuntimeError(
            "GitHub CLI (`gh`) is not installed. "
            "Install/authenticate gh or pass --branches explicitly."
        ) from exc
    if result.returncode != 0:
        raise RuntimeError(
            "Could not load open PRs from GitHub CLI. "
            "Either install/authenticate gh or pass --branches explicitly. "
            f"Details: {result.stderr.strip()}"
        )
    return json.loads(result.stdout)


def changed_files(base: str, branch: str) -> set[str]:
    merge_base = run_git(["merge-base", base, branch])
    out = run_git(["diff", "--name-only", f"{merge_base}..{branch}"])
    return {line.strip() for line in out.splitlines() if line.strip()}


def classify_topic(candidate: Candidate) -> str:
    lowered = (candidate.title + " " + candidate.name).lower()
    files = candidate.files

    if any("crosswalk" in f for f in files) or "crosswalk" in lowered or "dedupe" in lowered:
        return "crosswalk dedupe"
    if any(f.startswith("scripts/") for f in files) and "wrapper" in lowered:
        return "wrapper scripts"
    if "smoke" in lowered or "profile" in lowered or any("smoke" in f for f in files):
        return "smoke/profile changes"
    if any(f.startswith("docs/") for f in files):
        return "docs/base automation"
    return "other"


def score(candidate: Candidate) -> tuple[int, int, str]:
    topic = classify_topic(candidate)
    topic_rank = {
        "docs/base automation": 0,
        "crosswalk dedupe": 1,
        "wrapper scripts": 2,
        "smoke/profile changes": 3,
        "other": 4,
    }.get(topic, 4)
    return (topic_rank, len(candidate.files), candidate.name)


def compute_overlaps(candidates: list[Candidate], registry: HotspotRegistry) -> list[Overlap]:
    overlaps: list[Overlap] = []
    for i, left in enumerate(candidates):
        for right in candidates[i + 1 :]:
            inter = sorted(left.files & right.files)
            if not inter:
                continue
            block_files = [f for f in inter if registry.classify_file(f) == "block"]
            warn_files = [f for f in inter if registry.classify_file(f) == "warn"]
            neutral_files = [f for f in inter if registry.classify_file(f) == "none"]
            overlaps.append(
                Overlap(
                    left=left.name,
                    right=right.name,
                    block_files=block_files,
                    warn_files=warn_files,
                    neutral_files=neutral_files,
                )
            )
    overlaps.sort(
        key=lambda o: (
            0 if o.severity() == "block" else 1 if o.severity() == "warn" else 2,
            -(len(o.block_files) + len(o.warn_files) + len(o.neutral_files)),
            o.left,
            o.right,
        )
    )
    return overlaps


def build_candidates(base: str, explicit_branches: list[str] | None) -> list[Candidate]:
    if explicit_branches:
        rows = [
            {
                "headRefName": b,
                "title": f"Local branch {b}",
                "baseRefName": base,
            }
            for b in explicit_branches
        ]
    else:
        try:
            rows = run_gh_open_prs(base)
        except FileNotFoundError as exc:
            raise RuntimeError(
                "GitHub CLI (`gh`) is not installed or not on your PATH.\n"
                "Fallback: run with explicit branches instead, for example:\n"
                f"  {FALLBACK_USAGE}"
            ) from exc
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "GitHub CLI returned unreadable PR data. "
                "Run `gh auth status` (or `gh auth login`) and try again.\n"
                "Fallback: run with explicit branches instead, for example:\n"
                f"  {FALLBACK_USAGE}"
            ) from exc
        except RuntimeError as exc:
            raise RuntimeError(
                f"{exc}\n"
                "Try fallback usage with explicit branches:\n"
                f"  {FALLBACK_USAGE}"
            ) from exc

    candidates: list[Candidate] = []
    for row in rows:
        branch = row["headRefName"]
        if branch == base:
            continue
        try:
            files = changed_files(base, branch)
        except RuntimeError as exc:
            raise RuntimeError(
                f"Could not compare `{branch}` against `{base}`.\n"
                "Make sure both branches exist locally, then retry.\n"
                "Helpful commands:\n"
                f"  git fetch origin {base}:{base}\n"
                f"  git fetch origin {branch}:{branch}\n"
                f"  {FALLBACK_USAGE}"
            ) from exc
        candidates.append(
            Candidate(
                name=branch,
                title=row.get("title") or branch,
                base=row.get("baseRefName") or base,
                files=files,
            )
        )

    return candidates


def parse_simple_yaml_lists(path: Path) -> dict[str, list[str]]:
    """Minimal YAML parser for top-level `key:`, `- value` list style used in hotspots."""
    raw = path.read_text(encoding="utf-8").splitlines()
    result: dict[str, list[str]] = {}
    current_key: str | None = None
    for idx, line in enumerate(raw, start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if not line.startswith(" ") and stripped.endswith(":"):
            current_key = stripped[:-1]
            result.setdefault(current_key, [])
            continue
        if stripped.startswith("-"):
            if current_key is None:
                raise RuntimeError(f"Invalid YAML at line {idx}: list item without key")
            value = stripped[1:].strip()
            if value.startswith(("'", '"')) and value.endswith(("'", '"')) and len(value) >= 2:
                value = value[1:-1]
            result[current_key].append(value)
            continue
        raise RuntimeError(f"Unsupported YAML structure at line {idx}: {line}")
    return result


def load_registry(path: str) -> HotspotRegistry:
    yaml_path = Path(path)
    if not yaml_path.exists():
        raise RuntimeError(f"Hotspot registry not found: {path}")
    parsed = parse_simple_yaml_lists(yaml_path)

    single_writer_files = set(parsed.get("single_writer_files", []))
    single_writer_prefixes = tuple(parsed.get("single_writer_prefixes", []))

    advisory_entries = parsed.get("advisory_hotspots", [])
    advisory_hotspots = {v for v in advisory_entries if not v.endswith("/")}
    advisory_prefixes = tuple(v for v in advisory_entries if v.endswith("/"))

    return HotspotRegistry(
        single_writer_files=single_writer_files,
        single_writer_prefixes=single_writer_prefixes,
        advisory_hotspots=advisory_hotspots,
        advisory_prefixes=advisory_prefixes,
    )


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default="main", help="Base branch to diff against (default: main)")
    parser.add_argument(
        "--branches",
        nargs="*",
        help="Optional explicit branch names; skips gh pr list when provided.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON plus markdown report.",
    )
    parser.add_argument(
        "--fail-on-block",
        action="store_true",
        help="Exit non-zero when block overlaps are found.",
    )
    parser.add_argument(
        "--focus-branch",
        help="Limit fail-on-block/warn summaries to overlaps involving this branch.",
    )
    parser.add_argument(
        "--hotspot-registry",
        default=DEFAULT_REGISTRY,
        help=f"Hotspot registry YAML path (default: {DEFAULT_REGISTRY})",
    )
    parser.add_argument("--json-output", help="Write JSON summary to file.")
    parser.add_argument("--markdown-output", help="Write markdown summary to file.")
    return parser.parse_args(list(argv))


def build_payload(
    args: argparse.Namespace,
    ordered: list[Candidate],
    overlaps: list[Overlap],
    registry: HotspotRegistry,
) -> dict:
    relevant = [
        o
        for o in overlaps
        if not args.focus_branch or args.focus_branch in (o.left, o.right)
    ]
    block_overlaps = [o for o in relevant if o.block_files]
    warn_overlaps = [o for o in relevant if not o.block_files and o.warn_files]

    payload = {
        "base": args.base,
        "focus_branch": args.focus_branch,
        "registry": {
            "path": args.hotspot_registry,
            "single_writer_files": sorted(registry.single_writer_files),
            "single_writer_prefixes": sorted(registry.single_writer_prefixes),
            "advisory_hotspots": sorted(registry.advisory_hotspots),
            "advisory_prefixes": sorted(registry.advisory_prefixes),
        },
        "summary": {
            "branches_analyzed": len(ordered),
            "overlap_pairs": len(overlaps),
            "relevant_overlap_pairs": len(relevant),
            "block_pairs": len(block_overlaps),
            "warn_pairs": len(warn_overlaps),
            "has_blockers": len(block_overlaps) > 0,
        },
        "order": [
            {
                "branch": c.name,
                "title": c.title,
                "topic": classify_topic(c),
                "file_count": len(c.files),
                "files_changed": sorted(c.files),
            }
            for c in ordered
        ],
        "overlaps": [
            {
                "left": o.left,
                "right": o.right,
                "severity": o.severity(),
                "block_files": o.block_files,
                "warn_files": o.warn_files,
                "neutral_files": o.neutral_files,
            }
            for o in overlaps
        ],
        "relevant_overlaps": [
            {
                "left": o.left,
                "right": o.right,
                "severity": o.severity(),
                "block_files": o.block_files,
                "warn_files": o.warn_files,
                "neutral_files": o.neutral_files,
            }
            for o in relevant
        ],
    }
    return payload


def build_markdown(payload: dict) -> str:
    lines: list[str] = [f"# PR Conflict-Churn Plan (base: `{payload['base']}`)", ""]
    if payload.get("focus_branch"):
        lines.append(f"Focus branch: `{payload['focus_branch']}`")
        lines.append("")

    summary = payload["summary"]
    lines += [
        "## Overlap summary",
        f"- Branches analyzed: **{summary['branches_analyzed']}**",
        f"- Overlap pairs: **{summary['overlap_pairs']}**",
        f"- Relevant overlap pairs: **{summary['relevant_overlap_pairs']}**",
        f"- Block overlaps: **{summary['block_pairs']}**",
        f"- Advisory overlaps: **{summary['warn_pairs']}**",
        "",
        "## Merge/rebase order",
    ]

    for idx, entry in enumerate(payload["order"], start=1):
        lines.append(
            f"{idx}. `{entry['branch']}` — {entry['title']} "
            f"(topic: **{entry['topic']}**, files: {entry['file_count']})"
        )

    lines += ["", "## Overlaps"]
    relevant = payload["relevant_overlaps"]
    if not relevant:
        lines.append("No relevant overlaps detected.")
        return "\n".join(lines) + "\n"

    for overlap in relevant:
        left = overlap["left"]
        right = overlap["right"]
        severity = overlap["severity"].upper()
        lines.append(f"- `{left}` ↔ `{right}` — **{severity}**")
        if overlap["block_files"]:
            lines.append("  - block:")
            for name in overlap["block_files"]:
                lines.append(f"    - `{name}`")
        if overlap["warn_files"]:
            lines.append("  - warn:")
            for name in overlap["warn_files"]:
                lines.append(f"    - `{name}`")
        if overlap["neutral_files"]:
            lines.append("  - neutral:")
            for name in overlap["neutral_files"]:
                lines.append(f"    - `{name}`")

    return "\n".join(lines) + "\n"


def main(argv: Iterable[str]) -> int:
    args = parse_args(argv)

    try:
        registry = load_registry(args.hotspot_registry)
        candidates = build_candidates(args.base, args.branches)
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if not candidates:
        print("No PR branches found to analyze.")
        return 0

    ordered = sorted(candidates, key=score)
    overlaps = compute_overlaps(ordered, registry)
    payload = build_payload(args, ordered, overlaps, registry)

    markdown = build_markdown(payload)
    json_blob = json.dumps(payload, indent=2)

    if args.json_output:
        Path(args.json_output).write_text(json_blob + "\n", encoding="utf-8")
    if args.markdown_output:
        Path(args.markdown_output).write_text(markdown, encoding="utf-8")

    if args.json:
        print(json_blob)
        print()

    print(markdown, end="")

    if args.fail_on_block and payload["summary"]["has_blockers"]:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
