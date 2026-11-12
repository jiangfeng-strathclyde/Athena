from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from athena.cli import main


class AlphaCliTests(unittest.TestCase):
    def run_cli(self, *args: str) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = main(list(args))
        return code, stdout.getvalue(), stderr.getvalue()

    def test_init_creates_private_local_state(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "研究 project"
            code, stdout, stderr = self.run_cli("init", str(root), "--name", "My study", "--json")
            self.assertEqual(0, code, stderr)
            result = json.loads(stdout)
            self.assertTrue(result["created"])
            self.assertEqual(".athena", result["state_directory"])
            self.assertTrue((root / ".athena" / "project.json").is_file())
            self.assertTrue((root / ".athena" / "private").is_dir())
            self.assertFalse(any(root.glob(".athena-init-*")))

    def test_reinitialization_fails_without_changing_state(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "project"
            self.assertEqual(0, self.run_cli("init", str(root), "--name", "First")[0])
            state = (root / ".athena" / "project.json").read_bytes()
            code, _, stderr = self.run_cli("init", str(root), "--name", "Second")
            self.assertEqual(1, code)
            self.assertIn("already exists", stderr)
            self.assertEqual(state, (root / ".athena" / "project.json").read_bytes())

    def test_missing_project_is_actionable(self):
        with tempfile.TemporaryDirectory() as temporary:
            code, _, stderr = self.run_cli("status", "--project", temporary)
            self.assertEqual(1, code)
            self.assertIn("init", stderr)

    def test_unsafe_home_or_root_is_blocked(self):
        code, _, stderr = self.run_cli("init", str(Path.home()), "--name", "No")
        self.assertEqual(3, code)
        self.assertIn("home", stderr)


if __name__ == "__main__":
    unittest.main()

