# PLATFORM_MATRIX · 平台适配矩阵

> 快照日期：2026-11-06。各工具能力随版本变化，**以各工具当前官方文档为准**；
> 本表只描述“加载本分身”这件事在不同宿主上的落地形态与降级行为。
> 记号：✅ 原生支持　🟡 需配置/降级　⬜ 不适用（按协议明示，不伪造）

| 能力 | QoderWake 数字员工 | Claude Code | Codex 类 CLI | 任意对话模型（零依赖） |
|---|---|---|---|---|
| 加载协议（读 3 文件） | ✅ 身份/记忆内置 | ✅ `CLAUDE.md` + 会话引用 | 🟡 `AGENTS.md`；SKILL.md 自动触发视版本 | ✅ 开场粘贴三段 |
| 87 个 SKILL.md 技能 | ✅ 平台技能目录 | ✅ `.claude/skills/` | 🟡 视版本：skills 目录或转写为 `AGENTS.md` 指令 | 🟡 按路由表手动读全文 |
| 场景路由表 | ✅ | ✅ | ✅ | ✅ |
| 诚信三件套（citation / claim / experiment-audit） | ✅ | ✅ | ✅ | 🟡 可用，但无跨模型后端时降级为单模型自审并明示 |
| 跨模型审稿后端（auto-review-loop 等，标 ext） | 🟡 需配置 codex MCP | 🟡 需配置 | 🟡 需配置 | ⬜ 不可用 → 技能按声明跳过或报错，**不伪造审计结论** |
| 外部 API 技能（vast-gpu / modal / qzcli / ext 搜索） | 🟡 需 key/账号 | 🟡 需 key/账号 | 🟡 需 key/账号 | 🟡 需 key/账号 |
| 记忆层（项目事实、纠正史） | ✅ 平台记忆 | 🟡 项目文件（`CLAUDE.md`）承载 | 🟡 `AGENTS.md` 承载 | ⬜ 公开版本来不含记忆；会话内临时约定需每次重述 |
| 生成-校验分离管线（脚本） | ✅ | ✅ | ✅ | ✅（纯脚本，与宿主无关） |
| 员工包一键复活 | ✅ `--template-zip` | ⬜ | ⬜ | ⬜ |

## 怎么读这张表

- **零依赖列永远是兜底**：哪怕宿主什么都不支持，读三个文件 + 手动打开技能全文，红线依然生效；
- **🟡 不是“坏了”**：是“需要你做一步配置”或“按协议降级并明示”；
- **⬜ 是设计**：公开分身不含记忆层；跨模型后端缺失时审计降级，这两件事都在
  [`TRANSPARENCY_LOG.md`](TRANSPARENCY_LOG.md) 的自我声明里；
- 想验证某格：用 [`demo_assets/`](demo_assets/) 的三个演示在该宿主上跑一遍，
  对照 [`expected_findings.md`](demo_assets/expected_findings.md)。

## 维护约定

宿主能力变化时更新本表并在文首改快照日期；`scripts/check_repo_consistency.py`
不校验本表（能力声明无法机器验证），靠人工 + Discussion 报坑。
