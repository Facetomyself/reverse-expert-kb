# Kiro Docs Static Site

## 1. Summary
- Project: Kiro Docs
- Host: `oracle-proxy` source + `hk-relay` CN/HK edge
- Source repo: `https://github.com/Facetomyself/kiro`
- Source content scope: only `使用说明.md` plus required images under `图片/` and logo assets (`kiro.webp` / `kiro.jpg`)
- Site generator: VitePress
- Runtime status: running
- Priority: Tier 3

## 2. Entry Points
- Global/direct public docs site: `https://docs.zhangxuemin.work/`
- Domestic/HK-optimized public docs site: `https://docs-cn.zhangxuemin.work/`

Topology:

```text
Visitor -> docs.zhangxuemin.work -> oracle-proxy:caddy-cpam -> /srv/kiro-docs static dist
Visitor -> docs-cn.zhangxuemin.work -> hk-relay Caddy -> https://docs.zhangxuemin.work -> same static origin
```

## 3. Deployment Layout
On `oracle-proxy`:

```text
/root/containers/kiro-docs/site/
  package.json
  docs/index.md
  docs/图片/*.png
  docs/public/kiro.webp
  docs/public/kiro.jpg
  docs/.vitepress/config.mts
  docs/.vitepress/dist/
```

Caddy source front door:
- Compose directory: `/root/containers/caddy-cpam`
- Caddyfile: `/root/containers/caddy-cpam/Caddyfile`
- Static dist mount: `/root/containers/kiro-docs/site/docs/.vitepress/dist:/srv/kiro-docs:ro`
- Site block: `docs.zhangxuemin.work { root * /srv/kiro-docs; file_server }`

CN/HK edge on `hk-relay`:
- Caddyfile: `/etc/caddy/Caddyfile`
- Site block: `docs-cn.zhangxuemin.work` reverse-proxies to `https://docs.zhangxuemin.work` with origin Host/SNI set to `docs.zhangxuemin.work`.

## 4. Security Stance
- Public static docs only; no visitor uploads.
- Docs domain does not proxy Kiro-Go `/admin`, `/v1/messages`, `/v1/chat/completions`, or other API/admin paths.
- Kiro-Go secrets remain excluded: do not copy `/root/containers/kiro-go/.env`, `data/config.json`, admin passwords, account exports, cookies, or API keys into docs or chat.
- Source Caddy adds security headers: CSP, `nosniff`, `DENY` frame policy, strict referrer policy, and restrictive permissions policy.
- Examples in docs should use placeholders such as `YOUR_API_KEY`, `sk-...`, and sample domains rather than real credentials.

## 5. Traffic / Cache Stance
- Static Caddy front door uses gzip/zstd encoding where supported.
- Hashed assets under `/assets/*` use long immutable cache headers.
- Images and logo assets use long browser cache headers.
- HTML uses short cache headers so docs updates propagate quickly.
- HK edge currently reverse-proxies the source and relies on browser/cache headers; do not publish large downloads/videos through this docs site because `hk-relay` has a known 800G/month bidirectional traffic cap.

## 6. Operations

### Rebuild from source repo
```bash
rm -rf /tmp/kiro-doc-src /tmp/kiro-doc-site
git clone --depth 1 https://github.com/Facetomyself/kiro.git /tmp/kiro-doc-src
mkdir -p /tmp/kiro-doc-site/docs/public
cp /tmp/kiro-doc-src/使用说明.md /tmp/kiro-doc-site/docs/index.md
cp -a /tmp/kiro-doc-src/图片 /tmp/kiro-doc-site/docs/图片
cp /tmp/kiro-doc-src/kiro.webp /tmp/kiro-doc-site/docs/public/kiro.webp
cp /tmp/kiro-doc-src/kiro.jpg /tmp/kiro-doc-site/docs/public/kiro.jpg
# recreate package.json and docs/.vitepress/config.mts from the deployed copy if needed
cd /tmp/kiro-doc-site
npm install
npm run docs:build
```

### Health checks
```bash
curl -sS -o /dev/null -w '%{http_code}
' https://docs.zhangxuemin.work/
curl -sS -o /dev/null -w '%{http_code}
' https://docs-cn.zhangxuemin.work/
curl -sS -o /dev/null -w '%{http_code}
' https://kiro.zhangxuemin.work/admin
curl -sS -o /dev/null -w '%{http_code}
' https://kiro-cn.zhangxuemin.work/admin
```

Expected:
- docs global and CN return `200`
- Kiro-Go global and CN `/admin` remain `200`

## 7. DNS
Cloudflare DNS-only A records created on 2026-06-06:
- `docs.zhangxuemin.work` -> `158.178.236.241` (`oracle-proxy`)
- `docs-cn.zhangxuemin.work` -> `154.86.30.10` (`hk-relay`)

## 8. Change History
- 2026-06-06: Built VitePress docs site from `Facetomyself/kiro` using only `使用说明.md` and required images; deployed global source on `oracle-proxy` through `caddy-cpam`; added CN/HK edge on `hk-relay`; created Cloudflare DNS-only A records; verified both docs URLs returned HTTP 200 with security headers and image loading, and verified Kiro-Go `/admin` URLs still returned HTTP 200.

## 9. Anti-abuse / Rate-limit Protection
Implemented on 2026-06-06 using Caddy JSON access logs plus fail2ban/iptables bans. This avoids replacing the production Caddy binary with a plugin build.

### Global/source on `oracle-proxy`
- Caddy site: `docs.zhangxuemin.work`
- Access log: `/var/log/caddy/docs-access.log`
- fail2ban filters:
  - `/etc/fail2ban/filter.d/openclaw-caddy-json-docs.conf`
  - `/etc/fail2ban/filter.d/openclaw-caddy-json-docs-assets.conf`
- fail2ban jail file: `/etc/fail2ban/jail.d/openclaw-docs.local`
- Active jails:
  - `openclaw-docs-general`: 180 requests / 60s -> ban 30m
  - `openclaw-docs-assets`: 90 static/image requests / 60s -> ban 1h
- Important ignore list includes `154.86.30.10` (`hk-relay`) so domestic/CN edge traffic does not accidentally ban the relay at the source.

### CN/HK edge on `hk-relay`
- Caddy site: `docs-cn.zhangxuemin.work`
- Access log: `/var/log/caddy/docs-cn-access.log`
- fail2ban filters:
  - `/etc/fail2ban/filter.d/openclaw-caddy-json-docs.conf`
  - `/etc/fail2ban/filter.d/openclaw-caddy-json-docs-assets.conf`
- fail2ban jail file: `/etc/fail2ban/jail.d/openclaw-docs-cn.local`
- Active jails:
  - `openclaw-docs-cn-general`: 180 requests / 60s -> ban 30m
  - `openclaw-docs-cn-assets`: 90 static/image requests / 60s -> ban 1h

### Verification
- Synthetic log trigger test confirmed both `openclaw-docs-assets` and `openclaw-docs-cn-assets` ban at 95 static/image hits and can unban immediately.
- Runtime checks after enabling protection:
  - `https://docs.zhangxuemin.work/` -> HTTP 200
  - `https://docs-cn.zhangxuemin.work/` -> HTTP 200
  - sample docs image through CN edge -> HTTP 200
  - `https://kiro.zhangxuemin.work/admin` -> HTTP 200
  - `https://kiro-cn.zhangxuemin.work/admin` -> HTTP 200
