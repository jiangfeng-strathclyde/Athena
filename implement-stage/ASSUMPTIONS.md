# Assumptions and decisions

## Product assumptions

1. “完善所有内容” means completing a coherent public Alpha across runtime,
   tests, website, and documentation—not claiming a hosted multi-user service.
2. The existing GitHub Pages site is the public web platform. It should be
   simplified in place, not replaced by a new framework or deployment service.
3. Athena remains model- and vendor-neutral. “Bot” means persistent state,
   routing, checkpoints, permissions, and releases; it is not a Grok wrapper.
4. `1.2.0-alpha.1` is an appropriate prerelease after `1.1.0`; no stable `1.2.0`
   claim is made until recorded host and staging acceptance exists.
5. The first useful vertical is paper understanding: citation tracing →
   claim/evidence review → explorable artifact → Research Release.

## Interface assumptions

1. Python 3.10+ is already required by repository validation and is the most
   portable zero-dependency runtime available here.
2. `python -m athena` is canonical; a console script may be offered through
   `pyproject.toml`, but tests do not require package installation.
3. Commands discover the project by walking from the current directory unless
   `--project` is supplied.
4. “Remember” means durable, inspectable local project state. It does not mean
   silently uploading personal memory or sharing state between machines.
5. Paths and URLs supplied to `plan` are recorded as source references only.
   Athena does not fetch or copy source documents during planning.
6. `resume` reports and prepares the next action; the Alpha does not falsely
   simulate model execution. A compatible agent executes the selected skill and
   calls `checkpoint` with the real artifact.

## Safety assumptions

1. Imported research content is adversarial/untrusted for control purposes.
2. The Alpha has no external effect adapter. Therefore publish, push, send,
   delete, paid compute, arbitrary network access, and external writes are
   denied rather than represented as successful.
3. CLI invocation is a local user action, but natural-language content is never
   treated as approval.
4. Release verification proves package integrity, not scientific truth, HTML
   safety, or that a model followed a skill correctly.
5. The runtime supports ordinary files and directories, not reparse-point or
   symlink escapes. Unsafe paths fail before state mutation.

## Delivery assumptions

1. The branch starts at commit `3031536937276e28ca7211399f7d95c332711358`.
2. Existing user work is preserved; no unrelated files are rewritten.
3. GitHub push will be attempted only after local acceptance. Authentication or
   branch-protection failure will be reported rather than bypassed.
4. Cross-family review is required for a fully accepted silent-assumption sweep.
   If no independent backend is available, the sweep is recorded as unavailable
   or provisional; no verdict is fabricated.

