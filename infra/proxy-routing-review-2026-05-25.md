# Proxy routing review — 2026-05-25

## Scope
Review the current proxy / Clash / Mihomo design from `infra/` and live read-only checks, then compare with current Mihomo/sing-box guidance and multi-source search results.

## Current local facts

### Fleet shape
- `hk-relay` remains the HK optimized relay and exposes HTTP/SOCKS + Reality + Hysteria2, with an 800G/month bidirectional traffic cap.
- `ali-cloud` remains the domestic explicit-proxy gateway on authenticated `:2080`/`:2081`.
- `ali-cloud` already has a selector helper, but its current default is still `oracle-egress`.
- `oracle-proxy` has several extra public proxy protocol candidates verified in earlier docs and still has relevant listeners live.
- The private Mihomo draft already has richer groups than the tracked public `hosts/hk-relay/clash-meta.yaml`, including `Proxy-Auto`, `Home-Egress`, `Oracle-Proxy-Extra`, `Fallback-Auto`, and `Big-Transfer-Auto`.

### Live read-only check on 2026-05-25
- `ali-cloud` reachable; `/usr/local/bin/ali-cloud-proxy-select status` returned `oracle-egress`.
- `hk-relay` reachable; expected sing-box/Caddy/dufs listener surface still present.
- `oracle-gateway` reachable; Hysteria UDP `443` and helper web surfaces still present.
- `oracle-proxy` reachable; sing-box/xray/hysteria-related listeners still present.
- Simple curl smoke tests through explicit HTTP/SOCKS nodes succeeded for:
  - HK HTTP/SOCKS
  - Ali HTTP/SOCKS gateway
  - home HTTP direct exit

## External references checked
- Mihomo official docs: rules are matched top-to-bottom; if a UDP request matches a node without UDP support, matching can continue downward. This matters for mixed HTTP/SOCKS/HY2 groups.
- Mihomo official docs: `rule-providers` support `http/file/inline`, `domain/ipcidr/classical`, `yaml/text/mrs`, update intervals, and downloading through a specified proxy.
- Mihomo official docs: `url-test` selects by latency with `tolerance`; `fallback` selects the first available node in configured order after timeout.
- Mihomo official docs: `profile.store-selected` and `profile.store-fake-ip` exist and are useful for client UX/stability.
- sing-box official docs: Hysteria2 is QUIC-based and good under packet loss, but UDP-based proxies can have more obvious traffic characteristics than TCP-based proxies.
- Multi-source search also surfaced a practical point from the Mihomo issue tracker: after a rule chooses a proxy group, the group can only choose among members using its own strategy. In practice, the rule taxonomy and group taxonomy must be designed together, not independently.

## Diagnosis
The existing direction is not wrong, but it is over-manual and under-layered:

1. **Tracked public `clash-meta.yaml` is too small and manual.** It has only a few hard-coded domain suffix rules and manual groups. The richer private draft is closer to the desired shape, but it still needs cleanup and promotion into the managed artifact flow.
2. **HK optimized bandwidth is not being exploited by default.** `ali-cloud` still defaults to `oracle-egress`, and the client-side `Proxy` group can choose HK, Oracle, Ali, and home exits without an explicit cost/traffic policy.
3. **Rule coverage is fragile.** The current rules cover major AI/dev domains manually, but miss common categories that are better handled by maintained rule sets: `geosite/private`, `geosite/cn`, `geoip/private`, `geoip/cn`, category AI, Microsoft/Apple/Google split, Telegram/Discord/YouTube, package registries, model/download CDNs.
4. **Large-transfer policy is not sharp enough.** HF is routed to `Big-Transfer`, but GitHub release assets, model CDNs, Docker layers, npm/PyPI package downloads, and generic CDNs can still hit the everyday group.
5. **Home-Egress is useful but should be narrow.** It is best for login-sensitive / account-risk-sensitive AI sites, not as a general default; otherwise it becomes a latency and reliability bottleneck.
6. **Protocol diversity exists but is not presented as a failure-domain model.** Current nodes mix HK direct, HK chained, Oracle, Ali, and home exits, but groups should encode failure domains: `HK-fast`, `TCP-stealth`, `Oracle-fallback`, `Home-account`, `Big-transfer`.

## Recommended stable design

### 1. Keep two planes instead of one huge magic config

