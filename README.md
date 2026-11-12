# Athena

**Athena is an open-source Research Bot that turns a research question, paper, or dataset into a source-linked, versioned Research Release.**

[Start a research project](docs/START_HERE.md) · [Open sample release](docs/examples/antenna-direction.html) · [Install locally](docs/INSTALL_ONCE.md)

> **Alpha · local first.** The repository is Athena's control plane: it keeps
> project state, routes work, records artifacts, and exports verifiable releases.
> It does not run a hosted model, upload your files, or execute research by
> itself. A compatible local agent performs approved steps with the tools and
> accounts you choose. Read the [Alpha contract](docs/RESEARCH_BOT_ALPHA.md).

## One input, one inspectable output

| Input | Athena organizes | Output |
|---|---|---|
| A research question | A routed, ordered plan with explicit status | A versioned Research Release |
| A paper | Claims, sources, evidence state, uncertainty, and artifacts | A release that links conclusions back to evidence |
| A dataset | Recomputations, limitations, and recorded decisions | A local bundle with hashes and offline verification |

A **Research Release** is a local, versioned record of what was asked, what was
checked, what remains uncertain, and which artifacts support the result. It is
not automatically a publication, peer review, or endorsement.

## First local run

Requirements: Git and Python 3.10 or newer.

```bash
git clone https://github.com/jiangfeng-strathclyde/Athena.git
cd Athena
python -m athena init athena-demo --name "My first Research Release"
python -m athena plan --project athena-demo "Verify the supplied result and document its limits" --source docs/demo_assets/demo_results.csv --skill research-integrity-pipeline
python -m athena resume --project athena-demo
```

This fixture pins one bounded integrity step so you can complete and export it
locally. Routing can select a bounded subset for a goal; when a project uses
all three core stages, their order is `citation-tracing` →
`research-integrity-pipeline` → `explorable-paper` → Research Release.
Athena returns the next action, but it does not automatically execute the
selected skills.

`resume` returns an absolute, readable `instruction_path` to the installed
skill's actual `SKILL.md`, plus the `instruction_sha256` pinned at planning.
It also returns an absolute `result_contract.artifact_path`. Run that exact
step in your compatible local agent and write the completed result there, then
invoke the returned `checkpoint_argv` directly (preferred, without a shell) or
the self-contained `checkpoint_command`. Neither contract needs string
replacement or extra arguments. Export remains blocked until every planned
step is complete and at least one artifact is recorded.

If the task or its next step is `blocked`, both `resume` and `checkpoint` fail
closed. The Alpha does not automatically unlock a task in place: correct the
input or source problem, then run `plan` to create a new task.
The complete copy-and-run path is in [Start here](docs/START_HERE.md).

## The release gate

1. `plan` stores the goal, usable private source locators and fingerprints, a
   deterministic skill route, and each step's instruction hash.
2. `resume` returns one stable next action with the installed instruction's
   absolute readable path and pinned SHA-256. It does not call a model, and it
   blocks if those instructions have changed.
3. `checkpoint` marks that step complete and copies the supplied artifact into
   local project state.
4. `export` succeeds only after **all** steps are complete and a recorded
   artifact passes size and SHA-256 checks.
5. `verify` checks the exported release offline.

The exported draft is private and local by default. Absolute local source paths
are redacted from its task snapshot, and task-bound JSONL records are isolated
from other tasks. Athena does not publish or send it anywhere.

## A small evidence check

The included synthetic fixture contains paired changes of +3.2, +0.7, and
−0.4. The defensible all-run summary is **1.17 ± 1.84**, not the best single
run. Reporting only +3.2 would be cherry-picking.

```bash
python docs/demo_assets/verify_demo.py
```

The expected **1.17 ± 1.84** is recomputed directly from the CSV. This verifies
the example's arithmetic and README claim; it is not an end-to-end model audit.

For the reusable paired-results helper:

```bash
python skills/research-integrity-pipeline/scripts/paired_summary.py docs/demo_assets/demo_results.csv --metric miou --baseline baseline --candidate ours --unit percentage-points
```

## Install the research skill collection

The Research Bot Alpha uses a small core route. Athena also ships **110 research skills**
for literature work, experiments, writing, figures, review, patents, and grants.
Install the default reviewed selection:

```bash
python scripts/install_athena.py --auto
```

The catalog contains 110 skills; the installer selects 107 by default and
excludes three skills that require explicit review. To install only the
self-contained research integrity entry point:

```bash
python scripts/install_athena.py --agent universal --skill research-integrity-pipeline --strict-packaging --dry-run
python scripts/install_athena.py --agent universal --skill research-integrity-pipeline --strict-packaging
```

The core integrity workflows include `citation-audit`,
`paper-claim-audit`, and `experiment-audit`. Some specialized skills need
external tools, credentials, reviewer backends, or upstream support files.
Catalog presence does not mean those dependencies are installed. See
[installation](docs/INSTALL_ONCE.md) and [validation boundaries](docs/VALIDATION.md).

## Explore

- [Research Bot Alpha contract](docs/RESEARCH_BOT_ALPHA.md)
- [Quickstart](docs/START_HERE.md)
- [Sample release presentation](docs/examples/antenna-direction.html)
- [Skill map](docs/SKILL_COVERAGE.md)
- [FAQ](docs/FAQ.md)
- [Positioning](docs/POSITIONING.md)
- [Roadmap](ROADMAP.md)

## Principles

- Never fabricate results or citations.
- Keep sources untrusted until checked.
- Recompute important numbers from source artifacts.
- Separate verified findings, calculations, hypotheses, and unknowns.
- Record limitations and consequential decisions.
- Keep publication, external writes, paid compute, and deletion outside the
  default local workflow unless the user separately authorizes them.

Original project content is released under the [MIT License](LICENSE).
Mirrored skills retain upstream attribution in [skills/NOTICE.md](skills/NOTICE.md).
Contributions are welcome through [CONTRIBUTING.md](CONTRIBUTING.md).
