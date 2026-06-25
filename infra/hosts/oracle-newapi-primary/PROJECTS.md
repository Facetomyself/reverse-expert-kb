# oracle-newapi-primary / PROJECTS

## Summary
`oracle-newapi-primary` is the primary New API / AI API relay host.

Former identity: `oracle-registry`.

## Active project: New API primary
- Runtime directory: `/opt/new-api`
- Compose file: `/opt/new-api/docker-compose.yml`
- Compose project: `newapi`
- Container: `new-api`
- Image: `calciumion/new-api:latest`
- Restart policy: `unless-stopped`
- Data: `/opt/new-api/data`
- Backups: `/opt/new-api/backups`
- App listener: `127.0.0.1:13000 -> 3000/tcp` inside container
- Public front door: Caddy `:80` -> `127.0.0.1:13000`
- Role marker header: `X-NewAPI-Role: primary`
- Planned DNS: `newapi.zhangxuemin.work`
- Temporary/direct access before DNS/TLS finalization: `http://140.245.33.114/`

## Operational commands
```bash
ssh oracle-newapi-primary
cd /opt/new-api
docker compose -p newapi ps
docker compose -p newapi logs --tail=100
curl -I http://127.0.0.1:13000/
curl -I http://127.0.0.1/
```

## Retired project groups
The former registry-proxy and NexusVault monitor workloads were retired on 2026-06-08 before this host was re-positioned as New API primary. See `CHANGELOG.md` for details.


## Upstream channels provisioned in New API
Provisioned directly in the New API SQLite database on 2026-06-08; no UI-only setup is required for these baseline channels.

- `oracle-proxy-cliproxy-cpa`
  - Type: OpenAI-compatible channel
  - Base URL: `http://proxy.zhangxuemin.work:8317`
  - Source service: `oracle-proxy` CLIProxy / CPA-managed pool
  - Tag: `oracle-proxy/cpa`
  - Priority: `20`
  - Representative smoke model: `gpt-5.5`

- `oracle-proxy-kiro-go`
  - Type: OpenAI-compatible channel
  - Base URL: `https://kiro.zhangxuemin.work`
  - Source service: `oracle-proxy` Kiro-Go
  - Tag: `oracle-proxy/kiro-go`
  - Priority: `10`
  - Representative smoke model: `auto`

Other New API state:
- `SelfUseModeEnabled=true`, so the self-use relay can work before formal per-model pricing is configured.
- Downstream New API token for local/operator smoke tests is stored only on-host at `/opt/new-api/newapi-access-token.txt` (`0600`); do not copy the token into docs/chat.
- Pre-provision DB backup was written under `/opt/new-api/backups/one-api.before-channel-provision-*.db`.

Verification on 2026-06-08:
```text
POST /v1/chat/completions model=gpt-5.5 -> OK via CPA/CLIProxy
POST /v1/chat/completions model=auto    -> OK via Kiro-Go
```



## Semantic family routing layout

Updated on 2026-06-08 after user correction: New API channels should be semantic family groups, not raw upstream buckets. The public relay model surface intentionally excludes internal/aggregate models and duplicate aliases.

Current baseline channels:

- `gpt`
  - New API channel type: `1` / OpenAI-compatible
  - Upstream: CPA / CLIProxy at `http://proxy.zhangxuemin.work:8317`
  - Scope: GPT/OpenAI-family public relay models only
  - Models: `gpt-5.5`, `gpt-image-2`, `gpt-5.4-mini`, `gpt-5.4`
  - Excluded: `codex-auto-review` because it is for automatic review/internal workflow, not general relay exposure

- `claude`
  - New API channel type: `14` / Anthropic
  - Upstream: Kiro-Go at `https://kiro.zhangxuemin.work`
  - Scope: Claude/Anthropic-family models
  - Models: `claude-opus-*`, `claude-sonnet-*`, `claude-haiku-*` variants currently exposed by Kiro-Go

- `deepseek`
  - New API channel type: `1` / OpenAI-compatible
  - Upstream: Kiro-Go at `https://kiro.zhangxuemin.work`
  - Models: `deepseek-3.2`, `deepseek-3.2-thinking`

- `minimax`
  - New API channel type: `1` / OpenAI-compatible
  - Upstream: Kiro-Go at `https://kiro.zhangxuemin.work`
  - Models: `minimax-m2.5`, `minimax-m2.5-thinking`, `minimax-m2.1`, `minimax-m2.1-thinking`

- `glm`
  - New API channel type: `1` / OpenAI-compatible
  - Upstream: Kiro-Go at `https://kiro.zhangxuemin.work`
  - Models: `glm-5`, `glm-5-thinking`

- `qwen`
  - New API channel type: `1` / OpenAI-compatible
  - Upstream: Kiro-Go at `https://kiro.zhangxuemin.work`
  - Models: `qwen3-coder-next`, `qwen3-coder-next-thinking`

Intentional exclusions:
- `auto` / `auto-thinking` are aggregate router names and are not exposed in New API.
- Uppercase duplicate GPT aliases (`GPT-5.5`, `GPT-5.4`, `GPT-5.4 Mini`) are not exposed; canonical lower-case names are used.
- Kiro-Go `gpt-4` / `gpt-4o` are not exposed, because GPT/OpenAI-family traffic should come from CPA/CLIProxy.
- Stale model rows for excluded names were purged from the New API `models` table, not merely disabled.

Verification on 2026-06-08:
```text
gpt-5.5            -> gpt      -> OK
claude-sonnet-4.6  -> claude   -> OK
deepseek-3.2       -> deepseek -> OK
minimax-m2.5       -> minimax  -> OK
glm-5              -> glm      -> OK
qwen3-coder-next   -> qwen     -> OK
auto               -> model_not_found (expected)
claude via /v1/messages -> OK through Anthropic channel type 14
```

Protocol note:
- Kiro-Go exposes both OpenAI-compatible `/v1/chat/completions` and Anthropic-native `/v1/messages`. New API therefore uses Anthropic channel type `14` for the `claude` family, while non-Claude Kiro-Go families remain OpenAI-compatible type `1`.


## Static documentation site

A custom static documentation site was deployed on 2026-06-08 under `/opt/new-api-docs` and served by Caddy at `/docs/` on both primary and standby New API hosts. It intentionally references the external PackyAPI quick-start page only as an information-architecture reference; copy, endpoint values, model groups, protocol notes, and CLI examples are adapted to this private New API relay deployment.

Routing shape:
- `/docs` -> `308` redirect to `/docs/`
- `/docs/*` -> Caddy static file server rooted at `/opt/new-api-docs`
- all other paths -> New API app at `127.0.0.1:13000`

Content coverage:
- quick start
- endpoint selection for primary/standby
- account and token creation guidance
- semantic model families: `gpt`, `claude`, `deepseek`, `minimax`, `glm`, `qwen`
- OpenAI-compatible examples using `/v1/chat/completions`
- Anthropic-native examples using `/v1/messages`
- CLI base URL notes and common FAQ

Current access:
- primary: `http://140.245.33.114/docs/`
- standby: `http://140.245.61.236/docs/`

Verification on 2026-06-08:
```text
GET /docs      -> 308 /docs/
GET /docs/     -> 200 text/html
GET /docs/style.css -> 200 text/css
GET /          -> 200 New API console, still reverse-proxied
```
