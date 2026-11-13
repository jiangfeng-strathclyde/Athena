# Athena FAQ

## What is Athena?

Athena is an open-source Research Bot that turns a research question, paper, or dataset into a source-linked, versioned Research Release.

The current Alpha is a local-first control plane. It plans work, records state and artifacts, and gates release export. A compatible local agent or tool performs the research steps; Athena does not hide that execution behind a hosted service.

## What is a Research Release?

A Research Release is a versioned directory containing the task record, claims, evidence, decisions, registered artifacts, and integrity metadata needed to inspect what was produced. `python -m athena verify <release-dir>` checks the package structure and recorded file hashes.

Verification proves package integrity, not that the scientific conclusions are correct. Researchers and reviewers still need to assess source quality, methods, statistics, and interpretation.

## Is this website a hosted Research Bot?

No. The website is static documentation plus an illustrative sample release. It does not run a model, accept project uploads, or store research in the cloud.

Use the [local quickstart](START_HERE.md) to create a project on your own machine. See the [Alpha contract](RESEARCH_BOT_ALPHA.md) for the precise boundary.

## What can I give Athena?

A task can begin with a research question and source references such as a local paper, local dataset, or URL. Local files are fingerprinted when they are registered. In the core Alpha CLI, a URL is recorded as a sanitized reference; Athena does not fetch it automatically.

One or more repeated `--skill` options select that exact supported, nonempty
subset. Athena normalizes the subset to the documented canonical order; it does
not silently add another skill. Without explicit options, goal routing may
select the broader core path.

## What actually runs the research?

The CLI returns an explicit next-action contract. Its `instruction_path` is an
absolute, readable path to the installed skill's actual `SKILL.md`, and its
`instruction_sha256` matches the hash pinned when the task was planned. A
compatible local agent, script, or researcher carries out that action using the
tools and permissions available in its host, then checkpoints the resulting
artifact. The core CLI itself does not execute a model or silently call external
services.

## What happens if a task or step is blocked?

`resume` and `checkpoint` fail closed when the task or its next step is
`blocked`; they do not advance state or register an artifact. The Alpha does not
automatically unlock that task in place. Correct the input or source problem,
then run `plan` to create a new task instead of editing `.athena/` state.

## Can I export unfinished work?

No. Export requires every planned step to be complete and at least one registered artifact. Athena also checks that registered artifacts are regular files in the task artifact directory and that their bytes and SHA-256 hashes still match. See [Start here](START_HERE.md) for an executable example.

## Is my data private?

The core CLI stores project state locally under `.athena/` and does not upload it. Private project state contains usable absolute paths for local sources, while an exported Research Release replaces those paths with a fixed private-source marker. The files under `.athena/` are not encrypted by Athena. If you connect a model, search provider, cloud runner, or another third-party tool, that tool has its own data handling and privacy terms. Review them before providing sensitive or unpublished material.

## Does Athena require an account or paid service?

The repository, CLI, documentation, and bundled validation assets require no Athena account and are MIT licensed. Optional skills or the host you use may require an API key, subscription, search service, or compute budget. A missing dependency must be reported rather than replaced with an invented result.

## What does “110 research skills” mean?

The repository contains a catalog of 110 research skills; the full installer selects 107 by default. Skills have different dependencies and are not all exercised or automatically executed by the core Alpha CLI. Routing can select a bounded subset for a goal; across all three core stages, the canonical order is `citation-tracing` → `research-integrity-pipeline` → `explorable-paper` → Research Release. The larger catalog remains available for compatible hosts.

The integrity catalog includes `citation-audit`, `paper-claim-audit`, and `experiment-audit`. See [skill coverage](SKILL_COVERAGE.md) and [installation](INSTALL_ONCE.md).

## Is the sample release real research?

No. The [damped-oscillator sample](examples/damped-oscillator.html) is a fully synthetic teaching model computed from the equation shown on the page. It contains no paper results, private data, or empirical research claim; it only demonstrates the intended inspection experience.

## How does Athena relate to ARIS?

Many skills originated in the upstream ARIS project and retain attribution under the MIT License. [Upstream sync notes](UPSTREAM_SYNC.md) distinguish mirrored content from Athena-specific changes.

## Can I use Athena commercially or contribute?

Yes, subject to the license attached to each component and to the terms of any external services you choose. Read the [contribution guide](../CONTRIBUTING.md) before proposing a change.

## Where should I start?

Follow the [local quickstart](START_HERE.md), inspect the [synthetic sample](examples/damped-oscillator.html), or read the [Research Bot Alpha contract](RESEARCH_BOT_ALPHA.md).
