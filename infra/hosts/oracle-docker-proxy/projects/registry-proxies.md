# registry proxies on oracle-docker-proxy

## 1. Summary
This host runs a set of long-lived Docker registry proxy/mirror containers, all fronted by Caddy and exposed via dedicated `*.zhangxuemin.work` hostnames.

## 2. Access / Entry Points
Public hostnames currently mapped through Caddy:
- `hub.zhangxuemin.work` -> `localhost:51000`
- `ghcr.zhangxuemin.work` -> `localhost:52000`
- `gcr.zhangxuemin.work` -> `localhost:53000`
- `k8sgcr.zhangxuemin.work` -> `localhost:54000`
- `k8s.zhangxuemin.work` -> `localhost:55000`
- `quay.zhangxuemin.work` -> `localhost:56000`
- `mcr.zhangxuemin.work` -> `localhost:57000`
- `elastic.zhangxuemin.work` -> `localhost:58000`
- `nvcr.zhangxuemin.work` -> `localhost:59000`

Host SSH entry:
```bash
ssh oracle-docker_proxy
```

## 3. Deployment Layout
Containers observed:
- `reg-docker-hub`
- `reg-ghcr`
- `reg-gcr`
- `reg-k8s-gcr`
- `reg-k8s`
- `reg-quay`
- `reg-mcr`
- `reg-elastic`
- `reg-nvcr`

All currently use image:
- `dqzboy/registry:latest`

## 4. Runtime Topology
Each registry proxy publishes host port `5x000` to container port `5000`.

Common mount pattern:
- per-registry config file under `/data/registry-proxy/registry-*.yml` -> `/etc/distribution/config.yml`
- shared registry data directory `/data/registry-proxy/registry/data` -> `/var/lib/registry`

Observed mapping:
- `reg-docker-hub`: `/data/registry-proxy/registry-hub.yml`
- `reg-ghcr`: `/data/registry-proxy/registry-ghcr.yml`
- `reg-gcr`: `/data/registry-proxy/registry-gcr.yml`
- `reg-k8s-gcr`: `/data/registry-proxy/registry-k8sgcr.yml`
- `reg-k8s`: `/data/registry-proxy/registry-k8s.yml`
- `reg-quay`: `/data/registry-proxy/registry-quay.yml`
- `reg-mcr`: `/data/registry-proxy/registry-mcr.yml`
- `reg-elastic`: `/data/registry-proxy/registry-elastic.yml`
- `reg-nvcr`: `/data/registry-proxy/registry-nvcr.yml`

## 5. Purpose and Workflow
This stack provides domain-based registry mirrors/proxies so clients can pull through stable local hostnames rather than directly from upstream registries.

## 6. Configuration
Configuration is primarily file-based:
- per-registry config in `/data/registry-proxy/registry-*.yml`
- shared storage/cache in `/data/registry-proxy/registry/data`

## 7. Operations
### Check all proxy containers
```bash
ssh oracle-docker_proxy
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}' | egrep 'reg-|NAMES'
```

### Inspect one proxy config mount
```bash
ssh oracle-docker_proxy
docker inspect reg-ghcr --format '{{json .Mounts}}'
```

### Inspect config files on disk
```bash
ssh oracle-docker_proxy
find /data/registry-proxy -maxdepth 1 -type f | sort
```

## 8. Health Checks
Healthy signs:
- all `reg-*` containers are `Up`
- corresponding public hostname returns expected registry behavior
- container logs do not show persistent upstream/auth failures

## 9. Data and Persistence
Shared data/cache path:
- `/data/registry-proxy/registry/data`

Operational implication:
- multiple registry proxies appear to share one backing data directory, so storage pressure and cache interactions should be monitored carefully.

## 10. Common Tasks
- confirm hostname -> port -> container mapping
- inspect a per-registry config file
- restart one registry proxy without affecting the others

## 11. Failure Modes / Troubleshooting
### Symptom: one registry hostname fails
Check:
- Caddy hostname mapping
- matching host port listener
- target `reg-*` container status
- corresponding `/data/registry-proxy/registry-*.yml`

### Symptom: storage growth / cache confusion
Check:
- `/data/registry-proxy/registry/data`
- whether shared storage layout is intentional and acceptable

## 12. Dependencies / Cross-links
- Fronted by `projects/caddy.md`
- Likely related to Harbor stack under `/root/harbor`, but exact coupling still needs confirmation

## 13. Change History
- 2026-03-15: First documented from container inspection.
