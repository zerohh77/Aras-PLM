# Aras PLM Engineering Skill

面向 Aras Innovator 安装、建模、开发、集成、安全审查和故障诊断的可执行 Agent Skill。

该 Skill 将 Aras Innovator 2024 Release 官方安装指南作为最高优先级依据，并把第三方文章、开发讲义和经验总结作为次级解释材料。遇到冲突时，它会明确标注证据层级、以官方资料为准，并隔离经典客户端或私有 API 兼容债务。

## 能做什么

- 提取 Aras 的核心数据流、模块依赖关系和元数据驱动设计原则
- 指导 ItemType、RelationshipType、AML/IOM、Method、Server Event、CUI、Vault 等开发
- 强制执行权限、事务、错误处理、查询边界和可升级性约束
- 提供 Aras Innovator 2024 Release 安装与验收清单
- 按“症状 → 证据 → 假设 → 验证 → 回滚”执行故障诊断
- 识别旧版本、经典客户端和私有 DOM/frame/grid API 风险

## 目录

```text
skills/aras-innovator-engineering/
├── SKILL.md
├── agents/openai.yaml
└── references/
    ├── architecture-and-data-flow.md
    ├── code-recipes.md
    ├── evaluations.md
    ├── evidence-policy.md
    ├── installation-2024.md
    ├── legacy-compatibility.md
    ├── modeling-and-development.md
    ├── security-and-transactions.md
    └── troubleshooting-runbook.md
```

## 安装到 Codex

```bash
git clone https://github.com/OWNER/REPOSITORY.git Aras-PLM
mkdir -p ~/.codex/skills
cp -R Aras-PLM/skills/aras-innovator-engineering ~/.codex/skills/
```

重启 Codex 或开始一个新会话，然后直接提出 Aras 相关任务即可。Skill 的描述会让 Codex 在相关任务中自动加载它。

## 安装到 Claude Code

```bash
git clone https://github.com/OWNER/REPOSITORY.git Aras-PLM
mkdir -p ~/.claude/skills
cp -R Aras-PLM/skills/aras-innovator-engineering ~/.claude/skills/
```

`SKILL.md` 与 `references/` 可被 Claude Code 使用；`agents/openai.yaml` 是 Codex 的展示元数据，Claude Code 会忽略它。安装后可让 Claude 自动匹配 Aras 任务，也可输入 `/aras-innovator-engineering` 显式调用。

如果只希望在某一个 Claude Code 项目中启用，可复制到项目目录：

```bash
mkdir -p .claude/skills
cp -R Aras-PLM/skills/aras-innovator-engineering .claude/skills/
```

## 使用示例

```text
请使用 aras-innovator-engineering Skill，审查这个 Server Method 的权限、事务和错误处理。
```

```text
我们运行 Aras Innovator 2024 Release。请设计 Part 与 CAD Document 的关系模型，并给出安全的 IOM 查询及验证矩阵。
```

```text
请按 troubleshooting runbook 诊断 OAuth discovery 正常但客户端登录失败的问题；先收集证据，不要直接改配置。
```

## 证据边界

- 官方目标版本资料优先于第三方总结和培训材料。
- 版本不明确时，Skill 会提供安全的版本中立路径，并标记需要针对目标 Release/SP/Hotfix 验证的签名。
- 仓库不包含原始 PDF、PPTX、DOCX 或第三方网页副本，避免重新分发受版权保护的源材料。
- 本项目是社区工程辅助资料，不是 Aras 官方产品或官方支持渠道。Aras 和 Aras Innovator 是其各自权利人的商标。

## License

[MIT](LICENSE)
