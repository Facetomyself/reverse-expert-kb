# Card Shop / Kiro Card Redeem

## 1. Summary
- Project: Card Shop
- Host: `oracle-proxy` source + `hk-relay` CN/HK edge
- Purpose: public card-code redemption/query site plus authenticated admin backend for JSON-driven card generation.
- Runtime status: running
- Priority: Tier 2
- Style target: dark/neon card layout inspired by `pool.acteam.lol`; only design mood was referenced, not after-sales/support flows.

## 2. Entry Points
- Global/direct public site: `https://card.zhangxuemin.work/`
- Domestic/HK-optimized site: `https://card-cn.zhangxuemin.work/`
- Admin login: `https://card.zhangxuemin.work/admin/login`

Topology:

```text
Visitor/Admin -> card.zhangxuemin.work -> oracle-proxy:caddy-cpam -> 127.0.0.1:18767 -> card-shop:3000
Visitor/Admin -> card-cn.zhangxuemin.work -> hk-relay Caddy -> https://card.zhangxuemin.work -> same origin
```

## 3. Deployment Layout
On `oracle-proxy`:

```text
/root/containers/card-shop/
  app/                  # Node/Express application source
  data/cardshop.db       # SQLite database
  data/cardshop.db-wal   # SQLite WAL, when active
  .env                  # 0600, contains ADMIN_PASSWORD and SESSION_SECRET
  docker-compose.yml
```

Container/runtime:
- Container name: `card-shop`
- Local published port: `127.0.0.1:18767 -> 3000`
- DB path in container: `/data/cardshop.db`
- Source Caddy access log: `/var/log/caddy/card-access.log`
- CN/HK Caddy access log: `/var/log/caddy/card-cn-access.log` on `hk-relay`

## 4. Functional Scope
Public visitor functions:
- Redeem a card code.
- Query card status/history only after the card has already been redeemed/opened.
- Unredeemed/new/nonexistent cards return a non-disclosing failure for history query.

Admin functions:
- Password-authenticated admin console.
- One-delivery-JSON-to-one-card generation.
- Single JSON object input, JSON object array input, and multi-file JSON upload/merge in the admin page.
- Delivery JSON deduplication by canonical SHA-256 hash (`delivery_hash`).
- Recent card list.
- Search by card code, batch id, or status.
- Card detail page with event history.

No after-sales/support function is implemented by design.

## 5. Card Generation
Admin delivery JSON model:

```json
{
  "account": "example@example.com",
  "password": "the-secret-to-deliver",
  "quota": 20000
}
```

或一次输入对象数组；每个对象生成一张卡密：

```json
[
  { "account": "a@example.com", "password": "secret-a" },
  { "account": "b@example.com", "password": "secret-b" }
]
```

Card code policy:
- Default random payload: 32 human-safe characters grouped with hyphens, e.g. `KIRO-XXXXX-XXXXX-...`.
- Default entropy is about 160 bits, enough for practical anti-guessing / anti-collision use.
- Generator enforces minimum `code_bytes = 32` and maximum `48`.
- Codes are stored uniquely in SQLite.
- `delivery_hash = sha256(stable/canonical JSON)` is unique for non-empty delivery payloads; duplicate delivery JSON is skipped instead of generating another card.

## 6. Security Stance
- Admin session cookie is `HttpOnly`, `Secure`, `SameSite=Lax`.
- Admin password and session secret are in `/root/containers/card-shop/.env`; do not copy values into docs/chat.
- SQLite stores card data and event history; no public file serving from the data directory.
- `payload` is the card delivery JSON: it is returned to the user on successful redeem and on later queries for already-redeemed cards.
- Public query still refuses unactivated inventory to prevent probing / pre-redeem leakage.
- Admin notes and internal event details are not exposed on the visitor UI/API.
- Application uses Helmet security headers and Caddy adds additional basic hardening headers.

## 7. Anti-abuse / Rate Limits
Application-level Express limits:
- Public routes: 60 requests / 60s
- `/api/redeem` and `/api/query`: 20 requests / 60s
- `/admin/*`: 40 requests / 60s

Source fail2ban on `oracle-proxy`:
- Log: `/var/log/caddy/card-access.log`
- Jails:
  - `openclaw-card-general`: 180 requests / 60s -> 30m ban
  - `openclaw-card-api`: 40 `/api/redeem`, `/api/query`, or `/admin/login` requests / 60s -> 1h ban
- `hk-relay` is in `ignoreip` to prevent the source from banning the CN edge.

CN/HK fail2ban on `hk-relay`:
- Log: `/var/log/caddy/card-cn-access.log`
- Jails:
  - `openclaw-card-cn-general`: 180 requests / 60s -> 30m ban
  - `openclaw-card-cn-api`: 40 `/api/redeem`, `/api/query`, or `/admin/login` requests / 60s -> 1h ban

## 8. Operations

### Status
```bash
ssh oracle-proxy
cd /root/containers/card-shop
docker compose ps
docker logs --tail 100 card-shop
curl -sS http://127.0.0.1:18767/healthz
```

### Restart / rebuild
```bash
ssh oracle-proxy
cd /root/containers/card-shop
docker compose build card-shop
docker compose up -d card-shop
```

### Public smoke checks
```bash
curl -sS -o /dev/null -w '%{http_code}
' https://card.zhangxuemin.work/
curl -sS -o /dev/null -w '%{http_code}
' https://card-cn.zhangxuemin.work/
curl -sS -o /dev/null -w '%{http_code}
' https://card.zhangxuemin.work/admin/login
```

