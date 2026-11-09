# EXAMPLES · Three End-to-End Cases

Cases 1 and 2 are reproducible runs on fully synthetic data in [`demo_assets/`](demo_assets/). Case 3 demonstrates the collaboration contract.

## Case 1 · Citation audit catches planted errors

**Input:** `demo_assets/demo.bib`, containing three deliberate errors and two negative controls.

```text
Review docs/demo_assets/demo.bib and provide evidence for every entry.
```

Expected excerpt:

```text
ronneberger2016unet   FIX     year 2016 -> 2015
he2016resnet          FIX     Kaiming He should be the first author
wang2024swinsr        REMOVE  article and venue cannot be verified
vaswani2017attention  KEEP    verified against the official record
chen2018deeplabv3plus KEEP    verified against the official record
verdict: FAIL (2 KEEP / 2 FIX / 1 REMOVE)
```

The full record is in [`CITATION_AUDIT.md`](demo_assets/audit_2026-11-06_run01/CITATION_AUDIT.md). It demonstrates the reusable `entry → evidence → conclusion` structure and requires manual confirmation before removing a citation.

## Case 2 · Numerical audit rejects cherry-picking

**Input:** `demo_assets/demo_results.csv`, with three seeds for a baseline and proposed method.

```bash
python docs/demo_assets/verify_demo.py
```

```text
seeds          : [0, 1, 2]
per-seed delta : [3.2, 0.7, -0.4]
mean +/- std   : 1.17 +/- 1.84  (sample std, n=3)
PASS: README statistics match the independent CSV recomputation.
```

If asked to report only `+3.2`, the clone should refuse because that value comes from a single seed. It should offer three choices: report `+1.17 ± 1.84`, run more seeds at additional cost, or show the per-seed table with a limitation note.

## Case 3 · Reviewer response with minimal scope

**Input:** “The comparison with recent SOTA methods on Dataset X is missing. The authors should add such comparisons.”

The clone should add only the requested Dataset X comparison, identify the exact manuscript locations, and avoid unrelated rewriting. A useful response structure is:

```text
> [Original reviewer comment]
Thank you for this suggestion.
We added comparisons with [SOTA-A, SOTA-B] on Dataset X.
The changes appear in Table III and Section IV-C.
The revised text is: "..."
```

If new experiments are required, it should state the cost and wait for approval before starting them.

## Reuse checklist

- Reproduce Cases 1 and 2 with [`demo_assets/README.md`](demo_assets/README.md).
- Start with `citation-audit`, `paper-claim-audit`, and `experiment-audit` as the minimum integrity set.
- Read [`DISTILLED_PUBLIC.md`](DISTILLED_PUBLIC.md) for the full agreement and [`ROUTING_TABLE.md`](../clone-kit/ROUTING_TABLE.md) for task-to-skill routing.
