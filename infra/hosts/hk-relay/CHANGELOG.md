# hk-relay / CHANGELOG

## 2026-07-07 — NexusVault monitor website route disabled
- Disabled the old NexusVault monitor website entry during the website revision / temporary retirement window:
  - removed `drop.hk.zhangxuemin.work/nvmon/*` from the `drop.hk.zhangxuemin.work` Caddy site
  - removed the legacy public `:58080` Caddy monitor edge on `hk-relay`
- Preserved the main `drop.hk.zhangxuemin.work` dufs upload/download service.
- Remote Caddy backup: `/etc/caddy/Caddyfile.bak-disable-nvmon-20260707002136`.
- Verification:
  - `caddy validate --config /etc/caddy/Caddyfile` passed
  - `systemctl reload caddy` succeeded and `caddy` stayed active
  - `https://drop.hk.zhangxuemin.work/` and `/nvmon/` now return the dufs auth challenge instead of the old monitor panel
  - `154.86.30.10:58080` no longer accepts connections

## 2026-07-06 — GPT Session Converter CN/HK edge added
- Added live Cloudflare DNS-only A records:
  - `gpt-session.zhangxuemin.work -> 158.178.236.241` (`oracle-proxy` source/global entry)
  - `gpt-session-cn.zhangxuemin.work -> 154.86.30.10` (`hk-relay` CN/HK edge)
- Added Caddy reverse-proxy site on `hk-relay`:
  - `gpt-session-cn.zhangxuemin.work -> https://gpt-session.zhangxuemin.work` (`oracle-proxy` static origin)
- Verification: both `https://gpt-session.zhangxuemin.work/` and `https://gpt-session-cn.zhangxuemin.work/` returned HTTP 200 and served the expected static HTML.
- Direct/global source remains available for overseas/global fallback; HK is only the optimized edge and does not run the app logic.

## 2026-06-29 — home-exit chaining normalized for Clash subscriptions
- Rechecked the private Clash/Mihomo subscription files after Anthropic API connection resets/timeouts through the `AI账号` path.
- Confirmed the clean consumer track's `家庭出口 01` HTTP node already uses `dialer-proxy: 香港 02`.
- Normalized the full/operator Clash.Meta track so all HTTP home-exit entries for the same home proxy are chained through its HK transit selector; no published home-exit entry should depend on direct client reachability to the home proxy.
- Created timestamped `.bak` copies beside the changed remote YAML files before replacement.
- Validation: all published YAML files parsed successfully with PyYAML; legacy public `/clash-meta.yaml` remains HTTP 404 as intended; `caddy`, `dufs-drop`, and `sing-box` remained active.

## 2026-06-23 — FileCodeBox CN/HK edge added
- Added live Cloudflare DNS-only A record: `drop-cn.zhangxuemin.work` -> `154.86.30.10` (`hk-relay`).
- Added Caddy reverse-proxy site on `hk-relay`: `drop-cn.zhangxuemin.work` -> `http://140.83.52.216:18085` (`oracle-mail` FileCodeBox origin).
- Added Caddy Basic Auth on the HK edge; the plaintext password is intentionally not stored in `infra/`.
- Verification: HTTPS returned HTTP 200 and HK-to-origin returned HTTP 200.
- Source port `oracle-mail:18085` is firewall-restricted to `154.86.30.10` plus localhost.

## 2026-06-16 — WA app CN/HK edge added
- Added live Cloudflare DNS-only A records:
  - `wa.zhangxuemin.work` -> `140.83.52.216` (`oracle-mail` source/global entry)
  - `wa-cn.zhangxuemin.work` -> `154.86.30.10` (`hk-relay` CN/HK edge)
- Added Caddy reverse-proxy site on `hk-relay`:
  - `wa-cn.zhangxuemin.work` -> `https://wa.zhangxuemin.work` (`oracle-mail` WA app origin)
- Verification: both `https://wa.zhangxuemin.work/` and `https://wa-cn.zhangxuemin.work/` returned HTTP 303 to `/login?next=%2F`, matching the password-protected dashboard behavior.
- Direct/global source remains available for overseas/global fallback; the `*-cn` route is the domestic/HK optimized entrypoint.

## 2026-06-09 — New API CN/HK edge added
- Added live Cloudflare DNS-only A record: `ai-cn.zhangxuemin.work` -> `154.86.30.10` (`hk-relay`).
- Added Caddy reverse-proxy site on `hk-relay`: `ai-cn.zhangxuemin.work` -> `https://ai.zhangxuemin.work` (`oracle-newapi-primary` New API origin).
- Verification: `https://ai-cn.zhangxuemin.work/` returned HTTP 200 with valid TLS; `https://ai.zhangxuemin.work/` also returned HTTP 200.

# hk-relay / CHANGELOG


