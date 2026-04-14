# oracle-mail / NETWORK

## 1. Public Network Identity
- Public IP: `140.83.52.216`
- Primary domain: `mail.zhangxuemin.work`
- Historical helper names once associated with this host:
  - `autoconfig.zhangxuemin.work`
  - `autodiscover.zhangxuemin.work`
- As of the 2026-04-14 live Cloudflare snapshot, those helper names are **not present** in the current live zone.

## 2. Current Reachability
Current documented state after the 2026-03-20 repurpose:
- `mail.zhangxuemin.work` is live on this host as the `Outlook Email Plus` web app
- public `80/443` are owned by the `outlook-email-plus-caddy` container
- `autoconfig.zhangxuemin.work` and `autodiscover.zhangxuemin.work` are no longer present in the current live Cloudflare zone; classic mail protocol stack has not been reactivated behind any equivalent discovery names

## 3. On-Host Listener Reality
Currently listening services include:
- `22/tcp` (SSH)
- `80/tcp` (Caddy container)
- `443/tcp` + `443/udp` (Caddy container with HTTPS/HTTP3)
- `111/tcp` (rpcbind)
- local PCP monitoring ports

Still not observed / not reactivated as of 2026-03-24:
- `25/465/587`
- `110/995`
- `143/993`
- `4190`

## 4. Interpretation
This host is no longer a dormant mail-stack candidate: runtime now clearly matches an active web application host for `mail.zhangxuemin.work`, while traditional mail protocols remain intentionally inactive.

## 5. To Be Confirmed
- whether `autoconfig` / `autodiscover` should later be reintroduced with explicit app-aware handling or redirects
- whether this host will remain a web-app-only mail-adjacent host or later regain classic mail services under a separate plan
- whether any remaining root-domain DKIM records should continue to exist independently of current provider-side / external sending paths
