---
name: prior-art-search
description: "Search patent databases and academic literature for prior art relevant to an invention. Use when user says \"Retrieval of existing technologies\", \"prior art search\", \"Patent Retrieval\", \"check patents\", or wants to find relevant prior art."
argument-hint: "[invention-description-or-path]"
allowed-tools: Bash(*), Read, Glob, Grep, WebSearch, WebFetch, Write
---

# Prior Art Search

Search patents and literature for prior art relevant to: **$ARGUMENTS**

Adapted from `/research-lit` for patent-specific searching.

## Constants

- `MAX_PATENT_RESULTS = 20` — Maximum patent documents to analyze in detail
- `MAX_PAPER_RESULTS = 15` — Maximum academic papers to analyze in detail
- `SEARCH_YEARS = 10` — How many years back to search
- `PATENT_DATABASES = "google-patents, espacenet"` — Patent databases to search

## Inputs

Read the invention description from:
1. `$ARGUMENTS` if it contains technical details
2. `patent/INVENTION_BRIEF.md` if it exists
3. `INVENTION_BRIEF.md` if it exists at project root

## Shared References

Load `../shared-references/prior-art-databases.md` for search strategy templates and IPC/CPC classification guidance.

## Workflow

### Step 1: Extract Search Concepts

From the invention description, identify:
1. **Core inventive concept**: The primary technical contribution (1-2 sentences)
2. **Technical problem**: What problem it solves
3. **Key technical features**: 4-6 specific technical elements that define the invention
4. **IPC/CPC classes**: Predict relevant classification codes (e.g., G06N, G06F)

### Step 2: Patent Search

For EACH search concept, search via:

**Google Patents** (via WebSearch):
```
WebSearch: "site:patents.google.com [keywords]"
WebSearch: "[keywords] patent"
```
- Try primary keywords + technical problem keywords
- Search in English regardless of target jurisdiction
- For CN inventions, also search Chinese keywords via WebSearch

**Espacenet** (via WebFetch):
- WebFetch worldwide.espacenet.com/search results for key queries
- Search by predicted IPC/CPC classes

**Assignee/Inventor Search**:
- If known companies/universities work in this area, search their patent portfolios
- WebSearch: "[assignee name] patent [technical area]"

For each potentially relevant patent found:
- WebFetch the patent page to extract: title, abstract, representative claims, filing date, assignee, current status
- Record IPC/CPC classification codes

### Step 3: Academic Literature Search

Search the same concepts in academic databases:

1. **Google Scholar** (via WebSearch): `WebSearch "[keywords] site:scholar.google.com"`
2. **arXiv** (via `/arxiv` if available, or WebSearch): Search for preprints
3. **Semantic Scholar** (via `/semantic-scholar` if API key set, or WebSearch)

For each relevant paper found:
- Extract title, authors, venue, year, key contribution

### Step 4: Classification and Analysis

For each reference found, assess:

1. **Relevance**: How closely does it relate to the invention?
2. **Overlap Risk**: Does it disclose the same or similar technical solution?
   - HIGH: Anticipates one or more claim elements
   - MEDIUM: Discloses a related but different approach
   - LOW: Same general field, different approach
3. **Relationship**: Is it anticipating, relevant, or merely background?

Organize results by IPC/CPC classification to see the technical landscape.

### Step 5: Freedom-to-Operate Assessment (Preliminary)

Based on the search results:
- Identify patents with claims that potentially cover the invention
- Note any expired patents (public domain)
- Flag areas where claim scope overlap is significant

**Disclaimer**: This is a preliminary assessment only. A professional freedom-to-operate analysis by a patent attorney is recommended before filing.

### Step 6: Output

Write `patent/PRIOR_ART_REPORT.md` with:

```markdown
## Prior Art Search Report

### Invention Summary
[1-2 sentence description of the searched invention]

### Search Strategy
- Keywords used: [...]
- IPC/CPC classes searched: [...]
- Databases searched: Google Patents, Espacenet, Google Scholar, arXiv
- Date range: [year] to present

### Patent References Found

| # | Patent No. | Title | Date | Assignee | IPC/CPC | Key Teaching | Overlap Risk |
|---|-----------|-------|------|----------|---------|-------------|-------------|
| 1 | CN... / US... | [title] | [date] | [assignee] | [codes] | [2-3 sentences] | HIGH/MEDIUM/LOW |

### Non-Patent Literature Found

| # | Reference | Title | Authors/Venue | Year | Key Contribution | Relevance |
|---|-----------|-------|--------------|------|-----------------|-----------|
| 1 | [DOI/link] | [title] | [authors] | [year] | [1-2 sentences] | HIGH/MEDIUM/LOW |

### Prior Art Landscape
[Organized by technical approach or IPC class, not just chronological]

### Freedom-to-Operate Preliminary Assessment
[Which existing patents might block the invention? What is the risk level?]

### Recommendations
- Suggested claim scope adjustments based on prior art
- Areas where novelty appears strongest
- References to watch during prosecution
```

## Key Rules

- Never fabricate patent numbers or citations. Mark uncertain references with `[VERIFY]`.
- Search in English AND the target jurisdiction language (Chinese for CN).
- Patent prior art includes everything published before the priority date, not just patents.
- Academic papers are valid prior art for both novelty and inventive step.
- Include expired patents -- they are public domain but still relevant for novelty.

## Mirror description (additional to this open warehouse)
- This document is considered upstream. ARIS mirrors in original;support files (scripts/、references/、../shared-references/）Not distributed with mirrors, full originals can be found at the upstream warehouse https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep 。
- If supporting documents are cited for implementation skills, then the relative path should be parsed from the upstream warehouse.

## Environmentally appropriate (additional to this open warehouse) Retrieval integrity supplement (red line executable on the basis of docs/LESSONS_FROM_OTHERS.md Section I:
- Minimum search source: quick check ≥2 Independent sources; overview ≥3；System Overview/Chasing ≥4，and record search mode;
- The results have to be reported."Not found"，(b) Prohibition of regression to training memory to create entries, authors or numbers;
- I'll be right over. checklist：①Each result contains verifiable information (titles)/Author/Year/Source)②Undefined item"To be verified"
  ③Specify screening criteria ④Retrieving contradictions/Negative evidence.
