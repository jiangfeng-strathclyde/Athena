# Athena antenna case study

The repository includes a self-contained explorable article on movable-antenna
channel geometry, three-dimensional placement, penalty continuation, feasible
regions, convergence assumptions, and empirical method comparisons.

- Live artifact: <https://jiangfeng-strathclyde.github.io/Athena/examples/antenna-direction.html>
- Repository copy: `docs/examples/antenna-direction.html`

The example is useful because its interactions are tied to explicit questions:
how phase alignment changes the channel, what a position-update block actually
does, when a two-dimensional slice misrepresents a three-dimensional feasible
set, and where penalty or convergence claims stop applying. Its original build
also checked known values, exercised controls in Chromium, inspected console
errors, and compared generated numerical behavior with research outputs.

Do not copy its Chinese prose, antenna equations, color system, or widget count
into unrelated papers. Reuse the method: claim-to-evidence mapping,
question-driven interaction, explicit boundaries, independent numerical
checks, and a portable offline build.

The public repository intentionally excludes the source paper PDF, third-party
archives, unpublished experiment outputs, and generated screenshot corpus. The
HTML is a curated demonstration artifact, not a redistribution of those inputs
or a claim that every underlying experiment can be rebuilt from the demo alone.
