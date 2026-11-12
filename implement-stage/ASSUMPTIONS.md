# Assumptions and decisions

ASK mode: `never`. Reversible defaults were implemented; semantic choices are
explicit so a later release can change them deliberately.

| ID | Under-determined choice | Chosen behavior | Class | Source |
|---|---|---|---|---|
| A-001 | Meaning of “Bot” | Persistent state, routing, permissions, checkpoints, and releases; not a Grok or hosted-model wrapper | semantic | user |
| A-002 | Meaning of “remember” | Durable, inspectable local project state; no upload or cross-device sync | semantic | user |
| A-003 | First end-to-end vertical | Citation tracing → integrity review → explorable paper → Research Release | semantic | user |
| A-004 | Meaning of Release verification | Package integrity and provenance only; never scientific truth, HTML safety, or correct agent behavior | semantic | default |
| A-005 | Reproducibility boundary | Deterministic rebuild from frozen inputs and recorded outputs; no promise of byte-identical fresh LLM runs | semantic | default |
| A-006 | Planning source behavior | Store usable absolute local paths plus file fingerprints in private project state; record sanitized HTTP(S) references; do not fetch or copy source documents during planning | semantic | sweep |
| A-007 | Skill execution | Return one stable next-action contract with an absolute readable installed-instruction path and its pinned SHA-256; a compatible agent performs real work and checkpoints its artifact | semantic | default |
| A-008 | Implicit broad-goal route order | `citation-tracing`, `research-integrity-pipeline`, `explorable-paper`; an explicitly supplied selection must be nonempty and is an exact subset normalized to this canonical order | semantic | sweep |
| A-009 | Public surface | Improve the existing GitHub Pages site rather than introduce another web stack | interface | user |
| A-010 | Runtime entry point | Python 3.10+ standard library via `python -m athena`; the wheel also installs `athena` and the skill instructions needed by resume | interface | sweep |
| A-011 | External effects | Network, paid compute, external write, overwrite, publish, send, and delete fail closed in Alpha | interface | default |
| A-012 | Release visibility | Immutable content-addressed local draft under `.athena/releases`; publishing is a future adapter | interface | default |
| A-013 | Version | Public `1.2.0-alpha.1`; PEP 440 package version `1.2.0a1` | interface | default |
| A-014 | Review assurance | Cross-family silent-assumption sweep is required for full certification; same-family review is provisional | semantic | default |
| A-015 | Skill instruction drift | Pin each planned step to its `SKILL.md` SHA-256 and block resume if installed instructions change; re-plan explicitly instead of silently changing work | semantic | sweep |
| A-016 | Source privacy in releases | Keep usable local paths only in private project state; replace them with `[private-local-source]` in exported task snapshots | semantic | sweep |
| A-017 | Research-record scope | Every nonempty JSONL record must be a strict object with `task_id`; export includes only the selected task and verification rejects cross-task records | semantic | sweep |
| A-018 | Pre-Alpha state compatibility | No automatic migration for task documents without instruction pins; strict validation fails closed and users re-plan | interface | sweep |
| A-019 | Abandoned write-lock recovery | Never steal a lock by age; after confirming no writer is active, a user may manually remove `.athena/.write-lock` and retry | interface | sweep |
| A-020 | Local filesystem threat model | Reject Windows junction/reparse ancestors, canonicalize stable POSIX parent aliases, reject links inside managed paths, and serialize Athena writers; do not claim sandboxing against a same-user process that races filesystem replacement | semantic | sweep |
| A-021 | Recovery from blocked work | Never mutate or auto-unblock a task in place; correct the source/input or instruction installation, then create a new task with `plan` so the blocked history remains inspectable | interface | sweep |
| A-022 | Credentials embedded in source URLs | Canonicalize and redact recognized sensitive query keys, including case/camel/acronym variants, common provider keys, and nested encoded parameters; this is a conservative heuristic, not an exhaustive secret detector, so users must not supply credentials as sources | semantic | sweep |
| A-023 | Meaning of release time | Bind `manifest.json` and `release.json` `created_at` to the completed task revision time for deterministic rebuilding; record each successful export/reuse invocation only in `current.json.updated_at` | interface | sweep |

Highest reversal costs are A-004/A-005 because they define what users may infer
from a Research Release. A-015/A-017/A-023 protect reproducibility, task
isolation, and content identity; changing them requires a deliberate schema
revision. A-009/A-010 remain comparatively cheap interface changes.
