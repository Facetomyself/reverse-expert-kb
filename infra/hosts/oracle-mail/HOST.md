# oracle-mail

## 1. Identity
- Host label: `oracle-mail`
- Static hostname: `instance-20250217-0809`
- Provider: Oracle Cloud
- Primary role: web-app host with archived mail-stack context
- SSH alias: `oracle-mail`
- Main purpose: 当前对外承载 `mail.zhangxuemin.work` 的 `Outlook Email Plus` Web 应用；同时保留历史 Mailu / `moemail` 背景用于归档与后续参考

## 2. System Baseline
- OS: Oracle Linux Server 8.10
- Kernel: `5.15.0-304.171.4.el8uek.aarch64`
- Architecture: `arm64 / aarch64`
- Root disk: `36G total / 20G used / 16G free`
- Memory: `5.5 GiB`
- Swap: `4.0 GiB`

## 3. Usage Pattern
- Host style: lightly loaded single-purpose app host with archived mail-stack residue
- Change sensitivity: medium-high; public `mail.zhangxuemin.work` is live here, but classic mail protocols remain intentionally inactive
- Operational preference: preserve the current Outlook Email Plus deployment, and treat Mailu/moemail material as historical until there is an explicit reactivation plan

## 4. Access Notes
- Main SSH alias: `oracle-mail`
- Expected user: `root`
- SSH auth: key-based login via local SSH config entry using `IdentityFile ~/.ssh/oracle-mail`
- Tailnet IPv4: `100.116.13.44` (joined 2026-03-25)

## 5. High-Level Service Map
Current observed runtime:
- `outlook-email-plus-caddy` owns public `80/443` for `mail.zhangxuemin.work`
- `outlook-email-plus-app` runs behind Caddy on internal port `5000`
- Docker daemon running
- No active classic mail listeners on `25/465/587/110/995/143/993/4190`

Historical / archived project footprints:
- `/root/retired-services/2026-03-15/mailu` — archived dormant Mailu compose deployment
- `/root/retired-services/2026-03-15/moemail` — archived separate email-related application/repository

## 6. Machine-Level Infrastructure Notes
- firewalld inactive
- SELinux: `Enforcing`
- no current evidence of active postfix/dovecot/nginx/httpd stack outside Docker
- current public HTTPS service is containerized behind Caddy, not a host-installed web server
- recurring 2026-03-20 check confirmed `outlook-email-plus-caddy` still owns public `80/443` and `outlook-email-plus-app` remained healthy behind it
- Oracle Linux base remains suitable for container-first deployments; this host is no longer "empty" on 80/443

## 7. Documentation Scope
This host's docs should focus on:
- the live `Outlook Email Plus` deployment and its public entrypoint
- archived Mailu / moemail context and why it is no longer the active runtime
- the deliberate mismatch between active web UI service and still-inactive classic mail protocols
