# TRANSPARENCY_LOG · 透明度日志

> 原则：**可信度靠公开，不靠承诺。** 本文件记录分身体系里"不顺利但被诚实处理"的事。

## 1. 被安全扫描器拦截的技能（拒绝绕过）

2026-11-06 将 ARIS 技能集注册到数字员工平台时，3 个技能被 daemon 安全扫描器拦截。
我们复核认为均为**关键词误报**，但**不改写内容骗过扫描器**，选择不安装并公开记录：

| 技能 | 扫描器警告 | 人工复核 | 替代方案 |
|---|---|---|---|
| deepxiv | 疑似外传本地凭据 | 正文仅描述 token 环境变量与 SDK 行为，且声明不读取/不回显 token | 文献阅读用 arxiv / alphaxiv / research-lit |
| paper-compile | 疑似提权 | 触发行为注释中的 `sudo apt-get`（目标机为 Windows，该行本就无用） | 用项目自有编译+独立校验管线 |
| paper-poster-html | 疑似外传本地凭据 | 触发词为排版术语 "design token" | 海报需求低频，暂缺 |

技能全文仍镜像在本仓库 `skills/`（含上述三个，供自行审查后本地使用），
平台侧安装状态以本日志为准。若未来启用：人工审核安装，或出具**逐行说明的透明修订稿**后重试。

## 2. 我们不开源什么（隐私设计清单）

- 分身的**长期记忆包**（含项目事实、协作史）——仅作者本地保存；
- 任何**密钥 / token / webhook**——员工包导出时显式排除 secrets；
- **未发表**的实验数据、论文稿、审稿状态与证据缺口清单；
- 可识别作者**真实身份/职务**的信息（公开人设为"ML/AI 初学者 + 遥感方向"）。

## 3. 误报与更正记录

- 曾把 PDF 低分辨率下的 `0.722` 误读为 `0.723`、把不同口径的训练时长误判为矛盾；
  均以生成脚本源码溯源复核后撤销质疑。教训：**对自家产物的质疑也要双实现复核**。

## 4. 已知局限（自我声明）

- 技能链中跨模型评审依赖外部后端；后端缺失时审计降级为单模型自审，结论强度下降且会明示；
- 蒸馏手册是压缩态，与全量记忆不一致时以全量为准；
- 本仓库技能镜像随上游 ARIS 演进，快照日期见 `clone-kit/MANIFEST.json`。

## 5. 未镜像技能清单（只列名，不镜像全文）

原则：**有许可声明才镜像**。以下 21 个技能在作者本地存在，但不进入公开 `skills/`，
在 `clone-kit/MANIFEST.json` 中以 `mirrored: false` 标记并附原因。

**上游未声明许可（16）**——公开再分发授权不明，仅列名：
analytics-data-analysis, chart-craft-plus, data-analysis-pro, data-extractor,
data-scientist, data-visualization, document-processor, excel,
excel-data-analysis-and-report-generation, excel-weekly-dashboard, finance-charts,
market-research-litiao, prompt-extractor, py-math-viz, report-generation, skill-file-converter

**平台内部（2）**——含平台管理面指令与受管启动器描述，不公开：
qoderwake-assistant, wake-dws-cli

**厂商发布（3）**——vendor 文档衍生，不代为再分发：
alibabacloud-dataworks-infra-manage, alibabacloud-dataworks-workspace-manage, alibabacloud-sls-query

若上游后续补充许可声明，按 `UPSTREAM_SYNC.md` 流程评估后策展入镜像，并在本节日志记录变更。

## 6. 许可证据不一致记录

- **Orchestra AI-Research-SKILLs 1.4.0**：README 徽章与仓库 LICENSE 文件均为 MIT
  （Copyright (c) 2025 Claude AI Research Skills Contributors），但 `package.json` 的
  `license` 字段写 ISC。本仓库以 **LICENSE 文件**为准镜像策展子集（12 个），
  并在 `skills/NOTICE.md` 保留 MIT 署名；若上游澄清为 ISC，将重新评估并记录。
