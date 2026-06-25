# oracle-newapi-primary / NETWORK

## Public identity
- Public IP: `140.245.33.114`
- Provider: Oracle Cloud Infrastructure
- Canonical SSH alias: `oracle-newapi-primary`
- Legacy SSH alias: `oracle-registry`
- Planned DNS: `newapi.zhangxuemin.work`
- Active DNS: `ai.zhangxuemin.work`

## Current listener interpretation
Intended listeners after the 2026-06-08 New API deployment:
- `22/tcp` — SSH
- `80/tcp` — Caddy HTTP front door for New API
- `127.0.0.1:13000` — New API container listener, loopback only
- `127.0.0.1:2019` — Caddy admin, loopback only
- system/local control listeners such as DNS stub / rpcbind may remain

## Caddy routing
Current active Caddy routes:
```caddy
:80 -> 127.0.0.1:13000
ai.zhangxuemin.work -> 127.0.0.1:13000
ai.zhangxuemin.work/docs/* -> /opt/new-api-docs
```

Current direct access until DNS/TLS is finalized:
```text
http://140.245.33.114/
```

Active HTTPS route:
```text
https://ai.zhangxuemin.work/
```

Planned/legacy candidate route after DNS points to this host, if still needed:
```text
https://newapi.zhangxuemin.work/
```

## Registry compatibility domains
The former dedicated registry stack was retired on 2026-06-08, but the DNS names themselves remain active A records on this host for compatibility and should not be treated as Cloudflare drift by default:
- `hub.zhangxuemin.work`
- `ghcr.zhangxuemin.work`
- `k8s.zhangxuemin.work`
- `mcr.zhangxuemin.work`

Retired NexusVault monitor mappings:
- `hub.zhangxuemin.work/nvmon/*`
- `140.245.33.114:58080` / `:58080`
- `drop.hk.zhangxuemin.work/nvmon/*`

If the registry compatibility names are ever removed from service, reconcile `infra/dns-reconciliation.md` and `infra/cloudflare-dns/baseline-records.json` before treating the live DNS records as stale.
