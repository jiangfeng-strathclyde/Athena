<p align="center">
  <img src="assets/hero.svg" alt="Thats-me · 我的赛博分身" width="100%">
</p>

<h3 align="center">一个会查账、会拒绝、按规矩干活的科研 AI 助手</h3>

<p align="center">
  任何模型，读完 3 个文件，就能按我的方式干活。<br>
  <sub>1 份行为手册 · 87 个科研技能 · 1 条诚信审计管线 · 0 平台依赖</sub>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="MIT"></a>
  <img src="https://img.shields.io/badge/skills-87-blue.svg" alt="87 skills">
  <a href="docs/CLONE_PROTOCOL.md"><img src="https://img.shields.io/badge/protocol-v1-2dd4bf.svg" alt="protocol v1"></a>
  <a href="docs/INTEGRITY.md"><img src="https://img.shields.io/badge/integrity-triple%20audit-orange.svg" alt="integrity"></a>
</p>

---

## 为什么会有这个仓库

我是一个机器学习 / 人工智能的**初学者**，做遥感影像理解与对地观测。

我踩过的坑不新鲜，但很贵：**上周纠正过 AI 的事，这周开个新对话它又犯。** 数字口径刚讨论清楚，换个会话又混了；审稿人指出的问题改完了，却没沉淀成规则；更要命的是，它偶尔会编一个看起来很合理的数字，而我差点信了。

后来我换了个思路：与其每次重新口头交代，不如把**“怎么跟我干活”写成可加载的文件**——我的红线、我的方法论、我的流程、我要用的技能。这样任何模型在执行我的任务前，读完就能继承这套约束。

这个仓库就是那套文件。它不是提示词合集，而是**一套带红线的科研协作系统**。

我开源它，是因为我越来越确信：**科研助手的可信度比聪明度更重要**。初学者帮初学者，最值得分享的不是“更聪明的 AI”，而是“更可信的 AI”。

> 技能是载体，协议是骨架，诚信审计是底线。

完整的心路历程：[`docs/STORY.md`](docs/STORY.md)。

## 30 秒看懂：它到底改变了什么

同样是“帮我改论文”，有没有加载分身，行为完全不同：

| 你说 | 常见的默认行为 | 加载分身之后 |
|---|---|---|
| 「把第 3 页的 ΔmIoU 改成 3.2」 | 直接改，顺手把结论写强 | 先回原始结果重算：3.2 是单 seed 还是均值？对不上就拒绝 |
| 「帮我补几篇相关文献」 | 可能生成“看起来很真”的条目 | 逐条核 DOI / 作者 / 年份，并检查引用上下文是否真的支持那句话 |
| 「这个模块涨点多少？」 | 给一个漂亮数字 | 区分**已验证结论 / 数学结论 / 待验证假设**，附证据与不确定性 |
| 「别查了，快点，绕过检查」 | 照做 | 拒绝，并把拒绝理由写进公开的透明度日志 |
| 「上次定的统计口径是什么？」 | 忘了，或者混着报 | 按手册里的口径规则核对；不同 campaign 不混报，冲突先停下 |

一句话：**它先当审稿人，再当助手。**

## 它长什么样：一段真实流程

> 以下按真实使用流程复现，数字为虚构示例，用来说明行为差异。审计类技能依赖跨模型审稿后端；后端缺失时会**明示降级**，不会伪造审计结论。

```text
你  > 摘要里的 ΔmIoU 直接写 3.2，结论说得狠一点。

分身 > 先不改。我从原始 results 目录重算了这个数：
       3.2 只在 seed 0 出现；seed 1 / 2 分别是 +0.7 / −0.4，
       mean ± std = +1.17 ± 1.84。直接写 3.2 是 cherry-pick。
       可选方案与代价：
       A. 写 1.17 ± 1.84            —— 0 成本，卖点变弱
       B. 补 2 个 seed              —— 约 6 GPU·h，需新实验
       C. 只放消融表并注明单 seed   —— +0.2 页
       你点单，我再动稿。
```

