from __future__ import annotations

import pathlib
import shutil
import subprocess
import tempfile
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT_SOURCE = REPO_ROOT / "scripts" / "auto_sync_pr_with_main.sh"


def _run(cmd: list[str], cwd: pathlib.Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, check=False)


def _init_repo(path: pathlib.Path) -> None:
    _run(["git", "init", "-b", "main"], path)
    _run(["git", "config", "user.email", "tests@example.com"], path)
    _run(["git", "config", "user.name", "Test Runner"], path)


class TestAutoSyncShellConflictModes(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.repo = pathlib.Path(self.tempdir.name)
        (self.repo / "scripts").mkdir(parents=True, exist_ok=True)
        shutil.copy2(SCRIPT_SOURCE, self.repo / "scripts" / "auto_sync_pr_with_main.sh")
        _init_repo(self.repo)
        self.default_branch = "main"

    def tearDown(self):
        self.tempdir.cleanup()

    def _create_conflict_state(self) -> None:
        (self.repo / "file.txt").write_text("base\n", encoding="utf-8")
        _run(["git", "add", "file.txt", "scripts/auto_sync_pr_with_main.sh"], self.repo)
        _run(["git", "commit", "-m", "base"], self.repo)
        _run(["git", "checkout", "-b", "feature"], self.repo)
        (self.repo / "file.txt").write_text("feature\n", encoding="utf-8")
        _run(["git", "commit", "-am", "feature change"], self.repo)
        _run(["git", "checkout", self.default_branch], self.repo)
        (self.repo / "file.txt").write_text("master\n", encoding="utf-8")
        _run(["git", "commit", "-am", f"{self.default_branch} change"], self.repo)
        _run(["git", "checkout", "feature"], self.repo)
        _run(["git", "merge", self.default_branch], self.repo)

    def test_conflict_only_state_returns_structured_mode(self):
        self._create_conflict_state()
        result = _run(["bash", "scripts/auto_sync_pr_with_main.sh"], self.repo)
        self.assertEqual(20, result.returncode)
        self.assertIn("EXIT_MODE=needs_manual_conflict", result.stdout)

    def test_conflict_plus_other_edit_returns_dirty_tree_error(self):
        self._create_conflict_state()
        (self.repo / "extra.txt").write_text("extra\n", encoding="utf-8")
        result = _run(["bash", "scripts/auto_sync_pr_with_main.sh"], self.repo)
        self.assertEqual(1, result.returncode)
        self.assertIn("non-conflict changes", result.stdout)


if __name__ == "__main__":
    unittest.main()
