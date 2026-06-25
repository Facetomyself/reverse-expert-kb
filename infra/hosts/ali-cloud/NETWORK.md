# ali-cloud / NETWORK

## 1. Public Network Identity
- Public IP: `106.15.239.221`
- Provider: Alibaba Cloud
- Historical mistaken zcode2api origin endpoint: `http://106.15.239.221:18084` (stopped after migration on 2026-06-22)
- Live zcode2api origin is now on `oracle-proxy`; `ali-cloud` should not be used for this project's domestic/global entry topology.

## 2. Current Listener Map
Observed listeners:
- `22/tcp` -> SSH
- `80/tcp` -> `1panel`
- `10086/tcp` -> Docker-published `easyimage`
- `39222/tcp` -> Docker-published `camoufox-remote`
- `18084/tcp` -> Docker-published `zcode2api` Anthropic-compatible gateway/admin UI

## 3. Interpretation
This host exposes a small application surface:
- one panel/control-plane HTTP endpoint on `80`
- one app endpoint on `10086`
- one remote browser/automation endpoint on `39222`
- one zcode2api gateway/admin endpoint on `18084`

For `39222`, the currently documented contract is a direct public websocket endpoint:
- `ws://106.15.239.221:39222/camoufox`
- no confirmed TLS termination or auth gateway currently documented in front of that port

## 4. To Be Confirmed
- whether `1panel` also serves an admin UI on a non-obvious path or additional port
- any bound domain names for `10086` / `39222`
- whether TLS termination exists elsewhere for `10086` / `39222` (CDN / reverse proxy / 1Panel site config)
