# Cloudflare DNS Snapshot

- zone_id: `b68f5785980dfe650ca4cdd7d237254d`
- record_count: 24
- type_counts:
  - A: 12
  - AAAA: 2
  - MX: 4
  - TXT: 6

## Records

- TXT _dmarc.zhangxuemin.work -> "v=DMARC1; p=reject; rua=mailto:f7f21e5e0ab844279caa542a187734f0@dmarc-reports.cloudflare.net,mailto:mail@zhangxuemin.work; ruf=mailto:mail@zhangxuemin.work; adkim=s; aspf=s" proxied=false ttl=1 comment=DMARC
- A backup.zhangxuemin.work -> 129.150.61.78 proxied=false ttl=1 comment=oracle-gateway / hysteria
- TXT cf2024-1._domainkey.zhangxuemin.work -> "v=DKIM1; h=sha256; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAiweykoi+o48IOGuP7GR3X0MOExCUDY/BCRHoWBnh3rChl7WhdyCxW3jgq1daEjPPqoi7sJvdg5hEQVsgVRQP4DcnQDVjGMbASQtrY4WmB1VebF+RPJB2ECPsEDTpeiI5ZyUAwJaVX7r6bznU67g7LvFq35yIo4sdlmtZGV+i0H4cpYH9+3JJ78k" "m4KXwaf9xUJCWF6nxeD+qG6Fyruw1Qlbds2r85U9dkNDVAS3gioCvELryh1TxKGiVTkg4wqHTyHfWsp7KD3WQHYJn0RyfJJu6YEmL77zonn7p2SRMvTMP3ZEXibnC9gz3nnhR6wcYL8Q7zXypKTMD58bTixDSJwIDAQAB" proxied=false ttl=1
- A clash.hk.zhangxuemin.work -> 154.86.30.10 proxied=false ttl=1
- A derp.zhangxuemin.work -> 129.150.61.78 proxied=false ttl=1
- A dev.zhangxuemin.work -> 64.110.106.11 proxied=false ttl=1 comment=openclaw-host
- TXT dkim._domainkey.zhangxuemin.work -> "v=DKIM1; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAq7g3SiXvUIPemirDgkgYiCP3gYBt9UOQbqgWtt5Obz7W+2y0BwuhXTLEfuFcQ+s/iPJvMuvoJqT9REUgCmDmoAkg9QQ3i1ZGFCjFjDQW/SntNfEZ8Ex//FeMsCLgft84V9N8np3Z6fB8EikOMLT2Ye0ZWqMdpS12CtVj2rNjXnGmgKneO1AM7URb2bAX88Kf3" "c8hBnVou9F7qt6c2fgmmSQt/y497LqOOuqa7P+/68pw3t6YDxe1zcIqTv9vA3QBJCMjnVxX7Bt0GlqVqBqOUiUcsll6bIGFA28TA/xN4EvP/gBAvDdCF/4nzgzws5u/S1i2k8mOgxOo0+k7gdyMNwIDAQAB" proxied=false ttl=1 comment=DKIM
- A drop.hk.zhangxuemin.work -> 154.86.30.10 proxied=false ttl=1
- A ghcr.zhangxuemin.work -> 140.245.33.114 proxied=false ttl=1 comment=oracle-registry
- A hk.zhangxuemin.work -> 154.86.30.10 proxied=false ttl=1
- A hub.zhangxuemin.work -> 140.245.33.114 proxied=false ttl=1 comment=oracle-registry
- A k8s.zhangxuemin.work -> 140.245.33.114 proxied=false ttl=1 comment=oracle-registry
- A mail.zhangxuemin.work -> 140.83.52.216 proxied=false ttl=1 comment=oracle-mail web-app host
- A mcr.zhangxuemin.work -> 140.245.33.114 proxied=false ttl=1
- A proxy.zhangxuemin.work -> 158.178.236.241 proxied=false ttl=1 comment=oracle-proxy
- TXT resend._domainkey.zhangxuemin.work -> "p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC9felGPWZikf51CuY9MhwC/5AWucfeOer9FJqnnsOneXey5zjULlubEb9bT3D/8G4/Em5ddoCjFHc+keeTF7rA/VwOjUUAAIVZiK92hkfYmXn2IpVEdu7LjeyRt881ca/E8cgfc5LJIvU6V8ZLP4oor13pOeVsTY9Wh0UtVMvA+wIDAQAB" proxied=false ttl=3600
- MX send.zhangxuemin.work -> feedback-smtp.ap-northeast-1.amazonses.com priority=10 proxied=false ttl=3600
- TXT send.zhangxuemin.work -> "v=spf1 include:amazonses.com ~all" proxied=false ttl=3600
- AAAA tmail-front.zhangxuemin.work -> 100:: proxied=true ttl=1
- AAAA tmail.zhangxuemin.work -> 100:: proxied=true ttl=1
- MX zhangxuemin.work -> route1.mx.cloudflare.net priority=56 proxied=false ttl=1
- MX zhangxuemin.work -> route2.mx.cloudflare.net priority=24 proxied=false ttl=1
- MX zhangxuemin.work -> route3.mx.cloudflare.net priority=98 proxied=false ttl=1
- TXT zhangxuemin.work -> "v=spf1 include:_spf.mx.cloudflare.net ~all" proxied=false ttl=1
