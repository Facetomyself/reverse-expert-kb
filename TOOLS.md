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

## Search / Fetch Reality on This Host

- Raw Brave-backed `web_search` is not currently configured in this environment; do not assume it is available.
- For general research, prefer the `search-layer` skill and default to Grok-only unless the human explicitly asks for other sources.
- `web_fetch` is fragile on some source types here:
  - direct PDF fetches may return raw `%PDF` bytes instead of readable extraction
  - academic / anti-bot / Cloudflare-protected pages may return interstitials or 403s
  - some Chinese content platforms (for example Zhihu/CSDN) may fail or degrade
- When readable extraction matters, prefer HTML landing pages, abstracts, GitHub pages, and open-source documentation before direct PDF/article fetches.

Add whatever helps you do your job. This is your cheat sheet.
