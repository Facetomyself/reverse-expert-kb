#!/usr/bin/env python3
"""Archive Suzhou travel notes as Markdown with local images."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

UA_MOBILE = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
)

OUT = Path("_tmp/suzhou-travel-blogs")

URLS = [
    "https://travel.qunar.com/youji/7887326",
    "https://travel.qunar.com/youji/7496057",
    "https://travel.qunar.com/youji/6497858",
    "https://travel.qunar.com/youji/3769363",
    "https://travel.qunar.com/youji/7680464",
    "https://travel.qunar.com/youji/6859082",
    "https://travel.qunar.com/youji/5381297",
    "https://travel.qunar.com/youji/7754966",
    "https://travel.qunar.com/youji/7395492",
    "https://travel.qunar.com/youji/5802828",
    "https://travel.qunar.com/youji/7532293",
    "https://travel.qunar.com/youji/7889501",
]


@dataclass
class Article:
    title: str
    source_url: str
    final_url: str
    slug: str
    text_lines: list[str]
    image_paths: list[str]


def slugify(value: str, fallback: str) -> str:
    value = re.sub(r"[\\/:*?\"<>|\s]+", "-", value.strip())
    value = re.sub(r"-+", "-", value).strip("-")
    value = value[:72].strip("-")
    return value or fallback


def normalize_url(url: str) -> str:
    m = re.search(r"/(?:youji|note)/(\d+)", url)
    if m:
        return f"https://travel.qunar.com/travelbook/note/{m.group(1)}"
    return url


def clean_line(line: str) -> str:
    line = re.sub(r"[\ue000-\uf8ff]", "", line)
    line = re.sub(r"\s+", " ", line).strip()
    return line


def useful_text(lines: Iterable[str]) -> list[str]:
    cleaned: list[str] = []
    skip_exact = {
        "首页",
        "游记详情",
        "马上下载",
        "分享到",
        "QQ空间",
        "新浪微博",
        "取 消",
        "暂无评论",
        "写评论...",
        "查看更多",
    }
    stop_prefixes = ("评论（", "相关游记")
    for raw in lines:
        line = clean_line(raw)
        if not line or line in skip_exact:
            continue
        if any(line.startswith(prefix) for prefix in stop_prefixes):
            break
        if len(line) == 1 and not re.search(r"[\u4e00-\u9fffA-Za-z0-9]", line):
            continue
        cleaned.append(line)

    for marker in ("前言", "说说这次旅行", "第1天"):
        if marker in cleaned:
            idx = max(0, cleaned.index(marker) - 6)
            cleaned = cleaned[idx:]
            break
    return cleaned


def choose_image_url(img, base_url: str) -> str | None:
    for attr in ("data-src", "data-original", "data-lazy", "src"):
        value = img.get(attr)
        if not value:
            continue
        value = value.strip()
        if not value or "space_3nd" in value or "share_" in value:
            continue
        absolute = urljoin(base_url, value)
        parsed = urlparse(absolute)
        host_path = parsed.netloc + parsed.path
        if any(token in host_path for token in ("headshot", "avatar", "site/images/travel/touch")):
            continue
        if any(token in host_path for token in ("tr-osd", "mapi-img", "space-img", "travel")):
            return absolute
    return None


def ext_for(resp: requests.Response, url: str) -> str:
    ctype = resp.headers.get("content-type", "").lower()
    if "png" in ctype:
        return ".png"
    if "webp" in ctype:
        return ".webp"
    if "gif" in ctype:
        return ".gif"
    suffix = Path(urlparse(url).path).suffix.lower()
    if suffix in {".jpg", ".jpeg", ".png", ".webp", ".gif"}:
        return suffix
    return ".jpg"


def download_image(session: requests.Session, url: str, out_dir: Path, idx: int, referer: str) -> str | None:
    try:
        resp = session.get(url, headers={"Referer": referer}, timeout=(5, 10))
        resp.raise_for_status()
    except Exception as exc:  # noqa: BLE001
        print(f"image failed: {url} ({exc})", file=sys.stderr)
        return None
    if len(resp.content) < 2048:
        return None
    digest = hashlib.sha1(url.encode()).hexdigest()[:8]
    name = f"img_{idx:02d}_{digest}{ext_for(resp, url)}"
    path = out_dir / name
    path.write_bytes(resp.content)
    return name


def archive_one(session: requests.Session, source_url: str, number: int) -> Article | None:
    url = normalize_url(source_url)
    try:
        resp = session.get(url, timeout=(5, 15))
        resp.raise_for_status()
    except Exception as exc:  # noqa: BLE001
        print(f"page failed: {source_url} ({exc})", file=sys.stderr)
        return None

    soup = BeautifulSoup(resp.text, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()

    title = soup.title.get_text(" ", strip=True) if soup.title else f"苏州游记 {number}"
    title = re.sub(r"-【去哪儿攻略】$", "", title).strip()
    slug = f"{number:02d}-{slugify(title, str(number))}"
    article_dir = OUT / slug
    image_dir = article_dir / "images"
    image_dir.mkdir(parents=True, exist_ok=True)

    lines = useful_text(soup.stripped_strings)
    seen: set[str] = set()
    image_urls: list[str] = []
    for img in soup.find_all("img"):
        img_url = choose_image_url(img, resp.url)
        if img_url and img_url not in seen:
            seen.add(img_url)
            image_urls.append(img_url)

    image_paths: list[str] = []
    for idx, image_url in enumerate(image_urls[:12], start=1):
        local = download_image(session, image_url, image_dir, idx, resp.url)
        if local:
            image_paths.append(f"images/{local}")

    if len("".join(lines)) < 180 or not image_paths:
        print(f"skip low-content: {source_url} text={len(''.join(lines))} images={len(image_paths)}", file=sys.stderr)
        shutil.rmtree(article_dir, ignore_errors=True)
        return None

    md: list[str] = [f"# {title}", "", f"来源：{source_url}", f"抓取地址：{resp.url}", ""]
    paragraph: list[str] = []
    heading_re = re.compile(r"^(第\d+天|前言|说说这次旅行|THE END)$")
    for line in lines:
        if heading_re.match(line):
            if paragraph:
                md.append(" ".join(paragraph))
                md.append("")
                paragraph = []
            md.extend([f"## {line}", ""])
        elif len(line) <= 12 and re.search(r"[\u4e00-\u9fff]", line) and line.endswith(("街", "园", "寺", "馆", "店", "路")):
            if paragraph:
                md.append(" ".join(paragraph))
                md.append("")
                paragraph = []
            md.extend([f"### {line}", ""])
        else:
            paragraph.append(line)
            if len("".join(paragraph)) > 180:
                md.append(" ".join(paragraph))
                md.append("")
                paragraph = []
    if paragraph:
        md.append(" ".join(paragraph))
        md.append("")

    md.extend(["## 图片", ""])
    for idx, image_path in enumerate(image_paths, start=1):
        md.append(f"![{title} 图 {idx}]({image_path})")
        md.append("")
    (article_dir / "article.md").write_text("\n".join(md), encoding="utf-8")
    return Article(title, source_url, resp.url, slug, lines, image_paths)


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    session = requests.Session()
    session.headers.update({"User-Agent": UA_MOBILE, "Accept-Language": "zh-CN,zh;q=0.9"})

    articles: list[Article] = []
    for idx, url in enumerate(URLS, start=1):
        article = archive_one(session, url, idx)
        if article:
            articles.append(article)
        if len(articles) >= 10:
            break

    manifest = [
        {
            "title": item.title,
            "source_url": item.source_url,
            "final_url": item.final_url,
            "folder": item.slug,
            "text_chars": len("".join(item.text_lines)),
            "images": len(item.image_paths),
        }
        for item in articles
    ]
    (OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    readme = ["# 苏州旅游图文博客离线包", "", f"共整理 {len(articles)} 篇，正文为 Markdown，图片已下载到各文章目录的 images/ 下。", ""]
    for item in articles:
        readme.append(f"- [{item.title}]({item.slug}/article.md) - 图片 {len(item.image_paths)} 张 - 来源：{item.source_url}")
    (OUT / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
