# CONTRIBUTING · 技能提交与社区规范

欢迎贡献！本仓库收两类贡献：**新技能**与**分身协议/文档改进**。

## 三分钟加一个技能（自己用或贡献都适用）

1. 复制模板：`cp clone-kit/SKILL_TEMPLATE.md skills/<my-skill>/SKILL.md`；
2. 填四块：触发场景 / 流程 / 输出物 / 红线（模板里有占位与示例）；
3. 在 frontmatter 写 `license: MIT`（原创）或注明上游出处；
4. 想让它被“目标路由”选中：在 `clone-kit/ROUTING_TABLE.md` 对应场景行加一个名字；
5. 自用到此为止；要贡献就开 PR，并按下面清单勾选。

## 提交技能（SKILL.md 格式）

1. 目录结构：`skills/<skill-name>/SKILL.md`（可带 `scripts/`、`references/` 子目录）。
2. frontmatter 必备：
   ```yaml
   ---
   name: <kebab-case-name>
   description: <一句话：何时使用 + 触发词；≤1024 字符>
   ---
   ```
3. **诚信自检清单**（PR 描述中逐条勾选）：
   - [ ] 技能不要求读取/回显密钥、token、webhook；确需凭据时用环境变量引用并声明；
   - [ ] 不含提权/绕过权限指令（sudo、--no-verify、关闭守卫等）；确需管理员操作时写明由用户自行执行；
   - [ ] 外部网络调用仅指向公开学术/文档 API，且失败时声明跳过或报错，不伪造结果；
   - [ ] 产出数字的步骤附带"独立重算/校验"说明，或声明依赖上游校验；
   - [ ] 许可兼容 MIT：原创或注明上游出处（含版权行）。
4. 命名不与前缀冲突；描述里写清触发词，方便路由。
5. 安全扫描：贡献将被平台/CI 安全扫描；**被拦截不绕过**——按
   [`docs/TRANSPARENCY_LOG.md`](docs/TRANSPARENCY_LOG.md) 的流程公开记录并讨论。

## 文档/协议改进

- 小改直接 PR；改 `docs/CLONE_PROTOCOL.md` 的版本语义需 bump 版本号并在 PR 说明兼容性。
- 蒸馏手册公开版**不得**引入：真实身份、未发表数据、私有记忆内容。

## 社区行为

- 对初学者友好：解释"为什么"，不甩术语；
- 展示你的分身请发 Discussion（模板 `clone-show-and-tell`）；
- 踩坑上报请附最小复现与期望行为。

## 许可

提交即同意以 MIT 发布（与仓库一致）；含上游内容的须保留上游版权与许可声明。
