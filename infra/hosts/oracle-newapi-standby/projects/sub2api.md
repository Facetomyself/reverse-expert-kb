# Sub2API on oracle-newapi-standby

## Status
- Deployed: 2026-07-22
- Runtime: Docker Compose under `/opt/sub2api`
- App image: `weishaw/sub2api:latest`
- Containers:
  - `sub2api`
  - `sub2api-postgres`
  - `sub2api-redis`
- Host listener: `127.0.0.1:18088 -> container:8080`
- Public source/global entry: `https://sub2api.zhangxuemin.work`
- Domestic/CN optimized entry: `https://sub2api-cn.zhangxuemin.work` via `hk-relay`

## Topology
- Business origin runs on `oracle-newapi-standby`.
- Caddy on `oracle-newapi-standby` terminates TLS for `sub2api.zhangxuemin.work` and reverse-proxies to `127.0.0.1:18088`.
- Caddy on `hk-relay` terminates TLS for `sub2api-cn.zhangxuemin.work` and reverse-proxies to `https://sub2api.zhangxuemin.work` with upstream Host/SNI set to the source domain.
- DNS records:
  - `sub2api.zhangxuemin.work A 140.245.61.236` DNS-only, ttl 300
  - `sub2api-cn.zhangxuemin.work A 154.86.30.10` DNS-only, ttl 300

## Data and credentials
- Deployment root: `/opt/sub2api`
- Compose file: `/opt/sub2api/docker-compose.yml`
- Persistent data directories:
  - `/opt/sub2api/data`
  - `/opt/sub2api/postgres_data`
  - `/opt/sub2api/redis_data`
- Environment / generated secrets: `/opt/sub2api/.env`
  - Includes `ADMIN_PASSWORD`, `POSTGRES_PASSWORD`, `JWT_SECRET`, and `TOTP_ENCRYPTION_KEY`.
  - Do not commit these secret values into infra docs.

## Operational commands
```bash
ssh oracle-newapi-standby
cd /opt/sub2api
sudo docker compose ps
sudo docker compose logs -f sub2api
sudo docker compose pull
sudo docker compose up -d
curl -fsS http://127.0.0.1:18088/health
```

## Network notes
- Sub2API itself is loopback-only on the origin host.
- Public access is through Caddy on `80/443`.
- On first deployment, origin iptables already allowed `22` and `80` but rejected `443`; an explicit `443/tcp` ACCEPT rule was inserted before the final reject rule.
- Keep the direct/global source entry reachable as a fallback; do not make HK relay the only path.

## Validation on 2026-07-22
- `https://sub2api.zhangxuemin.work/health` returned `200` with `{"status":"ok"}` from remote IP `140.245.61.236`.
- `https://sub2api-cn.zhangxuemin.work/health` returned `200` with `{"status":"ok"}` from remote IP `154.86.30.10`.
- `docker compose ps` showed all three containers up; `sub2api` health status was `healthy`.
