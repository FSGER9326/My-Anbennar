#!/usr/bin/env python3
"""Compile roadmap/backlog signals into a prioritized current work queue."""

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

EXTRA_RELEVANT_FILES = [
    Path("automation/country_profiles/verne.json"),
    Path("scripts/verne_smoke_checks.sh"),
    Path("scripts/verne_smoke_checks.ps1"),
    Path("scripts/verne_mode_impl.sh"),
    Path("scripts/verne_mode_impl.ps1"),
]

SENTINEL_FILES = [
    Path("automation/country_profiles/verne.json"),
    Path("scripts/verne_smoke_checks.sh"),
    Path("scripts/verne_smoke_checks.ps1"),
]

LEDGER_PATH = Path("docs/wiki/verne-id-ledger.md")
ID_PATTERN = re.compile(r"\bverne_[a-z0-9_]+\b")
LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
TODO_PATTERN = re.compile(r"\b(?:TODO|TBD|FIXME|PLACEHOLDER|_TBD_)\b", re.IGNORECASE)

IGNORED_SUFFIXES = {".dds", ".png", ".jpg", ".jpeg", ".svg", ".ogg", ".wav", ".tga", ".mp3", ".pdf"}
GAMEPLAY_PREFIXES = ("common/", "events/", "missions/", "decisions/", "localisation/", "automation/")


@dataclass(frozen=True)
class Task:
    title: str
    kind: str
    detail: str
    files: tuple[Path, ...]
    impact: str
    file_count: int
    fanout: int

    @property
    def effort(self) -> str:
        complexity = self.file_count + self.fanout
        if complexity <= 4:
            return "small"
        if complexity <= 10:
            return "medium"
        return "large"

    @property
    def score(self) -> int:
        impact_score = {
            "breaks CI": 100,
            "blocks milestones": 75,
            "high gameplay leverage": 55,
        }[self.impact]
        effort_penalty = {"small": 0, "medium": 12, "large": 24}[self.effort]
        return impact_score - effort_penalty

    @property
    def bucket(self) -> str:
        if self.impact == "breaks CI":
            return "Now"
        if self.score >= 70:
            return "Next"
        return "Later"


def safe_read(path: Path) -> str:
    abs_path = ROOT / path
    if not abs_path.exists() or not abs_path.is_file():
        return ""
    return abs_path.read_text(encoding="utf-8", errors="ignore")


def norm(paths: Iterable[Path]) -> tuple[Path, ...]:
    return tuple(sorted(set(paths), key=lambda p: str(p)))


def fanout(paths: Iterable[Path]) -> int:
    return len({p.parts[0] if p.parts else "" for p in paths})


def infer_target_files() -> tuple[Path, ...]:
    targets: set[Path] = set()
    for doc in DOC_SOURCES:
        text = safe_read(doc)
        for match in LINK_PATTERN.finditer(text):
            href = match.group(1).strip().split("#", 1)[0]
            if not href or href.startswith(("http://", "https://", "mailto:", "#")):
                continue
            resolved = (doc.parent / href).resolve()
            try:
                rel = resolved.relative_to(ROOT)
            except ValueError:
                continue
            if rel.suffix.lower() in IGNORED_SUFFIXES or rel.suffix.lower() == ".md":
                continue
            targets.add(rel)
    return norm(targets)


def relevant_files(targets: tuple[Path, ...]) -> tuple[Path, ...]:
    files: set[Path] = {p for p in targets if (ROOT / p).exists()}
    for extra in EXTRA_RELEVANT_FILES:
        if (ROOT / extra).exists():
            files.add(extra)
    return norm(files)


def todo_hits(files: tuple[Path, ...]) -> dict[Path, int]:
    hits: dict[Path, int] = {}
    for path in files:
        if path.suffix.lower() in IGNORED_SUFFIXES:
            continue
        text = safe_read(path)
        count = sum(1 for line in text.splitlines() if TODO_PATTERN.search(line))
        if count:
            hits[path] = count
    return hits


def sentinel_coverage_gaps(targets: tuple[Path, ...]) -> tuple[Path, ...]:
    haystack = "\n".join(safe_read(path) for path in SENTINEL_FILES)
    gaps = [
        path
        for path in targets
        if str(path).startswith(GAMEPLAY_PREFIXES) and str(path) not in haystack
    ]
    return norm(gaps)


def untracked_ids(files: tuple[Path, ...]) -> dict[str, tuple[Path, ...]]:
    ledger_ids = set(ID_PATTERN.findall(safe_read(LEDGER_PATH)))
    found: dict[str, set[Path]] = {}
    for path in files:
        text = safe_read(path)
        for id_value in ID_PATTERN.findall(text):
            found.setdefault(id_value, set()).add(path)
    return {
        id_value: norm(paths)
        for id_value, paths in found.items()
        if id_value not in ledger_ids
    }


