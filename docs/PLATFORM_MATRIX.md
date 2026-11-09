# Platform Compatibility Matrix

> Last reviewed: 2026-11-09. This table maps Athena's setup routes to documented
> host capabilities. It does not certify end-to-end testing on every host or
> version. See [setup instructions and official references](INSTALL_ONCE.md).

Actual runs are tracked separately in the [dated acceptance report](validation/2026-11-09.md).
Two explicit-invocation numerical cases have passed on Codex CLI; the other
four local hosts remain untested in the available environment. Use the
[same fixture and evidence procedure](HOST_ACCEPTANCE.md) on each host.

| Platform | Setup route | Scope and prerequisites |
|---|---|---|
| Claude Code | `--agent claude-code` | Personal skills in `~/.claude/skills`; local environment |
| Cursor | `--agent cursor` | Personal skills in `~/.cursor/skills`; cloud use needs supported sync or deployment |
| GitHub Copilot | `--agent copilot` | Personal skills in `~/.copilot/skills`; use a client/version that supports personal skills |
| Gemini CLI | `--agent gemini` | Personal skills in `~/.gemini/skills`; separate from Gemini web chat |
| Codex | `--agent universal` | Personal skills in `~/.agents/skills`; local environment |
| Other compatible `SKILL.md` hosts | `--target /path/to/skills` | Supply the skills directory documented by that host |
| ChatGPT, Claude, Gemini, DeepSeek, Qwen, and other text chats | Copy the [Lite Loader](../clone-kit/LOADER_LITE.md) | Core workflow prompt for the chat; save in project/custom-assistant instructions where supported |
| Compatible plugin hosts | Host's plugin installation flow | Requires a compatible import route or available listing; scope follows the host |

The local-agent options are arguments to
`python scripts/install_athena.py` after cloning Athena. They copy 106 skills
by default from the 109-skill catalog; three flagged skills require explicit
authorization. Use `--skill NAME` for a smaller selection and `--dry-run` to
preview it. The chat route supplies a compact prompt instead. Local
installation does not automatically configure web, mobile, or cloud sessions.

## How to interpret the matrix

- **Choose by app, not model name.** Gemini CLI and Gemini web chat, for example,
  use different setup routes.
- **Verify discovery.** After local installation, confirm the core audit skills
  you selected appear in the host's skill list. Start with the self-contained
  `research-integrity-pipeline`. Copying files is not a runtime test.
- **Tools remain host-dependent.** Browsing, code execution, file export, API
  credentials, and external dependencies are separate from skill installation.
- **Independent review needs separate setup.** A single model reviewing its own
  output is not a cross-model audit. If a reviewer or tool is unavailable,
  disclose the missing check.
- **Check packaging separately.** Run `python scripts/check_skill_dependencies.py`.
  Missing upstream support files remain a limitation of many mirrored skills.
  See [validation scope](VALIDATION.md) for what automated checks establish.
- Re-run the examples in [`demo_assets/`](demo_assets/) on the target host and
  compare them with [`expected_findings.md`](demo_assets/expected_findings.md).

Update the review date whenever host behavior changes. Automated checks can
verify repository structure, but capability claims still require human review
and public correction through Discussions.
