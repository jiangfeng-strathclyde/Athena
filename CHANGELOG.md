# Changelog

## 1.2.0-alpha.1 - 2026-11-12

### Added

- A local-first Research Bot Alpha control plane with `init`, `plan`, `status`,
  `resume`, `checkpoint`, `export`, and `verify` commands.
- Source-linked, versioned Research Releases with task records, claim/evidence/
  decision ledgers, registered artifacts, integrity metadata, and offline
  verification.
- A release export gate: all planned steps must be complete, at least one
  artifact must be registered, and recorded bytes and SHA-256 hashes must match.
- Instruction-hash pinning, task-bound strict JSONL records, private local-source
  redaction, non-stealable writer locks, and link/reparse-point defenses for
  managed state and release paths.
- Hash-bound release timestamps, fail-clean post-move verification, canonical
  POSIX parent handling, and conservative redaction for signed/source URLs.
- Exact `checkpoint_argv` plus a self-contained shell command, including Python
  and project paths with spaces, apostrophes, percent-delimited text, and shell
  metacharacters; Windows argv is protected from `cmd.exe` reinterpretation.
- Fail-closed scanning for malformed or nested credential URLs, Markdown URL
  delimiters, Unicode-encoded secrets, and over-nested escape encodings.
- Fail-closed research-record handling for decimal precision loss, numeric
  underflow, and Unicode surrogate escapes that cannot be emitted as UTF-8.
- Complete wheel packaging for all 110 skill instruction trees, plus an offline
  install smoke test that compares resources, checkpoints an artifact, exports
  a Research Release, and verifies it outside the repository.
- [`docs/RESEARCH_BOT_ALPHA.md`](docs/RESEARCH_BOT_ALPHA.md), defining the
  current execution, storage, network, and verification boundaries.

### Changed

- Reframed the README, documentation homepage, quickstart, positioning, FAQ,
  and roadmap around one product: an open-source Research Bot that produces
  Research Releases.
- Moved the 110-skill catalog behind the product workflow while preserving the
  existing installers, skill coverage, attribution, and validation material.
- Made explicit skill selection an exact, non-empty subset in canonical pipeline
  order; implicit routing still adds the integrity baseline when appropriate.

### Alpha boundaries

- Athena is a local control plane, not a hosted bot, model runtime, cloud store,
  or automatic publisher.
- A compatible local agent, script, or researcher performs planned actions and
  checkpoints artifacts. Package verification does not establish scientific
  truth.

## 1.1.0 - 2026-11-10

### Added

- `citation-tracing`: bounded backward-reference and forward-citation discovery,
  conservative identity resolution, source-backed edge tables, screening reasons,
  and explicit coverage/stop conditions. Works with supplied material and tools
  already available in the host; it does not bundle an online citation service.
- Offline literature-workflow evaluation materials and expected checks for
  citation direction, duplicates, inaccessible text, and conflicting evidence.

### Improved

- `research-lit`: an Athena-specific, self-contained evidence-matrix mode for
  supplied sources, with inclusion/exclusion reasons, per-claim support,
  counterevidence and uncertainty, passage locators, and applicability limits.
  The original mirrored ARIS workflow and its dependency notice remain visible.
- Task routing and examples for citation tracing and external-claim evidence
  review; catalog totals are now 110 skills, with 107 selected by default.
- Plugin package version is 1.1.0. Existing installations can select the new
  skill without replacing the whole catalog; the existing installer retains
  backups when updating an installed skill.

### Scope

No third-party tool endorsement, paid service integration, or automatic claim
verification is implied. See [validation and limitations](docs/VALIDATION.md)
for the distinction between packaging checks and actual agent behavior.

Earlier changes are recorded in Git history and the existing validation reports.
