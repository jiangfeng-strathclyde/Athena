# ROUTING_TABLE · 目标 → 工作流 → 技能

> 用法：**用户只说目标**。先匹配下面的工作流模板，得到一条技能链；链上每一步再按
> “场景 → 技能”表取 `skills/<名>/SKILL.md` 全文。模板不匹配时，按场景表自由组装，
> 并在动手前把“选了哪些技能、为什么、代价是什么”列给用户点单。
> 依赖警告：标注 (ext) 的技能需要外部后端/API key/账号；缺失时静默跳过或明示报错，不得伪造结果。

## 目标 → 工作流模板

| 目标（用户怎么说） | 技能链 | 出口产物 |
|---|---|---|
| 写一篇期刊/会议论文 | research-lit → novelty-check → experiment-plan → paper-plan → paper-write → paper-figure → citation-audit + paper-claim-audit + experiment-audit → auto-review-loop | 可投稿稿 + 审计账本 |
| 核查稿中数字/结论 | paper-claim-audit → 独立脚本重算 → 带代价修改清单 | 数字-结论对照表 |
| 审稿返修 | rebuttal →（需重投时）resubmit-pipeline | 回复信 + 标注稿 |
| 综述 / 精读清单 | arxiv / semantic-scholar / openalex → research-lit → comm-lit-review（通信域） | 分组书单 + 阅读顺序 |
| 找 idea / 查新 | idea-creator → novelty-check → research-refine | 排序后的候选方向 |
| 跑实验 / 调参 | experiment-plan → run-experiment / experiment-queue → monitor-experiment → analyze-results → result-to-claim | 结果板 + 结论裁决 |
| 证明 / 推导 | formula-derivation → proof-writer → proof-checker（可选 lean-formalize） | 命题 + 证明 |
| 做汇报 / 海报 / talk | paper-slides / paper-talk → slides-polish (ext) → paper-poster-html* | 幻灯片 + 讲稿 |
| 专利 / 基金 | invention-structuring → claims-drafting → specification-writing → jurisdiction-format；grant-proposal | 申请书草稿 |

组装规则：
1. **先审计后交付**：任何写作链末端默认挂诚信三件套（citation-audit / paper-claim-audit / experiment-audit）；
2. **代价先行**：链上若含需新实验/新训练的节点，先报机时与页数代价，等点单；
3. **可裁剪**：只要某一环（如只做引用核验）时，单独取该技能即可，红线不裁剪。

## 场景 → 技能（取用表）

| 场景 | 技能 |
|---|---|
| 文献检索与阅读 | arxiv, semantic-scholar, openalex, alphaxiv, deepxiv, research-lit, comm-lit-review（通信域）, gemini-search (ext), exa-search (ext), firecrawl-search (ext), keenable-search, crawl4ai-skill, lit-reading-assignment（精读清单/教学） |
| 引用核验 | citation-audit, citation-crosscheck |
| 选题 / 查新 / 打磨 | idea-creator, novelty-check, research-refine, research-refine-pipeline, idea-discovery, idea-discovery-robot（机器人域）, brainstorming-research-ideas |
| 实验规划与执行 | experiment-plan, experiment-bridge, research-implement-feature, run-experiment, experiment-queue, monitor-experiment, training-check, dse-loop（架构/EDA 域）, peft, accelerate, flash-attention（ML 系统侧） |
| 算力资源 | vast-gpu (ext), serverless-modal (ext), qzcli (ext), system-profile |
| 遥感/对地观测域 | remote-sensing-workbench（数据源/划分/评估口径/基线谱/写作约定）, clip, segment-anything, sentence-transformers（基础模型/检索） |
| 可解释性 | transformer-lens（机理分析，支撑“架构内在含义”链条） |
| 结果分析与裁决 | analyze-results, result-to-claim (ext), ablation-planner, experiment-audit, excel-formula（表格公式）, data-profile-and-plot（剖析与出版级出图）, lm-evaluation-harness, weights-and-biases, tensorboard |
| 论文写作 | paper-plan, paper-write, paper-writing, writing-systems-papers（系统会域）, specification-writing, academic-paper-narrative（叙事与贡献立论）, ml-paper-writing |
| 图表与示意 | paper-figure, figure-spec, mermaid-diagram, paper-illustration (ext), paper-illustration-image2 (ext), pixel-art, data-profile-and-plot |
| 编译与渲染 | paper-compile*, render-html |
| 评审与对抗 | research-review (ext), auto-review-loop (ext), auto-review-loop-llm (ext), auto-review-loop-minimax (ext), kill-argument, auto-paper-improvement-loop (ext) |
| 返修与重投 | rebuttal, resubmit-pipeline |
| 证明与公式 | proof-writer, proof-checker, proof-orchestrator, formula-derivation, lean-formalize |
| 诚信与取证 | integrity-forensics, paper-claim-audit, experiment-audit, citation-audit, research-integrity-pipeline（证据链门禁） |
| 知识库与元优化 | research-wiki, wiki-enrich, meta-optimize, meta-apply, skill-evolution-manager（技能沉淀/合并/丢弃） |
| 汇报与展示 | paper-slides, paper-talk, slides-polish (ext), paper-poster*, paper-poster-html*, paper-illustration |
| 专利与基金 | patent-pipeline, patent-novelty-check, claims-drafting, specification-writing, jurisdiction-format, embodiment-description, figure-description, prior-art-search, grant-proposal, patent-disclosure-drafter（交底书初稿） |
| 通知与杂项 | feishu-notify (ext), interview-cheatsheet, web-debug-search（调试用，不作引用证据） |

`*` = 平台侧未安装（安全扫描拦截，见 `docs/TRANSPARENCY_LOG.md`），镜像全文仅供本地自行审查使用。

## 最小可信集（推荐初学者先装这三个）

`citation-audit` + `paper-claim-audit` + `experiment-audit` —— 任何写作/实验流程即插即用的诚信三件套。
