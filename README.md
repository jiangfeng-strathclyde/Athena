<p align="center">
  <img src="assets/hero.svg" alt="Athena · a research copilot that verifies before it writes" width="100%">
</p>

<h3 align="center">Turn a research goal into a clear, verifiable workflow.</h3>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="MIT"></a>
  <img src="https://img.shields.io/badge/research_skills-109-blue.svg" alt="109 research skills">
  <a href="docs/CLONE_PROTOCOL.md"><img src="https://img.shields.io/badge/evidence-first-2dd4bf.svg" alt="Evidence first"></a>
</p>

**Athena** is an open-source research copilot. Tell it what you want to accomplish; it selects the right skills, proposes a plan, and checks the evidence before it writes conclusions.

## Get started on your platform

Choose the setup that matches where you work:

- **Local agents:** install research skills in Claude Code, Cursor,
  GitHub Copilot, Gemini CLI, Codex, or another compatible `SKILL.md` host.
- **Web or mobile chat:** use the [chat setup below](#web-or-mobile-chat) in
  ChatGPT, Claude, Gemini, DeepSeek, Qwen, or another text-chat app.

### Local agents: install once

With Git and Python 3.10 or newer installed, run these commands in PowerShell on Windows
or a terminal on macOS/Linux:

```bash
git clone https://github.com/jiangfeng-strathclyde/Athena.git
cd Athena
python scripts/install_athena.py --auto
```

If Python 3 is available as `py -3` on Windows or `python3` on macOS/Linux,
use that in place of `python`. Automatic setup configures the shared local
skills directory, plus Claude Code's directory if detected. Other supported
local agents can use the shared directory without duplicate native copies.
To select one agent instead, replace the last command with:

| Your agent | Install command |
|---|---|
| Claude Code | `python scripts/install_athena.py --agent claude-code` |
| Cursor | `python scripts/install_athena.py --agent cursor` |
| GitHub Copilot | `python scripts/install_athena.py --agent copilot` |
| Gemini CLI | `python scripts/install_athena.py --agent gemini` |
| Codex / shared local skills directory | `python scripts/install_athena.py --agent universal` |
| Another `SKILL.md` host | `python scripts/install_athena.py --target /path/to/skills` |

Start a new agent session. The catalog contains 109 skills; the installer
selects 106 by default and excludes three that require explicit review and
authorization. Compatible hosts discover installed skills and load relevant
instructions on demand. Check the host's skill list to confirm discovery. These local files
are separate from web accounts and remote or cloud sessions.

For a smaller start, install only the self-contained research entry point:

```bash
python scripts/install_athena.py --agent universal --skill research-integrity-pipeline --strict-packaging
```

Choose either this minimal route or the collection install above. Add
`--dry-run` to preview an installation without writing files. See
[update and recovery instructions](docs/INSTALL_ONCE.md#update-an-existing-installation)
if the skills are already installed.

**Availability is not the same as readiness.** Many mirrored skills reference
upstream support files or host-specific tools that are not bundled here.
Start with `research-integrity-pipeline` for source-backed checks and its
bundled offline paired-results calculator;
specialized audits may need additional setup. Run
`python scripts/check_skill_dependencies.py` for a static packaging report.
See [what has been tested](docs/VALIDATION.md).

### Web or mobile chat

No terminal is needed for this route:

1. Open the [Lite Loader](clone-kit/LOADER_LITE.md).
2. Copy the text inside its code block and replace `<your goal>` with your task.
3. Paste it into a new chat and provide the draft, data, or other material needed.

This provides Athena's core research workflow as a prompt, rather than
installing the 109-skill library. Repeat it in new chats, or save it in a
project or custom assistant's instructions if your app supports that feature.
Browsing, file handling, and code execution depend on the app you use.

For hosts that support plugin installation, this repository also includes a
plugin package. See the [platform setup guide](docs/INSTALL_ONCE.md) for
plugin prerequisites, installation directories, verification, and updates.

### Ask normally

After either setup, describe the outcome you want:

- `Check whether the numerical claims in my draft are supported.`
- `Plan a literature review on flood mapping with satellite imagery.`
- `Help me design a reproducible ablation study.`

## What Athena does

| You provide | Athena adds | You receive |
|---|---|---|
| A research goal | The relevant skills and an ordered plan | A workflow you can inspect before execution |
| Drafts, data, or results | Evidence and consistency checks | Claims tied to reproducible sources |
| Your constraints | Explicit trade-offs and approval points | Work that stays under your control |

Athena includes **109 reusable research skills** for literature review, experiment design, scientific writing, explorable papers, figures, citation checks, rebuttals, patents, grants, and more.
Its core integrity checks are `citation-audit`, `paper-claim-audit`, and
`experiment-audit`. These specialized workflows require their documented
support files and reviewer backends; their presence in the catalog is not a
claim that those dependencies have been installed.

## See the difference

The included synthetic example illustrates why every eligible run matters: the all-run summary is **1.17 ± 1.84**, not the cherry-picked best-run difference of 3.2. Athena's research entry point asks the agent to recompute the supplied results and tie its wording to that evidence.

<img src="assets/terminal_clone.png" alt="Athena checking a numerical claim before writing" width="100%">

The expected **1.17 ± 1.84** result is reproducible offline:

```bash
python docs/demo_assets/verify_demo.py
```

This script verifies the example's arithmetic, not an end-to-end model audit.

To inspect individual pairs and input provenance with the reusable helper:

```bash
python skills/research-integrity-pipeline/scripts/paired_summary.py docs/demo_assets/demo_results.csv --metric miou --baseline baseline --candidate ours --unit percentage-points
```

It reports all paired differences, their mean and sample standard deviation,
and the input file hash. Missing or duplicate pairs stop the calculation.

## Explore

- [Start here](docs/START_HERE.md) — a guided first session
- [Install once](docs/INSTALL_ONCE.md) — keep Athena available across conversations
- [Browse the skill map](docs/SKILL_COVERAGE.md) — see what Athena can do
- [Open the explorable antenna paper](https://jiangfeng-strathclyde.github.io/Athena/examples/antenna-direction.html) — a self-contained interactive research case study
- [Understand the evidence rules](docs/DISTILLED_PUBLIC.md) — how Athena avoids unsupported claims
- [Add a skill](CONTRIBUTING.md) — contribute a reusable research workflow

## Principles

- Never fabricate results or citations.
- Recompute important numbers from source data.
- Separate verified findings, mathematical conclusions, and hypotheses.
- Explain trade-offs and ask before making consequential changes.

Original content is released under the [MIT License](LICENSE). Mirrored skills retain their upstream attribution in [skills/NOTICE.md](skills/NOTICE.md).

Questions and ideas are welcome in [GitHub Discussions](https://github.com/jiangfeng-strathclyde/Athena/discussions).
