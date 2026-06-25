#!/usr/bin/env python3
"""Publish a local file into the private FileCodeBox deployment and print a pickup code."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import secrets
import shlex
import string
import subprocess
import sys
import uuid
from pathlib import Path

PUBLIC_URL = "https://drop-cn.zhangxuemin.work/"
EDGE_IP = "154.86.30.10"
ORIGIN_HOST = "oracle-mail"
DATA_ROOT = "/opt/filecodebox/data"
DB_PATH = f"{DATA_ROOT}/filecodebox.db"


def run(cmd: list[str], *, input_text: str | None = None) -> str:
    result = subprocess.run(
        cmd,
        input=input_text,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(
            f"command failed ({result.returncode}): {' '.join(shlex.quote(x) for x in cmd)}\n{result.stderr}"
        )
    return result.stdout


def five_digit_code() -> str:
    return str(secrets.randbelow(90000) + 10000)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--name", help="download filename shown in FileCodeBox")
    parser.add_argument("--downloads", type=int, default=1)
    parser.add_argument("--days", type=int, default=1)
    args = parser.parse_args()

    source = args.file.expanduser().resolve()
    if not source.is_file():
        raise SystemExit(f"not a file: {source}")
    if args.downloads < 1:
        raise SystemExit("--downloads must be >= 1")
    if args.days < 1:
        raise SystemExit("--days must be >= 1")

    display_name = args.name or source.name
    prefix, suffix = os.path.splitext(display_name)
    if not prefix:
        prefix = display_name
        suffix = ""

    file_uuid = uuid.uuid4().hex
    rel_dir = f"share/data/{dt.datetime.now().strftime('%Y/%m/%d')}/{file_uuid}"
    remote_tmp = f"/tmp/filecodebox-upload-{file_uuid}-{display_name}"
    remote_dest_dir = f"{DATA_ROOT}/{rel_dir}"
    remote_dest = f"{remote_dest_dir}/{display_name}"

    run(["ssh", "-o", "BatchMode=yes", ORIGIN_HOST, f"mkdir -p {shlex.quote(remote_dest_dir)} && chmod 700 {shlex.quote(remote_dest_dir)}"])
    run(["scp", str(source), f"{ORIGIN_HOST}:{remote_tmp}"])
    run(["ssh", "-o", "BatchMode=yes", ORIGIN_HOST, f"mv {shlex.quote(remote_tmp)} {shlex.quote(remote_dest)} && chmod 600 {shlex.quote(remote_dest)}"])

    code = five_digit_code()
    escaped = {
        "code": code,
        "prefix": prefix,
        "suffix": suffix,
        "name": display_name,
        "rel_dir": rel_dir,
        "size": str(source.stat().st_size),
        "downloads": str(args.downloads),
        "days": str(args.days),
    }
    env_prefix = " ".join(f"{k.upper()}={shlex.quote(v)}" for k, v in escaped.items())
    remote_python = r'''
import datetime as dt
import os
import random
import sqlite3

conn = sqlite3.connect(os.environ["DB_PATH"])
cur = conn.cursor()
code = os.environ["CODE"]
while cur.execute("select 1 from filecodes where code=?", (code,)).fetchone():
    code = str(random.randrange(10000, 100000))
expired_at = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=int(os.environ["DAYS"]))).strftime("%Y-%m-%d %H:%M:%S.%f+00:00")
cur.execute(
    """insert into filecodes
       (code,prefix,suffix,uuid_file_name,file_path,size,text,expired_at,expired_count,used_count,file_hash,is_chunked,upload_id)
       values (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
    (
        code,
        os.environ["PREFIX"],
        os.environ["SUFFIX"],
        os.environ["NAME"],
        os.environ["REL_DIR"],
        int(os.environ["SIZE"]),
        None,
        expired_at,
        int(os.environ["DOWNLOADS"]),
        0,
        None,
        0,
        None,
    ),
)
conn.commit()
print(code)
'''
    final_code = run(
        ["ssh", "-o", "BatchMode=yes", ORIGIN_HOST, f"DB_PATH={shlex.quote(DB_PATH)} {env_prefix} python3 - <<'PY'\n{remote_python}\nPY"]
    ).strip().splitlines()[-1]

    meta_raw = run(
        [
            "curl",
            "-sS",
            "--resolve",
            f"drop-cn.zhangxuemin.work:443:{EDGE_IP}",
            f"{PUBLIC_URL}share/metadata/?code={final_code}",
        ]
    )
    metadata = json.loads(meta_raw)
    if metadata.get("code") != 200:
        raise SystemExit(f"metadata check failed: {meta_raw}")

    print(json.dumps({"url": PUBLIC_URL, "pickup_code": final_code, "metadata": metadata["detail"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
