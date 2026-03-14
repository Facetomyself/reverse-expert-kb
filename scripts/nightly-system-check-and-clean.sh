#!/usr/bin/env bash
set -Eeuo pipefail

WORKSPACE="/root/.openclaw/workspace"
REPORT_DIR="$WORKSPACE/maintenance/nightly-system-checks"
mkdir -p "$REPORT_DIR"

TS="$(date '+%Y-%m-%d-%H%M%S')"
REPORT="$REPORT_DIR/$TS.md"

LOW_SPACE_PCT=15
LOW_SPACE_BYTES=$((5 * 1024 * 1024 * 1024))

ROOT_AVAIL_BEFORE="$(df -B1 --output=avail / | tail -n1 | tr -d ' ')"
WS_AVAIL_BEFORE="$(df -B1 --output=avail "$WORKSPACE" | tail -n1 | tr -d ' ')"
ROOT_USE_PCT_BEFORE="$(df --output=pcent / | tail -n1 | tr -dc '0-9')"

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

cleanup_workspace_caches() {
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
}

cleanup_workspace_build_dirs() {
  while IFS= read -r -d '' dir; do
    log "- remove stale build dir: $dir"
    safe_rm_rf_dir "$dir"
  done < <(find "$WORKSPACE" -xdev \( \
    -name dist -o \
    -name build -o \
    -name out -o \
    -name target \
  \) -type d -mtime +7 -print0 2>/dev/null)
}

cleanup_workspace_old_logs() {
  while IFS= read -r -d '' file; do
    log "- remove old workspace log/tmp file: $file"
    safe_rm_file "$file"
  done < <(find "$WORKSPACE" -xdev -type f \( \
    -name '*.log' -o \
    -name '*.log.*' -o \
    -name '*.out' -o \
    -name '*.tmp' \
  \) -mtime +14 -print0 2>/dev/null)
}

cleanup_tmp() {
  while IFS= read -r -d '' file; do
    log "- remove old /tmp file: $file"
    safe_rm_file "$file"
  done < <(find /tmp -xdev -user root -type f -mtime +7 -print0 2>/dev/null)

  while IFS= read -r -d '' dir; do
    rmdir "$dir" 2>/dev/null || true
  done < <(find /tmp -xdev -user root -type d -empty -mtime +7 -print0 2>/dev/null)
}

cleanup_pressure_caches() {
  log "### Pressure cleanup mode"
  log "- root filesystem is under configured pressure threshold"

  if command -v apt-get >/dev/null 2>&1; then
    log "- apt cache cleanup: apt-get clean"
    apt-get clean >> "$REPORT" 2>&1 || log "  - apt-get clean failed"
  fi

  if [ -d /var/tmp ]; then
    while IFS= read -r -d '' file; do
      log "- remove old /var/tmp file: $file"
      safe_rm_file "$file"
    done < <(find /var/tmp -xdev -user root -type f -mtime +14 -print0 2>/dev/null)

    while IFS= read -r -d '' dir; do
      rmdir "$dir" 2>/dev/null || true
    done < <(find /var/tmp -xdev -user root -type d -empty -mtime +14 -print0 2>/dev/null)
  fi

  if command -v journalctl >/dev/null 2>&1; then
    log "- journal cleanup: journalctl --vacuum-time=14d"
    journalctl --vacuum-time=14d >> "$REPORT" 2>&1 || log "  - journal cleanup failed"
  fi

  if command -v docker >/dev/null 2>&1; then
    log "- docker cache cleanup: docker system prune -f --volumes"
    docker system prune -f --volumes >> "$REPORT" 2>&1 || log "  - docker prune failed"
  fi

  if command -v npm >/dev/null 2>&1; then
    log "- npm cache cleanup: npm cache clean --force"
    npm cache clean --force >> "$REPORT" 2>&1 || log "  - npm cache clean failed"
  fi

  if command -v pip >/dev/null 2>&1; then
    log "- pip cache cleanup: pip cache purge"
    pip cache purge >> "$REPORT" 2>&1 || log "  - pip cache purge failed"
  fi

  if command -v pip3 >/dev/null 2>&1; then
    log "- pip3 cache cleanup: pip3 cache purge"
    pip3 cache purge >> "$REPORT" 2>&1 || log "  - pip3 cache purge failed"
  fi

  if command -v uv >/dev/null 2>&1; then
    log "- uv cache cleanup: uv cache clean"
    uv cache clean >> "$REPORT" 2>&1 || log "  - uv cache clean failed"
  fi
}

pressure_cleanup_needed() {
  if [ "$ROOT_USE_PCT_BEFORE" -ge $((100 - LOW_SPACE_PCT)) ]; then
    return 0
  fi
  if [ "$ROOT_AVAIL_BEFORE" -le "$LOW_SPACE_BYTES" ]; then
    return 0
  fi
  return 1
}

log "# Nightly system check and cleanup"
log ""
log "- Timestamp: $(date --iso-8601=seconds)"
log "- Host: $(hostname)"
log "- Goal: inspect memory/storage and clean safe stale build/cache/log artifacts"
log "- Pressure thresholds: available <= ${LOW_SPACE_BYTES} bytes OR root usage >= $((100 - LOW_SPACE_PCT))%"
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
du -sh "$WORKSPACE" "$WORKSPACE/research" /var/log /tmp /var/tmp 2>/dev/null | sort -h >> "$REPORT" || true
log '```'
log ""
log "## Top workspace directories"
log '```'
du -xhd1 "$WORKSPACE" 2>/dev/null | sort -h | tail -n 25 >> "$REPORT" || true
log '```'
log ""
log "## Cleanup actions"

cleanup_workspace_caches
cleanup_workspace_build_dirs
cleanup_workspace_old_logs
cleanup_tmp

if pressure_cleanup_needed; then
  cleanup_pressure_caches
else
  log "### Pressure cleanup mode"
  log "- skipped: root filesystem is not under configured pressure threshold"
fi

ROOT_AVAIL_AFTER="$(df -B1 --output=avail / | tail -n1 | tr -d ' ')"
WS_AVAIL_AFTER="$(df -B1 --output=avail "$WORKSPACE" | tail -n1 | tr -d ' ')"
ROOT_USE_PCT_AFTER="$(df --output=pcent / | tail -n1 | tr -dc '0-9')"
ROOT_FREED=$((ROOT_AVAIL_AFTER - ROOT_AVAIL_BEFORE))
WS_FREED=$((WS_AVAIL_AFTER - WS_AVAIL_BEFORE))

log ""
log "## Cleanup summary"
log "- Removed items count: ${#removed_items[@]}"
log "- Estimated removed bytes (sum of deleted items): $removed_bytes"
log "- Root filesystem freed bytes: $ROOT_FREED"
log "- Workspace filesystem freed bytes: $WS_FREED"
log "- Root usage before: ${ROOT_USE_PCT_BEFORE}%"
log "- Root usage after: ${ROOT_USE_PCT_AFTER}%"
if [ ${#removed_items[@]} -gt 0 ]; then
  log "- Removed paths:"
  for item in "${removed_items[@]}"; do
    log "  - $item"
  done
else
  log "- No direct file removals were needed tonight."
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
