# Changelog

## 1.1.0 - 2026-11-10

### Added

- `citation-tracing`: bounded backward-reference and forward-citation discovery,
  conservative identity resolution, source-backed edge tables, screening reasons,
  and explicit coverage/stop conditions. Works with supplied material and tools
  already available in the host; it does not bundle an online citation service.
- Offline literature-workflow evaluation materials and expected checks for
  citation direction, duplicates, inaccessible text, and conflicting evidence.

### Improved

- `research-lit`: an Athena-specific, self-contained evidence-matrix mode for
  supplied sources, with inclusion/exclusion reasons, per-claim support,
  counterevidence and uncertainty, passage locators, and applicability limits.
  The original mirrored ARIS workflow and its dependency notice remain visible.
- Task routing and examples for citation tracing and external-claim evidence
  review; catalog totals are now 110 skills, with 107 selected by default.
- Plugin package version is 1.1.0. Existing installations can select the new
  skill without replacing the whole catalog; the existing installer retains
  backups when updating an installed skill.

### Scope

No third-party tool endorsement, paid service integration, or automatic claim
verification is implied. See [validation and limitations](docs/VALIDATION.md)
for the distinction between packaging checks and actual agent behavior.

Earlier changes are recorded in Git history and the existing validation reports.
