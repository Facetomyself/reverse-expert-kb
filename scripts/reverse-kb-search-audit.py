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


def summarize(parsed):
    per_source = {}
    succeeded = set()
    failed = set()

    def mark_source(name, count=None, status=None):
        rec = per_source.setdefault(name, {})
        if count is not None:
            rec["resultCount"] = count
        if status is not None:
            rec["status"] = status
        if status == "ok":
            succeeded.add(name)
        elif status == "failed":
            failed.add(name)

    if isinstance(parsed, dict):
        if isinstance(parsed.get("resultsBySource"), dict):
            for name, value in parsed["resultsBySource"].items():
                if isinstance(value, list):
                    mark_source(name, len(value), "ok")
                elif isinstance(value, dict):
                    count = value.get("count")
                    if count is None and isinstance(value.get("results"), list):
                        count = len(value["results"])
                    status = value.get("status") or ("ok" if count is not None else None)
                    mark_source(name, count, status)
        if isinstance(parsed.get("sources"), list):
            for s in parsed["sources"]:
                if isinstance(s, dict):
                    name = s.get("name") or s.get("source")
                    if not name:
                        continue
                    count = s.get("count")
                    if count is None and isinstance(s.get("results"), list):
                        count = len(s["results"])
                    status = s.get("status") or ("ok" if count is not None else None)
                    mark_source(name, count, status)
        if isinstance(parsed.get("results"), list):
            grouped = {}
            for item in parsed["results"]:
                if isinstance(item, dict):
                    src = item.get("source") or item.get("engine")
                    if src:
                        grouped[src] = grouped.get(src, 0) + 1
            for src, cnt in grouped.items():
                mark_source(src, cnt, "ok")
    return {
        "perSource": per_source,
        "succeeded": sorted(succeeded),
        "failed": sorted(failed),
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
    summary = summarize(parsed)
    requested = [s.strip() for s in args.sources.split(",") if s.strip()]
    succeeded = summary["succeeded"]
    failed = sorted(set(requested) - set(succeeded))
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