def build_tasks() -> list[Task]:
    targets = infer_target_files()
    relevant = relevant_files(targets)
    tasks: list[Task] = []

    missing_targets = norm(path for path in targets if not (ROOT / path).exists())
    if missing_targets:
        tasks.append(
            Task(
                title="Create missing roadmap/backlog target files",
                kind="missing-target-files",
                detail="Missing targets: " + ", ".join(str(p) for p in missing_targets[:8]),
                files=missing_targets,
                impact="blocks milestones",
                file_count=len(missing_targets),
                fanout=fanout(missing_targets),
            )
        )

    todos = todo_hits(relevant)
    if todos:
        files = norm(todos)
        tasks.append(
            Task(
                title="Resolve TODO/placeholder debt in relevant gameplay + automation files",
                kind="todo-placeholders",
                detail=(
                    f"{len(files)} relevant files contain TODO markers "
                    f"({sum(todos.values())} total marker lines)."
                ),
                files=files,
                impact="high gameplay leverage",
                file_count=len(files),
                fanout=fanout(files),
            )
        )

    gaps = sentinel_coverage_gaps(targets)
    if gaps:
        tasks.append(
            Task(
                title="Add smoke/profile sentinels for uncovered roadmap targets",
                kind="missing-sentinels",
                detail=f"{len(gaps)} roadmap targets are missing sentinel/profile references.",
                files=gaps,
                impact="breaks CI",
                file_count=len(gaps),
                fanout=fanout(gaps),
            )
        )

    missing = untracked_ids(relevant)
    if missing:
        sample = ", ".join(sorted(missing)[:10])
        files = norm(file for paths in missing.values() for file in paths)
        tasks.append(
            Task(
                title="Register untracked verne_* IDs in docs/wiki/verne-id-ledger.md",
                kind="ledger-drift",
                detail=f"IDs not listed in ledger (sample): {sample}",
                files=files,
                impact="blocks milestones",
                file_count=len(files),
                fanout=fanout(files),
            )
        )

    return sorted(tasks, key=lambda t: (t.bucket, -t.score, t.title))


def command_triplet(kind: str) -> tuple[str, str, str]:
    validate = {
        "missing-target-files": "python scripts/backlog_compiler.py --plan --strict-missing-targets",
        "todo-placeholders": "python scripts/backlog_compiler.py --plan --strict-todo",
        "missing-sentinels": "python scripts/backlog_compiler.py --plan --strict-sentinels",
        "ledger-drift": "python scripts/backlog_compiler.py --plan --strict-ledger",
    }[kind]
    implement = f"python scripts/backlog_compiler.py --plan --focus {kind}"
    verify = "python scripts/backlog_compiler.py --plan"
    return validate, implement, verify


def write_queue(tasks: list[Task], output: Path) -> None:
    grouped = {"Now": [], "Next": [], "Later": []}
    for task in tasks:
        grouped[task.bucket].append(task)

    lines = [
        "# Current Work Queue (Generated)",
        "",
        "This file is generated by `python scripts/backlog_compiler.py --plan`. Do not hand-edit.",
        "",
    ]

    for section in ("Now", "Next", "Later"):
        lines.extend([f"## {section}", ""])
        section_tasks = grouped[section]
        if not section_tasks:
            lines.extend(["- _No queued tasks._", ""])
            continue

        for idx, task in enumerate(section_tasks, start=1):
            validate, implement, verify = command_triplet(task.kind)
            lines.extend(
                [
                    f"### {idx}. {task.title}",
                    f"- Impact: **{task.impact}**",
                    f"- Effort signal: **{task.effort}** (file_count={task.file_count}, dependency_fanout={task.fanout})",
                    f"- Priority score: **{task.score}**",
                    f"- Detail: {task.detail}",
                    "- Commands:",
                    f"  - validate: `{validate}`",
                    f"  - implement: `{implement}`",
                    f"  - verify: `{verify}`",
                    "",
                ]
            )

    (ROOT / output).write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", action="store_true", help="Write docs/wiki/current-work-queue.md")
    parser.add_argument("--output", default="docs/wiki/current-work-queue.md")
    parser.add_argument(
        "--focus",
        choices=["missing-target-files", "todo-placeholders", "missing-sentinels", "ledger-drift"],
        help="Print only one category summary.",
    )
    parser.add_argument("--strict-missing-targets", action="store_true")
    parser.add_argument("--strict-todo", action="store_true")
    parser.add_argument("--strict-sentinels", action="store_true")
    parser.add_argument("--strict-ledger", action="store_true")
    return parser.parse_args()


def strict_failures(tasks: list[Task], args: argparse.Namespace) -> list[Task]:
    enabled = {
        "missing-target-files": args.strict_missing_targets,
        "todo-placeholders": args.strict_todo,
        "missing-sentinels": args.strict_sentinels,
        "ledger-drift": args.strict_ledger,
    }
    active = {kind for kind, on in enabled.items() if on}
    return [task for task in tasks if task.kind in active]


def main() -> int:
    args = parse_args()
    tasks = build_tasks()

    if args.plan:
        write_queue(tasks, Path(args.output))
        print(f"Wrote {args.output} with {len(tasks)} tasks.")

    if args.focus:
        selected = [task for task in tasks if task.kind == args.focus]
        if not selected:
            print(f"No tasks found for focus={args.focus}")
        for task in selected:
            print(f"{task.title}: {task.detail}")

    violations = strict_failures(tasks, args)
    if violations:
        for task in violations:
            print(f"FAIL [{task.kind}] {task.title}")
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
