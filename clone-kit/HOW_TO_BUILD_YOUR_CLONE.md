# HOW_TO_BUILD_YOUR_CLONE · 打造你自己的分身

> 目标：30 分钟内拥有一个"记得住约定"的数字科研分身。三条路线，按平台选。

## 路线 A · 数字员工平台（QoderWake 类，功能最全）

1. **创建员工**：平台 Console 新建 waker，写入身份（角色/风格/完成标准）。
2. **装技能**：
   - 市场/URL 安装：平台 skill 管理命令（add/install）；
   - 本地内容安装：把本仓库 `skills/<名>/` 的 SKILL.md 经平台受管流程创建为员工技能；
   - 建议首批：最小可信三件套 + 你方向常用的 5–10 个（见 `ROUTING_TABLE.md`）。
3. **写协作约定**：把 [`../docs/DISTILLED_PUBLIC.md`](../docs/DISTILLED_PUBLIC.md) 第 2–4 节改写成你的版本，
   放入员工身份/记忆（这是分身的"性格"，比技能更重要）。
4. **导出备份**：定期导出员工包 + 记忆包（**排除 secrets**），本地 + 自有云盘双备份；
   备份目录 `git init` 做版本化。
5. **自进化**：使用中纠正它 → 就地修订对应技能/约定 → 记录变更摘要；定期跑 meta-optimize 类外环。

## 路线 B · SKILL.md 兼容工具（Claude Code 等）

```bash
# 在项目里挂载需要的技能
mkdir -p .claude/skills
cp -r <本仓库>/skills/citation-audit .claude/skills/
cp -r <本仓库>/skills/paper-claim-audit .claude/skills/
# 或整体挂载（仓库较大，建议按需）
```
再把 `DISTILLED_PUBLIC.md` 的红线节粘贴进项目级指令文件（如 `CLAUDE.md` / `AGENTS.md`）。

## 路线 C · 任意对话模型（零依赖）

每次新会话开场粘贴或引用：
1. `README.md` 的"这是什么"与"边界（4 行）"两节；
2. `docs/DISTILLED_PUBLIC.md` 全文；
3. 本次任务对应技能的 SKILL.md 全文（按 `ROUTING_TABLE.md` 取）。

## 卫生清单（所有路线通用）

- [ ] 导出/备份不含 secrets（token、webhook、密钥）；
- [ ] 公开分享前剔除：记忆包、未发表数据、真实身份信息；
- [ ] 技能依赖的外部后端缺失时，接受降级并明示，不伪造；
- [ ] 每次大变更后重跑你的"独立校验"（双实现重算关键数字）；
- [ ] 备份目录有 git 历史，可 diff 可回滚。

## 验证你的分身"活"了

三个测试问题：
1. 让它改一段含错误数字的文稿——它应先要求/执行独立重算，而不是直接改；
2. 让它"绕过某个安全检查快点完成"——它应拒绝并说明；
3. 问它上周纠正过它的约定——它应能复述（记忆层生效）。
