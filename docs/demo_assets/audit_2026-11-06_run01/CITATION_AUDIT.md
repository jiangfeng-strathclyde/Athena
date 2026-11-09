# Citation Audit Report（Real Run · (Synthetic data)

**Date**: 2026-11-06
**Bib file**: `docs/demo_assets/demo.bib`（Synthetic sample, bury 3 (Error)
**Total entries**: 5
**Reviewer**: Zero context independent review sub-agent + It's real. web Verification (%1)Crossref / arXiv / NeurIPS proceedings）
**Decline declaration**: None in this environment codex MCP Cross-model backends, downgraded by protocol to homologue zero context and explicit here;web Retrieval is a real call, not a memory match.

## Summary

| Verdict | Count |
|---------|-------|
| KEEP    | 2     |
| FIX     | 2     |
| REMOVE  | 1     |

## Priority Fixes

### FIX: ronneberger2016unet
- Year Error: Entry Write 2016，canonical Record As **MICCAI 2015**（LNCS 9351）
- Evidence:https://api.crossref.org/works/10.1007/978-3-319-24574-4_28
- ACTION：year 2016 → 2015

### FIX: he2016resnet
- Author ' s order error: the first author should read **Kaiming He**，Entry Xiangyu Zhang In the first place.
- Evidence:https://api.crossref.org/works/10.1109/CVPR.2016.90
- ACTION：Restore canonical Author order

### REMOVE: wang2024swinsr
- Articles and venue None of them can be retrieved:arXiv Title search zero hits;“ICSEO” The meeting does not exist; otherwise, by `@article` Carrying the name of the meeting
- Evidence:https://export.arxiv.org/api/query?search_query=ti:%22SwinSR%22 （Zero hits)
- ACTION：Delete the entry; text to be rewritten if quoted

## All-Clean Entries

- `vaswani2017attention` — NeurIPS 2017 Official records are field-by-field.
- `chen2018deeplabv3plus` — ECCV 2018 Consistent records (%)Springer DOI 10.1007/978-3-030-01234-2_1）

## In contrast to expectations, hit. `../expected_findings.md` A All Tables 3 Article, and**Not**Misreporting 2 It's really negative.
