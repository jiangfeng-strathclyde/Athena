#!/usr/bin/env python3
"""Build and exercise Athena's wheel without using the repository or network."""

from __future__ import annotations

import json
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Any, Sequence


class SmokeFailure(RuntimeError):
    """A wheel smoke-test invariant failed."""


def run(command: Sequence[str], *, cwd: Path, env: dict[str, str]) -> str:
    result = subprocess.run(
        [str(part) for part in command],
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode != 0:
        rendered = subprocess.list2cmdline([str(part) for part in command])
        raise SmokeFailure(
            f"Command failed with exit code {result.returncode}: {rendered}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )
    return result.stdout


def run_json(command: Sequence[str], *, cwd: Path, env: dict[str, str]) -> dict[str, Any]:
    output = run(command, cwd=cwd, env=env)
    try:
        value = json.loads(output)
    except json.JSONDecodeError as exc:
        raise SmokeFailure(f"Command did not return JSON:\n{output}") from exc
    if not isinstance(value, dict):
        raise SmokeFailure(f"Expected a JSON object, got {type(value).__name__}.")
    return value


def run_shell_json(command: str, *, cwd: Path, env: dict[str, str]) -> dict[str, Any]:
    result = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        shell=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode != 0:
        raise SmokeFailure(
            f"Shell checkpoint failed with exit code {result.returncode}.\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )
    try:
        value = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise SmokeFailure(f"Shell checkpoint did not return JSON:\n{result.stdout}") from exc
    if not isinstance(value, dict):
        raise SmokeFailure(f"Expected a JSON object, got {type(value).__name__}.")
    return value


def venv_python(venv: Path) -> Path:
    if os.name == "nt":
        return venv / "Scripts" / "python.exe"
    return venv / "bin" / "python"


def source_skill_resources(source: Path) -> set[str]:
    skills = source / "skills"
    resources: set[str] = set()
    for candidate in skills.rglob("*"):
        relative = candidate.relative_to(skills)
        if not candidate.is_file() or "__pycache__" in relative.parts or candidate.suffix == ".pyc":
            continue
        resources.add(f"skills/{relative.as_posix()}")
    return resources


def verify_wheel_resources(wheel: Path, source: Path) -> tuple[int, int]:
    expected = source_skill_resources(source)
    with zipfile.ZipFile(wheel) as archive:
        packaged = {
            name
            for name in archive.namelist()
            if name.startswith("skills/") and not name.endswith("/")
        }
    if packaged != expected:
        missing = sorted(expected - packaged)
        unexpected = sorted(packaged - expected)
        raise SmokeFailure(
            "Wheel skill resources differ from the source catalog. "
            f"Missing: {missing or 'none'}; unexpected: {unexpected or 'none'}."
        )
    required_core_resources = {
        "skills/citation-tracing/references/output-contract.md",
        "skills/explorable-paper/references/quality-gates.md",
        "skills/explorable-paper/scripts/validate_explorable.py",
        "skills/research-integrity-pipeline/scripts/paired_summary.py",
    }
    missing_core_resources = sorted(required_core_resources - packaged)
    if missing_core_resources:
        raise SmokeFailure(
            f"Wheel is missing referenced Alpha core resources: {missing_core_resources}."
        )
    instruction_count = sum(name.endswith("/SKILL.md") for name in packaged)
    return len(packaged), instruction_count


def main() -> int:
    repository = Path(__file__).resolve().parents[1]
    environment = os.environ.copy()
    environment.update(
        {
            "PIP_CONFIG_FILE": os.devnull,
            "PIP_DISABLE_PIP_VERSION_CHECK": "1",
            "PIP_NO_INDEX": "1",
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONNOUSERSITE": "1",
            "PYTHONUTF8": "1",
        }
    )
    environment.pop("PYTHONPATH", None)

    try:
        with tempfile.TemporaryDirectory(prefix="athena-wheel-smoke-") as temporary:
            root = Path(temporary).resolve()
            if root == repository or repository in root.parents:
                raise SmokeFailure("Temporary smoke-test directory must be outside the repository.")

            source = root / "source"
            wheelhouse = root / "wheelhouse"
            virtualenv = root / "%ATHENA_PERCENT_SENTINEL% venv'quote !&^"
            project = root / "%ATHENA_PERCENT_SENTINEL% project'quote !&^ ~~~"
            environment["ATHENA_PERCENT_SENTINEL"] = "must-not-expand"
            wheelhouse.mkdir()
            shutil.copytree(
                repository,
                source,
                ignore=shutil.ignore_patterns(
                    ".git",
                    ".athena",
                    ".mypy_cache",
                    ".pytest_cache",
                    "__pycache__",
                    "*.egg-info",
                    "*.pyc",
                    "build",
                    "dist",
                ),
            )
            cache_sentinels = (
                source / "skills" / "wheel-smoke.pyc",
                source / "skills" / "__pycache__" / "wheel-smoke.cache",
                source / "skills" / "explorable-paper" / "scripts" / "__pycache__" / "wheel-smoke.pyc",
            )
            for sentinel in cache_sentinels:
                sentinel.parent.mkdir(parents=True, exist_ok=True)
                sentinel.write_bytes(b"must not be packaged")

            run(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "wheel",
                    "--no-index",
                    "--no-deps",
                    "--no-build-isolation",
                    "--wheel-dir",
                    str(wheelhouse),
                    str(source),
                ],
                cwd=root,
                env=environment,
            )
            wheels = list(wheelhouse.glob("athena_research_bot-*.whl"))
            if len(wheels) != 1:
                raise SmokeFailure(f"Expected one Athena wheel, found {len(wheels)}.")
            resource_count, instruction_count = verify_wheel_resources(wheels[0], source)

            run([sys.executable, "-m", "venv", str(virtualenv)], cwd=root, env=environment)
            python = venv_python(virtualenv)
            run(
                [
                    str(python),
                    "-m",
                    "pip",
                    "install",
                    "--no-index",
                    "--no-deps",
                    str(wheels[0]),
                ],
                cwd=root,
                env=environment,
            )

            run_json(
                [str(python), "-I", "-m", "athena", "init", str(project), "--name", "Wheel smoke project", "--json"],
                cwd=root,
                env=environment,
            )
            planned = run_json(
                [
                    str(python),
                    "-I",
                    "-m",
                    "athena",
                    "plan",
                    "--project",
                    str(project),
                    "Audit the supplied evidence",
                    "--skill",
                    "research-integrity-pipeline",
                    "--json",
                ],
                cwd=root,
                env=environment,
            )
            resumed = run_json(
                [str(python), "-I", "-m", "athena", "resume", "--project", str(project), "--json"],
                cwd=root,
                env=environment,
            )

            if resumed.get("task_id") != planned.get("task_id"):
                raise SmokeFailure("Resume did not return the task created by plan.")
            action = resumed.get("action")
            if not isinstance(action, dict):
                raise SmokeFailure("Resume did not return an actionable step.")
            if action.get("skill") != "research-integrity-pipeline":
                raise SmokeFailure("Resume returned the wrong skill.")
            instruction_value = action.get("instruction_path")
            if not isinstance(instruction_value, str):
                raise SmokeFailure("Resume did not return an instruction path.")
            instruction = Path(instruction_value)
            if not instruction.is_absolute() or not instruction.is_file():
                raise SmokeFailure(
                    "Resume instruction path is not an absolute, readable installed resource: "
                    f"{instruction_value!r}."
                )
            resolved_instruction = instruction.resolve()
            if virtualenv not in resolved_instruction.parents:
                raise SmokeFailure(
                    "Resume instruction path did not resolve inside the installed virtualenv: "
                    f"{resolved_instruction}."
                )
            if resolved_instruction.name != "SKILL.md" or resolved_instruction.parent.name != action["skill"]:
                raise SmokeFailure("Resume returned the wrong installed skill instruction path.")
            digest = action.get("instruction_sha256")
            if not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None:
                raise SmokeFailure("Resume did not return a valid pinned instruction digest.")
            if hashlib.sha256(resolved_instruction.read_bytes()).hexdigest() != digest:
                raise SmokeFailure("Installed skill instructions do not match the pinned digest.")

            result_contract = action.get("result_contract")
            if not isinstance(result_contract, dict):
                raise SmokeFailure("Resume did not return a result contract.")
            artifact_value = result_contract.get("artifact_path")
            checkpoint_argv = result_contract.get("checkpoint_argv")
            checkpoint_command = result_contract.get("checkpoint_command")
            if (
                not isinstance(artifact_value, str)
                or not isinstance(checkpoint_argv, list)
                or not isinstance(checkpoint_command, str)
            ):
                raise SmokeFailure("Result contract is missing an executable checkpoint contract.")
            if checkpoint_argv[:4] != [str(python), "-m", "athena", "checkpoint"]:
                raise SmokeFailure("Result contract checkpoint argv does not target the installed runtime.")
            artifact = Path(artifact_value)
            if not artifact.is_absolute() or artifact.parent != Path(action["output_directory"]):
                raise SmokeFailure("Result contract artifact path is not inside its action output directory.")
            artifact.write_text("installed-wheel evidence\n", encoding="utf-8")
            checkpointed = run_shell_json(checkpoint_command, cwd=root, env=environment)
            if checkpointed.get("status") != "complete":
                raise SmokeFailure("Installed wheel did not complete the checkpointed task.")

            released = run_json(
                [
                    str(python),
                    "-I",
                    "-m",
                    "athena",
                    "export",
                    "--project",
                    str(project),
                    "--task",
                    str(planned["task_id"]),
                    "--release-version",
                    "0.0.1",
                    "--json",
                ],
                cwd=root,
                env=environment,
            )
            verified = run_json(
                [
                    str(python),
                    "-I",
                    "-m",
                    "athena",
                    "verify",
                    str(released["release_path"]),
                    "--json",
                ],
                cwd=root,
                env=environment,
            )
            if verified.get("verified") is not True:
                raise SmokeFailure("Installed wheel did not verify its exported Research Release.")

            print(
                "PASS: offline wheel completed and verified a Research Release outside the repository "
                f"with {resource_count} complete skill resources "
                f"({instruction_count} SKILL.md files)."
            )
        return 0
    except (OSError, SmokeFailure, zipfile.BadZipFile) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
