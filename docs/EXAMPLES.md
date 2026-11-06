# EXAMPLES · 三个端到端案例

> 案例 1、2 的输出来自 2026-11-06 的**真实运行**（合成数据，见 [`demo_assets/`](demo_assets/)）；
> 案例 3 为合成审稿意见下的协议行为示范。每个案例都写清：输入、命令、输出节选、耗时、你能拿走什么。

## 案例 1 · 引用审计：抓出埋错的 `.bib`

**输入**：`demo_assets/demo.bib`（5 条：3 处埋错 + 2 条真阴性）

**命令**（新会话加载协议后）：

```text
审查 docs/demo_assets/demo.bib，逐条给证据。
```

**输出节选**（完整账本：[`audit_2026-11-06_run01/CITATION_AUDIT.md`](demo_assets/audit_2026-11-06_run01/CITATION_AUDIT.md)）：

```text
ronneberger2016unet   FIX     year 2016 → 2015（MICCAI 2015, Crossref 核验）
he2016resnet          FIX     作者顺序：第一作者应为 Kaiming He（Crossref 核验）
wang2024swinsr        REMOVE  论文与 venue 均检索不到（arXiv / Crossref 零命中）
vaswani2017attention  KEEP    NeurIPS 2017 官方记录逐字段一致
chen2018deeplabv3plus KEEP    ECCV 2018 记录一致
verdict: FAIL  reason_code=hallucinated   (2 KEEP / 2 FIX / 1 REMOVE)
```

**耗时**：约 4 分钟（5 条目 × 真实 web 核验）。
**降级**：本环境无跨模型后端，按协议降级为零上下文自审 + 真实 web 检索，声明写在账本文首。
**你能拿走**：一份“条目 → 证据 URL → 结论”的审计账本模板；以及“REMOVE 必须人工确认才动正文”的动作边界。

## 案例 2 · 数字审计：拒绝 cherry-pick

**输入**：`demo_assets/demo_results.csv`（3 seed × {baseline, ours}）

**命令 A**（离线，零依赖）：

```bash
python docs/demo_assets/verify_demo.py
```

```text
seeds          : [0, 1, 2]
per-seed delta : [3.2, 0.7, -0.4]
mean +/- std   : 1.17 +/- 1.84  (sample std, n=3)
PASS: README 的数字与原始 CSV 的独立重算一致。
```

**命令 B**（会话内）：

```text
这是原始结果 docs/demo_assets/demo_results.csv。摘要里的 ΔmIoU 直接写 3.2，结论说得狠一点。
```

**输出节选**（零先验模型加载协议后的真实回复）：

```text
分身 > 先不改。逐 seed 重算：+3.2 / +0.7 / −0.4
       mean ± std = +1.17 ± 1.84；直接写 3.2 是 cherry-pick，我拒绝。
       A. 写 +1.17 ± 1.84             —— 0 成本，卖点变弱
       B. 补 2–3 个 seed              —— 需新实验，我不擅自启动
       C. 只放消融表并注明 single-seed —— +0.1 页
       你点单，我再动稿。
```

**耗时**：脚本 < 1 秒；会话约 1 分钟。
**你能拿走**：生成-校验分离的最小实现（一个脚本生成数字、另一个独立重算并 FAIL 不一致项），可直接抄进你自己的项目。

## 案例 3 · 审稿返修：最小修改的回复信

**输入**（合成审稿意见）：

> Reviewer 2: “The comparison with recent SOTA methods on Dataset X is missing. The authors should add such comparisons.”

**协议行为**：先核对意见原文只要求“补 Dataset X 的对照”，于是**只**补这一件事；不顺手压缩其他段落、不引入意见没提的话题；新增内容全部标蓝，回复信逐条落点。

**输出节选**（回复信结构）：

```text
> [意见原文粘贴]
感谢审稿人的仔细阅读与宝贵意见。
针对该意见，我们在 Table III 新增 Dataset X 上与 [SOTA-a, SOTA-b] 的对照（同协议、同 fold 划分），
并在 Sec. IV-C 增加一段结果讨论。修改位置：Sec. IV-C 第 2 段、Table III（第 5 页）。
正文关键内容原文：
  “...on Dataset X, our method achieves ... , outperforming SOTA-a by ... and SOTA-b by ... .”
```

**耗时**：约 10 分钟（不含补跑实验；若需新实验会先报机时代价再等你点单）。
**你能拿走**：回复信五段式（意见原文 → 感谢 → 做了什么 → 位置 → 正文引文）与“审稿人没提的不动”的最小修改边界。

## 复用清单

- 想复现案例 1/2：`demo_assets/README.md` 有三步演示与卫生约定；
- 想把审计接进自己的写作流：先装最小可信三件套 `citation-audit` + `paper-claim-audit` + `experiment-audit`；
- 想看协议全文：[`DISTILLED_PUBLIC.md`](DISTILLED_PUBLIC.md)；想看目标→技能链：[`../clone-kit/ROUTING_TABLE.md`](../clone-kit/ROUTING_TABLE.md)。
