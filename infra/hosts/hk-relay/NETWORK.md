# hk-relay / NETWORK

## 1. Public Network Identity
- Public IP: `154.86.30.10`
- Canonical domain: `hk.zhangxuemin.work`
- Additional domains:
  - `drop.hk.zhangxuemin.work`
  - `clash.hk.zhangxuemin.work`
  - `cliproxy-cn.zhangxuemin.work`
  - `proxy-bak-cn.zhangxuemin.work`
  - `claw-cn.zhangxuemin.work`
  - `ai-cn.zhangxuemin.work`
  - `cpam-cn.zhangxuemin.work`
  - `reverse-cn.zhangxuemin.work`
  - `ctf-gpt-cn.zhangxuemin.work`
  - `docs-cn.zhangxuemin.work`
  - `card-cn.zhangxuemin.work`
  - `wa-cn.zhangxuemin.work`
  - `zcode-cn.zhangxuemin.work`
  - `drop-cn.zhangxuemin.work`
- Provider: unknown / user-added Hong Kong VPS
- Intended role: 三网优化流量中转

## 2. Current confirmed addressing
Observed on 2026-04-13:
- interface: `enp1s0`
- primary address: `154.86.30.10/24`
- default gateway: `154.86.30.254`
- DNS via cloud-init netplan:
  - `8.8.8.8`
  - `1.1.1.1`

## 3. Current listener surface
First baseline snapshot showed only:
- TCP `22` (`sshd`)
- local-only stub resolver on `127.0.0.53:53`

After relay bootstrap on 2026-04-13, confirmed public listener map:
- TCP `22` -> SSH
- TCP `1080` -> sing-box authenticated mixed inbound (proxy/tools/general-purpose entry)
- TCP `1081` -> sing-box authenticated HTTP proxy inbound
- TCP `8080` -> authenticated Caddy browse/download entry for `hk.zhangxuemin.work`
- TCP `8088` -> local `dufs` upload/download backend (publicly surfaced via `drop.hk.zhangxuemin.work` through Caddy reverse proxy)
- TCP `22061` -> `socat` TCP relay to `oracle-reverse-dev` SSH (`140.245.61.236:22`), published as `reverse-cn.zhangxuemin.work:22061`
- TCP `8443` -> sing-box VLESS + Reality inbound
- UDP `8444` -> sing-box Hysteria2 inbound
- TCP `443` -> Caddy HTTPS front door serving:
  - `hk.zhangxuemin.work` (browse/download with Basic Auth)
  - `drop.hk.zhangxuemin.work` (HTTPS upload/download front door)
  - `clash.hk.zhangxuemin.work` (public Clash config download endpoint)
- TCP `80` -> ACME / HTTP redirect handling for the above hostnames

## 4. Egress validation
Validated on 2026-04-13:
- `https://www.google.com` reachable (`HTTP/2 200`)
- `https://github.com` reachable (`HTTP/2 200`)

Interpretation:
- outbound Internet access is available and appears healthy at baseline
- no additional bootstrap proxy/tunnel layer was required for ordinary foreign HTTPS reachability during first contact

## 5. Budget constraint
This machine has a user-declared **bidirectional monthly traffic cap of 800G**.

Operational implication:
- treat bandwidth usage as part of the network design, not just a billing footnote
- future services on this host should document whether they are expected to consume:
  - low steady-state control traffic
  - bursty download traffic
  - sustained relay/proxy traffic
- avoid undocumented large-image mirroring, package-cache hosting, or other silent high-egress roles here

## 6. Firewall baseline
Confirmed on 2026-04-13 with `ufw` active, and rechecked during the 2026-04-29 baseline hardening pass:
- default incoming: deny
- default outgoing: allow
- allow `22/tcp`
- allow `80/tcp`
- allow `443/tcp`
- allow `1080/tcp`
- allow `1081/tcp`
- allow `8080/tcp`
- allow `8088/tcp`
- allow `8443/tcp`
- allow `8444/udp`
- allow `22061/tcp`

