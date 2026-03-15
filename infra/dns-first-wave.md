# DNS First-Wave Change Set

这份文件是基于当前已知事实整理出的**第一波可执行 DNS 变更清单**。

适用前提：
- 当前邮件临时方案在 Cloudflare 侧
- 旧 `oracle-mail` 自建邮件栈已退役
- 不再依赖旧自建 IMAP / POP3 / SMTP submission / autodiscover 体系

如果这些前提改变，这份清单就要重审。

---

## 1. Recommended first-wave changes

### A. Remove or repoint these records first

#### A records / CNAMEs
1. `mail.zhangxuemin.work`
   - Current: `A 140.83.52.216`
   - Reason: points to retired `oracle-mail` host
   - Action: **remove** if no longer needed, or **repoint** if a new mail frontend now exists

2. `autoconfig.zhangxuemin.work`
   - Current: `CNAME mail.zhangxuemin.work`
   - Reason: legacy client autoconfig path still chained to retired host
   - Action: **remove** unless a new mail client autoconfig endpoint exists

3. `autodiscover.zhangxuemin.work`
   - Current: `CNAME mail.zhangxuemin.work`
   - Reason: legacy client autodiscover path still chained to retired host
   - Action: **remove** unless a new autodiscover endpoint exists

### B. Remove the old mail client protocol advertisement records

4. `_autodiscover._tcp.zhangxuemin.work`
5. `_imaps._tcp.zhangxuemin.work`
6. `_pop3s._tcp.zhangxuemin.work`
7. `_submissions._tcp.zhangxuemin.work`

Reason:
- these advertise old self-hosted client protocols on top of a retired local mail host path
- current Cloudflare-side mail routing does not need them just for forwarding

Action:
- **remove** if you are no longer offering those client protocols yourself

### C. Remove the old mail-host TLSA bindings

8. `_25._tcp.mail.zhangxuemin.work` TLSA record #1
9. `_25._tcp.mail.zhangxuemin.work` TLSA record #2

Reason:
- these are tied to the old `mail.zhangxuemin.work` SMTP identity/path
- local mail stack on `oracle-mail` has already been retired

Action:
- **remove** if SMTP no longer terminates on that host/path

---

## 2. Metadata-only cleanup in the same wave

### `dev.zhangxuemin.work`
- Keep the A record for now
- Update/remove the stale Cloudflare comment `n8n`
- Replace with something accurate like:
  - `openclaw host`
  - `current main host`
  - or leave comment blank

This is low-risk housekeeping and should be done with the first wave.

---

## 3. Explicitly NOT in first wave

Do **not** touch these in the first cleanup wave:
- `proxy.zhangxuemin.work`
- `hub.zhangxuemin.work`
- `ghcr.zhangxuemin.work`
- `gcr.zhangxuemin.work`
- `quay.zhangxuemin.work`
- `k8sgcr.zhangxuemin.work`
- `mcr.zhangxuemin.work`
- `nvcr.zhangxuemin.work`
- `elastic.zhangxuemin.work`
- `hubcmd.zhangxuemin.work`
- `ui.zhangxuemin.work`
- root MX records for Cloudflare Email Routing
- SES-related `send` MX/SPF records
- DKIM records
- `pend.zhangxuemin.work`
- `backup.zhangxuemin.work`

Reason:
- these are either active, still useful, or not yet verified enough

---

## 4. One-line execution summary

### Delete / repoint now (first wave)
- `mail`
- `autoconfig`
- `autodiscover`
- `_autodiscover._tcp`
- `_imaps._tcp`
- `_pop3s._tcp`
- `_submissions._tcp`
- `_25._tcp.mail` TLSA x2

### Edit only
- `dev` comment

### Leave alone for now
- all active infra hostnames
- current Cloudflare MX / SPF path
- DKIM / uncertain records / `backup` / `pend`

---

## 5. Safer execution order in Cloudflare

1. Fix the `dev` comment
2. Remove `autoconfig` and `autodiscover`
3. Remove old SRV records
4. Remove old `_25._tcp.mail...` TLSA records
5. Remove or repoint `mail.zhangxuemin.work`

Why this order:
- it retires the least useful compatibility records first
- it leaves the raw `mail` hostname until the end, in case you want a brief safety window before removing/repointing it

---

## 6. After-change verification checklist

After the first wave, verify:
- Cloudflare Email Routing still shows healthy MX/TXT state
- inbound forwarding still works
- no one needs `autoconfig` / `autodiscover`
- no clients complain about missing IMAP/SMTP discovery
- no internal docs still point users at `mail.zhangxuemin.work`