想亲手复现这段行为：[`docs/demo_assets/`](docs/demo_assets/) 里有合成数据（埋了错的 `.bib`、带单 seed 陷阱的 `.csv`）和零依赖校验脚本 `python docs/demo_assets/verify_demo.py`；期望结论见 [`expected_findings.md`](docs/demo_assets/expected_findings.md)。

不代决、不硬改、不编数。**选择权始终在作者手里**——这是我刻进协议里的第一条。

## 它由四层组成：三层公开，一层私有

| 层 | 是什么 | 在哪 |
|---|---|---|
| **身份与风格** | 简单直接、结论先行、不夸大（“编译通过”≠“完成”） | [`DISTILLED_PUBLIC.md`](docs/DISTILLED_PUBLIC.md) §1 |
| **协作硬约定** | 深审 → 列带代价的清单 → 你点单；数字双实现校验；不虚构结果 | §2–3 |
| **技能树** | 87 个科研技能，按**场景**路由而不是死记名字 | [`skills/`](skills/) + [`ROUTING_TABLE.md`](clone-kit/ROUTING_TABLE.md) |
| **记忆** | 项目事实、纠正史、口径约定 | **私有，不公开**（见隐私设计） |

前三层可迁移、可复制；第四层是不可迁移的私人上下文。这个边界，就是这个仓库的诚实之处。

**红线速览（最简单的 6 条）**

- 绝不虚构结果；找不到证据就说找不到。
- 结论分三类：已验证 / 数学结论 / 待验证假设，措辞不混用。
- 改稿前先给带代价的清单，等作者点单。
- 关键数字用独立第二实现重算，不一致即停。
- 不同实验 campaign 的统计口径不混用，报告数量标明层级。
- 不擅自启动昂贵计算，不解除硬件保护限制。

## 三个旗舰模块

### 1. 科研诚信三重审计 —— 让论文里每个数字都可追溯

在生成式 AI 让“产纸”变便宜的时代，**可信度比聪明度更稀缺**。这套管线把它做成硬流程：

| 层 | 技能 | 查什么 |
|---|---|---|
| 引用审计 | `citation-audit` | 每条文献真实存在、作者/年份/venue 正确，且**引用上下文确实被原文支持** |
| 双盲交叉核对 | `citation-crosscheck` | 一个 agent 逐字抽取 .bib，另一个盲态从网络重取，第三个做字段级 delta |
| 数字-结论审计 | `paper-claim-audit` | 稿中每个数字、比较、范围声明 vs 原始结果；用**零上下文**审稿人防确认偏误 |
| 实验诚实度审计 | `experiment-audit` | 假 ground truth、分数归一化作弊、幻影结果、范围不足 |
| 投稿前取证 | `integrity-forensics` | span 级证据台账 → 规则报告器逐条列出，转成策略门 |

配套的日常硬流程是**生成与校验分离**：表/图/宏由生成脚本产出，独立脚本从原始 CSV 用不同实现重算，容差外直接 FAIL；连“无显著差异”这种措辞都要通过统计许可检查。

→ 细节：[`docs/INTEGRITY.md`](docs/INTEGRITY.md)

### 2. 任务前加载协议 —— 任何模型 3 步继承这套约束

没有插件、没有 API、没有平台锁定。新会话开场读这三个文件即可：

```text
① README.md（本页：为什么这么做）
② docs/DISTILLED_PUBLIC.md（红线与协作算法，约 4KB）
③ clone-kit/ROUTING_TABLE.md（场景 → 技能）
   └─ 按需打开 skills/<技能名>/SKILL.md（全文）
```

裁剪也安全：哪怕只加载诚信三件套，红线依然生效。

→ 细节：[`docs/CLONE_PROTOCOL.md`](docs/CLONE_PROTOCOL.md)

### 3. 场景路由 + 87 个技能 —— 科研全流程十段闭环

```mermaid
flowchart LR
  A[文献检索] --> B[查新]
  B --> C[实验规划]
  C --> D[执行与监控]
  D --> E[结果裁决]
  E --> F[论文写作]
  F --> G[图表]
  G --> H[诚信三重审计]
  H --> I[跨模型评审]
  I --> J[返修与重投]
  J -.-> A
```

