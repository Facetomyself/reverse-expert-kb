# Infrastructure Documentation Conventions

## 1. Host folder layout

Each host gets its own folder:

```text
infra/hosts/<host>/
  HOST.md
  NETWORK.md
  PROJECTS.md
  CHANGELOG.md
  projects/*.md
```

## 2. Required sections for each project doc

每个 `projects/*.md` 至少包含：

1. Summary
2. Access / Entry Points
3. Deployment Layout
4. Runtime Topology
5. Purpose and Workflow
6. Configuration
7. Operations
8. Health Checks
9. Data and Persistence
10. Common Tasks
11. Failure Modes / Troubleshooting
12. Dependencies / Cross-links
13. Change History

## 3. Command style

- 所有命令尽量写成可直接复制执行
- 默认写完整路径，不依赖 shell 当前目录
- 如果命令有风险，先写说明再写命令

## 4. Unknown fields

未知时不要瞎填，用：
- `Unknown`
- `Not yet documented`
- `To be confirmed`

## 5. Change logging

每次重要变更后，至少更新：
- 对应项目文档的 `Change History`
- 主机级 `CHANGELOG.md`

## 6. Secrets handling

- 文档中默认不直接展开 secrets
- 如果必须提，写“在哪里取”，不要写全值
- 示例：`Configured in /root/project/.env` 或 `stored in ~/.openclaw/credentials/...`
