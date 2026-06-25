# EasyImages on ali-cloud

## 1. Summary
EasyImages is a 1Panel-managed app container providing an image-hosting service on host port `10086`.

## 2. Access / Entry Points
- Container: `easyimage`
- Public host port: `10086`
- Compose path: `/opt/1panel/apps/easyimage2/easyimage2/docker-compose.yml`

## 3. Deployment Layout
- Managed through 1Panel Apps
- Compose project: `easyimage2`
- Image: `ddsderek/easyimage:v2.8.6`
- Network: `1panel-network`

## 4. Runtime Topology
- host `10086` -> container `80`
- internal stack starts bundled `php-fpm` and `nginx`

## 5. Configuration / State
Config/data root:
- `/opt/1panel/apps/easyimage2/easyimage2/data/`

Important paths:
- `data/config/config.php`
- `data/config/config.guest.php`
- `data/config/config.manager.php`
- `data/config/api_key.php`
- `data/i/` (uploaded/generated images/cache)

## 6. Operations
### Check container
```bash
ssh ali-cloud
docker ps --filter name=easyimage
```

### Check compose definition
```bash
ssh ali-cloud
sed -n '1,260p' /opt/1panel/apps/easyimage2/easyimage2/docker-compose.yml
```

### Check logs
```bash
ssh ali-cloud
docker logs --tail 120 easyimage
```

## 7. Health Checks
Healthy signs:
- container is `Up`
- port `10086` is listening
- logs show normal init followed by `php-fpm` + `nginx` services

## 8. Data and Persistence
- images/cache persist under `data/i/`
- app config persists under `data/config/`

## 9. Failure Modes / Troubleshooting
### Symptom: app unavailable on `10086`
Check:
- `docker ps --filter name=easyimage`
- compose file in the 1Panel app path
- logs for init/config generation issues

## 10. Dependencies / Cross-links
- 1Panel-managed app
- see `projects/1panel.md`

## 11. Change History
- 2026-03-15: First documented from compose + container inspection.
