# Fleet Summary - 2026-03-17

首版运维 assistant 巡检 MVP 输出。

## ali-cloud
- overall: OK
- uptime/load:  22:56:39 up 38 days,  8:52,  1 user,  load average: 0.16, 0.06, 0.01
- root fs: /dev/vda3        40G  6.7G   31G  18% /
- docker containers seen: 2
- running services sampled: 20
- compose files discovered: 0
- sample containers:
  - camoufox-remote	Up 2 weeks
  - easyimage	Up 5 weeks

## oracle-docker-proxy
- overall: OK
- uptime/load:  14:56:32 up 222 days, 13:43,  0 users,  load average: 0.00, 0.00, 0.00
- root fs: /dev/sda1        45G   17G   29G  37% /
- docker containers seen: 4
- running services sampled: 20
- compose files discovered: 0
- sample containers:
  - reg-ghcr	Up 7 months
  - reg-mcr	Up 7 months
  - reg-docker-hub	Up 7 months
  - reg-k8s	Up 7 months

## oracle-mail
- overall: OK
- uptime/load:  22:56:40 up 388 days,  8:28,  0 users,  load average: 0.01, 0.01, 0.00
- root fs: /dev/mapper/ocivolume-root   36G   20G   16G  56% /
- docker containers seen: 0
- running services sampled: 20
- compose files discovered: 0

## oracle-open_claw
- overall: OK
- uptime/load:  22:56:27 up 4 days, 23:41,  0 users,  load average: 0.02, 0.23, 0.14
- root fs: /dev/sda1        45G   17G   29G  37% /
- docker containers seen: 0
- running services sampled: 20
- compose files discovered: 0

## oracle-proxy
- overall: OK
- uptime/load:  14:56:29 up 18 days, 11:51,  1 user,  load average: 0.00, 0.02, 0.03
- root fs: /dev/sda1        45G   24G   22G  53% /
- docker containers seen: 9
- running services sampled: 20
- compose files discovered: 13
- sample containers:
  - tavily-scheduler	Up 5 hours
  - tavily-camoufox-adapter	Up 5 hours
  - tavily-camoufox	Up 5 hours
  - exafree	Up 30 hours (healthy)
  - proxy-tavily-proxy-1	Up 4 hours
- compose discoveries (potential undocumented/drift candidates):
  - /root/AntiCAP-WebApi-docker/docker-compose.yml
  - /root/ExaFree/docker-compose.yml
  - /root/FlareSolverr/docker-compose.yml
  - /root/ProxyCat/docker-compose.yml
  - /root/backups/grok2api-20260313-133823/docker-compose.yml

## self-server
- overall: ATTENTION
- docker containers seen: 0
- running services sampled: 0
- compose files discovered: 0
- errors:
  - host: ssh: connect to host 211.144.221.229 port 44005: Connection timed out
  - docker: ssh: connect to host 211.144.221.229 port 44005: Connection timed out
  - systemd: ssh: connect to host 211.144.221.229 port 44005: Connection timed out
  - drift: ssh: connect to host 211.144.221.229 port 44005: Connection timed out

## Initial observations
- oracle-proxy has many compose projects visible on disk, including several likely not yet normalized into current infra documentation; this is exactly the kind of undocumented/drift surface the ops assistant should keep flagging.
- self-server remains the likely exception path and should be treated as an unreachable-observe target, not a blocking failure for the entire fleet run.
- oracle-docker-proxy and ali-cloud responded cleanly in this MVP pass.

