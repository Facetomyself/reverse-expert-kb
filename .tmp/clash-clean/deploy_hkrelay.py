import pathlib, shutil, os, subprocess, sys
from textwrap import dedent

TOKEN = "2ad908995c00263f55d7879b03e6fa09c37f256a"
ROOT = pathlib.Path("/srv/drop/public")
SUBDIR = ROOT / f"sub-{TOKEN}"
SUBDIR.mkdir(parents=True, exist_ok=True)

# Preserve previous artifacts if present.
for name in ["clash-clean.yaml", "clash-clean.yaml.bak", "clash-meta.yaml", "clash-compat.yaml", "clash-classic.yaml"]:
    p = SUBDIR / name
    if p.exists():
        pass

src = pathlib.Path("/root/.openclaw/workspace/.tmp/clash-clean/clash-clean.yaml")
clean_dst = SUBDIR / "clash-clean.yaml"
shutil.copy2(src, clean_dst)

# Update Caddyfile with a new exact path matcher.
caddy = pathlib.Path("/etc/caddy/Caddyfile")
old = caddy.read_text()
block = f"""clash.hk.zhangxuemin.work {{
	encode gzip
	root * /srv/drop/public
	@yaml path /sub-a49d371396d93e9572ddecff6f51fc4707316b99c0edc0b6/clash-meta.yaml /sub-a49d371396d93e9572ddecff6f51fc4707316b99c0edc0b6/clash-compat.yaml /sub-a49d371396d93e9572ddecff6f51fc4707316b99c0edc0b6/clash-classic.yaml /sub-{TOKEN}/clash-clean.yaml
	handle @yaml {{
		header Content-Type "text/yaml; charset=utf-8"
		file_server
	}}
	respond 404
}}
"""
new = old.replace(
    "clash.hk.zhangxuemin.work {\n\tencode gzip\n\troot * /srv/drop/public\n\t@yaml path /sub-a49d371396d93e9572ddecff6f51fc4707316b99c0edc0b6/clash-meta.yaml /sub-a49d371396d93e9572ddecff6f51fc4707316b99c0edc0b6/clash-compat.yaml /sub-a49d371396d93e9572ddecff6f51fc4707316b99c0edc0b6/clash-classic.yaml\n\thandle @yaml {\n\t\theader Content-Type \"text/yaml; charset=utf-8\"\n\t\tfile_server\n\t}\n\trespond 404\n}\n",
    block,
)
if new == old:
    raise SystemExit("Caddyfile block not replaced")
caddy.write_text(new)

# Validate YAML syntax before reload.
import yaml
yaml.safe_load(clean_dst.read_text())
print("deployed", clean_dst)
print("caddyfile updated")
