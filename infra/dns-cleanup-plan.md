# DNS Cleanup Plan

这份计划不是直接动 DNS，而是把当前对账结果转成**可执行动作清单**。

本版已按 **2026-06-08 live Cloudflare zone** 更新。

原则：
- 先保守，不误删现役记录
- 先承认哪些历史清理已经完成，不重复规划已经不存在的记录
- 优先清理“文档漂移”，再决定是否需要继续清理 live DNS
- 对 DKIM / 发件链路相关记录尤其谨慎，先确认归属再动

---

## 1. Do not touch now

这些记录当前与现实基本一致，暂时不要改：

### Core active infra / delivery surfaces
- `proxy.zhangxuemin.work`
- `proxy-bak.zhangxuemin.work`
- `backup.zhangxuemin.work`
- `derp.zhangxuemin.work`
- `dev.zhangxuemin.work`
- `hub.zhangxuemin.work`
- `ghcr.zhangxuemin.work`
- `k8s.zhangxuemin.work`
- `mcr.zhangxuemin.work`
- `mail.zhangxuemin.work`
- `hk.zhangxuemin.work`
- `drop.hk.zhangxuemin.work`
- `clash.hk.zhangxuemin.work`
- `cliproxy-cn.zhangxuemin.work`
- `proxy-bak-cn.zhangxuemin.work`
- `claw-cn.zhangxuemin.work`
- `cpam.zhangxuemin.work`
- `cpam-cn.zhangxuemin.work`
- `gptam.zhangxuemin.work`
- `gptam-cn.zhangxuemin.work`
- `kiro.zhangxuemin.work`
- `kiro-cn.zhangxuemin.work`
- `kiro-rs.zhangxuemin.work`
- `kiro-rs-cn.zhangxuemin.work`
- `docs.zhangxuemin.work`
- `docs-cn.zhangxuemin.work`
- `card.zhangxuemin.work`
- `card-cn.zhangxuemin.work`
- `gpt-card.zhangxuemin.work`
- `gpt-card-cn.zhangxuemin.work`
- `reverse-cn.zhangxuemin.work`
- `ctf-gpt-cn.zhangxuemin.work`
- `tmail.zhangxuemin.work`
- `tmail-front.zhangxuemin.work`

### Current policy / mail-path records
- `zhangxuemin.work MX -> route*.mx.cloudflare.net`
- `send.zhangxuemin.work MX -> feedback-smtp.ap-northeast-1.amazonses.com`
- `zhangxuemin.work TXT SPF include:_spf.mx.cloudflare.net`
- `send.zhangxuemin.work TXT SPF include:amazonses.com`
- `_dmarc.zhangxuemin.work`

Reason:
- 这些记录要么已与活跃主机/服务对齐
- 要么与当前 Cloudflare / SES mail path 相符
- 要么是当前 live zone 的核心 front door / 分发面 / SSH 边缘入口

---

## 2. Keep but monitor

### `backup.zhangxuemin.work`
- **Action**: keep for now
- **Reason**: 仍指向 `oracle-gateway`，且仍保留 gateway / Hysteria 语义
- **Follow-up**: 未来可单独判断是否继续保留为历史兼容入口，或与 `derp`/新网关命名体系做收口

### Remaining DKIM record
- `cf2024-1._domainkey.zhangxuemin.work`
- **Action**: keep first, document ownership before any further deletion
- **Reason**: 当前最大的不确定点不是 A 记录映射，而是这最后一条剩余 DKIM 与当前 provider-side / 根域邮件策略的关系
- **Reference**: `infra/cloudflare-dns/dkim-reconciliation.md`

---

## 3. Historical cleanup already completed

以下项目曾经属于合理清理目标，但**现在已经不在 live zone**：

### Old mail compatibility names
- `autoconfig.zhangxuemin.work`
- `autodiscover.zhangxuemin.work`

### Old mail discovery SRV records
- `_autodiscover._tcp.zhangxuemin.work`
- `_imaps._tcp.zhangxuemin.work`
- `_pop3s._tcp.zhangxuemin.work`
- `_submissions._tcp.zhangxuemin.work`

