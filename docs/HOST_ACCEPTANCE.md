# Cross-host acceptance tests

Installation checks answer whether files were copied. These tests check whether
an actual agent reads an installed skill, runs its helper, and handles the
result correctly. The [dated report](validation/2026-11-09.md) records outcomes;
this page describes how to reproduce them.

## Prepare an isolated test

Use Python 3.10+ from the Athena checkout. With no arguments, the harness only
looks for CLI executables on PATH; it does not inspect credentials or launch AI.

```text
python scripts/host_acceptance.py
python scripts/host_acceptance.py --platform cursor --case paired
python scripts/host_acceptance.py --platform cursor --case missing
```

Replace `cursor` with any platform below. Each invocation creates a new temporary
run directory containing `workspace/`, `prompt.txt`, and a manifest of input
hashes. Only `research-integrity-pipeline` and its helper are installed. Nothing
is installed into personal skill directories, and no login or purchase occurs.

| Platform argument | Prepared project directory | Actual execution route |
|---|---|---|
| `codex` | `.agents/skills` | Installed Codex CLI; optional runner below |
| `claude-code` | `.claude/skills` | Start Claude Code in `workspace/` |
| `cursor` | `.cursor/skills` | Open `workspace/` in Cursor Agent, or use its Agent CLI |
| `copilot` | `.github/skills` | Open `workspace/` in a compatible Copilot Agent client |
| `gemini` | `.gemini/skills` | Start Gemini CLI in `workspace/` |

These are **project** directories for the test, not the personal installation
directories used by `install_athena.py`. Directory support is documented by
[Codex](https://developers.openai.com/codex/skills/),
[Claude Code](https://code.claude.com/docs/en/skills),
[Cursor](https://cursor.com/docs/skills),
[Copilot](https://docs.github.com/en/copilot/concepts/customizations/agent-skills),
and [Gemini CLI](https://geminicli.com/docs/cli/skills/). Use a compatible version
and the host's normal workspace trust flow; do not bypass approval controls.

## Execute with a real host

In a fresh session rooted at the generated `workspace/`, send the exact text
from `prompt.txt`. Record the client version, OS, selected model if exposed,
Python version, skill hashes, and any relevant permissions. Keep expected
answers outside the agent workspace. Existing global configuration may still
load: this is an isolated project fixture, not a clean account or provider.

Save the final JSON as `answer.txt` beside `manifest.json`. Save the tool trace
as `trace.jsonl`, using the host's export when available. For a manually recorded
trace, retain command/argument, actual output, exit status, and skill-reading
events; identify it as a manual transcription and retain the original export
or screenshots privately. Do not reconstruct a trace from the final answer.

For an already authenticated Codex CLI, the harness can execute and capture
both files directly:

```text
python scripts/host_acceptance.py --platform codex --case paired --run-codex
python scripts/host_acceptance.py --platform codex --case missing --run-codex
```

This makes real model calls and may use account quota. It uses a read-only,
ephemeral session and the host's configured model. It does not install a CLI,
configure credentials, or disable safeguards. Other platforms use their native
interface; their launch flags are not emulated by calling Codex under a different
directory name. The Cursor editor launcher alone is not an Agent CLI.

## Grade the output and inspect the trace

For any of the five hosts, run:

```text
python scripts/host_acceptance.py --check-run "/absolute/path/to/athena-host-RUN"
```

This updates the run's `result.json`, compares the output with the expected
arithmetic, requires a nonempty trace, and checks every original workspace file
hash and the file inventory. The result remains `completed_needs_trace_review`
until a reviewer examines the actual trace. A trace's existence proves neither
its accuracy nor that the right skill ran.

| Case | Expected result |
|---|---|
| `paired` | Seed differences 4, 1, -2; n = 3; mean = 1; sample SD = 3 |
| `missing` | Seed 3 reported incomplete; status `blocked`; no aggregate mean or SD; no invented third result |

For each case, verify that the trace shows the installed `SKILL.md` being read
and the installed `paired_summary.py` being executed on this fixture. For the
missing case, verify that the helper error becomes an explicit limitation in
the answer. Inspect for unexpected network calls, dependency installation,
publication, or changes outside the workspace. Hash checks cover only the
workspace, not all account or filesystem side effects.

Record each case as passed, failed, or not run, with the evidence location and
reason. Record unknown model identity as unknown. A missing executable or login
is an unavailable test environment, not a successful compatibility result.

## Scope and evidence handling

These cases explicitly name one skill. They do not test implicit activation,
all 110 skills, web/mobile chat, citations, reviewer independence, or scientific
validity of real experiments. Text-chat Lite Loader use needs a separate test
of the capabilities actually offered by that app; it cannot inherit a local
CLI result.

Keep raw traces private by default: they may contain local paths, configuration,
or account details. Publish only reviewed, redacted evidence and its limitations.
No authenticated host tests run in repository CI. Unit tests exercise fixture
preparation and grading without launching a model; they are not host E2E passes.
