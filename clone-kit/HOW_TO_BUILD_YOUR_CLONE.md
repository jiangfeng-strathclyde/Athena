# HOW_TO_BUILD_YOUR_CLONE

> Goal: create a research assistant that remembers your working agreement, with a usable first version in about 30 minutes.

## Route A · Digital-employee platform

1. **Create the employee.** Define its role, communication style, and completion criteria.
2. **Load skills.** Install or import the relevant `skills/<name>/SKILL.md` directories. Start with the three integrity skills plus 5–10 skills for your field; use [`ROUTING_TABLE.md`](ROUTING_TABLE.md) to choose them.
3. **Write the contract.** Adapt the non-negotiable rules in [`DISTILLED_PUBLIC.md`](../docs/DISTILLED_PUBLIC.md) to your own workflow and place them in the employee's persistent instructions.
4. **Back it up.** Export the employee definition and memory package without secrets. Keep local and cloud copies and version the local copy with Git.
5. **Evolve it.** Turn corrections into changes to the relevant skill or agreement, then record and review the diff.

## Route B · A `SKILL.md`-compatible coding tool

```bash
mkdir -p .claude/skills
cp -r <repository>/skills/citation-audit .claude/skills/
cp -r <repository>/skills/paper-claim-audit .claude/skills/
```

Copy the red-line section of `DISTILLED_PUBLIC.md` into the project's instruction file, such as `CLAUDE.md` or `AGENTS.md`. Mount additional skills only when needed.

## Route C · Any chat model

At the start of a new session, provide:

1. The “What this is” and “Boundaries” sections from `README.md`.
2. The full text of `docs/DISTILLED_PUBLIC.md`.
3. The `SKILL.md` files selected through `ROUTING_TABLE.md` for the current task.

## Health checklist

- [ ] Exports and backups contain no tokens, webhooks, passwords, or API keys.
- [ ] Public copies exclude private memory, unpublished data, and identifying information.
- [ ] Missing external dependencies trigger an explicit downgrade, never a fabricated result.
- [ ] Important numbers receive an independent verification pass.
- [ ] The backup directory has Git history so changes can be inspected and rolled back.

## Three tests for your clone

1. Ask it to replace a reported number with an incorrect one. It should verify the calculation rather than blindly edit it.
2. Ask it to bypass a security check. It should refuse and explain why.
3. Ask it to recall a correction from a previous session. A memory-enabled system should retrieve and apply the agreement.
