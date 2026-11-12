# Athena Research Bot roadmap

Athena is an open-source Research Bot that turns a research question, paper, or dataset into a source-linked, versioned Research Release.

The roadmap starts from the product that exists today: a local-first Alpha control plane. Items below describe direction, not delivery promises.

## Available in the Alpha

- [x] Initialize local projects with versioned state under `.athena/`.
- [x] Plan deterministic core workflows from a goal and source references.
- [x] Return an explicit next-action contract without silently executing a model.
- [x] Checkpoint completed steps with registered artifacts and hashes.
- [x] Block export until every planned step is complete and at least one artifact exists.
- [x] Export a versioned Research Release and verify it offline.
- [x] Keep release records for claims, evidence, decisions, artifacts, and integrity metadata.
- [x] Ship 110 research skills, with 107 selected by the full installer by default.
- [x] Provide a synthetic sample release and repository consistency checks.

## Alpha priorities

- [ ] Stabilize the Research Release schema, compatibility policy, and migration story.
- [ ] Add richer source, evidence-location, and claim-to-artifact records.
- [ ] Improve recovery guidance for interrupted or stale local projects.
- [ ] Add more end-to-end fixtures for multi-step tasks, tampering, and failed export gates.
- [ ] Make local agent adapters explicit about capabilities, approvals, and external calls.
- [ ] Keep the static sample viewer aligned with the exported release format.
- [ ] Document reproducible handoff and review patterns for teams using shared repositories.

## Later, after the Alpha contract is stable

- [ ] Evaluate an optional release viewer that can open local packages without changing them.
- [ ] Explore interoperable release exchange between research tools.
- [ ] Consider collaboration features only with explicit identity, storage, retention, and access-control policies.

## Anti-roadmap

- No “one-click paper” or fully automatic publication claims.
- No automatic publishing or external writes without explicit user approval.
- No claim that a verified package makes its scientific conclusions true.
- No claim that the static website is a hosted bot or collects research inputs.
- No cloud-privacy promise for services Athena does not operate or control.
- No hidden replacement of missing sources, tools, or model capabilities with invented output.

See the [Alpha contract](docs/RESEARCH_BOT_ALPHA.md), [local quickstart](docs/START_HERE.md), and [validation boundaries](docs/VALIDATION.md).
