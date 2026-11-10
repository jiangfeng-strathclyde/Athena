"""Install the new literature resources in isolation; not a model behavior test."""

import tempfile
import unittest
from pathlib import Path

from scripts import install_athena as installer
from scripts.check_skill_dependencies import inspect_skill, needs_attention

ROOT = Path(__file__).resolve().parents[1]


class LiteratureSkillPackagingTests(unittest.TestCase):
    def check_isolated_resource(self, name, resource):
        source = ROOT / "skills" / name
        with tempfile.TemporaryDirectory(prefix="athena-literature-test-") as temp:
            target = Path(temp) / "installed"
            self.assertEqual(installer.install(target, False, skills=[source]),
                             (1, 0, None))
            self.assertEqual({p.name for p in target.iterdir()}, {name})
            for relative in ["SKILL.md", resource]:
                self.assertEqual((target / name / relative).read_bytes(),
                                 (source / relative).read_bytes())
            return inspect_skill(target / name)

    def test_citation_tracing_is_self_contained_after_install(self):
        report = self.check_isolated_resource(
            "citation-tracing", "references/output-contract.md")
        self.assertFalse(needs_attention(report))

    def test_evidence_mode_reference_survives_install(self):
        # The legacy research-lit workflow still has other unbundled resources;
        # this check certifies only that the new mode's reference is shipped.
        self.check_isolated_resource("research-lit", "references/evidence-matrix.md")


if __name__ == "__main__":
    unittest.main()
