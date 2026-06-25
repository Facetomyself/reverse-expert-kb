# Kiro 文档静态站架构设计

Created: 2026-06-06
Status: draft-design
Scope: 游客可访问的 Kiro 反代文档静态站；首期只提供 Markdown 文档和图片，后续预留发卡 / 购买 / 授权扩展。

## 1. 目标

- 对外提供公开文档站，游客无需登录即可访问。
- 支持 Markdown 内容、图片、版本化文档、搜索、基础 SEO。
- 国内外双通道访问：海外/全局直达源站，国内走香港优化入口。
- 安全优先：文档站与 Kiro-Go 管理/API面彻底隔离，不暴露后台、密钥、配置、账号信息。
- 流量优先：静态化、边缘缓存、图片压缩、限速/防盗链，避免 HK relay 被无意消耗流量。
- 可扩展：后续发卡/订单/支付/API 授权作为独立服务挂载，不污染静态文档站。

## 2. 推荐总体架构

```text
Visitor Global
  -> docs.zhangxuemin.work
  -> Oracle/global HTTPS edge
  -> static docs origin/container

Visitor CN
  -> docs-cn.zhangxuemin.work
  -> hk-relay Caddy HTTPS edge
  -> reverse_proxy + cache
  -> docs.zhangxuemin.work / origin

Editor / Operator
  -> Git repo docs source
  -> CI/build or host-side build
  -> static output / image assets
```

首期不要把文档站和 `kiro.zhangxuemin.work` / `kiro-cn.zhangxuemin.work` 混在同一域名路径下。推荐使用独立域名：

- Global: `docs.zhangxuemin.work` 或 `kiro-docs.zhangxuemin.work`
- CN/HK: `docs-cn.zhangxuemin.work` 或 `kiro-docs-cn.zhangxuemin.work`

理由：文档是公开游客面，Kiro-Go 是管理/API面；域名隔离能降低 Cookie、CORS、路径穿越、缓存误配、后台暴露等风险。

## 3. 站点生成器选择

推荐：`VitePress`

原因：
- 原生 Markdown + 图片，构建产物纯静态。
- 轻量，流量和运行成本低。
- 默认适合 API / 使用文档、指南、FAQ。
- 后续可接 Algolia/Pagefind、本地搜索、版本化目录。

备选：
- `Astro Starlight`：更漂亮、内容集合能力强；略复杂。
- `Docusaurus`：生态成熟，适合大文档；首期偏重。

首期建议不要上 Next.js/SSR。静态站即可，减少攻击面和服务器资源消耗。

## 4. 部署落点

### 推荐首期部署方式

- 源站：`oracle-proxy` 上新增独立静态容器或 Caddy 静态目录。
- 源站服务只监听 `127.0.0.1:<port>`，由现有 `caddy-cpam` 或新增独立 Caddy server block 对外提供 TLS。
- Global 域名直达源站。
- CN 域名在 `hk-relay` Caddy 上反代 Global 域名，并开启缓存 / 限速。

注意：`oracle-proxy` 当前承载多个生产服务，修改要增量、低侵入。优先新增独立目录和独立 server block，不复用 Kiro-Go 容器，也不要改动 Kiro-Go 敏感配置。

### 目录建议

```text
/root/containers/kiro-docs/
  repo/                 # 文档源码仓库或工作树
  site/                 # VitePress 项目
  site/docs/            # Markdown 内容
  site/public/images/   # 图片静态资源
  dist/                 # 构建产物
  Caddyfile.snippet     # 可选：该站点的 Caddy 片段
  deploy.sh             # 构建 + 原子替换 dist
```

## 5. 安全设计

### 域名 / 面隔离

- 文档域名独立：`docs*`。
- Kiro 管理/API继续使用：`kiro.zhangxuemin.work` / `kiro-cn.zhangxuemin.work`。
- 文档站不设置能覆盖 `.zhangxuemin.work` 的宽域 Cookie。
- 文档站不反代 `/admin`、`/v1/*`、`/api/*` 到 Kiro-Go。

### 内容安全

- 文档源码不得提交：Kiro key、账号、cookie、admin token、真实上游凭据、内部随机路径。
- 示例配置使用占位符：`sk-xxxx`、`YOUR_API_KEY`、`https://kiro.example.com`。
- 图片发布前压缩并检查是否含敏感截图、token、浏览器地址栏私密路径。
- 禁止游客上传；图片只走 repo/构建产物。

### HTTP 安全头

建议文档站 Caddy/Nginx 添加：

```text
Content-Security-Policy: default-src 'self'; img-src 'self' data: https:; style-src 'self' 'unsafe-inline'; script-src 'self'; font-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=(), camera=(), payment=()
```

如果后续接发卡支付，支付页单独域名/子路径放宽 CSP，不要让文档站全局放宽。

