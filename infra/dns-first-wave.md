# DNS First-Wave Change Set

这份文件已按 **2026-04-14 live Cloudflare 对账结果**重写。

它现在描述的是：
- **第一波低风险 DNS 清理里，哪些目标已经事实上完成**
- **从当前状态继续往下，剩下哪些才是下一步低风险动作**

不是历史上的预清理草案副本。

---

## 1. First-wave items already completed in the live zone

基于 2026-04-14 live zone：

- 当前 live zone **没有 `CNAME` 记录**
- 当前 live zone **没有 `SRV` 记录**
- 当前 live zone **没有 `TLSA` 记录**
- `autoconfig.zhangxuemin.work` / `autodiscover.zhangxuemin.work` 已不在 live zone
- 旧 mail client discovery 记录（`_autodiscover._tcp` / `_imaps._tcp` / `_pop3s._tcp` / `_submissions._tcp`）已不在 live zone
- 旧 `_25._tcp.mail.zhangxuemin.work` TLSA 已不在 live zone
- `dev.zhangxuemin.work` 的注释已与当前主机事实对齐（`openclaw-host`）
- `pend.zhangxuemin.work` 已不在当前 live zone

结论：
**最典型的“旧 mail 兼容记录清理”这波，DNS 层面其实已经基本做完。**

---

## 2. Preserve in the current live set

以下记录在当前 live zone 中应视为 **保留项**，不是第一波清理目标：

### Core active infra / delivery surfaces
- `proxy.zhangxuemin.work`
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
- `tmail.zhangxuemin.work`
- `tmail-front.zhangxuemin.work`

### Mail policy / sending-path records
- root MX records for Cloudflare Email Routing
- `zhangxuemin.work` root SPF
- `_dmarc.zhangxuemin.work`
- `send.zhangxuemin.work` MX / SPF (SES path)
- DKIM records (`cf2024-1._domainkey`, `dkim._domainkey`, `resend._domainkey`) — 先做归属文档化，不先删

---

## 3. What is no longer a first-wave deletion target

这些项不应再写成“第一波建议删除 / repoint”：

### `mail.zhangxuemin.work`
- 当前是 `oracle-mail` 上的 **活跃 `Outlook Email Plus` web app front door**
- 不能再沿用旧的“退役 mail host 待删除”判断

### `autoconfig` / `autodiscover` / old mail SRV / old mail TLSA
- 这些记录已经不在 live zone
- 对它们的正确描述应是：**历史清理已完成**，而不是“下一步准备删”

### `pend.zhangxuemin.work`
- 已不在当前 live zone
- 应从后续 cleanup 候选里移除

---

## 4. The real next low-risk actions from here

### A. Finish DKIM ownership reconciliation
目标记录：
- `cf2024-1._domainkey.zhangxuemin.work`
- `dkim._domainkey.zhangxuemin.work`
- `resend._domainkey.zhangxuemin.work`

动作：
- 把它们分别映射到当前或历史的发送路径
- 用“证据 + 置信度 + 处置建议”记录，而不是直接删除
- 参考：`infra/cloudflare-dns/dkim-reconciliation.md`

### B. Re-evaluate `backup.zhangxuemin.work`
- 当前它仍然指向 `oracle-gateway`
- 仍有实际 gateway / Hysteria 语义，不是“明显死记录”
- 但它已经不再是主公共 HTTPS front door，因此后续可以继续判断：
  - 保留为历史兼容 / 配置分发入口
  - 或在未来做更激进的网关命名收口

### C. Optional metadata hygiene
- 给活跃记录补更准确的注释/标签
- 避免把 comment 当成事实来源，但可以把 comment 维持在不误导的状态

---

## 5. Recommended execution order now

1. 完成 DKIM 归属文档化
2. 复核 `backup.zhangxuemin.work` 是否仍值得长期保留
3. 如有需要，再做 comment/tag 层面的轻量整理
4. 只有当未来 `mail.zhangxuemin.work` 角色再次迁移时，才重新讨论其 A 记录调整

---

## 6. One-line summary

### 已经完成的第一波
- 旧 mail 兼容层（CNAME / SRV / TLSA）已从 live zone 清掉
- `dev` 注释已纠正
- `pend` 已移除

### 当前该继续做的
- DKIM 归属收口
- `backup` 价值复核
- 活跃记录元数据整理

### 当前不要误删的
- `mail`
- `derp`
- `hk` / `drop.hk` / `clash.hk`
- `tmail` / `tmail-front`
- root MX / SPF / DMARC
- `send` SES 路径
- DKIM 记录
