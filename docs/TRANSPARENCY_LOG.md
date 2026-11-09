# Transparency log

This log records known limitations, corrections, and redistribution decisions.
Historical review notes are not security certifications.

## 1. Skills blocked by a platform scanner

On 2026-11-06, a platform scanner blocked registration of three mirrored
skills: `deepxiv`, `paper-compile`, and `paper-poster-html`. They were not
installed on that platform.

The recorded manual review suggested that token-handling documentation,
an optional privileged package-install command, and the phrase "design token"
might explain the warnings. Those explanations remain hypotheses, not proof
of false positives. The warnings were retained rather than bypassed.
See [the detailed record](../skills/BLOCKED_NOTE.md).

The Python installer now excludes these three skills by default. Users must
review and explicitly authorize each one before installing it. Plugin imports
and manual copies have their own host-controlled review process; the Python
filter does not apply to those routes.

## 2. Public-release boundary

The public project is intended to exclude:

- Private long-term memory and collaboration histories.
- Keys, tokens, webhook secrets, and account credentials.
- Unpublished experimental data, manuscripts, reviews, and private evidence-gap lists.
- Personal details not explicitly selected for public release.

This boundary is a release requirement, not a claim that a comprehensive
secret or privacy audit has been performed.

## 3. Recorded corrections

An earlier review misread `0.722` as `0.723` in a low-resolution PDF and
compared training durations defined on different bases. The original record
states that the sources were rechecked and those challenges withdrawn.
The lesson is to verify an apparent discrepancy against the original evidence
before presenting it as an error.

## 4. Known capability limits

- Many mirrored procedures reference upstream scripts and support documents
  that are not bundled here. File discovery does not establish runtime readiness.
- Independent review needs an available, appropriately configured reviewer.
  A narrower same-agent check must be labeled self-review, not a completed
  independent or cross-model audit.
- Public workflows must work from public instructions and supplied task
  material. Private memory is not a hidden prerequisite or authority.
- The mirror is a snapshot; version and source records are in
  [the manifest](../clone-kit/MANIFEST.json).
- Static packaging checks and the synthetic arithmetic demo do not establish
  scientific quality or end-to-end behavior. See [validation scope](VALIDATION.md).

## 5. Listed but not mirrored

The manifest records 21 individually named skills that are not redistributed.

**Sixteen with no clear upstream redistribution permission:**

analytics-data-analysis, chart-craft-plus, data-analysis-pro, data-extractor,
data-scientist, data-visualization, document-processor, excel,
excel-data-analysis-and-report-generation, excel-weekly-dashboard, finance-charts,
market-research-litiao, prompt-extractor, py-math-viz, report-generation,
skill-file-converter.

**Two platform-internal skills:**

qoderwake-assistant, wake-dws-cli.

**Three vendor-published skills not redistributed here:**

alibabacloud-dataworks-infra-manage, alibabacloud-dataworks-workspace-manage,
alibabacloud-sls-query.

A separate manifest entry tracks the remaining 74 Orchestra skills outside
the curated mirror. Future additions require source, license, dependency,
and compatibility review following [the upstream sync process](UPSTREAM_SYNC.md).

## 6. Recorded license-metadata discrepancy

For Orchestra AI-Research-SKILLs 1.4.0, the recorded README and repository
LICENSE indicate MIT, with copyright attributed to the Claude AI Research
Skills Contributors (2025), while `package.json` declares ISC. This repository
used the repository LICENSE for its 12-skill subset and retains attribution
in [NOTICE.md](../skills/NOTICE.md). The discrepancy remains unresolved;
future expansion should revisit the upstream evidence rather than assume
that metadata is consistent.

## 7. Installation and verification improvements, 2026-11-09

The installer now stages copies before replacement, retains prior versions,
attempts rollback on replacement failure, rejects unsafe source/target overlap,
and supports non-mutating previews and selected-skill installs. Automatic
setup uses a shared location and adds Claude Code's native location when
detected, avoiding additional native copies for shared-directory hosts.

The original `research-integrity-pipeline` entry was rewritten as self-contained
guidance. It no longer references absent private source directories. Missing
sources, tools, or independent reviewers are reported explicitly.

Isolated installer tests and a static dependency report have been added.
CI is configured for Windows, Linux, and macOS; configuration alone is not
a completed run. Unbundled upstream dependencies and host-level acceptance
testing remain open work.

Installation now reports known packaging findings for the selected skills;
`--strict-packaging` can block installation before writing. The entry point
also includes an offline paired-results calculator, tested from an isolated
installed copy. It reports source hashes, all pair differences, and sample
variability, and rejects incomplete or duplicate pairs. This verifies
descriptive arithmetic, not experimental validity or model review behavior.
