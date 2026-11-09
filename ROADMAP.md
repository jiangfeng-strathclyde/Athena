# ROADMAP · 分身还能长成什么样

## 近期（next）

- [x] **克隆卡徽章**：一键生成"我的分身卡"（技能数 / 协议版本 / 诚信审计开关 / 快照日期）的 shields 组合或 SVG。
- [x] **技能请求队列**：Discussion 模板 `skill-request` 收集需求，按月 batching 策展进 `skills/`（队列见 `clone-kit/SKILL_QUEUE.md`）。
- [x] **双语蒸馏手册**：`DISTILLED_PUBLIC.md` 完整英文化（现为中英混排）。
- [x] **最小可信集 quickstart**：三件套审计（citation / claim / experiment-audit）的 10 分钟上手示例（见 `docs/EXAMPLES.md`）。
- [x] **多平台适配验证矩阵**：QoderWake / Claude Code / Codex / 纯对话模型 四列对照表（见 `docs/PLATFORM_MATRIX.md`）。
- [x] **外链周报**：周 cron 探测 README/docs 外链存活（`.github/workflows/external-links-weekly.yml`）。

## 中期

- [ ] **知识库云化**：把公开方法论层写入可检索知识库，分身协议第 2 步支持"云端读取"。
- [ ] **视频演示**：3 分钟录屏——从空会话到加载分身完成一次带审计的改稿（脚本见 `docs/DEMO_SCRIPT.md`）。
- [ ] **上游同步机器人**：跟踪 ARIS 上游新增技能，自动开 PR 提议策展（人工合并）。

## 长期

- [ ] **分身联邦**：不同方向的分身互相加载对方的路由表子集（协议 v2：命名空间化技能路由）。
- [ ] **可复现科研工件标准**：把"生成-校验分离 + 三重审计"沉淀为投稿级 checklist 模板，供期刊/会议复用。

## 不做（anti-roadmap）

- 不做"全自动发论文"流水线、不做"一键出 paper"：科研的乐趣与训练都在过程里，我们降低门槛但不替代思考（见 `docs/POSITIONING.md`）；
- 不收集使用者数据；不做云端托管他人记忆。
