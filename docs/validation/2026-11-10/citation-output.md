# One-hop citation network from seed S

This is an offline exercise using invented fixture records, not a scientific literature review. All research evidence comes from [citation-corpus.md](../../demo_assets/literature_workflows/citation-corpus.md). Its DOI-shaped strings are synthetic identifiers; none was looked up or externally validated.

## Scope and coverage

- **Question:** Which works cited by S or citing S concern damping-ratio estimators and their synthetic evaluations?
- **Seed:** S, *DampTrace: damping-ratio estimation from low-noise oscillator traces*, Mira Example and Rowan Fixture, 2024, preprint v1, synthetic ID `10.0000/fixture.s`.
- **Inclusion:** Works addressing damping-ratio estimation methods or their evaluations. Potentially relevant but insufficiently evidenced records remain pending. A verified citation alone does not establish topical relevance.
- **Limits:** One hop backward and forward from S; at most 10 unique candidate works; supplied corpus only; no online retrieval. Related recommendations are recorded separately from verified adjacency.
- **Dates:** Inspected on 2026-11-10 (Asia/Shanghai); corpus and `CitingExport` snapshot dated 2026-11-09.
- **Counts:** Six unique non-seed candidate works, seven works including S. Both counts are below 10. P-alias is merged into P, and the two export rows for F are deduplicated. Four unique citation edges are verified within the fixture.

| Seed/direction | Coverage | Evidence and stopping reason |
|---|---|---|
| S backward, hop 1 | **Complete within the inspected source** | The corpus explicitly supplies S's complete reference list: S.Ref.1 and S.Ref.2. Both were processed. This is completeness for the supplied seed version and reference list, not global literature coverage. |
| S forward, hop 1 | **Partial** | All three rows of supplied export page 1 were processed, yielding two unique citing works. `next_page=2` is present, page 2 is missing, and the total record count is unknown. F.Ref.7 independently corroborates one edge. |

Expansion stopped after the supplied one-hop evidence was exhausted. The work cap was not reached; the missing forward-export page prevents completion of that source. No recursive expansion was attempted.

## Work ledger and screening

Locators below refer to the single corpus file identified above. “Include” means relevant at the available evidence level, not a judgment of scientific quality or correctness.

| Work ID | Bibliographic record | Synthetic identifier; publication/version | Inspected source and access level | Screening decision |
|---|---|---|---|---|
| S | *DampTrace: damping-ratio estimation from low-noise oscillator traces* — Mira Example and Rowan Fixture, 2024 | `10.0000/fixture.s`; preprint v1 | “Seed S — record and supplied excerpt”; S.Results.1; S.Ref.1–2. Metadata, relevant result passage, complete reference list; no full text. | **Include — seed.** Directly concerns damping-ratio estimation and a low-noise synthetic evaluation. |
| P | *PeakDrop baseline for damping-ratio estimation* — Lee Sample, 2022 | `10.0000/fixture.p`; journal v1 | Bibliographic catalog rows P and P-alias; P.Abstract.1; S.Ref.1. Metadata and abstract. | **Include.** The abstract describes a damping-ratio estimator for a synthetic oscillator and reports a reference implementation. The implementation itself is not supplied. |
| M | *Calibration notes for synthetic ring-down signals* — Nia Placeholder, 2023 | `10.0000/fixture.m`; report v1 | Bibliographic catalog row M; S.Ref.2. Metadata only. | **Pending.** A verified predecessor citation, but the title alone does not establish its connection to damping-ratio estimation methods or evaluations. |
| F | *High-noise evaluation of DampTrace* — Eli Test, 2025 | `10.0000/fixture.f`; journal v1 | Bibliographic catalog row F; F.Results.1; F.Ref.7; CitingExport.page1.row1 and row2. Metadata, relevant result passage, one reference, export rows; no full text. | **Include.** The supplied passage evaluates DampTrace and PeakDrop on a high-noise synthetic trace set. |
| X | *Teaching citation management with DampTrace* — Avery Demo, 2025 | `10.0000/fixture.x`; workshop v1 | Bibliographic catalog row X; X.Abstract.1; CitingExport.page1.row3. Metadata and abstract, plus citation-export evidence. | **Exclude.** Its abstract explicitly concerns bibliography formatting and says it does not study oscillator models or estimation error. Its citation remains part of the verified network. |
| R | *A different estimator for oscillator damping ratio* — Quinn Mock, 2025 | `10.0000/fixture.r`; preprint v1 | Bibliographic catalog row R; RelatedList.row1. Metadata and topic-similarity recommendation only. | **Pending; outside the verified one-hop network.** The title suggests relevance, but no substantive text or citation relation is supplied. |
| J | *DampTrace: damping-ratio estimation from low-noise oscillator traces* — Mira Example and Rowan Fixture, 2025 | `10.0000/fixture.j`; journal v1 | Bibliographic catalog row J; RelatedList.row2. Metadata and possible-version recommendation only. | **Pending; outside the verified one-hop network.** Its relationship to S is unconfirmed. Title and author overlap does not verify a version mapping or a citation edge. |