Interpretation:
- current exposure is intentionally wider than a minimal host because the machine is being positioned as a self-use multi-role relay node
- port/service exposure was intentionally not narrowed during the 2026-04-29 baseline hardening pass, and should **not** be narrowed just because HK edge entrypoints now exist; the intended design keeps direct/global source endpoints as emergency fallback and overseas access paths if `hk-relay` is unavailable
- management surface is improved from 2026-04-29 onward: SSH password auth is disabled, root remains key-only, and `fail2ban` protects the `sshd` jail

## 7. Current distribution endpoints
Validated on 2026-04-13, then hardened on 2026-04-21:
- `https://hk.zhangxuemin.work/` -> authenticated browse/download entry
- `https://drop.hk.zhangxuemin.work/` -> HTTPS upload/download entry backed by local `dufs`
- `https://clash.hk.zhangxuemin.work/` -> Clash distribution hostname, with the legacy public `/clash-meta.yaml` family kept disabled and private YAML downloads served only from randomized private path segments
- `https://cliproxy-cn.zhangxuemin.work/` -> CN/HK TLS edge for primary cliproxy, reverse-proxied to `proxy.zhangxuemin.work:8317`
- `https://proxy-bak-cn.zhangxuemin.work/` -> CN/HK TLS edge for CLIProxy backup pool, reverse-proxied to `https://proxy-bak.zhangxuemin.work`
- `https://claw-cn.zhangxuemin.work/` -> CN/HK TLS edge for OpenClaw Control UI, reverse-proxied to `https://dev.zhangxuemin.work` while preserving origin auth behavior
- `https://ai-cn.zhangxuemin.work/` -> CN/HK TLS edge for New API, reverse-proxied to `https://ai.zhangxuemin.work`
- `https://cpam-cn.zhangxuemin.work/` -> CN/HK TLS edge for CPA Manager Plus, reverse-proxied to `https://cpam.zhangxuemin.work`
- `https://kiro-cn.zhangxuemin.work/admin` -> CN/HK TLS edge for Kiro-Go, reverse-proxied to `https://kiro.zhangxuemin.work/admin`
- `https://docs-cn.zhangxuemin.work/` -> CN/HK TLS edge for Kiro docs static site, reverse-proxied to `https://docs.zhangxuemin.work/`
- `https://card-cn.zhangxuemin.work/` -> CN/HK TLS edge for Card Shop, reverse-proxied to `https://card.zhangxuemin.work/`
- `https://wa-cn.zhangxuemin.work/` -> CN/HK TLS edge for WA app, reverse-proxied to `https://wa.zhangxuemin.work/`
- `https://zcode-cn.zhangxuemin.work/` -> CN/HK TLS edge for zcode2api admin/API traffic, reverse-proxied to `https://zcode.zhangxuemin.work` on `oracle-proxy`; HK does not run the business container
- `https://drop-cn.zhangxuemin.work/` -> CN/HK TLS edge for FileCodeBox file/text transfer, reverse-proxied to `oracle-mail:18085`
- `reverse-cn.zhangxuemin.work:22061` -> CN/HK TCP edge for `oracle-reverse-dev` SSH, forwarding to `140.245.61.236:22`; normal use: `ssh -p 22061 ubuntu@reverse-cn.zhangxuemin.work`
- `https://ctf-gpt-cn.zhangxuemin.work/ctf-gpt-plus` -> CN/HK TLS edge for `oracle-reverse-dev` CTF GPT Plus, reverse-proxied to `http://140.245.61.236:8000/ctf-gpt-plus`
- `https://kiro-rs-cn.zhangxuemin.work/` -> exact-root `308` redirect to `/admin` on HK edge; other paths reverse-proxy to `https://kiro-rs.zhangxuemin.work` with origin Host/TLS SNI preserved

