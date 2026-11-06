# Citation Audit Report（真实运行 · 合成数据）

**Date**: 2026-11-06
**Bib file**: `docs/demo_assets/demo.bib`（合成样例，埋入 3 处错误）
**Total entries**: 5
**Reviewer**: 零上下文独立审稿子代理 + 真实 web 核验（Crossref / arXiv / NeurIPS proceedings）
**降级声明**: 本环境无 codex MCP 跨模型后端，按协议降级为同族模型零上下文自审并在此明示；web 检索为真实调用，非记忆匹配。

## Summary

| Verdict | Count |
|---------|-------|
| KEEP    | 2     |
| FIX     | 2     |
| REMOVE  | 1     |

## Priority Fixes

### FIX: ronneberger2016unet
- 年份错误：条目写 2016，canonical 记录为 **MICCAI 2015**（LNCS 9351）
- 证据：https://api.crossref.org/works/10.1007/978-3-319-24574-4_28
- ACTION：year 2016 → 2015

### FIX: he2016resnet
- 作者顺序错误：第一作者应为 **Kaiming He**，条目把 Xiangyu Zhang 放在首位
- 证据：https://api.crossref.org/works/10.1109/CVPR.2016.90
- ACTION：恢复 canonical 作者顺序

### REMOVE: wang2024swinsr
- 论文与 venue 均检索不到：arXiv 标题检索零命中；“ICSEO” 会议不存在；另以 `@article` 承载会议名
- 证据：https://export.arxiv.org/api/query?search_query=ti:%22SwinSR%22 （零命中）
- ACTION：删除该条目；正文如有引用需改写

## All-Clean Entries

- `vaswani2017attention` — NeurIPS 2017 官方记录逐字段一致
- `chen2018deeplabv3plus` — ECCV 2018 记录一致（Springer DOI 10.1007/978-3-030-01234-2_1）

## 与期望对照

命中 `../expected_findings.md` A 表全部 3 条，且**未**误报 2 条真阴性。
