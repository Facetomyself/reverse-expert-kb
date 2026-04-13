# Domestic Clash Unification Plan

Updated: 2026-04-13

## Goal
Unify outbound access around Clash/Mihomo-style explicit proxy switching, while keeping FRP only for the home-service publish use case and removing the old overlay-network layer from the fleet.

## User intent
- The old overlay-network layer must be completely removed from domestic and overseas machines with no residual operational role.
- `infra/` should also stop treating that removed overlay layer as a live or historical documentation axis; remove the related references directly instead of archiving them.
- Keep `home-macmini` and `home-nas` published through FRP with port forwards for selected home services.
- All other servers should use Clash/Mihomo-style proxying for outbound Internet traffic and be able to switch nodes.
- `home-macmini` and `home-nas` should also have local Clash/Mihomo available for direct outbound proxy use.
- Existing mixed proxy/routing residue (old transparent tunnels, ad-hoc proxy envs, route hacks) should be retired once the new path is verified.

## Target architecture

### 1. Roles
#### A. Proxy providers (stable upstream nodes)
- `ali-cloud`
  - role: default domestic-side everyday outbound exit
  - keep current authenticated explicit proxy ingress:
    - SOCKS5 `106.15.239.221:2080`
    - HTTP `106.15.239.221:2081`
  - keep as the safest fallback/default route for domestic servers

- `hk-relay`
  - role: user-selectable Hong Kong relay for explicit proxy use + large-file relay
  - current node set exposed via Clash subscription:
    - `hk-socks`
    - `hk-http`
    - `hk-hy2`
    - `hk-reality`
  - subscription rule: prefer bare IP `154.86.30.10` inside node `server` fields

- `oracle-gateway`
  - role: keep as gateway/tunnel/fallback infra, not the main domestic default for every box
  - can remain as a backup/fallback node in subscriptions

#### B. Domestic proxy consumers
- `self-server` (`:44001` / 181)
- `self-server-44005` (`host185`)
- `home-macmini`
- `home-nas`
- optionally other domestic desktops/servers later

#### C. Home-service publish path
- Keep FRP only for inbound publication of selected home services
- Current intended FRP home-service map on `:44001`:
  - `30014` -> `home-macmini` ComfyUI
  - `30015` -> `home-nas` DSM HTTPS
  - `30016` -> `home-nas` Synology Drive

### 2. Traffic model
#### Outbound Internet traffic
- domestic machines -> local Clash/Mihomo -> selectable upstream node
- default group ordering should bias:
  1. `ali-oracle` style node(s) for stable everyday use
  2. `hk-*` nodes for better overseas quality / optional switching
  3. `oracle-gateway` fallback where retained

#### Inbound published home services
- continue through FRP on `self-server(:44001)`
- do not reintroduce any removed overlay-network-based publish or access path

## Standard per-machine end state

### self-server (:44001)
- Keep:
  - `1Panel`
  - FRPS
  - local DNS helper only if still needed during migration
  - local Clash/Mihomo client for outbound switching
- Remove/retire after cutover verification:
  - old ad-hoc explicit proxy env residue that points directly to `ali-cloud` without a local selector
  - any abandoned transparent TUN experiments
- Desired user experience:
  - machine itself can switch outbound node by changing local Clash group
  - still serves as FRP entry for home services

### self-server-44005
- Keep:
  - `1Panel`
  - NapCat
  - AstrBot
  - local Clash/Mihomo client for outbound switching
- Remove/retire after cutover verification:
  - leftover direct proxy env hacks
  - any old mihomo/tun residue if reintroduced manually outside the new managed setup
- Avoid disturbing current public app port budget on `30001-30010`

### home-macmini
- Keep:
  - FRP client for published services
  - local Clash/Mihomo for outbound foreign traffic
- Remove:
  - the old overlay-network client completely
- Desired UX:
  - normal outbound browsing/downloads/model pulls can use local Clash
  - published service exposure still goes through FRP

### home-nas
- Keep:
  - FRP client for DSM / Drive publication
  - local Clash/Mihomo-capable outbound path for direct foreign traffic
- Remove:
  - the old overlay-network client completely
- Important caution:
  - Synology package/runtime management is non-standard; any Clash deployment must respect DSM/Synology service conventions
  - do not trust DSM package UI state alone as service truth

## Subscription / policy design

### 1. Subscription variants
Maintain one main Mihomo/Clash.Meta subscription as the primary distribution artifact:
- `https://clash.hk.zhangxuemin.work/clash-meta.yaml`

Keep reduced variants only for compatibility/debug:
- `clash-compat.yaml`
- `clash-classic.yaml`

### 2. Group design
Recommended default groups:
- `Proxy` -> main manual select group
- `HK` -> Hong Kong-only group
- `Fallback` -> ali/oracle fallback group
- `Big-Transfer` -> HF/GitHub/large-transfer-biased group

### 3. Routing policy direction
Recommended practical policy:
- CN direct
- common foreign AI/dev sites through `Proxy`
- large model/file sources through `Big-Transfer`
- leave room for machine-specific overrides if one host has unique workload patterns

### 4. Provider selection policy
Default recommendation:
- day-to-day default: `ali-oracle` style node
- better overseas quality / manual switch: `hk-*`
- special fallback: `oracle-gateway-*`

