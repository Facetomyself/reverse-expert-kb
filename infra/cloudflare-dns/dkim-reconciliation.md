# DKIM Reconciliation Notes

本文件记录 **2026-04-14** 对当前 live zone 中 DKIM 相关记录的归属判断，以及同日执行的 Mailu / moemail 残留清理结果。

目标：
- 不把 DKIM 当作“看不懂就删”的残留项
- 用可追溯证据把它们映射到当前或历史发送路径
- 在证据不足时明确写出置信度，而不是装确定

---

## Current live DKIM-related records

- `cf2024-1._domainkey.zhangxuemin.work`

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

### `resend._domainkey.zhangxuemin.work`

#### Best mapping before deletion
**较大概率对应历史/外部 Resend 发件路径，也就是 moemail 相关残留。**

#### Evidence used for the decision
- `oracle-mail` 归档 `moemail` 项目 README 明确写明：
  - 发件能力基于 **Resend**
  - 自定义域名发件需要在 **Resend** 中验证域名
  - 代码中存在对 `https://api.resend.com/emails` 的调用
- 记录名本身直接包含供应商语义：`resend._domainkey`
- `oracle-mail` 上唯一仍保留的 moemail 主体残留是：
  - `/root/retired-services/2026-03-15/moemail`（约 1.9G，已删除）
- 主机上还可见 3 个明确带 `moemail` 内容的 Wrangler 日志（已删除）

#### Action taken
- 用户明确要求：**删/清理 moemail 相关残留**
- 已删除 `oracle-mail` 主机上的 moemail 归档目录：
  - `/root/retired-services/2026-03-15/moemail`
- 已删除 `oracle-mail` 主机上的 3 个 moemail Wrangler 日志：
  - `/root/.config/.wrangler/logs/wrangler-2026-02-26_02-35-54_337.log`
  - `/root/.config/.wrangler/logs/wrangler-2026-02-36-27_330.log`
  - `/root/.config/.wrangler/logs/wrangler-2026-02-36-42_948.log`
- 已从 Cloudflare live zone 删除：
  - `resend._domainkey.zhangxuemin.work`

#### Confidence
**高（作为 moemail 残留）**

#### Current status
- 该记录已不在当前 live zone
- 这条线现在应视为：**已完成的历史 moemail / Resend DKIM 清理**

---

## Record-by-record mapping

### 1. `cf2024-1._domainkey.zhangxuemin.work`

#### Best current mapping
**更像 provider-side / Cloudflare-side 的当前根域邮件策略相关 DKIM，而不是任何本机自建服务残留。**

#### Evidence
- selector 名称本身带有明显 provider 风格：`cf2024-1`
- 当前根域 mail policy 仍明显保留 Cloudflare 侧语义：
  - root MX -> `route*.mx.cloudflare.net`
  - root SPF -> `include:_spf.mx.cloudflare.net`
  - `_dmarc` 记录中也包含 Cloudflare DMARC 报告收件路径
- 2026-04-14 API probe with the current zone token confirmed Email Routing rules are active and route mail into the `temp-mail` worker (`tmail@zhangxuemin.work` plus an all-match worker rule), but the Cloudflare Email Routing DNS docs only explicitly require MX/SPF records rather than exposing a user-managed DKIM requirement at this layer.
- 当前已文档化的活跃主机/应用中，没有找到与 `cf2024-1` 对应的本机/容器内 DKIM 产物或自建发送器配置
- 当前 `Outlook Email Plus` 活跃部署未发现 DKIM / SMTP provider 线索，说明它不是 owner

#### Confidence
**中等**

#### Operational interpretation
- 这条记录更像**当前根域邮件策略链路中的 provider-side key**，而不是历史自建 Mailu / moemail 的直接遗留。
- 已有证据表明 zone 的 Email Routing / worker 接收链路仍在用，但现有证据还不足以把 `cf2024-1` 精确钉成某个单一 Cloudflare 子产品内部生成的 key。
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
- 不能简单把当前仅剩的 `cf2024-1` 武断归到 SES
- 也不能因为没看到明显 SES selector，就倒推出当前 provider-side key 一定没用

---

## Practical cleanup stance

### Keep now
- `cf2024-1._domainkey.zhangxuemin.work`
  - 当前更像 provider-side / Cloudflare-side mail-policy key，且 zone 的 Email Routing / worker 接收链路仍处于启用状态

### Already cleaned up
- `dkim._domainkey.zhangxuemin.work`
  - 已在 2026-04-14 随 Mailu 退场一起删除
- `resend._domainkey.zhangxuemin.work`
  - 已在 2026-04-14 随 moemail 残留清理一起删除

### Not safe to delete blindly
- `cf2024-1._domainkey.zhangxuemin.work`

---

## Summary

- `dkim._domainkey`：**高概率历史 Mailu，已于 2026-04-14 删除**
- `resend._domainkey`：**高概率 moemail / Resend 残留，已于 2026-04-14 删除**
- `cf2024-1._domainkey`：**中概率当前 provider-side / Cloudflare-side 根域邮件策略 key**

当前最合理动作不再是继续讨论 Mailu / moemail 残留是否保留，而是：
**把这两条已完成退场，把后续注意力只留给剩下的 `cf2024-1`。**
