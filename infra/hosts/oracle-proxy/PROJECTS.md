# oracle-proxy / Projects

## Project Navigation

| Project | Status | Access | Purpose | Priority | Doc |
|---|---|---|---|---|---|
| Tavily Proxy | running | `proxy.zhangxuemin.work:9874` | Tavily key pool, admin UI, unified search/extract API | Tier 1 | `./projects/tavily-proxy.md` |
| Tavily Key Generator | running | internal scheduler | 自动注册 Tavily 账号并产出 / 上传 key | Tier 1 | `./projects/tavily-key-generator.md` |
| ExaFree | running | `:7860` | Exa 注册与账号池管理服务；当前用宿主机 cron 近似每 3 小时触发 1 次 5 账号批量注册 | Tier 1 | `./projects/exafree.md` |
| Grok Register Stack | running | `:15072` adapter | 独立 Grok Turnstile solver stack | Tier 2 | `./projects/grok-register.md` |
| Grok2API | running | `:8000` | Grok API bridge/service | Tier 2 | `./projects/grok2api.md` |
| CLIProxy | running | `:8317` | OpenAI-compatible CLI proxy for local tools | Tier 2 | `./projects/cliproxy.md` |
| ExaFree | running | `:7860` | Exa 账号注册 / 刷新 / 管理面板服务 | Tier 2 | `./projects/exafree.md` |
| Network Stack | running | machine-level | nginx / sing-box / xray / cloudflared infrastructure | Infra | `./projects/network-stack.md` |
| OpenAi (migrated) | migrated-not-running | `/root/OpenAi` | 已从 OpenClaw 本机迁移过来的项目目录；当前仅存放文件，未纳入运行态 | Archive / Pending | `./projects/openai-migrated.md` |

## Relationship Snapshot

```mermaid
flowchart LR
  A[tavily-scheduler] --> B[output/api_keys.md]
  A --> C[auto-upload]
  C --> D[Tavily Proxy]
  D --> E[proxy token]
  E --> F[local search-layer]
  E --> G[external clients]
```

## Operational Notes
- Tavily chain is currently the most deeply documented and most actively maintained path on this host.
- Some machine-level services exist outside this project list (nginx, 1panel, sing-box, xray, cloudflared) and should be documented later as infrastructure services rather than app projects.
