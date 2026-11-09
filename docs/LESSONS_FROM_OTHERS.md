# LESSONS_FROM_OTHERS · 同类项目逐个调研与可吸收经验

> 快照：2026-11-09。调研范围：本地收集的约 45 个开源自主科研框架、技能库与相关平台，
> 逐个读 README 与关键架构文件（编排入口、技能/prompt 格式、验证环节）。
> 原则：**只调研机制、不复制内容**——本页所有"可吸收"均指做法与思路；
> 任何文本/代码引入都须先过 [`skills/NOTICE.md`](../skills/NOTICE.md) 的许可门。
> 定位不变：我们不做一键出 paper（见 [`POSITIONING.md`](POSITIONING.md)）。

## 一、五条横向结论（对我们最有价值）

### 1. 把诚实变成机制，而不是口号

我们的红线（不虚构、数字可重算）在最好的几个项目里都有"可执行化"的对应物：

- **ScienceClaw**（MIT）：零幻觉规则措辞最硬——"每条引用必须来自当前对话的工具返回；
  数据库没返回就不能引；查不到就报告空结果，**禁止回退到训练知识**"；并有"反过早结论协议"：
  按任务类型规定最低工具调用数（quick=5 / survey=30 / review=60），收尾前必须过 7 项 checklist。
- **AutoResearchClaw**（MIT）：VerifiedRegistry——论文中每个数字必须能对应到真实实验产物，
  未验证数字被强制清洗；4 层引用核验（arXiv→CrossRef→S2→LLM 相关性），幻觉引用自动删除。
- **codex-autoresearch**（MIT）：Verify/Guard 双门——Verify 检查指标是否改善，Guard 检查
  是否弄坏了别的，guard 文件永不可改，防"数值变好但机制不对"的假成功。
- **OpenScholar**（Apache-2.0）：回答逐句挂引用、引用可回溯；自反馈循环
  （生成→自评缺证据→定向补检索→修订）。

**吸收方向**：检索/综述类技能加"最低检索源数 + 收尾 checklist"；"查不到就显式报告空结果"
的措辞进红线文档；评估类技能推广"评分公式完全显式、参数可定制"（PaperClaw 的正面范例）。

### 2. 人机确认点的分级设计（对初学者默认保守）

- AutoResearchClaw：固定管线中设 3 个人工审批 gate，拒绝即回滚；
- codex-autoresearch：启动前 Wizard 1–5 轮确认目标/指标/verify 命令；
- EvoScientist（Apache-2.0）：shell 命令默认人工批准 + 命令前缀白名单 + 会话级"本次全批"；
- oh-my-claudecode（MIT）：技能 frontmatter 加 `level: 1-4` 标注自主度。

**吸收方向**：我们的"先给代价清单、等点单再执行"已经是同一族做法；可进一步在
ROUTING_TABLE 的组装规则里按操作代价标注默认审批级别，高成本操作强制低自主度。

### 3. 新手引导层：比我们做得好的地方

- **claude-howto**（MIT）：LEARNING-ROADMAP 按水平分级 + "Find Your Level" 入口 + 单页 QUICK_REFERENCE；
- **research-skills**（无 LICENSE，只可借鉴做法）：README 顶部"技能/描述/触发词"三列表，新手不用点进目录；
- **academic-ai-prompt**（MIT）：填空题式模板（[年级][导师方向][想避免的方向]），对不会写代码的学生极友好；
- **DeepTutor**（Apache-2.0）：错题本（Question Notebook）、读完自测三题、持久 TutorBot——受众与我们完全重合；
- **autoresearch**（Karpathy 原型）：固定 5 分钟预算 + 单一可比指标 + "只许改一个文件"，
  是让本科生理解"公平比较、diff 可审"的最小教材。

**吸收方向**：START_HERE 已是同一方向；可补"信息采集填空模板"进路由表前置步骤、
给文献技能加"读完自测三题"环节。

### 4. 技能组织与状态管理的工程做法

- **codex-autoresearch**：SKILL.md + `references/` 按需加载（按模式只加载所需分册，控 token）；
- **AI-Research-SKILLs / Orchestra**（MIT）：frontmatter 加 `tags`/`dependencies` 字段；
  编排技能维护 `research-state.yaml` + `findings.md` 跨会话状态；`to_human/` 目录定期产出人类可读进度报告；
- **DrClaw**（README 称 MIT，无 LICENSE 文件）：MEMORY.md（可重写的长期记忆）与
  HISTORY.md（append-only 审计日志）分离；工具型子代理无状态 + 硬性迭代上限 + 必须回报；
