---
license: MIT
name: academic-paper-narrative
description: >-
  Designs defensible paper angles, contribution claims, and section-level story
  arcs for technical publications (IEEE GRSL/TGRS-style geoscience + ML).
  Use when the user asks for paper direction, framing, contribution wording,
  introduction structure, how to position results vs baselines, novelty vs
  incremental work, or "Tell a story." for academic writing without overstating.
---

# Academic Paper Narrative (Story + Substance)

## When This Skill Applies

Use for: Theme orientation, contribution point language,Introduction/Discussion The narrative, a reasonable explanation of the comparison between the main indicator and the baseline, the writing of “not all” as a credible scientific conclusion, and the pre-allocation of potential attack points by the reviewers.

**Non-goals**: Do not help users hide negative results, fictional experiments, or write unverified claims into fact.**Reframe the problem and the evidence chain**，Not cover up.

---

## Operating Principles

1. **One-sentence thesis**: The whole text gives only one core proposition; the rest are supportive or border conditions.
2. **Claim–evidence pairing**: Each contribution line must be capable of referring to experiments, theories, agreements, or retrospective works.
3. **Primary vs secondary metrics**: Let's start with "Major Mission." + Main indicators 1–2 ; the rest of the tables are supplementary and not a means of rebuttal.
4. **Regime honesty**: If a data set/Letter Noise/A better baseline under the sample system, clearly stated. *regime* or *trade-off*，And explain the physical or statistical reasons.
5. **Novelty ladder** (pick the highest honestly available):
   - **New problem** (Constraint/Objective/Assessments are different.) > **new metric** > **new protocol** > **new inductive bias** > **new architecture** (It's usually the weakest, unless there's a theory or a substantial generalization of evidence.).

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

- **Gap**: What is missing from the existing work (using a detectable perception of gaps, not adjectives).
- **Question**: Let's look at the problem in one sentence.
- **Approach**: The way it's done. + Key assumptions (probability).
- **Evidence plan**: Which tables?/Which one does it prove? claim。
- **Limitations**: Active 3 Article (in advance of the speaker).

### B) Contribution bullets (for abstract / intro end)

- 3–4 Article, each format:`We [verb] [artifact], enabling [measurable effect], under [assumption].`
- To avoid the "first" "better than the first" unless there is a systematic synthesis of evidence.

### C) Threat–response map

For each threat:**Scope of recognition → There's evidence. → Future work**。Don't argue that "we actually won" if there's no data.

---

## Section-Level Story Arc (Default)

| Section | Job of the narrative |
|--------|------------------------|
| Abstract | Problem 1 Word + Methodology 1 Word + **Main outcome (main indicator)** + Data/Code line. |
| Intro | The costs of the scene (why is it important)→ gap（What's missing?→ question → contributions（(number)→ paper map |
| Related | **Axis Organization**（By Question/For you. gap Service, not list |
| Method | Definition of objectives and constraints → Design Selection Match gap → Complexity/Implement details with attachments |
| Experiments | Deal first. → master chart → Take it easy on each one. claim → Cases of failure/Limits |
| Discussion | Explain the intuition line. + Meaning of deployment + Don't do it this way. |
| Conclusion | Restatement thesis + **One.** takeaway + Future work |

---

## If Baselines Win Some Cells (Very Common)

Allowed narratives (choose one, honestly):

1. **Pareto**: Less complex with equal accuracy/Less Label/It's easier to explain./It's more stable. CV。
2. **Primary-metric win**: Only the main indicators are declared; others are supplemented and explained.
3. **Regime specialization**: We're just... X（Low SNR、Multi-channels, cross-stations.…）Visible better;Y Down RF Still strong. → A guide to selection.
4. **Downstream utility**: Classification Accuracy but Positioning/Early warning is more effective (chain-based experiments are required).

Forbidden: Sub-indicators are exchanged for main findings; methods of comparison are deleted; statistical visibility is exaggerated.

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

If the user says any of: 「"The Angle of the Thesis." "How to write the contributions."intro What's the point? "No more than that." baseline What do we do?GRSL "How?"—read and follow this skill.

**Repo integration:** After literature approval, the workflow runs **Problem Extension** (`PROBLEM_EXTENSION`) then pauses at **`HUMAN_GATE_PROBLEM_EXT`** for human lock-in or revision. Artifacts: `problem_extension_report.md` and `problem_extension_meta.json` under the task workspace. Align narrative with those files when the user works in this repository.
