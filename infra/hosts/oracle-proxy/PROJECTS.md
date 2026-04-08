# oracle-proxy / Projects

## Project Navigation

| Project | Status | Access | Purpose | Priority | Doc |
|---|---|---|---|---|---|
| Tavily Proxy | running | `proxy.zhangxuemin.work:9874` | Tavily key pool, admin UI, unified search/extract API | Tier 1 | `./projects/tavily-proxy.md` |
| ExaFree | running | `:7860` | Exa 账号注册 / 刷新 / 管理面板服务，并为本机 search-layer 提供 Exa 代理号池入口 | Tier 1 | `./projects/exafree.md` |
| Grok Register Stack | running | `:15072` adapter | 独立 Grok Turnstile solver stack | Tier 2 | `./projects/grok-register.md` |
| Grok2API | running | `:8000` | Grok API bridge/service | Tier 2 | `./projects/grok2api.md` |
| CLIProxy | running | `:8317` | OpenAI-compatible CLI proxy for local tools | Tier 2 | `./projects/cliproxy.md` |
| Network Stack | running | machine-level | nginx / sing-box / xray / cloudflared infrastructure | Infra | `./projects/network-stack.md` |
| OpenAi (migrated) | migrated-not-running | `/root/OpenAi` | 已从 OpenClaw 本机迁移过来的项目目录；当前仅存放文件，未纳入运行态 | Archive / Pending | `./projects/openai-migrated.md` |

## Relationship Snapshot

```mermaid
flowchart LR
  D[Tavily Proxy] --> E[proxy token]
  E --> F[local search-layer]
  E --> G[external clients]

  H[ExaFree on :7860] --> I[ExaFree user API key]
  I --> J[local search-layer Exa source]
```

## Operational Notes
- `proxy-tavily-proxy-1` remains active production surface for the Tavily proxy service.
- ExaFree is both a standalone service and a downstream dependency of the local `search-layer` skill.
- Some machine-level services exist outside this project list (nginx, 1panel, sing-box, xray, cloudflared) and should be documented later as infrastructure services rather than app projects.
