from __future__ import annotations

import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from athena.release import (
    LOCAL_SOURCE_LOCATOR,
    ReleaseError,
    SecretDetectedError,
    _assert_text_has_no_local_path,
    export_release,
    verify_release,
)
from athena.state import (
    BlockedError,
    ConflictError,
    atomic_write_text,
    canonical_json,
    checkpoint_task,
    create_task,
    init_project,
    read_json,
)


NOW = "2026-01-02T03:04:05Z"
TASK_ID = "tsk_012345abcdef"
PROJECT_ID = "prj_012345abcdef"


class ResearchReleaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = self._new_project()

    def _new_project(self) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name) / "project"
        init_project(root, "Release test", now=NOW, project_id=PROJECT_ID)
        return root

    def _reset_project(self) -> None:
        self.root = self._new_project()

    def _planned(
        self,
        task_id: str = TASK_ID,
        sources=(),
        *,
        goal: str = "What does the recorded evidence support?",
    ):
        return create_task(
            self.root,
            goal,
            sources,
            requested_skills=["research-integrity-pipeline"],
            now=NOW,
            task_id=task_id,
        )

    def _completed(
        self,
        content: str = "# Finding\n\nEvidence-linked result.\n",
        sources=(),
        *,
        goal: str = "What does the recorded evidence support?",
        note: str | None = None,
    ):
        task = self._planned(sources=sources, goal=goal)
        source = self.root / "finding.md"
        atomic_write_text(source, content)
        return checkpoint_task(
            self.root,
            task["task_id"],
            task["steps"][0]["step_id"],
            artifact=source,
            note=note,
            now=NOW,
        )

    def _exported(self):
        task = self._completed()
        result = export_release(self.root, task["task_id"], "1.2.0-alpha.1", now=NOW)
        return task, result, Path(result["release_path"])

    def _reseal_release_file(self, release: Path, relative: str) -> Path:
        changed = release / Path(*relative.split("/"))
        payload = changed.read_bytes()
        manifest_path = release / "manifest.json"
        manifest = read_json(manifest_path)
        entry = next(item for item in manifest["files"] if item["path"] == relative)
        entry["bytes"] = len(payload)
        entry["sha256"] = hashlib.sha256(payload).hexdigest()
        for artifact in manifest["artifacts"]:
            if artifact["path"] == relative:
                artifact["bytes"] = len(payload)
                artifact["sha256"] = entry["sha256"]
        atomic_write_text(manifest_path, canonical_json(manifest))
        core_sha256 = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
        envelope_path = release / "release.json"
        envelope = read_json(envelope_path)
        envelope["core_sha256"] = core_sha256
        atomic_write_text(envelope_path, canonical_json(envelope))
        destination = release.with_name(f"{manifest['release_version']}-{core_sha256[:12]}")
        if destination != release:
            release.rename(destination)
        return destination

    def test_happy_path_is_private_content_addressed_and_verifiable(self) -> None:
        task, result, release = self._exported()
        self.assertTrue(result["created"])
        self.assertTrue(result["verified"])
        self.assertEqual(result["visibility"], "private-local-draft")
        self.assertRegex(release.name, r"^1\.2\.0-alpha\.1-[0-9a-f]{12}$")
        self.assertTrue((release / "README.md").is_file())
        self.assertTrue((release / "task.json").is_file())
        self.assertTrue((release / "manifest.json").is_file())
        self.assertTrue((release / "release.json").is_file())
        self.assertEqual(verify_release(release)["task_id"], task["task_id"])

    @unittest.skipIf(os.name == "nt", "POSIX parent-alias canonicalization regression")
    def test_verifier_accepts_canonicalized_posix_parent_alias(self) -> None:
        _, _, release = self._exported()
        alias = release.parent.parent.parent / "release-parent-alias"
        try:
            alias.symlink_to(release.parent, target_is_directory=True)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"directory symlink creation failed: {exc}")
        result = verify_release(alias / release.name)
        self.assertTrue(result["verified"])
        self.assertEqual(str(release.resolve()), result["release_path"])

    def test_local_source_locator_is_redacted_and_verifier_enforces_sentinel(self) -> None:
        source_directory = self.root.parent / "local-source-location"
        source_directory.mkdir()
        source = source_directory / "private-paper.pdf"
        source.write_bytes(b"local source bytes")
        task = self._completed(sources=[str(source)])
        result = export_release(self.root, task["task_id"], "1.0.0", now=NOW)
        release = Path(result["release_path"])
        snapshot_path = release / "task.json"
        snapshot = read_json(snapshot_path)
        self.assertEqual(LOCAL_SOURCE_LOCATOR, snapshot["sources"][0]["locator"])
        release_bytes = b"".join(
            path.read_bytes() for path in release.rglob("*") if path.is_file()
        )
        self.assertNotIn(str(source.resolve()).encode("utf-8"), release_bytes)
        self.assertNotIn(str(source_directory.resolve()).encode("utf-8"), release_bytes)
        self.assertTrue(verify_release(release)["verified"])

        snapshot["sources"][0]["locator"] = str(source.resolve())
        atomic_write_text(snapshot_path, canonical_json(snapshot))
        release = self._reseal_release_file(release, "task.json")
        with self.assertRaisesRegex(ReleaseError, "redacted sentinel|absolute-looking"):
            verify_release(release)

    def test_records_are_filtered_to_task_and_verifier_rejects_foreign_task(self) -> None:
        task = self._completed()
        foreign_task_id = "tsk_fedcba654321"
        records = (
            {"task_id": foreign_task_id, "claim": "foreign-only"},
            {"task_id": task["task_id"], "claim": "selected"},
        )
        claims = self.root / ".athena" / "claims.jsonl"
        claims.write_text(
            "".join(
                json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n"
                for record in records
            ),
            encoding="utf-8",
            newline="\n",
        )
        result = export_release(self.root, task["task_id"], "1.0.0", now=NOW)
        release = Path(result["release_path"])
        released_claims = release / "records" / "claims.jsonl"
        released_records = [
            json.loads(line) for line in released_claims.read_text("utf-8").splitlines()
        ]
        self.assertEqual([task["task_id"]], [record["task_id"] for record in released_records])
        self.assertNotIn("foreign-only", released_claims.read_text("utf-8"))
        self.assertTrue(verify_release(release)["verified"])

        released_claims.write_text(
            json.dumps(records[0], sort_keys=True, separators=(",", ":")) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        release = self._reseal_release_file(release, "records/claims.jsonl")
        with self.assertRaisesRegex(ReleaseError, "another task"):
            verify_release(release)

    def test_records_fail_closed_on_missing_or_invalid_binding_and_strict_json(self) -> None:
        cases = (
            ("missing-task", '{"claim":"missing"}\n', "task_id"),
            ("wrong-task-type", '{"task_id":123}\n', "task_id"),
            ("invalid-task-id", '{"task_id":"not-a-task"}\n', "task_id"),
            ("malformed", '{"task_id":', "invalid JSON"),
            (
                "duplicate-key",
                f'{{"task_id":"{TASK_ID}","task_id":"{TASK_ID}"}}\n',
                "duplicate JSON key",
            ),
            ("non-finite", f'{{"task_id":"{TASK_ID}","score":NaN}}\n', "non-finite"),
            ("overflow-float", f'{{"task_id":"{TASK_ID}","score":1e999}}\n', "non-finite"),
            (
                "nested-overflow-float",
                f'{{"task_id":"{TASK_ID}","nested":{{"score":-1e999}}}}\n',
                "non-finite",
            ),
        )
        for name, payload, message in cases:
            with self.subTest(case=name):
                self._reset_project()
                task = self._completed()
                claims = self.root / ".athena" / "claims.jsonl"
                claims.write_text(payload, encoding="utf-8", newline="\n")
                with self.assertRaisesRegex(ReleaseError, message):
                    export_release(self.root, task["task_id"], "1.0.0", now=NOW)

    def test_foreign_task_non_finite_record_is_still_rejected(self) -> None:
        task = self._completed()
        claims = self.root / ".athena" / "claims.jsonl"
        claims.write_text(
            '{"task_id":"tsk_fedcba654321","score":1e999}\n'
            + json.dumps({"task_id": task["task_id"], "claim": "selected"})
            + "\n",
            encoding="utf-8",
            newline="\n",
        )
        with self.assertRaisesRegex(ReleaseError, "non-finite"):
            export_release(self.root, task["task_id"], "1.0.0", now=NOW)

    def test_records_fail_closed_before_decimal_precision_can_be_lost(self) -> None:
        for name, number in (
            ("long-decimal", "0.123456789012345678901"),
            ("underflow", "1e-400"),
        ):
            with self.subTest(case=name):
                self._reset_project()
                task = self._completed()
                claims = self.root / ".athena" / "claims.jsonl"
                claims.write_text(
                    f'{{"task_id":"{task["task_id"]}","score":{number}}}\n',
                    encoding="utf-8",
                    newline="\n",
                )
                with self.assertRaisesRegex(ReleaseError, "lose decimal precision"):
                    export_release(self.root, task["task_id"], "1.0.0", now=NOW)

        self._reset_project()
        _, _, release = self._exported()
        claims = release / "records" / "claims.jsonl"
        claims.write_text(
            f'{{"task_id":"{TASK_ID}","score":0.123456789012345678901}}\n',
            encoding="utf-8",
            newline="\n",
        )
        release = self._reseal_release_file(release, "records/claims.jsonl")
        with self.assertRaisesRegex(ReleaseError, "lose decimal precision"):
            verify_release(release)

    def test_records_reject_unencodable_unicode_surrogates_on_export_and_verify(self) -> None:
        task = self._completed()
        payload = (
            f'{{"task_id":"{task["task_id"]}","text":"\\uD800"}}\n'
        ).encode("ascii")
        claims = self.root / ".athena" / "claims.jsonl"
        claims.write_bytes(payload)
        with self.assertRaisesRegex(ReleaseError, "Unicode surrogate"):
            export_release(self.root, task["task_id"], "1.0.0", now=NOW)

        self._reset_project()
        _, _, release = self._exported()
        claims = release / "records" / "claims.jsonl"
        claims.write_bytes(
            f'{{"task_id":"{TASK_ID}","text":"\\uD800"}}\n'.encode("ascii")
        )
        release = self._reseal_release_file(release, "records/claims.jsonl")
        with self.assertRaisesRegex(ReleaseError, "Unicode surrogate"):
            verify_release(release)

    def test_decoded_assigned_secrets_are_blocked_on_export_and_verify(self) -> None:
        secret = "correct-horse-battery"
        task = self._completed(note=f'password = "{secret}"')
        with self.assertRaises(SecretDetectedError) as caught:
            export_release(self.root, task["task_id"], "1.0.0", now=NOW)
        self.assertNotIn(secret, str(caught.exception))

        self._reset_project()
        task = self._completed()
        claims = self.root / ".athena" / "claims.jsonl"
        claims.write_text(
            json.dumps(
                {"task_id": task["task_id"], "note": f'password = "{secret}"'},
                sort_keys=True,
                separators=(",", ":"),
            )
            + "\n",
            encoding="utf-8",
            newline="\n",
        )
        with self.assertRaises(SecretDetectedError) as caught:
            export_release(self.root, task["task_id"], "1.0.0", now=NOW)
        self.assertNotIn(secret, str(caught.exception))

        self._reset_project()
        _, _, release = self._exported()
        snapshot_path = release / "task.json"
        snapshot = read_json(snapshot_path)
        snapshot["steps"][0]["note"] = f'password = "{secret}"'
        atomic_write_text(snapshot_path, canonical_json(snapshot))
        release = self._reseal_release_file(release, "task.json")
        with self.assertRaises(SecretDetectedError) as caught:
            verify_release(release)
        self.assertNotIn(secret, str(caught.exception))

    def test_json_escaped_assigned_secrets_are_blocked_everywhere(self) -> None:
        secret = "escaped-production-password"
        escaped = f'password = \\"{secret}\\"'

        task = self._completed(note=escaped)
        with self.assertRaises(SecretDetectedError) as caught:
            export_release(self.root, task["task_id"], "1.0.0", now=NOW)
        self.assertNotIn(secret, str(caught.exception))

        self._reset_project()
        task = self._completed()
        claims = self.root / ".athena" / "claims.jsonl"
        claims.write_text(
            json.dumps(
                {"task_id": task["task_id"], "note": escaped},
                sort_keys=True,
                separators=(",", ":"),
            )
            + "\n",
            encoding="utf-8",
            newline="\n",
        )
        with self.assertRaises(SecretDetectedError) as caught:
            export_release(self.root, task["task_id"], "1.0.0", now=NOW)
        self.assertNotIn(secret, str(caught.exception))

        self._reset_project()
        task = self._completed(content=escaped)
        with self.assertRaises(SecretDetectedError) as caught:
            export_release(self.root, task["task_id"], "1.0.0", now=NOW)
        self.assertNotIn(secret, str(caught.exception))

        self._reset_project()
        _, _, release = self._exported()
        snapshot_path = release / "task.json"
        snapshot = read_json(snapshot_path)
        snapshot["steps"][0]["note"] = escaped
        atomic_write_text(snapshot_path, canonical_json(snapshot))
        release = self._reseal_release_file(release, "task.json")
        with self.assertRaises(SecretDetectedError) as caught:
            verify_release(release)
        self.assertNotIn(secret, str(caught.exception))

    def test_json_short_escaped_secret_is_blocked_in_artifacts_and_verify(self) -> None:
        secret = "correct-horse-battery"
        payload = json.dumps(
            {"note": f'password\t=\t"{secret}"'},
            separators=(",", ":"),
        ) + "\n"
        task = self._completed(content=payload)
        with self.assertRaises(SecretDetectedError) as caught:
            export_release(self.root, task["task_id"], "1.0.0", now=NOW)
        self.assertNotIn(secret, str(caught.exception))

        self._reset_project()
        _, _, release = self._exported()
        manifest = read_json(release / "manifest.json")
        artifact_relative = next(
            entry["path"] for entry in manifest["files"] if entry["role"] == "artifact"
        )
        artifact_path = release / Path(*artifact_relative.split("/"))
        artifact_path.write_text(payload, encoding="utf-8")
        release = self._reseal_release_file(release, artifact_relative)
        with self.assertRaises(SecretDetectedError) as caught:
            verify_release(release)
        self.assertNotIn(secret, str(caught.exception))

    def test_excessively_nested_escape_encoding_fails_closed(self) -> None:
        payload = r"api_key\u003dexamplevalue"
        for _ in range(12):
            payload = payload.replace("\\", r"\u005c")

        task = self._completed(content=payload)
        with self.assertRaisesRegex(SecretDetectedError, "nested escape encoding"):
            export_release(self.root, task["task_id"], "1.0.0", now=NOW)

        self._reset_project()
        _, _, release = self._exported()
        manifest = read_json(release / "manifest.json")
        artifact_relative = next(
            entry["path"] for entry in manifest["files"] if entry["role"] == "artifact"
        )
        artifact_path = release / Path(*artifact_relative.split("/"))
        artifact_path.write_text(payload, encoding="utf-8")
        release = self._reseal_release_file(release, artifact_relative)
        with self.assertRaisesRegex(SecretDetectedError, "nested escape encoding"):
            verify_release(release)

    def test_absolute_local_metadata_paths_are_blocked_but_http_urls_are_allowed(self) -> None:
        private_path = str((self.root.parent / "private" / "paper.pdf").resolve())
        blocked_values = (
            private_path,
            "C:\\Users\\Alice\\private.pdf",
            "/home/alice/private.pdf",
            "file:///C:/Users/Alice/private.pdf",
            "FiLe%3A%2F%2F%2Fhome%2Falice%2Fprivate.pdf",
            "path:/home/alice/private.pdf",
            "C%2525253A%2525252FUsers%2525252FAlice%2525252Fprivate.pdf",
            "%2525252Fhome%2525252Falice%2525252Fprivate.pdf",
            "file%2525253A%2525252F%2525252F%2525252Fhome%2525252Falice%2525252Fprivate.pdf",
            "https://example.test/callback?next=/home/alice/private.pdf",
            "https://example.test/callback?next=C%3A%5CUsers%5CAlice%5Cprivate.pdf",
            "https://example.test/callback?next=file%3A%2F%2F%2Fhome%2Falice%2Fprivate.pdf",
            "https://example.test/callback?next=%2525252Fhome%2525252Falice%2525252Fprivate.pdf",
            "https://example.test/#route=/home/alice/private.pdf",
            "https://safe.test/a,/home/alice/private.pdf",
            "https://safe.test/a;C:\\Users\\Alice\\private.pdf",
            "https://safe.test/a)/home/alice/private.pdf",
            "https://safe.test/a]|/home/alice/private.pdf",
            "Reference `https://safe.test/a`/home/alice/private.pdf",
            "Reference `https://safe.test/a`C:\\Users\\Alice\\private.pdf",
            "https:///home/alice/private.pdf",
            "https:///C:/Users/Alice/private.pdf",
            "https://localhost/C:/Users/Alice/private.pdf",
            (
                "https://outer.test/callback?redirect="
                "https://inner.test/?next=/home/alice/private.pdf"
            ),
        )
        for value in blocked_values:
            with self.subTest(value=value):
                self._reset_project()
                task = self._completed(goal=f"Review {value}")
                with self.assertRaisesRegex(
                    ReleaseError,
                    "local file URI|absolute-looking|malformed HTTP",
                ):
                    export_release(self.root, task["task_id"], "1.0.0", now=NOW)

        self._reset_project()
        task = self._completed(goal="Review https://example.org/papers/private.pdf")
        result = export_release(self.root, task["task_id"], "1.0.0", now=NOW)
        self.assertTrue(verify_release(result["release_path"])["verified"])

    def test_markdown_url_delimiter_cannot_hide_a_local_path(self) -> None:
        values = (
            "Reference `https://safe.test/a`/home/alice/private.pdf",
            "Reference `https://safe.test/a`C:\\Users\\Alice\\private.pdf",
        )
        for value in values:
            with self.subTest(value=value, layer="direct"):
                with self.assertRaisesRegex(ReleaseError, "absolute-looking"):
                    _assert_text_has_no_local_path(value, "test metadata")
            with self.subTest(value=value, layer="export"):
                self._reset_project()
                task = self._completed(goal=value)
                with self.assertRaisesRegex(ReleaseError, "absolute-looking"):
                    export_release(self.root, task["task_id"], "1.0.0", now=NOW)

    def test_signed_urls_are_blocked_in_metadata_records_artifacts_and_verify(self) -> None:
        signed_urls = (
            "https://example.test/download?sig=opaque-production-credential-1234567890",
            "https://example.test/download?code=oauth-production-code-1234567890",
            "https://example.test/download?sessionId=session-production-value",
            "https://example.test/download?X-Amz-Credential=account%2Fscope",
            "https://example.test/download?callback=x%253BaccessToken%253Dnested-value",
            (
                "https://outer.test/callback?redirect="
                "https://alice:supersecretpassword@inner.test/private"
            ),
            (
                "https://safe.test/a,"
                "https://alice:correct-horse-battery@inner.test/private"
            ),
            (
                "https://safe.test/a;"
                "https://alice:correct-horse-battery@inner.test/private"
            ),
            "https://alice:correct-horse-battery@",
            "https://alice:correct-horse-battery@/private",
            "https:///alice:correct-horse-battery@/private",
        )
        for index, signed_url in enumerate(signed_urls):
            with self.subTest(location="goal", index=index):
                self._reset_project()
                task = self._completed(goal=f"Review {signed_url}")
                with self.assertRaises(SecretDetectedError):
                    export_release(self.root, task["task_id"], "1.0.0", now=NOW)

        self._reset_project()
        task = self._completed()
        claims = self.root / ".athena" / "claims.jsonl"
        claims.write_text(
            json.dumps(
                {"task_id": task["task_id"], "url": signed_urls[0]},
                sort_keys=True,
                separators=(",", ":"),
            )
            + "\n",
            encoding="utf-8",
            newline="\n",
        )
        with self.assertRaises(SecretDetectedError):
            export_release(self.root, task["task_id"], "1.0.0", now=NOW)

        self._reset_project()
        task = self._planned()
        artifact = self.root / "signed-url.md"
        artifact.write_text(f"Download: {signed_urls[0]}\n", encoding="utf-8")
        checkpoint_task(
            self.root,
            task["task_id"],
            task["steps"][0]["step_id"],
                artifact=artifact,
            now=NOW,
        )
        with self.assertRaises(SecretDetectedError):
            export_release(self.root, task["task_id"], "1.0.0", now=NOW)

        self._reset_project()
        _, _, release = self._exported()
        snapshot_path = release / "task.json"
        snapshot = read_json(snapshot_path)
        snapshot["goal"] = f"Review {signed_urls[0]}"
        atomic_write_text(snapshot_path, canonical_json(snapshot))
        release = self._reseal_release_file(release, "task.json")
        with self.assertRaises(SecretDetectedError):
            verify_release(release)

    def test_overlong_url_like_artifact_fails_closed_on_export_and_verify(self) -> None:
        overlong = "https://example.test/" + ("a" * 70_000)
        task = self._completed(content=overlong)
        with self.assertRaisesRegex(SecretDetectedError, "overlong URL-like token"):
            export_release(self.root, task["task_id"], "1.0.0", now=NOW)

        self._reset_project()
        _, _, release = self._exported()
        manifest = read_json(release / "manifest.json")
        artifact_relative = next(
            entry["path"] for entry in manifest["files"] if entry["role"] == "artifact"
        )
        artifact_path = release / Path(*artifact_relative.split("/"))
        artifact_path.write_text(overlong, encoding="utf-8")
        release = self._reseal_release_file(release, artifact_relative)
        with self.assertRaisesRegex(SecretDetectedError, "overlong URL-like token"):
            verify_release(release)

    def test_utf_encoded_secrets_and_chunk_boundaries_fail_closed(self) -> None:
        secret_text = "password=correct-horse-battery"
        payloads = (
            secret_text.encode("utf-16"),
            secret_text.encode("utf-16-le"),
            secret_text.encode("utf-16-be"),
            secret_text.encode("utf-32"),
        )
        for index, payload in enumerate(payloads):
            with self.subTest(encoding=index):
                self._reset_project()
                task = self._planned()
                artifact = self.root / f"encoded-{index}.bin"
                artifact.write_bytes(payload)
                task = checkpoint_task(
                    self.root,
                    task["task_id"],
                    task["steps"][0]["step_id"],
                    artifact=artifact,
                    now=NOW,
                )
                with self.assertRaises(SecretDetectedError):
                    export_release(self.root, task["task_id"], "1.0.0", now=NOW)

        for prefix_bytes in (4096, 20_000, (1024 * 1024) - 10):
            with self.subTest(mixed_prefix=prefix_bytes):
                self._reset_project()
                task = self._planned()
                artifact = self.root / "mixed-prefix.bin"
                artifact.write_bytes(
                    b"A" * prefix_bytes + secret_text.encode("utf-16-le")
                )
                task = checkpoint_task(
                    self.root,
                    task["task_id"],
                    task["steps"][0]["step_id"],
                    artifact=artifact,
                    now=NOW,
                )
                with self.assertRaises(SecretDetectedError):
                    export_release(self.root, task["task_id"], "1.0.0", now=NOW)

        self._reset_project()
        task = self._planned()
        artifact = self.root / "boundary.bin"
        prefix_characters = ((1024 * 1024) - 2) // 2 - 5
        artifact.write_bytes(
            (("A" * prefix_characters) + secret_text).encode("utf-16")
        )
        task = checkpoint_task(
            self.root,
            task["task_id"],
            task["steps"][0]["step_id"],
            artifact=artifact,
            now=NOW,
        )
        with self.assertRaises(SecretDetectedError):
            export_release(self.root, task["task_id"], "1.0.0", now=NOW)

        self._reset_project()
        _, _, release = self._exported()
        manifest = read_json(release / "manifest.json")
        artifact_relative = next(
            entry["path"] for entry in manifest["files"] if entry["role"] == "artifact"
        )
        artifact_path = release / Path(*artifact_relative.split("/"))
        artifact_path.write_bytes(b"A" * 4096 + secret_text.encode("utf-16-le"))
        release = self._reseal_release_file(release, artifact_relative)
        with self.assertRaises(SecretDetectedError):
            verify_release(release)

    def test_verifier_rejects_resealed_absolute_path_in_task_metadata(self) -> None:
        _, _, release = self._exported()
        snapshot_path = release / "task.json"
        snapshot = read_json(snapshot_path)
        snapshot["goal"] = "Review C:\\Users\\Alice\\private.pdf"
        atomic_write_text(snapshot_path, canonical_json(snapshot))
        release = self._reseal_release_file(release, "task.json")
        with self.assertRaisesRegex(ReleaseError, "absolute-looking"):
            verify_release(release)

    def test_incomplete_task_and_completed_task_without_artifact_are_blocked(self) -> None:
        task = self._planned()
        with self.assertRaises(BlockedError):
            export_release(self.root, task["task_id"], "1.0.0", now=NOW)
        checkpoint_task(
            self.root,
            task["task_id"],
            task["steps"][0]["step_id"],
            now=NOW,
        )
        with self.assertRaises(BlockedError):
            export_release(self.root, task["task_id"], "1.0.0", now=NOW)

    def test_registered_artifact_must_still_match_checkpoint_hash(self) -> None:
        task = self._completed()
        relative = task["artifacts"][0]["relative_path"]
        artifact = self.root / ".athena" / Path(*relative.split("/"))
        artifact.write_text("changed", encoding="utf-8")
        with self.assertRaises(ConflictError) as caught:
            export_release(self.root, task["task_id"], "1.0.0", now=NOW)
        self.assertIn("changed after checkpoint", str(caught.exception))

    def test_tamper_and_unexpected_file_fail_closed(self) -> None:
        _, _, release = self._exported()
        readme = release / "README.md"
        readme.write_text(readme.read_text(encoding="utf-8") + "tamper\n", encoding="utf-8")
        with self.assertRaises(ReleaseError):
            verify_release(release)

        # Restore by making a separate release in a fresh project fixture.
        self._reset_project()
        _, _, release = self._exported()
        (release / "extra.txt").write_text("unexpected", encoding="utf-8")
        with self.assertRaises(ReleaseError):
            verify_release(release)

    def test_release_envelope_creation_time_is_hash_bound(self) -> None:
        _, _, release = self._exported()
        envelope_path = release / "release.json"
        envelope = read_json(envelope_path)
        envelope["created_at"] = "2099-01-01T00:00:00Z"
        atomic_write_text(envelope_path, canonical_json(envelope))
        with self.assertRaisesRegex(ReleaseError, "creation time"):
            verify_release(release)

    def test_signed_url_secrets_do_not_enter_release_snapshot(self) -> None:
        secrets = (
            "opaque-production-credential-1234567890",
            "opaque-session-credential-1234567890",
            "opaque-aws-credential-1234567890",
            "opaque-nested-credential-1234567890",
        )
        source = (
            f"https://example.test/download?sig={secrets[0]}&public=paper"
            f"&sessionId={secrets[1]}&AWSAccessKeyId={secrets[2]}"
            f"&callback=x%253BaccessToken%253D{secrets[3]}"
        )
        task = self._completed(sources=[source])
        result = export_release(self.root, task["task_id"], "1.0.0", now=NOW)
        snapshot_bytes = (Path(result["release_path"]) / "task.json").read_bytes()
        for secret in secrets:
            self.assertNotIn(secret.encode("utf-8"), snapshot_bytes)
        self.assertIn(b"REDACTED", snapshot_bytes)
        self.assertTrue(verify_release(result["release_path"])["verified"])

    def test_jsonl_unicode_line_separator_round_trips(self) -> None:
        task = self._completed()
        claims = self.root / ".athena" / "claims.jsonl"
        claims.write_text(
            '{"task_id":"'
            + task["task_id"]
            + '","claim":"before'
            + chr(0x2028)
            + 'after"}\n',
            encoding="utf-8",
            newline="\n",
        )
        result = export_release(self.root, task["task_id"], "1.0.0", now=NOW)
        self.assertTrue(verify_release(result["release_path"])["verified"])

    def test_failed_post_move_verification_removes_new_release(self) -> None:
        task = self._completed()
        releases = self.root / ".athena" / "releases"
        with mock.patch(
            "athena.release.verify_release",
            side_effect=ReleaseError("simulated verification failure"),
        ):
            with self.assertRaisesRegex(ReleaseError, "simulated"):
                export_release(self.root, task["task_id"], "1.0.0", now=NOW)
        self.assertFalse((releases / "current.json").exists())
        self.assertEqual([], list(releases.iterdir()))

    def test_manifest_traversal_and_casefold_collision_are_rejected(self) -> None:
        _, _, release = self._exported()
        manifest_path = release / "manifest.json"
        manifest = read_json(manifest_path)
        manifest["files"][0]["path"] = "../escape"
        atomic_write_text(manifest_path, canonical_json(manifest))
        with self.assertRaises(ReleaseError):
            verify_release(release)

        self._reset_project()
        _, _, release = self._exported()
        manifest_path = release / "manifest.json"
        manifest = read_json(manifest_path)
        duplicate = dict(next(item for item in manifest["files"] if item["path"] == "README.md"))
        duplicate["path"] = "readme.md"
        manifest["files"].append(duplicate)
        manifest["files"].sort(key=lambda item: item["path"])
        atomic_write_text(manifest_path, canonical_json(manifest))
        with self.assertRaisesRegex(ReleaseError, "Case-insensitive"):
            verify_release(release)

    def test_manifest_absolute_and_windows_reserved_paths_are_rejected(self) -> None:
        for unsafe in ("/absolute.txt", "records/CON", "records/trailing."):
            with self.subTest(path=unsafe):
                self._reset_project()
                _, _, release = self._exported()
                manifest_path = release / "manifest.json"
                manifest = read_json(manifest_path)
                manifest["files"][0]["path"] = unsafe
                atomic_write_text(manifest_path, canonical_json(manifest))
                with self.assertRaises(ReleaseError):
                    verify_release(release)

    def test_symlink_or_reparse_entry_is_rejected(self) -> None:
        _, _, release = self._exported()
        target = release / "README.md"
        link = release / "linked.md"
        try:
            os.symlink(target, link)
        except (OSError, NotImplementedError) as exc:
            # Windows commonly denies symlink creation to unprivileged tests;
            # still exercise the fail-closed reparse branch deterministically.
            with mock.patch(
                "athena.release.is_link",
                side_effect=lambda path: Path(path).name == "README.md",
            ):
                with self.assertRaisesRegex(ReleaseError, "reparse-point"):
                    verify_release(release)
            self.assertIsInstance(exc, (OSError, NotImplementedError))
            return
        with self.assertRaises(ReleaseError):
            verify_release(release)

    def test_rebuild_reuses_same_deterministic_core(self) -> None:
        task = self._completed()
        first = export_release(self.root, task["task_id"], "1.2.0", now=NOW)
        second = export_release(
            self.root,
            task["task_id"],
            "1.2.0",
            now="2026-01-03T04:05:06Z",
        )
        self.assertTrue(first["created"])
        self.assertFalse(second["created"])
        self.assertEqual(first["release_path"], second["release_path"])
        self.assertEqual(first["core_sha256"], second["core_sha256"])
        envelope = read_json(Path(second["release_path"]) / "release.json")
        self.assertEqual(envelope["created_at"], NOW)

    def test_private_directory_is_never_exported_or_scanned(self) -> None:
        task = self._completed()
        private = self.root / ".athena" / "private" / "credentials.txt"
        private.write_text("api_key=THIS_PRIVATE_VALUE_MUST_STAY_LOCAL", encoding="utf-8")
        result = export_release(self.root, task["task_id"], "1.0.0", now=NOW)
        release = Path(result["release_path"])
        paths = {path.relative_to(release).as_posix() for path in release.rglob("*")}
        self.assertFalse(any("private" in path.casefold() for path in paths))

    def test_current_pointer_is_written_only_after_verified_release(self) -> None:
        task = self._completed()
        result = export_release(self.root, task["task_id"], "2.0.0", now=NOW)
        pointer_path = self.root / ".athena" / "releases" / "current.json"
        pointer = read_json(pointer_path)
        self.assertEqual(pointer["release_directory"], Path(result["release_path"]).name)
        self.assertEqual(pointer["core_sha256"], result["core_sha256"])
        self.assertEqual(pointer["task_id"], task["task_id"])
        self.assertTrue(verify_release(Path(result["release_path"]))["verified"])

        original_pointer = pointer_path.read_bytes()
        registered = self.root / ".athena" / Path(
            *task["artifacts"][0]["relative_path"].split("/")
        )
        registered.write_text("changed after checkpoint", encoding="utf-8")
        with self.assertRaises(ConflictError):
            export_release(self.root, task["task_id"], "2.0.1", now=NOW)
        self.assertEqual(original_pointer, pointer_path.read_bytes())
        self.assertTrue(verify_release(Path(result["release_path"]))["verified"])

    def test_common_secret_in_artifact_blocks_export_without_leaking_value(self) -> None:
        cases = (
            "sk-abcdefghijklmnopqrstuvwxyz123456",
            'password = "correct-horse-battery"',
            "-----BEGIN RSA PRIVATE KEY-----\nnot-real-key-material",
        )
        for secret in cases:
            with self.subTest(secret_kind=secret.splitlines()[0].split("=")[0]):
                self._reset_project()
                task = self._completed(f"credential: {secret}\n")
                with self.assertRaises(SecretDetectedError) as caught:
                    export_release(self.root, task["task_id"], "1.0.0", now=NOW)
                self.assertNotIn(secret, str(caught.exception))
                releases = self.root / ".athena" / "releases"
                self.assertFalse((releases / "current.json").exists())
                self.assertFalse(any(path.is_dir() for path in releases.iterdir()))

    def test_invalid_release_version_is_blocked(self) -> None:
        task = self._completed()
        for version in ("v1", "1.0", "../1.0.0", "1.0.0+local"):
            with self.subTest(version=version):
                with self.assertRaises(BlockedError):
                    export_release(self.root, task["task_id"], version, now=NOW)


if __name__ == "__main__":
    unittest.main()