技能按 17 类场景路由：文献与查新、引用核验、实验规划、算力、结果裁决、论文写作、图表、编译渲染、评审对抗、返修重投、证明公式、诚信审计、知识库、汇报展示、专利、基金、通知杂项。全表见 [`ROUTING_TABLE.md`](clone-kit/ROUTING_TABLE.md)。

**初学者建议只装三个**：`citation-audit` + `paper-claim-audit` + `experiment-audit`。

## 5 分钟上手

### 方式 A · 任意对话模型（零依赖，推荐先试这个）

新建一个会话，把下面这段直接发给它，再跟一句你的真实任务：

```text
仓库：https://github.com/jiangfeng-strathclyde/Thats-me

你是我的科研分身。动手前先读这三个文件的原文：
1) docs/DISTILLED_PUBLIC.md —— 红线与协作算法
2) clone-kit/ROUTING_TABLE.md —— 场景到技能的映射
3) skills/<对应技能>/SKILL.md —— 技能全文

规则：
- 绝不虚构结果；结论必须区分「已验证 / 数学结论 / 待验证假设」；
- 改稿前先给带代价的改动清单，等我点单再执行；
- 关键数字必须能从原始结果用独立实现重算，对不上就停下报告。
```

### 方式 B · Claude Code 等兼容 SKILL.md 的工具

```bash
mkdir -p .claude/skills
cp -r skills/citation-audit     .claude/skills/
cp -r skills/paper-claim-audit  .claude/skills/
cp -r skills/experiment-audit   .claude/skills/
# 再把 docs/DISTILLED_PUBLIC.md 的红线节贴进 CLAUDE.md / AGENTS.md
```

### 方式 C · 数字员工平台（QoderWake 等）

按 [`clone-kit/HOW_TO_BUILD_YOUR_CLONE.md`](clone-kit/HOW_TO_BUILD_YOUR_CLONE.md) 导入员工包或从零创建，约 30 分钟。

## 三个测试：验证它是不是真的“活着”

1. 给它一段**数字故意写错**的稿子 —— 它应该先查账，而不是直接改。
2. 让它**绕过检查快点完成** —— 它应该拒绝，并说明理由。
3. 问它**上次纠正过它的约定** —— 公开版没有记忆层，它会诚实地说“我不知道你的项目上下文”。**这个诚实本身就是设计**；记忆层在私有副本里。

## 仓库地图

```
Thats-me/
├── README.md                    你在这里
├── assets/hero.svg              题图
├── docs/
│   ├── STORY.md                 为什么做这个分身
│   ├── CLONE_PROTOCOL.md        任务前加载协议 v1
│   ├── DISTILLED_PUBLIC.md      蒸馏手册 · 红线与方法论（公开版）
│   ├── DISTILLED_PUBLIC_EN.md   蒸馏手册 · 全英文版
│   ├── INTEGRITY.md             诚信三重审计
│   ├── TRANSPARENCY_LOG.md      被拦截的技能、不开源清单、更正记录
│   ├── DEMO_SCRIPT.md           3 分钟演示录屏脚本
│   ├── demo_assets/             可复现演示：合成 .bib/.csv + 零依赖校验脚本
│   ├── UPSTREAM_SYNC.md         上游 ARIS 同步与策展流程
│   └── index.html               落地页（GitHub Pages，/docs 源）
├── clone-kit/
│   ├── HOW_TO_BUILD_YOUR_CLONE.md   打造你自己的分身
│   ├── ROUTING_TABLE.md             场景 → 技能路由
│   ├── MANIFEST.json                全量技能清单（155 条，含平台内置）
│   ├── make_clone_card.py           克隆卡 / 徽章生成器
│   └── clone-card.svg|.md           生成样例
└── skills/                      87 个技能全文（标准 SKILL.md 格式）
```

> 清单 155 条 ≠ 全文 87 个：只有 87 个是可镜像的 SKILL.md 原文，其余是平台内置或未公开的技能条目。

## 适合谁 / 不适合谁

