# Alert Policy

## Channel
- Primary: Telegram
- Email: not enabled in v1

## Severity

### P1 Critical
立即推送：
- 主机不可达
- 核心服务中断
- OpenClaw / gateway 异常
- 核心代理/入口不可用
- 磁盘 > 90%
- 证书 < 7 天

### P2 Warning
推送：
- 关键容器退出
- 项目 healthcheck 失败
- 文档/运行态漂移
- 发现未登记服务/项目/端口/反代
- 同一任务连续失败

### P3 Info
默认不推送，只写报告：
- 巡检成功
- 轻微波动
- 低风险自愈成功

## Message template
- title
- host
- severity
- summary
- observed_at
- attempted_action
- next_step
- report_path
