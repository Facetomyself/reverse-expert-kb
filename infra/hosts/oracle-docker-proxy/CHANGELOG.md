# oracle-docker-proxy / CHANGELOG

- 2026-03-15: Created placeholder host documentation from Cloudflare DNS export only. No SSH verification yet. Initial mapping suggests `129.150.61.78` is a shared `docker_proxy` host serving multiple `*.zhangxuemin.work` names including registry-related endpoints and a UI endpoint.
- 2026-03-15: External probe pass confirmed this host group is fronted by Caddy: `hub`, `ghcr`, `gcr`, and `quay` return `HTTP 200` with `server: Caddy`; `ui.zhangxuemin.work` currently returns `HTTP 502` from Caddy.
- 2026-03-15: Confirmed actual SSH entry via local alias `oracle-docker_proxy` with key `~/.ssh/oracle-docker_proxy`. On-host inspection verified `24-7-10-2055` (Ubuntu 20.04.6, x86_64) runs Caddy on `80/443`, Caddy admin on `127.0.0.1:2019`, and a set of long-lived Docker registry proxy containers mapped through `/etc/caddy/Caddyfile`. Also confirmed the `ui` backend issue is not just edge-facing: local access to `127.0.0.1:50000` resets the connection.
