#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path
from typing import Any

WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_TFVARS = WORKSPACE_ROOT / "infra" / "cloudflare-dns" / "terraform.auto.tfvars"
API_BASE = "https://api.cloudflare.com/client/v4"
PER_PAGE = 100

ENV_TOKEN_KEYS = ("CLOUDFLARE_API_TOKEN", "CF_API_TOKEN")
ENV_ZONE_KEYS = ("CLOUDFLARE_ZONE_ID", "CF_ZONE_ID")


class CloudflareApiError(RuntimeError):
    pass


def parse_tfvars(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    pattern = re.compile(r'^\s*([A-Za-z0-9_]+)\s*=\s*"((?:[^"\\]|\\.)*)"\s*$')
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        match = pattern.match(raw_line)
        if not match:
            continue
        key, value = match.groups()
        values[key] = bytes(value, "utf-8").decode("unicode_escape")
    return values


def resolve_credentials(config_path: Path) -> tuple[str, str]:
    token = next((os.environ[k] for k in ENV_TOKEN_KEYS if os.environ.get(k)), None)
    zone_id = next((os.environ[k] for k in ENV_ZONE_KEYS if os.environ.get(k)), None)

    if token and zone_id:
        return zone_id, token

    tfvars = parse_tfvars(config_path)
    zone_id = zone_id or tfvars.get("zone_id")
    token = token or tfvars.get("cloudflare_api_token")

    if not zone_id or not token:
        missing = []
        if not zone_id:
            missing.append("zone id")
        if not token:
            missing.append("API token")
        joined = " and ".join(missing)
        raise SystemExit(
            f"Missing Cloudflare {joined}. Set env vars or populate {config_path}."
        )

    return zone_id, token


def api_get_json(path: str, token: str, query: dict[str, Any] | None = None) -> dict[str, Any]:
    url = f"{API_BASE}{path}"
    if query:
        url = f"{url}?{urllib.parse.urlencode(query)}"

    request = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "openclaw-cloudflare-zone-snapshot/1.0",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise CloudflareApiError(f"HTTP {exc.code} for {path}: {body[:400]}") from exc
    except urllib.error.URLError as exc:
        raise CloudflareApiError(f"Network error for {path}: {exc}") from exc

    if not payload.get("success"):
        errors = payload.get("errors") or []
        raise CloudflareApiError(f"Cloudflare API error for {path}: {errors}")

    return payload


def fetch_all_records(zone_id: str, token: str) -> list[dict[str, Any]]:
    page = 1
    records: list[dict[str, Any]] = []

    while True:
        payload = api_get_json(
            f"/zones/{zone_id}/dns_records",
            token,
            query={"page": page, "per_page": PER_PAGE},
        )
        batch = payload.get("result") or []
        records.extend(batch)

        result_info = payload.get("result_info") or {}
        total_pages = result_info.get("total_pages") or 1
        if page >= total_pages:
            break
        page += 1

    return records


def deep_sort(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: deep_sort(value[key]) for key in sorted(value)}
    if isinstance(value, list):
        return [deep_sort(item) for item in value]
    return value


def compact_record(record: dict[str, Any]) -> dict[str, Any]:
    keep_fields = (
        "name",
        "type",
        "content",
        "ttl",
        "proxied",
        "comment",
        "priority",
        "tags",
        "data",
    )
    out: dict[str, Any] = {}
    for field in keep_fields:
        if field not in record:
            continue
        value = record[field]
        if value in (None, "", [], {}):
            continue
        if field == "tags" and isinstance(value, list):
            out[field] = sorted(value)
            continue
        if field == "data":
            out[field] = deep_sort(value)
            continue
        out[field] = value
    return out


def sort_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        records,
        key=lambda item: (
            item.get("name", ""),
            item.get("type", ""),
            json.dumps(item, sort_keys=True, ensure_ascii=False),
        ),
    )


