"""Command-line interface for Athena Research Bot Alpha."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

from . import __version__
from .state import (
    AthenaError,
    BlockedError,
    action_for_task,
    checkpoint_task,
    create_task,
    discover_project,
    init_project,
    project_status,
)


def _project_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--project", type=Path,
        help="Project root. Defaults to the nearest parent containing .athena.",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="athena",
        description="Persistent, local-first research projects and verifiable Research Releases.",
    )
    parser.add_argument("--version", action="version", version=f"Athena {__version__}")
    commands = parser.add_subparsers(dest="command", required=True)

    init = commands.add_parser("init", help="Create transparent local Athena project state.")
    init.add_argument("directory", nargs="?", type=Path, default=Path.cwd())
    init.add_argument("--name", required=True, help="Human-readable project name.")
    init.add_argument("--json", action="store_true")

    plan = commands.add_parser("plan", help="Route and persist a research goal.")
    _project_argument(plan)
    plan.add_argument("goal", help="Research question or desired outcome.")
    plan.add_argument("--source", action="append", default=[], help="Local file or HTTP(S) reference; repeatable.")
    plan.add_argument(
        "--skill", action="append",
        choices=["citation-tracing", "research-integrity-pipeline", "explorable-paper"],
        help="Select an exact core-skill subset; repeat as needed. Steps use canonical order.",
    )
    plan.add_argument("--json", action="store_true")

    status = commands.add_parser("status", help="Show persisted project and task state without changing it.")
    _project_argument(status)
    status.add_argument("--task")
    status.add_argument("--json", action="store_true")

    resume = commands.add_parser("resume", help="Return the stable next action for a compatible agent.")
    _project_argument(resume)
    resume.add_argument("--task")
    resume.add_argument("--json", action="store_true")

    checkpoint = commands.add_parser("checkpoint", help="Record a genuinely completed workflow step.")
    _project_argument(checkpoint)
    checkpoint.add_argument("--task", required=True)
    checkpoint.add_argument("--step", required=True)
    checkpoint.add_argument("--artifact", type=Path)
    checkpoint.add_argument("--note")
    checkpoint.add_argument("--expected-revision", type=int)
    checkpoint.add_argument("--json", action="store_true")

    export = commands.add_parser("export", help="Create an immutable local Research Release draft.")
    _project_argument(export)
    export.add_argument("--task", required=True)
    export.add_argument(
        "--release-version", "--version", dest="release_version", required=True,
        help="Semantic version or draft label for the local release.",
    )
    export.add_argument("--title")
    export.add_argument("--json", action="store_true")

    verify = commands.add_parser("verify", help="Verify a Research Release entirely offline.")
    verify.add_argument("release", type=Path)
    verify.add_argument("--json", action="store_true")
    return parser


def _emit(value: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False))
        return
    if "action" in value:
        if value["action"] is None:
            print(f"Task {value['task_id']} is complete.")
        else:
            action = value["action"]
            print(f"Next: {action['step_id']} — {action['skill']}")
            print(f"Instructions: {action['instruction_path']} ({action['instruction_sha256'][:12]})")
            print(f"Artifact: {action['result_contract']['artifact_path']}")
            print(f"Checkpoint: {action['result_contract']['checkpoint_command']}")
        return
    if "tasks" in value:
        print(f"Athena project: {value['name']} ({value['project_id']})")
        if not value["tasks"]:
            print("No tasks yet. Run `python -m athena plan \"<goal>\"`.")
        for task in value["tasks"]:
            marker = "*" if task["task_id"] == value["active_task_id"] else " "
            print(f"{marker} {task['task_id']}  {task['status']}  next={task['next_step'] or '-'}")
        return
    print(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False))


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "init":
            project = init_project(args.directory, args.name)
            value = {
                "created": True,
                "project_id": project["project_id"],
                "name": project["name"],
                "state_directory": ".athena",
                "privacy": "Local project state; nothing was uploaded.",
            }
            _emit(value, args.json)
            return 0
        if args.command == "plan":
            root = discover_project(args.project) if args.project else discover_project()
            task = create_task(root, args.goal, args.source, args.skill)
            value = {
                "created": True,
                "task_id": task["task_id"],
                "route": task["route"],
                "source_count": len(task["sources"]),
                "next_step": task["steps"][0]["step_id"],
            }
            _emit(value, args.json)
            return 0
        if args.command == "status":
            root = discover_project(args.project) if args.project else discover_project()
            _emit(project_status(root, args.task), args.json)
            return 0
        if args.command == "resume":
            root = discover_project(args.project) if args.project else discover_project()
            _emit(action_for_task(root, args.task), args.json)
            return 0
        if args.command == "checkpoint":
            root = discover_project(args.project) if args.project else discover_project()
            task = checkpoint_task(
                root,
                args.task,
                args.step,
                artifact=args.artifact,
                note=args.note,
                expected_revision=args.expected_revision,
            )
            _emit({
                "checkpointed": True,
                "task_id": task["task_id"],
                "revision": task["revision"],
                "status": task["status"],
                "next_step": (
                    next((step["step_id"] for step in task["steps"] if step["status"] != "complete"), None)
                ),
            }, args.json)
            return 0
        if args.command == "export":
            from .release import export_release
            root = discover_project(args.project) if args.project else discover_project()
            release = export_release(root, args.task, args.release_version, title=args.title)
            _emit(release, args.json)
            return 0
        if args.command == "verify":
            from .release import verify_release
            result = verify_release(args.release)
            _emit(result, args.json)
            return 0
    except BlockedError as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        return 3
    except AthenaError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"ERROR: filesystem operation failed: {exc}", file=sys.stderr)
        return 1
    return 1
