# MEMORY.md

- 2026-03-07: For openclaw-search-skills on this host, only use the user-provided API tokens from ~/.openclaw/credentials/search.json. When a search source is not explicitly specified, default to using Grok only (exa/tavily disabled unless the user asks).

- 2026-03-12: Headless cloud server (no GUI). Tooling/runtime baselines:
  - OS: Ubuntu 22.04.5 LTS (arm64/aarch64)
  - OpenClaw: /usr/bin/openclaw — OpenClaw 2026.3.8 (3caab92)
  - Node.js: /usr/bin/node v22.22.0 (npm/npx 10.9.4)
  - Python: /usr/bin/python3 3.10.12; pip at /root/.local/bin/pip (pip 26.0.1)
  - uv: /root/.local/bin/uv 0.10.7
  - summarize CLI: /usr/bin/summarize 0.12.0
  - GitHub CLI: /usr/bin/gh 2.4.0+dfsg1
  - TLS/CA note: Node HTTPS may fail with "unable to get local issuer certificate" unless NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt is set (system bundle at /etc/ssl/certs/ca-certificates.crt).
