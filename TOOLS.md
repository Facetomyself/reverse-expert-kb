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

- On older CentOS/bash remote hosts such as `self-server-44005`, avoid `printf "--- label ---\n"` because the leading dashes can be interpreted as an option (`printf: --: invalid option`). Use `echo "--- label ---"` or `printf '%s\n' '--- label ---'` instead.
- For quote-heavy nested SSH checks, especially `ali-cloud -> home-macmini-via-frp`, avoid one-liners that combine regex pipes, nested quotes, and heredocs.
  - Safer pattern: stage a small local script (`cat > /tmp/check.sh` or `write`) and pipe it to the second hop, e.g. `ssh ali-cloud "ssh -F /root/.ssh/config home-macmini-via-frp bash -s" < /tmp/check.sh`.

- Current workspace shell does **not** provide an `apply_patch` binary.
  - When code-style patch edits are needed here, use the OpenClaw `edit` tool for exact replacements or `write` for whole-file generated artifacts instead of assuming `apply_patch` is installed.

## OpenClaw Model Provider / WebUI Visibility

- When adding or changing an OpenClaw model provider, do **not** stop at `models.providers.<provider>` plus raw `/v1/chat/completions` smoke tests.
- The WebUI model picker uses the configured model view. If `agents.defaults.models` exists, it is the allowlist for `/model`, `/models`, and the WebUI picker.
- Required completion checklist for provider/model changes:
  1. Add/update `models.providers.<provider>` with the endpoint, auth, adapter, and concrete `models[]` entries.
  2. Add/update `agents.defaults.models` for WebUI visibility and aliases.
  3. Use exact `provider/model` entries when only selected models should show; use `provider/*` only when dynamic discovery of every upstream model for that provider is intended.
  4. Validate with `gateway config.get` and with `openclaw models list <provider>` or another configured model-view call, not only with `curl`.
- In SecretRef objects such as `{ "source": "env", "provider": "default", "id": "CLIPROXY_API_KEY" }`, `provider` is the secret-provider alias, **not** the model provider id.
  - Do not set it to a new model provider name like `opencode` unless `secrets.providers.opencode` exists and resolves.
  - Schema validation can pass while runtime still reports `models.providers.<provider>.apiKey is unresolved in the active runtime snapshot`.
  - For the current config-local env secrets, use `provider: "default"`.
- This is a repeated user correction as of 2026-07-07; treat WebUI visibility as part of done criteria.

## OpenClaw Device Web Login / Pairing Approval

- When the user says a new Mac/browser needs "网页登录" or asks to approve a web login, treat it as **device pairing**, not node pairing.
- Do **not** rely only on the `nodes` tool or `openclaw nodes ...` for this flow. Those are node-host pairing views and may show `pending: []` / `paired: []` even when web device pairing exists.
- Correct first checks:
  - `openclaw devices list`
  - `openclaw devices approve --latest`
  - `openclaw devices approve <requestId>` when the request id is known
- Useful state files for diagnosis only:
  - `~/.openclaw/devices/pending.json`
  - `~/.openclaw/devices/paired.json`
- If `pending.json` contains an entry but `openclaw devices approve <requestId>` and `openclaw devices approve --latest` both say `unknown requestId` / no pending requests, treat the file entry as stale or out of sync with gateway runtime. Ask the user to re-trigger the browser pairing; do not hand-edit paired device auth files.

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

## ComfyUI on `home-macmini`

- ComfyUI runs as user `mengma` under `/Users/mengma/ai/ComfyUI`.
- When automating ComfyUI from the root SSH maintenance path, do **not** pre-create output subdirectories under `/Users/mengma/ai/ComfyUI/output/...` as root unless you immediately `chown -R mengma:staff`.
  - Otherwise `SaveImage` can finish sampling but fail at write time with `PermissionError: [Errno 13] Permission denied`.
  - Safer pattern: set `filename_prefix` to a new subfolder and let ComfyUI create it, or repair ownership before queueing.

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

## SSH / HK Edge Aliases

- As of 2026-04-29, local `~/.ssh/config` includes CN/HK-edge `ProxyJump hk-relay` aliases for domestic access testing and fallback:
  - `oracle-proxy-via-hk`
  - `oracle-openclaw-via-hk` / `oracle-open_claw-via-hk`
  - `oracle-gateway-via-hk`
  - `oracle-mail-via-hk`
  - `oracle-registry-via-hk`
  - `oracle-reverse-dev-via-hk`
- Use these when the domestic route to Oracle is poor. Do **not** use them for Oracle-to-Oracle machine traffic; direct/global Oracle endpoints should stay direct unless explicitly testing the HK edge path.

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
- `infra/` on this host may auto-push through repository-side hooks / automation after local commits.
  - Practical gotcha observed on 2026-04-21: an immediate manual `git push origin main` after commit returned a remote ref-lock / expected-old-SHA rejection, but `git ls-remote` showed the just-created commit was **already on remote**.
  - So for `infra/`, if a push fails right after commit, verify remote HEAD before retrying; it may already be synced.

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

## Docker Cleanup Safety

- For remote Docker cleanup, never use broad generic volume/image filters like `mongo|redis|rabbitmq` unless the user explicitly asked to remove every matching datastore on the host.
- Prefer Compose labels or exact project prefixes, for example:
  - `docker volume ls --filter label=com.docker.compose.project=<project>`
  - `grep -E '^<project>[_-]'`
- Before destructive volume deletion, print the candidate list and verify it is project-scoped. This matters on multi-app hosts such as `self-server-44005`, where unrelated projects can have redis/mongo volumes.

