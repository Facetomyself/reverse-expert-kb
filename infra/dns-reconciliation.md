# DNS / Host / Service Reconciliation

基于以下信息对账：
- Cloudflare 导出的 `zhangxuemin.work` zone
- 已完成的主机 SSH 盘点
- 当前运行态/端口/项目文档

目标不是马上改 DNS，而是把每条记录先分成：
- **匹配（matches reality）**
- **部分匹配（host right, service questionable）**
- **过时/漂移（stale or drifted）**
- **未核实（unverified）**

---

## 1. A / CNAME records reconciliation

| Record | DNS Target | Current reality | Status | Notes |
|---|---|---|---|---|
| `proxy.zhangxuemin.work` | `158.178.236.241` | 指向 `oracle-proxy`，且该主机现役 | **匹配** | 主入口域名已确认 |
| `hub.zhangxuemin.work` | `129.150.61.78` | 指向 `oracle-docker-proxy`，Caddy + registry proxy 现役 | **匹配** | 已验证 HTTP 200 |
| `ghcr.zhangxuemin.work` | `129.150.61.78` | 指向 `oracle-docker-proxy`，现役 | **匹配** | 已验证 HTTP 200 |
| `gcr.zhangxuemin.work` | `129.150.61.78` | 指向 `oracle-docker-proxy`，现役 | **匹配** | 已验证 HTTP 200 |
| `quay.zhangxuemin.work` | `129.150.61.78` | 指向 `oracle-docker-proxy`，现役 | **匹配** | 已验证 HTTP 200 |
| `k8sgcr.zhangxuemin.work` | `129.150.61.78` | 指向 `oracle-docker-proxy`，配置已确认 | **匹配** | 已确认 Caddy -> 54000 |
| `mcr.zhangxuemin.work` | `129.150.61.78` | 指向 `oracle-docker-proxy`，配置已确认 | **匹配** | 已确认 Caddy -> 57000 |
| `nvcr.zhangxuemin.work` | `129.150.61.78` | 指向 `oracle-docker-proxy`，配置已确认 | **匹配** | 已确认 Caddy -> 59000 |
| `elastic.zhangxuemin.work` | `129.150.61.78` | 指向 `oracle-docker-proxy`，配置已确认 | **匹配** | 已确认 Caddy -> 58000 |
| `hubcmd.zhangxuemin.work` | `129.150.61.78` | 指向 `oracle-docker-proxy`，hubcmd-ui 现役 | **匹配** | 已确认 Caddy -> 30080 |
| `ui.zhangxuemin.work` | `129.150.61.78` | 指向 `oracle-docker-proxy`，但 registry UI 当前异常 | **部分匹配** | 主机正确，服务存在，但功能不健康 |
| `backup.zhangxuemin.work` | `129.150.61.78` | 当前未在已读 Caddy 映射中确认 | **未核实 / 疑似漂移** | 可能历史残留 |
| `mail.zhangxuemin.work` | `140.83.52.216` | 指向 `oracle-mail`，但本地邮件栈已退役 | **过时/漂移** | DNS 仍指向旧主机，运行态不匹配 |
| `autoconfig.zhangxuemin.work` | `CNAME -> mail.zhangxuemin.work` | 仍链到退役邮件主机 | **过时/漂移** | 外部返回 Cloudflare 521 |
| `autodiscover.zhangxuemin.work` | `CNAME -> mail.zhangxuemin.work` | 仍链到退役邮件主机 | **过时/漂移** | 外部返回 Cloudflare 521 |
| `dev.zhangxuemin.work` | `64.110.106.11` | 这是本机；旧注释 `n8n` 已过时 | **部分匹配 / 注释过时** | IP 所指主机没错，但角色注释失真 |
| `pend.zhangxuemin.work` | `217.142.242.113` | 目前未通过 SSH 或服务探测核实 | **未核实** | 仅有 Cloudflare 导出线索 |

---

## 2. MX / mail-related reconciliation

