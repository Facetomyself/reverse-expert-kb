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

## 5. What is still unknown
- full sing-box protocol matrix and public subscription semantics
- exact xray inbound/outbound config graph
- whether system nginx is actually in the active public request path or just left installed with defaults
- exact cloudflared tunnel target(s)

## 6. Change History
- 2026-03-15: created dedicated machine-level network stack note during oracle-proxy second-pass documentation
