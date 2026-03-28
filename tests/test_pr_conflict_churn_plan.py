from __future__ import annotations

import importlib.util
import pathlib
import subprocess
import sys
import unittest
from unittest.mock import patch


def _load_module():
    repo_root = pathlib.Path(__file__).resolve().parents[1]
    script_path = repo_root / "scripts" / "pr_conflict_churn_plan.py"
    spec = importlib.util.spec_from_file_location("pr_conflict_churn_plan", script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class TestBuildCandidatesGhHandling(unittest.TestCase):
    def setUp(self):
        self.module = _load_module()

    def test_missing_gh_shows_fallback_guidance(self):
        with patch.object(
            self.module.subprocess,
            "run",
            side_effect=FileNotFoundError("gh not found"),
        ):
            with self.assertRaises(RuntimeError) as ctx:
                self.module.build_candidates("main", None)

        msg = str(ctx.exception)
        self.assertIn("GitHub CLI (`gh`) is not installed", msg)
        self.assertIn(self.module.FALLBACK_USAGE, msg)

    def test_nonzero_gh_exit_shows_fallback_guidance(self):
        result = subprocess.CompletedProcess(
            args=["gh", "pr", "list"],
            returncode=1,
            stdout="",
            stderr="not authenticated",
        )
        with patch.object(self.module.subprocess, "run", return_value=result):
            with self.assertRaises(RuntimeError) as ctx:
                self.module.build_candidates("main", None)

        msg = str(ctx.exception)
        self.assertIn("Could not load open PRs from GitHub CLI", msg)
        self.assertIn("not authenticated", msg)
        self.assertIn(self.module.FALLBACK_USAGE, msg)

    def test_invalid_json_shows_auth_and_fallback_guidance(self):
        result = subprocess.CompletedProcess(
            args=["gh", "pr", "list"],
            returncode=0,
            stdout="not-json",
            stderr="",
        )
        with patch.object(self.module.subprocess, "run", return_value=result):
            with self.assertRaises(RuntimeError) as ctx:
                self.module.build_candidates("main", None)

        msg = str(ctx.exception)
        self.assertIn("GitHub CLI returned unreadable PR data", msg)
        self.assertIn("gh auth status", msg)
        self.assertIn(self.module.FALLBACK_USAGE, msg)

    def test_valid_json_returns_rows(self):
        result = subprocess.CompletedProcess(
            args=["gh", "pr", "list"],
            returncode=0,
            stdout='[{"headRefName":"main","title":"Base","baseRefName":"main"}]',
            stderr="",
        )
        with patch.object(self.module.subprocess, "run", return_value=result):
            rows = self.module.build_candidates("main", None)

        self.assertEqual([], rows)


class TestBuildCandidates(unittest.TestCase):
    def setUp(self):
        self.module = _load_module()

    def test_branch_compare_failure_has_actionable_guidance(self):
        with patch.object(
            self.module,
            "changed_files",
            side_effect=RuntimeError("git merge-base failed"),
        ):
            with self.assertRaises(RuntimeError) as ctx:
                self.module.build_candidates("main", ["feature-1"])

        msg = str(ctx.exception)
        self.assertIn("Could not compare `feature-1` against `main`", msg)
        self.assertIn("git fetch origin main:main", msg)
        self.assertIn("git fetch origin feature-1:feature-1", msg)
        self.assertIn(self.module.FALLBACK_USAGE, msg)


if __name__ == "__main__":
    unittest.main()