Important external-reference conclusion:
- Cloudflare Email Routing documentation indicates the service requires appropriate `MX` and `TXT` records in DNS.
- It does not, by itself, require legacy self-hosted mail client discovery records like `mail`, `autoconfig`, or `autodiscover` merely to forward mail.
- That means the old self-hosted mail-family records should be evaluated as client-protocol compatibility records, not as core Cloudflare Email Routing requirements.


| Record | Current reading | Status | Notes |
|---|---|---|---|
| `zhangxuemin.work MX -> route*.mx.cloudflare.net` | 指向 Cloudflare 邮件路由 | **看起来匹配当前策略** | 与“临时邮箱在 Cloudflare 侧”方向一致 |
| `send.zhangxuemin.work MX -> feedback-smtp.ap-northeast-1.amazonses.com` | 专用于 SES | **未冲突** | 看起来是专用发送用途 |
| `_autodiscover/_imaps/_pop3s/_submissions SRV -> mail.zhangxuemin.work` | 仍指向旧 `oracle-mail` | **过时/漂移** | 如果本地 Mailu 已退役，应重新评估 |
| `_25._tcp.mail.zhangxuemin.work TLSA` | 仍绑定旧 mail 主机语义 | **疑似过时** | 若不再由本地主机提供 SMTP，应重新评估 |
| `zhangxuemin.work TLSA` | 存在但语义需复核 | **未核实** | 需确认它当前服务对象 |

---

## 3. TXT / mail-policy reconciliation

| Record | Current reading | Status | Notes |
|---|---|---|---|
| `zhangxuemin.work SPF include:_spf.mx.cloudflare.net` | 与 Cloudflare 邮件路由方向一致 | **看起来匹配** | 需结合当前实际发信路径复核 |
| `send.zhangxuemin.work SPF include:amazonses.com` | 与 SES 发送域一致 | **看起来匹配** | 无明显冲突 |
| `_dmarc.zhangxuemin.work` | 仍指向 mail-related reporting addresses | **基本匹配但应复核** | 如果收报邮箱仍有效则可保留 |
| DKIM records (`cf2024-1`, `dkim`, `resend`) | 存在多套 DKIM 轨迹 | **未完全核实** | 需按当前实际发信链路清理冗余 |

---

## 4. Most likely stale / cleanup candidates

优先怀疑为陈旧或需要复核的记录：

1. `mail.zhangxuemin.work`
2. `autoconfig.zhangxuemin.work`
3. `autodiscover.zhangxuemin.work`
4. `_autodiscover._tcp.zhangxuemin.work`
5. `_imaps._tcp.zhangxuemin.work`
6. `_pop3s._tcp.zhangxuemin.work`
7. `_submissions._tcp.zhangxuemin.work`
8. `_25._tcp.mail.zhangxuemin.work` TLSA
9. `backup.zhangxuemin.work`
10. `dev.zhangxuemin.work` 的旧注释语义

---

## 5. Recommended cleanup sequence

### Phase 1 — 只确认，不改
- 先确认当前 Cloudflare 临时邮箱到底依赖哪些 DNS 记录
- 确认 `mail/autoconfig/autodiscover` 是否已经完全不再被客户端使用
- 确认 `backup.zhangxuemin.work` 是否还有历史用途

### Phase 2 — 标注和分组
建议把 DNS 记录分成：
- **现役基础设施入口**
- **现役邮件相关**
- **历史兼容记录**
- **待删除候选**

### Phase 3 — 有计划地清理
优先处理明显漂移的：
- `mail/autoconfig/autodiscover` 相关旧本地邮箱记录
- 旧 SRV / TLSA
- 无人确认用途的 `backup`

---

## 6. Summary judgment

### Clearly aligned with reality
- `proxy.zhangxuemin.work`
- `hub/ghcr/gcr/quay/k8sgcr/mcr/nvcr/elastic/hubcmd`

### Host correct but service degraded
- `ui.zhangxuemin.work`

### Clearly drifted / stale
- `mail`
- `autoconfig`
- `autodiscover`
- 多个 mail SRV/TLSA 指向旧本地邮件主机

### Not yet verified enough
- `backup`
- `pend`
- 部分 DKIM/TLSA 记录的现役性
