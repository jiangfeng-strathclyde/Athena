# Install Athena once

Athena can stay available across conversations. The exact installation path
depends on whether the host supports plugins or user-level `SKILL.md` folders.

## The easiest option: automatic setup

Clone Athena, then configure the compatible agents detected on your computer:

```bash
git clone https://github.com/jiangfeng-strathclyde/Athena.git
cd Athena
python scripts/install_athena.py --auto
```

Automatic setup always installs to the portable `~/.agents/skills` directory.
It also installs to the native directory of any detected Claude Code, Cursor,
GitHub Copilot, or Gemini CLI installation. The native Cursor directory can be
synced to Cursor Cloud when Sync Skills is enabled.

## Choose one agent explicitly

| Agent | Command | User-level directory |
|---|---|---|
| Universal / Codex | `python scripts/install_athena.py --agent universal` | `~/.agents/skills` |
| Claude Code | `python scripts/install_athena.py --agent claude-code` | `~/.claude/skills` |
| Cursor | `python scripts/install_athena.py --agent cursor` | `~/.cursor/skills` |
| GitHub Copilot | `python scripts/install_athena.py --agent copilot` | `~/.copilot/skills` |
| Gemini CLI | `python scripts/install_athena.py --agent gemini` | `~/.gemini/skills` |

The previous `--agent codex` command is retained as a backward-compatible alias
for the universal directory. Cursor, Copilot, and Gemini CLI also recognize
that portable directory for local sessions.

For another compatible host, provide its skills directory explicitly:

```bash
python scripts/install_athena.py --target /path/to/user/skills
```

Start a new agent session after installation. From then on, describe the goal
normally, for example: `Audit the numerical claims in this draft.` The agent
sees each skill's name and description and loads the detailed instructions only
when the request matches.

The installer stops instead of overwriting same-named skills. To update an
earlier installation intentionally, repeat the same command with `--force`.

## ChatGPT and Codex plugin package

This repository is also a portable skills-only plugin. Its entry points are
`plugin.json` and `.codex-plugin/plugin.json`; `onboarding/SKILL.md` provides
first-run setup. Once Athena is installed or published through a supported
plugin directory, one installation makes its skills available to future chats.

## Hosts without persistent skills

An ordinary chat model cannot retain repository capabilities globally unless
its host provides plugins, custom agents, or persistent instructions. Use the
self-contained [Lite Loader](../clone-kit/LOADER_LITE.md) on those hosts. It is
a compatibility fallback, not the recommended Athena experience.

## What "all skills available" means

Athena does not paste 108 full instruction files into every prompt. The host
keeps their small metadata available, selects relevant skills for the current
goal, and loads only those instructions. This preserves context space and
reduces conflicts while removing the need to invoke Athena on every turn.
