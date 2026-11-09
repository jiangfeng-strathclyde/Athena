# BLOCKED_NOTE · Skills Blocked by a Platform Scanner

On 2026-11-06, a platform scanner blocked registration of three mirrored skills. They were not installed on that platform.

| Skill | Scanner warning | Manual review |
|---|---|---|
| `deepxiv` | Appears to exfiltrate local secrets or credentials | Likely triggered by documentation of the `DEEPXIV_TOKEN` environment variable. The skill says not to read or display the token. |
| `paper-compile` | Asks to bypass permissions or escalate privileges | Likely triggered by an optional `sudo apt-get install texlive-full` instruction, which is not applicable to this Windows environment. |
| `paper-poster-html` | Appears to exfiltrate local secrets or credentials | Likely triggered by the design term “token,” not an authentication credential. |

These are recorded manual-review hypotheses, not proof that the warnings were
false positives. We do not reword content merely to evade a scanner. Possible
alternatives include an already-installed local LaTeX compiler, available
literature-reading tools, and manual poster creation; each still needs normal
permission and output checks.

The Python installer excludes these three skills by default. After reading a
skill and its dependencies, the user can explicitly select it with
`--skill NAME --allow-flagged NAME`. Repeat the flags for each selected skill.
This authorization applies only to file installation, not commands or external
actions proposed by the skill, and does not override the host's scanner.
Existing copies from earlier installations are left untouched and reported.

This default filter applies to `scripts/install_athena.py`. Plugin packages
and manual copies still expose the mirrored catalog; use the host's review
and enablement controls before activating any flagged skill.
