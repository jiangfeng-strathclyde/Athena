"""Exercise installation in isolated temporary directories, never user skill paths."""

import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import install_athena as installer


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="athena-tests-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.repo = self.base / "checkout"
        self.source = self.repo / "skills"
        self.target = self.base / "user" / "skills"
        for name in ["alpha", "beta", *sorted(installer.FLAGGED)]:
            folder = self.source / name
            folder.mkdir(parents=True)
            (folder / "SKILL.md").write_text("new " + name, encoding="utf-8")
        for key, value in [("ROOT", self.repo), ("SOURCE", self.source)]:
            mock = patch.object(installer, key, value)
            mock.start()
            self.addCleanup(mock.stop)

    def old_install(self):
        for name in ["alpha", "beta", "unrelated"]:
            folder = self.target / name
            folder.mkdir(parents=True)
            (folder / "SKILL.md").write_text("old " + name, encoding="utf-8")

    def snapshot(self):
        return {str(p.relative_to(self.target)): p.read_bytes()
                for p in self.target.rglob("*") if p.is_file()}

    def run_main(self, *args):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return installer.main(list(args))

    def test_fresh_install_excludes_flagged(self):
        self.assertEqual(installer.install(self.target, False), (2, 0, None))
        self.assertEqual({p.name for p in self.target.iterdir()}, {"alpha", "beta"})

    def test_each_flagged_skill_requires_authorization(self):
        for name in installer.FLAGGED:
            with self.assertRaises(ValueError):
                installer.select_skills([name])
            self.assertEqual([p.name for p in installer.select_skills([name], [name])], [name])

    def test_unknown_selection_rejected(self):
        with self.assertRaises(ValueError):
            installer.select_skills(["../../elsewhere"])

    def test_force_preserves_backups_and_unrelated_skills(self):
        self.old_install()
        count, replaced, backup = installer.install(self.target, True)
        self.assertEqual((count, replaced), (2, 2))
        self.assertEqual((backup / "alpha" / "SKILL.md").read_text(), "old alpha")
        self.assertEqual((self.target / "alpha" / "SKILL.md").read_text(), "new alpha")
        self.assertEqual((self.target / "unrelated" / "SKILL.md").read_text(), "old unrelated")
        self.assertNotIn(self.target, backup.parents)

    def test_conflict_leaves_target_unchanged(self):
        self.old_install()
        before = self.snapshot()
        with self.assertRaises(FileExistsError):
            installer.install(self.target, False)
        self.assertEqual(before, self.snapshot())
        self.assertFalse(list(self.target.parent.glob(".athena-update-*")))

    def test_source_overlap_and_broad_targets_rejected(self):
        for target in [self.repo, self.source, self.source / "nested", self.repo.parent,
                       Path.home(), Path(self.base.anchor)]:
            with self.subTest(target=target), self.assertRaises(ValueError):
                installer.install(target, True)
        self.assertTrue((self.source / "alpha" / "SKILL.md").exists())

    def test_dry_run_creates_nothing(self):
        self.assertEqual(self.run_main("--target", str(self.target), "--dry-run"), 0)
        self.assertFalse(self.target.parent.exists())

    def test_strict_packaging_stops_before_any_write(self):
        (self.source / "alpha" / "SKILL.md").write_text("[required](missing.md)", encoding="utf-8")
        self.assertEqual(self.run_main("--target", str(self.target), "--strict-packaging"), 1)
        self.assertFalse(self.target.parent.exists())

    def test_packaging_findings_warn_without_blocking_default_install(self):
        (self.source / "alpha" / "SKILL.md").write_text("[required](missing.md)", encoding="utf-8")
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(installer.main(["--target", str(self.target)]), 0)
        self.assertIn("1 of 2 selected skills need review", output.getvalue())
        self.assertTrue((self.target / "alpha" / "SKILL.md").exists())

    def test_packaging_gate_only_inspects_selected_skills(self):
        (self.source / "alpha" / "SKILL.md").write_text("[required](missing.md)", encoding="utf-8")
        self.assertEqual(self.run_main("--target", str(self.target), "--skill", "beta",
                                       "--strict-packaging"), 0)
        self.assertEqual([p.name for p in self.target.iterdir()], ["beta"])

    def test_copy_failure_preserves_old_files(self):
        self.old_install()
        before = self.snapshot()
        original = installer.shutil.copytree

        def fail_beta(source, destination, *args, **kwargs):
            if Path(source).name == "beta":
                raise OSError("simulated full disk")
            return original(source, destination, *args, **kwargs)

        with patch.object(installer.shutil, "copytree", side_effect=fail_beta):
            with self.assertRaises(OSError):
                installer.install(self.target, True)
        self.assertEqual(before, self.snapshot())

    def test_commit_failure_rolls_back_all_skills(self):
        self.old_install()
        before = self.snapshot()
        rename = Path.rename

        def fail_beta(path, target):
            if path.parent.name == "staged" and path.name == "beta":
                raise OSError("simulated rename failure")
            return rename(path, target)

        with patch.object(Path, "rename", fail_beta), self.assertRaises(OSError):
            installer.install(self.target, True)
        self.assertEqual(before, self.snapshot())

    def test_new_install_failure_removes_partial_install(self):
        rename = Path.rename

        def fail_beta(path, target):
            if path.parent.name == "staged" and path.name == "beta":
                raise OSError("simulated rename failure")
            return rename(path, target)

        with patch.object(Path, "rename", fail_beta), self.assertRaises(OSError):
            installer.install(self.target, False)
        self.assertFalse(self.target.exists())

    def test_failed_rollback_keeps_recovery_material(self):
        self.old_install()
        rename = Path.rename

        def fail_commit_and_restore(path, target):
            if path.name == "beta" and path.parent.name in {"staged", "backup"}:
                raise OSError("simulated locked directory")
            return rename(path, target)

        with patch.object(Path, "rename", fail_commit_and_restore):
            with self.assertRaisesRegex(OSError, "recovery files retained"):
                installer.install(self.target, True)
        backups = list(self.target.parent.glob(".athena-update-*/backup/beta/SKILL.md"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(), "old beta")

    def test_non_directory_conflict_rejected(self):
        self.target.mkdir(parents=True)
        (self.target / "alpha").write_text("user file")
        with self.assertRaises(ValueError):
            installer.install(self.target, True)
        self.assertEqual((self.target / "alpha").read_text(), "user file")

    def test_symlink_destination_rejected(self):
        self.target.mkdir(parents=True)
        try:
            (self.target / "alpha").symlink_to(self.source / "alpha", target_is_directory=True)
        except OSError:
            self.skipTest("Symlink permission unavailable on this OS")
        with self.assertRaises(ValueError):
            installer.install(self.target, True)

    def test_source_symlink_rejected(self):
        try:
            (self.source / "alpha" / "linked.txt").symlink_to(self.source / "beta" / "SKILL.md")
        except OSError:
            self.skipTest("Symlink permission unavailable on this OS")
        with self.assertRaises(ValueError):
            installer.install(self.target, False)
        self.assertFalse(self.target.exists())

    def test_auto_avoids_duplicate_shared_host_copies(self):
        home = self.base / "home"
        for name in [".claude", ".cursor", ".copilot", ".gemini"]:
            (home / name).mkdir(parents=True)
        with patch.object(installer.shutil, "which", return_value=None):
            self.assertEqual([label for label, _ in installer.auto_targets(home)],
                             ["universal", "claude-code"])

    def test_multi_target_preflight_prevents_partial_conflict_install(self):
        self.old_install()
        first = self.base / "other" / "skills"
        with patch.object(installer, "auto_targets", return_value=[("one", first), ("two", self.target)]):
            self.assertEqual(self.run_main("--auto"), 1)
        self.assertFalse(first.exists())

    def test_all_explicit_agents_have_known_targets(self):
        for agent, parts in installer.AGENT_DIRECTORIES.items():
            self.assertEqual(installer.agent_target(agent, self.base), self.base.joinpath(*parts))

    def test_existing_unselected_flagged_skill_is_not_deleted(self):
        flagged = self.target / "deepxiv"
        flagged.mkdir(parents=True)
        (flagged / "SKILL.md").write_text("user-reviewed version")
        installer.install(self.target, False)
        self.assertEqual((flagged / "SKILL.md").read_text(), "user-reviewed version")

    def test_nested_multi_target_destinations_rejected(self):
        with patch.object(installer, "auto_targets", return_value=[
                ("one", self.target), ("two", self.target / "nested")]):
            self.assertEqual(self.run_main("--auto"), 1)
        self.assertFalse(self.target.exists())

    def test_later_target_failure_is_reported_without_undoing_first(self):
        second = self.base / "other" / "skills"
        real_install = installer.install

        def fail_second(target, force, skills):
            if target == second:
                raise OSError("simulated second-destination failure")
            return real_install(target, force, skills)

        error_output = io.StringIO()
        with patch.object(installer, "auto_targets", return_value=[
                ("one", self.target), ("two", second)]), \
                patch.object(installer, "install", side_effect=fail_second), \
                contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(error_output):
            self.assertEqual(installer.main(["--auto"]), 1)
        self.assertTrue((self.target / "alpha" / "SKILL.md").exists())
        self.assertFalse(second.exists())
        self.assertIn("Earlier destinations remain installed", error_output.getvalue())


class CatalogIntegrationTests(unittest.TestCase):
    def test_real_default_catalog_install_and_update(self):
        # The real catalog is read-only; all installed copies live under temp.
        selected = installer.select_skills()
        self.assertEqual(len(selected), 105)
        self.assertTrue(installer.FLAGGED.isdisjoint({p.name for p in selected}))
        with tempfile.TemporaryDirectory(prefix="athena-catalog-test-") as temp:
            target = Path(temp) / "skills"
            self.assertEqual(installer.install(target, False), (105, 0, None))
            for skill in selected:
                self.assertEqual((target / skill.name / "SKILL.md").read_bytes(),
                                 (skill / "SKILL.md").read_bytes())
            count, replaced, backup = installer.install(target, True)
            self.assertEqual((count, replaced), (105, 105))
            self.assertEqual(len(list(backup.iterdir())), 105)

    def test_entry_point_installs_alone(self):
        with tempfile.TemporaryDirectory(prefix="athena-entry-test-") as temp:
            target = Path(temp) / "skills"
            result = installer.install(target, False, installer.select_skills(["research-integrity-pipeline"]))
            self.assertEqual(result, (1, 0, None))
            self.assertEqual([p.name for p in target.iterdir()], ["research-integrity-pipeline"])


if __name__ == "__main__":
    unittest.main()
