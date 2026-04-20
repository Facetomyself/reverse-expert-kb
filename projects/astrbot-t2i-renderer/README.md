# astrbot-t2i-renderer

Minimal AstrBot-compatible HTML-to-image renderer.

API shape:
- `POST /text2img/generate`
- `GET /text2img/<image-file>`
- `GET /text2img/health`

Purpose:
- replace broken remote `t2i.soulter.top` endpoint for AstrBot custom HTML card rendering
- support Jinja2 HTML templates + Playwright screenshot generation

## Local development shape

Current OpenClaw host can still run the renderer directly with:

```bash
python3 server.py --bind 127.0.0.1 --port 18781
```

## host185 / AstrBot-machine deployment

Preferred production shape for the AstrBot stack is now **local-to-host185**, not OpenClaw-host + tunnel:

- deploy under `/opt/astrbot-t2i-renderer`
- build with `docker-compose.host185.yml`
- attach to Docker network `1panel-network`
- publish host `18783 -> container 18781`
- mount host fonts read-only into the container so Chromium can render Chinese text correctly

Bring-up:

```bash
cd /opt/astrbot-t2i-renderer
docker compose -f docker-compose.host185.yml build
docker compose -f docker-compose.host185.yml up -d
curl http://127.0.0.1:18783/text2img/health
```

Recommended AstrBot endpoint on `host185`:

- `http://10.10.21.185:18783/text2img`
