"""Offline tests, not evidence of live API or agent acceptance."""
import argparse
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch
from urllib.error import HTTPError, URLError

from scripts import install_athena as installer
from scripts.check_skill_dependencies import inspect_skill, needs_attention

ROOT = Path(__file__).resolve().parents[1]


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


transport = module("athena_transport", ROOT / "skills/openalex/scripts/literature_http.py")
with patch.dict(sys.modules, {"literature_http": transport}):
    oa = module("athena_openalex", ROOT / "skills/openalex/scripts/openalex_fetch.py")
    s2 = module("athena_s2", ROOT / "skills/semantic-scholar/scripts/semantic_scholar_fetch.py")


class TransportTests(unittest.TestCase):
    def fetch(self, body):
        opener = Mock()
        opener.open.return_value = io.BytesIO(body)
        with patch.object(transport, "build_opener", return_value=opener), patch.object(transport.time, "sleep") as sleep:
            result = transport.fetch_json("https://example.org", "/works", {"search": "a b"})
        sleep.assert_called_once_with(1.1)
        self.assertEqual(opener.open.call_args.kwargs, {"timeout": 30})
        self.assertIn("search=a+b", opener.open.call_args.args[0].full_url)
        return result

    def test_valid_empty_and_missing_metadata(self):
        self.assertEqual(self.fetch(b'{"results": [{"year": null}]}'), {"results": [{"year": None}]})
        self.assertEqual(transport.result_rows(self.fetch(b'{"results": []}'), "results"), [])

    def test_invalid_responses_are_not_empty_results(self):
        for data in [b"not json", b"[]", b'{"error": "private body"}', b'{"errors": []}']:
            with self.subTest(data=data), self.assertRaises(transport.FetchError):
                self.fetch(data)
        for data in [{}, {"results": None}, {"results": [1]}]:
            with self.assertRaises(transport.FetchError):
                transport.result_rows(data, "results")
        with patch.object(transport, "MAX_BYTES", 4), self.assertRaises(transport.FetchError):
            self.fetch(b"12345")

    def test_errors_are_redacted_without_retry(self):
        for status in [301, 401, 403, 429, 500]:
            opener = Mock()
            opener.open.side_effect = HTTPError("https://example.org/?key=SECRET", status, "SECRET", {}, io.BytesIO(b"SECRET"))
            with patch.object(transport, "build_opener", return_value=opener), patch.object(transport.time, "sleep"):
                with self.assertRaises(transport.FetchError) as error:
                    transport.fetch_json("https://example.org", "/", {})
            self.assertIn(str(status), str(error.exception))
            self.assertNotIn("SECRET", str(error.exception))
            opener.open.assert_called_once()
        self.assertIsNone(transport.NoRedirect().redirect_request(None, None, 302, "", {}, "https://other.org"))

    def test_network_error_redaction(self):
        opener = Mock()
        opener.open.side_effect = URLError("SECRET")
        with patch.object(transport, "build_opener", return_value=opener), patch.object(transport.time, "sleep"):
            with self.assertRaises(transport.FetchError) as error:
                transport.fetch_json("https://example.org", "/", {})
        self.assertNotIn("SECRET", str(error.exception))

    def test_standalone_transport_copies_match(self):
        self.assertEqual((ROOT / "skills/openalex/scripts/literature_http.py").read_bytes(),
                         (ROOT / "skills/semantic-scholar/scripts/literature_http.py").read_bytes())


