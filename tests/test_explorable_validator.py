import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "skills" / "explorable-paper" / "scripts" / "validate_explorable.py"
SPEC = importlib.util.spec_from_file_location("validate_explorable", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class ExplorableValidatorTests(unittest.TestCase):
    def write(self, text):
        tmp = tempfile.TemporaryDirectory()
        path = Path(tmp.name) / "page.html"
        path.write_text(text, encoding="utf-8")
        self.addCleanup(tmp.cleanup)
        return path

    def test_accepts_self_contained_interactive_html(self):
        path = self.write("""<!doctype html><title>Demo</title>
            <svg viewBox='0 0 10 10'></svg><input type='range'>
            <script>document.querySelector('input').oninput = () => {};</script>""")
        self.assertEqual(MODULE.audit(path), [])

    def test_rejects_remote_runtime_asset(self):
        path = self.write("""<!doctype html><title>Demo</title>
            <canvas></canvas><button>Run</button>
            <script src='https://cdn.example/app.js'></script>""")
        problems = MODULE.audit(path)
        self.assertTrue(any("remote runtime assets" in problem for problem in problems))

    def test_external_citation_link_is_allowed(self):
        path = self.write("""<!doctype html><title>Demo</title>
            <svg></svg><details><summary>Source</summary>
            <a href='https://doi.org/example'>paper</a></details>
            <script>document.body.dataset.ready = '1';</script>""")
        self.assertEqual(MODULE.audit(path), [])


if __name__ == "__main__":
    unittest.main()
