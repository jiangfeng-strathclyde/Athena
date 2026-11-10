# Citation network output contract

Use stable local work IDs and keep the following information, adapting the
presentation to the requested size. Empty or unavailable fields stay explicit;
they are not permission to infer identifiers, passages, or citation links.

## Scope and coverage

Record the question, seeds and versions, inclusion criteria, requested directions,
sources actually inspected, access/retrieval dates, depth and budget, and stop
reason. For each seed/direction, distinguish **complete within the inspected
source**, **partial**, **unavailable**, and **not requested**. A complete local
export is not a complete global literature search. Record an export's snapshot
date separately from today's inspection date when available.

## Work ledger

| Field | Meaning |
|---|---|
| work_id | Stable local identifier, not a made-up DOI |
| bibliographic record | Title, authors, year; unknown fields marked as such |
| persistent ID and version | Verified DOI/arXiv/provider ID, version, publication type |
| identity notes | Duplicate aliases, related versions, or unresolved matches |
| inspected source and locator | File/page or retrieved record URL; what was actually read |
| access level | Metadata, abstract, relevant passage, or full text |
| screening | Include / exclude / pending and reason against the question |

## Edge ledger

| Field | Meaning |
|---|---|
| citing_work_id | The work containing the citation |
| cited_work_id | The work referenced by it |
| discovery | Backward/forward relative to the seed; include seed ID and hop |
| evidence locator | Reference entry, export row, or citation endpoint record |
| verification | Verified or unresolved; only verified edges enter the network |

Preserve multiple source locators if the same edge occurs more than once, but
do not double-count the edge. Recommendation lists and missing pages belong in
an unresolved-candidate list, not in the verified-edge count.

## Reading order and limitations

Explain why each recommended work matters and which parts can currently be
assessed. Keep evidence for a scientific interpretation separate from evidence
that a citation exists. List remaining frontier items or pages, unavailable
directions, identity ambiguities, and a useful next action within the user's
scope. Do not describe citation frequency as proof of scientific correctness.
