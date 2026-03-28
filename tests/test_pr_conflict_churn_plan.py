from __future__ import annotations

import importlib.util
import pathlib
import subprocess
import sys
import unittest
from unittest.mock import patch


def load_module():
    path = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "pr_conflict_churn_plan.py"
    spec = importlib.util.spec_from_file_location("pr_conflict_churn_plan", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class TestRunGhOpenPrs(unittest.TestCase):
    def setUp(self):
        self.m = load_module()

    def test_missing_gh_shows_fallback(self):
        with patch.object(self.m.subprocess, "run", side_effect=FileNotFoundError("gh missing")):
            with self.assertRaises(RuntimeError) as ctx:
                self.m.run_gh_open_prs("main")
        self.assertIn(self.m.FALLBACK_USAGE, str(ctx.exception))

    def test_nonzero_gh_exit_shows_fallback(self):
        result = subprocess.CompletedProcess(args=["gh"], returncode=1, stdout="", stderr="auth failed")
        with patch.object(self.m.subprocess, "run", return_value=result):
            with self.assertRaises(RuntimeError) as ctx:
                self.m.run_gh_open_prs("main")
        msg = str(ctx.exception)
        self.assertIn("auth failed", msg)
        self.assertIn(self.m.FALLBACK_USAGE, msg)

    def test_invalid_json_shows_auth_hint(self):
        result = subprocess.CompletedProcess(args=["gh"], returncode=0, stdout="not-json", stderr="")
        with patch.object(self.m.subprocess, "run", return_value=result):
            with self.assertRaises(RuntimeError) as ctx:
                self.m.run_gh_open_prs("main")
        msg = str(ctx.exception)
        self.assertIn("gh auth status", msg)
        self.assertIn(self.m.FALLBACK_USAGE, msg)

    def test_valid_json_returns_rows(self):
        result = subprocess.CompletedProcess(
            args=["gh"],
            returncode=0,
            stdout='[{"headRefName":"feature-a","title":"Feature A","baseRefName":"main"}]',
            stderr="",
        )
        with patch.object(self.m.subprocess, "run", return_value=result):
            rows = self.m.run_gh_open_prs("main")
        self.assertEqual("feature-a", rows[0]["headRefName"])


if __name__ == "__main__":
    unittest.main()
