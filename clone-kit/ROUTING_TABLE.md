# Routing Table · Goal → Workflow → Skills

Users should be able to state a goal without knowing skill names. Match the goal
to a workflow below, then read the full `skills/<name>/SKILL.md` for every skill
you select. Before acting, explain which skills were selected, why, and at what
cost. Skills marked `(ext)` need an external service, account, or API key; skip
or report them when unavailable, and never fabricate a result.

## Workflow templates

| User goal | Suggested skill chain | Main output |
|---|---|---|
| Write a paper | research-lit → novelty-check → experiment-plan → paper-plan → paper-write → paper-figure → citation-audit + paper-claim-audit + experiment-audit | Submission draft and audit trail |
| Verify claims or numbers | paper-claim-audit → independent recomputation → costed correction list | Claim-to-evidence table |
| Respond to reviewers | rebuttal → resubmit-pipeline | Response letter and change log |
| Build a survey or reading list | arxiv / semantic-scholar / openalex → research-lit → comm-lit-review | Structured bibliography and reading order |
| Generate and refine ideas | idea-creator → novelty-check → research-refine | Ranked research directions |
| Run experiments | experiment-plan → run-experiment / experiment-queue → monitor-experiment → analyze-results → result-to-claim | Results dashboard and supported claims |
| Develop a proof | formula-derivation → proof-writer → proof-checker → optional lean-formalize | Assumptions, derivation, and verification |
| Prepare a talk or poster | paper-slides / paper-talk → slides-polish (ext) → paper-poster-html | Slides, notes, or poster |
| Prepare a patent or grant | invention-structuring → claims-drafting → specification-writing → jurisdiction-format; grant-proposal | Application draft |

## Assembly rules

1. **Audit before delivery.** Add `citation-audit`, `paper-claim-audit`, and
   `experiment-audit` to any workflow that produces scholarly claims.
2. **State costs first.** Estimate time, compute, data, pages, and external fees
   before adding experiments or training runs.
3. **Load only what is needed.** A single audit skill may be used independently,
   but it still inherits the project's integrity rules.
4. **Use approval levels.** L0 is read-only analysis; L1 edits local files; L2
   starts experiments, training, or paid API work; L3 performs irreversible or
   external actions such as publishing, pushing, or sending messages. Use the
   highest level required by any step and obtain approval where needed.

## Skills by scenario

| Scenario | Skills |
|---|---|
| Literature discovery | arxiv, semantic-scholar, openalex, alphaxiv, deepxiv, research-lit, comm-lit-review, gemini-search (ext), exa-search (ext), firecrawl-search (ext), keenable-search, crawl4ai-skill, lit-reading-assignment |
| Citation verification | citation-audit, citation-crosscheck |
| Research ideas and refinement | idea-creator, novelty-check, research-refine, research-refine-pipeline, idea-discovery, idea-discovery-robot, brainstorming-research-ideas |
| Experiment planning and execution | experiment-plan, experiment-bridge, research-implement-feature, run-experiment, experiment-queue, monitor-experiment, training-check, dse-loop, peft-fine-tuning, huggingface-accelerate, optimizing-attention-flash |
| Compute resources | vast-gpu (ext), serverless-modal (ext), qzcli (ext), system-profile |
| Remote sensing and field observation | remote-sensing-workbench, clip, segment-anything-model, sentence-transformers |
| Interpretability | transformer-lens-interpretability |
| Analysis and claim support | analyze-results, result-to-claim (ext), ablation-planner, experiment-audit, excel-formula, data-profile-and-plot, evaluating-llms-harness, weights-and-biases, tensorboard |
| Academic writing | paper-plan, paper-write, paper-writing, writing-systems-papers, specification-writing, academic-paper-narrative, ml-paper-writing |
| Figures and diagrams | paper-figure, figure-spec, mermaid-diagram, paper-illustration (ext), paper-illustration-image2 (ext), pixel-art, data-profile-and-plot |
| Compilation and rendering | paper-compile, render-html |
| Review and adversarial critique | research-review (ext), auto-review-loop (ext), auto-review-loop-llm (ext), auto-review-loop-minimax (ext), kill-argument, auto-paper-improvement-loop (ext) |
| Revision and resubmission | rebuttal, resubmit-pipeline |
| Proofs and formulas | proof-writer, proof-checker, proof-orchestrator, formula-derivation, lean-formalize |
| Integrity and evidence | integrity-forensics, paper-claim-audit, experiment-audit, citation-audit, research-integrity-pipeline |
| Knowledge and skill maintenance | research-wiki, wiki-enrich, meta-optimize, meta-apply, skill-evolution-manager |
| Presentations | paper-slides, paper-talk, slides-polish (ext), paper-poster, paper-poster-html, paper-illustration |
| Patents and grants | patent-pipeline, patent-novelty-check, claims-drafting, specification-writing, jurisdiction-format, embodiment-description, figure-description, prior-art-search, grant-proposal, patent-disclosure-drafter |
| Notifications and utilities | feishu-notify (ext), interview-cheatsheet, web-debug-search |

## Minimal trustworthy starter set

Start with `citation-audit` + `paper-claim-audit` + `experiment-audit`. Together
they provide a compact integrity layer for most writing and experiment tasks.