Expected: `200`.

## 9. DNS
Cloudflare DNS-only A records created on 2026-06-06:
- `card.zhangxuemin.work` -> `158.178.236.241` (`oracle-proxy`)
- `card-cn.zhangxuemin.work` -> `154.86.30.10` (`hk-relay`)

## 10. Verification
2026-06-06 smoke test:
- Local container health check returned JSON `ok: true`.
- Public global and CN home pages returned HTTP 200.
- Admin login page returned HTTP 200.
- Admin JSON generation created test cards.
- Query before redeem returned HTTP 404 / non-disclosing failure.
- Redeem through `card-cn` returned HTTP 200.
- Query after redeem through `card-cn` returned HTTP 200 with event history.
- Admin search found the smoke-test card.
- Synthetic 45-hit `/api/query` log tests triggered and then unbanned:
  - `openclaw-card-api`
  - `openclaw-card-cn-api`
- Existing `kiro.zhangxuemin.work/admin` and `docs.zhangxuemin.work/` remained HTTP 200.

## 11. Change History
- 2026-06-06: Deployed initial Card Shop MVP with public redeem/query, admin login, JSON batch generation, card search/detail/history, long random cards, app-level rate limits, Caddy front doors, DNS, and fail2ban anti-abuse protection.

## 12. 2026-06-06 admin hardening pass
- Removed MVP/test-site style wording from the visitor page.
- Visitor API no longer exposes internal payload JSON or admin notes.
- Added admin-side card deletion, bulk operations, per-card disable/enable, and global redeem on/off switch.
- Cleared smoke-test / length-check / admin-check cards and orphan test events from the live database; final verification showed `cards: []`, `events: []`, and `redeem_enabled: 1`.
- Verification covered: public home 200, CN home 200, admin login 200, admin search 200, disable blocking redeem, global switch blocking redeem, delete operation removing a disposable card, and existing Kiro/docs endpoints unaffected.

## 13. 2026-06-06 delivery JSON correction
- Corrected product behavior: card `payload` is not an internal-only field; it is the JSON payload delivered by a card.
- Admin generation form now labels `payload` as the JSON users receive after redeeming.
- Redeem success returns `card.payload`.
- Querying an already-redeemed card also returns `card.payload`.
- Querying before redeem still returns 404 and does not leak payload.
- Verification used a nested JSON payload with account/password/quota/features, confirmed redeem and post-redeem query returned it intact, then removed the temporary verification card.

## 14. 2026-06-06 one JSON per card model
- Corrected generation semantics: one complete delivery JSON maps to exactly one card code.
- Removed `count`-based same-payload batch generation.
- Admin generation now accepts either a single JSON object or an array of JSON objects; each object generates one card.
- Admin page includes multi-select JSON file input; selected files are read in-browser and merged into the delivery JSON textarea. If a file contains an array, its objects are expanded.
- Added `delivery_hash` with a unique index over canonical JSON content; duplicate JSON payloads are skipped and reported.
- Card list now has a visible per-row delete button in addition to bulk delete and detail-page delete.
- Verification: two distinct JSON objects generated two cards; resubmitting the same array created zero and skipped two; pre-redeem query did not leak payload; redeem returned the matching JSON; visible delete control confirmed; temporary verification cards were removed.

## 15. 2026-06-07 production Kiro JSON listing
- After user-side redemption testing, the remaining test cards/events were cleared from the live Card Shop database.
- Two delivery JSON objects from `Facetomyself/kiro` were listed as live `Kiro-Go / pro` cards.
- Live DB verification immediately after listing:
  - `cards`: 2
  - status summary: `new = 2`
  - `events`: one `batch_generated` maintenance event
- Public CN entry `https://card-cn.zhangxuemin.work/` returned HTTP 200 after the update.
- A database backup was created on `oracle-proxy` under `/root/containers/card-shop/data/cardshop.db.bak-before-kiro-prod-*` before the cleanup/listing operation.

## 16. 2026-06-07 delivery JSON order preservation
- The two live Kiro JSON card payloads were restored to the original repository key order after noticing that the initial listing stored canonical/sorted JSON for delivery display.
- Application generation logic now stores delivered payload JSON with `JSON.stringify(payload)` to preserve parsed input key order, while still using canonical SHA-256 hashing only for duplicate detection.
- Rebuilt/restarted `card-shop`; verified container up and `https://card-cn.zhangxuemin.work/` HTTP 200.

## 17. 2026-06-07 raw repository JSON delivery correction
- Corrected the live two Kiro cards to deliver the original JSON file content from `Facetomyself/kiro`, including the original top-level array wrapper and formatting, instead of the previously parsed single object form.
- Verification showed both live `payload_json` values parse as JSON arrays with one item and retain the repository file beginning/order.
- CN public entry remained HTTP 200 after the database correction.

## 18. 2026-06-07 raw Kiro card reissue
- The two Kiro cards were reissued from scratch to avoid ambiguity from earlier parsed/canonicalized payload attempts.
- Previous live card rows/events were deleted; two new `new` cards were inserted, each storing the original repository JSON file content as `payload_json`.
- Deduplication hash for this reissue was computed from the parsed full file content, including the top-level array wrapper.
- Verification: DB status `new=2`, both stored payloads parse as arrays with one item, and CN public entry returned HTTP 200.
