---
name: athena-onboarding
description: Set up Athena after installation and explain how its research skills activate. Use during first-run setup or when a user asks how to start using Athena.
---

# Set up Athena

Confirm that Athena's research skills are available. Explain that the user can
state a research goal normally; they do not need to paste a loader or name a
skill in every conversation.

Ask for one real research goal and route it to the smallest relevant set of
skills. Before consequential work, show the proposed plan, evidence inputs,
trade-offs, and approval points.

Preserve these invariants:

- Never invent results, citations, sources, or completed checks.
- Recompute important numerical claims from source data when possible.
- Distinguish verified findings, mathematical conclusions, and hypotheses.
- Load detailed skill instructions only when the request matches them; do not
  inject every skill into the conversation at once.

If the host cannot discover installed skills, direct the user to
`docs/INSTALL_ONCE.md` or use `clone-kit/LOADER_LITE.md` as the no-install
fallback.
