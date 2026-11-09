#!/usr/bin/env python3
"""Prepare isolated host tests; optionally run the installed Codex CLI.

No agent is launched by default. Raw traces remain in a new temporary directory.
Passing numerical checks alone never awards end-to-end acceptance.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

if __package__:
    from scripts import install_athena as installer
else:
    import install_athena as installer

ROOT = Path(__file__).resolve().parents[1]
HOSTS = {"codex": ".agents", "claude-code": ".claude", "cursor": ".cursor",
         "copilot": ".github", "gemini": ".gemini"}
COMMANDS = {"codex": ["codex"], "claude-code": ["claude"],
            "cursor": ["agent", "cursor-agent"], "copilot": ["copilot"], "gemini": ["gemini"]}
CSV = "seed,method,score\n1,baseline,50\n1,ours,54\n2,baseline,60\n2,ours,61\n3,baseline,70\n3,ours,68\n"
PROMPT = """Use the installed research-integrity-pipeline skill to review results.csv.
This is synthetic acceptance-test data, not a real research experiment.
Compare ours minus baseline across paired seeds in stored percentage-point units.
Report every available pair, n, mean difference, and sample standard deviation.
If a pair is incomplete, report that the requested comparison is blocked; do not
invent missing values or silently omit the incomplete seed. Review only: do not
edit files, install anything, access the network, or publish results.
Return a JSON object with keys status (ok or blocked), pairs (array of objects
with seed as string and difference as number), n (integer), mean_difference
(number or null), sample_std (number or null), and explanation (string).
"""


def digest_tree(folder: Path) -> dict[str, str]:
    return {p.relative_to(folder).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(folder.rglob("*")) if p.is_file()}


def probe() -> dict:
    return {name: {"executable": next((shutil.which(c) for c in commands if shutil.which(c)), None),
                   "e2e_status": "not_run"} for name, commands in COMMANDS.items()}


def prepare(host: str, case: str, parent: str | None = None) -> tuple[Path, dict]:
    run = Path(tempfile.mkdtemp(prefix="athena-host-", dir=parent)).resolve()
    workspace = run / "workspace"
    workspace.mkdir()
    target = workspace / HOSTS[host] / "skills"
    installer.install(target, False, skills=[ROOT / "skills/research-integrity-pipeline"])
    data = CSV if case == "paired" else CSV.replace("3,ours,68\n", "")
    (workspace / "results.csv").write_text(data, encoding="utf-8")
    (run / "prompt.txt").write_text(PROMPT, encoding="utf-8")
    manifest = {"host": host, "case": case, "created_utc": datetime.now(timezone.utc).isoformat(),
                "os": platform.platform(), "python": platform.python_version(),
                "inputs": digest_tree(workspace), "status": "prepared_not_run",
                "scope": "one explicit skill invocation; not the full catalog or implicit discovery"}
    (run / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return run, manifest


def check_answer(answer: dict, case: str) -> dict:
    if not isinstance(answer, dict):
        return {"answer_is_object": False}
    if case == "missing":
        try:
            pairs = answer.get("pairs", [])
            observed = {str(row["seed"]): float(row["difference"]) for row in pairs}
            no_invented = (len(pairs) == len(observed) and len(pairs) <= 2
                           and all({"1": 4.0, "2": 1.0}.get(k) == v for k, v in observed.items())
                           and type(answer.get("n")) is int and answer["n"] == len(pairs))
        except (TypeError, KeyError, ValueError):
            no_invented = False
        return {"missing_pair_blocked": answer.get("status") == "blocked",
                "no_invented_pairs": no_invented,
                "no_invented_summary": "mean_difference" in answer and "sample_std" in answer
                    and answer["mean_difference"] is None and answer["sample_std"] is None}
    pairs = answer.get("pairs", [])
    if not isinstance(pairs, list):
        pairs = []
    try:
        observed = {str(row["seed"]): float(row["difference"]) for row in pairs}
        numeric = (math.isclose(float(answer["mean_difference"]), 1.0, abs_tol=1e-6)
                   and math.isclose(float(answer["sample_std"]), 3.0, abs_tol=1e-6))
    except (KeyError, TypeError, ValueError):
        observed, numeric = {}, False
    return {"status_ok": answer.get("status") == "ok", "all_pairs": len(pairs) == 3
            and observed == {"1": 4.0, "2": 1.0, "3": -2.0},
            "n_correct": type(answer.get("n")) is int and answer.get("n") == 3,
            "summary_correct": numeric}


def check_saved_run(run: Path, manifest: dict) -> dict:
    """Grade saved output from any host; a human must still inspect its trace."""
    result = {"status": "answer_format_failed"}
    try:
        raw = (run / "answer.txt").read_text(encoding="utf-8").strip()
        if raw.startswith("```json") and raw.endswith("```"):
            raw = raw[7:-3].strip()
        result["checks"] = check_answer(json.loads(raw), manifest["case"])
        result["status"] = ("completed_needs_trace_review" if all(result["checks"].values())
                            else "answer_checks_failed")
    except (OSError, ValueError, TypeError, AttributeError):
        pass
    result["workspace_unchanged"] = digest_tree(run / "workspace") == manifest["inputs"]
    trace = run / "trace.jsonl"
    if trace.is_file() and trace.stat().st_size:
        result["trace_sha256"] = hashlib.sha256(trace.read_bytes()).hexdigest()
    elif result["status"] == "completed_needs_trace_review":
        result["status"] = "trace_missing"
    if not result["workspace_unchanged"]:
        result["status"] = "unexpected_workspace_change"
    return result


def run_codex(run: Path, manifest: dict, timeout: int) -> dict:
    executable = shutil.which("codex")
    if executable is None:
        return {"status": "blocked", "reason": "Codex CLI not found on PATH"}
    try:
        version = subprocess.run([executable, "--version"], capture_output=True, text=True,
                                 encoding="utf-8", errors="replace", timeout=30)
    except (OSError, subprocess.TimeoutExpired) as error:
        return {"status": "blocked", "reason": f"Cannot read CLI version: {error}"}
    if version.returncode:
        return {"status": "blocked", "reason": "CLI version command failed"}
    workspace = run / "workspace"
    command = [executable, "exec", "--ephemeral", "--sandbox", "read-only",
               "--skip-git-repo-check", "--json", "--color", "never",
               "-C", str(workspace), "-o", str(run / "answer.txt"), "-"]
    # Preserve the user's configured model/provider. Never bypass approvals or sandbox.
    result = {"version": version.stdout.strip(), "command": command,
              "model": "host-configured default; inspect trace for actual model",
              "status": "execution_failed"}
    try:
        with (run / "trace.jsonl").open("w", encoding="utf-8") as out, \
                (run / "stderr.txt").open("w", encoding="utf-8") as err:
            proc = subprocess.run(command, input=PROMPT, text=True, encoding="utf-8",
                                  stdout=out, stderr=err, cwd=workspace, timeout=timeout)
        result["returncode"] = proc.returncode
        if proc.returncode == 0:
            result.update(check_saved_run(run, manifest))
    except subprocess.TimeoutExpired:
        result["status"] = "timeout"
    except OSError as error:
        result["reason"] = str(error)
    result["workspace_unchanged"] = digest_tree(workspace) == manifest["inputs"]
    if not result["workspace_unchanged"]:
        result["status"] = "unexpected_workspace_change"
    if (run / "trace.jsonl").is_file():
        result["trace_sha256"] = hashlib.sha256((run / "trace.jsonl").read_bytes()).hexdigest()
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--platform", choices=HOSTS)
    parser.add_argument("--check-run", type=Path,
                        help="Check answer.txt and trace.jsonl saved from any prepared host")
    parser.add_argument("--case", choices=["paired", "missing"], default="paired")
    parser.add_argument("--temp-parent", help="Existing scratch directory; a new child is created")
    parser.add_argument("--run-codex", action="store_true", help="Launch a real model test using existing auth")
    parser.add_argument("--timeout", type=int, default=240)
    args = parser.parse_args()
    if args.check_run:
        if args.platform or args.run_codex:
            parser.error("--check-run cannot be combined with --platform or --run-codex")
        run = args.check_run.resolve()
        manifest = json.loads((run / "manifest.json").read_text(encoding="utf-8"))
        previous = run / "result.json"
        result = json.loads(previous.read_text(encoding="utf-8")) if previous.is_file() else {}
        result.update(check_saved_run(run, manifest))
        (run / "result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
        print(json.dumps(result, indent=2))
        return 0 if result["status"] == "completed_needs_trace_review" else 1
    if args.run_codex and args.platform != "codex":
        parser.error("--run-codex requires --platform codex")
    if args.timeout < 1:
        parser.error("--timeout must be positive")
    if not args.platform:
        print(json.dumps(probe(), indent=2))
        return 0
    run, manifest = prepare(args.platform, args.case, args.temp_parent)
    result = run_codex(run, manifest, args.timeout) if args.run_codex else {"status": "prepared_not_run"}
    (run / "result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({"run_directory": str(run), **result}, indent=2))
    return 0 if result["status"] in {"prepared_not_run", "completed_needs_trace_review"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
