# DNS / Host / Service Reconciliation

本文件反映 **2026-06-02** 抓取的 Cloudflare live zone 与当前 `infra/` 主机文档之间的正式对账结果。

基于以下信息对账：
- Cloudflare live zone (`zhangxuemin.work`)
- 已完成的主机 SSH / 网络盘点
- 当前运行态 / 端口 / 项目文档
- `infra/cloudflare-dns/baseline-records.json`

目标不是马上改 DNS，而是把 live 记录先分成：
- **匹配（matches reality）**
- **部分匹配（host right, service questionable）**
- **过时/漂移（stale or drifted）**
- **未核实（unverified）**

---

## Live snapshot summary

- zone: `zhangxuemin.work`
- zone_id: `b68f5785980dfe650ca4cdd7d237254d`
- current live record count: **28**
- type counts:
  - `A`: 18
  - `AAAA`: 2
  - `MX`: 4
  - `TXT`: 4
- current live snapshot vs committed baseline: **no semantic diff** after the 2026-06-02 baseline refresh that recorded Cloudflare MX priorities (`send`: 10; root `route1/2/3`: 56/24/98) on the existing MX records

---

## A / AAAA records reconciliation

| Record | DNS Target | Current reality | Status | Notes |
|---|---|---|---|---|
| `proxy.zhangxuemin.work` | `158.178.236.241` | 指向 `oracle-proxy`，且该主机现役 | **匹配** | 主入口域名已确认 |
| `backup.zhangxuemin.work` | `129.150.61.78` | 指向 `oracle-gateway`，当前承载 Hysteria / gateway 角色 | **匹配** | 仍然有效，但不再是主公共 HTTPS front door |
| `derp.zhangxuemin.work` | `129.150.61.78` | 指向 `oracle-gateway`，当前是该主机的主公共 TCP front door | **匹配** | `derper` 当前占用公共 `80/443` |
| `dev.zhangxuemin.work` | `64.110.106.11` | 指向当前 OpenClaw 本机 `oracle-open_claw` | **匹配** | 当前 comment `openclaw-host` 与事实一致 |
| `hub.zhangxuemin.work` | `140.245.33.114` | 指向 `oracle-registry`，现役 | **匹配** | registry front door |
| `ghcr.zhangxuemin.work` | `140.245.33.114` | 指向 `oracle-registry`，现役 | **匹配** | registry front door |
| `k8s.zhangxuemin.work` | `140.245.33.114` | 指向 `oracle-registry`，现役 | **匹配** | registry front door |
| `mcr.zhangxuemin.work` | `140.245.33.114` | 指向 `oracle-registry`，现役 | **匹配** | registry front door |
| `mail.zhangxuemin.work` | `140.83.52.216` | 指向 `oracle-mail`，当前是 `Outlook Email Plus` web app host | **匹配** | 当前应视为活跃 web-app 域名，而不是默认删除候选 |
| `hk.zhangxuemin.work` | `154.86.30.10` | 指向 `hk-relay`，当前是认证下载/浏览入口 | **匹配** | HK relay canonical domain |
| `drop.hk.zhangxuemin.work` | `154.86.30.10` | 指向 `hk-relay`，当前是 HTTPS 上传/下载入口 | **匹配** | 由 Caddy 反代本地 `dufs` |
| `clash.hk.zhangxuemin.work` | `154.86.30.10` | 指向 `hk-relay`，当前是 Clash 配置分发入口 | **匹配** | 公共订阅下载面 |
| `cliproxy-cn.zhangxuemin.work` | `154.86.30.10` | 指向 `hk-relay`，当前是 cliproxy 国内/HK 边缘入口 | **匹配** | HK Caddy -> `proxy.zhangxuemin.work:8317` |
| `cpam.zhangxuemin.work` | `158.178.236.241` | 指向 `oracle-proxy`，当前是 CPA Manager Plus direct/source 入口 | **匹配** | 直连/海外路径 |
| `cpam-cn.zhangxuemin.work` | `154.86.30.10` | 指向 `hk-relay`，当前是 CPA Manager Plus 国内/HK 边缘入口 | **匹配** | HK Caddy -> `https://cpam.zhangxuemin.work` |
| `reverse-cn.zhangxuemin.work` | `154.86.30.10` | 指向 `hk-relay`，当前是 `oracle-reverse-dev` 的国内/HK SSH 边缘入口（HK `:22061` -> Oracle `:22`） | **匹配** | DNS-only A；使用 `ssh -p 22061 ubuntu@reverse-cn.zhangxuemin.work` |
| `ctf-gpt-cn.zhangxuemin.work` | `154.86.30.10` | 指向 `hk-relay`，当前是 `oracle-reverse-dev` CTF GPT Plus 的国内/HK HTTPS 边缘入口 | **匹配** | HK Caddy -> `http://140.245.61.236:8000`; 使用 `https://ctf-gpt-cn.zhangxuemin.work/ctf-gpt-plus` |
| `claw-cn.zhangxuemin.work` | `154.86.30.10` | 指向 `hk-relay`，当前是 OpenClaw 国内/HK 边缘入口 | **匹配** | HK Caddy -> `https://dev.zhangxuemin.work` |
| `tmail.zhangxuemin.work` | Cloudflare proxied (`AAAA 100::`) | 当前仍作为 Cloudflare 侧临时邮箱/worker front path | **匹配** | 非主机直连记录 |
| `tmail-front.zhangxuemin.work` | Cloudflare proxied (`AAAA 100::`) | 当前仍作为 Cloudflare 侧 front path | **匹配** | 非主机直连记录 |

