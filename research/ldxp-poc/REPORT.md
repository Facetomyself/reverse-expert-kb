# 链动小铺 pay.ldxp.cn 多来源搜索 PoC

时间：2026-06-09 19:43 Asia/Shanghai

## 目标

验证仅使用多来源搜索，能否完成 `site:pay.ldxp.cn` 下链动小铺店铺/商品入口的初级筛选。

## 搜索配置

- 来源：Exa + Tavily + Grok（Grok 本次请求返回 502，未形成有效结果）
- 查询组：`site:pay.ldxp.cn/shop`、`site:pay.ldxp.cn/item`、`链动小铺`、`自动发卡`、`商品 价格`、`店铺 公告` 等组合
- 输出文件：
  - `search_raw.json`
  - `search_exa_expand.json`
  - `search_tavily_check.json`
  - `candidates_merged.csv`
  - `candidates_merged.json`
  - `summary.json`

## 结果摘要

- 原始命中批次：{'research/ldxp-poc/search_raw.json': 16, 'research/ldxp-poc/search_exa_expand.json': 26, 'research/ldxp-poc/search_tavily_check.json': 8}
- 去重后唯一入口：32
- 店铺入口：21
- 商品入口：11
- Exa 与 Tavily 同时命中的入口：8

## 店铺入口样本

| 类型 | ID | 标题/可推断名称 | 来源 | URL |
|---|---|---|---|---|
| shop | `2XLR97IG` | https://pay.ldxp.cn/shop/2XLR97IG | exa | https://pay.ldxp.cn/shop/2XLR97IG |
| shop | `52ai` | https://pay.ldxp.cn/shop/52ai | exa | https://pay.ldxp.cn/shop/52ai |
| shop | `96H3487D` | 晓晓游戏屋- 链动小铺 | exa, tavily | https://pay.ldxp.cn/shop/96H3487D |
| shop | `9WQWAIMD` | 9wqwaimd | exa | https://pay.ldxp.cn/shop/9WQWAIMD |
| shop | `F6R79HVA` | F6r79hva | exa | https://pay.ldxp.cn/shop/F6R79HVA |
| shop | `HF7SHNTA` | wobuhuijianji - 链动小铺 | exa, tavily | https://pay.ldxp.cn/shop/HF7SHNTA |
| shop | `HNGFW0MA` | Hngfw0ma | exa | https://pay.ldxp.cn/shop/HNGFW0MA |
| shop | `ice` | Ice | exa | https://pay.ldxp.cn/shop/ice |
| shop | `JVDCG8IG` | Jvdcg8ig | exa | https://pay.ldxp.cn/shop/JVDCG8IG |
| shop | `KD7HE66S` | Kd7he66s | exa | https://pay.ldxp.cn/shop/KD7HE66S |
| shop | `LOA3IZW5` | Loa3izw5 | exa | https://pay.ldxp.cn/shop/LOA3IZW5 |
| shop | `lucifer` | 冒险岛宇宙- 链动小铺 | exa, tavily | https://pay.ldxp.cn/shop/lucifer |
| shop | `Lucoo` | 店铺地址 - 自动发卡网 | exa | https://pay.ldxp.cn/shop/Lucoo |
| shop | `LVVK5RTY` | Lvvk5rty | exa | https://pay.ldxp.cn/shop/LVVK5RTY |
| shop | `MAMY9DA8` | https://pay.ldxp.cn/shop/MAMY9DA8/wxct14 | exa | https://pay.ldxp.cn/shop/MAMY9DA8/wxct14 |

## 商品入口样本

| 类型 | ID | 标题/可推断名称 | 来源 | URL |
|---|---|---|---|---|
| item | `42fli5` | 11780 - 链动小铺 | exa, tavily | https://pay.ldxp.cn/item/42fli5 |
| item | `9axixc` | https://pay.ldxp.cn/item/9axixc | exa | https://pay.ldxp.cn/item/9axixc |
| item | `9t0s0y` | Untitled | exa | https://pay.ldxp.cn/item/9t0s0y |
| item | `hdb12m` | Qt 5.15.17 linux binary package - ubuntu22.04.5 - 链动小铺 | exa, tavily | https://pay.ldxp.cn/item/hdb12m |
| item | `k41h4o` | https://pay.ldxp.cn/item/k41h4o | exa | https://pay.ldxp.cn/item/k41h4o |
| item | `owiwr6` | 库存63 - 自动发卡网 | exa | https://pay.ldxp.cn/item/owiwr6 |
| item | `r6j5pd` | Untitled | exa, tavily | https://pay.ldxp.cn/item/r6j5pd |
| item | `vsnb8d` | 可灵钻石会员一个月- 链动小铺 | exa | https://pay.ldxp.cn/item/vsnb8d |
| item | `wezle9` | 打开商品 - 自动发卡网 | exa | https://pay.ldxp.cn/item/wezle9 |
| item | `wv08td` | 下雪的史努比- 链动小铺 | exa, tavily | https://pay.ldxp.cn/item/wv08td |
| item | `x3bps3` | 鬼灭之刃蛇恋CP - 链动小铺 | tavily | https://pay.ldxp.cn/item/x3bps3 |

## 字段可得性判断

| 字段 | 仅靠搜索结果 | 说明 |
|---|---|---|
| 店铺 URL | 可用 | `shop/<slug>` 召回效果可接受 |
| 商品 URL | 可用 | `item/<id>` 可召回，但覆盖有限 |
| 店名 | 部分可用 | title 中有时包含“店名 - 链动小铺”，有时只有 slug |
| 公告 | 不可稳定获取 | 搜索 snippet 未稳定包含公告 |
| 商品名 | 部分可用 | title 中可见一部分商品名 |
| 商品介绍 | 不可稳定获取 | snippet 多为平台通用介绍 |
| 价格 | 不可稳定获取 | 本批搜索结果未稳定出现价格字段 |

## 页面访问观察

- 直接请求 `https://pay.ldxp.cn/shop/lucifer` 返回长度约 4321 的 JS 防护 HTML。
- `robots.txt` / `sitemap.xml` 也返回同类 JS 防护页，不能作为索引源。
- OpenClaw 内置浏览器本次调用超时，未重启网关；因此本 PoC 只验证搜索发现阶段，不宣称完成页面字段抽取。

## 结论

多来源搜索可以完成“小规模候选入口发现”的初级筛选：本次获得 32 个唯一入口，其中 21 个店铺、11 个商品。但它不能单独满足“店名 + 公告 + 商品名 + 商品介绍 + 价格”的完整采集目标。

推荐下一阶段：基于 `candidates_merged.csv` 做浏览器渲染抽取 PoC，先抽 3 个店铺 + 3 个商品，确认是否能稳定穿过 JS 防护并提取字段。若可行，再扩展搜索 API 与爬取队列。
