---
name: explorable-paper
description: "Create, audit, or extend an evidence-linked interactive HTML exploration of a scholarly paper. Use for explorable papers, interactive research articles, paper-to-HTML projects, parameter or theorem explorers, and offline scientific demos; not for ordinary landing pages, posters, or decorative paper summaries."
license: MIT
---

# Explorable paper

Turn a paper into an interface for testing understanding, not merely a more
visual abstract. Work from the paper, supplements, code, and data actually
provided or accessed. Keep reported results, recomputations, teaching models,
and new proposals visibly distinct.

## Choose the mode

- **Create:** map a paper to a new interactive, offline-first HTML artifact.
- **Audit:** inspect an existing explorable page for evidence, numerical,
  interaction, accessibility, and portability problems. Do not silently
  redesign it when the user requested findings only.
- **Extend:** add a bounded module while preserving existing claims, styles,
  source links, and verified behavior.

Ordinary paper websites, posters, slide decks, and static summaries are outside
this skill unless the user specifically wants an explorable research interface.

## Build the evidence map first

Identify the reader's hardest useful questions before choosing widgets. For
each important module, record:

1. the question a reader should be able to answer;
2. the source locator: page, section, equation, figure, table, dataset field,
   or repository file and revision;
3. the capability type: **reported evidence**, **data exploration**,
   **teaching model**, or **method execution**;
4. inputs, units, fixed assumptions, outputs, and valid range;
5. what the interaction does not establish.

Do not infer sample-level data from a summary figure. Do not call a simplified
equation a reproduction, or a parameter sweep a convergence proof. If the
paper, code, or data is missing, retain the gap and build only what the
available evidence supports.

## Select interactions by explanatory value

Prefer a small number of modules that expose a mechanism or decision:

- sensitivity and boundary-condition explorers;
- objective, constraint, penalty, and intermediate-term decomposition;
- algorithm traces with pause, reset, and known checkpoints;
- theorem assumption, implication, and counterexample views;
- comparable result filters with units, denominators, and uncertainty;
- failure-region or transfer-condition probes.

Static derivation or evidence-linked prose is better than a slider with no
defensible computation. Animation must reveal state change rather than decorate
the page. Place the governing evidence, assumptions, and boundary beside the
control instead of hiding them in a distant methods note.

## Implement an offline-first artifact

Default to a self-contained HTML file that opens from `file://` with no server,
network request, telemetry, or CDN. Use semantic HTML and code-native SVG,
Canvas, or CSS when practical. If the artifact genuinely needs multiple files,
deliver a portable directory with one documented entry point.

Render research text as text rather than executable markup. Provide keyboard
operation, visible focus, useful alt text, narrow-screen behavior, and reduced
motion. Preserve the user's established visual language when extending an
existing page.

Keep editable source separate from the built artifact when the implementation
is substantial. The source of truth should generate displayed numbers rather
than require parallel manual edits. Include a short provenance note describing
inputs, transformations, and build commands.

## Verify claims and behavior separately

For every computed module, test representative internal values and important
boundaries against a hand derivation, independent implementation, or canonical
data. State the tolerance and why it is appropriate. A moving control is not a
numerical test, and a correct formula outside the browser is not a UI test.

Open the delivered artifact in a real browser and:

- exercise every control, reset, preset, link, and dialog;
- check desktop and narrow layouts, keyboard use, and reduced motion;
- fail on console errors or unintended network requests;
- confirm source locators, units, assumptions, and limitation text;
- copy the artifact to a clean directory and retest offline.

Run the bundled static preflight from this skill directory:

```bash
python scripts/validate_explorable.py /path/to/output.html
```

This preflight detects common packaging failures; it does not validate the
science or replace browser interaction tests. Read
[quality-gates.md](references/quality-gates.md) for the delivery checklist.

## Deliver the result honestly

Return the runnable artifact, editable source when applicable, provenance note,
and a validation report separating:

- structural/static checks;
- source and numerical review;
- browser behavior and accessibility checks;
- actual research reproduction status;
- unresolved or stale items.

Never describe template validation as scientific reproduction or self-review
as independent review. The bundled Athena synthetic example is summarized in
[damped-oscillator-case-study.md](references/damped-oscillator-case-study.md);
use it as a design reference, not as a universal page template.