### Identity handling

- **P:** The S.Ref.1 identifier is `https://doi.org/10.0000/FIXTURE.P`; P-alias uses `HTTPS://DOI.ORG/10.0000/FIXTURE.P`. Removing the DOI URL prefix and comparing without case yields `10.0000/fixture.p`. The catalog also explicitly labels P-alias as the same source record as P, so these are one work.
- **F:** Export row 1 uses `10.0000/fixture.f`; row 2 uses `https://doi.org/10.0000/FIXTURE.F`. The same normalization identifies one citing work and one edge. Both evidence locators are retained.
- **S and J:** Kept as separate records with their supplied identifiers, years, and versions. J is only an unverified possible journal publication of S. Edges to S remain attached to the 2024 preprint v1; no edge or result is transferred to J.
- All bibliographic identities and identifiers are accepted only as local fixture records. No external identifier verification or full-text identity resolution was performed.

## Verified citation network

Every arrow means **citing work → cited work**. The table is the network; screening does not erase a verified but out-of-scope citation.

| Citing work | Cited work | Discovery relative to S | Evidence locator(s) | Verification |
|---|---|---|---|---|
| S | P | Backward, hop 1 | S.Ref.1; identity matched to catalog P/P-alias | Verified in supplied corpus |
| S | M | Backward, hop 1 | S.Ref.2 | Verified in supplied corpus |
| F | S | Forward, hop 1 | CitingExport.page1.row1; CitingExport.page1.row2; F.Ref.7 explicitly cites preprint v1, 2024, `10.0000/fixture.s` | Verified in supplied corpus; one edge with three supporting locators |
| X | S | Forward, hop 1 | CitingExport.page1.row3 | Verified in supplied corpus; X excluded by topical screening |

R's recommendation and J's possible-version suggestion are **not citation edges**. There is no evidence for an edge between S and either work in either direction. F's comparison with PeakDrop also does not, by itself, verify an F → P citation.

## Reading order

1. **S — read the seed's supplied result passage first.** This defines the method name, baseline, and low-noise synthetic evaluation setting. The available passage supports only a narrow account of reported results; it does not disclose enough to reconstruct the method.
2. **P — read P.Abstract.1 for the baseline's stated purpose.** It identifies PeakDrop as a damping-ratio estimator for a synthetic oscillator and reports a reference implementation. Detailed algorithm, implementation, and evaluation assessment require material absent from this corpus.
3. **F — read F.Results.1 and F.Ref.7.** The result passage supplies a relevant evaluation on high-noise synthetic traces; the reference separately confirms that F cites the seed preprint. This is the most directly relevant supplied follow-up evaluation, but its full methods and uncertainty assessment are unavailable.

M, R, and J remain conditional follow-up candidates rather than assessed on-topic reading. X is excluded and is not recommended for this research question.

### What the result passages actually support

| Passage | Supplied test condition | Reported mean absolute damping-ratio error | Limits of the passage |
|---|---|---|---|
| S.Results.1 | Low-noise synthetic trace set | DampTrace: 0.02; PeakDrop: 0.04 | No high-noise results or uncertainty estimates in this excerpt. |
| F.Results.1 | Separately generated high-noise synthetic trace set | DampTrace: 0.06; PeakDrop: 0.04 | No uncertainty estimates in this excerpt. |

These invented passages report different error orderings under different test conditions. They do not establish a general contradiction, replication, causal explanation, or statistically reliable superiority. The citation evidence establishes that F cites S; it does not establish that F extends, validates, or refutes S.

## Remaining frontier and limitations

- **Missing forward frontier:** `CitingExport` page 2 and any subsequent pages. Their records and count are unknown, so unseen candidates cannot be enumerated or counted. Page 1 is not a complete global forward-citation index.
- **Unresolved topical coverage:** M has no text. R has metadata only and no citation adjacency. J has neither a verified relationship to S nor citation adjacency. All remain separate from supported topical conclusions.
- **Access ceiling:** No work has supplied full text. S and F provide short result excerpts; P and X provide abstracts; M, R, and J provide metadata only. Method details, evaluation design, uncertainty, and broader limitations cannot be reconstructed from these materials.
- **Version ceiling:** The seed is specifically the 2024 preprint v1. The 2025 journal record J is unconfirmed, so results and citations cannot be pooled across the two.
- **Depth ceiling:** Work beyond one hop was not explored. No second-hop frontier was enumerated, and a shared method name, baseline mention, or recommendation was never converted into a citation.
- **Next action within the offline scope:** If the supplied corpus is later extended, inspect the missing export page, then M's relevant text and evidence resolving J's version relationship. Any newly encountered unique work must still respect the cap; conservatively counting the seed leaves three slots before reaching ten total works. No additional material was retrieved for this answer.
