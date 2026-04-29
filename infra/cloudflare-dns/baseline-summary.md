# Cloudflare DNS Baseline Summary

Generated from live Cloudflare zone snapshot on 2026-04-30 after refreshing MX priorities from Cloudflare Email Routing / SES records.

- zone_id: `b68f5785980dfe650ca4cdd7d237254d`
- record_count: **24**
- type_counts:
  - `A`: 14
  - `AAAA`: 2
  - `MX`: 4
  - `TXT`: 4

## Records

| Name | Type | Content | Priority | TTL | Proxied | Comment |
|---|---|---|---:|---:|---|---|
| `_dmarc.zhangxuemin.work` | `TXT` | `"v=DMARC1; p=reject; rua=mailto:f7f21e5e0ab844279caa542a187734f0@dmarc-reports.cloudflare.net,mailto:mail@zhangxuemin.work; ruf=mailto:mail@...` |  | 1 | False | DMARC |
| `backup.zhangxuemin.work` | `A` | `129.150.61.78` |  | 1 | False | oracle-gateway / hysteria |
| `cf2024-1._domainkey.zhangxuemin.work` | `TXT` | `"v=DKIM1; h=sha256; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAiweykoi+o48IOGuP7GR3X0MOExCUDY/BCRHoWBnh3rChl7WhdyCxW3jgq1daEjPPqoi...` |  | 1 | False |  |
| `clash.hk.zhangxuemin.work` | `A` | `154.86.30.10` |  | 1 | False |  |
| `claw-cn.zhangxuemin.work` | `A` | `154.86.30.10` |  | 300 | False | CN edge via hk-relay for OpenClaw |
| `cliproxy-cn.zhangxuemin.work` | `A` | `154.86.30.10` |  | 300 | False | CN edge via hk-relay for cliproxy |
| `derp.zhangxuemin.work` | `A` | `129.150.61.78` |  | 1 | False |  |
| `dev.zhangxuemin.work` | `A` | `64.110.106.11` |  | 1 | False | openclaw-host |
| `drop.hk.zhangxuemin.work` | `A` | `154.86.30.10` |  | 1 | False |  |
| `ghcr.zhangxuemin.work` | `A` | `140.245.33.114` |  | 1 | False | oracle-registry |
| `hk.zhangxuemin.work` | `A` | `154.86.30.10` |  | 1 | False |  |
| `hub.zhangxuemin.work` | `A` | `140.245.33.114` |  | 1 | False | oracle-registry |
| `k8s.zhangxuemin.work` | `A` | `140.245.33.114` |  | 1 | False | oracle-registry |
| `mail.zhangxuemin.work` | `A` | `140.83.52.216` |  | 1 | False | oracle-mail web-app host |
| `mcr.zhangxuemin.work` | `A` | `140.245.33.114` |  | 1 | False |  |
| `proxy.zhangxuemin.work` | `A` | `158.178.236.241` |  | 1 | False | oracle-proxy |
| `send.zhangxuemin.work` | `MX` | `feedback-smtp.ap-northeast-1.amazonses.com` | 10 | 3600 | False |  |
| `send.zhangxuemin.work` | `TXT` | `"v=spf1 include:amazonses.com ~all"` |  | 3600 | False |  |
| `tmail-front.zhangxuemin.work` | `AAAA` | `100::` |  | 1 | True |  |
| `tmail.zhangxuemin.work` | `AAAA` | `100::` |  | 1 | True |  |
| `zhangxuemin.work` | `MX` | `route1.mx.cloudflare.net` | 56 | 1 | False |  |
| `zhangxuemin.work` | `MX` | `route2.mx.cloudflare.net` | 24 | 1 | False |  |
| `zhangxuemin.work` | `MX` | `route3.mx.cloudflare.net` | 98 | 1 | False |  |
| `zhangxuemin.work` | `TXT` | `"v=spf1 include:_spf.mx.cloudflare.net ~all"` |  | 1 | False |  |
