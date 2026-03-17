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

## GitHub / gh on This Host

- Installed GitHub CLI is relatively old: `/usr/bin/gh 2.4.0+dfsg1`.
- Do **not** assume newer `gh` JSON fields exist; verify with local help/output before using examples from newer docs.
- Do **not** assume helper subcommands like `gh auth token` exist here.
- `gh auth status` being OK does **not** guarantee raw `git push` over HTTPS will work; if needed, prefer `gh`-managed flows or run `gh auth setup-git` first.

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

Add whatever helps you do your job. This is your cheat sheet.
