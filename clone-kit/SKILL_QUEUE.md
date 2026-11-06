# SKILL_QUEUE · 技能请求队列（月度 batching）

> 流程定义见 [`../docs/UPSTREAM_SYNC.md`](../docs/UPSTREAM_SYNC.md)；许可门槛见
> [`../docs/TRANSPARENCY_LOG.md`](../docs/TRANSPARENCY_LOG.md) 第 5 节。
> 规则一句话：**有许可声明才镜像；没声明的进队列等许可，不偷偷镜像。**

## 流程（每月第一个周一，或上游大版本时）

1. 从 Discussions 的 `skill-request` 模板收集新请求，登记到下表“社区请求”区；
2. 逐条判定：许可声明？与现有技能重复？维护成本？给出 `accept / defer / reject` 与理由；
3. accept 的按 UPSTREAM_SYNC 策展入 `skills/`，刷新 MANIFEST 与克隆卡；
4. 在 Discussions 发一条 batching 公告（接受了什么、拒绝了什么、为什么）；
5. 本文件留痕：每次 batching 追加一节，不删历史。

## 社区请求（当前：0 条）

| # | 技能/能力 | 请求来源 | 状态 | 理由 |
|---|---|---|---|---|
| — | （暂无） | — | — | 队列于 2026-11-06 建立 |

## 等待许可（listed-only，16 条）

这些技能在作者本地存在、MANIFEST 中以 `mirrored: false` 标记；
上游补出许可声明后，按上面流程评估策展。

| 技能 | 阻塞 | 下一步 |
|---|---|---|
| analytics-data-analysis | 上游未声明许可 | 向上游请求补 LICENSE / frontmatter license 字段 |
| chart-craft-plus | 同上 | 同上 |
| data-analysis-pro | 同上 | 同上 |
| data-extractor | 同上 | 同上 |
| data-scientist | 同上 | 同上 |
| data-visualization | 同上 | 同上 |
| document-processor | 同上 | 同上 |
| excel | 同上 | 同上 |
| excel-data-analysis-and-report-generation | 同上 | 同上 |
| excel-weekly-dashboard | 同上 | 同上 |
| finance-charts | 同上 | 同上 |
| market-research-litiao | 同上 | 同上 |
| prompt-extractor | 同上 | 同上 |
| py-math-viz | 同上 | 同上 |
| report-generation | 同上 | 同上 |
| skill-file-converter | 同上 | 同上 |

不进入队列的两类（永久排除，理由见 TRANSPARENCY_LOG 第 5 节）：
平台内部技能（qoderwake-assistant、wake-dws-cli）、厂商技能（alibabacloud-* 3 个）。

## 第三方 MIT 技能包（待策展）

| 技能包 | 许可 | 状态 | 下一步 |
|---|---|---|---|
| Orchestra AI-Research-SKILLs 1.4.0 剩余 74 个 | MIT（LICENSE 文件；package.json 字段为 ISC，见 TRANSPARENCY_LOG §6） | 已策展 12 个入镜像；其余待需求 | 有 Discussion 需求时按 UPSTREAM_SYNC 策展 |

## Batching 历史

### 2026-11-06 · 策展 Orchestra 子集
- 入镜像 12 个：peft, accelerate, flash-attention, lm-evaluation-harness, weights-and-biases,
  tensorboard, sentence-transformers, clip, segment-anything, transformer-lens,
  ml-paper-writing, brainstorming-research-ideas；
- 其余 74 个继续列名待需求。

### 2026-11-06 · 建队
- 社区请求 0 条；
- 16 条 listed-only 入账“等待许可”；
- 已镜像 89 个（87 ARIS MIT + crawl4ai-skill MIT-0 + excel-formula MIT）。
