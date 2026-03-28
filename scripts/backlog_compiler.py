#!/usr/bin/env python3
"""Compile Verne backlog/roadmap signals into a prioritized work queue."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]

DOC_SOURCES = [
    Path("docs/implementation-roadmap.md"),
    Path("docs/first-wave-backlog.md"),
    Path("docs/repo-maps/anbennar-systems-scan-roadmap.md"),
    Path("docs/design/verne_overhaul_restructured_master_plan.md"),
]

RELEVANT_SCAN_DIRS = [
    Path("common"),
    Path("events"),
    Path("missions"),
    Path("decisions"),
    Path("automation"),
    Path("scripts"),
    Path("localisation"),
]

TODO_PATTERNS = (
    "TODO",
    "TBD",
    "FIXME",
    "placeholder",
    "_TBD_",
)

SENTINEL_FILES = [
    Path("automation/country_profiles/verne.json"),
    Path("scripts/verne_smoke_checks.sh"),
    Path("scripts/verne_smoke_checks.ps1"),
]

LEDGER = Path("docs/wiki/verne-id-ledger.md")
ID_PATTERN = re.compile(r"\bverne_[a-z0-9_]+\b")
LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


@dataclass
class Task:
    title: str
    detail: str
    kind: str
    files: set[Path]
    impact: str
    effort: str

    @property
    def score(self) -> int:
        impact_score = {
            "breaks CI": 100,
            "blocks milestones": 70,
            "high gameplay leverage": 50,
        }[self.impact]

        effort_adjust = {
            "small": 15,
            "medium": 5,
            "large": -10,
        }[self.effort]

        fanout = min(len(self.files), 6)
        return impact_score + effort_adjust - fanout

    @property
    def bucket(self) -> str:
        if self.score >= 85:
            return "Now"
        if self.score >= 55:
            return "Next"
        return "Later"


def read_text(path: Path) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def safe_read(path: Path) -> str:
    abs_path = ROOT / path
    if not abs_path.exists():
        return ""
    return abs_path.read_text(encoding="utf-8", errors="ignore")


def infer_target_files(doc_paths: Iterable[Path]) -> set[Path]:
    targets: set[Path] = set()
    for doc in doc_paths:
        abs_doc = ROOT / doc
        if not abs_doc.exists():
            continue
        text = read_text(doc)
        for match in LINK_PATTERN.finditer(text):
            raw = match.group(1).strip()
            if raw.startswith(("http://", "https://", "#")):
                continue
            cleaned = raw.split("#", 1)[0]
            if not cleaned or cleaned.startswith("mailto:"):
                continue
            resolved = (doc.parent / cleaned).resolve()
            try:
                rel = resolved.relative_to(ROOT)
            except ValueError:
                continue
            if rel.suffix in {".md", ".png", ".jpg", ".dds", ".svg"}:
                continue
            targets.add(rel)
    return targets


def find_todo_hits() -> dict[Path, list[str]]:
    hits: dict[Path, list[str]] = {}
    for base in RELEVANT_SCAN_DIRS:
        base_abs = ROOT / base
        if not base_abs.exists():
            continue
        for file in base_abs.rglob("*"):
            if not file.is_file() or file.suffix.lower() in {".dds", ".png", ".jpg", ".ogg", ".wav", ".tga"}:
                continue
            rel = file.relative_to(ROOT)
            lines: list[str] = []
            text = safe_read(rel)
            for i, line in enumerate(text.splitlines(), start=1):
                if any(p.lower() in line.lower() for p in TODO_PATTERNS):
                    lines.append(f"L{i}: {line.strip()[:120]}")
            if lines:
                hits[rel] = lines[:4]
    return hits


def parse_ledger_ids() -> set[str]:
    text = safe_read(LEDGER)
    return set(ID_PATTERN.findall(text))


def collect_repo_verne_ids() -> dict[str, set[Path]]:
    out: dict[str, set[Path]] = {}
    for base in RELEVANT_SCAN_DIRS:
        base_abs = ROOT / base
        if not base_abs.exists():
            continue
        for file in base_abs.rglob("*"):
            if not file.is_file():
                continue
            rel = file.relative_to(ROOT)
            text = safe_read(rel)
            for id_value in ID_PATTERN.findall(text):
                out.setdefault(id_value, set()).add(rel)
    return out


def effort_from_files(files: set[Path]) -> str:
    n = len(files)
    if n <= 2:
        return "small"
    if n <= 5:
        return "medium"
    return "large"


def make_tasks() -> list[Task]:
    tasks: list[Task] = []

    targets = infer_target_files(DOC_SOURCES)
    missing_targets = sorted(path for path in targets if not (ROOT / path).exists())
    if missing_targets:
        files = set(missing_targets)
        tasks.append(
            Task(
                title="Create missing roadmap/backlog target files",
                detail="Missing referenced files: " + ", ".join(str(p) for p in missing_targets[:8]),
                kind="missing-target-files",
                files=files,
                impact="blocks milestones",
                effort=effort_from_files(files),
            )
        )

    todo_hits = find_todo_hits()
    if todo_hits:
        todo_files = set(todo_hits.keys())
        tasks.append(
            Task(
                title="Resolve TODO/placeholder debt in gameplay + automation files",
                detail=f"{len(todo_files)} files have TODO-style markers.",
                kind="todo-placeholders",
                files=todo_files,
                impact="high gameplay leverage",
                effort=effort_from_files(todo_files),
            )
        )

    sentinel_text = "\n".join(safe_read(path) for path in SENTINEL_FILES)
    sentinel_missing: set[Path] = set()
    sentinel_targets = [
        p
        for p in targets
        if str(p).startswith(("common/", "events/", "missions/", "decisions/", "localisation/"))
    ]
    for path in sentinel_targets:
        if str(path) not in sentinel_text:
            sentinel_missing.add(path)
    if sentinel_missing:
        tasks.append(
            Task(
                title="Add smoke/profile sentinels for uncovered target files",
                detail=f"{len(sentinel_missing)} target files are not referenced by smoke/profile scripts.",
                kind="missing-sentinels",
                files=sentinel_missing,
                impact="breaks CI",
                effort=effort_from_files(sentinel_missing),
            )
        )

    ledger_ids = parse_ledger_ids()
    repo_ids = collect_repo_verne_ids()
    untracked = {id_value: files for id_value, files in repo_ids.items() if id_value not in ledger_ids}
    if untracked:
        files = {file for group in untracked.values() for file in group}
        sample = ", ".join(sorted(untracked.keys())[:10])
        tasks.append(
            Task(
                title="Register untracked verne_* IDs in ID ledger",
                detail=f"IDs missing from ledger (sample): {sample}",
                kind="ledger-drift",
                files=files,
                impact="blocks milestones",
                effort=effort_from_files(files),
            )
        )

    return sorted(tasks, key=lambda t: t.score, reverse=True)


def command_block(task: Task) -> str:
    validator = {
        "missing-target-files": "python scripts/backlog_compiler.py --plan --strict-missing-targets",
        "todo-placeholders": "python scripts/backlog_compiler.py --plan --strict-todo",
        "missing-sentinels": "python scripts/backlog_compiler.py --plan --strict-sentinels",
        "ledger-drift": "python scripts/backlog_compiler.py --plan --strict-ledger",
    }[task.kind]
    return (
        f"- validate: `{validator}`\n"
        f"- implement: `python scripts/backlog_compiler.py --plan --focus {task.kind}`\n"
        "- verify: `python scripts/backlog_compiler.py --plan`"
    )


def write_queue(tasks: list[Task], output_path: Path) -> None:
    buckets: dict[str, list[Task]] = {"Now": [], "Next": [], "Later": []}
    for task in tasks:
        buckets[task.bucket].append(task)

    lines = [
        "# Current Work Queue (Generated)",
        "",
        "This file is generated by `scripts/backlog_compiler.py --plan`. Do not hand-edit.",
        "",
    ]

    for section in ("Now", "Next", "Later"):
        lines.extend([f"## {section}", ""])
        section_tasks = buckets[section]
        if not section_tasks:
            lines.append("- _No queued tasks._")
            lines.append("")
            continue

        for idx, task in enumerate(section_tasks, start=1):
            lines.append(f"### {idx}. {task.title}")
            lines.append(f"- Impact: **{task.impact}**")
            lines.append(f"- Effort signal: **{task.effort}** ({len(task.files)} touched files, fanout heuristic)")
            lines.append(f"- Priority score: **{task.score}**")
            lines.append(f"- Detail: {task.detail}")
            lines.append("- Commands:")
            lines.append(command_block(task))
            lines.append("")

    (ROOT / output_path).write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", action="store_true", help="Compile and write the work queue markdown output.")
    parser.add_argument("--output", default="docs/wiki/current-work-queue.md", help="Output markdown path.")
    parser.add_argument("--focus", choices=["missing-target-files", "todo-placeholders", "missing-sentinels", "ledger-drift"], help="Print only a specific category summary.")
    parser.add_argument("--strict-missing-targets", action="store_true")
    parser.add_argument("--strict-todo", action="store_true")
    parser.add_argument("--strict-sentinels", action="store_true")
    parser.add_argument("--strict-ledger", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    tasks = make_tasks()

    if args.plan:
        write_queue(tasks, Path(args.output))
        print(f"Wrote {args.output} with {len(tasks)} tasks.")

    if args.focus:
        focus_tasks = [t for t in tasks if t.kind == args.focus]
        for task in focus_tasks:
            print(f"{task.title}: {task.detail}")
        if not focus_tasks:
            print(f"No tasks for focus={args.focus}")

    strict_flags = {
        "missing-target-files": args.strict_missing_targets,
        "todo-placeholders": args.strict_todo,
        "missing-sentinels": args.strict_sentinels,
        "ledger-drift": args.strict_ledger,
    }
    if any(strict_flags.values()):
        active_kinds = {k for k, enabled in strict_flags.items() if enabled}
        violations = [task for task in tasks if task.kind in active_kinds]
        if violations:
            for task in violations:
                print(f"FAIL [{task.kind}] {task.title}")
            return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
