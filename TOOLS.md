# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## Shell / exec on This Host

- Default `exec` shell here is `/bin/sh`, not Bash.
- Do **not** assume `set -o pipefail`, Bash arrays, or other Bash-only syntax will work directly in the raw `command` field.
- When a command needs Bash semantics or safer complex quoting, wrap it explicitly as:
  - `bash -lc '...'`
- Do **not** force `exec.host = sandbox` on this deployment unless policy has explicitly enabled that override.
  - The normal configured exec host here is the gateway.
  - For routine commands, omit `host` or use the default/`auto`; otherwise the call can fail before the command even starts with `exec host not allowed`.
- In exec-event flows, avoid broad recursive `grep` / `find` over large trees (`node_modules`, `.next`, `.git`, archived app bundles, 1Panel-managed directories) when you only need a few config hits.
- Prefer staged discovery + narrow reads:
  - first identify likely paths/files
  - then grep/read only those targets
  - cap output early with `head`, `sed -n`, or tighter `rg` patterns
- Otherwise large-output commands may get cut off by exec-event with `SIGTERM` / `SIGKILL` before the useful lines come back.
- When writing remote config files through `exec` + `ssh`, avoid fragile nested here-doc / inline-shell generation if the payload contains `$`-heavy secrets or hashes (for example Caddy bcrypt strings like `$2a$...`) or large multiline YAML.
  - On this host, `/bin/sh` interpolation plus SSH remote-shell joining can silently mangle those payloads.
  - Safer pattern: use `write` to stage a local script/file, then run it directly (`python3 /path/to/script.py`) and feed the final remote script/body via SSH stdin (`ssh host python3 -`).
  - This also avoids `exec` preflight refusing complex inline interpreter invocations.

## GitHub / gh on This Host

- Installed GitHub CLI is relatively old: `/usr/bin/gh 2.4.0+dfsg1`.
- Do **not** assume newer `gh` JSON fields exist; verify with local help/output before using examples from newer docs.
- Do **not** assume helper subcommands like `gh auth token` exist here.
- `gh auth status` being OK does **not** guarantee raw `git push` over HTTPS will work; if needed, prefer `gh`-managed flows or run `gh auth setup-git` first.

## Docker Compose Gotcha on `self-server-44005` / `host185`

- On this CentOS 7 AstrBot host, prefer the explicit binary:
  - `/usr/local/bin/docker-compose`
- Do **not** assume `docker compose ...` will behave the same in non-interactive SSH runs here.
- Observed on 2026-04-20 during remote renderer deployment:
  - `docker compose version` looked superficially available in one probe,
  - but the reliable remote build path was still `docker-compose -f ... build`
  - and `docker compose -f ...` could fail with parsing/command-shape errors in SSH execution.
- Practical rule for this host:
  - if running compose remotely through `ssh self-server-44005`, use `docker-compose` explicitly.

## Docker / Redeploy Gotcha on oracle-proxy

- For `oracle-proxy:/root/grok2api`, do **not** assume `docker compose up -d --build grok2api` can safely replace the running service.
- Current compose pins `container_name: grok2api`, and there may already be a long-lived manually recreated container using that exact name.
- Safe redeploy pattern for this project:
  1. `cd /root/grok2api`
  2. ensure deployment env pins `GROK2API_IMAGE=grok2api-official-local:latest` (for example in `.env`)
  3. `docker build -t grok2api-official-local:latest .`
  4. `docker rm -f grok2api`
  5. `docker compose up -d grok2api`
  6. verify with `docker inspect grok2api --format '{{.Config.Image}}'`
- Otherwise compose may silently recreate the service from its default remote image `ghcr.io/tqzhr/grok2api:latest`, making local code changes appear to "not take effect".
- Inspect `docker ps -a`, `docker inspect grok2api`, `.env`, and `docker compose config` first if the runtime topology seems inconsistent.

## Git / GitHub Auth on This Host

- Git itself is fine here; the fragile part was GitHub credential wiring.
- Prefer **HTTPS remotes** for GitHub on this host.
- GitHub SSH (`git@github.com:...`) is not configured by default and may fail with `Permission denied (publickey)`.
- Stable HTTPS auth helper now lives at:
  - `/root/.openclaw/workspace/scripts/git-credential-github-helper.sh`
- Global git is configured to use that helper for `https://github.com`, reading the existing token from:
  - `~/.config/gh/hosts.yml`
- If GitHub private-repo `fetch` / `push` starts failing again, first inspect:
  - `git config --global --get-regexp '^(credential|credential\..*)'`
  - and verify the helper still has execute permission.
- This host may still have **no default git author identity** configured (`user.name` / `user.email`).
  - If `git commit` fails with `Author identity unknown`, set a **repo-local** identity first for the working repo instead of assuming a global identity exists.
- Default init branch is now set globally to `main`.

## Search / Fetch Reality on This Host

- Raw Brave-backed `web_search` is not currently configured in this environment; do not assume it is available.
- For general research, prefer the `search-layer` skill and default to Grok-only unless the human explicitly asks for other sources.
- Local `search-layer` Exa source is currently wired via `~/.openclaw/credentials/search.json` to:
  - `exa.apiUrl = http://158.178.236.241:7860`
  - `exa.apiKey = <configured>`
- `proxy.zhangxuemin.work` currently resolves to the same public host (`158.178.236.241`), so `http://proxy.zhangxuemin.work:7860` and `http://158.178.236.241:7860` are effectively the same Exa-facing service endpoint from an operator point of view.
- Local `search-layer` currently also points Tavily and Grok to:
  - `tavily.apiUrl = http://proxy.zhangxuemin.work:9874/api`
  - `grok.apiUrl = http://proxy.zhangxuemin.work:8000/v1`
- As of 2026-03-17 smoke testing:
  - Exa works
  - Grok works
  - Tavily returns `401 Unauthorized`
- `skills/search-layer/scripts/search.py` supports both:
  - official Exa direct key string
  - Exa/object config (`apiUrl + apiKey`) using `/search` with Bearer auth
- `web_fetch` is fragile on some source types here:
  - direct PDF fetches may return raw `%PDF` bytes instead of readable extraction
  - academic / anti-bot / Cloudflare-protected pages may return interstitials or 403s
  - some Chinese content platforms (for example Zhihu/CSDN) may fail or degrade
- When readable extraction matters, prefer HTML landing pages, abstracts, GitHub pages, and open-source documentation before direct PDF/article fetches.

## OpenClaw Local Memory Embeddings on This Host

- As of 2026-04-18, local memory embeddings are workable here via:
  - global package: `node-llama-cpp`
  - default local model: `hf:ggml-org/embeddinggemma-300m-qat-q8_0-GGUF/embeddinggemma-300m-qat-Q8_0.gguf`
  - cache dir: `/root/.cache/node-llama-cpp`
- Practical setup shape that worked:
  - install `cmake`
  - install global npm package `node-llama-cpp`
  - set `agents.defaults.memorySearch.provider = "local"`
- Validation commands:
  - `openclaw memory status --deep --agent main`
  - `openclaw memory status --deep --agent reverse`
- Known gotcha:
  - `openclaw doctor --non-interactive` may still warn that local embeddings are "not ready" because the **gateway doctor probe** can time out, even when `openclaw memory status --deep` shows `Embeddings: ready` and `openclaw gateway call doctor.memory.status --json --timeout 60000` returns `embedding.ok = true`.
  - Treat that specific combination as a **probe-timeout inconsistency**, not immediate proof that local memory embeddings are broken.

Add whatever helps you do your job. This is your cheat sheet.