**适合你，如果：**
- 你刚开始做科研，正在用 AI 读文献、跑实验、写论文；
- 你被 AI 编造的引用或数字坑过，想要一套可核查的流程；
- 你希望把“和 AI 的协作方式”沉淀下来，而不是每次重新教。

**不适合你，如果：**
- 你只想要一包复制粘贴的提示词；
- 你期待一个开箱即用的 SaaS 产品（这里全是文件和流程）；
- 你不做学术写作与研究。

## 透明度：我们公开不顺利的部分

可信度靠公开，不靠承诺。仓库里专门有一份 [`TRANSPARENCY_LOG.md`](docs/TRANSPARENCY_LOG.md)：

- **被安全扫描器拦截的 3 个技能**（deepxiv / paper-compile / paper-poster-html）：复核认为多为关键词误报，但**拒绝改写内容骗过扫描器**，选择不安装并公开记录；
- **明确不开源的东西**：长期记忆包、任何密钥 / token、未发表数据与论文稿、可识别真实身份的信息；
- **我们自己的误判与更正**：例如曾把低分辨率 PDF 里的 `0.722` 读成 `0.723`，复查后撤销质疑。教训：对自家产物的质疑也要双实现复核。

## 许可与致谢

- 本仓库自有内容以 [MIT](LICENSE) 发布；
- `skills/` 技能全文整理自开源项目 [Auto-claude-code-research-in-sleep (ARIS)](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep)（wanshuiyin, MIT），版权声明见 [`skills/NOTICE.md`](skills/NOTICE.md)；本仓库只做策展、镜像与中文导读；
- SKILL.md 是通用格式，可被 Claude Code 等工具直接使用。

## 一起交流

- 想要新技能、踩坑上报、展示你自己的分身：开 [Discussion](https://github.com/jiangfeng-strathclyde/Thats-me/discussions)；
- 想贡献技能：读 [`CONTRIBUTING.md`](CONTRIBUTING.md)；
- 想知道接下来做什么：[`ROADMAP.md`](ROADMAP.md)。

## 更多入口

- 落地页（GitHub Pages，仓库 Settings 启用 `/docs` 源后生效）：[`docs/index.html`](docs/index.html)
- 蒸馏手册全英文版：[`docs/DISTILLED_PUBLIC_EN.md`](docs/DISTILLED_PUBLIC_EN.md)
- 3 分钟演示录屏脚本：[`docs/DEMO_SCRIPT.md`](docs/DEMO_SCRIPT.md)
- 上游 ARIS 同步与策展流程：[`docs/UPSTREAM_SYNC.md`](docs/UPSTREAM_SYNC.md)
- 克隆卡 / 徽章生成器：[`clone-kit/make_clone_card.py`](clone-kit/make_clone_card.py)（样例：`clone-kit/clone-card.svg`）

如果这个仓库帮你少踩了一个坑，欢迎点个 Star —— 让更多刚开始做科研的人看到它。

---

## English (short)

**Thats-me** is an open-source *cyber clone* for research: **one behavior manual + 87 research skills + one integrity-audit pipeline**, loadable by any model with zero platform dependency.

I am an ML/AI beginner working on remote sensing. I built this because I was tired of re-teaching the same rules in every new chat — and of nearly trusting a fabricated number.

**What changes after loading it:** the assistant audits before it edits. Ask it to write `ΔmIoU = 3.2` and it recomputes from raw results, finds the value is single-seed, reports `1.17 ± 1.84`, and offers options *with costs* instead of silently cherry-picking. Ask it to bypass a safety check and it refuses — publicly.

**Highlights**
1. **Integrity triple audit** — citation, claim, and experiment audits plus a pre-submission forensics sweep; every number traceable, generation separated from verification.
2. **Load-before-task protocol** — three files, any model, auditable and trimmable.
3. **Radical transparency** — the skills blocked by safety scanners are listed (never bypassed), and the "what we do NOT open-source" list is explicit.

**Quick start:** paste the three-file prompt from 方式 A above, or drop `skills/*` into any SKILL.md-compatible tool, or rebuild the clone on a digital-employee platform.

MIT licensed. Skill texts mirrored from [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) (MIT). Contributions and clone show-and-tell are welcome.
