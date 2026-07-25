# oracle-newapi-standby / NETWORK

## Public identity
- Public IP: `140.245.61.236`
- Provider: Oracle Cloud Infrastructure
- Canonical SSH alias: `oracle-newapi-standby`
- Legacy SSH alias: `oracle-reverse-dev`
- Former DNS purpose: `newapi-standby.zhangxuemin.work` (New API standby retired 2026-07-07)
- Active Sub2API global/source domain: `sub2api.zhangxuemin.work`
- Active Sub2API CN/HK edge domain: `sub2api-cn.zhangxuemin.work`
- Existing HK SSH edge domain: `reverse-cn.zhangxuemin.work`

## SSH access paths

### Direct / global path
```bash
ssh oracle-newapi-standby
# legacy compatibility alias still works:
ssh oracle-reverse-dev
```

### Domestic/HK optimized edge path
Existing SSH edge retained for compatibility:
```bash
ssh -p 22061 ubuntu@reverse-cn.zhangxuemin.work
ssh oracle-reverse-dev-cn
ssh reverse-cn
```

Runtime topology:
- Cloudflare DNS-only A: `reverse-cn.zhangxuemin.work` -> `154.86.30.10` (`hk-relay`)
- `hk-relay` systemd service: `oracle-reverse-dev-ssh-edge.service` (legacy name)
- public listener on HK relay: `0.0.0.0:22061`
- TCP target: `140.245.61.236:22` (`oracle-newapi-standby` SSH)

## Current listener interpretation
Intended listeners after the 2026-07-22 Sub2API deployment:
- `22/tcp` — SSH
- `80/tcp` — Caddy HTTP redirect / ACME
- `443/tcp` — Caddy HTTPS for `sub2api.zhangxuemin.work`
- `127.0.0.1:18088/tcp` — Sub2API origin app, Docker-published loopback-only
- system/local control listeners such as DNS stub / rpcbind may remain

Public project listeners:
- `80/tcp` and `443/tcp` through Caddy only

Removed project listeners:
- `127.0.0.1:13000` New API container listener is gone
- legacy `127.0.0.1:8888` Python/GPT helper listener is gone

## Caddy state
Caddy is active. `/etc/caddy/Caddyfile` serves `sub2api.zhangxuemin.work` and reverse-proxies to `127.0.0.1:18088`.

## Sub2API dual-channel topology
- Global/source path: `https://sub2api.zhangxuemin.work` -> `oracle-newapi-standby` Caddy -> `127.0.0.1:18088`.
- Domestic/CN optimized path: `https://sub2api-cn.zhangxuemin.work` -> `hk-relay` Caddy -> `https://sub2api.zhangxuemin.work`.
- DNS:
  - `sub2api.zhangxuemin.work A 140.245.61.236` DNS-only
  - `sub2api-cn.zhangxuemin.work A 154.86.30.10` DNS-only
- Origin iptables note: deployment found `443/tcp` missing from the accepted INPUT rules; an explicit `443/tcp` ACCEPT was inserted before the final `REJECT --reject-with icmp-host-prohibited` rule.

## CTF GPT Plus / HK edge compatibility
Older docs recorded a domestic/HK optimized edge for `https://ctf-gpt-cn.zhangxuemin.work/ctf-gpt-plus` pointing through `hk-relay` to this host. As of the 2026-07-07 cleanup, this host no longer has the origin app/listener for that route. Treat any remaining DNS/HK-relay config as stale edge configuration until deliberately rebuilt or removed in a coordinated DNS/relay cleanup.