## Migration order

### Phase 1 — lock the node/control plane
1. Freeze the upstream node inventory and keep subscriptions stable
2. Treat `clash.hk.../clash-meta.yaml` as the main managed config
3. Keep HK nodes on bare IPs in published subscriptions

### Phase 2 — domestic server cutover first
1. `self-server(:44001)`
2. `self-server-44005`

Reason:
- these are easier to modify remotely
- they already have explicit-proxy residue we want to replace cleanly
- they are lower-risk than immediately touching home endpoints

### Phase 3 — home endpoints
1. `home-macmini`
2. `home-nas`

Reason:
- both need coexistence of FRP + local outbound Clash
- NAS especially needs a careful host-native deployment shape

### Phase 4 — cleanup
Per machine, only after validation:
- remove old explicit shell proxy environment residue
- remove abandoned transparent/tun experiments
- remove old overlay-network packages/services/config completely
- normalize DNS helper usage if no longer needed
- write final runtime/docs back to `infra/`

## Per-machine acceptance criteria

### Outbound success
- host can fetch foreign HTTPS through its local Clash/Mihomo path
- node switching works between at least:
  - `ali-oracle`
  - one `hk-*` node
- Docker / curl / package/runtime downloads behave predictably through the chosen local path

### Inbound home-service success
- `home-macmini` ComfyUI remains reachable through FRP
- `home-nas` DSM / Drive remain reachable through FRP

### Cleanup success
- old overlay-network packages/services/config are absent from all targeted hosts
- old proxy/routing residue is removed or explicitly documented as intentionally retained

## Immediate next implementation steps
1. Audit current outbound-proxy residue on:
   - `self-server(:44001)`
   - `self-server-44005`
2. Choose deployment shape per domestic Linux host:
   - standalone Mihomo binary + systemd, or
   - sing-box client + generated config
3. Cut over `self-server(:44001)` first and validate:
   - shell traffic
   - Docker traffic
   - node switching
4. Repeat on `self-server-44005`
5. Then design the host-native shape for:
   - `home-macmini`
   - `home-nas`

## 2026-04-13 implementation findings
### Current domestic-server reality
Runtime audit confirmed both `self-server(:44001)` and `self-server-44005` are still in the pre-unification transition state:
- shell sessions inherit proxy env from `/etc/profile.d/ali-proxy.sh`
- Docker inherits proxy env from `/etc/systemd/system/docker.service.d/proxy.conf`
- `dnsmasq` is still running locally on both hosts
- neither host currently has an active local `mihomo`, `clash-meta`, or `sing-box` client binary in place
- however, 2026-04-13 live validation proved these hosts can already inherit centralized upstream switching transparently through `ali-cloud`: with no host-local config changes, observed egress moved from `129.150.61.78` (`oracle-egress`) to `154.86.30.10` (`hk-socks`) and back again after only changing `ali-cloud`'s selector default

### Current ali-cloud gateway reality
Runtime audit on `ali-cloud` confirmed that the existing authenticated proxy entry (`106.15.239.221:2080/:2081`) is implemented as:
- sing-box public inbounds on `2080` / `2081`
- a single sing-box final outbound `oracle-egress`
- local SOCKS5 hop `127.0.0.1:18080`
- Hysteria client dialing `backup.zhangxuemin.work:443`

Practical meaning:
- the current domestic default path is effectively a fixed `ali-cloud ingress -> local Hysteria -> oracle-gateway` chain
- this is stable, but it is not yet the user-requested selectable multi-exit control plane

### Recommended next cutover path
Use `ali-cloud` as the first selector/control-plane insertion point before touching every domestic consumer host:
1. keep `:2080` / `:2081` as the stable authenticated ingress already used by domestic servers
2. expand `sing-box-gateway` from a single fixed outbound into a selector-style config that can target at least:
   - current `oracle-gateway` Hysteria egress
   - one `hk-*` path from `hk-relay`
   - optional direct HK SOCKS/HTTP fallback from `hk-relay`
   - status on 2026-04-13: this selector stage is now deployed on `ali-cloud`, with default still pinned to `oracle-egress`
   - live switch test already passed: `hk-socks` changed observed egress to `154.86.30.10`, and switching back restored observed egress to `129.150.61.78`
3. once `ali-cloud` can switch upstream exits cleanly, decide whether domestic consumers still need full local Mihomo, or whether some Linux servers can remain on the lighter explicit-proxy model with centrally managed upstream selection
   - current evidence strongly favors the lighter centralized model for `self-server(:44001)` and `self-server-44005`, because both already followed selector changes without any per-host software rollout
4. only after that, replace host-local `ali-proxy.sh` / Docker drop-ins on domestic consumers with the finalized managed layout
5. operational switching on `ali-cloud` is now mediated by `/usr/local/bin/ali-cloud-proxy-select`, so future exit tests can change only the selector default instead of hand-editing JSON

## Notes
- Missing local docs were noticed for `home-macmini` in the current `infra/hosts/` tree; add/refresh host docs during the implementation phase.
- Overseas machines are also in scope for old-overlay removal; do not leave cloud hosts in a mixed state where Clash is the main path but the removed overlay client still lingers.
