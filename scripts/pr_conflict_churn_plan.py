#!/usr/bin/env python3
"""Plan low-conflict PR merge/rebase order.

The script inspects open PR branches (via `gh pr list`) or a user-specified branch list,
compares changed files, and highlights overlap hotspots so you can merge foundational
work first and keep downstream PRs narrow.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass, field
from typing import Iterable

HOTSPOTS = {
    "docs/implementation-crosswalk.md",
    "docs/start-here.md",
}
HOTSPOT_PREFIXES = ("scripts/",)
FALLBACK_USAGE = (
    "python scripts/pr_conflict_churn_plan.py --base main --branches branch-a branch-b"
)


@dataclass
class Candidate:
    name: str
    title: str
    base: str
    files: set[str] = field(default_factory=set)

    def touches_hotspot(self) -> bool:
        return any(
            f in HOTSPOTS or f.startswith(HOTSPOT_PREFIXES) for f in self.files
        )


@dataclass
class Overlap:
    left: str
    right: str
    files: list[str]


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
            "GitHub CLI (`gh`) is not installed or not on your PATH.\n"
            "Fallback: run with explicit branches instead, for example:\n"
            f"  {FALLBACK_USAGE}"
        ) from exc

    if result.returncode != 0:
        raise RuntimeError(
            "Could not load open PRs from GitHub CLI. "
            "Either install/authenticate gh or pass --branches explicitly. "
            "Try:\n"
            f"  {FALLBACK_USAGE}\n"
            f"Details: {result.stderr.strip()}"
        )
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            "GitHub CLI returned unreadable PR data. "
            "Run `gh auth status` (or `gh auth login`) and try again.\n"
            "Fallback: run with explicit branches instead, for example:\n"
            f"  {FALLBACK_USAGE}"
        ) from exc


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
    if any(f in HOTSPOTS for f in files):
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


def compute_overlaps(candidates: list[Candidate]) -> list[Overlap]:
    overlaps: list[Overlap] = []
    for i, left in enumerate(candidates):
        for right in candidates[i + 1 :]:
            inter = sorted(left.files & right.files)
            if inter:
                overlaps.append(Overlap(left.name, right.name, inter))
    overlaps.sort(key=lambda o: (-len(o.files), o.left, o.right))
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
        rows = run_gh_open_prs(base)

    candidates: list[Candidate] = []
    for row in rows:
        branch = row["headRefName"]
        if branch == base:
            continue
        files = changed_files(base, branch)
        candidates.append(
            Candidate(
                name=branch,
                title=row.get("title") or branch,
                base=row.get("baseRefName") or base,
                files=files,
            )
        )

    return candidates


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
        help="Emit machine-readable JSON instead of markdown report.",
    )
    return parser.parse_args(list(argv))


def main(argv: Iterable[str]) -> int:
    args = parse_args(argv)

    try:
        candidates = build_candidates(args.base, args.branches)
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if not candidates:
        print("No PR branches found to analyze.")
        return 0

    ordered = sorted(candidates, key=score)
    overlaps = compute_overlaps(ordered)

    if args.json:
        payload = {
            "base": args.base,
            "order": [
                {
                    "branch": c.name,
                    "title": c.title,
                    "topic": classify_topic(c),
                    "file_count": len(c.files),
                    "touches_hotspot": c.touches_hotspot(),
                }
                for c in ordered
            ],
            "overlaps": [
                {"left": o.left, "right": o.right, "files": o.files}
                for o in overlaps
            ],
        }
        print(json.dumps(payload, indent=2))
        return 0

    print(f"# PR Conflict-Churn Plan (base: `{args.base}`)\n")
    print("## Suggested merge/rebase order")
    for idx, c in enumerate(ordered, start=1):
        topic = classify_topic(c)
        hotspot = "hotspot" if c.touches_hotspot() else "no-hotspot"
        print(
            f"{idx}. `{c.name}` — {c.title}  "
            f"(topic: **{topic}**, files: {len(c.files)}, {hotspot})"
        )

    print("\n## Overlapping files between PR branches")
    if not overlaps:
        print("No overlaps detected.")
    else:
        for overlap in overlaps:
            print(f"- `{overlap.left}` ↔ `{overlap.right}` ({len(overlap.files)} files)")
            for name in overlap.files:
                marker = " ⚠️ hotspot" if name in HOTSPOTS or name.startswith(HOTSPOT_PREFIXES) else ""
                print(f"  - `{name}`{marker}")

    print("\n## Downstream cleanup checklist")
    print("1. Merge the first (most foundational) PR into `main`.")
    print("2. For each remaining branch, rebase onto updated `main`.")
    print("3. Drop merged commits (`git rebase -i main`) or recreate via cherry-pick.")
    print("4. Keep PRs single-topic (smoke/profile, crosswalk dedupe, wrapper scripts).")
    print("5. Avoid parallel edits to `docs/implementation-crosswalk.md`, `docs/start-here.md`, and `scripts/*`.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