#### Domestic server plane
Use `ali-cloud` as the centralized explicit-proxy selector for domestic servers that already consume `:2080/:2081`.

Recommended default:
- Keep `oracle-egress` as conservative fallback.
- Add a scheduled or manual health report for `hk-hy2`, `hk-reality`, `hk-socks`, `hk-http`.
- If HK proves stable for a week, switch everyday default to `hk-reality` or `hk-hy2`; keep `oracle-egress` as one-command rollback.

Reason: this avoids rolling a local Mihomo runtime to every domestic Linux host before the control plane is proven.

#### End-user / desktop plane
Use Mihomo subscription for phones/desktops/home endpoints, with clear strategy groups and rule-providers.

### 2. Main Mihomo group taxonomy

Recommended groups:
- `Proxy`: default foreign traffic; first entry `Proxy-Auto`; manual choices after it.
- `Proxy-Auto`: `url-test`; include stable low-cost nodes only, not every exotic fallback.
- `HK`: HK-only manual group.
- `HK-Auto`: HK-only `url-test`.
- `Home-Egress`: manual + fallback; only for login-sensitive AI/account sites.
- `Oracle-Proxy-Extra`: fallback pool for Oracle proxy host protocols.
- `Big-Transfer`: download/model/package registry group; prefer cheaper/less account-sensitive exits.
- `Fallback`: ordered failover group; first available in priority order.
- Optional `Streaming` / `Media`: only if actual media workload appears.

### 3. Rule strategy

Use three layers:

1. **Safety/direct first**
   - private/local/reserved CIDRs direct with `no-resolve`
   - `GEOSITE,private,DIRECT`
   - `GEOIP,private,DIRECT,no-resolve`
   - `GEOSITE,CN,DIRECT`
   - `GEOIP,CN,DIRECT`

2. **High-value explicit overrides**
   - AI/account: OpenAI/ChatGPT/Anthropic/Claude/x.ai/Grok -> `Home-Egress`
   - dev/control: GitHub/GitLab/Google/Cloudflare/Tailscale-like infra -> `Proxy`
   - model/package transfer: Hugging Face, HF CDN/LFS, Docker/ghcr/quay, npm/PyPI, GitHub release assets -> `Big-Transfer`

3. **Maintained providers**
   - Adopt `rule-providers` from MetaCubeX `meta-rules-dat` for broad categories instead of growing only hard-coded suffixes.
   - Prefer `.mrs` for large domain/ipcidr sets where clients support it; keep YAML fallback only if compatibility requires it.
   - Set provider `interval` to a sane value such as 86400 seconds, not frequent churn.
   - Use provider `proxy` for rule downloads if direct GitHub/raw access is unreliable on some clients.

### 4. DNS/client defaults

Add/keep:
- `mode: rule`
- `unified-delay: true`
- `tcp-concurrent: true` if client core supports it
- `profile.store-selected: true`
- `profile.store-fake-ip: true`
- `dns.enhanced-mode: fake-ip`
- `fake-ip-filter` for LAN, NTP, connectivity checks, and services that dislike fake IP

Avoid:
- making all fallback nodes part of the default `url-test`; that can select a technically fast but semantically wrong exit.
- sending all AI traffic through generic HK/Oracle if account stability matters.
- letting `MATCH,Proxy` hide missing direct/private rules.

## Concrete next steps

1. Promote the richer private Mihomo draft into the managed subscription generator, but remove/avoid secret leakage in tracked docs.
2. Add rule-providers for private/CN/direct and common category rules; keep local manual overrides for personal preferences.
3. Narrow `Home-Egress` to account-sensitive AI/login sites.
4. Split `Big-Transfer` more aggressively: HF/model CDNs, Docker/ghcr/quay, npm/PyPI, GitHub release assets.
5. Add a small health script/report that tests explicit nodes and records latency/egress IP without printing credentials.
6. After one week of health data, decide whether `ali-cloud` default should stay `oracle-egress` or switch to a HK-optimized default.

## Best immediate recommendation
Do **not** buy another optimization line yet. The current infra already has enough exits. The better win is to make selection automatic, category-aware, and measurable:

- use `ali-cloud` as the central selector for domestic servers;
- use Mihomo rule-providers + clean groups for user devices;
- keep HK optimized nodes as preferred fast path only after health data proves they are actually stable;
- keep Oracle/home exits as specific-purpose fallbacks, not mixed into every auto group.
