# ali-cloud / PROJECTS

## 1. 1Panel
Confirmed:
- systemd unit: `1panel.service`
- binary: `/usr/local/bin/1panel`
- state/data path: `/opt/1panel`
- DB: `/opt/1panel/db/1Panel.db`
- logs: `/opt/1panel/log/`
- host port `80` currently owned by `1panel`

Operational implication:
- this host is not “just Docker”; 1Panel is the machine-level app/control plane and may manage app deployment metadata and lifecycle.

## 2. EasyImages
Confirmed:
- container name: `easyimage`
- image: `ddsderek/easyimage:v2.8.6`
- published port: `10086 -> 80`
- compose project: `easyimage2`
- compose path: `/opt/1panel/apps/easyimage2/easyimage2/docker-compose.yml`
- data mounts:
  - `/opt/1panel/apps/easyimage2/easyimage2/data/i` -> `/app/web/i`
  - `/opt/1panel/apps/easyimage2/easyimage2/data/config` -> `/app/web/config`
- lifecycle labels suggest it was created by 1Panel Apps

## 3. camoufox-remote
Confirmed:
- container name: `camoufox-remote`
- image: `apify/actor-python-playwright-camoufox:latest`
- published port: `39222 -> 39222`
- env indicates websocket/browser service on `0.0.0.0:39222`
- deployment clue path: `/opt/camoufox-remote/run_camoufox_server_compat.py`

Operational implication:
- this service looks separate from 1Panel-managed apps and may be a manually maintained automation endpoint.

## 4. Hysteria egress (persistent local outbound path)
Confirmed on 2026-04-04:
- deployment root: `/opt/hysteria-egress`
- runtime shape: Docker Compose via legacy `/usr/bin/docker-compose`
- compose file: `/opt/hysteria-egress/docker-compose.yml`
- config file: `/opt/hysteria-egress/client.yaml`
- container name: `hysteria-client`
- image pinned by digest: `tobyxdd/hysteria@sha256:f66cda11f8e72e70bbf6f623d51ac6a09be878933850e0425c0253d7d756015e`
- network mode: `host`
- local SOCKS5 listener: `127.0.0.1:18080`
- systemd wrapper: `hysteria-egress.service`

Validated behavior:
- egress IP through the SOCKS5 listener was `129.150.61.78`
- `https://registry-1.docker.io/v2/` returned expected `401` via SOCKS5
- this shape is intentionally local-only for now: it improves this host's outbound access but does not yet expose a general-purpose public gateway service

## 5. Docker daemon outbound proxying
Confirmed on 2026-04-04:
- drop-in path: `/etc/systemd/system/docker.service.d/proxy.conf`
- configured env:
  - `HTTP_PROXY=socks5://127.0.0.1:18080`
  - `HTTPS_PROXY=socks5://127.0.0.1:18080`
  - `NO_PROXY=localhost,127.0.0.1,::1`

Operational implication:
- Docker pulls on this host now rely on the local Hysteria SOCKS5 path to reach unstable foreign registry endpoints
- this was validated with successful pulls for both `hello-world` and `tobyxdd/hysteria:latest`

## Next operational step
- inspect 1Panel status/routes/config further
- inspect EasyImages compose and health model
- inspect camoufox-remote deployment wrapper and intended consumers
- later decide what externalized gateway shape this host should offer (if any) instead of prematurely exposing the current local-only egress helper
