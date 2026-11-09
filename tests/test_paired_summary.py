"""Test the helper after installation, with no imports from the source checkout."""

import hashlib
import json
import math
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts import install_athena as installer


class PairedSummaryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="athena-pairs-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        target = self.base / "installed"
        installer.install(target, False, installer.select_skills(["research-integrity-pipeline"]))
        self.script = target / "research-integrity-pipeline" / "scripts" / "paired_summary.py"
        self.data = self.base / "runs.csv"

    def run_helper(self, data, *extra):
        self.data.write_bytes(data.encode("utf-8"))
        before = self.data.read_bytes()
        result = subprocess.run(
            [sys.executable, "-I", str(self.script), str(self.data), "--metric", "score",
             "--baseline", "baseline", "--candidate", "ours", "--unit", "points", *extra],
            cwd=self.base, capture_output=True, text=True, timeout=15)
        self.assertEqual(self.data.read_bytes(), before)
        return result

    def test_all_pairs_sample_std_and_provenance(self):
        result = self.run_helper("seed,method,score\n1,baseline,70\n1,ours,73.2\n"
                                 "2,baseline,70\n2,ours,70.7\n3,baseline,70\n3,ours,69.6\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["n_pairs"], 3)
        self.assertAlmostEqual(report["mean_difference"], 1.166666666666667)
        # For differences 3.2, 0.7, -0.4, the exact sample variance is 1021/300.
        self.assertAlmostEqual(report["sample_std_difference"], math.sqrt(1021 / 300), places=10)
        self.assertEqual(report["source"]["sha256"], hashlib.sha256(self.data.read_bytes()).hexdigest())
        self.assertEqual(report["pairs"][0]["baseline"]["csv_line_end"], 2)
        self.assertLess(report["pairs"][2]["difference"], 0)

    def test_single_pair_has_undefined_sample_std(self):
        result = self.run_helper("seed,method,score\nx,baseline,2\nx,ours,1\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["mean_difference"], -1)
        self.assertIsNone(report["sample_std_difference"])

    def test_bom_and_other_method_rows_reported(self):
        result = self.run_helper("\ufeffseed,method,score\na,other,4\na,baseline,2\na,ours,3\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["ignored_other_method_rows"], 1)

    def test_bad_inputs_fail_without_partial_report(self):
        cases = [
            "seed,method,score\n1,baseline,1\n",  # incomplete
            "seed,method,score\n1,baseline,1\n1,baseline,2\n1,ours,3\n",  # duplicate
            "seed,method,score\n1,baseline,nan\n1,ours,3\n",
            "seed,method,score\n1,baseline,inf\n1,ours,3\n",
            "seed,method,score\n1,baseline,\n1,ours,3\n",
            "seed,method,score\n,baseline,1\n1,ours,3\n",
            "seed,method,score\n1,,1\n1,ours,3\n",
            "seed,method,score\n1,baseline,1,extra\n1,ours,3\n",
            "seed,method,score\n1,baseline\n1,ours,3\n",
            "seed,method,score,score\n1,baseline,1,2\n",
            "seed,method,wrong\n1,baseline,1\n",
            "seed,method,score\n",
            "seed,method,score\n1,other,3\n",
            "seed,method,score\n1,baseline,-1e308\n1,ours,1e308\n",
            'seed,method,score\n1,baseline,"1\n',
        ]
        for data in cases:
            with self.subTest(data=data):
                result = self.run_helper(data)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertEqual(result.stdout, "")
                self.assertNotIn("Traceback", result.stderr)

    def test_identical_methods_and_columns_rejected(self):
        for extra in [("--candidate", "baseline"), ("--pair-column", "score"), ("--unit", " ")]:
            with self.subTest(extra=extra):
                result = self.run_helper("seed,method,score\n1,baseline,1\n1,ours,2\n", *extra)
                self.assertEqual(result.returncode, 2)

    def test_custom_columns(self):
        result = self.run_helper("run,algorithm,score\nx,baseline,0.1\nx,ours,0.2\n",
                                 "--pair-column", "run", "--method-column", "algorithm")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertAlmostEqual(json.loads(result.stdout)["mean_difference"], 0.1)


if __name__ == "__main__":
    unittest.main()
