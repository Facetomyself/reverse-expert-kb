# DKIM Reconciliation Notes

本文件记录 **2026-04-14** 对当前 live zone 中 DKIM 相关记录的归属判断，以及同日执行的 Mailu 退场清理结果。

目标：
- 不把 DKIM 当作“看不懂就删”的残留项
- 用可追溯证据把它们映射到当前或历史发送路径
- 在证据不足时明确写出置信度，而不是装确定

---

## Current live DKIM-related records

- `cf2024-1._domainkey.zhangxuemin.work`
- `resend._domainkey.zhangxuemin.work`

同时可见的相关邮件策略记录：
- root MX -> `route*.mx.cloudflare.net`
- root SPF -> `include:_spf.mx.cloudflare.net`
- `_dmarc.zhangxuemin.work`
- `send.zhangxuemin.work MX -> feedback-smtp.ap-northeast-1.amazonses.com`
- `send.zhangxuemin.work SPF -> include:amazonses.com`

---

## Removed on 2026-04-14

### `dkim._domainkey.zhangxuemin.work`

#### Best mapping before deletion
**高概率对应历史 `oracle-mail` 上的自建 Mailu 邮件栈。**

#### Evidence used for the decision
- `oracle-mail` 归档 Mailu 配置曾保留：
  - `/root/retired-services/2026-03-15/mailu/mailu.env`
  - 其中明确：
    - `DOMAIN=zhangxuemin.work`
    - `HOSTNAMES=mail.zhangxuemin.work`
- `oracle-mail` 主机上当时仍存在 Mailu 持久化 DKIM 实体文件：
  - `/mailu/dkim/zhangxuemin.work.dkim.key`
- 该记录名本身是最常见、最朴素的通用 selector：`dkim`
- 当前活跃的 `Outlook Email Plus` 部署中未发现任何 DKIM / SMTP provider 配置线索，说明活跃 web app 本身不是这条记录的直接 owner

#### Action taken
- 用户明确确认：**Mailu 已不再使用，可以删除**
- 已删除 `oracle-mail` 主机上的 Mailu 相关残留：
  - `/mailu`
  - `/root/retired-services/2026-03-15/mailu`
- 已从 Cloudflare live zone 删除：
  - `dkim._domainkey.zhangxuemin.work`

#### Confidence
**高**

#### Current status
- 该记录已不在当前 live zone
- 这条线现在应视为：**已完成的历史 Mailu DKIM 清理**

---

## Record-by-record mapping

### 1. `resend._domainkey.zhangxuemin.work`

#### Best current mapping
**较大概率对应历史/外部 Resend 发件路径。**

#### Evidence
- `oracle-mail` 归档 `moemail` 项目 README 明确写明：
  - 发件能力基于 **Resend**
  - 自定义域名发件需要在 **Resend** 中验证域名
  - 代码中存在对 `https://api.resend.com/emails` 的调用
- 记录名本身直接包含供应商语义：`resend._domainkey`
- 归档 `moemail/.env` 中 `CUSTOM_DOMAIN=""`，说明保存在仓库里的样例/本地配置并未把自定义域名硬编码死；因此这条 live 记录可能是：
  - 某次实际 Resend 域名验证后保留的记录
  - 或另一个未完整保存在该归档 `.env` 中的 Resend 发件链路

#### Confidence
**中等**

#### Operational interpretation
- 这条记录非常像 **Resend 相关 DKIM**，但仅凭当前仓库/归档不能证明它今天一定仍在用。
- 它不是当前 `Outlook Email Plus` 活跃 web app 的直接配置产物。

#### Recommended action
- 当前先保留
- 未来若要清理，需先确认是否仍存在任何 Resend-based 发件或历史依赖

---

### 2. `cf2024-1._domainkey.zhangxuemin.work`

#### Best current mapping
**更像 provider-side / Cloudflare-side 的当前根域邮件策略相关 DKIM，而不是任何本机自建服务残留。**

#### Evidence
- selector 名称本身带有明显 provider 风格：`cf2024-1`
- 当前根域 mail policy 仍明显保留 Cloudflare 侧语义：
  - root MX -> `route*.mx.cloudflare.net`
  - root SPF -> `include:_spf.mx.cloudflare.net`
  - `_dmarc` 记录中也包含 Cloudflare DMARC 报告收件路径
- 当前已文档化的活跃主机/应用中，没有找到与 `cf2024-1` 对应的本机/容器内 DKIM 产物或自建发送器配置
- 当前 `Outlook Email Plus` 活跃部署未发现 DKIM / SMTP provider 线索，说明它不是 owner

#### Confidence
**中等**

#### Operational interpretation
- 这条记录更像**当前根域邮件策略链路中的 provider-side key**，而不是历史自建 Mailu 的直接遗留。
- 在没有 Cloudflare 控制台侧进一步确认前，不应把它当成可随手删除的历史垃圾。

#### Recommended action
- 当前保留
- 未来如果做一次完整的 Cloudflare mail-policy / provider inventory，再从控制台或供应商文档确认其确切归属

---

## What is clearly separate from these DKIM records

### `send.zhangxuemin.work` SES path
当前 live zone 里已确认：
- `send.zhangxuemin.work MX -> feedback-smtp.ap-northeast-1.amazonses.com`
- `send.zhangxuemin.work SPF -> include:amazonses.com`

这说明 **SES 发送路径是存在的**。

但在当前 live snapshot 中，没有看到一个显式以 `send` 为 selector/owner 命名的 DKIM 记录，因此：
- 不能简单把现有 3 条 DKIM 中任意一条武断归到 SES
- 也不能因为没看到明显 SES selector，就倒推出其它 DKIM 一定没用

---

## Practical cleanup stance

### Keep now
- `cf2024-1._domainkey.zhangxuemin.work`
- `resend._domainkey.zhangxuemin.work`

### Already cleaned up
- `dkim._domainkey.zhangxuemin.work`
  - 已在 2026-04-14 随 Mailu 退场一起删除

### Not safe to delete blindly
- `cf2024-1._domainkey.zhangxuemin.work`
- `resend._domainkey.zhangxuemin.work`

---

## Summary

- `dkim._domainkey`：**高概率历史 Mailu，已于 2026-04-14 删除**
- `resend._domainkey`：**中概率历史/外部 Resend 发件路径**
- `cf2024-1._domainkey`：**中概率当前 provider-side / Cloudflare-side 根域邮件策略 key**

当前最合理动作不再是继续讨论 Mailu DKIM 是否保留，而是：
**把 Mailu 视为已完成退场，把后续注意力留给剩余两条 DKIM 的归属与长期去留。**
