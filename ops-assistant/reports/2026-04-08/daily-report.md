[ops-assistant] 每日服务器巡检日报 2026-04-08

今日结论:
- 当前无重大异常
- 一般关注项 1 项
- 核心: 3/3 正常
- 标准: 3/4 正常
- 观察: 1/1 正常
- 例外: 3/4 正常

一般关注项:
- ali-cloud: core inspection partial failure -> drift

主机与部署状态:
- ✅ oracle-open_claw (核心)
  - 主机名: instance-20250911-1634
  - Uptime: 14:41:59 up 26 days, 15:26,  0 users,  load average: 0.02, 0.04, 0.01
  - 根盘: /dev/sda1        45G   25G   21G  55% /
  - 容器: 无 / 未发现
  - 关键服务样本: containerd.service, cron.service, dbus.service, docker.service ...
  - 已登记项目: 无

- ✅ oracle-proxy (核心)
  - 主机名: 24-7-10-2039
  - Uptime: 06:42:01 up 40 days,  3:36,  1 user,  load average: 0.26, 0.15, 0.10
  - 根盘: /dev/sda1        45G   23G   23G  51% /
  - 容器: 7 个（cliproxy, grok2api, grok2api-camoufox-solver, exafree, proxy-tavily-proxy-1, grok-register-camoufox ...）
  - 关键服务样本: 1panel.service, accounts-daemon.service, argo.service, atd.service ...
  - 已登记项目:
    - ✅ Tavily Proxy: 容器 proxy-tavily-proxy-1; 编排 /root/tavily-key-generator/proxy/docker-compose.yml
    - 🚨 Tavily Key Generator: 缺容器 tavily-camoufox, tavily-camoufox-adapter, tavily-scheduler; 编排 /root/tavily-key-generator/docker-compose.yml
    - ✅ ExaFree: 容器 exafree; 编排 /root/ExaFree/docker-compose.yml
    - ✅ Grok Register Stack: 容器 grok-register-camoufox, grok-register-camoufox-adapter; 编排 /root/grok-register-standalone/docker-compose.yml, /root/grok-register/docker/docker-compose.yml
    - ✅ Grok2API: 容器 grok2api; 编排 /root/grok2api-official/docker-compose.yml, /root/grok2api/docker-compose.yml
    - ✅ CLIProxy: 容器 cliproxy
    - 🗄️ OpenAi (migrated): 编排漂移 /root/OpenAi/docker-compose.yml

- ✅ oracle-gateway (核心)
  - 主机名: 24-7-10-2055
  - Uptime: 06:42:03 up 244 days,  5:28,  1 user,  load average: 0.00, 0.00, 0.00
  - 根盘: /dev/sda1        45G   15G   30G  34% /
  - 容器: 1 个（hysteria）
  - 关键服务样本: accounts-daemon.service, atd.service, caddy.service, containerd.service ...
  - 已登记项目:
    - ✅ Hysteria gateway: 容器 hysteria
    - ✅ DERP server: 服务 derper.service
    - ✅ helper caddy: 服务 caddy.service

- 🚨 ali-cloud (标准)
  - 主机名: iZuf658qfolzlj2t1l53uyZ
  - Uptime: 14:42:06 up 18 days,  4:37,  1 user,  load average: 0.00, 0.00, 0.00
  - 根盘: /dev/vda3        40G  9.0G   29G  25% /
  - 容器: 5 个（sing-box-gateway, hysteria-client, coredns-gateway, camoufox-remote, easyimage）
  - 关键服务样本: 1panel.service, aliyun.service, chrony.service, cron.service ...
  - 已登记项目:
    - ✅ EasyImages: 容器 easyimage; 编排漂移 /opt/1panel/apps/easyimage2/easyimage2/docker-compose.yml
    - ✅ camoufox-remote: 容器 camoufox-remote
    - ✅ 1Panel control plane: 服务 1panel.service
    - ⚠️ Hysteria egress: 编排漂移 /opt/hysteria-egress/docker-compose.yml
    - ⚠️ sing-box gateway: 编排漂移 /opt/sing-box-gateway/docker-compose.yml
    - ⚠️ CoreDNS gateway: 编排漂移 /opt/coredns-gateway/docker-compose.yml

