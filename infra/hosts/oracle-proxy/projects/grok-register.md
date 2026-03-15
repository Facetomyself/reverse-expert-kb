# Grok Register Stack

## 1. Summary
- Project: Grok Register Standalone / solver stack
- Host: `oracle-proxy`
- Purpose: 为 Grok 相关注册/求解链路提供独立的 Camoufox + adapter 基础设施
- Runtime status: running
- Priority: Tier 2

## 2. Access / Entry Points
- Repo path: `/root/grok-register-standalone`
- Compose file: `/root/grok-register-standalone/docker-compose.yml`
- Exposed adapter port: `15072`
- Main running containers:
  - `grok-register-camoufox`
  - `grok-register-camoufox-adapter`

## 3. Deployment Layout
- Root path: `/root/grok-register-standalone`
- Compose-managed deployment
- Details beyond port/container topology still need a dedicated audit pass

## 4. Runtime Topology
- `grok-register-camoufox`: browser runtime
- `grok-register-camoufox-adapter`: adapter exposed to host as `15072 -> 5072`
- Kept intentionally separate from Tavily solver stack

## 5. Purpose and Workflow
This stack exists to avoid cross-project interference. Tavily was explicitly isolated away from Grok's solver path, so this Grok stack should be treated as independent infrastructure.

## 6. Configuration
Known fact:
- host port `15072` belongs to Grok's adapter, not Tavily's

Unknown / to document later:
- exact env vars
- external callers
- repo-specific operational caveats

## 7. Operations

### Check status
```bash
ssh oracle-proxy
docker ps | grep grok-register
```

### Follow adapter logs
```bash
ssh oracle-proxy
docker logs -f grok-register-camoufox-adapter
```

### Follow browser runtime logs
```bash
ssh oracle-proxy
docker logs -f grok-register-camoufox
```

## 8. Health Checks
Healthy signs:
- both containers are `Up`
- `ss -ltnp | grep 15072` shows listener

## 9. Data and Persistence
Not yet documented in detail.

## 10. Common Tasks
- Verify adapter endpoint is listening on `15072`
- Ensure Tavily changes do not accidentally reuse or break this stack

## 11. Failure Modes / Troubleshooting
### Symptom: Grok solver path stops working after Tavily changes
Check whether anyone mistakenly repointed Tavily back to port `15072`.

## 12. Dependencies / Cross-links
- Related to: Grok-related tooling on this host
- Compare with: `./tavily-key-generator.md`

## 13. Change History
- 2026-03-15: documented as independent stack from Tavily solver chain
