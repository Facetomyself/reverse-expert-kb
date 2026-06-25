---
name: filecodebox-drop
description: "Publish local files through the private FileCodeBox drop service and return pickup codes."
allowed-tools:
  - exec
  - memory_search
---

# FileCodeBox drop

Use when the user asks to make a local file externally downloadable, send a file through 文件快递柜/FileCodeBox, or provide a 取件码.

## Current deployment

- Public entry: `https://drop-cn.zhangxuemin.work/`
- Edge: `hk-relay` Caddy, no extra Basic Auth.
- Origin: `oracle-mail:/opt/filecodebox`, container `filecodebox`.
- Data root: `oracle-mail:/opt/filecodebox/data` mounted to `/app/data`.
- Source port `18085` should stay reachable only from `hk-relay` plus localhost.

## Workflow

1. Confirm the source path exists and is the intended file; avoid printing secret file contents.
2. Run `scripts/publish_filecodebox.py <local-file> [--name download-name] [--downloads 1] [--days 1]`.
3. Verify the script reports metadata from `/share/metadata/` with the expected filename, size, and remaining downloads.
4. Reply with only the public entry URL, pickup code, filename, expiry, and usage note.

## Safety

- For private keys and credentials, default to `--downloads 1 --days 1`.
- Do not paste secret material into chat; provide the FileCodeBox code instead.
- The code must be 5 digits for numeric FileCodeBox compatibility; do not hand-generate 6-digit codes.
- If the public upload API says guest upload is disabled, use the script; it writes through the trusted origin data root and SQLite DB.
