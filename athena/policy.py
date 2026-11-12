"""Fail-closed permission policy for the local-only Athena Alpha.

Only public/local reads, offline computation, and creation of a *new* derived
artifact inside a caller-supplied project sandbox are supported.  There is no
external-effect adapter in this Alpha, so approval text cannot make a network,
paid, destructive, overwrite, publishing, or messaging action available.
"""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import re
import stat
import unicodedata


@dataclass(frozen=True)
class PolicyDecision:
    """The result of evaluating one requested action."""

    allowed: bool
    intent: str
    permission_level: str | None
    reason: str
    matched_rules: tuple[str, ...]
    target: str | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "allowed": self.allowed,
            "intent": self.intent,
            "permission_level": self.permission_level,
            "reason": self.reason,
            "matched_rules": list(self.matched_rules),
            "target": self.target,
        }


_P0_NO_TARGET = {
    "offline-compute",
    "p0-offline-compute",
}

_P0_EXISTING_LOCAL_TARGET = {
    "public-read",
    "read-public",
    "read-local-public",
    "verify-local",
    "p0-public-read",
}

_P1_NEW_LOCAL_TARGET = {
    "create-artifact",
    "create-derived-artifact",
    "create-local-release",
    "local-create",
    "p1-create-derived-artifact",
}

# Ordered so a decision is stable when an intent contains several forbidden
# effects.  Substring matching is intentional: compound intents such as
# ``create-artifact-and-publish`` must not inherit the safe create permission.
_FORBIDDEN_EFFECTS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("delete", ("delete", "remove", "destroy", "purge")),
    ("overwrite", ("overwrite", "replace-existing", "clobber")),
    ("publish", ("publish", "make-public", "public-release")),
    ("send", ("send", "email", "message", "notify")),
    ("external-write", ("external-write", "upload", "push", "deploy")),
    (
        "network",
        (
            "network",
            "fetch",
            "download",
            "http",
            "browse-web",
            "web-search",
            "request-url",
        ),
    ),
    ("paid", ("paid", "purchase", "billing", "rent-gpu")),
)


def normalize_intent(intent: str) -> str:
    if not isinstance(intent, str):
        raise TypeError("intent must be a string")
    normalized = unicodedata.normalize("NFKC", intent).casefold().strip()
    normalized = re.sub(r"[\s_]+", "-", normalized)
    return re.sub(r"-+", "-", normalized)


def _contains_effect(intent: str, phrase: str) -> bool:
    pattern = r"(?<![0-9a-z])" + re.escape(phrase) + r"(?![0-9a-z])"
    return re.search(pattern, intent) is not None


def _is_link_or_reparse(path: Path) -> bool:
    try:
        metadata = path.lstat()
    except OSError:
        return False
    if stat.S_ISLNK(metadata.st_mode):
        return True
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    attributes = getattr(metadata, "st_file_attributes", 0)
    return bool(reparse_flag and attributes & reparse_flag)


def _existing_chain(path: Path):
    """Yield existing components from the filesystem anchor to *path*."""

    absolute = path.absolute()
    parts = absolute.parts
    if not parts:
        return
    current = Path(parts[0])
    if current.exists() or current.is_symlink():
        yield current
    for part in parts[1:]:
        current = current / part
        if current.exists() or current.is_symlink():
            yield current
        else:
            break


def _sandbox_target(
    project_root: str | os.PathLike[str] | None,
    target: str | os.PathLike[str] | None,
    *,
    must_exist: bool,
    must_be_new: bool,
) -> tuple[Path | None, str | None, str | None]:
    """Return ``(resolved_target, rule, error)`` for a sandboxed local path."""

    if project_root is None or target is None:
        return None, "path:missing", "a project root and target path are required"

    raw_root = os.fspath(project_root)
    raw_target = os.fspath(target)
    if not isinstance(raw_root, str) or not isinstance(raw_target, str):
        return None, "path:type", "project root and target must be filesystem paths"
    if "\x00" in raw_root or "\x00" in raw_target:
        return None, "path:nul", "NUL bytes are not valid in project paths"
    if ".." in re.split(r"[\\/]", raw_target):
        return None, "path:traversal", "path traversal is not allowed"

    root = Path(raw_root).absolute()
    if not root.exists() or not root.is_dir():
        return None, "path:root", "the project sandbox must be an existing directory"
    if any(_is_link_or_reparse(component) for component in _existing_chain(root)):
        return None, "path:symlink", "symlink or reparse-point sandboxes are not supported"

    candidate_input = Path(raw_target)
    candidate = candidate_input if candidate_input.is_absolute() else root / candidate_input
    if any(_is_link_or_reparse(component) for component in _existing_chain(candidate)):
        return None, "path:symlink", "symlink or reparse-point paths are not supported"

    try:
        resolved_root = root.resolve(strict=True)
        resolved_target = candidate.resolve(strict=False)
        root_key = os.path.normcase(os.fspath(resolved_root))
        target_key = os.path.normcase(os.fspath(resolved_target))
        if os.path.commonpath((root_key, target_key)) != root_key:
            return None, "path:outside-sandbox", "target is outside the project sandbox"
    except (OSError, RuntimeError, ValueError):
        return None, "path:invalid", "target path could not be validated safely"

    if must_exist and not resolved_target.exists():
        return None, "path:missing-target", "the local read target does not exist"
    if must_be_new and resolved_target.exists():
        return None, "effect:overwrite", "the target already exists; overwrite is unavailable"
    return resolved_target, "path:inside-sandbox", None