- **ResearchClaw**（Apache-2.0）：claim/evidence 图——每个论断挂证据（论文/笔记/实验/引用）；
  缺口自动生成补救任务；README 坦率写"still incomplete + 最大缺口清单"；
- **MedgeClaw**（README 称 MIT，无 LICENSE 文件）：state.json + 单 HTML 轮询的零依赖进度仪表盘；
- **PaperClaw**（README 称 MIT，无 LICENSE 文件）："元技能生成领域 Agent"——访谈式收集领域知识
  再脚手架出一个带 5 技能和定时任务的论文追踪 Agent；去重索引 + 文件锁的状态文件设计。

**吸收方向**：108 技能的大技能可拆 `references/` 按需加载；长链技能约定统一状态文件；
"可重写记忆 vs 只追加日志"的分离写进协作约定。

### 5. 许可卫生与期望管理（反面教材同样有用）

- 多个项目（DrClaw / PaperClaw / MedgeClaw / Auto-Resubmit / autoresearch / research-skills /
  Memento-Skills）**README 声称 MIT 但仓库里没有 LICENSE 文件**——法律上默认保留所有权利。
  我们只借鉴其做法，不复制文本；这也是我们 MANIFEST 坚持"镜像必须有明确宽松许可声明"的原因；
- CitationClaw 是 CC BY-NC 4.0（非商用）；ipaperview 是自定义条款——同样只调研不引入；
- Auto-Resubmit 的 README 把"哪些情况会失败、需要手修"写在最显眼处，DrClaw 明说
  "不能帮你拿博士学位"——期望管理写法的范本，与我们"边界（4 行）"同族。

## 二、逐项目速览表

许可列：✅=有 LICENSE 文件　⚠️=README 声称但无文件　❌=无声明。
"引入"列一律为**否**：本页项目均只调研、不镜像（我们的镜像来源与理由见
[`TRANSPARENCY_LOG.md`](TRANSPARENCY_LOG.md) §5）。

### 自主科研框架

| 项目 | 一句话 | 许可 | 最值得借鉴的一点 |
|---|---|---|---|
| AutoResearchClaw | 23 阶段"话题进论文出"全自动管线 | ✅ MIT | VerifiedRegistry：数字必须溯源到实验产物 |
| ScienceClaw | 285 技能 + 629 行 SCIENCE.md 协议 | ✅ MIT | 最低工具调用数 + 反过早结论 checklist |
| codex-autoresearch | 目标驱动无人值守迭代循环 | ✅ MIT | Verify/Guard 双门验证 |
| autoresearch | Karpathy 极简过夜实验原型 | ⚠️ | 固定预算 + 单一可比指标 |
| EvoScientist | LangChain DeepAgents 自进化科学家 | ✅ Apache-2.0 | 分级审批 + 命令白名单 |
| ResearchClaw | Local-first "Research OS" | ✅ Apache-2.0 | claim/evidence 图 |
| ClawPhD | 论文→图表/海报/评审 Agent | ✅ MIT | 用真实历史录用结果校准评审提示词 |
| DrClaw | 微内核多智能体"龙虾实验室" | ⚠️ | MEMORY/HISTORY 双语义状态分离 |
| dr-claw (OpenLAIR) | TS 全栈科研工作台（与上一行非同一项目） | ✅ GPL/AGPL | 对话式 pipeline planner + 固定产物目录 |
| PaperClaw | 元技能生成领域论文追踪 Agent | ⚠️ | 评分公式完全显式、参数可定制 |
| MedgeClaw | IM→Docker 生信分析助手 | ⚠️ | state.json + 单 HTML 零依赖仪表盘 |
| CitationClaw | 引用画像引擎 | ✅ CC BY-NC | 三档成本模式（Basic/Advanced/Full）先选再跑 |
| Auto-Resubmit | 纯规则 LaTeX 模板迁移 | ❌ | content_audit.json + 失败边界写在最显眼处 |

### 技能库 / Prompt 合集

