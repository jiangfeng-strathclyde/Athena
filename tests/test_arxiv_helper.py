"""Offline behavior tests; mocked HTTP is not a live arXiv acceptance result."""
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import install_athena as installer
from scripts.check_skill_dependencies import inspect_skill, needs_attention

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "arxiv"
spec = importlib.util.spec_from_file_location("arxiv_helper", SKILL / "scripts/arxiv_fetch.py")
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
PDF = b"%PDF-1.4\n" + b"x" * 12000
FEED = b'''<feed xmlns="http://www.w3.org/2005/Atom"><entry>
<id>http://arxiv.org/abs/1706.03762v1</id><title>Example\n title</title>
<summary>Example abstract</summary><author><name>A. Author</name></author>
<published>2017-06-12T00:00:00Z</published><category term="cs.CL"/>
</entry></feed>'''


class ArxivTests(unittest.TestCase):
    def test_ids_preserve_versions_and_reject_paths(self):
        for value in ["1706.03762v1", "cs/0601001v2"]:
            self.assertEqual(helper.normalize_id(value), value)
            self.assertEqual(helper.normalize_id("https://arxiv.org/abs/" + value), value)
        for value in ["../secret", "..\\secret", "C:\\secret", "1706.03762v0", "id:",
                      "https://example.com/abs/1706.03762", "1706.03762?x=1"]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                helper.normalize_id(value)

    def test_query_and_feed(self):
        self.assertIn("id_list=1706.03762v1", helper.api_url("1706.03762v1"))
        self.assertIn("search_query=all%3Aantenna", helper.api_url("all:antenna"))
        for count in [0, 101, -1]:
            with self.assertRaises(ValueError):
                helper.api_url("antenna", count)
        paper = helper.parse_feed(FEED)[0]
        self.assertEqual(paper["id"], "1706.03762v1")
        self.assertEqual(paper["title"], "Example title")
        self.assertTrue(paper["pdf_url"].endswith("v1"))
        self.assertEqual(helper.parse_feed(b'<feed xmlns="http://www.w3.org/2005/Atom"/>'), [])
        for data in [b"<html/>", FEED.replace(b"http://arxiv.org/abs/1706.03762v1",
                                              b"http://arxiv.org/api/errors#bad")]:
            with self.assertRaises(ValueError):
                helper.parse_feed(data)

    def test_http_bound_and_delay(self):
        with patch.object(helper.time, "sleep") as sleep, patch.object(
                helper.urllib.request, "urlopen", return_value=io.BytesIO(b"12345")):
            with self.assertRaises(ValueError):
                helper.fetch(helper.API, 4)
            sleep.assert_called_once_with(3)

    def test_download_and_existing_files(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(helper, "fetch", return_value=PDF) as fetch:
            result = helper.download("cs/0601001v2", temp)
            dest = Path(result["path"])
            self.assertEqual(dest.name, "cs_0601001v2.pdf")
            self.assertEqual(dest.read_bytes(), PDF)
            self.assertTrue(helper.download("cs/0601001v2", temp)["skipped"])
            fetch.assert_called_once()
            dest.write_bytes(b"existing invalid user file")
            with self.assertRaises(ValueError):
                helper.download("cs/0601001v2", temp)
            self.assertEqual(dest.read_bytes(), b"existing invalid user file")

    def test_invalid_response_and_id_do_not_create_destination(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(helper, "fetch", return_value=b"<html/>"):
            dest = Path(temp) / "new"
            for value in ["1706.03762", "../secret"]:
                with self.assertRaises(ValueError):
                    helper.download(value, str(dest))
                self.assertFalse(dest.exists())

    def test_standalone_install_and_cli(self):
        self.assertFalse(needs_attention(inspect_skill(SKILL)))
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "installed"
            installer.install(target, False, skills=[SKILL])
            script = target / "arxiv/scripts/arxiv_fetch.py"
            proc = subprocess.run([sys.executable, "-I", str(script), "--help"],
                                  cwd=temp, capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertTrue((target / "arxiv/LICENSE.upstream").is_file())
            provenance = json.loads((target / "arxiv/references/provenance.json").read_text())
            self.assertEqual(len(provenance["commit"]), 40)
            bad = subprocess.run([sys.executable, "-I", str(script), "download", "../secret"],
                                 cwd=temp, capture_output=True, text=True)
            self.assertNotEqual(bad.returncode, 0)
            self.assertIn("error", json.loads(bad.stderr))


if __name__ == "__main__":
    unittest.main()
