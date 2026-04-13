# oracle-mail

## Identity
- Name: `oracle-mail`
- Provider: Oracle Cloud Infrastructure
- Public IP: `140.83.52.216`
- SSH alias: `oracle-mail`
- Default SSH user: `opc`
- Primary role: web-app host

## Access
- OpenClaw-side SSH key path: `~/.ssh/oracle-mail.key`
- Current SSH verification: success
- Hostname is semantically treated as `oracle-mail`

## Runtime summary
- `mail.zhangxuemin.work` is currently live as the Outlook Email Plus web app via Docker Compose + Caddy
- active containers live under `/opt/outlook-email-plus`
- this host should be treated as an application host, not as part of any overlay-network control plane