---

## MX records reconciliation

| Record | DNS Target | Current reality | Status | Notes |
|---|---|---|---|---|
| `zhangxuemin.work` | `route1/2/3.mx.cloudflare.net` (`priority`: 56/24/98) | 根域当前仍走 Cloudflare Email Routing | **匹配** | 与当前保留策略一致；优先级来自当前 Cloudflare live zone |
| `send.zhangxuemin.work` | `feedback-smtp.ap-northeast-1.amazonses.com` (`priority`: 10) | 当前保留 SES 发送/反馈路径 | **匹配** | 与现有 `send` SPF 记录配套；优先级来自当前 Cloudflare live zone |

---

## TXT records reconciliation

| Record | Current reality | Status | Notes |
|---|---|---|---|
| `zhangxuemin.work` SPF | `v=spf1 include:_spf.mx.cloudflare.net ~all` | **匹配** | 与根域 Cloudflare Email Routing 路径一致 |
| `send.zhangxuemin.work` SPF | `v=spf1 include:amazonses.com ~all` | **匹配** | 与 `send` 子域 SES 路径一致 |
| `_dmarc.zhangxuemin.work` | 根域 DMARC 策略当前仍在 live zone | **匹配** | 当前为 `p=reject`，并保留 Cloudflare DMARC 报告收件路径 |
| `cf2024-1._domainkey.zhangxuemin.work` | 更像 provider-side / Cloudflare-side 根域邮件策略 key | **未核实（中高置信度）** | 当前 zone 的 Email Routing / worker 接收规则仍在用，且现有证据更支持 provider-side mail-policy key 而非本机残留；见 `infra/cloudflare-dns/dkim-reconciliation.md` |

---

## Records not currently present in live zone

当前 live zone **没有**以下类型：
- `CNAME`
- `SRV`
- `TLSA`

这意味着：
- 旧的 `autoconfig` / `autodiscover` CNAME 已不在当前 live zone
- 旧 mail client discovery (`_autodiscover._tcp` / `_imaps._tcp` / `_pop3s._tcp` / `_submissions._tcp`) 已不在当前 live zone
- 旧 `_25._tcp.mail...` TLSA 记录已不在当前 live zone
- 历史 Mailu 根域 DKIM `dkim._domainkey.zhangxuemin.work` 已于 2026-04-14 在用户确认 Mailu 不再使用后删除
- 历史 moemail / Resend DKIM `resend._domainkey.zhangxuemin.work` 已于 2026-04-14 在用户要求清理 moemail 残留后删除

因此，任何仍声称这些记录“当前还存在”的文档都应视为**文档漂移**，而不是 live DNS 事实。

---

## Current reconciliation summary

- 当前 live zone 与提交的 baseline **一致**，没有即时 drift。
- 当前核心活跃基础设施域名与主机文档 **整体一致**。
- 新纳入当前事实的域名组包括：`derp.*`、CPA Manager Plus 入口（`cpam` / `cpam-cn`）、`oracle-reverse-dev` SSH 边缘入口（`reverse-cn`）与 `hk-relay` 相关记录（`hk` / `drop.hk` / `clash.hk` / `cliproxy-cn` / `claw-cn` / `cpam-cn` / `reverse-cn`）。
- 当前 DNS 主要未闭环点不是主机映射，而是 **剩余唯一一条 DKIM（`cf2024-1`）的发送方归属与长期去留还需继续收口**。
- 已新增 `infra/cloudflare-dns/dkim-reconciliation.md` 作为 DKIM 归属说明页，后续优先在那一页继续推进而不是在各处零散猜测。
- 历史 Mailu 相关主机残留与其对应 `dkim._domainkey` 记录已在 2026-04-14 按用户确认完成删除。
- `mail.zhangxuemin.work` 当前应被视为 **活跃 web-app front door**；后续若要删改，需基于新应用路径单独评估，而不是沿用旧“退役 mail host”判断。

---

## Notes
- 当前文档与自动化仅使用 canonical 主机名：`oracle-gateway`、`oracle-registry`、`oracle-reverse-dev`。
- 历史过渡名不再作为当前事实来源。
