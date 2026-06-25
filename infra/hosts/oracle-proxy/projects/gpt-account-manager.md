# GPT Account Manager

## 1. Summary
- Project: GPT Account Manager
- Upstream repo: `https://github.com/margetrp-hub/gpt-account-manager`
- Host: `oracle-proxy`
- Purpose: GPT 账号、邮箱、验证码、刷新队列、CPA 仓管等账号维护工作台
- Runtime status: running
- Priority: Tier 2

## 2. Entry Points
- Global/direct entry: `https://gptam.zhangxuemin.work/`
- Domestic/HK-optimized entry: `https://gptam-cn.zhangxuemin.work/`
- Site-level auth: application-level login page, enabled by `GPT_ACCOUNT_MANAGER_REQUIRE_LOGIN=1`; access token = `MAIL_PICKUP_ADMIN_TOKEN` from `/root/containers/gpt-account-manager/.env`
- Local origin port: `127.0.0.1:18765` -> container `8765`

Topology:

```text
Browser -> gptam.zhangxuemin.work -> oracle-proxy:caddy-cpam -> 127.0.0.1:18765 -> gpt-account-manager:8765
Browser -> gptam-cn.zhangxuemin.work -> hk-relay Caddy -> https://gptam.zhangxuemin.work -> same origin service
```

## 3. Deployment Layout
- Compose directory: `/root/containers/gpt-account-manager`
- Compose file: `/root/containers/gpt-account-manager/docker-compose.yml`
- Secret env file: `/root/containers/gpt-account-manager/.env` (`0600`; contains `MAIL_PICKUP_ADMIN_TOKEN`)
- Container name: `gpt-account-manager`
- Image: local build `gpt-account-manager:latest`
- Source revision deployed at initial install: `c18cbd4`
- Local deployment patch revisions:
  - `43d7676` (`feat: add optional site-wide login`)
  - `dcbb8f0` (`feat: group mailbox accounts by status`)
  - `e5e169a` (`feat: group unregistered mailbox accounts`)
  - `3f2d63c` (`fix: base unregistered grouping on verification mail evidence`)
  - `1f65603` (`feat: expose automatic mailbox status groups`)
- Persistent data directories: `/root/containers/gpt-account-manager/data` and `/root/containers/gpt-account-manager/.cache`

Security notes:
- Do not copy `.env` contents into docs or chat.
- The admin token is stored only on-host in `/root/containers/gpt-account-manager/.env`.
- The upstream application originally only protected admin endpoints with `MAIL_PICKUP_ADMIN_TOKEN`; this deployment adds a minimal, maintainable application-level full-site login switch via `GPT_ACCOUNT_MANAGER_REQUIRE_LOGIN=1`.
- The default upstream compose exposed `8765` publicly; deployment was corrected so the service is only published on `127.0.0.1:18765` and public traffic must pass through Caddy TLS.

## 4. TLS / Front Door
### Origin / direct path
- Caddy compose directory: `/root/containers/caddy-cpam`
- Caddyfile: `/root/containers/caddy-cpam/Caddyfile`
- Container name: `caddy-cpam`
- Public listener: `*:443`
- Site: `gptam.zhangxuemin.work` -> `127.0.0.1:18765`
- Caddy only handles TLS and reverse proxying; full-site access control is handled by the application login page.
- ACME note: `1panel` owns public `:80`, so the `gptam.zhangxuemin.work` Caddy site disables HTTP-01 and relies on TLS-ALPN-01 over `:443`.

### Domestic / HK edge path
- Host: `hk-relay`
- Caddyfile: `/etc/caddy/Caddyfile`
- Site: `gptam-cn.zhangxuemin.work` -> `https://gptam.zhangxuemin.work`
- HK edge Caddy only handles TLS and reverse proxying; full-site access control is handled by the origin application login page.
- Host header and TLS SNI are set to `gptam.zhangxuemin.work`.

## 5. DNS
Cloudflare DNS records created on 2026-06-06:
- `gptam.zhangxuemin.work` -> `158.178.236.241` (`oracle-proxy`)
- `gptam-cn.zhangxuemin.work` -> `154.86.30.10` (`hk-relay`)

