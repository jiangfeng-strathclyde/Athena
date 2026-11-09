# FAQ

## 1. How is this different from a prompt pack?

A prompt is usually a one-off instruction. This repository is a loadable behavior system: it defines non-negotiable boundaries, a collaboration workflow, skill routing, and separate generation and verification paths. The rules can be reloaded for every task and tested with the assets in [`demo_assets/`](demo_assets/).

## 2. How does it relate to Claude Code skills?

The `skills/` directory uses the standard `SKILL.md` format and can be mounted by compatible tools. This repository also adds a scene-based [`ROUTING_TABLE.md`](../clone-kit/ROUTING_TABLE.md) and a behavior guide, [`DISTILLED_PUBLIC.md`](DISTILLED_PUBLIC.md).

## 3. Does it cost money or require an account?

The core workflow is free, account-free, and readable as plain text. Skills marked `(ext)` may require your own API key, cloud GPU, search service, or other external account. If a dependency is unavailable, the skill must skip or disclose the limitation rather than invent a result.

## 4. Is it safe? Does it collect my data?

The repository contains no tokens or webhooks and does not collect user data. External calls happen only when a selected skill explicitly requires them. See the anti-roadmap in [`ROADMAP.md`](../ROADMAP.md).

## 5. Why is the private memory not included?

Long-term collaboration history can contain real project facts, unpublished work, and personal preferences. The public repository therefore exposes the transferable methods, not private memory. A trustworthy public clone should say clearly that it does not remember you yet.

## 6. What happens when a cross-model review backend is unavailable?

Audit skills fall back to a single-model self-review and disclose the downgrade. Confidence should be lower, never disguised. A real example is recorded in [`CITATION_AUDIT.md`](demo_assets/audit_2026-11-06_run01/CITATION_AUDIT.md).

## 7. Why not rewrite skills to bypass a security scanner?

Credibility matters more than convenience. We record scanner blocks, review the findings, and offer safe alternatives. We do not disguise content to evade a check. See [`TRANSPARENCY_LOG.md`](TRANSPARENCY_LOG.md).

## 8. What is the relationship with upstream ARIS?

Many skills are mirrored from [Auto-claude-code-research-in-sleep](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) under the MIT License, with attribution preserved. [`UPSTREAM_SYNC.md`](UPSTREAM_SYNC.md) explains how mirror-only changes, semantic changes, and reviews are tracked.

## 9. Can I use it commercially?

Yes, subject to the MIT or MIT-0 license attached to each component. You are also responsible for the commercial terms of any external API, model, or cloud service you use.

## 10. How can I contribute or build my own clone?

- Open a [Discussion](https://github.com/jiangfeng-strathclyde/Thats-me/discussions) for a skill request or clone showcase.
- Read [`CONTRIBUTING.md`](../CONTRIBUTING.md) before submitting a skill.
- Follow [`HOW_TO_BUILD_YOUR_CLONE.md`](../clone-kit/HOW_TO_BUILD_YOUR_CLONE.md) to create your own version.
