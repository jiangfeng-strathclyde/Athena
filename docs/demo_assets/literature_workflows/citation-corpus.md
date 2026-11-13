# Synthetic citation corpus

All names, identifiers, papers, and results below are invented fixtures, not
scientific evidence. DOI-shaped strings are test identifiers and must not be
looked up. The corpus is a local snapshot dated 2026-11-09.

## Seed S — record and supplied excerpt

- Title: DampTrace: damping-ratio estimation from low-noise oscillator traces
- Authors: Mira Example and Rowan Fixture
- Year: 2024
- Type/version: preprint v1
- Identifier: `10.0000/fixture.s`
- Material: metadata, result excerpt, and complete reference list only
- Result excerpt S.Results.1: In the low-noise synthetic trace set, DampTrace's
  mean absolute damping-ratio error was 0.02 and the PeakDrop baseline's was 0.04.
  No high-noise traces or uncertainty estimates are included in this excerpt.
- Reference S.Ref.1: Lee Sample. PeakDrop baseline for damping-ratio estimation. 2022.
  `https://doi.org/10.0000/FIXTURE.P`
- Reference S.Ref.2: Nia Placeholder. Calibration notes for synthetic ring-down signals.
  2023. `10.0000/fixture.m`

## Bibliographic catalog

| ID | Title | Authors | Year | ID/version | Available content |
|---|---|---|---|---|---|
| P | PeakDrop baseline for damping-ratio estimation | Lee Sample | 2022 | `10.0000/fixture.p`; journal v1 | Metadata and P.Abstract.1 below |
| P-alias | PeakDrop baseline for damping-ratio estimation | Lee Sample | 2022 | `HTTPS://DOI.ORG/10.0000/FIXTURE.P`; journal v1 | Same source record as P |
| M | Calibration notes for synthetic ring-down signals | Nia Placeholder | 2023 | `10.0000/fixture.m`; report v1 | Metadata only; no text supplied |
| F | High-noise evaluation of DampTrace | Eli Test | 2025 | `10.0000/fixture.f`; journal v1 | Metadata, result excerpt, one reference |
| X | Teaching citation management with DampTrace | Avery Demo | 2025 | `10.0000/fixture.x`; workshop v1 | Metadata and abstract |
| R | A different estimator for oscillator damping ratio | Quinn Mock | 2025 | `10.0000/fixture.r`; preprint v1 | Metadata only |
| J | DampTrace: damping-ratio estimation from low-noise oscillator traces | Mira Example and Rowan Fixture | 2025 | `10.0000/fixture.j`; journal v1 | Metadata only; relationship to S not confirmed |

P.Abstract.1: This paper introduces the PeakDrop baseline for estimating the
damping ratio of a synthetic oscillator. It reports a reference implementation.

F.Results.1: On a separately generated high-noise synthetic trace set, DampTrace's
mean absolute damping-ratio error was 0.06 and PeakDrop's was 0.04. No uncertainty
estimates are supplied in this excerpt.

F.Ref.7: Mira Example and Rowan Fixture. DampTrace: damping-ratio estimation from
low-noise oscillator traces. Preprint v1, 2024. `10.0000/fixture.s`.

X.Abstract.1: This workshop exercise uses DampTrace's reference list to teach
bibliography formatting. It does not study oscillator models or estimation error.

## Forward-citation export for S

Source: supplied local export `CitingExport`, snapshot 2026-11-09. Page 1 only.
The export's relation field means the row's citing record cites the cited record.
The indicated page 2 has not been supplied.

| Row locator | Citing record | Cited record | Relation |
|---|---|---|---|
| CitingExport.page1.row1 | `10.0000/fixture.f` | `10.0000/fixture.s` | cites |
| CitingExport.page1.row2 | `https://doi.org/10.0000/FIXTURE.F` | `10.0000/fixture.s` | cites |
| CitingExport.page1.row3 | `10.0000/fixture.x` | `10.0000/fixture.s` | cites |

Pagination: `next_page=2`; total records unknown.

## Other discovery records

- RelatedList.row1 recommends R for topic similarity to S. No citation relation
  is present in the recommendation record.
- RelatedList.row2 suggests J as a possible publication of S. No version mapping,
  full text, or reference list is supplied.
