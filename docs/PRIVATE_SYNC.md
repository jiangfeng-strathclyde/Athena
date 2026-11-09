# PRIVATE_SYNC · Private parties ↔ Synchronization protocol for the public manual

> Private copies (including memory and project facts) are stored only locally by the author; public versions only carry**Migrationable Methods and Red Lines**。
> This document sets out how they should be maintained.“The unity, the isolation.”。

## Trigger timing

- When the private distilled guide changes, review it for public-safe methodological updates without copying private paths, facts, or memory.
- Open `docs/DISTILLED_PUBLIC.md` Amended;
- First Monday of the month, synchronized with upstream. batching Run together.

## Steps

1. Run drift inspection (output count and belonging only, without writing private contents into the warehouse):

   ```bash
   python scripts/private_sync_diff.py
   ```

2. Yeah. `only-private` Article-by-article determination (Note: match)**Word-by-word matching**，The public rewrite entry will appear on both sides of the list and will need to be manually identified as“Modified with different wording”，Not new drifting:
   - **Removable**（Universal red lines, collaborative algorithms, writing engagements, methodological links)→ (b) Rewrite de-identification and incorporate it into the public version of the corresponding section;
   - **Non-movable**（Project facts, calibre details, evidentiary gaps, collaborators ' information)→ Stay still, stay in the private version;
3. Yeah. `only-public` (b) To decide, article by article, whether it has been abandoned in a private version; to remove it from the public version and to record a line in the transparency log;
4. Changes to the public version: run again `scripts/check_repo_consistency.py` and `docs/demo_assets/verify_demo.py`；
5. Private Packer Re-export (staff bag) + Memory packs, excluded. secrets），A snapshot of the same date as the public edition;
6. In this document“History”Section Add a row: Date + On both sides. sha + Number of migration bars (%)**Do Not Write**）。

## Red Line

- Private memory bags, keys, unpublished data, identifiable information**Never.**Access to open warehouses;
- The output of the drift check shall not be pasted into the warehouse file (which may contain private representations);
- When a public version conflicts with a private version, the private version is used as a standard of conduct and the public version as a standard of external commitment; the difference must be visible in the original script.

## History

| Date | private sha | public sha | Number of migration bars | Remarks |
|---|---|---|---|---|
| 2026-11-06 | ♪ See the current run ♪ | ♪ See the current run ♪ | 0 | Agreement-building; summary of first-run drifting only reports in session |
