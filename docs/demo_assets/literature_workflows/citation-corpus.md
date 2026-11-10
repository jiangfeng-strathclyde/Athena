# Synthetic citation corpus

All names, identifiers, papers, and results below are invented fixtures, not
scientific evidence. DOI-shaped strings are test identifiers and must not be
looked up. The corpus is a local snapshot dated 2026-11-09.

## Seed S — record and supplied excerpt

- Title: AngleStep: antenna direction estimation in a clear corridor
- Authors: Mira Example and Rowan Fixture
- Year: 2024
- Type/version: preprint v1
- Identifier: `10.0000/fixture.s`
- Material: metadata, result excerpt, and complete reference list only
- Result excerpt S.Results.1: In the clear-corridor test set, AngleStep's mean
  angular error was 2 degrees and the Grid baseline's was 4 degrees. No obstructed
  corridor tests or uncertainty estimates are included in this excerpt.
- Reference S.Ref.1: Lee Sample. Grid baseline for antenna direction. 2022.
  `https://doi.org/10.0000/FIXTURE.P`
- Reference S.Ref.2: Nia Placeholder. Calibration notes for direction sensors.
  2023. `10.0000/fixture.m`

## Bibliographic catalog

| ID | Title | Authors | Year | ID/version | Available content |
|---|---|---|---|---|---|
| P | Grid baseline for antenna direction | Lee Sample | 2022 | `10.0000/fixture.p`; journal v1 | Metadata and P.Abstract.1 below |
| P-alias | Grid baseline for antenna direction | Lee Sample | 2022 | `HTTPS://DOI.ORG/10.0000/FIXTURE.P`; journal v1 | Same source record as P |
| M | Calibration notes for direction sensors | Nia Placeholder | 2023 | `10.0000/fixture.m`; report v1 | Metadata only; no text supplied |
| F | Obstructed-corridor evaluation of AngleStep | Eli Test | 2025 | `10.0000/fixture.f`; journal v1 | Metadata, result excerpt, one reference |
| X | Teaching citation management with AngleStep | Avery Demo | 2025 | `10.0000/fixture.x`; workshop v1 | Metadata and abstract |
| R | A different estimator for antenna direction | Quinn Mock | 2025 | `10.0000/fixture.r`; preprint v1 | Metadata only |
| J | AngleStep: antenna direction estimation in a clear corridor | Mira Example and Rowan Fixture | 2025 | `10.0000/fixture.j`; journal v1 | Metadata only; relationship to S not confirmed |

P.Abstract.1: This paper introduces the Grid baseline for estimating antenna
direction in a clear corridor. It reports a reference implementation.

F.Results.1: On a separately collected obstructed-corridor test set, AngleStep's
mean angular error was 6 degrees and Grid's was 4 degrees. No uncertainty
estimates are supplied in this excerpt.

F.Ref.7: Mira Example and Rowan Fixture. AngleStep: antenna direction estimation
in a clear corridor. Preprint v1, 2024. `10.0000/fixture.s`.

X.Abstract.1: This workshop exercise uses AngleStep's reference list to teach
bibliography formatting. It does not study antenna-direction methods or accuracy.

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
