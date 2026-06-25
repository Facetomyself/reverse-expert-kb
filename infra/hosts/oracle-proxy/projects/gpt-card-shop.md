# GPT Card Shop

## Purpose

ChatGPT account/card delivery service, separate from the Kiro Card Shop. It keeps the same operational pattern as the existing Card Shop, but its business logic is format-aware:

- admin uploads ChatGPT account/session JSON inventory
- system detects/normalizes session-like, CPA-like, and sub2api-like payloads
- each generated card can carry one or more account items
- public redemption supports multiple card codes in one request
- redeemed users can download:
  - CPA-compatible zip package
  - sub2api-compatible merged JSON
  - original JSON zip backup

## Runtime

- Host: `oracle-proxy`
- Directory: `/root/containers/gpt-card-shop`
- Compose service/container: `gpt-card-shop`
- Loopback origin: `127.0.0.1:18768 -> 3000`
- DB: `/root/containers/gpt-card-shop/data/gpt-cardshop.db`
- Env/secrets: `/root/containers/gpt-card-shop/.env` (`0600`; do not copy secret values into repo/docs)
- Source Caddy route: `/root/containers/caddy-cpam/Caddyfile`
- Source access log: `/var/log/caddy/gpt-card-access.log`

## Entry points

Configured:

- Global/source: `https://gpt-card.zhangxuemin.work/` -> `127.0.0.1:18768`
- CN/HK edge: `https://gpt-card-cn.zhangxuemin.work/` -> HK relay -> `https://gpt-card.zhangxuemin.work`

Cloudflare DNS records added on 2026-06-07:

- `gpt-card.zhangxuemin.work` A -> `158.178.236.241`
- `gpt-card-cn.zhangxuemin.work` A -> `154.86.30.10`

## Admin

- Admin URL after DNS: `https://gpt-card.zhangxuemin.work/admin/login`
- Username is stored in `.env` as `ADMIN_USER`.
- Password is stored in `.env` as `ADMIN_PASSWORD` and should not be committed.

## Data model

Core SQLite tables:

- `cards`: card codes and redemption status
- `account_items`: account inventory linked to cards; stores raw JSON and normalized conversion output
- `redeem_batches`: multi-card redemption batches and short-lived download tokens
- `redeem_batch_cards`: cards included in a redemption batch
- `download_events`: CPA/sub2api/original download audit events
- `events`: admin/public operational events
- `settings`: reserved settings table

## Format behavior

- Input supports JSON files containing ChatGPT session-like objects, CPA-like objects, sub2api documents, and arrays/nested collections where account-like objects can be discovered.
- Download behavior:
  - `sub2api`: one merged JSON document shaped as `{ exported_at, proxies, accounts }`
  - `cpa`: zip containing one CPA JSON per account under `cpa-auth/`, plus `manifest.json` and `README.txt`
  - `original`: zip containing uploaded original JSON files plus `manifest.json`
- Duplicate/inventory fingerprinting is based on canonicalized parsed account identity/token material, but delivered original backup keeps the raw uploaded JSON.

## Verification on 2026-06-07

- Cloudflare DNS added for `gpt-card` and `gpt-card-cn`.
- Source HTTPS verified: `https://gpt-card.zhangxuemin.work/healthz` -> HTTP 200.
- CN/HK HTTPS verified: `https://gpt-card-cn.zhangxuemin.work/healthz` -> HTTP 200.

- `node --check app/src/server.js` passed.
- Container built and started successfully.
- Direct health check passed: `http://127.0.0.1:18768/healthz` -> `{"ok":true,"brand":"ChatGPT 发卡中心"}`.
- Direct homepage returned `ChatGPT 发卡中心`.
- End-to-end smoke test passed with a synthetic account:
  - admin generated one card
  - public redeem succeeded with `card_count=1`, `account_count=1`
  - `sub2api` download produced parseable JSON with one account
  - `cpa` download produced a zip with `cpa-auth/*.json`, `manifest.json`, and `README.txt`
  - `original` download produced a zip with `original/smoke.json` and `manifest.json`
  - smoke test inventory/card/batch/events were cleaned afterward, leaving zero cards in DB

## Anti-abuse

Source/origin fail2ban on `oracle-proxy`:

- `openclaw-gpt-card-general`: `/var/log/caddy/gpt-card-access.log`, 180 req / 60s -> 30m ban
- `openclaw-gpt-card-api`: `/var/log/caddy/gpt-card-access.log`, 40 API/admin-login req / 60s -> 1h ban

HK edge fail2ban on `hk-relay`:

- `openclaw-gpt-card-cn-general`: `/var/log/caddy/gpt-card-cn-access.log`, 180 req / 60s -> 30m ban
- `openclaw-gpt-card-cn-api`: `/var/log/caddy/gpt-card-cn-access.log`, 40 API/admin-login req / 60s -> 1h ban

## Pending

- Cloudflare DNS records added and both source/CN HTTPS entries verified HTTP 200 on 2026-06-07.
- Optionally add richer admin controls: delete/disable/restore cards, CSV export, file/card mapping export, and batch inventory grouping controls.
