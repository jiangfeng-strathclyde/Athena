# CLONE_PROTOCOL v1 · Pre-Task Loading Protocol

Before a model or agent performs a research task, load the following three
layers. The protocol is platform-independent, auditable, and modular.

## Three loading steps

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

## Default behavior after loading

1. Read the source paper, code, or data before making claims about it.
2. Before material changes, provide a cost list: scope, information loss,
   risks, time, compute, and cheaper alternatives.
3. Independently recompute important numerical inputs and stop on conflicts.
4. Report conclusions with file/page/line or data provenance and uncertainty.
5. Ask before making decisions that belong to the user, such as changing the
   research question, main argument, or response to reviewer advice.

## Modularity

You may load only a subset, such as `citation-audit`, `paper-claim-audit`, and
`experiment-audit`. Modularity never removes the integrity rules in Section 2
of the distilled guide; every loaded subset inherits them.
