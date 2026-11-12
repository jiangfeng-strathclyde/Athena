# Positioning

**Athena is an open-source Research Bot that turns a research question, paper,
or dataset into a source-linked, versioned Research Release.**

## The category

Athena is a **local-first research control plane**. It sits between a research
goal and the local agent or tools that do the work. Its job is to make the
route, evidence, artifacts, uncertainty, and release history inspectable.

The unit of value is not a chat answer or a generated manuscript. It is a
**Research Release**: a versioned local bundle that records the question,
sources, completed steps, supporting artifacts, limitations, and checksums.

## Who it is for

- Researchers who want an auditable handoff between a question and its evidence.
- Students who need a visible process instead of an opaque final answer.
- Teams that want a reproducible local record before sharing or publishing.
- Builders who want portable `SKILL.md` workflows without coupling the
  research record to one model provider.

## The difference

| Approach | Primary output | Typical state | Athena's boundary |
|---|---|---|---|
| General chat assistant | A response | Conversation history | Athena records a project, artifacts, and release manifest |
| Prompt or skill pack | Reusable instructions | Host-specific configuration | Athena adds lifecycle state and an export gate |
| Autonomous paper generator | A document | Hidden or tool-specific run | Athena keeps the human decision point and does not claim one-click science |
| Repository template | Files and conventions | Git working tree | Athena adds deterministic routing, checkpoints, and offline verification |

Athena can work with a compatible local agent, but the Alpha does not contain
or host that agent. It controls the workflow; it does not pretend to have
executed research that another tool must perform.

## Product principles

1. **Evidence before prose.** Important claims should point to sources or be
   marked unverified.
2. **Artifacts before completion.** Work is not exportable merely because an
   agent says it is done.
3. **Local before hosted.** The Alpha stores project state and releases on the
   user's machine.
4. **Explicit uncertainty.** Calculations, verified findings, hypotheses, and
   unknowns remain distinct.
5. **Human authority.** Publishing, sending, paid compute, deletion, and other
   consequential effects require a separate decision.

## Alpha reality

Today Athena provides a local CLI, deterministic routing across three core
skills (`citation-tracing` → `research-integrity-pipeline` →
`explorable-paper`), checkpointed artifacts, a strict release gate, and offline verification.
The website is documentation and a sample entry point. There is no hosted
Athena bot, model runtime, account system, or cloud storage.

The repository also includes [110 research skills](SKILL_COVERAGE.md). They
extend what compatible agents can do, but many specialized workflows require
their own tools, credentials, or support files. The catalog is a capability
library, not evidence that every workflow is ready in every host.

## What Athena does not claim

- It does not turn one idea into a trustworthy paper automatically.
- A verified package is not the same as a verified scientific conclusion.
- It does not guarantee citation correctness without accessible sources.
- It does not make third-party model or cloud use private.
- It does not replace peer review, domain expertise, or research judgment.

## Short description

> Athena turns a research question, paper, or dataset into a local,
> source-linked, versioned Research Release—with explicit steps, recorded
> artifacts, and an offline verification gate.

See the [Alpha contract](RESEARCH_BOT_ALPHA.md), [quickstart](START_HERE.md),
and [roadmap](../ROADMAP.md).
