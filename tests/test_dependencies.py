import tempfile
import unittest
import contextlib
import io
from pathlib import Path
from unittest.mock import patch

from scripts import check_skill_dependencies as scanner
from scripts.check_skill_dependencies import inspect_skill, needs_attention


class DependencyTests(unittest.TestCase):
    def inspect(self, text):
        with tempfile.TemporaryDirectory(prefix="athena-deps-") as temp:
            folder = Path(temp) / "skill"
            folder.mkdir()
            (folder / "SKILL.md").write_text(text, encoding="utf-8")
            (folder / "available.md").write_text("present", encoding="utf-8")
            (Path(temp) / "sibling.md").write_text("present in checkout only", encoding="utf-8")
            return inspect_skill(folder)

    def test_missing_and_external_folder_links(self):
        result = self.inspect("[ok](available.md#part) [missing](scripts/run.py) [shared](../sibling.md)")
        self.assertEqual(result["missing_local_references"], ["scripts/run.py"])
        self.assertEqual(result["references_outside_skill"], ["../sibling.md"])
        self.assertTrue(needs_attention(result))

    def test_external_urls_and_anchors_are_not_local_dependencies(self):
        result = self.inspect("[web](https://example.org) [mail](mailto:x@example.org) [heading](#part)")
        self.assertFalse(needs_attention(result))

    def test_mirror_notice_is_detected(self):
        result = self.inspect("support files (scripts/) Not distributed with mirrors")
        self.assertTrue(result["declares_unbundled_support"])
        self.assertTrue(needs_attention(result))

    def test_other_mirror_notice_wordings_are_detected(self):
        for text in ["supporting documentation was not distributed with the mirror",
                     "Support documents and scripts were not distributed with mirrors"]:
            self.assertTrue(self.inspect(text)["declares_unbundled_support"])

    def test_empty_link_does_not_crash_scan(self):
        self.assertFalse(needs_attention(self.inspect("[empty]()")))

    def test_code_examples_are_not_markdown_links(self):
        result = self.inspect('''```python
model = registry["vit_b"](checkpoint="weights.pth")
```
~~~text
[example](not-a-real-file.md)
~~~
Inline `[example](also-not-a-file.md)` and ``[x](code.md)``.
    [indented](example.md)
[actual](missing.md)
''')
        self.assertEqual(result["missing_local_references"], ["missing.md"])

    def test_shorter_fence_does_not_end_code_block(self):
        result = self.inspect('````text\n```\n[x](code.md)\n````\n[x](real.md)')
        self.assertEqual(result["missing_local_references"], ["real.md"])

    def test_strict_mode_fails_on_missing_packaging(self):
        with tempfile.TemporaryDirectory(prefix="athena-strict-test-") as temp:
            folder = Path(temp) / "skills" / "incomplete"
            folder.mkdir(parents=True)
            (folder / "SKILL.md").write_text("[required](references/missing.md)", encoding="utf-8")
            with patch.object(scanner, "ROOT", Path(temp)), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(scanner.main([]), 0)
                self.assertEqual(scanner.main(["--strict"]), 1)
                self.assertEqual(scanner.main(["--skill", "incomplete", "--json", "--strict"]), 1)

    def test_host_tools_are_reported_without_claiming_availability(self):
        result = self.inspect("allowed-tools: Bash(*), mcp__reviewer__review")
        self.assertTrue(result["mentions_host_tools"])
        self.assertFalse(needs_attention(result))


if __name__ == "__main__":
    unittest.main()
