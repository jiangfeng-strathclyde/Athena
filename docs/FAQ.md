# FAQ · 读者最常问的 10 个问题

## 1. 这和“一包提示词”有什么区别？

提示词是**一次性的话**；这里是**可加载的行为系统**：红线（什么绝不能做）、协作算法（先审后改、列代价再动手）、技能路由（什么场景用什么工具）、以及一条把“生成”和“校验”分开的审计管线。提示词会被模型遗忘或稀释，协议文件每次任务前重新加载，且红线可被检验（见 [`demo_assets/`](demo_assets/)）。

## 2. 和 Claude Code 的 skills 是什么关系？

`skills/` 就是标准 SKILL.md 格式，Claude Code 等兼容工具可直接挂载。本仓库额外提供两样东西：**路由表**（87 个技能按 17 类场景组织，不用死记名字）和**行为手册**（`DISTILLED_PUBLIC.md`），后者才是“分身”的性格来源。

## 3. 要钱吗？要账号吗？

不要。核心路径（读三个文件 + 按需读技能全文）零依赖、零费用。标 `(ext)` 的技能需要你自己的外部 key/账号（GPU 云、搜索 API 等），缺失时按协议跳过或报错，不会伪造结果。

## 4. 安全吗？会不会偷我的数据？

仓库不含任何密钥、token、webhook；技能里的外部调用只在该技能被触发时发生，且都在技能正文里写明。我们不收集使用者数据，也不托管他人记忆（见 [`ROADMAP.md`](../ROADMAP.md) 的 anti-roadmap）。

## 5. 记忆层为什么不开源？

记忆里有真实项目事实、协作史和口径约定，属于私人上下文，公开它会泄露未发表信息。公开的是**可迁移的方法论层**；这也让“公开版会诚实说自己没有你的记忆”成为一个可检验的行为（README 的三个测试之一）。

## 6. 跨模型审稿后端缺失时会怎样？

审计类技能默认调用跨模型后端做零上下文复核。后端缺失时**降级为单模型自审并明示**，结论强度下降但不伪装。仓库里 2026-11-06 那次真实审计就是这么跑的，降级声明写在 [`audit_2026-11-06_run01/CITATION_AUDIT.md`](demo_assets/audit_2026-11-06_run01/CITATION_AUDIT.md) 文首。

## 7. 被安全扫描器拦截的技能，为什么不改改内容绕过去？

因为可信度比可用性重要。改写内容骗过扫描器等于把安全机制变成形式审查。我们选择不安装、公开记录、给出替代方案（[`TRANSPARENCY_LOG.md`](TRANSPARENCY_LOG.md)）。技能全文仍镜像在仓库里，供你自行审查后本地使用。

## 8. 和上游 ARIS 是什么关系？会被上游变动打乱吗？

`skills/` 镜像自 [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep)（MIT），保留版权署名；本仓库只做策展与中文导读。同步流程见 [`UPSTREAM_SYNC.md`](UPSTREAM_SYNC.md)：只镜像不魔改、语义变更重过自检、全程留痕。

## 9. 我能商用吗？

自有内容 MIT，可商用；`skills/` 镜像部分遵循上游 MIT 条款（保留署名）。商用时请自行确认你调用的外部服务（GPU 云、API）的条款。

## 10. 怎么贡献 / 怎么要新技能？

- 要新技能或报坑：开 [Discussion](https://github.com/jiangfeng-strathclyde/Thats-me/discussions)（模板：`skill-request`、`clone-show-and-tell`）；
- 提交技能：读 [`CONTRIBUTING.md`](../CONTRIBUTING.md)，含 frontmatter 规范与诚信自检清单；
- 想打造自己的分身：[`clone-kit/HOW_TO_BUILD_YOUR_CLONE.md`](../clone-kit/HOW_TO_BUILD_YOUR_CLONE.md)。
