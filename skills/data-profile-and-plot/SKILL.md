---
license: MIT
name: data-profile-and-plot
description: >-
  Table data profile and publishing grade mapping skills: statement of line particle size and caliber before doing profile（Lines/Missing/Repeat/
  Type/Distribution), cleaning logs, diagram specifications (types)/Axis/Units/Error stick./seed），Final check with a stand-alone script
  “The figure is consistent with the figure.”。♪ When the user wants ♪ EDA、It is used for cleaning, drawing, reporting or multi-pane comparison.
version: 1.0.0
---

# Data Profile & Plot（Parsing + (publishing grade drawings)

## Trigger scene

- “Take a look at this. CSV/Parquet/SQLite What do you look like?”“Draw a comparison.”“Reporting Chart”；
- Papers/Results maps, melting maps, multi-pane maps in the report;
- Any tabular data tasks that need to be cleaned up before they can be visualized.

## Process (five steps, in order not to jump)

1. **Declares particle size (grain）**：What's a line? What's the only key? Follow up. join Do you think it'll blow up? `PROFILE.md` First row; particle size is unclear.
2. **Profile**：Number of rows, missing rates, repeat keys, type extrapolation, key column distribution (segment instead of average), time/Group coverage. Output. `PROFILE.md` + Machine reading `profile.json`。
3. **Purge Log**：(b) Deleting samples must keep the original lines and be noted, and should not be allowed to be lost in silence.
4. **Diagram specification first**：Prescription Specifications——Charts, figuresx/y Meaning and unit, range of coordinates (not to cut misdirection), error rod caliberstd / sem / Runtime Variation)seed and n、Colour-blind friendly palettes, vector output.
5. **Independent Validation**：Another script, which is not consistent with the original data recalculation figure for each mark and the statistics. FAIL；Diagrams must contain n With the caliber statement.

## Chart specification (publishing level)

- Default matplotlib/seaborn Pure style; forbidden 3D (a) Pie charts, information-free gradients background;
- Fonts ≥ (a) The minimum word number of the periodical; the multi-faceted uniform coordinates scale or a visible indication of different scales;
- The comparison map must contain a baseline and uncertainty zone; seed Curves shall not be drawn to conclusions;
- Output PDF/SVG Vector + 300dpi PNG backups;file names with calibre suffix (e.g. `_scene-held-out`）。

## Red Line

- Non-compilation of data, non-refilling of points, no extrapolation of undetected areas; absence of measurements leads to a lack of measurements;
- Inconsistent axle creates a perception of difference; if the magnitude must be cut, it is clearly marked break；
- “No significant differences”These words require statistical permission:|Δ| Falling in a variable zone between run-times and p>0.05 (b) To be able to write;
- When the figure is not in line with the text, the figure is closed and the data pipe is fixed before the chart is fixed.

## Output

- `PROFILE.md` / `profile.json`；
- `CLEANING_LOG.md`；
- `figures/`（Vector + PNG）and `figure_spec.yaml`；
- `verify_figures.py`（Independent recalculation of scripts.

## Analysis of results of collaboration skills `analyze-results`；Chart of the paper `paper-figure`；Digital audits `paper-claim-audit`；
Remote sensing domain calibre `remote-sensing-workbench`。
