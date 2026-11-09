# START_HERE · 快速上手科研的 7 天路线

> 目标不是“帮你出论文”，是让你**亲手做完一个小而完整的科研闭环**，并在这个过程中
> 感受到做科研的快乐。每天 30–60 分钟；全部用本仓库的合成数据或你自己的课程材料，
> 不需要 GPU、不需要账号、不需要会编程（会复制粘贴即可）。
> 中学生版在路线末尾有降级说明。

## 出发前（5 分钟）

新开一个 AI 会话，粘贴：

```text
仓库：https://github.com/jiangfeng-strathclyde/Thats-me
读 docs/DISTILLED_PUBLIC.md 和 clone-kit/ROUTING_TABLE.md。
（读不到仓库时用直链：https://raw.githubusercontent.com/jiangfeng-strathclyde/Thats-me/main/docs/DISTILLED_PUBLIC.md ）
我是初学者：先给方案和代价，等我点单再执行；不虚构结果；数字要能重算。
```

## Day 1 · 让它先学会“查账”

- 跑 `python docs/demo_assets/verify_demo.py`，看它怎么从原始 CSV 重算 mean ± std；
- 然后对它说：“摘要写 Δ=3.2，说狠一点。”看它拒绝并给你三个带代价的选项。
- **快乐点**：你第一次拥有一个不会顺着你说瞎话的助手。

## Day 2 · 审你自己的课程论文参考文献

- 把你课程报告/毕设开题的 `.bib`（或手抄 5 条参考文献）发给它：“逐条核 DOI/作者/年份，给证据。”
- 对照 `docs/demo_assets/expected_findings.md` 看它该给出什么结构。
- **快乐点**：抓出一条错年份或错作者，比读十篇综述都有成就感。

## Day 3 · 把一份数据看懂并画成图

- 用任意一份课程数据（CSV/Excel）说：“先声明行粒度，再 profile，再给我图规格。”
- 走 `data-profile-and-plot` 的五步；图出来后用它的校验脚本复核图注数字。
- **快乐点**：你的第一张“能进论文”的图。

## Day 4 · 给同门/自己列一份精读清单

- 说：“给<你的方向>列 8 篇精读，标优先级，每篇写读什么和 3 个问题。”
- 走 `lit-reading-assignment`；核对每条 DOI 是否真能打开。
- **快乐点**：你开始有自己的“地图”，而不是随机刷论文。

## Day 5 · 复现一个最小实验

- 选一个公开小数据集（或 `demo_results.csv` 扩充版），让它按 `experiment-plan`
  写一个 30 行内的脚本：一个基线 + 一个改动 + 3 个 seed。
- **快乐点**：跑出来的数字是你自己的，且口径写得清清楚楚。

## Day 6 · 写一页报告并接受审计

- 用 `paper-plan` + `academic-paper-narrative` 写一页报告；
- 然后主动说：“对这份报告跑数字审计和引用审计。”看它挑毛病。
- **快乐点**：被审计挑出的每个毛病，都是你下次不会踩的坑。

## Day 7 · 晒出来

- 把 Day 1–6 的产物整理成一页，用 Discussions 的 `clone-show-and-tell` 模板发出来；
- 想要某个新技能？用 `skill-request` 提，我们按月策展。
- **快乐点**：你的工作被别人看到、被别人复用。

## 更年轻的读者（中学版降级）

- 跳过 Day 5 的脚本，改为“让它用表格算并展示每一步”；
- Day 2/4 改用科普文章而非论文；其余不变。
- 原则不变：**先查账、再结论、列代价、等你点单**。

## 常用三件套（任何时候都可单独用）

`citation-audit`（引用）· `paper-claim-audit`（数字）· `experiment-audit`（实验诚实度）
