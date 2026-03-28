#!/usr/bin/env python3
"""Unified automation entrypoint for Verne branch sync + validation.

Stages:
  sync -> resolve_conflicts -> validate -> summarize -> ready_to_push
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


@dataclass
class StepResult:
    name: str
    command: list[str]
    returncode: int

    @property
    def ok(self) -> bool:
        return self.returncode == 0


class Orchestrator:
    def __init__(self, args: argparse.Namespace) -> None:
        self.args = args
        self.results: list[StepResult] = []

    def run(self, cmd: list[str], *, allow_failure: bool = False) -> StepResult:
        printable = " ".join(cmd)
        print(f"$ {printable}")
        result = subprocess.run(cmd, cwd=ROOT, text=True, check=False)
        step = StepResult(name=cmd[1] if len(cmd) > 1 else cmd[0], command=cmd, returncode=result.returncode)
        self.results.append(step)
        if result.returncode != 0 and not allow_failure:
            raise SystemExit(result.returncode)
        return step

    def unresolved_files(self) -> list[str]:
        proc = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=U"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


    def has_merge_head(self) -> bool:
        proc = subprocess.run(
            ["git", "rev-parse", "-q", "--verify", "MERGE_HEAD"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        return proc.returncode == 0

    def apply_fallback_preference(self, files: list[str]) -> None:
        if not files:
            return
        if self.args.prefer_main:
            selector = "--theirs"
            label = "prefer-main"
        elif self.args.prefer_branch:
            selector = "--ours"
            label = "prefer-branch"
        else:
            return

        print(f"Applying {label} fallback strategy to {len(files)} unresolved files...")
        for rel_path in files:
            self.run(["git", "checkout", selector, "--", rel_path])
            self.run(["git", "add", "--", rel_path])

    def stage_sync(self) -> None:
        print("\n=== Stage: sync ===")
        # Existing sync logic (fetch/merge/no-commit + initial guardrails).
        sync_step = self.run([
            sys.executable,
            str(SCRIPTS / "auto_sync_pr_with_main.py"),
            "--base-ref",
            self.args.base_ref,
            "--sync-only",
        ], allow_failure=True)

        if not sync_step.ok and not self.has_merge_head():
            print("Sync failed before merge state was created. Stopping.")
            raise SystemExit(sync_step.returncode)

    def stage_resolve_conflicts(self) -> None:
        print("\n=== Stage: resolve_conflicts ===")
        unresolved_before = self.unresolved_files()
        if unresolved_before:
            print(f"Starting with {len(unresolved_before)} unresolved files.")
        else:
            print("No unresolved files detected; running resolver scripts as safety checks.")

        # Docs conflict hotspots first.
        self.run([sys.executable, str(SCRIPTS / "resolve_docs_conflicts.py")], allow_failure=True)

        content_cmd = [sys.executable, str(SCRIPTS / "resolve_content_conflicts.py")]
        if self.args.mode == "strict":
            content_cmd.append("--union-docs-only")
        if self.args.prefer_main:
            content_cmd.append("--prefer-main")
        elif self.args.prefer_branch:
            content_cmd.append("--prefer-branch")
        self.run(content_cmd, allow_failure=True)

        unresolved = self.unresolved_files()
        if unresolved:
            print("Unresolved files after scripted resolution:")
            for path in unresolved:
                print(f" - {path}")

        if self.args.mode == "fast" and unresolved:
            self.apply_fallback_preference(unresolved)

    def stage_validate(self) -> bool:
        print("\n=== Stage: validate ===")
        failures: list[str] = []

        checks: list[list[str]] = [
            [sys.executable, str(SCRIPTS / "country_smoke_runner.py"), "--profile", "automation/country_profiles/verne.json"],
            [sys.executable, str(SCRIPTS / "docs_conflict_guard.py")],
            [sys.executable, str(SCRIPTS / "localisation_audit.py"), "--file", "localisation/Flavour_Verne_A33_l_english.yml"],
            [
                sys.executable,
                str(SCRIPTS / "event_id_audit.py"),
                "--file",
                "events/Flavour_Verne_A33.txt",
                "--file",
                "events/verne_overhaul_dynasty_events.txt",
            ],
        ]

        for cmd in checks:
            step = self.run(cmd, allow_failure=True)
            if not step.ok:
                failures.append(" ".join(cmd))
                if self.args.mode == "strict":
                    break

        if failures:
            print("Validation failures:")
            for entry in failures:
                print(f" - {entry}")
            return False
        return True

    def stage_summarize(self, validation_ok: bool) -> None:
        print("\n=== Stage: summarize ===")
        unresolved = self.unresolved_files()
        print(f"Mode: {self.args.mode}")
        print(f"Base ref: {self.args.base_ref}")
        if self.args.prefer_main:
            print("Conflict preference: main (theirs)")
        elif self.args.prefer_branch:
            print("Conflict preference: branch (ours)")
        else:
            print("Conflict preference: none (manual for non-scripted conflicts)")

        print("Step results:")
        for idx, step in enumerate(self.results, start=1):
            state = "OK" if step.ok else "FAIL"
            print(f" {idx:02d}. [{state}] {' '.join(step.command)}")

        print(f"Validation status: {'passed' if validation_ok else 'failed'}")
        print(f"Unresolved conflicts remaining: {len(unresolved)}")
        for path in unresolved:
            print(f" - {path}")

    def stage_ready_to_push(self, validation_ok: bool) -> int:
        print("\n=== Stage: ready_to_push ===")
        unresolved = self.unresolved_files()
        if unresolved:
            print("NOT READY: unresolved conflicts remain. Resolve and rerun.")
            return 1
        if not validation_ok:
            print("NOT READY: validation failed. Fix issues and rerun.")
            return 1

        branch = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        ).stdout.strip()
        upstream = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        print("READY: clean conflict state and validations passed.")
        print("Habit reminder: sync first, then push.")
        if upstream.returncode == 0 and upstream.stdout.strip():
            print("Next command: git push")
        else:
            print(f"Next command: git push --set-upstream origin {branch}")
        return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Single Verne automation entrypoint (sync/resolve/validate/summarize/ready_to_push)."
    )
    parser.add_argument("--base-ref", default="origin/main", help="Merge source for sync stage.")
    parser.add_argument(
        "--mode",
        choices=("strict", "fast"),
        default="strict",
        help="strict=stop on first validation failure; fast=attempt fallback auto-resolution + keep validating.",
    )

    strategy = parser.add_mutually_exclusive_group()
    strategy.add_argument(
        "--prefer-main",
        action="store_true",
        help="Prefer main/theirs when resolving conflict blocks.",
    )
    strategy.add_argument(
        "--prefer-branch",
        action="store_true",
        help="Prefer branch/ours when resolving conflict blocks.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    orchestrator = Orchestrator(args)
    orchestrator.stage_sync()
    orchestrator.stage_resolve_conflicts()
    validation_ok = orchestrator.stage_validate()
    orchestrator.stage_summarize(validation_ok)
    return orchestrator.stage_ready_to_push(validation_ok)


if __name__ == "__main__":
    sys.exit(main())
