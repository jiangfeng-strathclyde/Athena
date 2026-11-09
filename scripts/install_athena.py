#!/usr/bin/env python3
"""Install selected Athena skills with staging, backups, and rollback."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
import tempfile
from pathlib import Path

if __package__:
    from .check_skill_dependencies import inspect_skill, needs_attention
else:
    from check_skill_dependencies import inspect_skill, needs_attention

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "skills"
FLAGGED = frozenset({"deepxiv", "paper-compile", "paper-poster-html"})
AGENT_DIRECTORIES = {
    "universal": (".agents", "skills"),
    "codex": (".agents", "skills"),  # Backward-compatible alias.
    "claude-code": (".claude", "skills"),
    "cursor": (".cursor", "skills"),
    "copilot": (".copilot", "skills"),
    "gemini": (".gemini", "skills"),
}


def agent_target(agent: str, home: Path | None = None) -> Path:
    root = home if home is not None else Path.home()
    return root.joinpath(*AGENT_DIRECTORIES[agent])


def auto_targets(home: Path | None = None) -> list[tuple[str, Path]]:
    """Use shared discovery; only Claude Code needs an additional native copy."""
    root = home if home is not None else Path.home()
    targets = [("universal", agent_target("universal", root))]
    if shutil.which("claude") or (root / ".claude").exists():
        targets.append(("claude-code", agent_target("claude-code", root)))
    return targets


def is_link(path: Path) -> bool:
    """Also reject Windows junctions/reparse points (including on Python 3.10)."""
    if not os.path.lexists(path):
        return False
    return path.is_symlink() or bool(
        getattr(path.lstat(), "st_file_attributes", 0) & 0x400
    )


def select_skills(names: list[str] | None = None,
                  allowed: list[str] | None = None) -> list[Path]:
    catalog = {p.name: p for p in SOURCE.iterdir()
               if p.is_dir() and (p / "SKILL.md").is_file()}
    allowed_set = set(allowed or [])
    if allowed_set - FLAGGED:
        raise ValueError("Unknown flagged skill authorization.")
    selected = set(names) if names else set(catalog) - (FLAGGED - allowed_set)
    if selected - set(catalog):
        raise ValueError("Unknown skill(s): " + ", ".join(sorted(selected - set(catalog))))
    if selected & (FLAGGED - allowed_set):
        raise ValueError("Review skills/BLOCKED_NOTE.md, then explicitly pass "
                         "--allow-flagged NAME for each flagged skill selected.")
    if not selected:
        raise ValueError("No installable skills found.")
    return [catalog[name] for name in sorted(selected)]


def validate_sources(skills: list[Path]) -> None:
    for source in skills:
        if is_link(source):
            raise ValueError(f"Linked source skill is unsupported: {source}")
        for directory, dirs, files in os.walk(source, followlinks=False):
            for name in dirs + files:
                item = Path(directory) / name
                if is_link(item):
                    raise ValueError(f"Linked source resource is unsupported: {item}")


def preflight(target: Path, skills: list[Path], force: bool) -> tuple[Path, list[str]]:
    expanded = target.expanduser()
    if is_link(expanded):
        raise ValueError(f"Target must not be a symlink or junction: {expanded}")
    target = expanded.resolve()
    repository = ROOT.resolve()
    if (target == repository or target in repository.parents
            or repository in target.parents or target == Path.home().resolve()
            or target == Path(target.anchor)):
        raise ValueError("Target must be a dedicated skills directory outside the Athena checkout, "
                         "not a drive root, home directory, or ancestor of the checkout.")
    if target.exists() and not target.is_dir():
        raise ValueError(f"Target is not a directory: {target}")
    conflicts = []
    for source in skills:
        destination = target / source.name
        if os.path.lexists(destination):
            if is_link(destination) or not destination.is_dir():
                raise ValueError(f"Refusing to replace a linked or non-directory entry: {destination}")
            conflicts.append(source.name)
    if conflicts and not force:
        raise FileExistsError(f"{len(conflicts)} same-named skill folders exist in {target}. "
                              "Use --force to back up and replace them.")
    return target, conflicts


def install(target: Path, force: bool, skills: list[Path] | None = None
            ) -> tuple[int, int, Path | None]:
    skills = select_skills() if skills is None else skills
    validate_sources(skills)
    target, _ = preflight(target, skills, force)
    target.parent.mkdir(parents=True, exist_ok=True)
    # Same filesystem as the target: commits and restores use directory renames.
    work = Path(tempfile.mkdtemp(prefix=".athena-update-", dir=target.parent))
    staged, backup = work / "staged", work / "backup"
    staged.mkdir()
    backup.mkdir()
    installed: list[str] = []
    saved: list[str] = []
    preserve_work = False
    created_target = False
    try:
        # A failed copy leaves every installed skill untouched.
        for source in skills:
            shutil.copytree(source, staged / source.name)
        preflight(target, skills, force)
        created_target = not target.exists()
        target.mkdir(exist_ok=True)
        try:
            for source in skills:
                destination = target / source.name
                if destination.exists():
                    destination.rename(backup / source.name)
                    saved.append(source.name)
                (staged / source.name).rename(destination)
                installed.append(source.name)
        except BaseException:
            # Restore in reverse order; keep recovery material if any restore fails.
            errors = []
            for name in reversed(installed):
                try:
                    (target / name).rename(staged / name)
                except OSError as exc:
                    errors.append(str(exc))
            for name in reversed(saved):
                try:
                    (backup / name).rename(target / name)
                except OSError as exc:
                    errors.append(str(exc))
            if errors:
                preserve_work = True
                raise OSError(f"Rollback incomplete; recovery files retained at {work}: "
                              + "; ".join(errors))
            if created_target:
                target.rmdir()
            raise
        preserve_work = bool(saved)
        return len(skills), len(saved), backup if saved else None
    finally:
        if not preserve_work:
            shutil.rmtree(work)
        elif staged.exists() and not any(staged.iterdir()):
            staged.rmdir()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    destination = parser.add_mutually_exclusive_group(required=True)
    destination.add_argument("--agent", choices=sorted(AGENT_DIRECTORIES))
    destination.add_argument("--target", type=Path, help="Dedicated user skills directory.")
    destination.add_argument("--auto", action="store_true",
                             help="Shared directory, plus Claude Code if detected.")
    parser.add_argument("--force", action="store_true", help="Back up and replace existing skills.")
    parser.add_argument("--dry-run", action="store_true", help="Validate and print the plan without writing files.")
    parser.add_argument("--skill", action="append", help="Install only this skill; repeat to select several.")
    parser.add_argument("--strict-packaging", action="store_true",
                        help="Stop before writing if selected skills have static packaging findings.")
    parser.add_argument("--allow-flagged", action="append", choices=sorted(FLAGGED),
                        help="Authorize this skill after reviewing skills/BLOCKED_NOTE.md; repeat as needed.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    targets = auto_targets() if args.auto else [
        ("custom", args.target) if args.target is not None
        else (args.agent, agent_target(args.agent))]
    completed = []
    try:
        skills = select_skills(args.skill, args.allow_flagged)
        validate_sources(skills)
        findings = [report for source in skills
                    if needs_attention(report := inspect_skill(source))]
        print(f"Static packaging check: {len(findings)} of {len(skills)} selected skills need review.")
        if findings:
            print("Packaging findings: " + ", ".join(report["skill"] for report in findings))
            print("Inspect details with: python scripts/check_skill_dependencies.py --json")
            if args.strict_packaging:
                raise ValueError("Selected skills have packaging findings; no installation was started. "
                                 "Review their dependencies or select research-integrity-pipeline.")
        # Check every destination before the first write. Runtime rollback is per target.
        plans = [(label, *preflight(target, skills, args.force)) for label, target in targets]
        resolved = [target for _, target, _ in plans]
        if len(set(resolved)) != len(resolved) or any(
                a in b.parents for a in resolved for b in resolved if a != b):
            raise ValueError("Installation targets must be distinct, non-nested directories.")
        for label, target, conflicts in plans:
            print(f"{'Would install' if args.dry_run else 'Plan'}: {len(skills)} skills "
                  f"for {label} at {target}; replace {len(conflicts)}.")
            existing_flagged = [name for name in FLAGGED if (target / name).exists()
                                and name not in {p.name for p in skills}]
            if existing_flagged:
                print("Existing unselected flagged skills are left untouched: "
                      + ", ".join(sorted(existing_flagged)))
        print("Default selection excludes flagged skills. See skills/BLOCKED_NOTE.md.")
        print("Static checks do not validate code references, runtime tools, credentials, or agent behavior.")
        if args.dry_run:
            return 0
        for label, target, _ in plans:
            count, replaced, backup = install(target, args.force, skills)
            completed.append(str(target))
            print(f"Installed {count} skills for {label}; updated {replaced}.")
            if backup:
                print(f"Previous versions retained at: {backup}")
        print("Start a new agent session and confirm skill discovery. "
              "For an evidence-backed research task, try research-integrity-pipeline.")
        return 0
    except (OSError, ValueError) as exc:
        print(f"Installation stopped: {exc}", file=sys.stderr)
        if completed:
            print("Earlier destinations remain installed: " + ", ".join(completed), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
