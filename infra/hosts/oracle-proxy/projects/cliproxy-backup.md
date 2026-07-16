# CLIProxy Backup Pool

## 1. Summary
- Project: CLIProxy Backup Pool / `cliproxy-backup`
- Host: `oracle-proxy`
- Purpose: 独立备用 CLI Proxy API 池，与主池 `cliproxy` 区分开，作为备用 OpenAI-compatible proxy endpoint
- Runtime status: running
- Priority: Tier 2

## 2. Entry Points
- Global/direct API base: `https://proxy-bak.zhangxuemin.work/v1`
- Domestic/HK-optimized API base: `https://proxy-bak-cn.zhangxuemin.work/v1`
- Local container port: `8318`
- Public host port: `8318`

Topology:

```text
Client -> proxy-bak.zhangxuemin.work -> oracle-proxy:caddy-cpam -> 127.0.0.1:8318 -> cliproxy-backup
Client -> proxy-bak-cn.zhangxuemin.work -> hk-relay Caddy -> https://proxy-bak.zhangxuemin.work -> same backup pool
```

## 3. Deployment Layout
- Config directory: `/root/containers/cliproxy-backup`
- Config file: `/root/containers/cliproxy-backup/config.yaml`
- Auth directory: `/root/containers/cliproxy-backup/auth-dir`
- Container name: `cliproxy-backup`
- Image: `eceasy/cli-proxy-api:latest`
- Update helpers: `/root/update_cliproxy_backup.sh` under `/root/lib/cpa-stack/`, with unified stack wrapper `/root/update_cpa_stack.sh`
- Update logs: `/var/log/cpa-stack-update.log` (current unified cron) and legacy `/var/log/cliproxy-backup-update.log`

The pool was seeded from the primary `cliproxy` config/auth material, then separated onto port `8318`. From this point forward it should be treated as an independent pool: do not assume auth/config changes in one pool automatically propagate to the other unless deliberately copied.

## 4. Proxy / Egress Policy
- The backup pool intentionally keeps the same static residential proxy configuration as the primary pool at initial deployment.
- Do not remove or replace `proxy-url` lines casually; prior performance work showed the proxy affects latency but is part of the account-sensitive network posture.
- Secrets and full proxy credentials must stay on-host in config files and must not be copied into docs or chat.

## 5. TLS / Front Doors
### Direct/source front door on `oracle-proxy`
- Caddy container: `caddy-cpam`
- Config root: `/root/containers/caddy-cpam`
- Site: `proxy-bak.zhangxuemin.work` -> `127.0.0.1:8318`
- Public listener: shared `443`

### CN/HK edge on `hk-relay`
- Caddy config: `/etc/caddy/Caddyfile`
- Site: `proxy-bak-cn.zhangxuemin.work` -> `https://proxy-bak.zhangxuemin.work`
- Host header and TLS SNI are set to `proxy-bak.zhangxuemin.work`.

## 6. Update Automation
Root crontab on `oracle-proxy`:

```cron
30 6 * * * /root/update_cpa_stack.sh >> /var/log/cpa-stack-update.log 2>&1
```

The unified stack wrapper updates primary `cliproxy`, `cliproxy-backup`, and `cpa-manager-plus` in one daily batch so the CPA/CPA Plus estate advances together. Old backup scripts/logs were moved to `/root/.trash/cpa-update-cleanup-20260710-125712/`; active per-service implementations live under `/root/lib/cpa-stack/`. The backup helper now defaults to `eceasy/cli-proxy-api:latest`, matching the primary pool, and still validates `/management.html` HTTP 200 with rollback on failure.

Manual update:

```bash
ssh oracle-proxy
/root/update_cpa_stack.sh
```

Force recreate only the backup pool:

```bash
ssh oracle-proxy
/root/lib/cpa-stack/update_cliproxy_backup.sh --force-recreate
```

## 7. Operations
### Status
```bash
ssh oracle-proxy
docker ps --filter name=cliproxy-backup
ss -ltnp | grep 8318
```

### Logs
```bash
ssh oracle-proxy
docker logs --tail 100 cliproxy-backup
tail -n 100 /var/log/cliproxy-backup-update.log
```

### Health checks
```bash
curl -sS https://proxy-bak.zhangxuemin.work/
curl -sS https://proxy-bak-cn.zhangxuemin.work/
```

Expected unauthenticated `/` response includes:

```json
{"endpoints":["POST /v1/chat/completions","POST /v1/completions","GET /v1/models"],"message":"CLI Proxy API Server"}
```

`/v1/models` without an API key is expected to return `{"error":"Missing API key"}`.

## 8. Change History
- 2026-07-10: Updated both primary `cliproxy` and `cliproxy-backup` to the same latest CLIProxy image `eceasy/cli-proxy-api:latest` (`sha256:3e9b10b128286aaa0c172acb7f34d2f5b36710e1afff982aa3e5b260f9e4b7ed`). `cliproxy-backup` is no longer pinned to `v7.1.56`; `/root/lib/cpa-stack/update_cliproxy_backup.sh` now defaults to `latest`. Added unified `/root/update_cpa_stack.sh` and replaced the daily backup-only cron with `30 6 * * * /root/update_cpa_stack.sh >> /var/log/cpa-stack-update.log 2>&1`, so primary CPA, backup CPA, and CPA Manager Plus update together. Verified local and public direct/HK management pages returned HTTP 200 after update.
- 2026-06-09: Verified by direct tag testing that the `/management.html` outage was a bad upstream Docker build window, not a permanent CLIProxy feature removal: `v7.1.44` served the page, `v7.1.52` returned 404, and `v7.1.53` / `v7.1.56` served it normally again. The likely fix upstream was the `v7.1.52 -> v7.1.53` Docker change adding CA certificates for HTTPS support, which matches the panel’s runtime download/update mechanism. `cliproxy-backup` was first restored from the last known-good image already used by primary `cliproxy` (`sha256:249c97b7dea1ed1e258e0fb17704c8f2dbbef34c476b685587f1522c5443ce56`), then upgraded and pinned to `eceasy/cli-proxy-api:v7.1.56` after validation. `/root/lib/cpa-stack/update_cliproxy_backup.sh` now defaults to the pinned `v7.1.56` tag (with `CLIPROXY_BACKUP_IMAGE` override support) and treats `/management.html` returning HTTP 200 as part of health/rollback checks, not just container running + port listening.
- 2026-06-04: Deployed independent `cliproxy-backup` pool on `oracle-proxy:8318`; added direct `proxy-bak.zhangxuemin.work` and HK/CN `proxy-bak-cn.zhangxuemin.work`; installed daily image update cron; verified both HTTPS entrypoints returned HTTP 200 from the CLI Proxy API root endpoint.
