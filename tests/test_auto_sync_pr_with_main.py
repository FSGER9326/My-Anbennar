from __future__ import annotations

import contextlib
import importlib.util
import io
import pathlib
import subprocess
import sys
import unittest
from unittest.mock import patch


def _load_module():
    repo_root = pathlib.Path(__file__).resolve().parents[1]
    script_path = repo_root / "scripts" / "auto_sync_pr_with_main.py"
    spec = importlib.util.spec_from_file_location("auto_sync_pr_with_main", script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class TestEnsureCleanWorktree(unittest.TestCase):
    def setUp(self):
        self.module = _load_module()

    def test_existing_unresolved_conflicts_returns_structured_mode(self):
        unresolved = subprocess.CompletedProcess(
            args=["git", "diff", "--name-only", "--diff-filter=U"],
            returncode=0,
            stdout="missions/verne.txt\n",
            stderr="",
        )
        with patch.object(self.module, "run", return_value=unresolved):
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                with self.assertRaises(SystemExit) as ctx:
                    self.module.ensure_clean_worktree()

        self.assertEqual(self.module.EXIT_NEEDS_MANUAL_CONFLICT, ctx.exception.code)
        rendered = output.getvalue()
        self.assertIn("Existing unresolved merge conflicts detected.", rendered)
        self.assertIn("EXIT_MODE=needs_manual_conflict", rendered)


class TestMainMergeFailureHandling(unittest.TestCase):
    def setUp(self):
        self.module = _load_module()

    def test_merge_failure_without_merge_head_returns_error(self):
        def fake_run(cmd: list[str], *, check: bool = False):
            if cmd == ["git", "fetch", "origin"]:
                return subprocess.CompletedProcess(cmd, 0, "", "")
            if cmd[:4] == ["git", "merge", "--no-commit", "--no-ff"]:
                return subprocess.CompletedProcess(cmd, 1, "", "fatal: bad revision")
            if cmd == ["git", "diff", "--name-only", "--diff-filter=U"]:
                return subprocess.CompletedProcess(cmd, 0, "", "")
            raise AssertionError(f"Unexpected command: {cmd}")

        with (
            patch.object(self.module, "ensure_clean_worktree", return_value=None),
            patch.object(self.module, "current_branch", return_value="feature/test"),
            patch.object(self.module, "has_merge_head", return_value=False),
            patch.object(self.module, "run_python_script", return_value=0),
            patch.object(self.module, "run", side_effect=fake_run),
        ):
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                code = self.module.main()

        self.assertEqual(1, code)
        self.assertIn("Merge failed before creating a merge state", output.getvalue())


if __name__ == "__main__":
    unittest.main()
