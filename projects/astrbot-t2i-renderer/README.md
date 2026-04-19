# astrbot-t2i-renderer

Minimal AstrBot-compatible HTML-to-image renderer.

API shape:
- `POST /text2img/generate`
- `GET /text2img/<image-file>`
- `GET /text2img/health`

Purpose:
- replace broken remote `t2i.soulter.top` endpoint for AstrBot custom HTML card rendering
- support Jinja2 HTML templates + Playwright screenshot generation
