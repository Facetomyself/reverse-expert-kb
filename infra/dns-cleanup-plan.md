# DNS Cleanup Plan

这份计划不是直接动 DNS，而是把对账结果转成**可执行动作清单**。

原则：
- 先保守，不误删现役记录
- 先清明显漂移，再碰历史兼容记录
- 对邮件相关记录尤其谨慎，先确认 Cloudflare 临时邮箱当前依赖

---

## 1. Do not touch now

这些记录当前与现实基本一致，暂时不要改：

### Core active infra
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

### Likely still valid policy records
- `zhangxuemin.work MX -> route*.mx.cloudflare.net`
- `send.zhangxuemin.work MX -> feedback-smtp.ap-northeast-1.amazonses.com`
- `zhangxuemin.work TXT SPF include:_spf.mx.cloudflare.net`
- `send.zhangxuemin.work TXT SPF include:amazonses.com`

Reason:
- these are either directly verified against active hosts
- or they align with the current Cloudflare/SES mail direction and should not be changed casually

---

## 2. Keep but monitor

### `ui.zhangxuemin.work`
- **Action**: keep
- **Reason**: host mapping is correct; problem is service health, not DNS
- **Follow-up**: only revisit DNS if the registry UI is intentionally retired or replaced

### `dev.zhangxuemin.work`
- **Action**: keep the A record for now
- **Reason**: it points to the correct machine (the current local host)
- **Cleanup needed**: remove/update the stale Cloudflare comment `n8n`

---

## 3. Confirm before changing

These are likely stale or uncertain, but should be explicitly confirmed before editing DNS.

### `backup.zhangxuemin.work`
- **Current status**: points to `oracle-docker-proxy`, but current Caddy mapping not confirmed
- **Action**: confirm whether it still has any real use
- **If no known use**: mark for deletion

### `pend.zhangxuemin.work`
- **Current status**: unresolved host (`217.142.242.113`), not yet audited
- **Action**: verify whether the host/service still exists
- **If dead/abandoned**: mark for deletion

### DKIM records
- `cf2024-1._domainkey.zhangxuemin.work`
- `dkim._domainkey.zhangxuemin.work`
- `resend._domainkey.zhangxuemin.work`
- **Action**: map each one to the currently active sending path
- **If tied to retired mail flows**: remove later in a controlled phase

### `zhangxuemin.work TLSA`
- **Action**: verify what service it is meant to authenticate today
- **Do not remove blindly** without understanding present usage

---

## 4. Strong cleanup candidates

These are the clearest drift candidates.

### Mail host A/CNAME records
- `mail.zhangxuemin.work`
- `autoconfig.zhangxuemin.work`
- `autodiscover.zhangxuemin.work`

**Why they are candidates:**
- they point to `oracle-mail`
- local Mailu/moemail stacks on that host have been retired
- current temporary mail is handled by another Cloudflare-based deployment
- external probes already show failed behavior (`443 refused` / `521`)

**Recommended action:**
1. confirm the Cloudflare temporary mail setup does not rely on these names
2. then either:
   - repoint them to the new active mail frontend, or
   - delete them if no longer needed

### Mail SRV records pointing to old host semantics
- `_autodiscover._tcp.zhangxuemin.work`
- `_imaps._tcp.zhangxuemin.work`
- `_pop3s._tcp.zhangxuemin.work`
- `_submissions._tcp.zhangxuemin.work`

**Why they are candidates:**
- they still advertise client protocols on the retired `mail.zhangxuemin.work` path
- runtime reality no longer matches

**Recommended action:**
- if the Cloudflare temporary mail solution does not use classic IMAP/POP3/SMTP submission on these names, retire these records

### TLSA records bound to old mail host path
- `_25._tcp.mail.zhangxuemin.work` TLSA records

**Why they are candidates:**
- they imply SMTP service semantics on the old local mail host path
- local mail service on `oracle-mail` is retired

**Recommended action:**
- confirm whether inbound/outbound SMTP still terminates there
- if not, remove with the mail cleanup wave

---

## 5. Suggested execution order

### Phase 0 — Metadata cleanup only (safe)
1. Update/remove stale Cloudflare comment for `dev.zhangxuemin.work` (`n8n`)
2. Add admin notes/tags to records that are known active vs known stale

### Phase 1 — Confirm old mail path is unused
Before changing records, answer:
- Does current Cloudflare temporary mail use `mail.zhangxuemin.work`?
- Does any client still rely on `autoconfig` / `autodiscover`?
- Are IMAP/POP3/SMTP submission protocols still supposed to exist for this domain?

### Phase 2 — Mail drift cleanup
If Phase 1 confirms the old path is unused:
1. repoint or remove:
   - `mail.zhangxuemin.work`
   - `autoconfig.zhangxuemin.work`
   - `autodiscover.zhangxuemin.work`
2. retire old SRV records
3. retire old mail TLSA records

### Phase 3 — Unused service-name cleanup
1. decide fate of `backup.zhangxuemin.work`
2. verify or remove `pend.zhangxuemin.work`
3. prune DKIM/TLSA leftovers that no longer map to active senders

---

## 6. Fast decision matrix

### Safe to keep now
- `proxy`
- `hub`
- `ghcr`
- `gcr`
- `quay`
- `k8sgcr`
- `mcr`
- `nvcr`
- `elastic`
- `hubcmd`
- Cloudflare MX
- SES MX/SPF

### Keep but fix metadata
- `dev`
- `ui`

### Likely remove or repoint after confirmation
- `mail`
- `autoconfig`
- `autodiscover`
- old mail SRV
- old mail TLSA

### Investigate first
- `backup`
- `pend`
- DKIM set overlap
- root TLSA

---

## 7. Most probable first cleanup wave

If you want the **lowest-risk first wave**, do this order:

1. Fix stale record comments/notes (`dev`)
2. Confirm old mail path is unused
3. Remove/repoint `mail` / `autoconfig` / `autodiscover`
4. Remove matching stale SRV/TLSA records
5. Audit `backup` and `pend`

That gives the best ratio of cleanup value to breakage risk.
