<p align="center">
  <img src="assets/hero.svg" alt="Athena · a research copilot that verifies before it writes" width="100%">
</p>

<h3 align="center">Turn a research goal into a clear, verifiable workflow.</h3>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="MIT"></a>
  <img src="https://img.shields.io/badge/research_skills-108-blue.svg" alt="108 research skills">
  <a href="docs/CLONE_PROTOCOL.md"><img src="https://img.shields.io/badge/evidence-first-2dd4bf.svg" alt="Evidence first"></a>
</p>

**Athena** is an open-source research copilot. Tell it what you want to accomplish; it selects the right skills, proposes a plan, and checks the evidence before it writes conclusions.

## Try it in one minute

Open ChatGPT, Claude, Codex, Cursor, or another AI assistant that can read web links. Paste this:

```text
Use Athena: https://github.com/jiangfeng-strathclyde/Athena

Read docs/DISTILLED_PUBLIC.md and clone-kit/ROUTING_TABLE.md.
Choose the skills needed for my goal. Show me the plan and its trade-offs first,
then wait for my approval. Do not invent evidence or report numbers that cannot
be reproduced from the source data.

My goal: <describe what you want to do>
```

Replace the final line with a real goal, for example:

- `Check whether the numerical claims in my draft are supported.`
- `Plan a literature review on flood mapping with satellite imagery.`
- `Help me design a reproducible ablation study.`

Using a chat app that cannot open GitHub links? Paste the self-contained [Lite Loader](clone-kit/LOADER_LITE.md) instead.

## What Athena does

| You provide | Athena adds | You receive |
|---|---|---|
| A research goal | The relevant skills and an ordered plan | A workflow you can inspect before execution |
| Drafts, data, or results | Evidence and consistency checks | Claims tied to reproducible sources |
| Your constraints | Explicit trade-offs and approval points | Work that stays under your control |

Athena includes **108 reusable research skills** for literature review, experiment design, scientific writing, figures, citation checks, rebuttals, patents, grants, and more.

## See the difference

When asked to report only the best result, Athena recomputes every run, identifies cherry-picking, and offers honest alternatives instead of silently accepting the claim. In the included synthetic example, the honest summary is **1.17 ± 1.84**, not the cherry-picked 3.2.

<img src="assets/terminal_clone.png" alt="Athena checking a numerical claim before writing" width="100%">

The expected **1.17 ± 1.84** result is reproducible offline:

```bash
python docs/demo_assets/verify_demo.py
```

## Explore

- [Start here](docs/START_HERE.md) — a guided first session
- [Browse the skill map](docs/SKILL_COVERAGE.md) — see what Athena can do
- [Understand the evidence rules](docs/DISTILLED_PUBLIC.md) — how Athena avoids unsupported claims
- [Add a skill](CONTRIBUTING.md) — contribute a reusable research workflow

<details>
<summary><strong>Use Athena as a local skill library</strong></summary>

```bash
git clone https://github.com/jiangfeng-strathclyde/Athena.git
```

Tools that support `SKILL.md` can mount individual folders from `Athena/skills/`. Start with the integrity trio: `citation-audit`, `paper-claim-audit`, and `experiment-audit`.

```bash
cp -r Athena/skills/citation-audit Athena/skills/paper-claim-audit Athena/skills/experiment-audit .claude/skills/
```

See the [platform guide](docs/PLATFORM_MATRIX.md) for other tools.

</details>

## Principles

- Never fabricate results or citations.
- Recompute important numbers from source data.
- Separate verified findings, mathematical conclusions, and hypotheses.
- Explain trade-offs and ask before making consequential changes.

Original content is released under the [MIT License](LICENSE). Mirrored skills retain their upstream attribution in [skills/NOTICE.md](skills/NOTICE.md).

Questions and ideas are welcome in [GitHub Discussions](https://github.com/jiangfeng-strathclyde/Athena/discussions).
