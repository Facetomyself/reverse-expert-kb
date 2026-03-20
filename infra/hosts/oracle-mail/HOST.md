# oracle-mail

## 1. Identity
- Host label: `oracle-mail`
- Static hostname: `instance-20250217-0809`
- Provider: Oracle Cloud
- Primary role: mail host / mail platform staging-or-dormant host
- SSH alias: `oracle-mail`
- Main purpose: 计划/曾经承载 Mailu 邮件栈；同时存在一个独立的 `moemail` 项目仓

## 2. System Baseline
- OS: Oracle Linux Server 8.10
- Kernel: `5.15.0-304.171.4.el8uek.aarch64`
- Architecture: `arm64 / aarch64`
- Root disk: `36G total / 20G used / 16G free`
- Memory: `5.5 GiB`
- Swap: `4.0 GiB`

## 3. Usage Pattern
- Host style: currently underutilized / partially deployed
- Change sensitivity: medium-high; MX/DNS already point here, but active mail service is not currently exposed
- Operational preference: verify why Mailu is not running before attempting any activation

## 4. Access Notes
- Main SSH alias: `oracle-mail`
- Expected user: `root`
- SSH auth: key-based login via local SSH config entry using `IdentityFile ~/.ssh/oracle-mail`

## 5. High-Level Service Map
Current observed runtime:
- SSH only on port `22`
- Docker daemon running
- No running containers
- No active host mail/web listeners on `25/80/443/143/993/...`

Retired on-disk project footprints:
- `/root/retired-services/2026-03-15/mailu` — archived dormant Mailu compose deployment
- `/root/retired-services/2026-03-15/moemail` — archived separate email-related application/repository

## 6. Machine-Level Infrastructure Notes
- firewalld inactive
- SELinux: `Enforcing`
- no current evidence of active postfix/dovecot/nginx/httpd stack outside Docker
- current public HTTPS service is containerized behind Caddy, not a host-installed web server
- Oracle Linux base remains suitable for container-first deployments; this host is no longer "empty" on 80/443

## 7. Documentation Scope
This host needs documentation for:
- Mailu deployment layout and why it is dormant
- moemail project purpose and deployment state
- DNS vs actual runtime mismatch
 is dormant
- moemail project purpose and deployment state
- DNS vs actual runtime mismatch
