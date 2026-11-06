---
name: paper-poster
description: "DEPRECATED — superseded by /paper-poster-html. Kept only as a redirect for muscle memory; do not use for new posters."
argument-hint: "[paper-dir-or-pdf]"
allowed-tools: Read
---

# Paper Poster (DEPRECATED → /paper-poster-html)

This skill is retired. The LaTeX/tcbposter pipeline it described produced posters with
unbounded color palettes, no real paper figures, and no print-canvas verification, and
has been replaced by the measurement-gated HTML/CSS pipeline.

**Immediately proceed with `/paper-poster-html`**, passing through all of the user's
arguments unchanged. Do not attempt the legacy LaTeX flow.

The full legacy implementation remains available in git history
(`git log -- skills/paper-poster/SKILL.md`) if a venue ever mandates LaTeX poster
source — none is known to.

## 镜像说明（本公开仓库追加）
- 本文件为上游 ARIS 原文镜像；支持文件（scripts/、references/、../shared-references/）未随镜像分发，
  完整原件见上游仓库 https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep 。
- 执行技能时若引用支持文件，请从上游仓库解析相对路径。
