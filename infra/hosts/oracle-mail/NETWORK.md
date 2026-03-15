# oracle-mail / NETWORK

## 1. Public Network Identity
- Public IP: `140.83.52.216`
- Primary domain: `mail.zhangxuemin.work`
- Related DNS:
  - `autoconfig.zhangxuemin.work` -> CNAME to `mail.zhangxuemin.work`
  - `autodiscover.zhangxuemin.work` -> CNAME to `mail.zhangxuemin.work`

## 2. Current Reachability
Observed externally on 2026-03-15:
- `https://mail.zhangxuemin.work` -> connection refused on `443`
- `https://autoconfig.zhangxuemin.work` -> `HTTP 521` from Cloudflare
- `https://autodiscover.zhangxuemin.work` -> `HTTP 521` from Cloudflare

## 3. On-Host Listener Reality
Currently listening services are minimal:
- `22/tcp` (SSH)
- `111/tcp` (rpcbind)
- local PCP monitoring ports

No current listeners observed for:
- `80/443`
- `25/465/587`
- `110/995`
- `143/993`
- `4190`

## 4. Interpretation
DNS says this should be a mail host, but runtime says the intended mail/web stack is currently not active.

## 5. To Be Confirmed
- whether Mailu was intentionally shut down
- whether this host is waiting for manual bring-up
- whether some external dependency (certs, DNS, storage migration) blocked activation
