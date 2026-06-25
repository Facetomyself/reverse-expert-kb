# 1Panel on ali-cloud

## 1. Summary
1Panel is the machine-level control plane on `ali-cloud`. It is running as a systemd-managed service and appears to own host port `80` directly.

## 2. Access / Entry Points
- systemd unit: `1panel.service`
- binary: `/usr/local/bin/1panel`
- host listener: `0.0.0.0:80`
- state root: `/opt/1panel`
- DB: `/opt/1panel/db/1Panel.db`
- logs: `/opt/1panel/log/`
- resource metadata: `/opt/1panel/resource/1panel.json`

## 3. Deployment Layout
- host-installed panel, not containerized
- integrates with Docker to manage at least some app deployments

## 4. Runtime Topology
- `1panel` process binds host port `80`
- Docker apps can coexist on alternate ports (for example EasyImages on `10086`)

## 5. Purpose and Workflow
Acts as the host's operations/control plane and likely stores app metadata, lifecycle state, and app marketplace/resource info.

## 6. Configuration / State
Observed state locations:
- `/opt/1panel/db/1Panel.db`
- `/opt/1panel/log/`
- `/opt/1panel/resource/1panel.json`

CLI capabilities observed:
- `1panel app`
- `1panel listen-ip`
- `1panel reset`
- `1panel restore`
- `1panel update`
- `1panel user-info`
- `1panel version`

## 7. Operations
### Check service status
```bash
ssh ali-cloud
systemctl status 1panel --no-pager -l
```

### Inspect service definition
```bash
ssh ali-cloud
sed -n '1,220p' /etc/systemd/system/1panel.service
```

### Check CLI help
```bash
ssh ali-cloud
1panel --help
```

## 8. Health Checks
Healthy signs:
- `1panel.service` is active/running
- host port `80` is listening by `1panel`
- `/opt/1panel/log/1Panel.log` updates normally

## 9. Data and Persistence
- panel state persisted under `/opt/1panel`
- app/control metadata likely stored in the SQLite DB `/opt/1panel/db/1Panel.db`

## 10. Common Tasks
- inspect panel status and logs
- determine whether an app is managed by 1Panel or manually deployed
- use 1Panel CLI carefully for recovery/update operations

## 11. Failure Modes / Troubleshooting
### Symptom: panel unavailable on port 80
Check:
- `systemctl status 1panel`
- `ss -ltnp | grep :80`
- `/opt/1panel/log/1Panel.log`

## 12. Dependencies / Cross-links
- coexists with Docker-managed apps
- see `PROJECTS.md` and `projects/easyimage.md`

## 13. Change History
- 2026-03-15: First documented from on-host inspection.
