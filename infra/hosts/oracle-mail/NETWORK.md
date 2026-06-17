# oracle-mail / NETWORK

## 1. Public Network Identity
- Public IP: `140.83.52.216`
- Primary domain: `mail.zhangxuemin.work`
- Additional active domain: `wa.zhangxuemin.work`
- Retired / no longer live DNS:
  - `autoconfig.zhangxuemin.work`
  - `autodiscover.zhangxuemin.work`

## 2. Current Reachability
Current documented state after the 2026-03-20 repurpose:
- `mail.zhangxuemin.work` is live on this host as the `Outlook Email Plus` web app
- `wa.zhangxuemin.work` is live on this host as the WA app global/source entrypoint
- public `80/443` are owned by the `outlook-email-plus-caddy` container, which fronts both web-app routes
- `autoconfig.zhangxuemin.work` and `autodiscover.zhangxuemin.work` are no longer present in the current Cloudflare live zone; no classic mail protocol stack has been reactivated behind them

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
This host is no longer a dormant mail-stack candidate: runtime now clearly matches active web application hosting for `mail.zhangxuemin.work` and `wa.zhangxuemin.work`, while traditional mail protocols remain intentionally inactive.

## 5. To Be Confirmed
- whether this host will remain a web-app-only mail-adjacent host or later regain classic mail services under a separate plan
