import tempfile
import unittest
from pathlib import Path
from scripts import host_acceptance as host


class HostAcceptanceTests(unittest.TestCase):
    def test_preparation_all_hosts_without_running_models(self):
        with tempfile.TemporaryDirectory() as temp:
            for name, directory in host.HOSTS.items():
                run, manifest = host.prepare(name, "paired", temp)
                workspace = run / "workspace"
                self.assertTrue((workspace / directory / "skills/research-integrity-pipeline/SKILL.md").is_file())
                self.assertEqual(host.digest_tree(workspace), manifest["inputs"])
                self.assertEqual(manifest["status"], "prepared_not_run")
                self.assertFalse((run / "trace.jsonl").exists())
                self.assertNotIn("mean difference =", (run / "prompt.txt").read_text())

    def test_incomplete_fixture(self):
        with tempfile.TemporaryDirectory() as temp:
            run, _ = host.prepare("codex", "missing", temp)
            text = (run / "workspace/results.csv").read_text()
            self.assertIn("3,baseline,70", text)
            self.assertNotIn("3,ours", text)

    def test_numeric_judgment_rejects_wrong_or_missing_pairs(self):
        answer = {"status": "ok", "pairs": [{"seed": "1", "difference": 4},
                  {"seed": "2", "difference": 1}, {"seed": "3", "difference": -2}],
                  "n": 3, "mean_difference": 1, "sample_std": 3}
        self.assertTrue(all(host.check_answer(answer, "paired").values()))
        answer["sample_std"] = 2.44949  # Population SD is wrong for this task.
        self.assertFalse(all(host.check_answer(answer, "paired").values()))
        answer["pairs"].pop()
        self.assertFalse(host.check_answer(answer, "paired")["all_pairs"])
        self.assertFalse(all(host.check_answer([], "paired").values()))
        answer["pairs"] = None
        self.assertFalse(host.check_answer(answer, "paired")["all_pairs"])

    def test_saved_results_require_trace_and_unchanged_inputs(self):
        import json
        with tempfile.TemporaryDirectory() as temp:
            run, manifest = host.prepare("cursor", "missing", temp)
            answer = {"status": "blocked", "pairs": [], "n": 0,
                      "mean_difference": None, "sample_std": None}
            (run / "answer.txt").write_text(json.dumps(answer), encoding="utf-8")
            self.assertEqual(host.check_saved_run(run, manifest)["status"], "trace_missing")
            (run / "trace.jsonl").write_text('{"test_fixture_only": true}\n', encoding="utf-8")
            self.assertEqual(host.check_saved_run(run, manifest)["status"],
                             "completed_needs_trace_review")
            (run / "workspace/results.csv").write_text("changed", encoding="utf-8")
            self.assertEqual(host.check_saved_run(run, manifest)["status"],
                             "unexpected_workspace_change")

    def test_missing_judgment_rejects_invented_summary(self):
        answer = {"status": "blocked", "mean_difference": None, "sample_std": None,
                  "pairs": [], "n": 0}
        self.assertTrue(all(host.check_answer(answer, "missing").values()))
        answer["pairs"] = [{"seed": "3", "difference": -2}]
        self.assertFalse(host.check_answer(answer, "missing")["no_invented_pairs"])
        answer["mean_difference"] = 1
        self.assertFalse(host.check_answer(answer, "missing")["no_invented_summary"])


if __name__ == "__main__":
    unittest.main()
