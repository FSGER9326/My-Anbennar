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


class TestBuildCandidatesErrors(unittest.TestCase):
    def setUp(self):
        self.m = load_module()

    def test_missing_gh_prints_fallback_usage(self):
        with patch.object(self.m.subprocess, "run", side_effect=FileNotFoundError("missing gh")):
            with self.assertRaises(RuntimeError) as ctx:
                self.m.build_candidates("main", None)
        self.assertIn(self.m.FALLBACK_USAGE, str(ctx.exception))

    def test_bad_json_prints_auth_hint(self):
        result = subprocess.CompletedProcess(args=["gh"], returncode=0, stdout="not-json", stderr="")
        with patch.object(self.m.subprocess, "run", return_value=result):
            with self.assertRaises(RuntimeError) as ctx:
                self.m.build_candidates("main", None)
        msg = str(ctx.exception)
        self.assertIn("gh auth status", msg)
        self.assertIn(self.m.FALLBACK_USAGE, msg)

    def test_compare_error_prints_fetch_commands(self):
        with patch.object(self.m, "changed_files", side_effect=RuntimeError("merge-base failed")):
            with self.assertRaises(RuntimeError) as ctx:
                self.m.build_candidates("main", ["feature-a"])
        msg = str(ctx.exception)
        self.assertIn("git fetch origin main:main", msg)
        self.assertIn("git fetch origin feature-a:feature-a", msg)


if __name__ == "__main__":
    unittest.main()