### Old mail TLSA records
- `_25._tcp.mail.zhangxuemin.work` TLSA x2

### Old uncertain host record
- `pend.zhangxuemin.work`

### Historical Mailu / moemail DKIM
- `dkim._domainkey.zhangxuemin.work`
- 已于 2026-04-14 在用户确认 Mailu 不再使用后删除
- `resend._domainkey.zhangxuemin.work`
- 已于 2026-04-14 在用户要求清理 moemail 残留后删除

结论：
这些不应该再出现在“待删第一波”的动作列表里；正确说法应是：
**live DNS 已经没有它们了，剩下的问题是文档是否同步。**

---

## 4. Current strongest documentation fixes

这些不是 live DNS 变更，而是应优先确保文档不再误导：

1. 不再把 `mail.zhangxuemin.work` 写成“退役 mail host 待删除”
   - 当前它是 `oracle-mail` 上的 `Outlook Email Plus` 活跃 web-app 域名

2. 不再把 `autoconfig` / `autodiscover` / old SRV / old TLSA 写成“仍存在的 live 记录”
   - 它们已经不在 2026-04-14 live zone

3. 把最后剩余 DKIM 记录从“模糊 leftovers”推进到“有来源说明的当前 provider-side / 根域邮件策略候选”

---

## 5. Remaining cleanup decisions

### A. Remaining DKIM ownership consolidation
对最后这条剩余记录回答：
- 它是否确实是当前 provider-side key？
- 是否仍有根域邮件策略依赖它？
- 如果未来删除，应该在哪个更大的邮件/发件切换窗口里做？

### B. `backup.zhangxuemin.work` role decision
需要回答：
- 它是长期保留的 gateway 兼容入口吗？
- 还是会在未来被 `derp` / 新网关命名替代？

### C. Optional comment/tag cleanup
如果未来还要做轻量整理：
- 优先补活跃记录的 comment/tag
- 不要把 comment 当唯一事实来源

---

## 6. Suggested execution order

### Phase 0 — Already done
- `dev` comment 已纠正
- old mail compatibility CNAME/SRV/TLSA 已从 live zone 消失
- `pend` 已移除
- `dkim._domainkey` 已随 Mailu 退场完成删除
- `resend._domainkey` 已随 moemail 残留清理完成删除

### Phase 1 — Finish DKIM reconciliation
- 完成 `infra/cloudflare-dns/dkim-reconciliation.md`
- 同步 `infra/dns-reconciliation.md` 中最后剩余 DKIM 的判断与状态

### Phase 2 — Review `backup`
- 明确 `backup.zhangxuemin.work` 的长期角色

### Phase 3 — Metadata-only cleanup
- comment / tag 级整理（如果值得）

### Phase 4 — Future mail-front-door review only if role changes
- 仅当 `mail.zhangxuemin.work` 的应用角色再次迁移时，才重新评估其 A 记录

---

## 7. Fast decision matrix

### Safe to keep now
- `proxy`
- `backup`
- `derp`
- `dev`
- `hub`
- `ghcr`
- `k8s`
- `mcr`
- `mail`
- `hk`
- `drop.hk`
- `clash.hk`
- `cliproxy-cn`
- `claw-cn`
- `tmail`
- `tmail-front`
- Cloudflare MX
- root SPF
- `_dmarc`
- `send` SES MX/SPF

### Investigate / document before touching
- `cf2024-1._domainkey`
- long-term role of `backup`

### No longer active cleanup targets because already gone
- `autoconfig`
- `autodiscover`
- old mail SRV
- old mail TLSA
- `pend`

---

## 8. Practical recommendation right now

基于当前 live zone 与主机文档：

### 现在最值得做的
- 完成最后剩余 DKIM 归属文档化
- 让 DNS 计划文档与 live zone 保持一致

### 现在最不值得做的
- 重复规划已经不在 live zone 的旧 mail 兼容记录
- 在没有发件链路归属证据前贸然删最后剩余 DKIM
- 把 `mail.zhangxuemin.work` 当作明显清理候选