class HelperTests(unittest.TestCase):
    def test_ids_and_encoded_paths(self):
        self.assertEqual(oa.work_id("https://doi.org/10.1234/example"), "doi:10.1234/example")
        self.assertEqual(s2.paper_id("10.1234/example"), "DOI:10.1234/example")
        self.assertEqual(s2.paper_id("ARXIV:1706.03762"), "ARXIV:1706.03762")
        for fn in [oa.work_id, s2.paper_id]:
            for value in ["../secret", "https://example.org/x", "10.1234/x?key=y"]:
                with self.assertRaises(argparse.ArgumentTypeError):
                    fn(value)
        for helper, command in [(oa, "work"), (s2, "paper")]:
            path, _ = helper.build_request(helper.parser().parse_args([command, "10.1234/example"]))
            self.assertIn("10.1234%2Fexample", path)

    def test_validation_before_network(self):
        for helper in [oa, s2]:
            for tail in [["--max", "0"], ["--max", "101"], ["--year", "2026-2020"],
                         ["--year", "bad"], ["--min-citations", "-1"]]:
                with self.assertRaises(ValueError):
                    helper.build_request(helper.parser().parse_args(["search", "test", *tail]))
            with self.assertRaises(ValueError):
                helper.build_request(helper.parser().parse_args(["search", " "]))

    def test_filters_and_bulk_bound(self):
        _, params = oa.build_request(oa.parser().parse_args(["search", "test", "--min-citations", "5", "--open-access"]))
        self.assertIn("cited_by_count:>4", params["filter"])
        self.assertIn("is_oa:true", params["filter"])
        path, params = s2.build_request(s2.parser().parse_args(["search-bulk", "test"]))
        self.assertTrue(path.endswith("/bulk"))
        self.assertNotIn("fieldsOfStudy", params)
        self.assertNotIn("limit", params)
        self.assertNotIn("tldr", params["fields"].split(","))
        with patch.object(s2, "fetch_json", return_value={"data": [{"year": None}] * 20}), patch("sys.stdout", new_callable=io.StringIO) as output:
            self.assertEqual(s2.main(["search-bulk", "test", "--max", "2"]), 0)
        self.assertEqual(json.loads(output.getvalue())["returned"], 2)

    def test_credentials_are_headers_and_nulls_preserved(self):
        for helper, env, header, value, field in [(oa, "OPENALEX_API_KEY", "Authorization", "Bearer SECRET", "results"),
                                                (s2, "SEMANTIC_SCHOLAR_API_KEY", "x-api-key", "SECRET", "data")]:
            with patch.dict(os.environ, {env: "SECRET"}), patch.object(helper, "fetch_json", return_value={field: [{"year": None}]}) as fetch, patch("sys.stdout", new_callable=io.StringIO) as output:
                self.assertEqual(helper.main(["search", "test"]), 0)
            self.assertEqual(fetch.call_args.args[3][header], value)
            self.assertNotIn("SECRET", repr(fetch.call_args.args[2]))
            self.assertIsNone(json.loads(output.getvalue())["results"][0]["year"])

    def test_failure_is_nonzero_with_no_success_output(self):
        for helper in [oa, s2]:
            with patch.object(helper, "fetch_json", side_effect=transport.FetchError("HTTP 429")), patch("sys.stdout", new_callable=io.StringIO) as out, patch("sys.stderr", new_callable=io.StringIO) as err:
                self.assertEqual(helper.main(["search", "test"]), 1)
            self.assertEqual(out.getvalue(), "")
            self.assertIn("429", err.getvalue())

    def test_installed_helpers_outside_checkout(self):
        for name, script in [("openalex", "openalex_fetch.py"), ("semantic-scholar", "semantic_scholar_fetch.py")]:
            skill = ROOT / "skills" / name
            self.assertFalse(needs_attention(inspect_skill(skill)))
            with tempfile.TemporaryDirectory() as temp:
                target = Path(temp) / "installed"
                installer.install(target, False, skills=[skill])
                executable = target / name / "scripts" / script
                # Ignore user site and Python environment, retain this script's bundled imports.
                proc = subprocess.run([sys.executable, "-E", "-s", str(executable), "--help"], cwd=temp, capture_output=True, text=True)
                self.assertEqual(proc.returncode, 0, proc.stderr)
                self.assertTrue((target / name / "LICENSE.upstream").is_file())
                provenance = json.loads((target / name / "references/provenance.json").read_text())
                self.assertEqual(len(provenance["commit"]), 40)
                bad = subprocess.run([sys.executable, "-E", "-s", str(executable), "search", "test", "--max", "0"], cwd=temp, capture_output=True, text=True)
                self.assertNotEqual(bad.returncode, 0)
                self.assertIn("--max", bad.stderr)


if __name__ == "__main__":
    unittest.main()
