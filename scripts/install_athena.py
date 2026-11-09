#!/usr/bin/env python3
"""Install every Athena skill for one or more compatible AI agents."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "skills"
AGENT_DIRECTORIES = {
    "universal": (".agents", "skills"),
    "codex": (".agents", "skills"),  # Backward-compatible alias.
    "claude-code": (".claude", "skills"),
    "cursor": (".cursor", "skills"),
    "copilot": (".copilot", "skills"),
    "gemini": (".gemini", "skills"),
}

DETECTION_HINTS = {
    "claude-code": ("claude", ".claude"),
    "cursor": ("cursor", ".cursor"),
    "copilot": ("copilot", ".copilot"),
    "gemini": ("gemini", ".gemini"),
}


def agent_target(agent: str, home: Path | None = None) -> Path:
    """Return the user-level skills directory for a named agent."""
    root = home if home is not None else Path.home()
    return root.joinpath(*AGENT_DIRECTORIES[agent])


def auto_targets(home: Path | None = None) -> list[tuple[str, Path]]:
    """Choose a portable target plus native directories for detected agents."""
    root = home if home is not None else Path.home()
    targets = [("universal", agent_target("universal", root))]
    for agent, (executable, config_dir) in DETECTION_HINTS.items():
        if shutil.which(executable) or (root / config_dir).exists():
            targets.append((agent, agent_target(agent, root)))
    return targets


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install Athena's skills once for one or more AI agents."
    )
    destination = parser.add_mutually_exclusive_group(required=True)
    destination.add_argument(
        "--agent",
        choices=sorted(AGENT_DIRECTORIES),
        help="Agent whose user-level skills directory should be used.",
    )
    destination.add_argument(
        "--target",
        type=Path,
        help="Custom skills directory. Use this for another SKILL.md-compatible agent.",
    )
    destination.add_argument(
        "--auto",
        action="store_true",
        help=(
            "Install to the universal directory and to native directories for "
            "compatible agents detected on this computer."
        ),
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace same-named skill folders already present in the target.",
    )
    return parser.parse_args()


def install(target: Path, force: bool) -> tuple[int, int]:
    skill_dirs = sorted(
        path for path in SOURCE.iterdir() if path.is_dir() and (path / "SKILL.md").is_file()
    )
    target = target.expanduser().resolve()
    target.mkdir(parents=True, exist_ok=True)

    conflicts = [path.name for path in skill_dirs if (target / path.name).exists()]
    if conflicts and not force:
        preview = ", ".join(conflicts[:5])
        suffix = " ..." if len(conflicts) > 5 else ""
        raise FileExistsError(
            f"{len(conflicts)} same-named skill folder(s) already exist: "
            f"{preview}{suffix}. Re-run with --force to update them."
        )

    for source in skill_dirs:
        destination = target / source.name
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(source, destination)

    return len(skill_dirs), len(conflicts)


def target_conflicts(target: Path) -> list[str]:
    """Return Athena skill names that already exist at a target."""
    resolved = target.expanduser().resolve()
    return sorted(
        source.name
        for source in SOURCE.iterdir()
        if source.is_dir()
        and (source / "SKILL.md").is_file()
        and (resolved / source.name).exists()
    )


def main() -> int:
    args = parse_args()
    if args.auto:
        targets = auto_targets()
    elif args.target is not None:
        targets = [("custom", args.target)]
    else:
        targets = [(args.agent, agent_target(args.agent))]

    if not args.force:
        blocked = [
            (label, target, target_conflicts(target))
            for label, target in targets
        ]
        blocked = [item for item in blocked if item[2]]
        if blocked:
            for label, target, conflicts in blocked:
                preview = ", ".join(conflicts[:5])
                suffix = " ..." if len(conflicts) > 5 else ""
                print(
                    f"Installation stopped for {label}: {len(conflicts)} same-named "
                    f"skill folder(s) already exist in {target.expanduser().resolve()}: "
                    f"{preview}{suffix}.",
                    file=sys.stderr,
                )
            print("Re-run with --force to update them.", file=sys.stderr)
            return 1

    total_installed = 0
    total_replaced = 0
    for label, target in targets:
        try:
            installed, replaced = install(target, args.force)
        except (FileExistsError, OSError) as exc:
            print(f"Installation stopped for {label}: {exc}", file=sys.stderr)
            return 1
        total_installed += installed
        total_replaced += replaced
        print(f"Installed {installed} Athena skills for {label}: {target.expanduser().resolve()}")

    if len(targets) > 1:
        print(f"Configured {len(targets)} skill directories ({total_installed} copies).")
    if total_replaced:
        print(f"Updated {total_replaced} existing Athena skill folder(s).")
    print("Start a new agent session, then describe your research goal normally.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
