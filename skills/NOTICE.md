# NOTICE · 上游版权与许可声明

本目录是 **Max 的技能库**：技能全文按“有许可声明才镜像”的原则策展。
镜像部分的 upstream 归属如下，版权与许可随原文保留：

- **Auto-claude-code-research-in-sleep (ARIS)**
  https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep
  Copyright (c) 2026 wanshuiyin, MIT License.（87 个科研技能）
- **crawl4ai-skill** — Copyright (c) Lancelin, MIT-0 License.
- **excel-formula** — MIT License（upstream frontmatter 声明，作者未署名）。
- **自研技能（4 个）** — academic-paper-narrative、research-integrity-pipeline、
  skill-evolution-manager、patent-disclosure-drafter；
  Copyright (c) 2026 Thats-me contributors, MIT License。
  其中 patent-disclosure-drafter 的流程思想借鉴 `handsomestWei/patent-disclosure-skill`，文本为自研；
  公开版已移除私有仓库路径引用与内部角色名。

MIT / MIT-0 许可全文见各上游仓库。本仓库对上游内容仅做：
策展、镜像（逐字保留 SKILL.md 原文）、中文导读（路由表/清单），
并在部分技能文末追加"环境适配"附注段（声明支持文件源目录解析方式）；
追加段以注释性说明形式存在，不改变上游指令语义。

## 未镜像技能（只列名，不镜像全文）

21 个本地存在的技能**不**进入本目录，原因见 `../docs/TRANSPARENCY_LOG.md` 第 5 节：
16 个上游未声明许可（公开再分发授权不明）、2 个平台内部技能、3 个厂商技能。
它们在 `../clone-kit/MANIFEST.json` 中以 `mirrored: false` 标记并附原因。

## 平台安装状态差异

其中 3 个技能（deepxiv、paper-compile、paper-poster-html）在作者的平台注册中被安全扫描器
拦截而未安装；镜像全文仅供本地自行审查使用。详见 `../docs/TRANSPARENCY_LOG.md`。

## 快照

镜像快照日期：2026-11-06；清单与版本见 `../clone-kit/MANIFEST.json`。
