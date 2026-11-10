# Athena screening and claim-evidence workflow

Use this standalone mode for a supplied paper collection, a reading route, or
claim-level evidence synthesis. It can be completed manually in the conversation
without ARIS helpers, MCP services, scripts, a wiki, or parallel agents. It does
not require executing the upstream `research-lit` search or save steps.

## Contents

- [Bound the task and inventory the sources](#1-bound-the-task-and-inventory-the-sources)
- [Keep a screening ledger](#2-keep-a-screening-ledger)
- [Build evidence rows](#3-build-evidence-rows-per-claim-not-per-papers-reputation)
- [Reconcile support, opposition, and uncertainty](#4-reconcile-support-opposition-and-uncertainty)
- [Deliver within scope](#5-deliver-within-scope)

## 1. Bound the task and inventory the sources

State the research question or exact claim, intended population/system, relevant
intervention or method, comparator, outcome, and time/context constraints when
they matter. For screening, state inclusion/exclusion criteria before applying
them. Use the user's supplied corpus and requested retrieval scope. Ask only for
missing choices that materially change the result; otherwise label assumptions.

Assign a stable paper ID to every input. Record the title and supplied identifier
or URL, the particular version, and how it entered the corpus. Deduplicate by
confirmed identifiers or inspected bibliographic evidence; map duplicates to the
retained ID rather than dropping them silently. Keep ambiguous matches separate.
A preprint and its published version may differ; record which text supports a
finding instead of treating them as interchangeable independent studies.

Separate two facts for each source:

- **Identity status:** verified against a named source actually checked,
  user-supplied but not independently verified, unresolved, or conflicting.
  A plausible DOI or a working link alone does not verify all bibliographic data.
- **Material inspected:** full text (identify sections actually inspected),
  abstract only, specific excerpt/pages, secondary account, or metadata only.
  Access to a PDF does not imply the whole paper was read. User notes and search
  snippets are not primary-study full text; label their origin and limitations.

Do not use titles, citation counts, model memory, or an inaccessible URL to infer
methods, numerical results, or a paper's stance. With metadata only, record
`pending content` and the missing evidence. Without usable content across the
corpus, deliver the inventory and gaps only, not a fabricated synthesis.

## 2. Keep a screening ledger

Account for every supplied or retrieved candidate, including duplicates,
exclusions, inaccessible items, and unfinished readings. One row per input:

| Input ID / retained paper ID | Source and version | Identity status | Material inspected / locator | Decision | Criterion-based reason | Group / reading priority | Missing material |
| --- | --- | --- | --- | --- | --- | --- | --- |

Use decisions such as `include`, `exclude`, `pending content`, `duplicate of ID`,
or `not yet assessed`. Missing text is not evidence of irrelevance. Explain an
exclusion with the stated criterion and available source evidence. A tentative
title/abstract screening decision must remain tentative at that screening level.

Reconcile the input IDs with the ledger and report counts by decision. State any
processing cap and list unassessed IDs; never imply complete coverage if papers
were omitted. For a reading route, group by actual research problem or approach,
give a short reason for each reading priority, and explain dependencies between
foundational, methods, evaluation, and disagreement papers as the corpus allows.
Do not manufacture groups or a definitive reading order from missing content.

## 3. Build evidence rows per claim, not per paper's reputation

Split compound claims when their components have different evidence. Give each
claim an ID and preserve its exact wording and scope. Record one row for each
claim–source finding; the same paper may support one claim and oppose another.

| Claim ID / exact claim | Paper ID / version | Relation | Finding and reasoning | Source locator / inspected material | Applicable conditions | Limitations / independence |
| --- | --- | --- | --- | --- | --- | --- |

Each row must include:

- **Relation:** `supports`, `opposes`, or `uncertain / insufficient`. Describe
  precisely what is supported or opposed. Absence of a significant effect is not
  automatically evidence of no effect; lack of discussion is not opposition.
- **Finding:** a faithful paraphrase or short permitted quotation from the
  inspected source, plus an explicitly labeled inference if needed. Copy numbers
  only when present in that material, including units, comparator, uncertainty,
  and relevant settings. Never invent a missing effect size or confidence interval.
- **Locator:** DOI, stable URL, or supplied local path plus a page, section,
  table, figure, or identifiable passage. For abstract-only evidence, say
  `abstract` and identify the relevant passage; do not fabricate page numbers.
  If the text has no page or section markers, use a short identifiable excerpt
  and its source. For text pasted into the conversation without a URL/path,
  assign a supplied-excerpt ID and identify the passage; mark any unresolved
  bibliographic identity and do not imply external verification. A bibliography
  entry alone is not an evidence locator.
- **Conditions:** population or dataset, method/intervention, comparator,
  outcome, evaluation setup, and other boundaries needed to interpret the
  finding. Mark fields not reported in the available material as unknown.
- **Limitations and independence:** study design, bias or measurement concerns
  visible in the material, indirectness to the claim, and shared datasets,
  cohorts, experiments, or versions. A review repeating a primary result is not
  independent replication; do not double-count it as a separate experiment.

With abstracts or excerpts, conclusions are provisional and bounded to what
those materials report. A verified paper identity is not verification that its
findings are correct or that they support the user's claim. A citation-graph edge
likewise shows a citation relationship, not support or opposition.

## 4. Reconcile support, opposition, and uncertainty

Compare the findings under comparable conditions before describing a conflict.
Different populations, metrics, baselines, or versions may explain a difference;
state this as an explanation to check, not a resolved fact without evidence.
Distinguish direct contradiction from narrower applicability or indirect evidence.

Assess the quality, relevance, precision, and independence of the available
evidence. Do not count papers as votes, use citation counts or journal prestige
as truth scores, or average incompatible results. Do not force equal quantities
of supporting and opposing evidence. Report `not found in the inspected corpus`
when a side is absent, never `no contrary evidence exists`.

For each claim, give a scoped conclusion with links to the relevant evidence
rows, unresolved disagreements, and the missing checks that could change it.
Use cautious wording proportional to the evidence; no universal numerical
confidence score is required. If retrieval was requested, record the sources,
queries, date, bounds, and failures actually encountered. If it was not requested
or tools are unavailable, identify the coverage limit without claiming a search.

## 5. Deliver within scope

Return the task/corpus boundary, screening ledger and coverage receipt, the
requested reading route or evidence matrix, and the unresolved gaps. Claim-level
analysis needs the matrix; a reading-list-only request does not require inventing
claims merely to fill one. Tables may be split for readability while preserving
the IDs and source links. Save files only within the user's requested scope.

Keep these outcomes separate:

- Bibliographic identity: does the referenced work/version exist and match?
- External claim support: does inspected literature support this exact claim
  under the stated conditions? This workflow addresses that question.
- Internal numerical audit: do the user's manuscript numbers match their raw
  experiment artifacts? Route that distinct requested task to `paper-claim-audit`.

Before delivery, check that every input is accounted for, every substantive
finding has a real locator, abstract-only evidence is marked, unresolved evidence
has not become certainty, and no unrequested search or wiki write was performed.
