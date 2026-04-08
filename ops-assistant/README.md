# Ops Assistant Workspace

这是当前 OpenClaw 环境中的**独立运维工作区**，用于：

- 服务器与业务巡检
- 告警与通知（当前只走 Telegram，且使用独立 alerts bot）
- 低风险自愈
- 运维留痕与报告归档
- 发现未归档 / 漏归档 / 漂移项目

该工作区与主 workspace 共享同一 OpenClaw 实例与工具能力，但在目录、文档、报告、策略上独立。

## 设计目标

1. 运维当前已知服务器与其承载业务
2. 所有工作必须留痕
3. 留痕尽量可 Git 化，并推送到私有 GitHub 仓库
4. 权限边界明确：只读、低风险自愈、高风险需审批
5. 具备“发现遗漏项目 / 未归档改动 / 资产漂移”的能力
6. 支持后台自动运行（cron / 定时任务）
7. Telegram 作为主告警渠道

## 建议目录

- `docs/`：设计文档、策略、运行方式
- `inventory/`：从主 `infra/` 同步/映射出的运维视图
- `checks/`：巡检脚本
- `runbooks/`：故障手册 / 自愈策略
- `reports/`：周期巡检输出
- `alerts/`：告警策略与模板
- `state/`：运行状态、上次检查时间、指纹缓存（运行态目录，默认不入 Git）
- `proposals/`：待人工确认的变更建议

详细方案见 `docs/ops-assistant-design-v1.md`。

## Git hygiene

- `reports/` 下的有意义 Markdown 报告可以提交。
- `state/` 下的运行态文件（`last-run.json`、stdout/stderr、cron log、alert state 等）默认不提交。
- `reports/` 顶层的临时 `.log` 产物默认不提交。

## Alert-state sync note

- `run_fleet_check.py` now does a best-effort follow-up call to `send_alerts.py` after it writes and filters `last-run.json`.
- This reduces the common confusion where a manual fleet check has already cleared alerts, but `alert-state.json` still reflects the previously sent alert signature.
- Existing cron chains that still call `run_fleet_check.py && send_alerts.py` remain safe because `send_alerts.py` deduplicates by alert signature.

## Alerting / daily report policy

- High-frequency checks are for state refresh, not for blasting Telegram every hour.
- Immediate Telegram push is reserved for significant incidents only:
  - new `P1`
  - newly down/unreachable `core` / `standard` hosts
  - recovery of those significant incidents
- A separate daily Telegram report should carry the broad per-host summary.
