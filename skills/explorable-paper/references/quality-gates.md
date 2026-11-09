# Quality gates

Use these gates proportionally. Record `passed`, `failed`, `not run`, or `not
applicable`; do not collapse them into one unqualified “validated” label.

## Evidence

- Every material reported claim has a usable source locator.
- Reported evidence, observed runs, teaching models, inference, and proposals
  are visually distinguishable.
- Units, denominators, uncertainty, sample counts, and comparison conditions
  remain attached to the result they qualify.
- Missing supplements, raw data, code, or coverage are visible limitations.

## Computation

- Inputs, fixed conditions, valid ranges, and outputs are documented.
- Representative, boundary, invalid, and degenerate cases are checked where
  relevant.
- Reference values come from a hand calculation, independent code path, or
  canonical data rather than the rendering function under test.
- Tolerances and numerical precision are justified.

## Interaction and presentation

- Every control answers a stated reader question and visibly changes the
  relevant state or explanation.
- Reset and preset actions are deterministic.
- Comparable quantities share units and definitions; incomparable metrics are
  not placed on a misleading common scale.
- Focus order, labels, keyboard operation, contrast, narrow layout, and reduced
  motion have been checked.

## Packaging and behavior

- The documented entry point opens from a clean directory while offline.
- No unintended network request, telemetry, console error, or missing asset
  occurs.
- All controls, dialogs, source links, and navigation paths are exercised in a
  real browser.
- Editable source, build steps, input provenance, and generated artifact are
  clearly separated.

## Scientific status

- A successful page build is described as a build, not a reproduction.
- A method is called executed only when the actual implementation ran with a
  recorded input and log.
- Reader understanding is not claimed to improve unless real reader evaluation
  was conducted; otherwise label that evaluation planned or not run.
