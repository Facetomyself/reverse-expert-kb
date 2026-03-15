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
Currently only container/runtime facts are documented.
Underlying compose/unit file is not yet captured in this first pass.

## 4. Runtime Topology
- Host exposure: `0.0.0.0:8317 -> 8317/tcp`
- Container env observed:
  - `TZ=Asia/Shanghai`
- Consumers: local tooling such as summarize / OpenAI-compatible CLI clients on this host

## 5. Purpose and Workflow
Acts as a stable compatibility layer so local tools can talk to one endpoint while upstream model/provider details stay abstracted.

## 6. Configuration
Known:
- container env currently observed is minimal

Unknown / TBD:
- exact compose or systemd source
- upstream routing rules
- config file location

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
