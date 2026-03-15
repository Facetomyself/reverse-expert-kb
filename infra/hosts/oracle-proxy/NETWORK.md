# oracle-proxy / Network

## 1. Addressing
- Public IP: `158.178.236.241`
- Primary documented domain: `proxy.zhangxuemin.work`
- Observed local/private addresses at snapshot:
  - `10.0.0.68`
  - multiple docker bridge ranges (`172.x.x.x`)

## 2. Open / Listening Ports (observed)

| Port | Bind | Component | Exposure guess | Notes |
|---|---:|---|---|---|
| 22 | 0.0.0.0 | sshd | public | SSH access |
| 80 | 0.0.0.0 | 1panel | public/internal-mgmt | Needs policy confirmation |
| 8000 | 0.0.0.0 | grok2api | public/direct | Grok API bridge |
| 8317 | 0.0.0.0 | cliproxy | public/direct | OpenAI-compatible CLI proxy |
| 9874 | 0.0.0.0 | Tavily proxy | public/direct | Web console + `/api/*` |
| 15072 | 0.0.0.0 | grok-register adapter | public/direct | Grok solver adapter |
| 16072 | 0.0.0.0 | Tavily adapter | public/direct | Tavily solver adapter |
| 30011 | 0.0.0.0 | nginx | public | exact purpose TBD |
| 30001 / 30004-30010 | * | sing-box | mixed | proxy/tunnel related, TBD |
| 14391 | * | xray | mixed | TBD |
| 20241 | 127.0.0.1 | cloudflared | local-only | tunnel local listener |

## 3. Domain Resolution
- `proxy.zhangxuemin.work` → `158.178.236.241`

## 4. Tavily-related entry points
- Web console: `http://proxy.zhangxuemin.work:9874/`
- API base: `http://proxy.zhangxuemin.work:9874/api`
- Internal proxy target used by scheduler container: `http://host.docker.internal:9874`

## 5. Notes / Caveats
- This host does **not** currently have `ufw` installed (`ufw: command not found` at snapshot time).
- Several ports are directly bound on `0.0.0.0`; future hardening review is recommended.
- Network documentation is only partially complete; nginx / cloudflared / sing-box / xray mappings still need a dedicated pass.
