# BLOCKED_NOTE · Skills Blocked by a Platform Scanner

On 2026-11-06, a platform scanner blocked registration of three mirrored skills. They were not installed on that platform.

| Skill | Scanner warning | Manual review |
|---|---|---|
| `deepxiv` | Appears to exfiltrate local secrets or credentials | Likely triggered by documentation of the `DEEPXIV_TOKEN` environment variable. The skill says not to read or display the token. |
| `paper-compile` | Asks to bypass permissions or escalate privileges | Likely triggered by an optional `sudo apt-get install texlive-full` instruction, which is not applicable to this Windows environment. |
| `paper-poster-html` | Appears to exfiltrate local secrets or credentials | Likely triggered by the design term “token,” not an authentication credential. |

We do not reword content merely to evade a scanner. Safe alternatives include a local `latexmk` and `scripts/validate_paper.py` workflow, the available literature-reading tools, and manual poster creation. Installation should proceed only after the user reviews and explicitly authorizes the skill.