Subscription hardening on 2026-04-21:
- legacy public paths `/clash-meta.yaml`, `/clash-compat.yaml`, and `/clash-classic.yaml` were disabled and now return 404
- active subscription files are served only from randomized private paths on the same host
- a separate cleaner client-facing track was added later for day-to-day use; it keeps the same privacy model but exposes fewer nodes/groups than the full operator subscription
- the exact secret path is intentionally not stored in repo-tracked docs; treat it as a credential
- the private Clash.Meta subscription was also expanded to support a chained home-exit pattern, where a `Home-Egress` group can land on a user-controlled HTTP proxy while using `HK-Transit` as the `dialer-proxy` upstream
- the newer clean track intentionally hides most internal protocol names and presents a smaller set of human-friendly groups for day-to-day client use
- by 2026-04-21 this private Clash.Meta track was further upgraded from pure manual selectors to a mixed **manual + auto** design:
  - each main group now keeps a manual shell (`Proxy`, `HK`, `HK-Transit`, `Home-Egress`, `Fallback`, `Big-Transfer`, `Oracle-Proxy-Extra`)
  - but the first/default option inside those groups is now an automatically chosen `*-Auto` provider using `url-test` or `fallback`
  - practical result: fresh clients no longer have to hand-pick a node first just to get moving, while manual override still remains available
- the same private Clash.Meta track now also carries a small verified `oracle-proxy` fallback pack rather than only one extra datacenter node; current private-track additions include `hysteria2`, `shadowsocks`, `trojan`, `tuic`, and Xray `VLESS Reality Vision`

The published Clash config intentionally aggregates both newly deployed HK relay entries and pre-existing usable proxy entries, currently including:
- `hk-hy2`
- `hk-reality`
- `hk-socks`
- `hk-http`
- `oracle-gateway-hy2-backup`
- `ali-socks-oracle-egress`
- `ali-http-oracle-egress`
- additional private-track-only entries such as `Home-Egress` / `HK-Transit` chaining, automatic `*-Auto` selector groups, and a verified `Oracle-Proxy-Extra` fallback group

Runtime note confirmed on 2026-04-13:
- the HK relay services themselves were healthy (HTTP/SOCKS direct tests via `1080/1081` succeeded), but Clash-side HK node runtime only stabilized after the subscription was changed to use the bare server IP `154.86.30.10` for all HK node entries instead of `hk.zhangxuemin.work`
- keep `hk.zhangxuemin.work`, `drop.hk.zhangxuemin.work`, and `clash.hk.zhangxuemin.work` for web/file/distribution use
- for published proxy node definitions on this host, prefer IP literals over the hostname unless/until a specific client population proves domain-form entries are equally reliable
- for subscription sharing, do not publish repo-visible docs or public messages containing the randomized private path; rotate the path if it is ever widely exposed
- current private-track routing is also materially richer than the old minimal domain list: common AI/account-sensitive domains prefer `Home-Egress`, common dev/proxy ecosystems such as GitHub / Google / jsDelivr / Cloudflare prefer `Proxy`, model/package/container/download ecosystems such as Hugging Face / Docker / GHCR / Quay / npm / PyPI prefer `Big-Transfer`, local/private networks are forced `DIRECT`, and `GEOSITE,CN` + `GEOIP,CN` still keep mainland traffic direct
- on 2026-05-25 the private track was refreshed with MetaCubeX `meta-rules-dat` MRS `rule-providers`, persistent client profile defaults, `tcp-concurrent`, and a conservative fake-IP filter; see `private-mihomo-subscription.md` for the operator-level policy summary

## 8. CN / Global endpoint policy
- The `*-cn.zhangxuemin.work` names are the domestic-optimized HK edge path.
- The existing Oracle/source names remain the global/foreign and machine-to-machine path, and should stay publicly reachable as the planned fallback if HK has an outage:
  - cliproxy primary global/source: `proxy.zhangxuemin.work:8317`
  - cliproxy backup pool global/source: `https://proxy-bak.zhangxuemin.work`
  - OpenClaw global/source: `dev.zhangxuemin.work`
  - New API global/source: `ai.zhangxuemin.work`
  - CPA Manager Plus global/source: `cpam.zhangxuemin.work`
  - Kiro-Go global/source: `kiro.zhangxuemin.work`
  - Kiro docs global/source: `docs.zhangxuemin.work`
  - Card Shop global/source: `card.zhangxuemin.work`
  - WA app global/source: `wa.zhangxuemin.work`
  - zcode2api global/source: `zcode.zhangxuemin.work`
  - oracle-reverse-dev global/source SSH: `140.245.61.236:22` / `oracle-reverse-dev`
  - oracle-reverse-dev CTF GPT Plus origin: `http://140.245.61.236:8000/ctf-gpt-plus`
