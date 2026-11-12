from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from athena.state import (
    ConflictError,
    StateError,
    action_for_task,
    atomic_write_json,
    checkpoint_task,
    create_task,
    init_project,
    load_project,
    load_task,
    project_status,
    read_json,
)


class AlphaStateTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name) / "Athena 项目"
        init_project(
            self.root,
            "Evidence project",
            now="2026-01-01T00:00:00Z",
            project_id="prj_000000000001",
        )

    def tearDown(self):
        self.temporary.cleanup()

    def test_plan_persists_redacted_source_and_stable_resume(self):
        source = Path(self.temporary.name) / "paper.pdf"
        source.write_bytes(b"paper bytes")
        task = create_task(
            self.root,
            "Trace citations and make an explorable paper",
            [str(source), "https://example.org/paper?id=1&api_key=secret#section"],
            now="2026-01-01T00:01:00Z",
            task_id="tsk_000000000001",
        )
        self.assertEqual(
            ["citation-tracing", "explorable-paper", "research-integrity-pipeline"],
            task["route"]["skills"],
        )
        serialized = (self.root / ".athena" / "tasks" / "tsk_000000000001.json").read_text("utf-8")
        self.assertNotIn(str(source.parent), serialized)
        self.assertNotIn("secret", serialized)
        self.assertIn("REDACTED", serialized)
        first = action_for_task(self.root)
        second = action_for_task(self.root)
        self.assertEqual(first, second)
        self.assertEqual("citation-tracing", first["action"]["skill"])
        self.assertNotIn(str(self.root), json.dumps(first))

    def test_checkpoint_advances_and_survives_restart(self):
        task = create_task(
            self.root,
            "Trace citations",
            now="2026-01-01T00:01:00Z",
            task_id="tsk_000000000002",
        )
        artifact = Path(self.temporary.name) / "citation-table.md"
        artifact.write_text("# Citation table\n", encoding="utf-8")
        updated = checkpoint_task(
            self.root,
            task["task_id"],
            "01-citation-tracing",
            artifact=artifact,
            note="Screened supplied corpus only.",
            expected_revision=0,
            now="2026-01-01T00:02:00Z",
        )
        self.assertEqual(1, updated["revision"])
        self.assertEqual("in_progress", updated["status"])
        self.assertEqual(1, len(updated["artifacts"]))
        stored = self.root / ".athena" / Path(*updated["artifacts"][0]["relative_path"].split("/"))
        self.assertEqual(artifact.read_bytes(), stored.read_bytes())
        resumed = action_for_task(self.root, task["task_id"])
        self.assertEqual("research-integrity-pipeline", resumed["action"]["skill"])
        with self.assertRaises(ConflictError):
            checkpoint_task(self.root, task["task_id"], "01-citation-tracing")

    def test_status_is_byte_for_byte_read_only(self):
        create_task(
            self.root,
            "Check the evidence",
            now="2026-01-01T00:01:00Z",
            task_id="tsk_000000000003",
        )
        files = sorted((self.root / ".athena").rglob("*"))
        before = {path: path.read_bytes() for path in files if path.is_file()}
        first = project_status(self.root)
        second = project_status(self.root)
        after = {path: path.read_bytes() for path in files if path.is_file()}
        self.assertEqual(first, second)
        self.assertEqual(before, after)

    def test_corrupt_future_and_extra_state_fail_closed(self):
        state_path = self.root / ".athena" / "project.json"
        original = state_path.read_bytes()
        data = read_json(state_path)
        data["schema_version"] = 999
        atomic_write_json(state_path, data)
        with self.assertRaisesRegex(StateError, "future"):
            load_project(self.root)
        state_path.write_bytes(original)
        data = read_json(state_path)
        data["surprise"] = True
        atomic_write_json(state_path, data)
        with self.assertRaisesRegex(StateError, "unexpected"):
            load_project(self.root)

    def test_atomic_replace_failure_keeps_old_state(self):
        path = self.root / ".athena" / "project.json"
        original = path.read_bytes()
        data = read_json(path)
        data["revision"] = 1
        with mock.patch("athena.state.os.replace", side_effect=OSError("locked")):
            with self.assertRaises(OSError):
                atomic_write_json(path, data)
        self.assertEqual(original, path.read_bytes())
        self.assertFalse(any(path.parent.glob(f".{path.name}.*.tmp")))

    def test_revision_cas_and_step_order_fail_closed(self):
        task = create_task(
            self.root,
            "Trace citations and create explorable HTML",
            now="2026-01-01T00:01:00Z",
            task_id="tsk_000000000004",
        )
        with self.assertRaises(ConflictError):
            checkpoint_task(
                self.root,
                task["task_id"],
                "02-explorable-paper",
                expected_revision=0,
            )
        checkpoint_task(
            self.root,
            task["task_id"],
            "01-citation-tracing",
            expected_revision=0,
            now="2026-01-01T00:02:00Z",
        )
        with self.assertRaisesRegex(ConflictError, "revision changed"):
            checkpoint_task(
                self.root,
                task["task_id"],
                "02-explorable-paper",
                expected_revision=0,
            )
        self.assertEqual(1, load_task(self.root, task["task_id"])["revision"])

    @unittest.skipIf(os.name == "nt", "Windows symlink creation may require privileges")
    def test_linked_artifact_is_rejected(self):
        task = create_task(
            self.root,
            "Check evidence",
            task_id="tsk_000000000005",
            now="2026-01-01T00:01:00Z",
        )
        target = Path(self.temporary.name) / "real.md"
        target.write_text("data", encoding="utf-8")
        link = Path(self.temporary.name) / "linked.md"
        link.symlink_to(target)
        with self.assertRaises(Exception):
            checkpoint_task(self.root, task["task_id"], task["steps"][0]["step_id"], artifact=link)


if __name__ == "__main__":
    unittest.main()