def build_snapshot(zone_id: str, records: list[dict[str, Any]]) -> dict[str, Any]:
    normalized = sort_records([compact_record(record) for record in records])
    type_counts = dict(sorted(Counter(r["type"] for r in normalized).items()))
    return {
        "zone_id": zone_id,
        "record_count": len(normalized),
        "type_counts": type_counts,
        "records": normalized,
    }


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def diff_snapshots(current: dict[str, Any], baseline: dict[str, Any]) -> dict[str, Any]:
    current_counter = Counter(
        json.dumps(record, sort_keys=True, ensure_ascii=False)
        for record in current.get("records", [])
    )
    baseline_counter = Counter(
        json.dumps(record, sort_keys=True, ensure_ascii=False)
        for record in baseline.get("records", [])
    )

    added: list[dict[str, Any]] = []
    removed: list[dict[str, Any]] = []

    for record_text, count in (current_counter - baseline_counter).items():
        record = json.loads(record_text)
        for _ in range(count):
            added.append(record)

    for record_text, count in (baseline_counter - current_counter).items():
        record = json.loads(record_text)
        for _ in range(count):
            removed.append(record)

    added = sort_records(added)
    removed = sort_records(removed)
    return {
        "changed": bool(added or removed),
        "added_count": len(added),
        "removed_count": len(removed),
        "added": added,
        "removed": removed,
    }


def record_to_line(record: dict[str, Any]) -> str:
    pieces = [record.get("type", "?"), record.get("name", "?")]
    if "content" in record:
        pieces.append(f"-> {record['content']}")
    if "priority" in record:
        pieces.append(f"priority={record['priority']}")
    if "proxied" in record:
        pieces.append(f"proxied={str(record['proxied']).lower()}")
    if "ttl" in record:
        pieces.append(f"ttl={record['ttl']}")
    if "comment" in record:
        pieces.append(f"comment={record['comment']}")
    if "data" in record:
        pieces.append(f"data={json.dumps(record['data'], ensure_ascii=False, sort_keys=True)}")
    return " ".join(pieces)


def render_summary(snapshot: dict[str, Any], diff: dict[str, Any] | None = None) -> str:
    lines = [
        "# Cloudflare DNS Snapshot",
        "",
        f"- zone_id: `{snapshot['zone_id']}`",
        f"- record_count: {snapshot['record_count']}",
        "- type_counts:",
    ]
    for record_type, count in snapshot.get("type_counts", {}).items():
        lines.append(f"  - {record_type}: {count}")

    if diff is not None:
        lines.extend(
            [
                "",
                "## Diff vs baseline",
                "",
                f"- changed: {'yes' if diff['changed'] else 'no'}",
                f"- added: {diff['added_count']}",
                f"- removed: {diff['removed_count']}",
            ]
        )
        if diff["added"]:
            lines.extend(["", "### Added"])
            lines.extend(f"- {record_to_line(record)}" for record in diff["added"])
        if diff["removed"]:
            lines.extend(["", "### Removed"])
            lines.extend(f"- {record_to_line(record)}" for record in diff["removed"])

    lines.extend(["", "## Records", ""])
    lines.extend(f"- {record_to_line(record)}" for record in snapshot["records"])
    lines.append("")
    return "\n".join(lines)


def dump_json_text(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False) + "\n"


def write_if_changed(path: Path, text: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    path.write_text(text, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Export and diff a Cloudflare DNS zone snapshot.")
    parser.add_argument("--config", type=Path, default=DEFAULT_TFVARS, help="Path to terraform.auto.tfvars")
    parser.add_argument("--json-out", type=Path, help="Write deterministic snapshot JSON here")
    parser.add_argument("--summary-out", type=Path, help="Write Markdown summary here")
    parser.add_argument("--baseline", type=Path, help="Optional baseline snapshot JSON for diffing")
    parser.add_argument("--diff-out", type=Path, help="Write diff JSON here when --baseline is set")
    parser.add_argument(
        "--stdout",
        choices=("summary", "json", "none"),
        default="summary",
        help="What to print to stdout",
    )
    args = parser.parse_args()

    zone_id, token = resolve_credentials(args.config)
    records = fetch_all_records(zone_id, token)
    snapshot = build_snapshot(zone_id, records)

    diff = None
    if args.baseline:
        if not args.baseline.exists():
            raise SystemExit(f"Baseline file not found: {args.baseline}")
        baseline = load_json(args.baseline)
        diff = diff_snapshots(snapshot, baseline)

    if args.json_out:
        write_if_changed(args.json_out, dump_json_text(snapshot))
    if args.summary_out:
        write_if_changed(args.summary_out, render_summary(snapshot, diff))
    if args.diff_out and diff is not None:
        write_if_changed(args.diff_out, dump_json_text(diff))

    if args.stdout == "summary":
        print(render_summary(snapshot, diff), end="")
    elif args.stdout == "json":
        print(dump_json_text(snapshot), end="")

    if diff and diff["changed"]:
        return 2
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except CloudflareApiError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