- Do **not** apply source-firewall restrictions that make HK the only public route to these services. Keeping direct/global entrypoints is intentional for HK single-point-of-failure avoidance and overseas access.
- Oracle-to-Oracle traffic should not be routed through `hk-relay`; use direct Oracle/source endpoints, Oracle private networking if available, or a dedicated non-HK overlay.
- SSH via HK is normally exposed as client-side `ProxyJump` aliases. Exception added 2026-06-01: `reverse-cn.zhangxuemin.work:22061` is a dedicated TCP SSH edge for easier domestic access to `oracle-reverse-dev`; direct SSH aliases should remain available as emergency/global paths unless a separate hardening decision supersedes this.

## 9. To Be Confirmed
Still worth documenting once the host role is finalized:
- whether the initial Hysteria2 self-signed certificate should later be replaced with a domain-valid certificate for better client UX
- whether traffic monitoring / accounting / caps should be enforced on-host
- whether the provider offers a panel/API for monthly transfer inspection
- whether a dedicated file-transfer ingress (Caddy/Nginx/SFTP landing area) should become part of the standard design


## hk-relay -> self-server bulk pull test (2026-05-25)

A no-proxy pull test from `self-server` to existing `hk-relay` dufs (`154.86.30.10:8088`) was completed and then fully cleaned up.

Result:

- 512 MiB transfer completed with SHA256 verified.
- Initial 300s cap downloaded `395411152` bytes at about `1.32 MB/s`; resume via HTTP Range / `curl -C -` completed the remaining `141459760` bytes at about `1.14 MB/s`.
- 2 GiB sample capped at 180s downloaded `181026064` bytes at about `1.01 MB/s`, projecting roughly 35–36 minutes for a full 2 GiB file.
- Temporary files were removed from both `hk-relay` and `self-server`.

Interpretation:

- HK dufs is functional and resumable from `self-server`.
- It is not the preferred Oracle -> domestic large-file bridge because it is much slower than the previously measured direct no-proxy pull from `oracle-proxy` (`~6.9–9.6 MiB/s`).

Detailed report: `self-server-pull-test-2026-05-25.md`.

### Kiro docs CN/HK anti-abuse / rate-limit protection
- `docs-cn.zhangxuemin.work` has Caddy JSON access logging to `/var/log/caddy/docs-cn-access.log`.
- fail2ban jails protect the HK edge from high-frequency page/static-asset scraping:
  - `openclaw-docs-cn-general`: 180 requests / 60s -> 30m ban
  - `openclaw-docs-cn-assets`: 90 static/image requests / 60s -> 1h ban
- This is intentionally scoped to the public docs site and does not change Kiro-Go API/admin rate behavior.

### Card shop CN/HK anti-abuse / rate-limit protection
- `card-cn.zhangxuemin.work` has Caddy JSON access logging to `/var/log/caddy/card-cn-access.log`.
- fail2ban jails protect the HK edge from high-frequency redeem/query/admin-login abuse:
  - `openclaw-card-cn-general`: 180 requests / 60s -> 30m ban
  - `openclaw-card-cn-api`: 40 `/api/redeem`, `/api/query`, or `/admin/login` requests / 60s -> 1h ban
- This is scoped to Card Shop and does not change Kiro-Go API/admin rate behavior.

### GPT Card Shop CN/HK edge
- `gpt-card-cn.zhangxuemin.work` Caddy route is prepared on `hk-relay` and points to `https://gpt-card.zhangxuemin.work`.
- JSON access log: `/var/log/caddy/gpt-card-cn-access.log`.
- fail2ban jails prepared:
  - `openclaw-gpt-card-cn-general`: 180 requests / 60s -> 30m ban
  - `openclaw-gpt-card-cn-api`: 40 API/admin-login requests / 60s -> 1h ban
- Live verification completed on 2026-06-07: `https://gpt-card-cn.zhangxuemin.work/healthz` returned HTTP 200.

