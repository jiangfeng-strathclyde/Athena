# NOTICE · Upstream Copyright and Licenses

Skills in this repository retain their original attribution and license notices.

- **Auto-claude-code-research-in-sleep (ARIS)**
  <https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep>
  Copyright (c) 2026 wanshuiyin, MIT License.
- **crawl4ai-skill** — Copyright (c) Lancelin, MIT-0 License.
- **excel-formula** — MIT License, as declared in the upstream metadata.
- **Orchestra Research · AI-Research-SKILLs 1.4.0**
  <https://www.npmjs.com/package/@orchestra-research/ai-research-skills>
  Copyright (c) 2025 Claude AI Research Skills Contributors. The upstream evidence contains a license inconsistency: its README and LICENSE say MIT, while `package.json` says ISC. This repository preserves the upstream LICENSE and records the inconsistency in [`TRANSPARENCY_LOG.md`](../docs/TRANSPARENCY_LOG.md).
- **Nine original research skills** — `academic-paper-narrative`, `research-integrity-pipeline`, `explorable-paper`, `skill-evolution-manager`, `patent-disclosure-drafter`, `remote-sensing-workbench`, `data-profile-and-plot`, `lit-reading-assignment`, and `citation-tracing`; Copyright (c) 2026 Athena contributors, MIT License.

The full permissions are defined by each upstream license. Mirror notes are
explanatory; adapted implementations are identified separately below.

## Standalone adaptations

`arxiv` is an Athena adaptation of the ARIS skill and helper, pinned to commit
`f76ec8d6b77792e2242cca049e08d0cbb7d54e19`. Its installed folder includes the
Python helper, upstream MIT license, and [provenance record](arxiv/references/provenance.json).
The adaptation preserves explicit paper versions, uses Python's standard
library, and leaves existing files unchanged. Upstream wiki integration is
outside this adaptation. Review its local changes before synchronizing it;
replacing its instructions with the upstream mirror would restore dependencies
that are not bundled here.

`openalex` and `semantic-scholar` also adapt the ARIS workflows at that commit.
Each bundles an Athena-authored, read-only Python helper and HTTPS transport,
the upstream MIT license, and a pinned provenance record:
[OpenAlex](openalex/references/provenance.json) and
[Semantic Scholar](semantic-scholar/references/provenance.json).
These implementations do not require the ARIS runtime, shared references, or
wiki integration. External API availability and access policies still apply.

`research-lit` version 1.1.0 adds an Athena-authored screening and evidence-matrix
mode to the ARIS-derived instructions present in Athena commit
`0b023718c134b5f0535a94c0df0ec8e351971e12`. That is an Athena baseline, not a
verified upstream ARIS revision. The new mode and its bundled
[reference](research-lit/references/evidence-matrix.md) are Copyright (c) 2026
Athena contributors, MIT License. Only this supplied-corpus mode is standalone;
the retained original ARIS workflow still has unbundled dependencies. Its
upstream attribution and mirror notice remain unchanged.

## Skills listed but not mirrored

Twenty-one individually named local skills are listed in [`MANIFEST.json`](../clone-kit/MANIFEST.json) with `mirrored: false`: sixteen lacked clear redistribution permission, two were platform-internal, and three were vendor-published skills not redistributed here. A separate manifest entry tracks the remaining, unmirrored Orchestra collection. Details are recorded in [`TRANSPARENCY_LOG.md`](../docs/TRANSPARENCY_LOG.md).

## Platform installation status

Three mirrored skills—`deepxiv`, `paper-compile`, and `paper-poster-html`—were blocked by a platform security scanner and were not installed there. Their source remains available for local review. See [`BLOCKED_NOTE.md`](BLOCKED_NOTE.md).

Last reviewed: 2026-11-10. The authoritative inventory is [`MANIFEST.json`](../clone-kit/MANIFEST.json).
