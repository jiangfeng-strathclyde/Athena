# START_HERE · A 7-Day Research Sprint for Beginners

> Complete one small, verifiable research cycle yourself—and enjoy the process.
> Spend 30–60 minutes a day using the included synthetic data or your own course
> materials. No GPU, paid account, or programming experience is required.

## Before Day 1

Open a new AI conversation and paste:

```text
Repository: https://github.com/jiangfeng-strathclyde/Thats-me
Read docs/DISTILLED_PUBLIC.md and clone-kit/ROUTING_TABLE.md.
I am a beginner. Give me a plan and its costs before acting. Never invent
results, and independently recompute every important number.
```

If your chat tool cannot access repositories, paste
[`clone-kit/LOADER_LITE.md`](../clone-kit/LOADER_LITE.md) instead.

## Day 1 · Check the arithmetic

- Run `python docs/demo_assets/verify_demo.py` and inspect how it recomputes
  mean ± standard deviation from CSV data.
- Ask the assistant to report an incorrect value such as `Δ=3.2`. It should
  refuse and offer costed correction options.
- **Milestone:** an assistant that values evidence over obedience.

## Day 2 · Audit your reading list

- Provide a course bibliography (`.bib`) or a short handwritten list.
- Ask it to verify each title, DOI, author list, and year.
- Compare the result with `docs/demo_assets/expected_findings.md`.
- **Milestone:** finding one incorrect citation is more useful than generating
  ten unverified summaries.

## Day 3 · Profile a dataset

- Provide a CSV or spreadsheet. Ask the assistant to state the data grain,
  profile the columns, and propose a figure specification.
- Use `data-profile-and-plot` and independently check every number in the chart.
- **Milestone:** a publication-style figure with an audit trail.

## Day 4 · Build a guided reading map

- Ask for eight prioritized readings, with “what to read” and three questions
  for each paper.
- Use `lit-reading-assignment` and verify that every DOI is resolvable.
- Answer one methods, one limitations, and one “what could be wrong?” question
  after each paper.
- **Milestone:** a map, not a random pile of papers.

## Day 5 · Reproduce a small experiment

- Choose a small public dataset or `demo_results.csv`.
- Use `experiment-plan` to specify one baseline, one change, and three random
  seeds in a short script.
- **Milestone:** a result you ran yourself with clearly documented scope.

## Day 6 · Write and audit a one-page report

- Use `paper-plan` and `academic-paper-narrative` to draft the report.
- Request both a numerical audit and a citation audit.
- **Milestone:** every issue found now is one less issue in the submission.

## Day 7 · Publish what you learned

- Summarize the outputs from Days 1–6 on one page.
- Share it with the `clone-show-and-tell` Discussion template.
- If you need a new capability, submit a `skill-request`.
- **Milestone:** work that someone else can see and reproduce.

## Simpler route for younger learners

Skip Day 5 or replace the script with a hand-calculated table that shows every
step. On Days 2 and 4, use textbooks instead of research papers. The principle
does not change: **check the evidence, state the cost, then decide.**

The integrity tools also work independently: `citation-audit`,
`paper-claim-audit`, and `experiment-audit`.
