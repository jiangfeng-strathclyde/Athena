# Build note

## Scope

Athena Research Bot `1.2.0-alpha.1`, built from
`3031536937276e28ca7211399f7d95c332711358`, adds a dependency-free local
control plane while preserving the 110-skill catalog and existing GitHub Pages
site.

## Functional ladder

| Rung | Deliverable | Acceptance | Status |
|---|---|---|---|
| F0 | CLI and safe initialization | `tests.test_alpha_cli` | passed (5) |
| F1 | Durable plan/resume/checkpoint state | `tests.test_alpha_state` | passed (32; 2 platform skips) |
| F2 | Explainable router and fail-closed policy | router + policy suites | passed (24; 1 ordinary-symlink skip) |
| F3 | Immutable, offline-verifiable Research Release | `tests.test_alpha_release` | passed (33; 1 POSIX-only skip) |
| F4 | Website, docs, metadata, CI, regression | full validation suite | passed |

## Run record

- Alpha-focused suite: 94 tests executed; 90 passed and 4 platform-dependent
  tests skipped. Windows junction/reparse-point regressions ran and passed.
- Full repository suite: 161 tests executed; 155 passed and 6
  environment-dependent tests skipped.
- Repository consistency: passed, including runtime/package/plugin/CITATION
  versions, 110 skill directories, 200 manifest entries, docs, and links.
- Skill quality: 110 parsed; all hard checks passed.
- Independent demo recomputation: `1.17 ± 1.84`; passed.
- Strict dependency scans: integrity, literature helpers, and citation tracing;
  no packaging findings.
- Offline wheel installation: source and wheel inventories matched for 132
  skill resources, including all 110 `SKILL.md` files; the installed CLI then
  completed a checkpoint contract, exported a release, and verified it offline.
- Manual CLI spine: init → explicit three-skill plan → resume → three ordered
  checkpoints → export → offline verify; passed. Release core SHA-256:
  `21f6390e7da51ba1a5cd6d1ae3ab2a30de7499402264d6f47a5acf53b03f41f8`.
- `compileall` and `git diff --check`: passed (Git reports only Windows line-ending
  notices).

## Implemented boundaries

- Strict schemas, atomic writes, revisions, locks, checkpoint hash revalidation,
  deterministic bilingual routing, and model-independent permission denial.
- Plans pin the exact skill instruction digest; drift blocks resume. Private
  state keeps usable local source paths, while releases replace them with a
  fixed sentinel. JSONL records are strict and bound to one task; values that
  would lose decimal precision and unencodable Unicode surrogates fail closed.
- Each resumed action returns both exact checkpoint argv and a self-contained
  shell command. Windows transports the exact argv inside an encoded PowerShell
  program rather than treating CreateProcess quoting as cmd.exe escaping. Python
  and project paths containing spaces, apostrophes, percent-delimited text, and
  shell metacharacters are covered by installed-wheel regression tests.
- Export requires a completed task and registered artifacts. It rejects path
  traversal, links/reparse points, case-fold collisions, tampering, unexpected
  files, recognized URL credentials, secrets, over-nested escape encodings,
  Markdown URL-delimiter tricks, and copy races.
  `.athena/private/` is excluded. Failed post-move verification removes the new
  directory before `current.json` can advance.
- `manifest.json` and `release.json` bind their stable `created_at` value to the
  completed task revision. `current.json.updated_at` records the successful
  export/reuse invocation and advances only after verification.
- Windows reparse ancestors are rejected. Stable POSIX parent aliases are
  canonicalized before containment checks; same-user replacement races remain
  outside the stated threat model.
- Public copy says the Alpha returns a next action and does not itself execute
  skills, run a hosted model, upload memory, or publish a release.

## Explicit deferrals

No hosted accounts, web API, background worker, synchronized cloud memory,
model invocation, autonomous browsing, paid service, publication adapter, or
claim that all 110 skills are runtime-executable or independently audited.
Exactly-once external effects and byte-identical fresh LLM runs are not claimed.

## Assurance note

An independent same-family cold audit is run against the raw diff. It is useful
but remains provisional; without an available cross-family backend, the required
cross-family silent-assumption sweep is recorded as `SWEEP_UNAVAILABLE`, never
fabricated as a clean verdict.
