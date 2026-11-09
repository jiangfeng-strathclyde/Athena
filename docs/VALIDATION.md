# Validation and readiness

Athena's catalog, installation, and research behavior are different things.
A discoverable skill is an instruction package, not a verified tool service.

## Current verification scope

| Layer | Evidence available | What remains unverified |
|---|---|---|
| Repository structure | Count, frontmatter, README-link, and demo-number checks | Scientific quality of every skill |
| Installer | Isolated tests for selection, dry runs, conflicts, staging, backups, and rollback | Every host's discovery and synchronization behavior |
| Packaging | Static report of missing inline links, outside-folder references, and unbundled-support notices | Paths in executable examples, credentials, tools, and runtime behavior |
| Research entry point | Self-contained instructions, a strict packaging check, and a bundled paired-results helper tested after isolated installation | Model behavior across tasks and hosts |
| Numerical example | Offline recomputation from the included synthetic CSV | A model executing a complete scientific audit |
| Multi-platform support | Documented host directories; CI configured for Windows, Linux, and macOS on Python 3.10 and 3.13 | A successful CI run until the workflow actually executes; host-level acceptance tests |

The implementation was tested locally on Windows on 2026-11-09. Tests that
need symlink privileges can be skipped when the OS does not grant them; inspect
the test summary rather than treating a skipped check as passed.

## Run the checks

From the checkout, with Python 3.10 or newer:

```bash
python -m unittest discover -s tests -v
python scripts/check_repo_consistency.py
python scripts/check_skills_quality.py
python docs/demo_assets/verify_demo.py
python scripts/check_skill_dependencies.py
python scripts/check_skill_dependencies.py --skill research-integrity-pipeline --strict
python skills/research-integrity-pipeline/scripts/paired_summary.py docs/demo_assets/demo_results.csv --metric miou --baseline baseline --candidate ours --unit percentage-points
```

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

Install only `research-integrity-pipeline` to start with source-backed manual
checks using tools already available in your host. It reports unverified
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

## Remaining work

- Package and version the dependencies needed by the priority audit workflows.
- Run recorded end-to-end cases on each supported host.
- Review remaining mirrored instructions for translation quality and host-specific assumptions.
- Resolve the recorded upstream license-metadata discrepancy before broadening that mirror.

Keep those limitations visible when describing the 108-skill catalog.
