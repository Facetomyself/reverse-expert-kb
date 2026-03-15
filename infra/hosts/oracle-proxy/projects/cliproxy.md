# CLIProxy

## 1. Summary
- Project: cliproxy / CLI proxy API
- Host: `oracle-proxy`
- Purpose: 为本地 CLI 工具提供 OpenAI-compatible proxy endpoint
- Runtime status: running
- Priority: Tier 2

## 2. Access / Entry Points
- Container name: `cliproxy`
- Image: `eceasy/cli-proxy-api:latest`
- Exposed port: `8317`
- Observed endpoint family used elsewhere: `http://proxy.zhangxuemin.work:8317/v1`

## 3. Deployment Layout
Observed deployment source:
- Host path: `/root/containers/cliproxy`
- Mounted config: `/root/containers/cliproxy/config.yaml` -> `/CLIProxyAPI/config.yaml`
- Mounted auth dir: `/root/containers/cliproxy/auth-dir` -> `/root/.cli-proxy-api`
- Helper/update script observed: `/root/update_cliproxy.sh`

## 4. Runtime Topology
- Host exposure: `0.0.0.0:8317 -> 8317/tcp`
- Container image: `eceasy/cli-proxy-api:latest`
- Container command: `./CLIProxyAPI`
- Container env observed:
  - `TZ=Asia/Shanghai`
- Auth backend style: local file-based auth material under mounted auth directory
- Consumers: local tooling such as summarize / OpenAI-compatible CLI clients on this host

## 5. Purpose and Workflow
Acts as a stable compatibility layer so local tools can talk to one endpoint while upstream model/provider details stay abstracted.
Likely use case on this host: local CLI tools target `http://proxy.zhangxuemin.work:8317/v1` instead of talking to upstream model services directly.

Observed behavior from logs:
- serves OpenAI-compatible `POST /v1/chat/completions`
- requests are actively using OAuth-backed auth files
- model examples seen in logs include `gpt-5.4`
- auth refresh / onboarding logic exists for at least `codex` and `antigravity` providers

## 6. Configuration
Known:
- main config file on host: `/root/containers/cliproxy/config.yaml`
- auth material directory on host: `/root/containers/cliproxy/auth-dir`
- update helper script exists: `/root/update_cliproxy.sh`

Known config shape from update script template:
- `address`
- `port`
- `auth-dir`
- `api-keys`
- `debug`
- `usage-statistics-enabled`

Operational rule:
- `auth-dir` contains highly sensitive OAuth/session material. Document its location, but do **not** copy file contents into notes or chat.

Unknown / TBD:
- full upstream routing policy inside `config.yaml`
- exact meaning of all provider-specific auth files

## 7. Operations

### Check status
```bash
ssh oracle-proxy
docker ps | grep cliproxy
ss -ltnp | grep 8317
```

### Logs
```bash
ssh oracle-proxy
docker logs -f cliproxy
```

## 8. Health Checks
Healthy signs:
- container `cliproxy` is `Up`
- port `8317` listening
- dependent local tools can complete requests through `/v1`

## 9. Data and Persistence
Not yet documented.

## 10. Common Tasks
- verify listener on `8317`
- inspect container logs when local tools start failing

## 11. Failure Modes / Troubleshooting
### Symptom: local OpenAI-compatible CLI clients stop working
Check:
- whether `cliproxy` is up
- whether port `8317` is listening
- whether upstream endpoint credentials changed

## 12. Dependencies / Cross-links
- Related to local tooling that uses `http://proxy.zhangxuemin.work:8317/v1`
- Related host docs: `../HOST.md`, `../NETWORK.md`

## 13. Change History
- 2026-03-15: documented first-pass container and access information
ss container and access information
