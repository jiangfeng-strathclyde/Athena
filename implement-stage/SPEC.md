# Athena Research Bot Alpha — implementation specification

## Outcome

Turn Athena from a catalog that users must manually reload into a local-first,
vendor-neutral research bot spine that remembers a project, routes a goal to
the right skills, resumes from a durable checkpoint, and exports a verifiable
Research Release. The existing 110-skill catalog and GitHub Pages site remain
part of the product; the Alpha adds an easier default path rather than replacing
them.

Target version: `1.2.0-alpha.1`.
Implementation base: `3031536937276e28ca7211399f7d95c332711358`.

## Public contract

The supported, dependency-free entry point is Python 3.10+:

```text
python -m athena init <directory> --name <name>
python -m athena plan "<research goal>" --source <paper-or-url> ...
python -m athena status
python -m athena resume [--task <task-id>]
python -m athena checkpoint --task <task-id> --step <step-id> [--artifact <path>]
python -m athena export --task <task-id> --version <version>
python -m athena verify <release-directory>
```

`init` creates a `.athena/` project without copying private source material.
`plan` uses deterministic routing to choose the core skill chain and records a
task. `resume` reports the persisted next step; it does not pretend to have run
an LLM. `checkpoint` records real completed work and optionally copies a named
artifact into the project sandbox. `export` creates an immutable, local draft
Research Release. `verify` checks its manifest, paths, sizes, and hashes offline.

## Project state

The canonical state is transparent JSON/JSONL/Markdown under `.athena/`:

```text
.athena/
  project.json
  tasks/<task-id>.json
  runs/
  claims.jsonl
  evidence.jsonl
  decisions.jsonl
  artifacts/<task-id>/
  releases/<version>-<content-hash>/
  releases/current.json
  private/
```

Writes use a same-directory temporary file, flush, `fsync`, validation, and
atomic replacement. State has a schema version and monotonically increasing
revision. Invalid, corrupt, or future-version state blocks the operation; the
runtime must never silently reset it. Task IDs and release paths are generated
or validated, not accepted as arbitrary filesystem paths.

## Core routing

The approachable default surface exposes three abilities:

1. `citation-tracing` — find and screen backward/forward citation links.
2. `research-integrity-pipeline` — connect claims to evidence and uncertainty.
3. `explorable-paper` — turn supported findings into an evidence-linked HTML
   exploration.

Routing is deterministic and explainable. A broad paper-understanding goal may
select all three. A user can request a core skill explicitly. The remaining
catalog stays available as an advanced library, but the Alpha does not claim
that all 110 skills are executable by this runtime.

## Trust and permission boundary

- Paper text, HTML, BibTeX, tool output, skill text, and imported metadata are
  untrusted data. They never create policy, approval, or an action capability.
- P0 public reads and offline computation are allowed.
- P1 creation of a new derived artifact inside the project sandbox is allowed.
- Network access, paid compute, external writes, overwrite, publish, send, and
  delete are unavailable in this Alpha. The deterministic policy layer denies
  them even if an imported document or model output requests them.
- A Research Release is a private local draft by default. Export never pushes,
  publishes, sends, or uploads it.
- `.athena/private/` is excluded from export. Secrets must not be printed or
  included in a release.

## Research Release contract

Each release is immutable and content-addressed. It contains a deterministic
core (`README.md`, normalized task snapshot, logs/artifact index, and
`manifest.json`) plus a small non-deterministic envelope for creation time.
Manifest paths are canonical POSIX relative paths. Absolute paths, traversal,
symlinks, case-insensitive collisions, missing files, size mismatches, and hash
mismatches fail verification. `current.json` is only replaced after the staged
release verifies.

The reproducibility claim is intentionally narrow: frozen local inputs and
recorded raw outputs can rebuild the deterministic release core. Athena does
not claim that re-running an LLM will produce identical bytes.

## Functional ladder

### F0 — walking skeleton

- Package and CLI are importable with the standard library only.
- `init` creates a valid project and refuses unsafe/non-empty conflicting state.
- One-command acceptance: `python -m unittest tests.test_alpha_cli -v`.

### F1 — durable project and task memory

- Strict state validation, atomic writes, revisioning, deterministic planning,
  status, resume, and checkpointing work in a temporary project.
- Previously completed steps are not repeated after restart.
- One-command acceptance: `python -m unittest tests.test_alpha_state -v`.

### F2 — router and policy boundary

- Core routes are explainable and stable.
- Untrusted content cannot grant an action; unsupported side effects fail closed.
- One-command acceptance: `python -m unittest tests.test_alpha_policy -v`.

### F3 — Research Release

- Export is immutable, private by default, offline-verifiable, and rebuilds the
  same deterministic core from the same checkpoint.
- Traversal, symlink, case collision, corruption, and private material are
  rejected or excluded as specified.
- One-command acceptance: `python -m unittest tests.test_alpha_release -v`.

### F4 — public product integration

- README, START_HERE, FAQ, positioning, roadmap, validation, changelog, plugin
  metadata, GitHub Pages, and CI tell one honest story.
- The first screen leads with the five-minute persistent-project path, not the
  110-skill installation burden.
- One-command acceptance: `python -m unittest discover -s tests -v` plus the
  existing repository consistency, quality, demo, and strict packaging checks.

## Definition of done

- All five rungs pass locally and earlier rungs remain green.
- Existing repository checks and tests do not regress.
- The website remains static and deployable on GitHub Pages.
- No network, credential, model, GPU, or paid-service call is required by tests.
- Limitations and unverified claims remain visible.

