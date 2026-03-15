# ali-cloud / NETWORK

## 1. Public Network Identity
- Public IP: `106.15.239.221`
- Provider: Alibaba Cloud

## 2. Current Listener Map
Observed listeners:
- `22/tcp` -> SSH
- `80/tcp` -> `1panel`
- `10086/tcp` -> Docker-published `easyimage`
- `39222/tcp` -> Docker-published `camoufox-remote`

## 3. Interpretation
This host exposes a small application surface:
- one panel/control-plane HTTP endpoint on `80`
- one app endpoint on `10086`
- one remote browser/automation endpoint on `39222`

## 4. To Be Confirmed
- whether `1panel` also serves an admin UI on a non-obvious path or additional port
- any bound domain names for `10086` / `39222`
- whether TLS termination exists elsewhere (CDN / reverse proxy / 1Panel site config)
