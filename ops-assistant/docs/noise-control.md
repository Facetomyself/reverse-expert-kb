# Noise Control Rules

## Purpose
在正式启用 cron 之前，对已知会产生噪声但当前不应重复打扰的对象做分类。

## Current suppression rules
- `self-server`:
  - 视为 `observe_only`
  - 已知从当前 OpenClaw 不可达
  - 不再作为 P1 主机故障反复告警

- `oracle-mail`:
  - 视为 retired host
  - 退役项目 stale hints 不作为普通漂移告警

- `1panel`:
  - 在 `ali-cloud` / `oracle-proxy` 上优先视为机器级基础设施，不作为项目漂移噪声

- `oracle-docker-proxy`:
  - `harbor` / `hubcmd` / `registry` / `registry-ui` 当前先作为已知待细化映射，不在首版中反复告警

## Principle
降噪不是忽略问题，而是：
- 先把已知例外分类
- 让真正的新异常更显眼
- 后续随着文档完善再收紧规则
