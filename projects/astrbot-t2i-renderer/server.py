#!/usr/bin/env python3
from __future__ import annotations

import argparse
import asyncio
import json
import logging
import mimetypes
import os
import threading
import uuid
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote

from jinja2 import Template
from playwright.async_api import async_playwright

LOG = logging.getLogger("astrbot_t2i_renderer")


class Renderer:
    def __init__(self, storage_dir: Path):
        self.storage_dir = storage_dir
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def _resolve_chromium_executable(self) -> str | None:
        env_path = os.environ.get("PLAYWRIGHT_CHROMIUM_EXECUTABLE")
        if env_path and Path(env_path).is_file():
            return env_path

        cache_root = Path.home() / ".cache" / "ms-playwright"
        candidates = []
        for browser_dir in sorted(cache_root.glob("chromium-*"), reverse=True):
            candidates.extend(
                [
                    browser_dir / "chrome-linux" / "chrome",
                    browser_dir / "chrome-linux64" / "chrome",
                ]
            )
        for candidate in candidates:
            if candidate.is_file():
                return str(candidate)
        return None

    async def render(self, tmpl: str, tmpl_data: dict, options: dict | None = None) -> tuple[str, Path]:
        options = options or {}
        image_type = str(options.get("type") or "png").lower()
        if image_type == "jpg":
            image_type = "jpeg"
        if image_type not in {"png", "jpeg"}:
            image_type = "png"
        quality = int(options.get("quality") or 80)
        quality = max(0, min(quality, 100))
        width = int(options.get("width") or 1280)
        height = int(options.get("height") or 1600)
        full_page = bool(options.get("full_page", True))
        scale = str(options.get("scale") or "device")
        image_id = uuid.uuid4().hex
        ext = "jpg" if image_type == "jpeg" else "png"
        html_path = self.storage_dir / f"{image_id}.html"
        image_path = self.storage_dir / f"{image_id}.{ext}"

        rendered_html = Template(tmpl).render(**(tmpl_data or {}))
        html_path.write_text(rendered_html, encoding="utf-8")

        launch_args = ["--no-sandbox", "--disable-dev-shm-usage"]
        executable_path = self._resolve_chromium_executable()
        launch_kwargs = {"headless": True, "args": launch_args}
        if executable_path:
            launch_kwargs["executable_path"] = executable_path
            LOG.info("using explicit chromium executable: %s", executable_path)
        async with async_playwright() as p:
            browser = await p.chromium.launch(**launch_kwargs)
            try:
                page = await browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=2 if scale == "device" else 1)
                await page.goto(html_path.resolve().as_uri(), wait_until="networkidle")
                shot_kwargs = {
                    "path": str(image_path),
                    "type": image_type,
                    "full_page": full_page,
                }
                if image_type == "jpeg":
                    shot_kwargs["quality"] = quality
                await page.screenshot(**shot_kwargs)
            finally:
                await browser.close()

        return image_id, image_path


class Handler(BaseHTTPRequestHandler):
    server_version = "AstrBotT2IRenderer/0.1"

    def log_message(self, fmt: str, *args):
        LOG.info("%s - %s", self.address_string(), fmt % args)

    @property
    def renderer(self) -> Renderer:
        return self.server.renderer  # type: ignore[attr-defined]

    @property
    def prefix(self) -> str:
        return self.server.prefix  # type: ignore[attr-defined]

    def _send_json(self, payload: dict, status: int = 200):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_bytes(self, body: bytes, content_type: str, status: int = 200):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in {f"{self.prefix}/health", "/health"}:
            self._send_json({"ok": True, "service": "astrbot-t2i-renderer"})
            return
        if not self.path.startswith(f"{self.prefix}/"):
            self._send_json({"error": "not found"}, status=404)
            return
        image_name = unquote(self.path[len(self.prefix) + 1 :]).strip()
        if not image_name or "/" in image_name or image_name.startswith("."):
            self._send_json({"error": "bad id"}, status=400)
            return
        image_path = self.renderer.storage_dir / image_name
        if not image_path.is_file():
            self._send_json({"error": "not found"}, status=404)
            return
        content_type = mimetypes.guess_type(image_path.name)[0] or "application/octet-stream"
        self._send_bytes(image_path.read_bytes(), content_type)

    def do_POST(self):
        if self.path != f"{self.prefix}/generate":
            self._send_json({"error": "not found"}, status=404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length)
            payload = json.loads(raw.decode("utf-8")) if raw else {}
            tmpl = payload.get("tmpl") or ""
            tmpl_data = payload.get("tmpldata") or {}
            options = payload.get("options") or {}
            if not tmpl:
                self._send_json({"error": "tmpl is required"}, status=400)
                return
            image_id, image_path = asyncio.run(self.renderer.render(tmpl, tmpl_data, options))
            self._send_json(
                {
                    "success": True,
                    "data": {
                        "id": image_path.name,
                        "renderer_id": image_id,
                    },
                }
            )
        except Exception as exc:
            LOG.exception("render failed")
            self._send_json({"error": str(exc)}, status=500)


def main():
    parser = argparse.ArgumentParser(description="Minimal AstrBot-compatible HTML to image renderer")
    parser.add_argument("--bind", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=18781)
    parser.add_argument("--prefix", default="/text2img")
    parser.add_argument("--storage-dir", default=str(Path.home() / ".cache/astrbot-t2i-renderer"))
    parser.add_argument("--log-level", default="INFO")
    args = parser.parse_args()

    logging.basicConfig(
        level=getattr(logging, args.log_level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    storage_dir = Path(os.path.expanduser(args.storage_dir)).resolve()
    server = ThreadingHTTPServer((args.bind, args.port), Handler)
    server.renderer = Renderer(storage_dir)  # type: ignore[attr-defined]
    server.prefix = args.prefix.rstrip("/")  # type: ignore[attr-defined]

    LOG.info("starting renderer on %s:%s prefix=%s storage=%s", args.bind, args.port, server.prefix, storage_dir)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
