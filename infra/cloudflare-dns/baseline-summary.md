# Cloudflare DNS Baseline Summary

- zone_id: `b68f5785980dfe650ca4cdd7d237254d`
- record_count: **42**
- type_counts:
  - `A`: 32
  - `AAAA`: 2
  - `MX`: 4
  - `TXT`: 4

## Records

- `A` `backup.zhangxuemin.work` -> `129.150.61.78` (ttl=1, proxied=false, comment=oracle-gateway / hysteria)
- `A` `card-cn.zhangxuemin.work` -> `154.86.30.10` (ttl=300, proxied=false, comment=CN edge via hk-relay for card shop)
- `A` `card.zhangxuemin.work` -> `158.178.236.241` (ttl=300, proxied=false, comment=card shop global/source on oracle-proxy)
- `A` `clash.hk.zhangxuemin.work` -> `154.86.30.10` (ttl=1, proxied=false)
- `A` `claw-cn.zhangxuemin.work` -> `154.86.30.10` (ttl=300, proxied=false, comment=CN edge via hk-relay for OpenClaw)
- `A` `cliproxy-cn.zhangxuemin.work` -> `154.86.30.10` (ttl=300, proxied=false, comment=CN edge via hk-relay for cliproxy)
- `A` `cpam-cn.zhangxuemin.work` -> `154.86.30.10` (ttl=300, proxied=false, comment=CN edge via hk-relay for CPA Manager Plus)
- `A` `cpam.zhangxuemin.work` -> `158.178.236.241` (ttl=300, proxied=false, comment=oracle-proxy CPA Manager Plus)
- `A` `ctf-gpt-cn.zhangxuemin.work` -> `154.86.30.10` (ttl=300, proxied=false, comment=CN/HK edge via hk-relay for oracle-reverse-dev CTF GPT Plus)
- `A` `derp.zhangxuemin.work` -> `129.150.61.78` (ttl=1, proxied=false)
- `A` `dev.zhangxuemin.work` -> `64.110.106.11` (ttl=1, proxied=false, comment=openclaw-host)
- `A` `docs-cn.zhangxuemin.work` -> `154.86.30.10` (ttl=300, proxied=false, comment=CN edge via hk-relay for Kiro docs)
- `A` `docs.zhangxuemin.work` -> `158.178.236.241` (ttl=300, proxied=false, comment=Kiro docs global/source on oracle-proxy)
- `A` `drop.hk.zhangxuemin.work` -> `154.86.30.10` (ttl=1, proxied=false)
- `A` `ghcr.zhangxuemin.work` -> `140.245.33.114` (ttl=1, proxied=false, comment=oracle-registry)
- `A` `gpt-card-cn.zhangxuemin.work` -> `154.86.30.10` (ttl=1, proxied=false)
- `A` `gpt-card.zhangxuemin.work` -> `158.178.236.241` (ttl=1, proxied=false)
- `A` `gptam-cn.zhangxuemin.work` -> `154.86.30.10` (ttl=300, proxied=false, comment=CN/HK edge via hk-relay for GPT Account Manager)
- `A` `gptam.zhangxuemin.work` -> `158.178.236.241` (ttl=300, proxied=false, comment=oracle-proxy GPT Account Manager direct/source entry)
- `A` `hk.zhangxuemin.work` -> `154.86.30.10` (ttl=1, proxied=false)
- `A` `hub.zhangxuemin.work` -> `140.245.33.114` (ttl=1, proxied=false, comment=oracle-registry)
- `A` `k8s.zhangxuemin.work` -> `140.245.33.114` (ttl=1, proxied=false, comment=oracle-registry)
- `A` `kiro-cn.zhangxuemin.work` -> `154.86.30.10` (ttl=1, proxied=false)
- `A` `kiro-rs-cn.zhangxuemin.work` -> `154.86.30.10` (ttl=1, proxied=false)
- `A` `kiro-rs.zhangxuemin.work` -> `158.178.236.241` (ttl=1, proxied=false)
- `A` `kiro.zhangxuemin.work` -> `158.178.236.241` (ttl=1, proxied=false)
- `A` `mail.zhangxuemin.work` -> `140.83.52.216` (ttl=1, proxied=false, comment=oracle-mail web-app host)
- `A` `mcr.zhangxuemin.work` -> `140.245.33.114` (ttl=1, proxied=false)
- `A` `proxy-bak-cn.zhangxuemin.work` -> `154.86.30.10` (ttl=1, proxied=false, comment=cliproxy backup pool CN/HK edge on hk-relay)
- `A` `proxy-bak.zhangxuemin.work` -> `158.178.236.241` (ttl=1, proxied=false, comment=cliproxy backup pool direct/source entry on oracle-proxy)
- `A` `proxy.zhangxuemin.work` -> `158.178.236.241` (ttl=1, proxied=false, comment=oracle-proxy)
- `A` `reverse-cn.zhangxuemin.work` -> `154.86.30.10` (ttl=300, proxied=false, comment=CN/HK SSH edge via hk-relay to oracle-reverse-dev:22)
- `AAAA` `tmail-front.zhangxuemin.work` -> `100::` (ttl=1, proxied=true)
- `AAAA` `tmail.zhangxuemin.work` -> `100::` (ttl=1, proxied=true)
- `MX` `send.zhangxuemin.work` -> `feedback-smtp.ap-northeast-1.amazonses.com` (priority=10, ttl=3600, proxied=false)
- `MX` `zhangxuemin.work` -> `route1.mx.cloudflare.net` (priority=56, ttl=1, proxied=false)
- `MX` `zhangxuemin.work` -> `route2.mx.cloudflare.net` (priority=24, ttl=1, proxied=false)
- `MX` `zhangxuemin.work` -> `route3.mx.cloudflare.net` (priority=98, ttl=1, proxied=false)
- `TXT` `_dmarc.zhangxuemin.work` -> `"v=DMARC1; p=reject; rua=mailto:f7f21e5e0ab844279caa542a187734f0@dmarc-reports.cloudflare.net,mailto:mail@zhangxuemin.work; ruf=mailto:mail@zhangxuemin.work; adkim=s; aspf=s"` (ttl=1, proxied=false, comment=DMARC)
- `TXT` `cf2024-1._domainkey.zhangxuemin.work` -> `"v=DKIM1; h=sha256; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAiweykoi+o48IOGuP7GR3X0MOExCUDY/BCRHoWBnh3rChl7WhdyCxW3jgq1daEjPPqoi7sJvdg5hEQVsgVRQP4DcnQDVjGMbASQtrY4WmB1VebF+RPJB2ECPsEDTpeiI5ZyUAwJaVX7r6bznU67g7LvFq35yIo4sdlmtZGV+i0H4cpYH9+3JJ78k" "m4KXwaf9xUJCWF6nxeD+qG6Fyruw1Qlbds2r85U9dkNDVAS3gioCvELryh1TxKGiVTkg4wqHTyHfWsp7KD3WQHYJn0RyfJJu6YEmL77zonn7p2SRMvTMP3ZEXibnC9gz3nnhR6wcYL8Q7zXypKTMD58bTixDSJwIDAQAB"` (ttl=1, proxied=false)
- `TXT` `send.zhangxuemin.work` -> `"v=spf1 include:amazonses.com ~all"` (ttl=3600, proxied=false)
- `TXT` `zhangxuemin.work` -> `"v=spf1 include:_spf.mx.cloudflare.net ~all"` (ttl=1, proxied=false)


## 2026-06-07 Kiro-RS additions
- `kiro-rs.zhangxuemin.work` A -> `158.178.236.241` (`oracle-proxy`, Kiro-RS source)
- `kiro-rs-cn.zhangxuemin.work` A -> `154.86.30.10` (`hk-relay`, Kiro-RS CN/HK edge)
