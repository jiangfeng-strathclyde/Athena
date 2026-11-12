"""Deterministic, explainable routing for Athena's Alpha core skills.

The router deliberately does not invoke a model.  It normalises a goal, applies
small bilingual rules, and returns a stable skill chain that can be persisted in
project state.  Research integrity is the mandatory baseline for every route.
"""

from __future__ import annotations

from dataclasses import dataclass
import re
import unicodedata
from collections.abc import Iterable


CORE_SKILL_ORDER: tuple[str, ...] = (
    "citation-tracing",
    "explorable-paper",
    "research-integrity-pipeline",
)

_INTEGRITY_SKILL = "research-integrity-pipeline"


@dataclass(frozen=True)
class RouteDecision:
    """A JSON-friendly description of a deterministic routing decision."""

    goal: str
    normalized_goal: str
    skills: tuple[str, ...]
    matched_rules: tuple[str, ...]
    explanations: tuple[str, ...]
    explicit_override: bool

    @property
    def router_version(self) -> str:
        """Version persisted with task state for reproducible routing."""

        return "athena-router/1"

    @property
    def route_source(self) -> str:
        """Classify whether the decision was explicit, rule-based, or fallback."""

        if self.explicit_override:
            return "explicit"
        if self.matched_rules == ("default:integrity",):
            return "fallback"
        return "rule"

    def to_dict(self) -> dict[str, object]:
        """Return only standard JSON-compatible values."""

        return {
            "router_version": self.router_version,
            "route_source": self.route_source,
            "goal": self.goal,
            "normalized_goal": self.normalized_goal,
            "skills": list(self.skills),
            "matched_rules": list(self.matched_rules),
            "explanations": list(self.explanations),
            "explicit_override": self.explicit_override,
        }


@dataclass(frozen=True)
class _RoutingRule:
    name: str
    phrases: tuple[str, ...]
    skills: tuple[str, ...]
    explanation: str


def normalize_goal(goal: str) -> str:
    """Normalise Unicode and casing without discarding Chinese text."""

    if not isinstance(goal, str):
        raise TypeError("goal must be a string")
    normalized = unicodedata.normalize("NFKC", goal).casefold()
    return " ".join(normalized.split())


_RULES: tuple[_RoutingRule, ...] = (
    _RoutingRule(
        name="broad-paper-understanding",
        phrases=(
            "paper understanding",
            "understand this paper",
            "understand the paper",
            "explain this paper",
            "explain the paper",
            "read this paper",
            "理解这篇论文",
            "理解论文",
            "论文理解",
            "解读这篇论文",
            "解读论文",
            "论文解读",
            "解释这篇论文",
            "解释论文",
            "读懂论文",
            "把论文变得容易理解",
        ),
        skills=CORE_SKILL_ORDER,
        explanation=(
            "A broad paper-understanding goal uses citation context, an "
            "evidence check, and an explorable presentation."
        ),
    ),
    _RoutingRule(
        name="citation-context",
        phrases=(
            "citation",
            "citations",
            "cited by",
            "citation graph",
            "reference graph",
            "backward citation",
            "forward citation",
            "bibliography",
            "引用",
            "引文",
            "被引",
            "参考文献",
            "文献网络",
            "文献追踪",
            "追踪文献",
        ),
        skills=("citation-tracing",),
        explanation="The goal asks for citation or reference context.",
    ),
    _RoutingRule(
        name="claim-evidence-integrity",
        phrases=(
            "claim",
            "claims",
            "evidence",
            "verify",
            "verification",
            "audit",
            "uncertainty",
            "reproducibility",
            "research integrity",
            "论断",
            "证据",
            "核查",
            "验证",
            "审计",
            "不确定性",
            "可复现",
            "科研诚信",
        ),
        skills=(_INTEGRITY_SKILL,),
        explanation="The goal asks to connect claims with evidence or uncertainty.",
    ),
    _RoutingRule(
        name="explorable-output",
        phrases=(
            "explorable",
            "interactive",
            "interactive html",
            "html",
            "visualization",
            "visualisation",
            "easier to understand",
            "可探索",
            "交互式",
            "交互",
            "网页",
            "可视化",
            "易懂",
        ),
        skills=("explorable-paper",),
        explanation="The goal asks for an interactive or explorable output.",
    ),
)


_REQUEST_ALIASES: dict[str, str] = {
    "citation": "citation-tracing",
    "citations": "citation-tracing",
    "citation-tracing": "citation-tracing",
    "research-integrity": _INTEGRITY_SKILL,
    "integrity": _INTEGRITY_SKILL,
    "research-integrity-pipeline": _INTEGRITY_SKILL,
    "explorable": "explorable-paper",
    "explorable-paper": "explorable-paper",
}


