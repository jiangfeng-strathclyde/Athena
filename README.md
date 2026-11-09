<p align="center">
  <img src="assets/hero.svg" alt="Thats-me · an open-source research clone kit" width="100%">
</p>

<h3 align="center">You state the goal. It picks the skills, builds the workflow, and plays by the red lines.</h3>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="MIT"></a>
  <img src="https://img.shields.io/badge/skills-108-blue.svg" alt="108 skills">
  <a href="docs/CLONE_PROTOCOL.md"><img src="https://img.shields.io/badge/protocol-v1-2dd4bf.svg" alt="protocol v1"></a>
</p>

<p align="center"><b>English edition</b> — documentation, skills, examples, and repository tooling are available in English.</p>

## What this is

Mission in one sentence: **break the research barrier down into loadable files — so that undergrads (and eventually even middle-schoolers) can produce reproducible work step by step, and feel the joy of doing research along the way. We do NOT build one-click paper factories.**

- **A skill library**: the full text of 108 research skills in standard SKILL.md format (another 21 are listed but not mirrored for license/internal/vendor reasons). They cover literature, novelty checks, experiments, writing, figures, auditing, rebuttal, patents, and grants;
- **A router**: you state a goal ("write a TGRS-style paper", "verify these numbers", "build a reading list for my students") and the protocol assembles the skill chain automatically — no need to memorize skill names;
- **A set of red lines**: never fabricate results; audit before writing; list the cost of every change and wait for your go-ahead; never mix statistical conventions;
- **Extensible**: adding a skill = adding one SKILL.md file (template and 3-minute recipe in [`CONTRIBUTING.md`](CONTRIBUTING.md)).

This is not a prompt collection. Prompts get forgotten; these files are reloaded before every task, and they are **verifiable** (see the real run below).

## How to use

The flow is always the same, 4 steps:

**You state the goal → it proposes a skill chain + plan → it lists the costs, you approve → it executes and reports what changed where**

### ① Pick your entry by the tool you have

| Your situation | What to do |
|---|---|
| Any chat app: Doubao, Kimi, ChatGPT, your phone… | Paste the [zero-dependency lite loader](clone-kit/LOADER_LITE.md) — red lines are inlined; no need to read this repo; state your goal right after |
| AI tools that can read repos / fetch URLs: Cursor, Codex, Claude Code… | Paste the full loader in ② — you get all 108 research skills + the routing table |
| SKILL.md-compatible tools (e.g. Claude Code) that can auto-trigger skills | Full loader + mount the skills directory (④) |

First time here? Follow the 7-day onboarding route in [`docs/START_HERE.md`](docs/START_HERE.md).

### ② Open a new chat session and paste the full loader

```text
Repo: https://github.com/jiangfeng-strathclyde/Thats-me

Read docs/DISTILLED_PUBLIC.md (red lines) and clone-kit/ROUTING_TABLE.md (goal → skill chain).
(If you cannot read the repo, use these direct links:
 https://raw.githubusercontent.com/jiangfeng-strathclyde/Thats-me/main/docs/DISTILLED_PUBLIC.md
 https://raw.githubusercontent.com/jiangfeng-strathclyde/Thats-me/main/clone-kit/ROUTING_TABLE.md )
I state a goal; you assemble the skill chain: give me the plan and a cost list first,
and execute only after I approve. Never fabricate results; every key number must be
recomputable from raw results; label conclusions as verified / mathematical / hypothesis.

My goal: <your goal>
```

### ③ Replace `<your goal>` with your real task and send

The first reply should be: skill chain + plan + cost list, then it stops and waits for you.
If it starts working without approval, re-paste the rules.

### ④ Optional: mount the skills directory (SKILL.md-compatible tools)

The minimal trust trio:

```bash
cp -r skills/citation-audit skills/paper-claim-audit skills/experiment-audit .claude/skills/
```

All 108:

```bash
git clone https://github.com/jiangfeng-strathclyde/Thats-me.git
mkdir -p .claude/skills
for d in Thats-me/skills/*/; do cp -r "${d%/}" .claude/skills/; done
# On Windows, junctions save space: mklink /J .claude\skills\<name> Thats-me\skills\<name>
```

## Goal → workflow (assembly examples)

| Your goal | Assembled skill chain |
|---|---|
| Write a journal paper | `research-lit` → `novelty-check` → `experiment-plan` → `paper-plan` → `paper-write` → `paper-figure` → `citation-audit` + `paper-claim-audit` + `experiment-audit` → `auto-review-loop` |
| Verify the numbers in a draft | `paper-claim-audit` → independent recomputation script → costed fix list |
| Reviewer rebuttal / resubmit | `rebuttal` → `resubmit-pipeline` (minimal changes: don't touch what reviewers didn't raise) |
| Survey / reading list for students | `arxiv` / `semantic-scholar` → `research-lit` → `comm-lit-review` |
| Prove a proposition | `formula-derivation` → `proof-writer` → `proof-checker` |

Full table and pruning rules: [`clone-kit/ROUTING_TABLE.md`](clone-kit/ROUTING_TABLE.md).

## It really refuses (real run, synthetic data)

A zero-context model loads the protocol, then gets asked to "just write ΔmIoU = 3.2 in the abstract":

<img src="assets/terminal_clone.png" alt="Real reply after loading the protocol" width="100%">

It recomputes per seed (+3.2 / +0.7 / −0.4 → mean ± std = +1.17 ± 1.84), points out that 3.2 is a cherry-pick, offers three costed options, and waits. The citation-audit run against a `.bib` with planted errors (same +1.17 ± 1.84 convention) is in [`docs/demo_assets/`](docs/demo_assets/), reproducible offline: `python docs/demo_assets/verify_demo.py`.

## Boundaries (4 lines)

- The public kit contains **no** memory packs, secrets, unpublished data, or identity-revealing information;
- When a cross-model reviewer backend is missing, audits degrade to single-model self-review and **say so** — never faking a verdict;
- Skills blocked by security scanners are not bypassed; they are logged in [`docs/TRANSPARENCY_LOG.md`](docs/TRANSPARENCY_LOG.md);
- Licensing: original content [MIT](LICENSE); mirrored skills keep upstream attribution, see [`skills/NOTICE.md`](skills/NOTICE.md).

## Dive deeper

[`7-day onboarding`](docs/START_HERE.md) · [`Add a skill`](clone-kit/SKILL_TEMPLATE.md) · [`Skill coverage map`](docs/SKILL_COVERAGE.md) · [`Positioning`](docs/POSITIONING.md) · [`Survey of peer projects`](docs/LESSONS_FROM_OTHERS.md) · [`FAQ`](docs/FAQ.md) · [`End-to-end examples`](docs/EXAMPLES.md) · [`Platform matrix`](docs/PLATFORM_MATRIX.md) · [`Distilled manual`](docs/DISTILLED_PUBLIC.md) · [`Build your own clone`](clone-kit/HOW_TO_BUILD_YOUR_CLONE.md) · [`Landing page`](docs/index.html)

Questions, or want to show off your clone: [Discussions](https://github.com/jiangfeng-strathclyde/Thats-me/discussions).
