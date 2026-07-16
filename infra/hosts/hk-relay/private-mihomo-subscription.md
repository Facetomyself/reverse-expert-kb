# hk-relay private Mihomo subscription

Updated: 2026-06-29

## Purpose

This document describes the managed private Mihomo / Clash.Meta subscription served from `clash.hk.zhangxuemin.work` behind a randomized private path.

The exact randomized path is intentionally not recorded here. Treat it as a credential.

## Current shape

The private subscription is the richer client-facing policy track. It is distinct from the smaller tracked compatibility examples under `hosts/hk-relay/clash-*.yaml`.

Current validated contents after the 2026-05-25 refresh:

- proxies: 14
- proxy groups: 14
- rule providers: 15
- rules: 54

A newer clean consumer-facing track was then added on 2026-05-30. It reuses the same routing policy family but exposes a smaller set of human-friendly nodes/groups for day-to-day use. Important: home-exit nodes in the clean track must preserve `dialer-proxy` chaining through HK; direct home-exit tests from the OpenClaw host do not prove end-user clients can reach the home proxy directly. The `oracle-gateway` Hysteria node should be presented as `新加坡 01` in the clean track, not as a generic backup node.

On 2026-06-29, the published tracks were rechecked after connection resets/timeouts against Anthropic through the `AI账号` / home-exit path. The clean track's `家庭出口 01` node already used `dialer-proxy: 香港 02`; the full/operator track was normalized so every HTTP home-exit entry for the same home proxy is chained through its HK transit selector instead of leaving any direct home-exit entry.

Major groups:

- `Proxy` — default foreign traffic selector; first entry is `Proxy-Auto`.
- `Proxy-Auto` — general automatic pool, intentionally narrower than “all nodes”.
- `HK` / `HK-Auto` — HK-only manual and automatic groups.
- `HK-Transit` / `HK-Transit-Auto` — upstream group for chained home-exit nodes via `dialer-proxy`.
- `Home-Egress` / `Home-Egress-Auto` — account-sensitive AI/login traffic only.
- `Oracle-Proxy-Extra` / `Oracle-Proxy-Extra-Auto` — fallback pack from `oracle-proxy`.
- `Fallback` / `Fallback-Auto` — ordered non-primary fallback pool.
- `Big-Transfer` / `Big-Transfer-Auto` — model/package/image/large-download biased pool.

## Rule-provider layer

The 2026-05-25 refresh added MetaCubeX `meta-rules-dat` MRS providers for broad maintained categories:

- `geosite-private` -> DIRECT
- `geoip-private` -> DIRECT
- `geosite-cn` -> DIRECT
- `geoip-cn` -> DIRECT
- `ai-non-cn` -> `Home-Egress`
- `dev` -> `Proxy`
- `github` -> `Proxy`
- `google` -> `Proxy`
- `cloudflare` -> `Proxy`
- `docker` -> `Big-Transfer`
- `npmjs` -> `Big-Transfer`
- `python` -> `Big-Transfer`
- `telegram` -> `Proxy`
- `discord` -> `Proxy`
- `youtube` -> `Proxy`

Provider interval is currently `86400` seconds. Providers are configured to download through `Proxy` so clients in restrictive networks do not depend on raw GitHub direct reachability.

## Manual override policy

Manual rules still sit above broad providers for personal routing semantics:

- OpenAI / ChatGPT / Claude / Anthropic / x.ai / Grok -> `Home-Egress`
- Hugging Face, GitHub release objects, Docker/GHCR/Quay, npm, PyPI, Python package hosts -> `Big-Transfer`
- selected dev/CDN surfaces -> `Proxy`

Private/local rules are first, before account/download/foreign rules.

## Client defaults

The private track now carries:

- `mode: rule`
- `unified-delay: true`
- `tcp-concurrent: true`
- `profile.store-selected: true`
- `profile.store-fake-ip: true`
- `dns.enhanced-mode: fake-ip`
- a conservative `fake-ip-filter` for LAN/NTP/connectivity-check names

## Health check

A lightweight credential-redacting helper exists at:

```bash
infra/scripts/proxy-health-check.py
```

It reads a Mihomo YAML file and tests explicit HTTP/SOCKS nodes via curl. It does not print proxy credentials. Protocols that require a Mihomo core, such as Hysteria2, VLESS Reality, TUIC, Trojan, and Shadowsocks, are skipped by the lightweight checker unless separately tested with a real Mihomo core.

Example local run against the generated private draft:

```bash
infra/scripts/proxy-health-check.py --config /root/.openclaw/workspace/_tmp_live_private_clash_meta_v4.yaml --timeout 15
```

2026-05-25 smoke-test result from the OpenClaw host:

- `hk-socks` -> ok, egress `154.86.30.10`
- `hk-http` -> ok, egress `154.86.30.10`
- `home-http-via-hk` -> ok, egress `204.237.153.49`
- `home-http-direct` -> ok, egress `204.237.153.49`
- `ali-http-oracle-egress` -> ok, egress `129.150.61.78`
- `ali-socks-oracle-egress` -> ok at 15s timeout; one 8s run timed out, so keep watching this path before treating it as low-latency

## Deployment notes

The 2026-05-25 update was deployed only to the randomized private path on `hk-relay`. The legacy public root paths should remain disabled/404 as documented in `NETWORK.md`.

Deployment created a timestamped backup beside the private `clash-meta.yaml` before replacing it.

## Next checks

- Test the private subscription in a real Mihomo client/core so MRS provider download and non-curl protocols are validated end-to-end.
- Consider a small scheduled health report before changing `ali-cloud`'s default selector away from `oracle-egress`.
- Keep `Home-Egress` narrow unless there is explicit evidence a site needs account-sensitive routing.
