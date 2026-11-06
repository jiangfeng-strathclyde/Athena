# UPSTREAM_SYNC · 上游同步与策展流程

> `skills/` 镜像自 [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep)（MIT）。
> 本文件规定如何跟踪上游演进并把变更**策展**进本仓库：只镜像、不魔改、全程留痕。

## 快照基线

- 快照日期与清单：`clone-kit/MANIFEST.json`（含每个技能的 source / version / installUrl）。
- 镜像范围：上游顶层 87 个技能目录的 SKILL.md 原文 + 本仓库追加的"镜像说明"段（见 `skills/NOTICE.md`）。
- 支持文件（scripts/、references/、../shared-references/）**不随镜像分发**，使用时回上游解析。

## 同步流程（每月或上游大版本时）

1. **取差异**：拉上游最新 tag/commit，与 MANIFEST 的快照 commit 对比：
   `git -C <上游克隆> log --oneline <快照commit>..HEAD -- skills/`；
   列出 新增 / 删除 / 修改 的技能目录。
2. **分类**：
   - 修改：逐技能 diff SKILL.md；判断是否影响指令语义（语义变更→重跑安全自检清单；纯措辞→直接同步）；
   - 新增：按 `CONTRIBUTING.md` 的诚信自检清单过一遍，再决定是否策展入镜像；
   - 删除：从镜像移除并在 TRANSPARENCY_LOG 记录"上游移除"。
3. **安全扫描**：新/改内容提交平台或 CI 扫描；**被拦截不绕过**，按 TRANSPARENCY_LOG 流程公开记录。
4. **更新清单**：刷新 MANIFEST 的快照日期与 version 字段；README 徽章如含计数则同步。
5. **留痕提交**：commit message 固定前缀 `sync(aris): <快照commit短哈希> -> <新短哈希>`，
   body 列出 新增/删除/语义变更 三类清单。
6. **公告**：Discussions 发一条 sync 公告（模板可复用 skill-request 的结构）。

## 策展原则（为什么不是全自动镜像）

- 本仓库是**策展版**：保留对初学者有用的子集与中文导读，不做上游的完整 fork；
- 上游新增技能默认**不进**镜像，经 Discussion 需求或维护者评估后进入（需求驱动）；
- 任何对上游文本的追加段（如"镜像说明"）必须显式标注、不改变指令语义；
- 许可链不断：NOTICE 与 LICENSE 附录始终保留上游版权行。

## 非 ARIS 来源技能

社区贡献或自研技能进入 `skills/` 时：frontmatter 注明来源（原创/上游 URL），
许可必须 MIT 兼容；在 MANIFEST 中以 `source: community|original` 标记，与 `source: aris-mirror` 区分。
