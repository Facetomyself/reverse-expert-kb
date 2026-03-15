# oracle-docker-proxy / CHANGELOG

- 2026-03-15: Created placeholder host documentation from Cloudflare DNS export only. No SSH verification yet. Initial mapping suggests `129.150.61.78` is a shared `docker_proxy` host serving multiple `*.zhangxuemin.work` names including registry-related endpoints and a UI endpoint.
- 2026-03-15: External probe pass confirmed this host group is fronted by Caddy: `hub`, `ghcr`, `gcr`, and `quay` return `HTTP 200` with `server: Caddy`; `ui.zhangxuemin.work` currently returns `HTTP 502` from Caddy. SSH transport is reachable, but `root@129.150.61.78` failed with `Permission denied (publickey,password)`, so on-host validation still requires the correct user/key.
