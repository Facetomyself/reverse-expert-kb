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

## Next operational step
- inspect 1Panel status/routes/config further
- inspect EasyImages compose and health model
- inspect camoufox-remote deployment wrapper and intended consumers
