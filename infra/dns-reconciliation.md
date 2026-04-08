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

## A / CNAME records reconciliation

| Record | DNS Target | Current reality | Status | Notes |
|---|---|---|---|---|
| `proxy.zhangxuemin.work` | `158.178.236.241` | 指向 `oracle-proxy`，且该主机现役 | **匹配** | 主入口域名已确认 |
| `backup.zhangxuemin.work` | `129.150.61.78` | 指向 `oracle-gateway`，当前是网关/DERP 主机 | **匹配** | 语义已切到 gateway |
| `hub.zhangxuemin.work` | `140.245.33.114` | 指向 `oracle-registry`，现役 | **匹配** | 已迁移到 registry front door |
| `ghcr.zhangxuemin.work` | `140.245.33.114` | 指向 `oracle-registry`，现役 | **匹配** | 已迁移到 registry front door |
| `k8s.zhangxuemin.work` | `140.245.33.114` | 指向 `oracle-registry`，现役 | **匹配** | 已迁移到 registry front door |
| `mcr.zhangxuemin.work` | `140.245.33.114` | 指向 `oracle-registry`，现役 | **匹配** | 已迁移到 registry front door |
| `mail.zhangxuemin.work` | `140.83.52.216` | 指向 `oracle-mail`，当前是 web app host | **匹配** | 当前非传统 mail infra 语义 |
| `tmail.zhangxuemin.work` | Cloudflare proxied | 活服务 | **匹配** | worker/front path |
| `tmail-front.zhangxuemin.work` | Cloudflare proxied | 活服务 | **匹配** | worker/front path |

---

## Notes
- 当前文档与自动化仅使用 canonical 主机名：`oracle-gateway`、`oracle-registry`、`oracle-reverse-dev`。
- 历史过渡名不再作为当前事实来源。
