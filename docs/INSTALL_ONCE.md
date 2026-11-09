# Set up Athena on your platform

Local agents can install Athena's research skill collection. Web and mobile chats
can use its self-contained research prompt. Choose the route for your actual
app: Claude Code and Gemini CLI are distinct from Claude and Gemini web chat.

- [Local agents](#local-agents): Claude Code, Cursor, GitHub Copilot, Gemini CLI,
  Codex, and other compatible `SKILL.md` hosts.
- [Web and mobile chats](#web-and-mobile-chats): ChatGPT, Claude, Gemini,
  DeepSeek, Qwen, and other apps that accept text prompts.
- [Plugin-capable hosts](#plugin-capable-hosts): use the packaged plugin when
  your host provides a compatible installation route.

## Local agents

Install Git, Python 3.10 or newer, and the agent you intend to use. Run the commands below
in Windows PowerShell or a macOS/Linux terminal. Use `py -3` on Windows or
`python3` on macOS/Linux in place of `python` if that is your Python 3 command.
The installer uses Python's standard library; it requires no pip packages.

### Automatic setup

Clone Athena, then configure the compatible agents detected on your computer:

```bash
git clone https://github.com/jiangfeng-strathclyde/Athena.git
cd Athena
python scripts/install_athena.py --auto
```

Automatic setup always installs to the portable `~/.agents/skills` directory.
It also installs to `~/.claude/skills` when the `claude` command is on PATH or
the `.claude` configuration directory exists in your home folder. Cursor,
Copilot, and Gemini CLI can use the shared directory, so automatic setup does
not also create native copies for them. It does not install those apps or
configure browser accounts. Choose a native directory explicitly below if
your client or sync workflow needs it. Previously installed native copies are
left untouched; use one active location per host to avoid stale duplicates.

The catalog contains 109 skills. The default install selects 106, excluding
`deepxiv`, `paper-compile`, and `paper-poster-html`. Review
[`BLOCKED_NOTE.md`](../skills/BLOCKED_NOTE.md) before explicitly authorizing any
of those skills; a scanner warning is not a confirmed diagnosis of harm.

### Choose one agent explicitly

| Agent | Command | User-level directory |
|---|---|---|
| Claude Code | `python scripts/install_athena.py --agent claude-code` | `~/.claude/skills` |
| Cursor | `python scripts/install_athena.py --agent cursor` | `~/.cursor/skills` |
| GitHub Copilot | `python scripts/install_athena.py --agent copilot` | `~/.copilot/skills` |
| Gemini CLI | `python scripts/install_athena.py --agent gemini` | `~/.gemini/skills` |
| Codex / shared local directory | `python scripts/install_athena.py --agent universal` | `~/.agents/skills` |

Here `~` means your OS user home directory. For example, `~/.cursor/skills`
is typically `C:\Users\<username>\.cursor\skills` on Windows,
`/Users/<username>/.cursor/skills` on macOS, or
`/home/<username>/.cursor/skills` on Linux. The installer resolves this path
for you. Run it in the environment where the agent runs; Windows, WSL,
containers, and remote machines can have different home directories.

The previous `--agent codex` command is retained as a backward-compatible alias
for the universal directory. Cursor, Copilot, and Gemini CLI also recognize
that portable directory for local sessions.

For another compatible host, provide its skills directory explicitly:

```bash
python scripts/install_athena.py --target /path/to/user/skills
```

### Verify and use

Start a new agent session after installation. Check the host's skill list or
customization settings for `research-integrity-pipeline` and any other skills
you selected. Gemini CLI also provides `/skills list`. If skills are
missing, check the installer's reported destination against the active agent's
user and environment, then confirm that skills are enabled in that host.

From then on, describe the goal
normally, for example: `Audit the numerical claims in this draft.` The agent
sees each skill's name and description and loads the detailed instructions only
when the request matches.

To start with one self-contained workflow instead of the full default selection:

```bash
python scripts/install_athena.py --agent universal --skill research-integrity-pipeline --strict-packaging --dry-run
python scripts/install_athena.py --agent universal --skill research-integrity-pipeline --strict-packaging
```

Repeat `--skill NAME` to choose multiple skills. The entry point works from
provided sources and available host tools; it does not require root-level
Athena guides or private files. It reports unavailable checks explicitly.
Its bundled Python helper recomputes paired CSV results without third-party
packages; see the skill's instructions for the input schema and limits.

Every installation checks the selected skills for known static packaging
gaps and prints affected names. `--strict-packaging` stops before writing if
it finds any. Without that flag, findings are warnings so that users who have
reviewed and supplied upstream prerequisites can still install the catalog.
Passing the check does not establish runtime or scientific readiness.

To authorize a flagged skill after reviewing it, select and authorize it by
name, for example:

```bash
python scripts/install_athena.py --agent universal --skill paper-compile --allow-flagged paper-compile --dry-run
```

Remove `--dry-run` only when ready to install. This flag does not bypass any
host security check. Excluded or unselected skills from earlier installations
are not deleted; the installer warns about existing unselected flagged copies.

### Update an existing installation

Update your Athena checkout, then repeat your original install command with
`--force`. For example, for Cursor:

```bash
git pull --ff-only
python scripts/install_athena.py --agent cursor --force
```

Run these commands from the Athena checkout. `--force` stages the selected
skills before replacing anything and retains previous versions in the printed
`.athena-update-<id>/backup` directory beside the skills directory. Unrelated
skills are left untouched. Without that flag, the installer stops on conflicts.
Use `--dry-run --force` first to inspect the plan. Restart the agent after updating.

If a copy fails, existing skills remain untouched. If a replacement fails,
the installer attempts rollback for that destination. An incomplete rollback
prints the recovery directory and leaves its files in place. Multiple targets
are prechecked together but updated separately: an earlier completed target
remains updated if a later target fails. Do not run concurrent installers or
edit installed skills during an update. Abrupt process termination or power
loss requires manual inspection of the retained working directory.

To recover an old version, close the agent, move the current same-named skill
to a separate recovery location, and move its folder from the printed backup
directory into the skills directory. Confirm its contents before restarting.
Backups are not deleted automatically; remove only the specific backup folder
after verifying the update. Never target the checkout, its ancestors, a drive
root, or your home directory as the skills directory.

### Local, remote, and cloud scope

User-level installation applies to the current OS user in that environment.
For remote or cloud sessions, use the host's supported sync, project-skill,
or deployment mechanism. For example, Cursor offers Sync Skills for Cloud
Agents for `~/.cursor/skills`; the shared `~/.agents/skills` directory is not
automatically synced. See the official host documentation linked below.

## Web and mobile chats

For a text-only starting point in ChatGPT, Claude, Gemini, DeepSeek, Qwen, or
another chat app:

1. Open the [Lite Loader](../clone-kit/LOADER_LITE.md).
2. Copy the text inside its code block.
3. Replace `<your goal>` with a concrete task and paste it into a new chat.
4. Supply the relevant draft, data, or excerpts using the app's available tools.

The loader contains the core research workflow and evidence rules. It does
not install the full skill library or give the app new tools. If browsing or
code execution is unavailable, provide sources or computed outputs yourself
and ask the assistant to label what it could not verify.

For reuse, save the prompt in project or custom-assistant instructions when
your host supports them, then start future work inside that project or
assistant. Otherwise, paste it in each new conversation. A saved prompt's
scope depends on the host; it need not apply to every chat in your account.

## Plugin-capable hosts

This repository is also a portable skills-only plugin. Its entry points are
`plugin.json` and `.codex-plugin/plugin.json`; `onboarding/SKILL.md` provides
first-run setup. Use your host's documented plugin import or marketplace
installation process if it supports this format, then enable Athena and check
its skill list in a new session. The manifests alone do not establish an
available public marketplace listing. If your app has no compatible install
option, use the local-agent or chat route above.

## What "all skills available" means

The local installer copies the selected folders (106 by default from a catalog
of 109). A compatible host discovers
skill metadata and loads relevant instructions on demand, rather than pasting
all instruction files into every prompt. Actual discovery depends on the
host's version, configuration, and limits. Skills that require external tools,
credentials, or additional files still need those prerequisites. Many mirrored
procedures depend on unbundled upstream scripts and shared references.

Inspect the packaging report before relying on a specialized workflow:

```bash
python scripts/check_skill_dependencies.py
python scripts/check_skill_dependencies.py --skill citation-audit --json
python scripts/check_skill_dependencies.py --skill research-integrity-pipeline --strict
```

The first two commands report findings without failing; `--strict` exits with
an error when packaging gaps are detected. This static scan does not verify
tool access, credentials, model behavior, or all paths embedded in code.
See [`VALIDATION.md`](VALIDATION.md) for the verification boundary.

## Host documentation

Directory conventions checked on 2026-11-09. These references describe host
support, not an end-to-end Athena test on every platform:

- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Cursor skills and cloud sync](https://cursor.com/docs/skills)
- [GitHub Copilot agent skills](https://docs.github.com/en/copilot/concepts/customizations/agent-skills)
- [Gemini CLI skills](https://geminicli.com/docs/cli/skills/)
- [OpenAI skills and Codex local directories](https://learn.chatgpt.com/docs/build-skills)
