# prompt-optimizer-studio on `self-server-44005`

## Purpose
Self-hosted deployment of Prompt Optimizer Studio for domestic access on the cleaner `host185` VM behind shared public IP `211.144.221.229`.

## Placement
- Host: `self-server-44005` / hostname `host185`
- Public entrypoint: `http://211.144.221.229:30001`
- Port mapping: `30001 -> 3000`
- Reason for placement:
  - domestic machine for lower-latency local use
  - cleaner rebuild target than `:44001`
  - fits the user-confirmed `30001-30010` public TCP budget for `:44005`

## Runtime shape
- Deployment root: `/opt/prompt-optimizer-studio`
- Data path on host: `/opt/prompt-optimizer-studio/data`
- Container data path: `/app/data`
- Compose runtime: `docker-compose`
- Main container: `prompt-optimizer-studio-app-1`
- Health endpoint: `GET /api/health`

## Build/update workflow
Because direct GitHub/GHCR bootstrap from this host was flaky during the initial deployment, prefer this update pattern:

1. Fetch or refresh source on a better-connected machine
2. Copy source to `host185` under `/opt/prompt-optimizer-studio`
3. Rebuild in place with:
   - `docker-compose up -d --build`
4. Verify with:
   - `docker ps`
   - `curl http://127.0.0.1:30001/api/health`

## Operational notes
- Keep public exposure trimmed to `30001` only.
- Do not casually reuse `30002-30010` without recording the change in `infra/`.
- Persistent app data currently lives in local SQLite under `/opt/prompt-optimizer-studio/data`.
- If later adding a domain/reverse proxy, document the new route in `NETWORK.md` and update this file with the chosen front-door path.

## Read-only maintenance checklist
Useful checks for recurring health reviews:
- container present and `healthy`
- only `30001` exposed publicly for this service
- `/api/health` returns `200 OK`
- root disk and memory remain comfortable
- no unexpected sidecar containers appeared in `/opt/prompt-optimizer-studio`

## Local health-check helper
- script: `infra/bin/check-prompt-optimizer-self-server.sh`
- output directory: `infra/reports/prompt-optimizer-studio/`
- current schedule: daily at `03:25` Asia/Shanghai via OpenClaw cron job `infra:self-server-44005:prompt-optimizer-health`
- normal policy: read-only check + report generation; only write back into `infra/` when there is a meaningful operational delta
