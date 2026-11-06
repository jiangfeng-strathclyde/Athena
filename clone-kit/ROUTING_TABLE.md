# ROUTING_TABLE · 场景 → 技能路由

> 分身不靠记技能名字工作，靠**场景路由**。任务来了先定位场景，再读对应 `skills/<名>/SKILL.md`。
> 依赖警告：标注 (ext) 的技能需要外部后端/API key/账号；缺失时静默跳过或明示报错，不得伪造结果。

| 场景 | 技能 |
|---|---|
| 文献检索与阅读 | arxiv, semantic-scholar, openalex, alphaxiv, deepxiv, research-lit, comm-lit-review（通信域）, gemini-search (ext), exa-search (ext), firecrawl-search (ext), keenable-search |
| 引用核验 | citation-audit, citation-crosscheck |
| 选题 / 查新 / 打磨 | idea-creator, novelty-check, research-refine, research-refine-pipeline, idea-discovery, idea-discovery-robot（机器人域） |
| 实验规划与执行 | experiment-plan, experiment-bridge, research-implement-feature, run-experiment, experiment-queue, monitor-experiment, training-check, dse-loop（架构/EDA 域） |
| 算力资源 | vast-gpu (ext), serverless-modal (ext), qzcli (ext), system-profile |
| 结果分析与裁决 | analyze-results, result-to-claim (ext), ablation-planner, experiment-audit |
| 论文写作 | paper-plan, paper-write, paper-writing, writing-systems-papers（系统会域）, specification-writing |
| 图表与示意 | paper-figure, figure-spec, mermaid-diagram, paper-illustration (ext), paper-illustration-image2 (ext), pixel-art |
| 编译与渲染 | paper-compile*, render-html |
| 评审与对抗 | research-review (ext), auto-review-loop (ext), auto-review-loop-llm (ext), auto-review-loop-minimax (ext), kill-argument, auto-paper-improvement-loop (ext) |
| 返修与重投 | rebuttal, resubmit-pipeline |
| 证明与公式 | proof-writer, proof-checker, proof-orchestrator, formula-derivation, lean-formalize |
| 诚信与取证 | integrity-forensics, paper-claim-audit, experiment-audit, citation-audit |
| 知识库与元优化 | research-wiki, wiki-enrich, meta-optimize, meta-apply |
| 汇报与展示 | paper-slides, paper-talk, slides-polish (ext), paper-poster*, paper-poster-html*, paper-illustration |
| 专利与基金 | patent-pipeline, patent-novelty-check, claims-drafting, specification-writing, jurisdiction-format, embodiment-description, figure-description, prior-art-search, grant-proposal |
| 通知与杂项 | feishu-notify (ext), interview-cheatsheet, web-debug-search（调试用，不作引用证据） |

`*` = 平台侧未安装（安全扫描拦截，见 `docs/TRANSPARENCY_LOG.md`），镜像全文仅供本地自行审查使用。

## 最小可信集（推荐初学者先装这三个）

`citation-audit` + `paper-claim-audit` + `experiment-audit` —— 任何写作/实验流程即插即用的诚信三件套。
