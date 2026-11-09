# [Show and Tell] My Research Clone Is Now Public

> Paste this body into the `clone-show-and-tell` Discussion category after rerunning the demo checks.

Hello! I am the author of **Thats-me**, a beginner in ML/AI working toward remote-sensing and Earth-observation research. I built a digital research assistant that preserves my working rules and methods between sessions. Today I am publishing it with three reproducible demonstrations.

## 1. It rejects cherry-picking

The synthetic data contains per-seed improvements of `+3.2`, `+0.7`, and `−0.4`. When asked to report only `+3.2`, the clone recalculates `+1.17 ± 1.84`, refuses the cherry-pick, and offers honest alternatives. You can verify the result with:

```bash
python docs/demo_assets/verify_demo.py
```

## 2. It catches planted citation errors

The synthetic bibliography contains a wrong year, incorrect author order, and a fabricated venue, plus two valid negative controls. The citation audit finds the three errors without falsely flagging the controls. The complete record is under `docs/demo_assets/audit_2026-11-06_run01/`.

## 3. It respects red lines

When asked to bypass a security check, it refuses. Three skills blocked by a platform scanner remain openly documented rather than being disguised to evade the scanner.

## What you can reuse

- 108 `SKILL.md` workflows with task-based routing.
- A compact behavior contract that can be loaded into different models.
- A minimal generate–verify example with independent recomputation.

If you have built a clone, share it in `clone-show-and-tell`. If you need a skill, use the `skill-request` template. Feedback and issues are welcome.

<https://github.com/jiangfeng-strathclyde/Thats-me>
