# Upstream synchronization

Athena contains selected upstream skills and explicitly identified local
adaptations. Synchronization must preserve licensing, provenance, and the
dependencies required by each installed skill.

## Baselines and packaging

- The catalog is recorded in [MANIFEST.json](../clone-kit/MANIFEST.json).
- The ARIS comparison baseline is recorded in
  [UPSTREAM_SNAPSHOT.json](../clone-kit/UPSTREAM_SNAPSHOT.json).
- Most of the 87 ARIS-derived skills contain mirrored instructions, not the
  upstream scripts and shared references. Consult the dependency report before
  describing them as standalone.
- The `arxiv` skill is a standalone adaptation, with its own pinned
  [provenance](../skills/arxiv/references/provenance.json), helper, and upstream
  license. It must not be overwritten as an unchanged mirror.
- Attribution and known license discrepancies are recorded in
  [NOTICE.md](../skills/NOTICE.md) and
  [TRANSPARENCY_LOG.md](TRANSPARENCY_LOG.md).

## Review a proposed update

1. Select an explicit upstream commit or release. Compare it with the recorded
   baseline in a dedicated checkout. Inspect new, changed, and removed files;
   do not execute fetched installers or skill commands merely to inspect them.
2. Classify each change as mirrored text, a local adaptation, or a new skill.
   For adaptations, reconcile upstream fixes with the local behavior and tests.
   Check scripts, templates, references, imports, and external tools as well as
   `SKILL.md`; the static link scanner does not cover every dependency.
3. Verify redistribution permission for every bundled file. Preserve upstream
   copyright and license text. Record the source commit, source checksum where
   applicable, local changes, and runtime requirements with the installed skill.
4. Review executable behavior and host assumptions. Existing user data must not
   be deleted or overwritten to recover from a failed dependency check. Missing
   credentials or reviewer services must remain explicit limitations.
5. Test the skill after installing it outside the Athena checkout. Run its
   fixture tests, strict packaging check, and appropriate real-host acceptance
   cases. Distinguish mocked requests, live helper calls, and agent-driven runs.
6. Update the manifest or adaptation provenance, notices, and dated validation
   record. Commit only the reviewed changes. Publishing announcements is a
   separate maintainer action.

`scripts/upstream_diff.py` is a legacy comparison utility that updates an
upstream cache. Inspect its filesystem and Git operations before using it;
this procedure does not require running it or changing its baseline.

## Reusable checks

```text
python scripts/check_skill_dependencies.py
python scripts/check_skill_dependencies.py --skill arxiv --strict
python -m unittest discover -s tests -v
python scripts/check_repo_consistency.py
```

Use [host acceptance](HOST_ACCEPTANCE.md) for model-driven checks. Passing a
packaging scan establishes neither tool availability nor scientific validity.
New upstream skills are reviewed individually rather than added automatically.
