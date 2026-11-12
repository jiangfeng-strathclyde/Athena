# Athena Research Bot Alpha — specification

Target: `1.2.0-alpha.1`; base `3031536937276e28ca7211399f7d95c332711358`.

Outcome: add a dependency-free local bot spine while retaining the 110-skill
catalog and GitHub Pages site.

Inputs: project directory, research goal, optional local-file/HTTP(S) source
references, and artifacts produced by a compatible agent.

Outputs: transparent `.athena/` JSON/JSONL state, stable next-action contracts,
checkpointed artifacts, and an immutable private Research Release.

MUST:

- initialize safely and persist strict, revisioned state atomically;
- route a bounded subset in canonical order: citation tracing, integrity,
  explorable paper;
- resume without pretending to execute a model or skill;
- reject corrupt state, unsafe paths, stale revisions, untrusted approval, and
  all external effects;
- export only completed work, exclude private content, detect secrets, and
  verify canonical paths, tree shape, sizes, hashes, links, and collisions;
- keep public docs, metadata, CI, and runtime on one honest Alpha contract.

Functional ladder: F0 CLI; F1 memory; F2 router/policy; F3 Release; F4 public
integration. Each rung retains all earlier acceptance tests.

Success command: `python -m unittest discover -s tests -v`, followed by the
repository consistency, quality, demo, and strict dependency checks.

Scope cuts: no hosted model, autonomous skill execution, cloud memory, account
system, publishing adapter, paid compute, or scientific-truth guarantee.
