# CLONE_PROTOCOL v2 · Research Entry and Optional Guides

For installed skills, start with `research-integrity-pipeline` when the task
needs an evidence-backed research workflow. Its instructions are self-contained;
the installer does not copy root-level guides into each skill directory.
For text chat, paste the code block in
[`LOADER_LITE.md`](../clone-kit/LOADER_LITE.md).

The three-layer route below remains available when working from the checkout.
Version 2 preserves that route but removes the assumption that every installed
skill can access these repository files. It does not claim that other skills
automatically inherit instructions they have not loaded.

## Optional three-layer route from a checkout

1. **Read the story and boundaries:** read the root `README.md` for the
   project's purpose, privacy boundary, and transparency commitments.
2. **Read the operating principles:** read
   [`DISTILLED_PUBLIC.md`](DISTILLED_PUBLIC.md) for the collaboration method,
   integrity rules, writing standards, statistics standards, and methodology.
3. **Load only the relevant skills:** use
   [`../clone-kit/ROUTING_TABLE.md`](../clone-kit/ROUTING_TABLE.md), then read the
   full `skills/<skill-name>/SKILL.md` for each selected skill. If a skill needs
   an unavailable API, account, or external service, skip it explicitly or
   report the limitation. Never fabricate a tool result.

## Deployment options

| Mode | Method | Best for |
|---|---|---|
| Zero dependency | Paste or read the three layers above | Any chat model |
| `SKILL.md`-compatible tool | Copy or link selected skill folders into the tool's skill directory | Claude Code, Codex, and similar tools |
| Digital employee platform | Follow [`HOW_TO_BUILD_YOUR_CLONE.md`](../clone-kit/HOW_TO_BUILD_YOUR_CLONE.md) | Platforms with packaged agents or employees |

## Behavior supported by the research entry point

1. Read the source paper, code, or data before making claims about it.
2. Before material changes, explain consequential costs, risks, and scope
   changes in proportion to the task.
3. Independently recompute important numerical inputs and stop on conflicts.
4. Report conclusions with file/page/line or data provenance and uncertainty.
5. Ask before making decisions that belong to the user, such as changing the
   research question, main argument, or response to reviewer advice.

## Modularity

You may load only a subset, such as `citation-audit`, `paper-claim-audit`, and
`experiment-audit`, after checking their prerequisites. The distilled guide
provides additional context when available. Missing reviewer backends or
support files must be reported; the entry point can offer a narrower manual
check, not certify an incomplete specialized audit.
