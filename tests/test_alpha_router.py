from __future__ import annotations

import contextlib
import io
import itertools
import unittest

from athena.cli import build_parser
from athena.router import CORE_SKILL_ORDER, route_goal


class ExactSubsetRoutingTests(unittest.TestCase):
    def test_each_explicit_singleton_remains_exact_despite_broad_goal(self):
        for skill in CORE_SKILL_ORDER:
            with self.subTest(skill=skill):
                decision = route_goal("Paper understanding: citations, evidence and HTML", [skill])
                self.assertEqual((skill,), decision.skills)
                self.assertEqual((f"explicit:{skill}",), decision.matched_rules)
                self.assertTrue(decision.explicit_override)

    def test_every_explicit_subset_is_deduplicated_in_canonical_order(self):
        for size in range(1, len(CORE_SKILL_ORDER) + 1):
            for subset in itertools.combinations(CORE_SKILL_ORDER, size):
                for permutation in itertools.permutations(subset):
                    with self.subTest(request=permutation):
                        requested = (*permutation, permutation[0])
                        self.assertEqual(subset, route_goal("Paper understanding", requested).skills)

    def test_embedded_explicit_request_is_also_an_exact_subset(self):
        decision = route_goal("use explorable-paper and use citation-tracing")
        self.assertEqual(("citation-tracing", "explorable-paper"), decision.skills)
        self.assertTrue(decision.explicit_override)

    def test_argument_subset_overrides_embedded_skill_invocation(self):
        decision = route_goal("use citation-tracing", ["explorable-paper"])
        self.assertEqual(("explorable-paper",), decision.skills)

    def test_implicit_goals_retain_integrity_baseline(self):
        expected = {
            "Trace citations": ("citation-tracing", "research-integrity-pipeline"),
            "Create explorable HTML": ("research-integrity-pipeline", "explorable-paper"),
            "Paper understanding": CORE_SKILL_ORDER,
            "Study a question": ("research-integrity-pipeline",),
        }
        for goal, skills in expected.items():
            with self.subTest(goal=goal):
                decision = route_goal(goal)
                self.assertEqual(skills, decision.skills)
                self.assertFalse(decision.explicit_override)

    def test_empty_explicit_subset_does_not_silently_select_implicit_route(self):
        with self.assertRaisesRegex(ValueError, "must not be empty"):
            route_goal("Paper understanding", [])

    def test_cli_skill_help_describes_exact_subset_and_canonical_order(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output), self.assertRaises(SystemExit) as raised:
            build_parser().parse_args(["plan", "--help"])
        self.assertEqual(0, raised.exception.code)
        help_text = " ".join(output.getvalue().split())
        self.assertIn("exact core-skill subset", help_text)
        self.assertIn("canonical order", help_text)


if __name__ == "__main__":
    unittest.main()