| 项目 | 一句话 | 许可 | 最值得借鉴的一点 |
|---|---|---|---|
| AI-Research-SKILLs (Orchestra) | 91 技能全生命周期库 | ✅ MIT | frontmatter tags/dependencies + to_human/ 进度汇报 |
| Awesome-Scientific-Skills | 技能策展索引 + 质量评估器 | ✅ MIT | 24 分制技能质量 rubric（可做成入库 QC） |
| scientific-agent-skills (K-Dense) | 133 技能 + 100 科学数据库 | ✅ MIT | scan_skills.py 仓库级技能校验进 CI |
| claude-scientific-writer | 先检索后写作的写作工具 | ✅ MIT | 逐 claim 可验证引用的核对流程 |
| research-skills | 3 技能迷你合集 | ❌ | README"技能/描述/触发词"三列表 |
| Memento-Skills | 自进化 agent 框架 | ❌ | 技能 utility score + 失败即修订 |
| academic-ai-prompt | 中文研究生 89+ prompt 合集 | ✅ MIT | 填空题式信息采集模板 |
| claude-howto | Claude Code 教学库（377 md） | ✅ MIT | 分级学习路线图 + 单页速查 |
| oh-my-claudecode | CC 重度增强框架 | ✅ MIT | level 1-4 自主度字段 + `<Use_When>` 反例 |
| oh-my-codex | Codex 工作流层 | ✅ MIT | missions/ 任务剧本作为一等公民 |
| system_prompts_leaks | 商业产品系统提示词泄露集 | ⚠️ | 仅结构参考：身份→工具规则→输出约束→红线 |

### 平台 / 单点工具

| 项目 | 一句话 | 许可 | 最值得借鉴的一点 |
|---|---|---|---|
| OpenScholar (AllenAI) | 检索增强科学问答 LM | ✅ Apache-2.0 | 逐句挂引用 + 自反馈补检索 |
| DeepTutor (HKUDS) | Agent 原生个性化辅导平台 | ✅ Apache-2.0 | 错题本 + 读完自测；随仓库发 SKILL.md |
| onyx (原 Danswer) | 企业级 Agentic RAG 应用层 | ✅ MIT | Deep Research 计划→多轮检索→汇总报告结构 |
| OpenVitamin | 本地优先 AI 平台 | ✅ Apache-2.0 | Intent Rules + Skill Discovery 的路由产品化 |
| hermes-agent (Nous) | 自我改进通用 Agent | ✅ MIT | 任务后自动沉淀技能；对齐 agentskills.io 标准 |
| paperclip | 多 Agent"零人公司"编排器 | ✅ MIT | 预算/成本仪表盘呼应"代价清单" |
| ppt-master | 文档→可编辑 PPTX 技能 | ✅ MIT | examples/ 端到端样例 + 多 Agent 入口适配 |
| forgecode | Rust 终端 AI 编码环境 | ✅ Apache-2.0 | 技能配置全局/项目/会话分层覆盖 |
| ipaperview | arXiv 浏览+可视化网站 | ❌ 自定义 | 文献计量模板化图表（趋势/共现） |
| LLM Wiki（哈希名目录） | 持久 Markdown 知识库理念文 | ❌ | 知识编译一次持续更新，矛盾点显式标记 |
| sherlock | 用户名 OSINT 工具 | ✅ MIT | 数据文件驱动规则、代码只做引擎 |
| gallery (Google) | 手机端本地 LLM 体验 App | ✅ Apache-2.0 | 模型白名单/许可过滤文件 |

### 与科研无关（一句话排除）

markitdown（文件转 Markdown 基建）· timesfm（时序模型）· VibeVoice（语音 TTS）·
nvim-treesitter（编辑器插件）· tdesktop（Telegram 客户端）· openscreen（屏幕录制）·
LiteRT-LM（端侧推理框架）· xiaohongshu_import（内部语料库，非项目）。

## 三、明确不吸收的（定位对照）

| 做法 | 谁在用 | 为什么我们不 |
|---|---|---|
| 全自动"话题进论文出" | AutoResearchClaw 等 | 与使命冲突：初学者要亲手走完闭环才有成长；我们保留 gate 但默认人在环上 |
| 运行时自动写新技能并即时生效 | ScienceClaw / Memento / hermes | 未经审查的自进化技能会破坏可审计性；我们走"月策展 + PR + 诚信自检"（CONTRIBUTING） |
| 商业提示词文本复用 | system_prompts_leaks | 授权状态存疑，只看结构不抄内容 |
| 无 LICENSE 项目的代码/文本 | 上表 ⚠️/❌ 项 | 法律上默认保留所有权利；只借鉴公开描述的做法 |

## 四、落到本仓库的行动清单（候选，按代价排序）

1. **低成本**：检索/综述类技能补"最低检索源数 + 收尾 checklist + 空结果显式报告"措辞；
   START_HERE 加"读完自测三题"环节；
2. **中成本**：入库 QC 脚本（借鉴 24 分 rubric + scan_skills 思路）进 CI；
   ROUTING_TABLE 组装规则按操作代价标注默认审批级别；
3. **高成本（暂缓）**：claim/evidence 图、技能 utility score、references/ 按需加载改造——
   等技能库规模和社区反馈到位再做。

以上任何一项动手前，照例先给方案和代价清单，等维护者点单。
