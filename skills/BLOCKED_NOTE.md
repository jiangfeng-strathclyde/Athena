# BLOCKED_NOTE — 未注册平台的 3 个技能

以下 3 个技能的 SKILL.md 原文保存在本语料树中（来自用户本地 ARIS 仓库
`D:\skills\Auto-claude-code-research-in-sleep-main\...\skills\`），但 2026-11-06 通过
QoderWake `skill manage --action create` 注册时被 daemon 安全扫描器拦截，**未安装到平台**：

| 技能 | 扫描器警告 | 人工复核结论 |
|---|---|---|
| deepxiv | "appears to exfiltrate local secrets or credentials" | 误报倾向：正文描述 DEEPXIV_TOKEN 环境变量与 SDK 自动注册行为，且声明不读取/不回显 token |
| paper-compile | "asks to bypass permissions or escalate privileges" | 误报：触发行为注释中的 `sudo apt-get install texlive-full`（本机为 Windows，该行本就无用） |
| paper-poster-html | "appears to exfiltrate local secrets or credentials" | 误报：触发词为排版术语 "design token" |

处置原则：不绕过安全扫描器（不改写内容骗过扫描）。三者功能均有替代：
论文编译用项目自有 latexmk + `scripts/validate_paper.py` 管线；文献阅读用 arxiv/alphaxiv/research-lit；海报需求低频。

如确需启用：由用户在 Console 人工审核安装，或用户明确授权后由 Max 出具**透明修订稿**（仅删/改触发行并逐行说明）再重试一次。