### 访问控制与滥用防护

- 文档公开，不加登录。
- 对大文件、图片、搜索接口限速。
- 禁止目录列表。
- 禁止公开构建缓存、`.git`、`.env`、源 Markdown 以外的临时文件。
- 404/错误页不泄漏服务路径。

## 6. 流量设计

### 缓存策略

- HTML：短缓存，方便内容更新。
  - `Cache-Control: public, max-age=60, stale-while-revalidate=300`
- JS/CSS/hash assets：长缓存。
  - `Cache-Control: public, max-age=31536000, immutable`
- 图片：长缓存，文件名带 hash 或版本号。
  - `Cache-Control: public, max-age=2592000`

### 图片策略

- 图片统一放 `public/images/` 或对象存储，避免外链热链失控。
- 默认压缩为 WebP/AVIF + 保留必要 PNG。
- 单图建议控制在 300KB-800KB，教程长图拆分。
- 图片路径按主题分目录：`/images/quickstart/...`。

### HK relay 流量保护

`hk-relay` 有 800G/月双向流量限制，所以 CN 入口必须：

- 开 Caddy cache 或前置缓存层，避免每个国内请求都回源。
- 限制单 IP 请求速率。
- 不承载大文件下载、模型、安装包、视频。
- 图片强压缩；后续若图片量大，迁到对象存储/CDN，HK 只做 HTML/API 轻代理。
- 监控 `vnstat` 月流量，超过阈值告警或降级。

建议阈值：
- 600G/月：提醒
- 700G/月：降低图片缓存 miss、限制非 HTML 大请求
- 760G/月：临时将 CN 入口切回 global 或启用更严格限速

## 7. 后续发卡扩展边界

发卡不要直接塞进静态站运行时。推荐拆成三层：

```text
Docs static site
  /pricing, /buy -> 静态介绍页

Card/Order service
  card.zhangxuemin.work / api-card.zhangxuemin.work
  独立后端、数据库、支付回调、库存/卡密/订单

Kiro-Go / API service
  kiro.zhangxuemin.work
  继续作为 API / admin 面
```

首期文档站只预留导航入口：
- `购买 / 发卡（Coming soon）`
- `套餐说明`
- `使用条款`
- `安全与退款说明`

后续上线发卡时必须额外设计：支付回调验签、订单幂等、库存加密、卡密展示次数、审计日志、风控/限购、管理后台鉴权。

## 8. 文档信息架构

建议首期目录：

```text
/
  index.md                         # 产品介绍 / 快速入口
  guide/
    quickstart.md                  # 快速开始
    endpoints.md                   # 国内/海外入口说明
    api-compatible.md              # OpenAI/Anthropic 兼容格式
    clients.md                     # 常见客户端配置
    errors.md                      # 常见错误
  security/
    key-safety.md                  # Key 使用安全
    rate-limit.md                  # 频率/滥用说明
  kiro/
    what-is-kiro-proxy.md          # Kiro 反代说明，避免泄漏内部机制
    account-policy.md              # 账号与用量策略
  changelog.md
  faq.md
  buy.md                           # Coming soon
```

文档展示原则：
- 面向游客讲清楚怎么用，不讲内部账号池、管理后台路径、私密运维细节。
- API 示例只给必要格式，不给真实 token。
- 对国内/海外入口解释清楚：国内优先 `*-cn`，海外优先 global；故障时切换。

## 9. 推荐实施步骤

1. 确认域名命名：推荐 `docs.zhangxuemin.work` + `docs-cn.zhangxuemin.work`。
2. 在 Git 中创建 VitePress 文档项目，填入首批页面和图片目录。
3. 本地/源站构建 `dist/`，用静态 Caddy/Nginx 预览。
4. 在 `oracle-proxy` 新增 loopback 静态服务 + HTTPS Caddy server block。
5. 在 `hk-relay` 新增 CN Caddy reverse proxy，带缓存、限速、安全头。
6. 配 Cloudflare DNS：global 指向源站，cn 指向 HK relay；建议 DNS-only，避免额外代理变量干扰排障。
7. 验证：HTTPS、缓存头、安全头、404、图片加载、国内/海外入口、源站回退。
8. 写入运维文档和变更记录。

## 10. 首期验收标准

- `docs.*` 和 `docs-cn.*` 均可打开首页。
- Markdown 页面、侧边栏、站内搜索、图片正常。
- 无游客上传、无后台入口、无 API 反代到 Kiro-Go。
- 安全头存在，`.git` / `.env` / 源码临时文件不可访问。
- 图片和静态资源命中合理缓存头。
- HK 入口启用限速/缓存，并能看到基础流量统计。
- Kiro-Go 原有 `kiro.*` / `kiro-cn.*` 不受影响。
