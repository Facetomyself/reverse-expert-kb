# oracle-newapi-standby / NETWORK

## Public identity
- Public IP: `140.245.61.236`
- Provider: Oracle Cloud Infrastructure
- Canonical SSH alias: `oracle-newapi-standby`
- Legacy SSH alias: `oracle-reverse-dev`
- Former DNS purpose: `newapi-standby.zhangxuemin.work` (New API standby retired 2026-07-07)
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
Intended listeners after the 2026-07-07 cleanup:
- `22/tcp` — SSH
- system/local control listeners such as DNS stub / rpcbind may remain

Public project listeners after cleanup:
- none

Removed project listeners:
- `80/tcp` Caddy front door for New API is no longer active
- `127.0.0.1:13000` New API container listener is gone
- `127.0.0.1:2019` Caddy admin is gone while Caddy is stopped
- legacy `127.0.0.1:8888` Python/GPT helper listener is gone

## Caddy state
Caddy is installed but stopped and disabled. `/etc/caddy/Caddyfile` is intentionally empty except for a cleanup note; the previous project Caddyfile was saved on-host as `/etc/caddy/Caddyfile.retired-20260707`.

## CTF GPT Plus / HK edge compatibility
Older docs recorded a domestic/HK optimized edge for `https://ctf-gpt-cn.zhangxuemin.work/ctf-gpt-plus` pointing through `hk-relay` to this host. As of the 2026-07-07 cleanup, this host no longer has the origin app/listener for that route. Treat any remaining DNS/HK-relay config as stale edge configuration until deliberately rebuilt or removed in a coordinated DNS/relay cleanup.