def _contains_phrase(text: str, phrase: str) -> bool:
    """Match Latin phrases on token edges and CJK phrases as substrings."""

    normalized_phrase = normalize_goal(phrase)
    if re.search(r"[\u3400-\u9fff]", normalized_phrase):
        return normalized_phrase in text
    pattern = r"(?<![0-9a-z])" + re.escape(normalized_phrase) + r"(?![0-9a-z])"
    return re.search(pattern, text) is not None


def _canonical_requested_skill(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError("requested skill names must be strings")
    normalized = normalize_goal(value).replace("_", "-")
    normalized = re.sub(r"\s+", "-", normalized)
    try:
        return _REQUEST_ALIASES[normalized]
    except KeyError as exc:
        allowed = ", ".join(CORE_SKILL_ORDER)
        raise ValueError(
            f"unsupported core skill {value!r}; choose one of: {allowed}"
        ) from exc


def _requested_from_argument(
    requested_skills: str | Iterable[str] | None,
) -> tuple[str, ...]:
    if requested_skills is None:
        return ()
    values = (requested_skills,) if isinstance(requested_skills, str) else requested_skills
    requested = {_canonical_requested_skill(value) for value in values}
    return tuple(skill for skill in CORE_SKILL_ORDER if skill in requested)


def _requested_from_goal(normalized_goal: str) -> tuple[str, ...]:
    """Recognise explicit canonical skill invocations embedded in a goal."""

    requested: set[str] = set()
    for skill in CORE_SKILL_ORDER:
        escaped = re.escape(skill)
        patterns = (
            rf"(?:^|\s)skill\s*[:=]\s*{escaped}(?=$|\s|[,;])",
            rf"(?:^|\s)/{escaped}(?=$|\s|[,;])",
            rf"(?:^|\s)use\s+{escaped}(?=$|\s|[,;])",
            rf"使用\s*{escaped}(?=$|\s|[,，;；])",
        )
        if any(re.search(pattern, normalized_goal) for pattern in patterns):
            requested.add(skill)
    return tuple(skill for skill in CORE_SKILL_ORDER if skill in requested)


def _with_integrity_baseline(skills: Iterable[str]) -> tuple[str, ...]:
    selected = set(skills)
    selected.add(_INTEGRITY_SKILL)
    return tuple(skill for skill in CORE_SKILL_ORDER if skill in selected)


def route_goal(
    goal: str,
    requested_skills: str | Iterable[str] | None = None,
) -> RouteDecision:
    """Route *goal* to an ordered Alpha skill chain.

    An explicit skill request overrides keyword routing.  The mandatory
    integrity baseline is then added exactly once.  Without an explicit request,
    bilingual rules are combined and emitted in ``CORE_SKILL_ORDER`` regardless
    of keyword order.  An unmatched goal defaults to integrity review.
    """

    normalized_goal = normalize_goal(goal)
    requested = _requested_from_argument(requested_skills)
    if not requested:
        requested = _requested_from_goal(normalized_goal)

    if requested:
        rules = [f"explicit:{skill}" for skill in requested]
        explanations = [f"The user explicitly requested {skill}." for skill in requested]
        if _INTEGRITY_SKILL not in requested:
            rules.append("invariant:integrity-baseline")
            explanations.append(
                "Research integrity is included once as Athena's mandatory baseline."
            )
        return RouteDecision(
            goal=goal,
            normalized_goal=normalized_goal,
            skills=_with_integrity_baseline(requested),
            matched_rules=tuple(rules),
            explanations=tuple(explanations),
            explicit_override=True,
        )

    selected: set[str] = set()
    rules: list[str] = []
    explanations: list[str] = []
    for rule in _RULES:
        if any(_contains_phrase(normalized_goal, phrase) for phrase in rule.phrases):
            selected.update(rule.skills)
            rules.append(f"goal:{rule.name}")
            explanations.append(rule.explanation)

    if not selected:
        selected.add(_INTEGRITY_SKILL)
        rules.append("default:integrity")
        explanations.append(
            "No specialised rule matched, so Athena defaults to an integrity review."
        )
    elif _INTEGRITY_SKILL not in selected:
        selected.add(_INTEGRITY_SKILL)
        rules.append("invariant:integrity-baseline")
        explanations.append(
            "Research integrity is included once as Athena's mandatory baseline."
        )

    return RouteDecision(
        goal=goal,
        normalized_goal=normalized_goal,
        skills=tuple(skill for skill in CORE_SKILL_ORDER if skill in selected),
        matched_rules=tuple(rules),
        explanations=tuple(explanations),
        explicit_override=False,
    )


__all__ = ["CORE_SKILL_ORDER", "RouteDecision", "normalize_goal", "route_goal"]
