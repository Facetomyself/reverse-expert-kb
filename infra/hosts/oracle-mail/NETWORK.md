# oracle-mail / NETWORK

## 1. Public Network Identity
- Public IP: `140.83.52.216`
- Primary domain: `mail.zhangxuemin.work`
- Related DNS:
  - `autoconfig.zhangxuemin.work` -> CNAME to `mail.zhangxuemin.work`
  - `autodiscover.zhangxuemin.work` -> CNAME to `mail.zhangxuemin.work`
  - `dreamhorse.eu.cc` -> A `140.83.52.216`
  - `www.dreamhorse.eu.cc` -> A `140.83.52.216`
  - `zhangxuemin.eu.cc` -> A `140.83.52.216`
  - `www.zhangxuemin.eu.cc` -> A `140.83.52.216`
  - `mengma.eu.cc` -> A `140.83.52.216`
  - `www.mengma.eu.cc` -> A `140.83.52.216`

## 2. Current Reachability
Current documented state after the 2026-03-20 repurpose:
- `mail.zhangxuemin.work` is live on this host as the `Outlook Email Plus` web app
- public `80/443` are owned by the `outlook-email-plus-caddy` container
- `dreamhorse.eu.cc` is now also live on this host as the public browser entrypoint for the `rbot` / `Radiance OCI Bot` web UI, fronted by the same Caddy instance and reverse-proxied to local `https://140.83.52.216:9527`
- `autoconfig.zhangxuemin.work` and `autodiscover.zhangxuemin.work` still resolve here via CNAME, but no classic mail protocol stack has been reactivated behind them

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
- whether `autoconfig` / `autodiscover` should later receive explicit app-aware handling or redirects
- whether this host will remain a web-app-only mail-adjacent host or later regain classic mail services under a separate plan
