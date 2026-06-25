# Domestic-optimized entrypoints inventory — 2026-05-25 14:43 GMT+8

Scope: list the existing domestic/HK-optimized entrypoints and related Oracle/1Panel/proxy surfaces documented in `infra/`. This is inventory only; no routing changes were made.

## Confirmed `*-cn` HK edge domains

| Domain | DNS target | Edge host | Origin / upstream | Purpose | Validation on 2026-05-25 |
|---|---:|---|---|---|---|
| `cliproxy-cn.zhangxuemin.work` | `154.86.30.10` | `hk-relay` | `proxy.zhangxuemin.work:8317` on `oracle-proxy` | Domestic/HK TLS edge for CLIProxy / OpenAI-compatible API | `/` -> 200, `/v1/models` -> 401 |
| `claw-cn.zhangxuemin.work` | `154.86.30.10` | `hk-relay` | `https://dev.zhangxuemin.work` | Domestic/HK TLS edge for OpenClaw Control UI | `/` -> 401 |
| `cpam-cn.zhangxuemin.work` | `154.86.30.10` | `hk-relay` | `https://cpam.zhangxuemin.work` | Domestic/HK TLS edge for CPA Manager Plus | `/management.html` -> 200 |

Caddy mapping verified on `hk-relay`:

- `cliproxy-cn.zhangxuemin.work` reverse-proxies to `proxy.zhangxuemin.work:8317` and sets `Host: proxy.zhangxuemin.work`.
- `claw-cn.zhangxuemin.work` reverse-proxies to `dev.zhangxuemin.work:443`, sets `Host: dev.zhangxuemin.work`, and uses TLS SNI `dev.zhangxuemin.work`.
- `cpam-cn.zhangxuemin.work` reverse-proxies to `cpam.zhangxuemin.work:443`, sets `Host: cpam.zhangxuemin.work`, and uses TLS SNI `cpam.zhangxuemin.work`.

Policy from existing docs:

- `*-cn.zhangxuemin.work` names are the domestic-optimized HK edge path.
- Existing Oracle/source names remain the global/foreign and machine-to-machine path.
- Do not firewall source services down to HK-only; the direct/global source endpoints are intentional fallbacks if HK is unavailable.

## Global/source domains behind those CN edges

| Domain / endpoint | DNS target | Host | Role | Notes |
|---|---:|---|---|---|
| `proxy.zhangxuemin.work:8317` | `158.178.236.241` | `oracle-proxy` | CLIProxy / `eceasy/cli-proxy-api` OpenAI-compatible API | Direct source/global endpoint; `/v1/models` returns 401 without auth |
| `dev.zhangxuemin.work` | `64.110.106.11` | `oracle-open_claw` / current OpenClaw host | OpenClaw Control UI origin | Direct source/global endpoint; `/` returns 401 |
| `cpam.zhangxuemin.work` | `158.178.236.241` | `oracle-proxy` | CPA Manager Plus / Manager Server | Direct source/global endpoint; `/management.html` returns 200 |

## Oracle / 1Panel-related surfaces in infra

| Host | IP | Domain(s) | 1Panel status in docs | Domestic optimization relation |
|---|---:|---|---|---|
| `oracle-proxy` | `158.178.236.241` | `proxy.zhangxuemin.work` | Public `:80` currently observed as owned by `1panel`; older nginx-only notes are stale | Its CLIProxy origin `:8317` is fronted by `cliproxy-cn.zhangxuemin.work` through HK |
| `oracle-open_claw` / OpenClaw origin | `64.110.106.11` | `dev.zhangxuemin.work` | Not documented as 1Panel in current infra excerpt | Origin is fronted by `claw-cn.zhangxuemin.work` through HK |
| `oracle-gateway` | `129.150.61.78` | `backup.zhangxuemin.work` | Not a 1Panel app host; focused gateway role | Used as Oracle Hysteria backup / egress path, not a `*-cn` web edge |
| `oracle-registry` | `140.245.33.114` | `hub.zhangxuemin.work`, `ghcr.zhangxuemin.work`, `k8s.zhangxuemin.work` | Not listed as 1Panel in current docs | Registry mirrors; no documented HK/CN edge domain found |
| `oracle-mail` | `140.83.52.216` | `mail.zhangxuemin.work` | Not listed as current 1Panel in current docs | Outlook Email Plus web app; no documented HK/CN edge domain found |
| `oracle-reverse-dev` | `140.245.61.236` | none found in Cloudflare baseline | Not listed as 1Panel in current docs | No documented HK/CN edge domain found |

## Alibaba Cloud domestic gateway

| Host | IP / endpoint | Purpose | Notes |
|---|---:|---|---|
| `ali-cloud` | `106.15.239.221:2080` SOCKS5, `:2081` HTTP | Domestic explicit-proxy gateway for other domestic servers | Authenticated public ingress; central selector currently defaults to `oracle-egress` |
| `ali-cloud` | host port `80` | 1Panel control-plane host | 1Panel is installed under `/opt/1panel`; EasyImages is 1Panel-managed |

Selector helper documented on `ali-cloud`:

```bash
/usr/local/bin/ali-cloud-proxy-select status
/usr/local/bin/ali-cloud-proxy-select oracle-egress|hk-hy2|hk-reality|hk-socks|hk-http
```

Current documented default: `oracle-egress`.

## SSH via HK aliases

Existing local SSH config includes HK ProxyJump aliases for domestic/HK-assisted operations:

- `oracle-proxy-via-hk`
- `oracle-openclaw-via-hk` / `oracle-open_claw-via-hk`
- `oracle-gateway-via-hk`
- `oracle-mail-via-hk`
- `oracle-registry-via-hk`
- `oracle-reverse-dev-via-hk`

These are client-side `ProxyJump hk-relay` helpers, not public per-host HK TCP ports.

## Quick validation results from OpenClaw host

```text
https://cliproxy-cn.zhangxuemin.work/           -> 200, remote_ip=154.86.30.10
https://cliproxy-cn.zhangxuemin.work/v1/models -> 401, remote_ip=154.86.30.10
https://claw-cn.zhangxuemin.work/              -> 401, remote_ip=154.86.30.10
https://cpam.zhangxuemin.work/management.html  -> 200, remote_ip=158.178.236.241
https://cpam-cn.zhangxuemin.work/management.html -> 200, remote_ip=154.86.30.10
http://proxy.zhangxuemin.work:8317/v1/models   -> 401, remote_ip=158.178.236.241
https://dev.zhangxuemin.work/                  -> 401, remote_ip=64.110.106.11
http://proxy.zhangxuemin.work:80/              -> 200, remote_ip=158.178.236.241
```

## Gaps / likely next inventory pass

- `oracle-proxy` still needs a fuller machine-level 1Panel/network-front-door audit: current docs say `:80` is owned by `1panel`, but project-level reverse-proxy ownership for all app domains is not fully mapped.
- `oracle-registry`, `oracle-mail`, and `oracle-reverse-dev` have no documented `*-cn` optimized web edge; if they should have domestic optimized domains, those would be new design work rather than current infra state.
- If `cli-proxy-api` should be the naming pattern, the current optimized name is `cliproxy-cn.zhangxuemin.work`, not `cli-proxy-api-cn...`.
