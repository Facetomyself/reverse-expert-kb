#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
from urllib.parse import urlparse

SEARCH_SCRIPT = "/root/.openclaw/workspace/skills/search-layer/scripts/search.py"
DEFAULT_SOURCES = "exa,tavily,grok"


def parse_args():
    p = argparse.ArgumentParser(description="Run search-layer with forced multi-source settings and emit audit JSON.")
    p.add_argument("query", nargs="?", help="Single query")
    p.add_argument("--queries", nargs="+", help="Multiple queries")
    p.add_argument("--mode", default="deep", choices=["fast", "deep", "answer"])
    p.add_argument("--num", type=int, default=5)
    p.add_argument("--intent", default="exploratory")
    p.add_argument("--freshness")
    p.add_argument("--domain-boost")
    p.add_argument("--sources", default=DEFAULT_SOURCES)
    p.add_argument("--save-audit", help="Path to write audit JSON")
    p.add_argument("--raw-out", help="Path to write raw stdout from search.py")
    return p.parse_args()


def build_cmd(args):
    cmd = [sys.executable, SEARCH_SCRIPT]
    if args.query:
        cmd.append(args.query)
    if args.queries:
        cmd.extend(["--queries", *args.queries])
    cmd.extend(["--mode", args.mode, "--num", str(args.num), "--intent", args.intent, "--source", args.sources])
    if args.freshness:
        cmd.extend(["--freshness", args.freshness])
    if args.domain_boost:
        cmd.extend(["--domain-boost", args.domain_boost])
    return cmd


def collect_hosts():
    hosts = {
        "exa": os.environ.get("REVERSE_KB_AUDIT_EXA_URL") or "http://158.178.236.241:7860",
        "tavily": os.environ.get("REVERSE_KB_AUDIT_TAVILY_URL") or "http://proxy.zhangxuemin.work:9874/api",
        "grok": os.environ.get("REVERSE_KB_AUDIT_GROK_URL") or "http://proxy.zhangxuemin.work:8000/v1",
    }
    return hosts


def try_parse_json(stdout: str):
    text = stdout.strip()
    if not text:
        return None
    candidates = [text]
    lines = text.splitlines()
    for i in range(len(lines)):
        chunk = "\n".join(lines[i:]).strip()
        if chunk.startswith("{") or chunk.startswith("["):
            candidates.append(chunk)
    for c in candidates:
        try:
            return json.loads(c)
        except Exception:
            pass
    return None


def summarize(parsed, requested_sources, stderr_text=""):
    per_source = {name: {"resultCount": 0, "status": "missing"} for name in requested_sources}
    stderr_lower = (stderr_text or "").lower()

    def normalize_name(name):
        if not name:
            return []
        if isinstance(name, str) and "," in name:
            return [part.strip() for part in name.split(",") if part.strip()]
        return [name]

    def upsert_source(name, count=None, status=None, note=None):
        rec = per_source.setdefault(name, {"resultCount": 0, "status": "missing"})
        if count is not None:
            rec["resultCount"] = max(rec.get("resultCount", 0), count)
        if status is not None:
            prev = rec.get("status")
            if prev == "failed":
                pass
            elif prev == "ok" and status in ("missing",):
                pass
            else:
                rec["status"] = status
        if note:
            notes = rec.setdefault("notes", [])
            if note not in notes:
                notes.append(note)

    if isinstance(parsed, dict):
        if isinstance(parsed.get("resultsBySource"), dict):
            for raw_name, value in parsed["resultsBySource"].items():
                names = normalize_name(raw_name)
                if isinstance(value, list):
                    count = len(value)
                    status = "ok" if count > 0 else "missing"
                    note = "composite-source-label" if len(names) > 1 else None
                    for name in names:
                        upsert_source(name, count=count, status=status, note=note)
                elif isinstance(value, dict):
                    count = value.get("count")
                    if count is None and isinstance(value.get("results"), list):
                        count = len(value["results"])
                    explicit_status = value.get("status")
                    if explicit_status == "failed":
                        status = "failed"
                    elif count is not None and count > 0:
                        status = "ok"
                    elif count == 0:
                        status = "missing"
                    else:
                        status = "missing"
                    note = "composite-source-label" if len(names) > 1 else None
                    for name in names:
                        upsert_source(name, count=count or 0, status=status, note=note)

        if isinstance(parsed.get("sources"), list):
            for s in parsed["sources"]:
                if isinstance(s, dict):
                    raw_name = s.get("name") or s.get("source")
                    names = normalize_name(raw_name)
                    if not names:
                        continue
                    count = s.get("count")
                    if count is None and isinstance(s.get("results"), list):
                        count = len(s["results"])
                    explicit_status = s.get("status")
                    if explicit_status == "failed":
                        status = "failed"
                    elif count is not None and count > 0:
                        status = "ok"
                    elif count == 0:
                        status = "missing"
                    else:
                        status = "missing"
                    note = "composite-source-label" if len(names) > 1 else None
                    for name in names:
                        upsert_source(name, count=count or 0, status=status, note=note)

        if isinstance(parsed.get("results"), list):
            grouped = {}
            for item in parsed["results"]:
                if isinstance(item, dict):
                    raw_name = item.get("source") or item.get("engine")
                    for name in normalize_name(raw_name):
                        grouped[name] = grouped.get(name, 0) + 1
            for name, count in grouped.items():
                upsert_source(name, count=count, status=("ok" if count > 0 else "missing"))

    for name in requested_sources:
        if f"[{name}] error:" in stderr_lower or f"[{name}] " in stderr_lower and "error:" in stderr_lower:
            upsert_source(name, status="failed", note="stderr-reported-error")
        elif per_source.get(name, {}).get("resultCount", 0) == 0 and per_source.get(name, {}).get("status") == "ok":
            upsert_source(name, status="missing", note="zero-results-not-counted-as-success")

    succeeded = sorted(name for name in requested_sources if per_source.get(name, {}).get("status") == "ok")
    failed = sorted(name for name in requested_sources if per_source.get(name, {}).get("status") != "ok")

    return {
        "perSource": per_source,
        "succeeded": succeeded,
        "failed": failed,
    }


def main():
    args = parse_args()
    if not args.query and not args.queries:
        print("need a query or --queries", file=sys.stderr)
        return 2
    cmd = build_cmd(args)
    proc = subprocess.run(cmd, capture_output=True, text=True)
    stdout = proc.stdout or ""
    stderr = proc.stderr or ""
    if args.raw_out:
        with open(args.raw_out, "w", encoding="utf-8") as f:
            f.write(stdout)
            if stderr:
                f.write("\n\n[stderr]\n")
                f.write(stderr)
    parsed = try_parse_json(stdout)
    requested = [s.strip() for s in args.sources.split(",") if s.strip()]
    summary = summarize(parsed, requested, stderr)
    succeeded = summary["succeeded"]
    failed = summary["failed"]
    hosts = collect_hosts()
    audit = {
        "query": args.query,
        "queries": args.queries,
        "mode": args.mode,
        "intent": args.intent,
        "requestedSources": requested,
        "succeededSources": succeeded,
        "failedSources": failed,
        "perSource": summary["perSource"],
        "endpoints": hosts,
        "searchScript": SEARCH_SCRIPT,
        "command": cmd,
        "returncode": proc.returncode,
        "stderr": stderr.strip(),
    }
    out = json.dumps(audit, ensure_ascii=False, indent=2)
    if args.save_audit:
        os.makedirs(os.path.dirname(args.save_audit), exist_ok=True)
        with open(args.save_audit, "w", encoding="utf-8") as f:
            f.write(out + "\n")
    print(out)
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