Both records are DNS-only A records with TTL 300.

## 6. Operations

### Status
```bash
ssh oracle-proxy
cd /root/containers/gpt-account-manager
docker compose ps
docker logs --tail 100 gpt-account-manager
```

### Front-door status
```bash
ssh oracle-proxy 'cd /root/containers/caddy-cpam && docker compose ps && docker logs --tail 100 caddy-cpam'
ssh hk-relay 'systemctl status caddy --no-pager; journalctl -u caddy -n 100 --no-pager'
```

### Health checks
```bash
TOKEN=$(ssh oracle-proxy 'sed -n "s/^MAIL_PICKUP_ADMIN_TOKEN=//p" /root/containers/gpt-account-manager/.env | head -1')
curl -sS -o /dev/null -w '%{http_code}\n' https://gptam.zhangxuemin.work/        # expected 401 without Basic Auth
curl -sS -o /dev/null -w '%{http_code}\n' https://gptam-cn.zhangxuemin.work/     # expected 401 without Basic Auth
curl -sSL -u "gptam:$TOKEN" https://gptam.zhangxuemin.work/ | grep -o '<title>[^<]*'
curl -sSL -u "gptam:$TOKEN" https://gptam-cn.zhangxuemin.work/ | grep -o '<title>[^<]*'
```

Expected signs:
- `gpt-account-manager` container is healthy.
- `ss -ltnp` on `oracle-proxy` shows only `127.0.0.1:18765` for this service.
- Both direct and CN entrypoints redirect unauthenticated users to `/login.html?next=...`.
- Both direct and CN login pages return `<title>GPT账号管理助手 - 登录`.
- Posting the access token to `/auth/login` returns `{ "success": true }`; subsequent cookie-authenticated GET returns `<title>GPT账号管理助手`.
- The app returns HTTP 501 to `HEAD /`; use GET-based checks.

## 7. Change History
- 2026-06-06: Deployed from upstream `margetrp-hub/gpt-account-manager` on `oracle-proxy`; added direct `gptam` and HK/CN `gptam-cn` entrypoints; verified both GET paths returned the expected page title via resolved endpoints.

- 2026-06-06: Replaced the temporary Caddy Basic Auth stopgap with a formal application-level login page. Added `GPT_ACCOUNT_MANAGER_REQUIRE_LOGIN=1`, reused the existing `MAIL_PICKUP_ADMIN_TOKEN` and login cookie path, preserved the existing UI style, and removed Basic Auth from both Caddy entrypoints. Verified unauthenticated requests redirect to `/login.html?next=...`, token login succeeds, and cookie-authenticated GET returns the expected title.

- 2026-06-06: Added mailbox account status grouping in the account-management UI. Existing ban/error detection logic was already present (`last_status`, `last_error*`); the change keeps stored user groups intact and only changes rendering/sorting: normal accounts, error accounts, and banned/deactivated accounts are displayed as separate visual sections with status pills. Verified the rebuilt container served the updated `mailboxes.js` / `styles.css` after login.

- 2026-06-06: Added an additional “未完成注册账号” visual group in the mailbox-management UI, then corrected its evidence model. The current classifier no longer treats “missing verification code” text as a mail signal. It loads cached `mail_type=verification` messages, filters for OpenAI/ChatGPT verification evidence, and marks a checked account as unregistered only when no matching OpenAI verification message exists for that mailbox (or a completed check found zero messages). This remains display-only and does not rewrite user-assigned groups. Verified the rebuilt container served the updated `mailboxes.js` and `/client-api/messages?mail_type=verification` returned successfully.

- 2026-06-06: Exposed automatic mailbox status groups as first-class filters in the mailbox-management UI. Added a “未完成注册” side filter and renamed the error bucket to “收件异常”. Date/manual group filters now only show normal accounts; unregistered, mail-error, and banned/disabled accounts are pulled out into their automatic status groups without rewriting the stored `category`. Verified rebuilt container served updated `mailboxes.html`, `mailboxes.js`, and `styles.css`.
