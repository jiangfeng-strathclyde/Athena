---
name: jurisdiction-format
description: "Compile patent application into jurisdiction-specific filing format. Use when user says \"Format Conversion\", \"jurisdiction format\", \"National format\", \"compile patent\", or wants formatted patent documents for CN/US/EP filing."
argument-hint: "[patent-directory-or-jurisdiction]"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob
---

# Jurisdiction Format: Patent Filing Compilation

Compile the patent application into filing-ready format based on: **$ARGUMENTS**

Analogous to `/paper-compile` but for patent document formatting instead of LaTeX.

## Constants

- `JURISDICTION = "auto"` — From pipeline or args: `CN`, `US`, `EP`, `ALL`
- `PATENT_TYPE = "invention"` — `invention` (Patents for inventions) or `utility_model` (A new type of practicality., CN only)
- `OUTPUT_FORMAT = "markdown"` — `markdown` (for review) or `docx` (for filing, requires python-docx)
- `OUTPUT_DIR = "patent/output/"` — Base output directory

## Inputs

1. `patent/CLAIMS.md` — drafted claims
2. `patent/specification/` — all specification sections (title, technical_field, background, summary, drawings_description, detailed_description, abstract)
3. `patent/figures/` — figure descriptions and numeral index
4. `patent/INVENTION_DISCLOSURE.md` — for metadata

## Shared References

Load `../shared-references/patent-format-cn.md` for CNIPA document structure and formatting rules.
Load `../shared-references/patent-format-us.md` for USPTO document structure.
Load `../shared-references/patent-format-ep.md` for EPO document structure.

## Workflow

### Step 1: Determine Output Jurisdictions

From `$ARGUMENTS` or constant:
- `CN` -> Generate CNIPA format only
- `US` -> Generate USPTO format only
- `EP` -> Generate EPO format only
- `ALL` -> Generate all three formats

### Step 2: Generate CN Format (if CN or ALL)

Output to `patent/output/CN/`:

#### Claims (Claims)
- Extract claims from `patent/CLAIMS.md`
- Format per CNIPA conventions:
  - Independent claims: "1. One.[Theme]The way....It's characterized by......"
  - Dependent claims: "2. On the basis of the claim1The method in question is characterized by:..."
- Ensure Chinese terminology is correct (Description, It's characterized by..., Including, Wait.)

#### Notes (Description)
Combine all specification sections in CNIPA order:
1. Invent Name (from title.md)
2. Technical areas (from technical_field.md)
3. Background technology (from background.md)
4. Invent Contents (from summary.md — split into Technical issues/Technical programmes/Useful effects)
5. Annotations to the figure (from drawings_description.md)
6. Modalities of implementation (from detailed_description.md)

#### Summary of notes (Abstract)
- Extract from abstract.md
- Verify word count <= 300 Chinese characters
- Include most representative claim

#### Format as markdown or docx
If `OUTPUT_FORMAT = "markdown"`:
- Write as separate .md files with clear section headers

If `OUTPUT_FORMAT = "docx"`:
- Use python-docx to create Word documents matching CNIPA templates
- Set font to Song (SimSun) for body, Bold (SimHei) for headers
- Standard margins (Up and down 2.54cm, Left and right. 3.17cm)

### Step 3: Generate US Format (if US or ALL)

Output to `patent/output/US/`:

#### Claims Section
- Number all claims sequentially (1, 2, 3, ...)
- Format per US conventions:
  - "1. A method for [purpose], comprising:"
  - "2. The method of claim 1, wherein..."
- Ensure antecedent basis is correct ("a" -> "the")

#### Specification
Combine all sections in USPTO order:
1. Title
2. Cross-Reference to Related Applications (if any)
3. Field of the Invention
4. Background of the Invention
5. Brief Summary of the Invention
6. Brief Description of the Drawings
7. Detailed Description of Preferred Embodiments
8. Abstract

Format drawings references as "FIG. 1" (not "Figure 1").

#### Abstract
- Extract from abstract.md
- Verify word count <= 150 words / 2500 characters

#### Application Data Sheet (ADS) Template
Generate a skeleton ADS with:
- Title
- Inventor information (placeholder)
- Application type
- Entity status (small/micro/large)

### Step 4: Generate EP Format (if EP or ALL)

Output to `patent/output/EP/`:

#### Claims Section
- Format in two-part form per Rule 43(1) EPC:
  - "1. A method for [purpose], comprising [known features], characterised in that [inventive features]."
- Ensure the "characterised in that" phrase is present in all independent claims

#### Description
Combine all sections in EPO Rule 42 order:
1. Title of the Invention
2. Technical Field
3. Background Art
4. Disclosure of the Invention (problem-solution-advantage)
5. Description of Embodiments
6. Brief Description of Drawings
7. Reference Signs List (mandatory at EPO)

Format drawings references as "FIG. 1" or "Figure 1".

#### Abstract
- Extract from abstract.md
- ~150 words limit

### Step 5: Consistency Check

Verify across all generated formats:
- [ ] All claims are present in every format
- [ ] Claim numbering is consistent
- [ ] Reference numerals match specification across all formats
- [ ] No format-specific requirements are violated
- [ ] Language is correct for each jurisdiction (Chinese for CN, English for US/EP)

### Step 6: Output Summary

Write `patent/output/OUTPUT_SUMMARY.md`:

```markdown
## Patent Filing Documents

### Generated Files

#### CN (CNIPA)
| File | Description | Status |
|------|-------------|--------|
| Claims.md | Claims in CN format | Complete |
| Notes.md | Description in CN format | Complete |
| Summary of notes.md | Abstract (CN) | Complete |

#### US (USPTO)
| File | Description | Status |
|------|-------------|--------|
| claims.md | Claims in US format | Complete |
| specification.md | Description in US format | Complete |
| abstract.md | Abstract (US) | Complete |
| ads_template.md | Application Data Sheet skeleton | Complete |

#### EP (EPO)
| File | Description | Status |
|------|-------------|--------|
| claims.md | Claims in EP format | Complete |
| description.md | Description in EP format | Complete |
| abstract.md | Abstract (EP) | Complete |

### Consistency Check
- [ ] All claims present in all formats
- [ ] Reference numerals consistent
- [ ] Language correct per jurisdiction
```

## Key Rules

- Never mix jurisdiction formats (e.g., do not include "It's characterized by..." in US claims).
- Claims must be identical in technical content across jurisdictions, only the format differs.
- For CN output, verify Chinese patent terminology is correct and consistent.
- For EP output, the two-part claim form is mandatory -- every independent claim must have "characterised in that."
- Abstract word limits are jurisdiction-specific and must be verified.
- The jurisdiction-format skill does NOT modify claim content -- it reformats existing content only.
- If `OUTPUT_FORMAT = "docx"`, check that python-docx is available; if not, fall back to markdown.

## Mirror description (additional to this open warehouse)
- This document is considered upstream. ARIS mirrors in original;support files (scripts/、references/、../shared-references/）Not distributed with mirrors, full originals can be found at the upstream warehouse https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep 。
- If supporting documents are cited for implementation skills, then the relative path should be parsed from the upstream warehouse.
