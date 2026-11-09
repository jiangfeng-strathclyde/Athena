# I Open-Sourced My AI Research Assistant

I am a beginner in machine learning, artificial intelligence, remote sensing, and Earth observation. Like many researchers, I use AI to read papers, plan experiments, and revise manuscripts. I also discovered a recurring problem: a correction made last week disappeared in a new session, an agreed statistical convention was forgotten, and a plausible-looking number nearly reached a summary before it was independently checked.

The problem was not simply model intelligence. The working agreement between the model and me did not persist.

So I turned the agreement into a loadable package: red lines, collaboration methods, task routes, and reusable skills. I call the result a research clone. It is not a prompt collection or chatbot personality. It is a portable behavior system.

## What it contains

- **Red lines:** no fabricated results, explicit verification status, and no silent changes to statistical conventions.
- **Routing:** describe the goal and load the relevant workflow instead of memorizing skill names.
- **Skills:** 108 `SKILL.md` workflows across literature, experiments, writing, figures, audits, reviews, patents, and grants.
- **Verification:** separate generation from checking; independent scripts fail loudly when results disagree.

## Three reproducible demonstrations

First, the clone rejects cherry-picking. Given synthetic per-seed improvements of `+3.2`, `+0.7`, and `−0.4`, it refuses to headline the best seed and instead reports `+1.17 ± 1.84`. Anyone can rerun the calculation with `python docs/demo_assets/verify_demo.py`.

Second, a citation audit finds three planted bibliography errors—a wrong year, incorrect author order, and fabricated venue—without falsely accusing two valid negative controls.

Third, the clone refuses requests to bypass a security check. When a platform scanner blocked three skills, the project documented the event and safe alternatives instead of disguising the text to evade the scanner.

## The main lesson

**The credibility of a scientific assistant matters more than apparent intelligence.** An assistant that can refuse, verify, disclose uncertainty, and publish its own failure records is more useful than one that agrees to everything.

## Boundaries

The public repository does not contain private memory, credentials, unpublished data, or identifying information. Skills are mirrored only when redistribution permission is clear, with upstream attribution preserved.

- Repository: <https://github.com/jiangfeng-strathclyde/Thats-me>
- Landing page: <https://jiangfeng-strathclyde.github.io/Thats-me/>

Beginners helping beginners—feedback is welcome.
