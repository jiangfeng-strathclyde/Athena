---
license: MIT
name: academic-paper-narrative
description: >-
  Designs defensible paper angles, contribution claims, and section-level story
  arcs for technical publications (IEEE GRSL/TGRS-style geoscience + ML).
  Use when the user asks for paper direction, framing, contribution wording,
  introduction structure, how to position results vs baselines, novelty vs
  incremental work, or "讲故事" for academic writing without overstating.
---

# Academic Paper Narrative (Story + Substance)

## When This Skill Applies

Use for: 选题方向、贡献点措辞、Introduction/Discussion 叙事、主指标与基线对比的合理解释、把「没全胜」写成可信科学结论、审稿人可能攻击点的预排。

**Non-goals**: 不要帮用户隐瞒负面结果、虚构实验、或把未验证的声称写成事实。叙事是**重新框定问题与证据链**，不是掩盖。

---

## Operating Principles

1. **One-sentence thesis**: 全文只允一个核心命题；其余都是支撑或边界条件。
2. **Claim–evidence pairing**: 每个贡献句必须能指到：实验、定理、协议、或可追溯工件。
3. **Primary vs secondary metrics**: 先定「主任务 + 主指标 1–2 个」；其余表格里是补充，不是翻案工具。
4. **Regime honesty**: 若某数据集/信噪比/样本制度下强基线更优，明确写成 *regime* 或 *trade-off*，并解释物理或统计原因。
5. **Novelty ladder** (pick the highest honestly available):
   - **New problem** (约束/目标/评测不同) > **new metric** > **new protocol** > **new inductive bias** > **new architecture** (通常最弱，除非有理论或大幅泛化证据).

---

## Workflow: From Idea to Submittable Angle

Copy and fill this checklist before drafting any section:

```
[ ] Venue tier (e.g., GRSL letter vs TGRS full): 
[ ] Dataset(s) + license/repro: 
[ ] Baselines (tuned? same data split? compute budget?): 
[ ] Primary metric(s) + why they matter for deployment: 
[ ] Where we win / tie / lose (numbers or pending): 
[ ] Biggest reviewer threat (1–3 bullets): 
[ ] Honest novelty (one line): 
```

Then run **three outputs** in order:

### A) One-page pitch (internal)

- **Gap**: 现有工作缺什么（用可检验的缺口感知，不要形容词堆砌）。
- **Question**: 一句话研究问题。
- **Approach**: 方法一句话 + 关键假设（可证伪）。
- **Evidence plan**: 哪些表/图证明哪一句 claim。
- **Limitations**: 主动写 3 条（比审稿人先写）。

### B) Contribution bullets (for abstract / intro end)

- 3–4 条，每条格式：`We [verb] [artifact], enabling [measurable effect], under [assumption].`
- 避免「首次」「全面优于」除非有系统综述级证据。

### C) Threat–response map

对每个威胁写：**承认范围 → 已有证据 → 未来工作**。不要辩称「我们其实赢了」若没有数据。

---

## Section-Level Story Arc (Default)

| Section | Job of the narrative |
|--------|------------------------|
| Abstract | 问题 1 句 + 方法 1 句 + **主结果（主指标）** + 数据/代码一句 |
| Intro | 场景代价（为何重要）→ gap（缺什么）→ question → contributions（编号）→ paper map |
| Related | **轴线组织**（按问题/按范式），为你的 gap 服务，不是文献列表 |
| Method | 定义目标与约束 → 设计选择对应 gap → 复杂度/实现细节放附录 |
| Experiments | 协议先行 → 主表主图 → 消融对准每个 claim → 失败例/局限 |
| Discussion | 解释反直觉行 + 部署含义 + 何时别用本方法 |
| Conclusion | 复述 thesis + **一条** takeaway + 未来工作 |

---

## If Baselines Win Some Cells (Very Common)

Allowed narratives (choose one, honestly):

1. **Pareto**: 同等精度下更低复杂度/更少标注/更可解释/更稳 CV。
2. **Primary-metric win**: 只宣称主指标；其他进补充材料并解释。
3. **Regime specialization**: 我们只在 X（低 SNR、多通道、跨站…）显著更好；Y 下 RF 仍强 → 给选用指南。
4. **Downstream utility**: 分类准确率略差但定位/预警效用更好（需链式实验）。

Forbidden: 用次要指标偷换主结论；删对比方法；夸大统计显著性。

---

## Microseismic / Monitoring-Specific Hooks (Optional)

When the paper touches microseismic, slope, or industrial monitoring, prefer problem hooks that are **deployment-real**:

- cost-asymmetric errors (miss vs false alarm), latency, missing sensors, domain shift, weak labels, human-in-the-loop.
- tie claims to **what operators optimize**, not only accuracy.

---

## Progressive Disclosure

- Short templates and checklists: this file.
- Longer outline templates and example contribution paragraphs: [reference.md](reference.md)

---

## Quick Trigger Phrases

If the user says any of: 「讲故事」「论文角度」「贡献怎么写」「intro 怎么立论」「没超过 baseline 怎么办」「审稿人会怎么怼」「GRSL 怎么投」—read and follow this skill.

**Repo integration:** After literature approval, the workflow runs **Problem Extension** (`PROBLEM_EXTENSION`) then pauses at **`HUMAN_GATE_PROBLEM_EXT`** for human lock-in or revision. Artifacts: `problem_extension_report.md` and `problem_extension_meta.json` under the task workspace. Align narrative with those files when the user works in this repository.
