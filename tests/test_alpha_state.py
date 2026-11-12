from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
import urllib.parse
from pathlib import Path
from unittest import mock

import athena.state as state_module
from athena.state import (
    PRIVATE_SOURCE_LOCATOR,
    BlockedError,
    ConflictError,
    StateError,
    action_for_task,
    atomic_write_json,
    canonical_json,
    checkpoint_task,
    create_task,
    init_project,
    load_project,
    load_task,
    project_lock,
    project_status,
    read_json,
    sha256_file,
    validate_task,
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

    def test_plan_persists_usable_local_source_and_stable_resume(self):
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
            ["citation-tracing", "research-integrity-pipeline", "explorable-paper"],
            task["route"]["skills"],
        )
        serialized = (self.root / ".athena" / "tasks" / "tsk_000000000001.json").read_text("utf-8")
        self.assertEqual(str(source.resolve()), json.loads(serialized)["sources"][0]["locator"])
        self.assertNotIn("secret", serialized)
        self.assertIn("REDACTED", serialized)
        first = action_for_task(self.root)
        second = action_for_task(self.root)
        self.assertEqual(first, second)
        self.assertEqual("citation-tracing", first["action"]["skill"])
        instruction = Path(first["action"]["instruction_path"])
        self.assertTrue(instruction.is_absolute())
        self.assertTrue(instruction.is_file())
        self.assertEqual(first["action"]["instruction_sha256"], sha256_file(instruction))
        action = first["action"]
        output = self.root / ".athena" / "artifacts" / task["task_id"] / action["step_id"]
        self.assertEqual(str(output), action["output_directory"])
        self.assertTrue(Path(action["output_directory"]).is_absolute())
        self.assertTrue(Path(action["output_directory"]).is_dir())
        checkpoint_argv = action["result_contract"]["checkpoint_argv"]
        self.assertEqual([sys.executable, "-m", "athena", "checkpoint"], checkpoint_argv[:4])
        self.assertEqual(str(self.root), checkpoint_argv[checkpoint_argv.index("--project") + 1])
        self.assertEqual(task["task_id"], checkpoint_argv[checkpoint_argv.index("--task") + 1])
        self.assertEqual(action["step_id"], checkpoint_argv[checkpoint_argv.index("--step") + 1])
        artifact_path = action["result_contract"]["artifact_path"]
        self.assertEqual(str(output / "result.md"), artifact_path)
        self.assertEqual(artifact_path, checkpoint_argv[checkpoint_argv.index("--artifact") + 1])
        self.assertEqual("--json", checkpoint_argv[-1])
        checkpoint_command = action["result_contract"]["checkpoint_command"]
        self.assertNotIn("ARTIFACT_PATH", checkpoint_command)
        self.assertNotIn(str(self.root), checkpoint_command)

    def test_same_named_sources_keep_distinct_usable_absolute_locators(self):
        sources = []
        for name in ("one", "two"):
            source = Path(self.temporary.name) / name / "paper.pdf"
            source.parent.mkdir()
            source.write_bytes(name.encode("ascii"))
            sources.append(source)
        task = create_task(self.root, "Check evidence", [str(path) for path in sources])
        persisted = load_task(self.root, task["task_id"])
        self.assertEqual([str(path.resolve()) for path in sources],
                         [source["locator"] for source in persisted["sources"]])
        for source, record in zip(sources, persisted["sources"]):
            self.assertEqual(source.read_bytes(), Path(record["locator"]).read_bytes())
            self.assertEqual(sha256_file(source), record["sha256"])

    def test_signed_url_credentials_are_redacted_from_persistent_state(self):
        opaque = "opaque-production-credential-1234567890"
        source = (
            "https://example.test/download?public=paper&sig=" + opaque
            + "&X-Amz-Credential=account%2Fscope&code=oauth-code"
            + "&sessionId=session-value&AWSAccessKeyId=aws-value"
            + "&GoogleAccessId=google-value&nested=x%3Btoken%3Dnested-value"
            + "&callback=x%253BaccessToken%253Ddouble-nested-value"
        )
        task = create_task(self.root, "Check signed source", [source])
        locator = task["sources"][0]["locator"]
        serialized = canonical_json(task)
        self.assertIn("public=paper", locator)
        self.assertEqual(8, locator.count("REDACTED"))
        self.assertNotIn(opaque, serialized)
        self.assertNotIn("account%2Fscope", locator)
        self.assertNotIn("oauth-code", serialized)
        self.assertNotIn("session-value", serialized)
        self.assertNotIn("aws-value", serialized)
        self.assertNotIn("google-value", serialized)
        self.assertNotIn("nested-value", serialized)
        self.assertNotIn("double-nested-value", serialized)

    def test_programmatically_injected_url_credentials_fail_validation(self):
        task = create_task(
            self.root,
            "Check source",
            ["https://example.test/paper?public=yes"],
        )
        task["sources"][0]["locator"] = (
            "https://example.test/paper?public=yes&sessionId=opaque-production-value"
        )
        with self.assertRaisesRegex(StateError, "credential-redacted"):
            validate_task(task)

    def test_embedded_and_adjacent_url_credentials_never_enter_state(self):
        secret = "correct-horse-battery"
        sources = (
            (
                "https://outer.test/callback?redirect="
                f"https://alice:{secret}@inner.test/private"
            ),
            (
                "https://outer.test/callback?next=prefix,"
                f"https://bob:{secret}@inner.test/private"
            ),
        )
        for source in sources:
            with self.subTest(source=source):
                task = create_task(self.root, "Check embedded URL", [source])
                serialized = canonical_json(task)
                self.assertIn("REDACTED", serialized)
                self.assertNotIn(secret, serialized)

        with self.assertRaisesRegex(BlockedError, "embedded credentials") as caught:
            create_task(
                self.root,
                "Check adjacent URL",
                [f"https://safe.test/a,https://alice:{secret}@inner.test/private"],
            )
        self.assertNotIn(secret, str(caught.exception))

        task["sources"][0]["locator"] = (
            "https://example.test/paper?next=x%253Btoken%253Dopaque-production-value"
        )
        with self.assertRaisesRegex(StateError, "credential-redacted"):
            validate_task(task)

    def test_excessively_encoded_url_credentials_fail_closed_before_persistence(self):
        nested = "x;token=supersecretvalue1234567890"
        for _ in range(10):
            nested = urllib.parse.quote(nested, safe="")
        source = "https://outer.test/callback?redirect=" + nested
        with self.assertRaisesRegex(StateError, "decoding depth") as caught:
            create_task(self.root, "Check deeply encoded source", [source])
        self.assertNotIn("supersecretvalue1234567890", str(caught.exception))

    def test_relative_local_source_is_stored_as_an_absolute_path(self):
        source = Path(self.temporary.name) / "relative.pdf"
        source.write_bytes(b"relative source")
        with mock.patch("athena.state.Path.cwd", return_value=source.parent):
            task = create_task(self.root, "Check evidence", [source.name])
        self.assertEqual(str(source.resolve()), task["sources"][0]["locator"])

    def test_source_schema_accepts_only_absolute_paths_or_private_sentinel(self):
        source = Path(self.temporary.name) / "paper.pdf"
        source.write_bytes(b"paper")
        task = create_task(self.root, "Check evidence", [str(source)])
        for locator in (str(source.absolute()), "C:\\papers\\paper.pdf", "/papers/paper.pdf",
                        PRIVATE_SOURCE_LOCATOR):
            with self.subTest(locator=locator):
                task["sources"][0]["locator"] = locator
                validate_task(task)
        for locator in ("paper.pdf", "../paper.pdf", "C:paper.pdf", "/paper\x00.pdf"):
            with self.subTest(locator=locator):
                task["sources"][0]["locator"] = locator
                with self.assertRaisesRegex(StateError, "absolute paths"):
                    validate_task(task)

    def test_every_planned_step_pins_current_instruction_digest(self):
        task = create_task(self.root, "Paper understanding")
        skills_root = Path(__file__).resolve().parents[1] / "skills"
        persisted = load_task(self.root, task["task_id"])
        self.assertEqual(3, len(persisted["steps"]))
        for step in persisted["steps"]:
            with self.subTest(skill=step["skill"]):
                self.assertEqual(sha256_file(skills_root / step["skill"] / "SKILL.md"),
                                 step["instruction_sha256"])

    def test_instruction_drift_blocks_resume_without_mutating_task(self):
        instruction = Path(self.temporary.name) / "SKILL.md"
        instruction.write_bytes(b"Pinned instruction version\n")
        with mock.patch("athena.state._catalog_skill_path", return_value=instruction):
            task = create_task(self.root, "Check evidence", requested_skills=["citation-tracing"])
            before = action_for_task(self.root, task["task_id"])
            task_path = self.root / ".athena" / "tasks" / f"{task['task_id']}.json"
            original_state = task_path.read_bytes()
            instruction.write_bytes(b"Changed instruction version\n")
            with self.assertRaisesRegex(BlockedError, "changed since planning"):
                action_for_task(self.root, task["task_id"])
            self.assertEqual(original_state, task_path.read_bytes())
            instruction.write_bytes(b"Pinned instruction version\n")
            self.assertEqual(before, action_for_task(self.root, task["task_id"]))

    def test_missing_or_invalid_instruction_pin_fails_closed(self):
        task = create_task(self.root, "Check evidence")
        step = task["steps"][0]
        original_pin = step.pop("instruction_sha256")
        with self.assertRaisesRegex(StateError, "missing.*instruction_sha256"):
            validate_task(task)
        for value in (None, "", "abc", "A" * 64, 1):
            with self.subTest(value=value):
                step["instruction_sha256"] = value
                with self.assertRaisesRegex(StateError, "pinned SHA-256"):
                    validate_task(task)
        step["instruction_sha256"] = original_pin
        validate_task(task)

    def test_missing_instruction_blocks_plan_before_writing_state(self):
        project_path = self.root / ".athena" / "project.json"
        before = project_path.read_bytes()
        missing = Path(self.temporary.name) / "missing" / "SKILL.md"
        with mock.patch("athena.state._catalog_skill_path", return_value=missing):
            with self.assertRaisesRegex(BlockedError, "instructions are unavailable"):
                create_task(self.root, "Check evidence")
        self.assertEqual(before, project_path.read_bytes())
        self.assertEqual([], list((self.root / ".athena" / "tasks").iterdir()))

    def test_blocked_task_and_step_cannot_resume_or_checkpoint(self):
        task = create_task(
            self.root,
            "Check evidence",
            task_id="tsk_000000000009",
            now="2026-01-01T00:01:00Z",
        )
        task["status"] = "blocked"
        task["steps"][0]["status"] = "blocked"
        task["steps"][0]["note"] = "Waiting for a trusted source."
        validate_task(task)
        task_path = self.root / ".athena" / "tasks" / f"{task['task_id']}.json"
        atomic_write_json(task_path, task)
        before = task_path.read_bytes()
        artifact = Path(self.temporary.name) / "result.md"
        artifact.write_text("must not be registered\n", encoding="utf-8")

        with self.assertRaisesRegex(BlockedError, "blocked at step"):
            action_for_task(self.root, task["task_id"])
        with self.assertRaisesRegex(BlockedError, "blocked at step"):
            checkpoint_task(
                self.root,
                task["task_id"],
                task["steps"][0]["step_id"],
                artifact=artifact,
                expected_revision=0,
            )

        self.assertEqual(before, task_path.read_bytes())
        artifact_root = self.root / ".athena" / "artifacts" / task["task_id"]
        self.assertFalse(artifact_root.exists())

    def _create_directory_link(self, link: Path, target: Path):
        if os.name == "nt":
            quoted_link = str(link).replace("'", "''")
            quoted_target = str(target).replace("'", "''")
            result = subprocess.run(
                ["powershell", "-NoProfile", "-NonInteractive", "-Command",
                 "$ErrorActionPreference = 'Stop'; New-Item -ItemType Junction "
                 f"-Path '{quoted_link}' -Target '{quoted_target}' | Out-Null"],
                capture_output=True, text=True,
            )
            if result.returncode:
                self.skipTest(f"junction creation failed: {result.stderr.strip()}")
        else:
            try:
                link.symlink_to(target, target_is_directory=True)
            except (OSError, NotImplementedError) as exc:
                self.skipTest(f"directory symlink creation failed: {exc}")

    def test_parent_alias_policy_is_platform_specific(self):
        self.assertEqual("reject", state_module._parent_alias_policy("nt"))
        self.assertEqual("canonicalize", state_module._parent_alias_policy("posix"))
        self.assertEqual("reject", state_module._parent_alias_policy("unknown"))

    def test_stable_parent_path_collapses_dot_segments_without_resolving_links(self):
        disguised = self.root / "missing" / ".."
        self.assertEqual(self.root, state_module._path_with_stable_parents(disguised))

    @unittest.skipUnless(os.name == "nt", "Windows junction policy regression")
    def test_project_root_parent_junction_cannot_redirect_task_creation(self):
        real_parent = Path(self.temporary.name) / "real-project-parent"
        real_root = real_parent / "project"
        init_project(
            real_root,
            "Junction target",
            now="2026-01-01T00:00:00Z",
            project_id="prj_000000000002",
        )
        alias = Path(self.temporary.name) / "project-parent-alias"
        self._create_directory_link(alias, real_parent)
        alias_root = alias / "project"
        project_before = (real_root / ".athena" / "project.json").read_bytes()

        with self.assertRaisesRegex(BlockedError, "link|reparse"):
            create_task(
                alias_root,
                "Check evidence",
                task_id="tsk_000000000099",
            )

        self.assertEqual(project_before,
                         (real_root / ".athena" / "project.json").read_bytes())
        self.assertFalse(
            (real_root / ".athena" / "tasks" / "tsk_000000000099.json").exists()
        )

    @unittest.skipIf(os.name == "nt", "POSIX parent-alias canonicalization regression")
    def test_posix_project_root_parent_alias_is_canonicalized(self):
        real_parent = Path(self.temporary.name).resolve() / "real-posix-parent"
        real_root = real_parent / "project"
        init_project(
            real_root,
            "POSIX alias target",
            now="2026-01-01T00:00:00Z",
            project_id="prj_000000000003",
        )
        alias = Path(self.temporary.name).resolve() / "posix-parent-alias"
        self._create_directory_link(alias, real_parent)
        alias_root = alias / "project"

        task = create_task(
            alias_root,
            "Check evidence",
            task_id="tsk_000000000098",
        )

        self.assertEqual(task, load_task(real_root, task["task_id"]))
        self.assertTrue(
            (real_root / ".athena" / "tasks" / "tsk_000000000098.json").is_file()
        )

    def test_artifact_ancestor_junction_cannot_redirect_checkpoint(self):
        task = create_task(self.root, "Check evidence")
        outside = Path(self.temporary.name) / "outside-artifacts"
        outside.mkdir()
        link = self.root / ".athena" / "artifacts" / task["task_id"]
        self._create_directory_link(link, outside)
        artifact = Path(self.temporary.name) / "result.md"
        artifact.write_text("result\n", encoding="utf-8")
        with self.assertRaisesRegex(BlockedError, "link|reparse"):
            checkpoint_task(self.root, task["task_id"], task["steps"][0]["step_id"],
                            artifact=artifact)
        self.assertEqual([], list(outside.iterdir()))
        self.assertEqual(task, load_task(self.root, task["task_id"]))

    def test_tasks_ancestor_junction_blocks_reads_and_writes(self):
        task = create_task(self.root, "Check evidence")
        tasks_path = self.root / ".athena" / "tasks"
        outside = Path(self.temporary.name) / "outside-tasks"
        tasks_path.rename(outside)
        self._create_directory_link(tasks_path, outside)
        before = {path.name: path.read_bytes() for path in outside.iterdir()}
        for operation in (
            lambda: load_task(self.root, task["task_id"]),
            lambda: project_status(self.root),
            lambda: create_task(self.root, "Check evidence"),
        ):
            with self.subTest(operation=operation):
                with self.assertRaisesRegex(BlockedError, "link|reparse"):
                    operation()
        self.assertEqual(before, {path.name: path.read_bytes() for path in outside.iterdir()})

    def test_old_live_lock_is_never_stolen(self):
        lock_path = self.root / ".athena" / ".write-lock"
        with project_lock(self.root):
            original_lock = lock_path.read_bytes()
            os.utime(lock_path, (0, 0))
            with self.assertRaisesRegex(ConflictError, "Another Athena process"):
                with project_lock(self.root, timeout=0.01):
                    self.fail("A live lock must not be stolen based on its age")
            self.assertTrue(lock_path.exists())
            self.assertEqual(original_lock, lock_path.read_bytes())
        self.assertFalse(lock_path.exists())

    def test_failed_lock_flush_does_not_leave_a_stale_lock(self):
        lock_path = self.root / ".athena" / ".write-lock"
        with mock.patch("athena.state.os.fsync", side_effect=OSError("disk flush failed")):
            with self.assertRaisesRegex(OSError, "disk flush failed"):
                with project_lock(self.root):
                    self.fail("Lock acquisition must fail before entering the critical section")
        self.assertFalse(lock_path.exists())

    def test_unverifiable_lock_cleanup_is_reported_as_ambiguous(self):
        lock_path = self.root / ".athena" / ".write-lock"
        try:
            with mock.patch(
                "athena.state.read_json",
                side_effect=StateError("simulated unreadable lock"),
            ):
                with self.assertRaisesRegex(StateError, "may have completed"):
                    with project_lock(self.root):
                        pass
            self.assertTrue(lock_path.exists())
        finally:
            if lock_path.exists():
                lock_path.unlink()

    def test_task_filename_and_embedded_identity_must_agree(self):
        first = create_task(self.root, "Check evidence", task_id="tsk_000000000010")
        second = create_task(self.root, "Check evidence", task_id="tsk_000000000011")
        first_path = self.root / ".athena" / "tasks" / f"{first['task_id']}.json"
        atomic_write_json(first_path, second)
        before = first_path.read_bytes()
        for operation in (
            lambda: load_task(self.root, first["task_id"]),
            lambda: project_status(self.root),
            lambda: action_for_task(self.root, first["task_id"]),
            lambda: checkpoint_task(self.root, first["task_id"], first["steps"][0]["step_id"]),
        ):
            with self.subTest(operation=operation):
                with self.assertRaisesRegex(StateError, "identity"):
                    operation()
        self.assertEqual(before, first_path.read_bytes())
        self.assertEqual(second, load_task(self.root, second["task_id"]))

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

    def test_artifact_references_must_match_their_owning_step(self):
        task = create_task(
            self.root,
            "Trace citations and create explorable HTML",
            now="2026-01-01T00:01:00Z",
            task_id="tsk_000000000006",
        )
        artifact = Path(self.temporary.name) / "citations.md"
        artifact.write_text("# Citations\n", encoding="utf-8")
        task = checkpoint_task(
            self.root,
            task["task_id"],
            "01-citation-tracing",
            artifact=artifact,
            now="2026-01-01T00:02:00Z",
        )
        artifact_id = task["artifacts"][0]["artifact_id"]
        task["steps"][0]["artifact_ids"] = []
        task["steps"][1]["artifact_ids"] = [artifact_id]
        with self.assertRaisesRegex(StateError, "owned by another step"):
            validate_task(task)

        task["steps"][1]["artifact_ids"] = []
        with self.assertRaisesRegex(StateError, "Every artifact"):
            validate_task(task)

    def test_artifact_change_during_copy_does_not_advance_task(self):
        task = create_task(
            self.root,
            "Trace citations",
            now="2026-01-01T00:01:00Z",
            task_id="tsk_000000000008",
        )
        artifact = Path(self.temporary.name) / "citations.md"
        artifact.write_text("original\n", encoding="utf-8")

        def copy_changed(_source: Path, destination: Path) -> None:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text("changed while copying\n", encoding="utf-8")

        with mock.patch("athena.state._copy_artifact_atomic", side_effect=copy_changed):
            with self.assertRaisesRegex(ConflictError, "changed while"):
                checkpoint_task(
                    self.root,
                    task["task_id"],
                    "01-citation-tracing",
                    artifact=artifact,
                    expected_revision=0,
                )

        unchanged = load_task(self.root, task["task_id"])
        self.assertEqual(0, unchanged["revision"])
        self.assertEqual([], unchanged["artifacts"])
        artifact_dir = self.root / ".athena" / "artifacts" / task["task_id"]
        self.assertFalse(artifact_dir.exists() and any(path.is_file() for path in artifact_dir.rglob("*")))

    def test_invalid_programmatic_skill_request_is_blocked(self):
        with self.assertRaisesRegex(Exception, "unsupported core skill"):
            create_task(
                self.root,
                "Run arbitrary code",
                requested_skills=["shell-executor"],
                task_id="tsk_000000000007",
            )

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
        try:
            link.symlink_to(target)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"symlink creation failed: {exc}")
        with self.assertRaises(BlockedError):
            checkpoint_task(self.root, task["task_id"], task["steps"][0]["step_id"], artifact=link)


if __name__ == "__main__":
    unittest.main()
