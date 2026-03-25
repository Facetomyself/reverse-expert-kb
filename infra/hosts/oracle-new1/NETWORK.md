# oracle-new1 / NETWORK

## 1. Public Network Identity
- Public IP: `140.245.33.114`
- Provider: Oracle Cloud Infrastructure

## 2. Domains currently mapped here
Current active public domains intentionally served by this host:
- `hub.zhangxuemin.work`
- `ghcr.zhangxuemin.work`
- `k8s.zhangxuemin.work`
- `mcr.zhangxuemin.work`

## 3. Front-door mapping
Observed intended mapping on 2026-03-25:
- `hub.zhangxuemin.work` -> `localhost:51000`
- `ghcr.zhangxuemin.work` -> `localhost:52000`
- `k8s.zhangxuemin.work` -> `localhost:55000`
- `mcr.zhangxuemin.work` -> `localhost:57000`

Infrastructure notes:
- `caddy` listens on public `*:80` and `*:443`
- `caddy` admin API listens on `127.0.0.1:2019`
- local registry backend listeners are on:
  - `51000`
  - `52000`
  - `55000`
  - `57000`

## 4. Host firewall note
OCI-side ingress rules alone were not sufficient during cutover.
Local host iptables originally allowed only SSH and rejected other inbound traffic. Successful public service required adding and persisting:
- `80/tcp`
- `443/tcp`

This rule persistence now lives in the host's saved iptables state (`/etc/iptables/rules.v4`).
