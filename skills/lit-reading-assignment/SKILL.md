---
license: MIT
name: lit-reading-assignment
description: >-
  For the students./Team generation of directly usable bibliography list: complete searchable bibliography (titles)/Author/venue/Year/DOI）、
  Grouping by theme, priority reading, description of each“What's it about? What's it got to do with the project?”Read in order with the recommendation./The team leader is required to prepare a list of reading tasks, group books, and an entry route.
version: 1.0.0
---

# Literature Reading Assignment（Exact List Generation)

## Trigger scene

- “I'll set up a few weeks of reading for the students.”“Group Books”“Give the newcomer an introduction route.”；
- There's a lot of paperwork that needs to be sorted out.“Directly enforceable”...the task of reading, not losing one. Zotero Coop.

## Input

- Theme or project background (one sentence sufficient);
- Reader ' s Level (HBO) / Master ' s first grade / Doctor. / (a) The number of weeks available;
- Optional: List of candidates, target periodicals available/Scope of the meeting.

## Process

1. **Search**：`research-lit` / `arxiv` / `semantic-scholar` / `openalex` Draws out candidatures (%)≥20 (b) Books;
2. **Bibliographic verification**：Line-by-line Nuclear DOI/Author/Year/venue（Lighter version `citation-audit`）；
   Unrecognizable markers UNCERTAIN And retrying with a new source.**I'll never make it up. DOI**；
3. **Grouping and Priority**：By theme 3–5 groups;headings per group have to be read / Select to read / (b) A general reading and a statement of reasons;
4. **All three questions.**：Read what?/Datasets/Which part of the conclusions, what relationship to the project (which ring it supports), what it's reading with it. 3 Question (prevention of general reading);
5. **Sort**：Suggested order of reading (summation of methodology, baseline) SOTA），And it's time-consuming to estimate each one.
6. **Delivery**：A single list of documents can be opened without further questions from students.

## Output Template

```markdown
# <Theme> Exact List (List)<Level> · <Weeks>）
## Group 1 · <Theme Group Name>
### [I'll read it.] <Title>
- Bibliography:<Author> , <venue> <Year> , DOI: <doi>
- Read what?<Methodology/Data/Specific part of the conclusions>
- Relationship to project:<Hold on to that ring.>
- Read it with questions:1) ... 2) ... 3) ...
- Projected time-consuming:<h>
...
## Recommended order and weekly plan

Week 1: establish the reading list and assign foundational papers. Week 2: compare methods, evidence, and open questions.
```

## Red Line

- Bibliography must be searchable: title/Author/venue/Year/DOI Full and verified;
- Priority versus“Read what?”There must be a reason not to write empty words (e.g.“It's important.”）；
- (b) Do not insert a collection of literature related to the weak theme; prefer not to abuse it;
- In connection with the ongoing trial/When not working, only public versions are quoted and no internal text information is disclosed.

## Collaborative skills Retrieval `research-lit`、`semantic-scholar`、`openalex`；Verification `citation-audit`；
Overview `comm-lit-review` / `research-lit`；The knowledge base settles. `research-wiki`。