## 2026-06-01 — oracle-reverse-dev CTF GPT Plus CN/HK edge added
- Added live Cloudflare DNS-only A record: `ctf-gpt-cn.zhangxuemin.work` -> `154.86.30.10` (`hk-relay`).
- Added Caddy reverse-proxy site on `hk-relay`:
  - `ctf-gpt-cn.zhangxuemin.work` -> `http://140.245.61.236:8000` (`oracle-reverse-dev` CTF GPT Plus origin)
- Verification:
  - origin `http://140.245.61.236:8000/ctf-gpt-plus` returned HTTP 200 for GET
  - HK-to-origin check returned expected HTTP 405 for HEAD / 200 for GET semantics
  - `https://ctf-gpt-cn.zhangxuemin.work/ctf-gpt-plus` returned HTTP 200 and served the app HTML
- Direct/global origin remains available; this is a domestic/HK-optimized TLS edge entrypoint.


## 2026-06-01 — oracle-reverse-dev CN/HK SSH edge added
- Added live Cloudflare DNS-only A record: `reverse-cn.zhangxuemin.work` -> `154.86.30.10` (`hk-relay`).
- Installed `socat` on `hk-relay` and enabled systemd service `oracle-reverse-dev-ssh-edge.service`:
  - public listener: `0.0.0.0:22061`
  - target: `140.245.61.236:22` (`oracle-reverse-dev` SSH)
- Added `ufw` allow rule for `22061/tcp` with comment `oracle-reverse-dev SSH edge`.
- Verification:
  - DNS resolves: `reverse-cn.zhangxuemin.work` -> `154.86.30.10`
  - SSH succeeds with `ssh -p 22061 ubuntu@reverse-cn.zhangxuemin.work` using the oracle-reverse-dev key
  - local SSH config alias `oracle-reverse-dev-cn` / `reverse-cn` succeeds.
- Direct/global SSH to `oracle-reverse-dev` remains available; this edge is for domestic/HK-optimized convenience, matching the `*-cn` entrypoint pattern.


## 2026-05-30 — CPA Manager Plus CN/HK edge added
- Added live Cloudflare DNS-only A records:
  - `cpam.zhangxuemin.work` -> `158.178.236.241` (`oracle-proxy`)
  - `cpam-cn.zhangxuemin.work` -> `154.86.30.10` (`hk-relay`)
- Added Caddy reverse-proxy site on `hk-relay`:
  - `cpam-cn.zhangxuemin.work` -> `https://cpam.zhangxuemin.work`
- Preserved the same split used by `cliproxy-cn`: direct/source endpoint remains on Oracle; `*-cn` is the domestic/HK optimized path.
- Verification:
  - `https://cpam.zhangxuemin.work/management.html` returned HTTP 200 from `158.178.236.241`
  - `https://cpam-cn.zhangxuemin.work/management.html` returned HTTP 200 from `154.86.30.10`
  - existing `https://cliproxy-cn.zhangxuemin.work/v1/models` still returned HTTP 401 through HK edge, matching expected API-auth behavior

## 2026-04-29 — baseline hardening before CN/Global edge expansion
- Added persistent 2G `/swapfile` on the 1G RAM relay host and verified it is active.
- Added journald cap at `/etc/systemd/journald.conf.d/90-openclaw-hardening.conf`:
  - `SystemMaxUse=128M`
  - `RuntimeMaxUse=64M`
  - `MaxRetentionSec=14day`
  - `Compress=yes`
- Installed and enabled `vnstat` for traffic accounting, important because this host has a user-declared bidirectional 800G/month traffic cap.
- Installed and enabled `fail2ban`; enabled the `sshd` jail with `maxretry=5`, `findtime=10m`, `bantime=1h`.
- Hardened SSH authentication while preserving key-based root access:
  - `PermitRootLogin prohibit-password` (effective `without-password`)
  - `PasswordAuthentication no`
  - `KbdInteractiveAuthentication no`
  - `ChallengeResponseAuthentication no`
  - `PubkeyAuthentication yes`
  - `MaxAuthTries 4`
- Verified post-change access and services:
  - SSH key login still works
  - `ssh`, `fail2ban`, `vnstat`, `caddy`, and `sing-box` are active
  - public web surfaces still respond as expected (`hk`/`drop` 401, `clash` root 404)
- Firewall exposure was not narrowed in this pass. Keep existing relay/file-transfer/proxy ports until the CN/Global endpoint topology is finalized.
- Remote backup directory for touched configs: `/root/hardening-backups/20260429-014050`.

## 2026-05-30 — clean Clash consumer track added
- Added a new cleaner consumer-facing Clash/Mihomo track on `clash.hk.zhangxuemin.work` as a separate randomized private path.
- The new track keeps the same routing policy family but reduces the visible node/group surface to a smaller human-friendly set for day-to-day use.
- Corrected the clean track so the visible home-exit node still preserves `dialer-proxy` chaining through a HK node; do not simplify home-exit nodes to direct-only form for user clients.
- Renamed the `oracle-gateway` Hysteria node in the clean track to the human-facing `新加坡 01` because `backup.zhangxuemin.work` / `129.150.61.78` geolocates to Singapore / Oracle.
- Legacy full/operator paths remain available and unchanged.

