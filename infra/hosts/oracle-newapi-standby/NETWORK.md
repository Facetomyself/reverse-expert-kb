# oracle-newapi-standby / NETWORK

## Public identity
- Public IP: `140.245.61.236`
- Provider: Oracle Cloud Infrastructure
- Canonical SSH alias: `oracle-newapi-standby`
- Legacy SSH alias: `oracle-reverse-dev`
- Planned DNS: `newapi-standby.zhangxuemin.work`
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
Intended listeners after the 2026-06-08 New API deployment:
- `22/tcp` — SSH
- `80/tcp` — Caddy HTTP front door for New API; host iptables explicitly allows new TCP/80 before the final reject rule and was persisted with `netfilter-persistent` on 2026-06-08
- `127.0.0.1:13000` — New API container listener, loopback only
- `127.0.0.1:2019` — Caddy admin, loopback only
- system/local control listeners such as DNS stub / rpcbind may remain

## Caddy routing
Current active Caddy route:
```caddy
:80 -> 127.0.0.1:13000
```

Current direct access until DNS/TLS is finalized:
```text
http://140.245.61.236/
```

Planned HTTPS route after DNS points to this host:
```text
https://newapi-standby.zhangxuemin.work/
```

## CTF GPT Plus / HK edge compatibility
The direct CTF GPT Plus app origin on this host was de-emphasized during the 2026-06-08 cleanup, but the HK/Cloudflare edge name remains in the current live DNS baseline and reconciliation docs:
- domestic/HK optimized edge: `https://ctf-gpt-cn.zhangxuemin.work/ctf-gpt-plus`
- live DNS: `ctf-gpt-cn.zhangxuemin.work` -> `154.86.30.10` (`hk-relay`)
- documented HK route: `hk-relay` forwards the HTTPS edge to `http://140.245.61.236:8000/ctf-gpt-plus`

Treat future cleanup of this edge as a coordinated DNS + HK relay + service-state decision, not as suspicious live DNS drift by itself.
