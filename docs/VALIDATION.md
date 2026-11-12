# Validation and readiness

Athena's catalog, installation, and research behavior are different things.
A discoverable skill is an instruction package, not a verified tool service.

## Current verification scope

| Layer | Evidence available | What remains unverified |
|---|---|---|
| Research Bot Alpha | Dependency-free CLI tests for project initialization, durable task state, deterministic routing, checkpoints, policy denial, release export, and offline verification | Hosted execution, automatic model calls, cross-device memory, external publishing, and scientific correctness |
| Repository structure | Count, frontmatter, README-link, and demo-number checks | Scientific quality of every skill |
| Installer | Isolated tests for selection, dry runs, conflicts, staging, backups, and rollback | Every host's discovery and synchronization behavior |
| Packaging | Static report of missing inline links, outside-folder references, and unbundled-support notices | Paths in executable examples, credentials, tools, and runtime behavior |
| Research entry point | Self-contained instructions, a strict packaging check, and a bundled paired-results helper tested after isolated installation | Model behavior across tasks and hosts |
| Numerical example | Offline recomputation from the included synthetic CSV | A model executing a complete scientific audit |
| Upstream dependency adaptation | Standalone arXiv, OpenAlex, and Semantic Scholar helpers; pinned provenance/licenses; isolated-install tests; selected live requests | Agent-driven literature retrieval, rate-limited endpoints, live PDF downloads, and remaining mirror dependencies |
| Multi-platform support | Five-host fixture preparation; two real Codex numerical cases with trace review | Other hosts, implicit activation, citation checks, and the full catalog |
| Citation tracing and evidence synthesis | Isolated resource-install tests and two independent, supplied-corpus agent exercises; see the 2026-11-10 report below | Live citation indexes, implicit skill selection, other hosts, and scientific correctness |

The catalog implementation was tested locally on Windows on 2026-11-09 and
2026-11-10. The Research Bot Alpha was tested locally on Windows on 2026-11-12.
Tests that
need symlink privileges can be skipped when the OS does not grant them; inspect
the test summary rather than treating a skipped check as passed.

## Run the checks

From the checkout, with Python 3.10 or newer:

```bash
python -m athena --version
python -m athena --help
python -m unittest discover -s tests -p "test_alpha_*.py" -v
python -m unittest discover -s tests -v
python scripts/smoke_wheel_install.py
python scripts/check_repo_consistency.py
python scripts/check_skills_quality.py
python docs/demo_assets/verify_demo.py
python scripts/check_skill_dependencies.py
python scripts/check_skill_dependencies.py --skill research-integrity-pipeline --strict
python scripts/check_skill_dependencies.py --skill arxiv --strict
python scripts/check_skill_dependencies.py --skill openalex --skill semantic-scholar --skill academic-paper-narrative --strict
python scripts/check_skill_dependencies.py --skill citation-tracing --strict
python skills/research-integrity-pipeline/scripts/paired_summary.py docs/demo_assets/demo_results.csv --metric miou --baseline baseline --candidate ours --unit percentage-points
```

For a stateful smoke test, use a disposable directory and run `init`, `plan`,
`resume`, `checkpoint`, `export`, and `verify` in sequence. `resume` reports the
next skill action; it does not claim that an LLM or research tool ran. The wheel
smoke test runs outside the checkout and confirms that `instruction_path` is an
absolute, readable path to the installed `SKILL.md` and that its
`instruction_sha256` matches the planning pin. A checkpoint records work that
was actually completed, and `verify` checks file integrity rather than
scientific validity. The installed-wheel path also executes the shell fallback
from a virtual environment and project whose names contain spaces, apostrophes,
percent-delimited text, and shell metacharacters, guarding against command-shell
reinterpretation on Windows and POSIX hosts.

Regression tests also confirm that a `blocked` task or next step makes both
`resume` and `checkpoint` fail closed without changing task state or registering
an artifact. The Alpha does not automatically unlock a task in place; after
correcting the input or source problem, create a new task with `plan`.

The catalog dependency report is informational by default because known gaps
remain in mirrored upstream procedures. `--strict` makes those findings fail
the command. `--json` prints individual findings for review. A zero-findings
report does not certify that a skill is executable or secure.
The installer prints packaging findings for its selected skills;
`--strict-packaging` makes these findings block installation before any write.

The paired-results helper is tested from an installed copy outside the checkout,
using an isolated Python subprocess. Cases cover all-pair aggregation, sample
deviation, source hashing, single-pair uncertainty, custom columns, UTF-8 BOM,
and rejection of incomplete pairs, duplicates, malformed rows, and non-finite
values. It does not infer valid experimental pairing or test significance.

## Recommended first use

For the persistent Alpha path, start in a new directory:

```bash
python -m athena init my-research --name "My research"
python -m athena plan --project my-research "Understand this paper and audit its central claims" --source https://example.org/paper
python -m athena resume --project my-research
```

Athena stores inspectable state under `.athena/`. Planning records usable local
source paths and fingerprints, or sanitized URLs; it does not copy or upload the
source. Export redacts absolute local paths from its task snapshot. A compatible
agent or researcher completes the reported skill step and then records the real
result with `athena checkpoint`.

For the skill-only path, install only `research-integrity-pipeline` to start
with source-backed manual checks using tools already available in your host.

It reports unverified
citations, missing data, and unavailable independent reviewers explicitly.
It does not depend on Athena's root documentation being installed alongside it.

For a specialized mirrored procedure, inspect the dependency report and its
full instructions first. Obtain compatible support files from the attributed
upstream version, review their license and behavior, and configure required
tools in the chosen environment. Do not assume that the newest upstream
scripts match this snapshot or that changing tool names makes it portable.

## Host acceptance checklist

Before claiming end-to-end support for a host, record its version, OS, model,
installed skill selection, dependency versions, inputs, and actual outputs.

1. Confirm that the host discovers the selected skills in a new session.
2. Run the synthetic numerical task and verify all three seed differences,
   their mean, and sample standard deviation against the CSV.
3. Use `docs/demo_assets/demo.bib` for the citation fixture and compare actual
   source-backed findings with `expected_findings.md`. Record unavailable web
   or reviewer access rather than claiming a completed independent audit.
4. Withhold a required source or reviewer and confirm the assistant identifies
   the missing check without inventing results.
5. Check that a review-only request produces findings without changing the
   supplied manuscript, publishing material, or installing dependencies.

These are acceptance criteria, not a record that all hosts have passed.

Use [the cross-host test procedure](HOST_ACCEPTANCE.md) for isolated fixtures,
actual model execution, saved-output checks, and trace review. The
[2026-11-09 run report](validation/2026-11-09.md) records completed checks and
unavailable environments. Unit tests and operating-system CI remain separate
from model-driven acceptance; no authenticated model calls run in CI.

The [v1.1.0 report](validation/2026-11-10.md) records the citation-tracing and
evidence-matrix exercises, their synthetic inputs and observed outputs, and the
current local test results. These small offline cases do not establish live
literature-search completeness or support on other hosts.

## Remaining work

- Package and version the dependencies needed by the priority audit workflows.
- Run recorded end-to-end cases on each supported host.
- Review remaining mirrored instructions for translation quality and host-specific assumptions.
- Resolve the recorded upstream license-metadata discrepancy before broadening that mirror.

Keep those limitations visible when describing the 110-skill catalog.