## 2026-04-29 — first CN/HK edge entrypoints
- Added live Cloudflare DNS-only A records:
  - `cliproxy-cn.zhangxuemin.work` -> `154.86.30.10`
  - `claw-cn.zhangxuemin.work` -> `154.86.30.10`
- Added Caddy reverse-proxy sites on `hk-relay`:
  - `cliproxy-cn.zhangxuemin.work` -> `proxy.zhangxuemin.work:8317`
  - `claw-cn.zhangxuemin.work` -> `https://dev.zhangxuemin.work`
- Preserved the architecture split: `*-cn` names are domestic/HK edge entrypoints; existing Oracle/source names remain the global and machine-to-machine endpoints.
- Follow-up policy clarification at 2026-04-29 09:59 Asia/Shanghai: do **not** add firewall restrictions that make HK the only route to source services. Keeping Oracle/source direct entrypoints public is intentional for HK single-point-of-failure emergency fallback and overseas access.
- Added local SSH `ProxyJump hk-relay` aliases for Oracle hosts (`oracle-*-via-hk`) so domestic SSH can use HK without forcing Oracle-to-Oracle traffic through HK.
- Verification:
  - `https://cliproxy-cn.zhangxuemin.work/` returned HTTP 200 through HK edge
  - `https://cliproxy-cn.zhangxuemin.work/v1/models` returned HTTP 401 through HK edge, matching API-auth behavior
  - `https://claw-cn.zhangxuemin.work/` returned HTTP 401 through HK edge, preserving OpenClaw origin auth behavior
  - SSH via HK aliases succeeded for `oracle-proxy`, `oracle-openclaw`, `oracle-gateway`, `oracle-mail`, `oracle-registry`, and `oracle-reverse-dev`
- Remote Caddy backup directory: `/root/hardening-backups/20260429-014745-edge-caddy`.

## 2026-06-06 — Kiro docs CN/HK edge added
- Added live Cloudflare DNS-only A record: `docs-cn.zhangxuemin.work` -> `154.86.30.10` (`hk-relay`).
- Added Caddy reverse-proxy site on `hk-relay`:
  - `docs-cn.zhangxuemin.work` -> `https://docs.zhangxuemin.work` (`oracle-proxy` Kiro docs static origin)
- Verification:
  - `https://docs-cn.zhangxuemin.work/` returned HTTP 200 from HK edge
  - existing `https://kiro-cn.zhangxuemin.work/admin` remained HTTP 200
- Direct/global docs source remains available at `https://docs.zhangxuemin.work/` for overseas/global fallback.

## 2026-06-06 — Kiro docs CN/HK anti-abuse protection added
- Added Caddy JSON access log for `docs-cn.zhangxuemin.work`: `/var/log/caddy/docs-cn-access.log`.
- Added docs-specific fail2ban filters/jails on `hk-relay`:
  - `openclaw-docs-cn-general`: 180 requests / 60s -> 30m ban
  - `openclaw-docs-cn-assets`: 90 static/image requests / 60s -> 1h ban
- This protects the HK 800G/month transfer budget from obvious high-frequency page/image scraping without replacing the production Caddy binary.
- Verification: synthetic 95-hit static asset log test banned/unbanned the test IP successfully; `docs-cn` and `kiro-cn` remained HTTP 200.

## 2026-06-06 — Card Shop CN/HK edge added
- Added live Cloudflare DNS-only A record: `card-cn.zhangxuemin.work` -> `154.86.30.10` (`hk-relay`).
- Added Caddy reverse-proxy site on `hk-relay`:
  - `card-cn.zhangxuemin.work` -> `https://card.zhangxuemin.work` (`oracle-proxy` Card Shop origin)
- Added Caddy JSON log `/var/log/caddy/card-cn-access.log` and fail2ban jails:
  - `openclaw-card-cn-general`: 180 requests / 60s -> 30m ban
  - `openclaw-card-cn-api`: 40 redeem/query/admin-login requests / 60s -> 1h ban
- Verification: `https://card-cn.zhangxuemin.work/` returned HTTP 200; redeem/query smoke test through CN edge succeeded; fail2ban synthetic trigger test succeeded.
## 2026-06-07 — GPT Card Shop CN/HK edge prepared
- Added Caddy reverse-proxy site on `hk-relay`:
  - `gpt-card-cn.zhangxuemin.work` -> `https://gpt-card.zhangxuemin.work` (`oracle-proxy` GPT Card Shop origin)
- Added Caddy JSON log `/var/log/caddy/gpt-card-cn-access.log` and fail2ban jails:
  - `openclaw-gpt-card-cn-general`: 180 requests / 60s -> 30m ban
  - `openclaw-gpt-card-cn-api`: 40 API/admin-login requests / 60s -> 1h ban
- Added live Cloudflare DNS-only A records for `gpt-card.zhangxuemin.work` and `gpt-card-cn.zhangxuemin.work`; source and CN HTTPS health checks returned HTTP 200 after certificate issuance.

