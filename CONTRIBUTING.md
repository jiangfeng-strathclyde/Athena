# Contributing

Contributions are welcome. This repository accepts new skills as well as
improvements to the clone protocol and documentation.

## Add a skill in five steps

1. Copy the template: `cp clone-kit/SKILL_TEMPLATE.md skills/<my-skill>/SKILL.md`.
2. Complete the trigger conditions, workflow, outputs, and integrity rules.
3. Add `license: MIT` to the frontmatter, or identify the upstream source and
   its compatible license.
4. Add the skill to `clone-kit/ROUTING_TABLE.md`.
5. Open a pull request with the checklist below completed.

## Skill format

Use `skills/<skill-name>/SKILL.md`. Optional supporting files may live in
`scripts/` and `references/` inside that skill directory.

Every skill needs valid frontmatter:

```yaml
---
name: <kebab-case-name>
description: <one sentence explaining when to use the skill and its trigger words>
license: MIT
---
```

Keep descriptions under 1,024 characters and make trigger terms easy to search.

## Integrity checklist

- [ ] The skill does not request credentials unless they are genuinely needed.
- [ ] Required tokens, webhooks, accounts, and environment variables are named.
- [ ] It does not bypass permissions, security checks, or administrator controls.
- [ ] External calls use appropriate public or documented APIs and fail clearly.
- [ ] Numerical outputs include a recomputation or test method.
- [ ] Upstream content has compatible licensing and attribution.
- [ ] A minimal reproduction and expected behavior are included.

Security scanners may block a contribution. Do not bypass them; document the
result in [`docs/TRANSPARENCY_LOG.md`](docs/TRANSPARENCY_LOG.md) and discuss it.

## Protocol and documentation changes

A semantic change to `docs/CLONE_PROTOCOL.md` should update the protocol version
and explain backward compatibility in the pull request. Never add private
identity information, unpublished data, credentials, or private memory to the
public distilled guide.

## Community standards

- Welcome beginners and explain the reason behind recommendations.
- Share clone examples through the `clone-show-and-tell` Discussion template.
- Keep criticism specific, reproducible, and focused on the work.

By contributing, you agree that your contribution may be published under this
repository's MIT license. Derived content remains subject to its original
copyright and license requirements.
