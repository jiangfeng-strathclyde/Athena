from __future__ import annotations

import contextlib
import io
import json
import os
import subprocess
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

    def test_resume_contract_checkpoints_from_outside_project(self):
        with tempfile.TemporaryDirectory() as temporary:
            parent = Path(temporary)
            root = parent / "%ATHENA_PERCENT_SENTINEL% project'quote with spaces"
            self.assertEqual(
                0,
                self.run_cli("init", str(root), "--name", "Portable contract")[0],
            )
            code, stdout, stderr = self.run_cli(
                "plan",
                "--project",
                str(root),
                "Record the evidence",
                "--skill",
                "research-integrity-pipeline",
                "--json",
            )
            self.assertEqual(0, code, stderr)
            task_id = json.loads(stdout)["task_id"]

            code, stdout, stderr = self.run_cli(
                "resume", "--project", str(root), "--task", task_id, "--json"
            )
            self.assertEqual(0, code, stderr)
            action = json.loads(stdout)["action"]
            self.assertTrue(Path(action["output_directory"]).is_absolute())
            self.assertTrue(Path(action["output_directory"]).is_dir())
            checkpoint_argv = action["result_contract"]["checkpoint_argv"]
            self.assertEqual(str(root), checkpoint_argv[checkpoint_argv.index("--project") + 1])
            self.assertNotIn(str(root), action["result_contract"]["checkpoint_command"])

            artifact = Path(action["result_contract"]["artifact_path"])
            artifact.write_text("evidence-linked result\n", encoding="utf-8")
            environment = os.environ.copy()
            environment["ATHENA_PERCENT_SENTINEL"] = "expanded-elsewhere"
            repository = str(Path(__file__).resolve().parents[1])
            environment["PYTHONPATH"] = os.pathsep.join(
                value for value in (repository, environment.get("PYTHONPATH", "")) if value
            )
            completed = subprocess.run(
                checkpoint_argv,
                cwd=parent,
                env=environment,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(0, completed.returncode, completed.stderr)
            self.assertEqual("complete", json.loads(completed.stdout)["status"])

            code, stdout, stderr = self.run_cli(
                "plan",
                "--project",
                str(root),
                "Record another result",
                "--skill",
                "research-integrity-pipeline",
                "--json",
            )
            self.assertEqual(0, code, stderr)
            second_task = json.loads(stdout)["task_id"]
            code, stdout, stderr = self.run_cli(
                "resume", "--project", str(root), "--task", second_task, "--json"
            )
            self.assertEqual(0, code, stderr)
            second_action = json.loads(stdout)["action"]
            second_artifact = Path(second_action["result_contract"]["artifact_path"])
            second_artifact.write_text("second result\n", encoding="utf-8")
            command = second_action["result_contract"]["checkpoint_command"]
            command_result = subprocess.run(
                command,
                cwd=parent,
                env=environment,
                shell=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(0, command_result.returncode, command_result.stderr)
            self.assertEqual("complete", json.loads(command_result.stdout)["status"])

    def test_unsafe_home_or_root_is_blocked(self):
        code, _, stderr = self.run_cli("init", str(Path.home()), "--name", "No")
        self.assertEqual(3, code)
        self.assertIn("home", stderr)


if __name__ == "__main__":
    unittest.main()
