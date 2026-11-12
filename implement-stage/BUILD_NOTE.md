# Build note

## Scope

Build Athena Research Bot `1.2.0-alpha.1` as a dependency-free local runtime,
integrate it with the existing repository and GitHub Pages site, and verify the
full public story without erasing the 110-skill catalog.

Base commit: `3031536937276e28ca7211399f7d95c332711358`.

## Planned rungs

| Rung | Deliverable | Acceptance command | Status |
|---|---|---|---|
| F0 | Importable CLI and safe project initialization | `python -m unittest tests.test_alpha_cli -v` | passed (4/4) |
| F1 | Durable tasks, planning, resume, checkpoint | `python -m unittest tests.test_alpha_state -v` | passed (6/6, 1 platform skip) |
| F2 | Core routing and deterministic policy denial | `python -m unittest tests.test_alpha_policy -v` | passed (16/16, 1 platform skip) |
| F3 | Immutable, verifiable Research Release | `python -m unittest tests.test_alpha_release -v` | pending |
| F4 | Website, docs, metadata, CI, full regression | full validation suite | pending |

Each rung must pass its own command and all earlier rung commands before the
next rung is considered complete.

## Explicit deferrals

- No hosted account system, tenant database, web API, background worker, or
  synchronized cloud memory.
- No real model invocation, autonomous browsing, citation-index subscription,
  GPU job, payment, email, GitHub push, or publication adapter.
- No claim that all 110 catalog skills are executable or independently audited.
- No exactly-once guarantee for future external services. Such a guarantee
  would require provider idempotency keys and reconciliation APIs.
- No byte-identical guarantee for a fresh LLM run. Reproducibility covers a
  rebuild from frozen inputs and recorded raw outputs.
- No assertion that integrity verification makes arbitrary bundled HTML safe to
  open or publish.

## Evidence log

- Baseline reported by independent read-only audit: 67 tests pass; two Windows
  symlink tests skip where privileges are unavailable; existing consistency,
  quality, demo, and strict packaging checks pass.
- Current risk gap: those tests cover installer behavior, not Bot checkpointing,
  policy enforcement, prompt-injection boundaries, or Release integrity.
- P0 enforcement will live outside the model in deterministic state, policy,
  path, and manifest code.

## Build log

- Specification and assumptions recorded before implementation.
- F0: `athena init` creates strict, private local state and refuses unsafe roots
  or accidental reinitialization.
- F1: tasks, routes, checkpoints, artifact hashes, revisions, and resumable next
  actions survive process restarts; corrupt or future state fails closed.
- F2: bilingual deterministic routing and model-independent policy enforcement
  deny network, paid, destructive, overwrite, and external-write effects.