- ✅ oracle-mail (观察)
  - 主机名: instance-20250217-0809
  - Uptime: 14:42:07 up 410 days, 14 min,  0 users,  load average: 0.00, 0.00, 0.00
  - 根盘: /dev/mapper/ocivolume-root   36G   21G   16G  57% /
  - 容器: 2 个（outlook-email-plus-caddy, outlook-email-plus-app）
  - 关键服务样本: atd.service, auditd.service, chronyd.service, containerd.service ...
  - 已登记项目:
    - ✅ Outlook Email Plus: 编排 /opt/outlook-email-plus/docker-compose.yml
    - 🚨 rbot service: 缺服务 rbot.service
    - 🗄️ Mailu deployment footprint: 编排漂移 /root/mailu/docker-compose.yml
    - 🗄️ moemail repository: 暂无足够运行态样本

- ✅ oracle-registry (标准)
  - 主机名: oracle-registry
  - Uptime: 06:42:08 up 13 days, 20:28,  1 user,  load average: 0.01, 0.00, 0.00
  - 根盘: /dev/sda1        96G  6.5G   90G   7% /
  - 容器: 4 个（reg-docker-hub, reg-ghcr, reg-mcr, reg-k8s）
  - 关键服务样本: caddy.service, containerd.service, cron.service, dbus.service ...
  - 已登记项目:
    - ✅ Registry front door: 服务 caddy.service

- ✅ oracle-reverse-dev (标准)
  - 主机名: instance-20260325-1818
  - Uptime: 06:42:10 up 13 days, 20:21,  2 users,  load average: 0.13, 0.03, 0.01
  - 根盘: /dev/sda1        96G  9.7G   87G  11% /
  - 容器: 无 / 未发现
  - 关键服务样本: containerd.service, cron.service, dbus.service, docker.service ...
  - 已登记项目:
    - ❔ js-reverse-mcp helper: 暂无足够运行态样本

- ⚠️ self-server (例外)
  - 主机名: -
  - Uptime: -
  - 根盘: -
  - 主机检查错误: Connection timed out during banner exchange
Connection to UNKNOWN port 65535 timed out
  - 容器: 1 个（1Panel-frps-aOX6）
  - 关键服务样本: 1panel-agent.service, 1panel-core.service, auditd.service, crond.service ...
  - 已登记项目: 无

- ✅ home (例外)
  - 主机名: -
  - Uptime: -
  - 根盘: -
  - 容器: 无 / 未发现
  - 已登记项目: 无

- ✅ company (例外)
  - 主机名: -
  - Uptime: -
  - 根盘: -
  - 容器: 无 / 未发现
  - 已登记项目: 无

- ✅ home-macmini (例外)
  - 主机名: -
  - Uptime: -
  - 根盘: -
  - 容器: 无 / 未发现
  - 已登记项目: 无

- ✅ home-nas (标准)
  - 主机名: NAS
  - Uptime: 14:42:21 up 7 days, 12:45,  0 users,  load average: 0.01, 0.04, 0.06 [IO: 0.00, 0.02, 0.00 CPU: 0.00, 0.01, 0.00]
  - 根盘: /dev/md0        7.9G  1.4G  6.4G  19% /
  - 容器: 已跳过（profile=nas-tailnet-minimal）
  - 服务: 已跳过（profile=nas-tailnet-minimal）
  - 已登记项目: 无

观察项:
- self-server: 已按观察/例外策略处理

报告: /root/.openclaw/workspace/ops-assistant/reports/2026-04-08/fleet-summary.md