def _untrusted_rule(untrusted_content: object | None) -> tuple[str, ...]:
    if untrusted_content is None or untrusted_content == "":
        return ()
    return ("trust:untrusted-content-is-data",)


def authorize_action(
    intent: str,
    *,
    project_root: str | os.PathLike[str] | None = None,
    target: str | os.PathLike[str] | None = None,
    untrusted_content: object | None = None,
) -> PolicyDecision:
    """Evaluate an Alpha action without interpreting approval-like content.

    ``untrusted_content`` is deliberately opaque.  Its presence is reported for
    auditability, but its words never change a denied action into an allowed
    one.  This makes paper text, HTML, BibTeX, model output, and imported
    metadata incapable of granting permission.
    """

    normalized = normalize_intent(intent)
    trust_rules = _untrusted_rule(untrusted_content)

    for effect, phrases in _FORBIDDEN_EFFECTS:
        if any(_contains_effect(normalized, phrase) for phrase in phrases):
            return PolicyDecision(
                allowed=False,
                intent=normalized,
                permission_level=None,
                reason=f"{effect} actions are unavailable in the local-only Alpha",
                matched_rules=(f"deny:{effect}",) + trust_rules,
                target=os.fspath(target) if target is not None else None,
            )

    if normalized in _P0_NO_TARGET:
        if target is not None:
            resolved, path_rule, error = _sandbox_target(
                project_root, target, must_exist=True, must_be_new=False
            )
            if error:
                return PolicyDecision(
                    False,
                    normalized,
                    None,
                    error,
                    (path_rule,) + trust_rules,
                    os.fspath(target),
                )
            target_value = os.fspath(resolved)
            rules = ("allow:p0-offline-compute", path_rule) + trust_rules
        else:
            target_value = None
            rules = ("allow:p0-offline-compute",) + trust_rules
        return PolicyDecision(
            True,
            normalized,
            "P0",
            "offline computation has no external side effect",
            rules,
            target_value,
        )

    if normalized in _P0_EXISTING_LOCAL_TARGET:
        resolved, path_rule, error = _sandbox_target(
            project_root, target, must_exist=True, must_be_new=False
        )
        if error:
            return PolicyDecision(
                False,
                normalized,
                None,
                error,
                (path_rule,) + trust_rules,
                os.fspath(target) if target is not None else None,
            )
        return PolicyDecision(
            True,
            normalized,
            "P0",
            "an existing local public artifact may be read inside the sandbox",
            ("allow:p0-public-read", path_rule) + trust_rules,
            os.fspath(resolved),
        )

    if normalized in _P1_NEW_LOCAL_TARGET:
        resolved, path_rule, error = _sandbox_target(
            project_root, target, must_exist=False, must_be_new=True
        )
        if error:
            return PolicyDecision(
                False,
                normalized,
                None,
                error,
                (path_rule,) + trust_rules,
                os.fspath(target) if target is not None else None,
            )
        return PolicyDecision(
            True,
            normalized,
            "P1",
            "a new derived artifact may be created inside the project sandbox",
            ("allow:p1-new-local-artifact", path_rule) + trust_rules,
            os.fspath(resolved),
        )

    return PolicyDecision(
        allowed=False,
        intent=normalized,
        permission_level=None,
        reason="unknown or unsupported actions fail closed",
        matched_rules=("deny:unsupported",) + trust_rules,
        target=os.fspath(target) if target is not None else None,
    )


def require_authorized(
    intent: str,
    **kwargs: object,
) -> PolicyDecision:
    """Return an allowed decision or raise ``PermissionError``."""

    decision = authorize_action(intent, **kwargs)
    if not decision.allowed:
        raise PermissionError(decision.reason)
    return decision


__all__ = [
    "PolicyDecision",
    "authorize_action",
    "normalize_intent",
    "require_authorized",
]
