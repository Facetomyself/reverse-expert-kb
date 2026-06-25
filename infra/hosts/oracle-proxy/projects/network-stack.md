# Machine Network Stack (nginx / sing-box / xray / cloudflared)

## 1. Summary
- Scope: host-level network and proxy services on `oracle-proxy`
- Purpose: 解释这台机器上非业务项目的入口层、代理层和订阅层
- Status: partially documented, second-pass complete
- Priority: Infra

## 2. Components
### System nginx
- systemd unit: `nginx.service`
- current enabled site: `/etc/nginx/sites-enabled/default`
- current role at snapshot: Debian default static site on port 80
- no custom reverse-proxy map identified in this pass

### sing-box
- systemd unit: `sing-box.service`
- binary path: `/etc/sing-box/sing-box`
- config dir: `/etc/sing-box/conf/`
- related files:
  - `/etc/sing-box/nginx.conf`
  - `/etc/sing-box/subscribe/*`
  - `/etc/sing-box/cert/cert.pem`
  - `/etc/sing-box/cert/private.key`
- likely role: proxy/relay/subscription distribution stack

### xray
- systemd unit: `xray.service`
- binary path: `/etc/v2ray-agent/xray/xray`
- config dir root: `/etc/v2ray-agent/xray/conf`
- observed active ports: `14391`, `127.0.0.1:45987`
- logs indicate accepted traffic forwarded to local `127.0.0.1:45987`

### cloudflared
- evidence: local listener previously observed on `127.0.0.1:20241`
- this pass did not recover a full config file or unit status details
- likely role: tunnel / edge transport helper

## 3. Ports and Ownership
| Port | Owner | Notes |
|---|---|---|
| 80 | system nginx / 1panel path | default site currently observed |
| 30001, 30004-30011 | sing-box | multi-protocol or subscription-related |
| 14391 | xray | public listener |
| 127.0.0.1:45987 | xray | local listener used in forwarding |
| 127.0.0.1:20241 | cloudflared | local-only observed |

## 4. Operational Checks
### nginx
```bash
ssh oracle-proxy
systemctl status nginx --no-pager -l
sed -n '1,140p' /etc/nginx/sites-enabled/default
```

### sing-box
```bash
ssh oracle-proxy
systemctl status sing-box --no-pager -l
find /etc/sing-box -maxdepth 2 -type f | sort
ss -ltnp | grep -E '30001|3000[4-9]|30010|30011'
```

### xray
```bash
ssh oracle-proxy
systemctl status xray --no-pager -l
ss -ltnp | grep -E '14391|45987'
journalctl -u xray -n 100 --no-pager
```

### cloudflared
```bash
ssh oracle-proxy
systemctl status cloudflared --no-pager -l
ss -ltnp | grep 20241
find /etc/cloudflared -maxdepth 2 -type f
```

## 5. Verified protocol snapshot (2026-04-21)
A later external Mihomo validation pass turned part of the previously fuzzy protocol surface into confirmed working candidates.

### Confirmed working sing-box inbounds
- `30002/udp` -> `hysteria2`
- `30003/udp` -> `tuic`
- `30005/tcp+udp` -> `shadowsocks`
- `30006/tcp+udp` -> `trojan`

### Confirmed working Xray inbound
- `14391/tcp` -> `VLESS Reality Vision`

Validation outcome:
- each of the above produced external egress IP `158.178.236.241` from a fresh Mihomo client smoke test
- this means the host still retains a usable multi-protocol fallback pool even though only a smaller subset may be published in day-to-day managed subscriptions
- operator-facing usage details, connection snippets, and recommended order now live in `./proxy-fallback-pool.md`

### Still unconfirmed / not promoted yet
The following surfaces were observed in config but were not promoted as default subscription inventory in this pass:
- `30001` sing-box `xtls-reality`
- `30004` `ShadowTLS`
- `30007` `vmess-ws`
- `30008` `vless-ws-tls`
- `30009` `h2-reality`
- `30010` `grpc-reality`

## 6. What is still unknown
- full sing-box protocol matrix and public subscription semantics beyond the now-verified subset
- exact xray inbound/outbound config graph beyond the confirmed `14391 -> 127.0.0.1:45987` reality chain
- whether system nginx is actually in the active public request path or just left installed with defaults
- exact cloudflared tunnel target(s)

## 7. Change History
- 2026-03-15: created dedicated machine-level network stack note during oracle-proxy second-pass documentation
- 2026-04-21: appended a verified external-protocol snapshot after Mihomo smoke tests confirmed working `hysteria2`, `tuic`, `shadowsocks`, `trojan`, and Xray `VLESS Reality Vision` paths
