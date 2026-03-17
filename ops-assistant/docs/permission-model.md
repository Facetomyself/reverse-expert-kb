# Permission Model

## Default principle

- 默认只读巡检
- 自动修复仅限白名单低风险动作
- 高风险动作必须人工确认
- 所有动作必须留痕

## Permission levels

### L1: ReadOnlyInspect
允许：
- SSH 只读命令
- systemd/docker 状态查看
- 端口/域名/证书检查
- 目录与项目发现
- 生成报告
- 发 Telegram 告警

### L2: SafeRemediate
允许（需白名单）：
- `systemctl restart <approved-service>`
- `docker restart <approved-container>`
- `docker compose up -d` in approved project dirs
- `openclaw gateway restart`

要求：
- 先检查后动作
- 动作后复检
- 失败不得无限重试

### L3: ChangeManaged
需要人工确认：
- 改配置文件
- 改 compose
- reload/restart 非白名单核心服务
- 新增/修改定时任务
- 变更反代映射

### L4: HumanOnly
禁止自动执行：
- firewall
- sshd
- sudoers / 用户 / 权限系统
- 系统升级 / reboot
- 删除数据库 / volume / 关键目录

## Escalation policy

- 巡检发现异常 → 先告警
- 若异常命中白名单自愈 → 尝试 1 次自动修复
- 若修复失败 → 升级为人工处理
- 若动作需要 L3/L4 → 只生成 proposal，不自动执行
