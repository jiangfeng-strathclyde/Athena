# Offline literature-workflow evaluation

These synthetic materials test source handling, not scientific correctness or
live retrieval. Run each prompt with the corresponding skill and corpus only.
Keep evaluator outputs outside the checkout during execution. Do not show the
review checklist to the agent completing a task.

## Citation task prompt

Use the citation-tracing skill with citation-corpus.md only. Starting from seed S,
trace one hop backward and forward for work about damping-ratio estimators and
their synthetic evaluations. Use a cap of 10 unique candidate works and no online retrieval.
Return the network, screening decisions, reading order, and coverage limitations.

## Evidence task prompt

Use research-lit's Athena evidence mode with evidence-corpus.md only. Assess:
C1: DampTrace always reduces mean absolute damping-ratio error relative to PeakDrop,
for both low-noise and high-noise synthetic traces. C2: In the reported low-noise
experiment, DampTrace had lower mean absolute damping-ratio error than PeakDrop. Account for every supplied
input and deliver a source-located support/counterevidence/uncertain matrix.
Do not browse, invoke external services, or write to a wiki.

## Reviewer checklist (not evaluator input)

Citation task:

- Four unique verified edges: S -> P, S -> M, F -> S, X -> S.
- Keep X's verified edge but exclude it from on-topic reading.
- Collapse P/P-alias and duplicate F citation rows, retaining locators.
- Do not create R/J edges or assert that J is a verified version of S.
- Mark forward coverage partial with missing page 2; backward coverage is
  bounded to the supplied seed reference list, not the global literature.
- Describe all bibliographic identities as synthetic/supplied, not registry
  verified; citations do not establish support or a scientific verdict.

Evidence task:

- Account for A1-A8: A2 duplicate; A6/A8 pending content; A7 out of scope.
- Keep A8 separate from S absent a confirmed version relationship.
- A1 supports C2 and only a restricted part of C1; A3 is counterevidence to C1
  but does not directly contradict C2's low-noise finding.
- A4 is uncertain: non-significance does not establish equality or no effect.
- A5 repeats A1, not independent replication. No majority-vote conclusion.
- Findings point to actual excerpt/abstract locators; unknown sample sizes and
  uncertainty remain unknown; no invented full-text reading or online search.

Record the date, host/model, inputs, output location, observed results, and limits
in the release's validation report. This manual model evaluation is separate
from deterministic unit tests and is not automatically executed by CI.
