# Infrastructure Overview

这份总览不是替代各主机手册，而是给你一个**一眼看全局**的入口：

- 哪些机器是现役
- 哪些机器是退役/停摆
- 哪些机器当前不可达
- 每台机器的大致职责
- 现在最该维护的点在哪里

---

## 1. Global status snapshot

### A. 现役核心主机

#### 1) `oracle-proxy`
- Provider: Oracle Cloud
- IP: `158.178.236.241`
- 主域名: `proxy.zhangxuemin.work`
- 当前角色:
  - Tavily 注册/代理链路
  - grok 相关服务
  - cliproxy
  - 辅助型反代/工具主机
- 当前状态: **现役 / 已深入建档**
- 关键事实:
  - Tavily proxy 已打通
  - grok2api / cliproxy 已有较完整运维说明
  - 是当前搜索/代理链路的重要节点

#### 2) `oracle-docker-proxy`
- Provider: Oracle Cloud
- IP: `129.150.61.78`
- 当前角色:
  - 多 registry proxy / mirror 主机
  - Caddy 前门
  - hubcmd UI
  - registry UI（当前有问题）
- 代表域名:
  - `hub.zhangxuemin.work`
  - `ghcr.zhangxuemin.work`
  - `gcr.zhangxuemin.work`
  - `quay.zhangxuemin.work`
  - `ui.zhangxuemin.work`
- 当前状态: **现役 / 已深入建档**
- 关键事实:
  - Caddy -> 本地高端口 -> `dqzboy/*` registry stack
  - Harbor 文件/数据足迹存在，但 Harbor 容器当前不在跑
  - `ui.zhangxuemin.work` 问题更像 UI 对 OCI index / manifest list 的兼容性问题

#### 3) `ali-cloud`
- Provider: Alibaba Cloud
- IP: `106.15.239.221`
- 当前角色:
  - 1Panel 控制面主机
  - EasyImages 图床
  - camoufox 远程浏览器节点
- 当前状态: **现役 / 已建第一、二轮文档**
- 关键事实:
  - `1panel.service` 占用 `80`
  - `easyimage` 暴露在 `10086`
  - `camoufox-remote` 暴露 websocket `39222/camoufox`

### B. 已退役 / 暂不作为现役服务使用

#### 4) `oracle-mail`
- Provider: Oracle Cloud
- IP: `140.83.52.216`
- DNS 仍指向邮件相关域名，但当前运行态不匹配
- 当前状态: **退役 / 本地旧邮件栈已归档**
- 关键事实:
  - Mailu 部署曾存在，但未运行
  - `moemail` 项目也未运行
  - 两者已归档到:
    - `/root/retired-services/2026-03-15/mailu`
    - `/root/retired-services/2026-03-15/moemail`
  - 当前临时邮箱使用的是另一套 Cloudflare 侧部署

### C. 当前不可达 / 待重验

#### 5) `self-server`
- IP: `211.144.221.229`
- SSH: `root@211.144.221.229:44005`
- 当前状态: **不可达**
- 关键事实:
  - 从当前 OpenClaw 主机测试时 TCP 失败
  - SSH 连接超时
  - 问题发生在认证前，属于网络连通性/目标存活问题
  - 可能受中国网络、端口映射、目标机在线状态影响

### D. 本机 / 不应误判成另一台远程主机

#### 6) `oracle-open_claw`
- 对应 IP: `64.110.106.11`
- 当前状态: **本机**
- 关键事实:
  - 这不是下一台待盘点机器，而是当前 OpenClaw 所在主机
  - Cloudflare 导出里 `dev.zhangxuemin.work` 的旧注释（`n8n`）已确认过时

---

## 2. Role map by function

### 搜索 / LLM 代理 / 注册链路
- `oracle-proxy`
  - Tavily proxy
  - Tavily registration scheduler
  - grok2api
  - cliproxy

### Registry / image mirror / UI
- `oracle-docker-proxy`
  - Docker Hub mirror
  - GHCR mirror
  - GCR mirror
  - K8s registry mirrors
  - Quay / MCR / Elastic / NVCR mirrors
  - hubcmd UI
  - registry UI（存在兼容问题）

### 图片托管 / 浏览器节点 / 面板
- `ali-cloud`
  - 1Panel
  - EasyImages
  - camoufox-remote

### 邮件
- 当前 Cloudflare 侧临时邮箱：**现役**（不在本次已盘主机内）
- `oracle-mail`：**旧本地邮件栈已退役**

---

## 3. Operational status tiers

### Tier 1 — 应优先关注
- `oracle-proxy`
- `oracle-docker-proxy`

理由：当前你的搜索链路、代理链路、registry/mirror 能力都直接依赖它们。

### Tier 2 — 次核心但现役
- `ali-cloud`

理由：它现在是明确在线且有实际服务的应用主机，但整体业务关键性看起来低于前两台 Oracle 主机。

### Tier 3 — 已退役或待判断
- `oracle-mail`
- `self-server`

理由：一个已归档停用，一个当前不可达。

---

## 4. Current known problem list

### Active problems
1. `oracle-docker-proxy`:
   - `ui.zhangxuemin.work` 不稳定/异常
   - 当前更像 `registry-ui` 对 OCI index / manifest list 的兼容问题
   - 已验证直接升级 `dqzboy/docker-registry-ui:latest` 的 canary **没有证明能修复**

2. `self-server`:
   - 当前网络不可达

### Configuration drift / stale metadata
1. Cloudflare DNS 导出中的 `dev.zhangxuemin.work` 注释 `n8n` 已过时
2. `oracle-mail` 的 DNS 仍指向旧邮件主机，但本地邮件栈已退役

---

## 5. Recommended next work

### Option A — 继续完善全局运维地图
- 给每台主机补 `status` / `lifecycle` 字段
- 把 Cloudflare 域名按机器重新整理成“现役 / 过时 / 待清理”

### Option B — 继续深挖现役问题点
- `oracle-docker-proxy` 的 registry UI 问题
- `ali-cloud` 上 1Panel 管理的站点/域名关系

### Option C — 做 DNS / 主机 / 服务三方对账
- 域名指向谁
- 那台机器现在是否真的提供该服务
- 哪些 DNS 记录已经陈旧

当前这一步已经落地到：`infra/dns-reconciliation.md`

---

## 6. Cross-links
- Host inventory: `infra/inventory.yaml`
- Machine status table: `infra/host-status.yaml`
- DNS reconciliation: `infra/dns-reconciliation.md`
- Per-host runbooks under `infra/hosts/`
