# Research Bot Alpha

**Athena is an open-source Research Bot that turns a research question, paper,
or dataset into a source-linked, versioned Research Release.**

The current release is a **local-first Alpha control plane**. It makes research
work inspectable and resumable, but it is not a hosted chat service.

## What the Alpha provides

- Transparent project state in a local `.athena/` directory.
- Deterministic routing across the Alpha core:
  `citation-tracing`, `research-integrity-pipeline`, and
  `explorable-paper`.
- One stable next action at a time, including an absolute, readable path to the
  installed skill instruction, its pinned hash, output location, permission
  boundary, and checkpoint contract.
- Artifact copies with media type, byte count, and SHA-256.
- A strict export gate and an offline release verifier.
- A separate optional catalog of [110 research skills](SKILL_COVERAGE.md).

Routing can select a bounded subset for a goal. When a project uses all three
core stages, their canonical order is `citation-tracing` →
`research-integrity-pipeline` → `explorable-paper` → Research Release.
The control plane returns one action at a time; it does not automatically
execute those skills.

## What it does not provide

- No Athena-hosted model or autonomous research executor.
- No hosted account, browser session, database, or cloud file store.
- No automatic source download by the core CLI.
- No automatic publication, sending, paid compute, deletion, or external write.
- No guarantee that a model, source, citation, or scientific conclusion is
  correct merely because a release verifies.

A compatible local agent performs the research step. Its model behavior, tool
access, network use, accounts, and data handling remain governed by that host.
The static website does not receive project files.

## Lifecycle

```text
init → plan → resume → execute locally → create artifact → checkpoint
                                      ↘ repeat until every step is complete
complete task + registered artifact → export → verify
```

Task state is explicit:

| Level | States |
|---|---|
| Task | `planned`, `in_progress`, `complete`, or `blocked` |
| Step | `pending`, `complete`, or `blocked` |

`resume` does not mutate the task or call a model. Its action contains an
absolute, readable `instruction_path` to the actual `SKILL.md` in the installed
Athena catalog and the matching `instruction_sha256` pinned when the task was
planned. `checkpoint` may be used only for the next pending step, after the work
is genuinely complete. The action supplies a fixed `result_contract.artifact_path`;
after writing the result there, a compatible agent can execute the returned
`checkpoint_argv` directly without a shell. The self-contained
`checkpoint_command` is provided for shell-only hosts and needs no placeholder
replacement or appended arguments. On Windows, that fallback carries the exact
argv inside an encoded PowerShell command so `cmd.exe` cannot reinterpret `%`,
`!`, `&`, `^`, spaces, or apostrophes in Python and project paths. Export does
not change task state. If the pinned instructions later change, `resume` blocks
instead of silently changing the task contract.

If either the task or its next step is `blocked`, `resume` and `checkpoint`
both fail closed without advancing the task or registering an artifact. The
Alpha has no in-place automatic unlock transition. Correct the input or source
problem, then use `plan` to create a new task; do not edit `.athena/` state by
hand.

## Export gate

`export` is blocked unless:

1. the requested task has status `complete`;
2. every planned step is complete;
3. at least one artifact is registered;
4. each artifact is a regular file inside the expected local artifact tree;
5. its current byte count and SHA-256 match the checkpoint record; and
6. the requested release version and output path are safe.

This gate proves package integrity and lifecycle completion. It does not prove
scientific truth or replace expert review.

## Research Release layout

An exported draft is stored below
`.athena/releases/<version>-<content-hash>/` and contains:

- `README.md` — human-readable release summary;
- `task.json` — the frozen goal, route, step state, redacted source references,
  instruction hashes, and artifacts;
- `records/` — strict JSONL claims, evidence, and decision logs bound to this
  task only;
- `artifacts/` — checkpointed outputs;
- `manifest.json` — deterministic file inventory and hashes; and
- `release.json` — release metadata such as the hash-bound completed-task
  revision time and visibility.

The default visibility is `private-local-draft`. During export, Athena verifies
the completed bundle before atomically advancing the local `current.json`
pointer. A later `verify` checks that release without changing it. Neither
command uploads or publishes the release. The immutable release's `created_at`
is the completed task revision time, so rebuilding identical state keeps the
same content identity. `current.json.updated_at` records the most recent
successful export or reuse invocation.

### Records contract

Each non-empty source record must be a strict UTF-8 JSON object on one JSONL
line and must carry a valid `task_id`. Blank lines, duplicate keys, malformed
JSON, non-finite numbers, missing or invalid task IDs, and non-object values are
rejected. Finite decimal numbers must also survive Athena's deterministic
binary64 round trip without changing value; record higher-precision scientific
values as strings instead of allowing silent rounding or underflow. UTF-16
surrogate escapes that cannot be emitted as strict UTF-8 are rejected. Export
selects only records belonging to the requested task; every record in the
resulting release must carry that selected task ID, and offline verification
fails if any packaged record names another task. This prevents one project's
claim, evidence, or decision log from leaking into another project's release.

## Sources and trust

Local source files are fingerprinted when a task is planned, and their usable
absolute paths remain in private `.athena/` project state. Export replaces each
such locator with `[private-local-source]`; it never places the absolute path in
the Research Release. For HTTP(S) references, Athena redacts recognized
credential-bearing query values and removes fragments before storing a source;
release export also blocks recognized credential-bearing URLs. This scanner is
conservative, not an exhaustive secret manager, so do not supply credentials in
URLs. The Alpha CLI does not fetch remote contents. Sources, skill text, and
artifacts are data—not authorization. The default action contract forbids network
use and consequential external effects until a user separately approves them
through the chosen host.

## Privacy boundary

The core CLI uses local files and does not make network calls. That is a
statement about this Alpha runtime, not a promise about third-party agents,
models, sync features, or tools. The `.athena/` directory is local but is not
encrypted; protect it like any other research directory.

State validation is intentionally strict. Task files created before instruction
hash pinning are not silently migrated; create a new plan. A writer lock is also
never stolen merely because it is old. If a process crashes, first confirm that
no Athena writer is active, then remove `.athena/.write-lock` manually and retry.
Athena rejects links and Windows reparse points found on managed paths, but it is
not an operating-system sandbox: do not let an untrusted same-user process race
changes inside a live project directory.

## Current scope

The Alpha is deliberately small: local state, bounded routes across three core stages, artifact
checkpoints, and verifiable release packaging. The broader skill catalog remains
available for compatible hosts, but catalog presence is not runtime readiness.
See [validation](VALIDATION.md), [FAQ](FAQ.md), and the
[roadmap](../ROADMAP.md) for the current boundary.
