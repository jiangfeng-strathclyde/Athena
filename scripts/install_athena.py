#!/usr/bin/env python3
"""Install every Athena skill into a user-level agent skills directory."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "skills"
DEFAULT_TARGETS = {
    "codex": Path.home() / ".agents" / "skills",
    "claude-code": Path.home() / ".claude" / "skills",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install Athena's skills once for an agent user account."
    )
    parser.add_argument(
        "--agent",
        choices=sorted(DEFAULT_TARGETS),
        help="Agent whose user-level skills directory should be used.",
    )
    parser.add_argument(
        "--target",
        type=Path,
        help="Custom skills directory. Use this for another SKILL.md-compatible agent.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace same-named skill folders already present in the target.",
    )
    args = parser.parse_args()
    if (args.agent is None) == (args.target is None):
        parser.error("choose exactly one of --agent or --target")
    return args


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


def main() -> int:
    args = parse_args()
    target = args.target if args.target is not None else DEFAULT_TARGETS[args.agent]
    try:
        installed, replaced = install(target, args.force)
    except (FileExistsError, OSError) as exc:
        print(f"Installation stopped: {exc}", file=sys.stderr)
        return 1

    print(f"Installed {installed} Athena skills in {target.expanduser().resolve()}")
    if replaced:
        print(f"Updated {replaced} existing Athena skill folder(s).")
    print("Start a new agent session, then describe your research goal normally.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
