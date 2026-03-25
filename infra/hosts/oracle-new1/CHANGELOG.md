# oracle-new1 / CHANGELOG

- 2026-03-25: Fresh Oracle ARM host (`140.245.33.114`) reached over SSH after OCI-side IPv4 ingress and internet-path fixes.
- 2026-03-25: Base environment installed: common ops tools, Python runtime/build packages, Docker Engine + Compose v2, and persistent 2G swap.
- 2026-03-25: Migrated live registry-proxy front door from `oracle-docker-proxy` to this host. New live public domains are `hub.zhangxuemin.work`, `ghcr.zhangxuemin.work`, `k8s.zhangxuemin.work`, and `mcr.zhangxuemin.work`.
- 2026-03-25: During cutover, local iptables initially allowed only SSH; adding and persisting `80/tcp` and `443/tcp` fixed ACME issuance and public service reachability.
- 2026-03-25: Installed local health-check helper `/usr/local/bin/check-registry-proxies` to validate both local backend ports and public HTTPS `/v2/` responses for the four registry domains.
