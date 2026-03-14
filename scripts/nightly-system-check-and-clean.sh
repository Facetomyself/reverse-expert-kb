#!/usr/bin/env bash
set -Eeuo pipefail

WORKSPACE="/root/.openclaw/workspace"
REPORT_DIR="$WORKSPACE/maintenance/nightly-system-checks"
mkdir -p "$REPORT_DIR"

TS="$(date '+%Y-%m-%d-%H%M%S')"
REPORT="$REPORT_DIR/$TS.md"

ROOT_AVAIL_BEFORE="$(df -B1 --output=avail / | tail -n1 | tr -d ' ')"
WS_AVAIL_BEFORE="$(df -B1 --output=avail "$WORKSPACE" | tail -n1 | tr -d ' ')"

removed_items=()
removed_bytes=0

log() {
  printf '%s\n' "$*" >> "$REPORT"
}

record_remove() {
  local path="$1"
  local bytes="${2:-0}"
  removed_items+=("$path")
  removed_bytes=$((removed_bytes + bytes))
}

safe_rm_rf_dir() {
  local dir="$1"
  [ -d "$dir" ] || return 0
  local bytes
  bytes="$(du -sb "$dir" 2>/dev/null | awk '{print $1}' || echo 0)"
  rm -rf --one-file-system "$dir"
  record_remove "$dir" "$bytes"
}

safe_rm_file() {
  local file="$1"
  [ -f "$file" ] || return 0
  local bytes
  bytes="$(stat -c '%s' "$file" 2>/dev/null || echo 0)"
  rm -f -- "$file"
  record_remove "$file" "$bytes"
}

log "# Nightly system check and cleanup"
log ""
log "- Timestamp: $(date --iso-8601=seconds)"
log "- Host: $(hostname)"
log "- Goal: inspect memory/storage and clean safe stale build/cache/log artifacts"
log ""
log "## Memory snapshot"
log '```'
free -h >> "$REPORT" 2>&1 || true
log '```'
log ""
log "## Filesystem snapshot (before cleanup)"
log '```'
df -h / "$WORKSPACE" >> "$REPORT" 2>&1 || true
log '```'
log ""
log "## Large directories snapshot"
log '```'
du -sh "$WORKSPACE" "$WORKSPACE/research" /var/log /tmp 2>/dev/null | sort -h >> "$REPORT" || true
log '```'
log ""
log "## Top workspace directories"
log '```'
du -xhd1 "$WORKSPACE" 2>/dev/null | sort -h | tail -n 25 >> "$REPORT" || true
log '```'
log ""
log "## Cleanup actions"

# 1) Workspace cache directories — safe to remove.
while IFS= read -r -d '' dir; do
  log "- remove cache dir: $dir"
  safe_rm_rf_dir "$dir"
done < <(find "$WORKSPACE" -xdev \( \
  -name '__pycache__' -o \
  -name '.pytest_cache' -o \
  -name '.mypy_cache' -o \
  -name '.ruff_cache' -o \
  -name '.cache' \
\) -type d -print0 2>/dev/null)

# 2) Common build artifact directories inside workspace, only if stale.
while IFS= read -r -d '' dir; do
  log "- remove stale build dir: $dir"
  safe_rm_rf_dir "$dir"
done < <(find "$WORKSPACE" -xdev \( \
  -name dist -o \
  -name build -o \
  -name out -o \
  -name target \
\) -type d -mtime +7 -print0 2>/dev/null)

# 3) Old workspace log-like files.
while IFS= read -r -d '' file; do
  log "- remove old workspace log/tmp file: $file"
  safe_rm_file "$file"
done < <(find "$WORKSPACE" -xdev -type f \( \
  -name '*.log' -o \
  -name '*.log.*' -o \
  -name '*.out' -o \
  -name '*.tmp' \
\) -mtime +14 -print0 2>/dev/null)

# 4) Old root-owned temporary files in /tmp.
while IFS= read -r -d '' file; do
  log "- remove old /tmp file: $file"
  safe_rm_file "$file"
done < <(find /tmp -xdev -user root -type f -mtime +7 -print0 2>/dev/null)

# 5) Empty old directories in /tmp after file cleanup.
while IFS= read -r -d '' dir; do
  rmdir "$dir" 2>/dev/null || true
done < <(find /tmp -xdev -user root -type d -empty -mtime +7 -print0 2>/dev/null)

ROOT_AVAIL_AFTER="$(df -B1 --output=avail / | tail -n1 | tr -d ' ')"
WS_AVAIL_AFTER="$(df -B1 --output=avail "$WORKSPACE" | tail -n1 | tr -d ' ')"
ROOT_FREED=$((ROOT_AVAIL_AFTER - ROOT_AVAIL_BEFORE))
WS_FREED=$((WS_AVAIL_AFTER - WS_AVAIL_BEFORE))

log ""
log "## Cleanup summary"
log "- Removed items count: ${#removed_items[@]}"
log "- Estimated removed bytes (sum of deleted items): $removed_bytes"
log "- Root filesystem freed bytes: $ROOT_FREED"
log "- Workspace filesystem freed bytes: $WS_FREED"
if [ ${#removed_items[@]} -gt 0 ]; then
  log "- Removed paths:"
  for item in "${removed_items[@]}"; do
    log "  - $item"
  done
else
  log "- No files needed removal tonight."
fi
log ""
log "## Filesystem snapshot (after cleanup)"
log '```'
df -h / "$WORKSPACE" >> "$REPORT" 2>&1 || true
log '```'
log ""
log "## High-memory processes"
log '```'
ps -eo pid,ppid,comm,%mem,%cpu,rss --sort=-%mem | head -n 20 >> "$REPORT" 2>&1 || true
log '```'

printf '%s\n' "$REPORT"
