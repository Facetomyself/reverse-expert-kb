# oracle-mail / NETWORK

## 1. Public Network Identity
- Public IP: `140.83.52.216`
- Primary domain: `mail.zhangxuemin.work`
- Additional active domain: `wa.zhangxuemin.work`
- FileCodeBox CN/HK edge domain: `drop-cn.zhangxuemin.work` (DNS points to `hk-relay`, origin service on this host)
- Retired / no longer live DNS:
  - `autoconfig.zhangxuemin.work`
  - `autodiscover.zhangxuemin.work`

## 2. Current Reachability
Current documented state after the 2026-03-20 repurpose:
- `mail.zhangxuemin.work` is live on this host as the `Outlook Email Plus` web app
- `wa.zhangxuemin.work` is live on this host as the WA app global/source entrypoint
- FileCodeBox is live as an origin service on `18085/tcp`; the intended browser entry is `https://drop-cn.zhangxuemin.work/` via `hk-relay` Caddy Basic Auth
- public `80/443` are owned by the `outlook-email-plus-caddy` container, which fronts both web-app routes
- `autoconfig.zhangxuemin.work` and `autodiscover.zhangxuemin.work` are no longer present in the current Cloudflare live zone; no classic mail protocol stack has been reactivated behind them

## 3. On-Host Listener Reality
Currently listening services include:
- `22/tcp` (SSH)
- `80/tcp` (Caddy container)
- `443/tcp` + `443/udp` (Caddy container with HTTPS/HTTP3)
- `111/tcp` (rpcbind)
- `18085/tcp` (FileCodeBox origin, iptables-restricted to `154.86.30.10` plus localhost)
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
