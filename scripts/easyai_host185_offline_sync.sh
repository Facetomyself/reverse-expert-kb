#!/usr/bin/env bash
set -euo pipefail

STATE_DIR=/root/.openclaw/workspace/state/easyai_host185
LOG_FILE="$STATE_DIR/orchestrator.log"
STATE_FILE="$STATE_DIR/orchestrator.env"
LOCK_FILE="$STATE_DIR/orchestrator.lock"
ALI_HTTP_ROOT=/tmp/easyai-image-cache/http-root
ALI_HTTP_PORT=18083
HOST_TEMP_DIR=/data

mkdir -p "$STATE_DIR"

ts() {
  date '+%F %T %Z'
}

log() {
  printf '[%s] %s\n' "$(ts)" "$*"
}

LAST_OK=""
CURRENT_STEP=""
CURRENT_IMAGE=""
CURRENT_SAFE=""
LAST_ERROR=""

write_state() {
  cat >"$STATE_FILE" <<EOF
status=${1}
updated_at=$(ts)
current_step=${2:-}
current_image=${3:-}
last_ok=${LAST_OK}
error=${4:-}
pid=$$
log_file=${LOG_FILE}
EOF
}

remote_host() {
  local cmd="$1"
  ssh -o BatchMode=yes self-server-44005 "bash -lc $(printf '%q' "$cmd")"
}

remote_ali() {
  local cmd="$1"
  ssh -o BatchMode=yes ali-cloud "bash -lc $(printf '%q' "$cmd")"
}

retry() {
  local max_attempts="$1"
  shift
  local attempt=1
  local rc=0
  while true; do
    if "$@"; then
      return 0
    else
      rc=$?
    fi
    if (( attempt >= max_attempts )); then
      return "$rc"
    fi
    log "retry ${attempt}/${max_attempts} failed (rc=${rc}): $*"
    sleep $(( attempt * 10 ))
    attempt=$(( attempt + 1 ))
  done
}

release_lock() {
  if [ -f "$LOCK_FILE" ] && [ "$(cat "$LOCK_FILE" 2>/dev/null || true)" = "$$" ]; then
    rm -f "$LOCK_FILE"
  fi
}

cleanup_current_temp() {
  if [ -n "$CURRENT_SAFE" ]; then
    remote_host "rm -f '${HOST_TEMP_DIR}/${CURRENT_SAFE}.tar.gz'" >/dev/null 2>&1 || true
    remote_ali "rm -f '${ALI_HTTP_ROOT}/${CURRENT_SAFE}.tar.gz'" >/dev/null 2>&1 || true
  fi
}

on_exit() {
  local rc=$?
  if (( rc != 0 )); then
    write_state failed "${CURRENT_STEP:-unknown}" "${CURRENT_IMAGE:-}" "${LAST_ERROR:-script exited rc=${rc}}"
    log "FAILED rc=${rc} step=${CURRENT_STEP:-unknown} image=${CURRENT_IMAGE:-none} error=${LAST_ERROR:-none}"
  fi
  cleanup_current_temp
  release_lock
  exit "$rc"
}

if [ -f "$LOCK_FILE" ]; then
  existing_pid="$(cat "$LOCK_FILE" 2>/dev/null || true)"
  if [ -n "$existing_pid" ] && kill -0 "$existing_pid" 2>/dev/null; then
    write_state already_running preflight "" "existing_pid=${existing_pid}"
    echo "orchestrator already running with pid ${existing_pid}"
    exit 99
  fi
  rm -f "$LOCK_FILE"
fi

echo "$$" >"$LOCK_FILE"
exec > >(tee -a "$LOG_FILE") 2>&1
trap on_exit EXIT

write_state running preflight "" ""
log "starting easyai host185 offline sync orchestrator"

ALI_PUBLIC_HOST="$(ssh -G ali-cloud 2>/dev/null | awk '$1=="hostname"{print $2; exit}' || true)"
ALI_PUBLIC_HOST="${ALI_PUBLIC_HOST:-106.15.239.221}"
log "ali-cloud public host resolved to ${ALI_PUBLIC_HOST}"

CURRENT_STEP=preflight_remote_check
write_state running "$CURRENT_STEP" "" ""
log "checking for remote transfer/import processes before starting"
HOST_BUSY="$(remote_host "ps -eo pid,etimes,cmd | grep -E 'curl -fL|wget |aria2c|docker load|gunzip|pigz|pv |python3 -m http.server|http.server|split -b|cat /data/.*tar|docker-compose up|docker compose up' | grep -v -E 'grep -E|egrep' || true")"
ALI_BUSY="$(remote_ali "ps -eo pid,etimes,cmd | grep -E 'docker pull|ctr --address /var/run/docker/containerd/containerd.sock -n moby images pull|docker save|gzip -1|pigz|split -b|tar -cf|cat .*tar|rsync .*easyai|scp .*easyai' | grep -v -E 'grep -E|egrep' || true")"
printf '%s\n' "$HOST_BUSY"
printf '%s\n' "$ALI_BUSY"
HOST_BUSY_FILTERED="$(printf '%s\n' "$HOST_BUSY" | grep -Ev '^[[:space:]]*$' || true)"
ALI_BUSY_FILTERED="$(printf '%s\n' "$ALI_BUSY" | grep -Ev '^[[:space:]]*$' || true)"
if [ -n "$HOST_BUSY_FILTERED" ] || [ -n "$ALI_BUSY_FILTERED" ]; then
  LAST_ERROR="existing remote transfer/import process detected"
  write_state already_running "$CURRENT_STEP" "" "$LAST_ERROR"
  log "$LAST_ERROR"
  exit 99
fi

CURRENT_STEP=ensure_http_server
write_state running "$CURRENT_STEP" "" ""
log "ensuring ali-cloud HTTP helper is ready"
remote_ali "mkdir -p '${ALI_HTTP_ROOT}' && if ! pgrep -af 'python3 -m http.server ${ALI_HTTP_PORT} --bind 0.0.0.0 --directory ${ALI_HTTP_ROOT}' >/dev/null 2>&1; then nohup python3 -m http.server ${ALI_HTTP_PORT} --bind 0.0.0.0 --directory '${ALI_HTTP_ROOT}' >/tmp/easyai-image-cache/http.log 2>&1 </dev/null & sleep 1; fi"
retry 2 remote_host "curl -fsI --max-time 15 'http://${ALI_PUBLIC_HOST}:${ALI_HTTP_PORT}/' >/dev/null"

images=(
  'registry.cn-shanghai.aliyuncs.com/easyaigc/pgvector:0.8.2-pg18-trixie'
  'registry.cn-shanghai.aliyuncs.com/comfy-ai/watchtower-aliyun:latest'
  'registry.cn-shanghai.aliyuncs.com/easyaigc/agent-memory:latest'
  'registry.cn-shanghai.aliyuncs.com/easyaigc/dozzle:latest'
  'registry.cn-shanghai.aliyuncs.com/easyaigc/mq:latest'
  'registry.cn-shanghai.aliyuncs.com/easyaigc/sandbox:latest'
  'registry.cn-shanghai.aliyuncs.com/easyaigc/videoedit:latest'
  'registry.cn-shanghai.aliyuncs.com/easyaigc/wsgateway:latest'
  'registry.cn-shanghai.aliyuncs.com/comfy-ai/comfy-server:latest'
)

for img in "${images[@]}"; do
  CURRENT_IMAGE="$img"
  CURRENT_SAFE="$(printf '%s' "$img" | sed 's#[/:]#-#g')"
  BUNDLE_PATH="${ALI_HTTP_ROOT}/${CURRENT_SAFE}.tar.gz"
  SOURCE_MODE=""

  if remote_host "docker image inspect '${img}' >/dev/null 2>&1"; then
    log "skip already-present image on host185: ${img}"
    LAST_OK="$img"
    write_state running skip_present "$img" ""
    CURRENT_SAFE=""
    continue
  fi

  CURRENT_STEP=ensure_source_image
  write_state running "$CURRENT_STEP" "$img" ""
  log "[${img}] ensuring source image exists on ali-cloud"
  if remote_ali "docker image inspect '${img}' >/dev/null 2>&1"; then
    SOURCE_MODE=docker
    log "[${img}] source already present on ali-cloud via docker"
  elif remote_ali "ctr --address /var/run/docker/containerd/containerd.sock -n moby images ls | grep -F '${img} ' >/dev/null 2>&1"; then
    SOURCE_MODE=ctr
    log "[${img}] source already present on ali-cloud via ctr"
  else
    SOURCE_MODE=ctr
    LAST_ERROR="ctr pull failed for ${img} on ali-cloud"
    retry 2 remote_ali "ctr --address /var/run/docker/containerd/containerd.sock -n moby images pull '${img}'"
  fi
  if [ "$SOURCE_MODE" = docker ]; then
    remote_ali "docker image inspect '${img}' --format 'source_size={{.Size}} bytes'"
  else
    remote_ali "ctr --address /var/run/docker/containerd/containerd.sock -n moby images ls | grep -F '${img} '"
  fi

  CURRENT_STEP=bundle_on_ali
  write_state running "$CURRENT_STEP" "$img" ""
  LAST_ERROR="bundle creation failed for ${img} on ali-cloud"
  log "[${img}] creating compressed bundle on ali-cloud"
  if [ "$SOURCE_MODE" = docker ]; then
    retry 2 remote_ali "rm -f '${BUNDLE_PATH}' && docker save '${img}' | gzip -1 > '${BUNDLE_PATH}' && chmod 644 '${BUNDLE_PATH}' && ls -lh '${BUNDLE_PATH}'"
  else
    retry 2 remote_ali "rm -f '${BUNDLE_PATH}' && ctr --address /var/run/docker/containerd/containerd.sock -n moby images export - '${img}' | gzip -1 > '${BUNDLE_PATH}' && chmod 644 '${BUNDLE_PATH}' && ls -lh '${BUNDLE_PATH}'"
  fi

  CURRENT_STEP=download_to_host185
  write_state running "$CURRENT_STEP" "$img" ""
  LAST_ERROR="download failed for ${img} to host185"
  log "[${img}] downloading compressed bundle to host185"
  retry 2 remote_host "rm -f '${HOST_TEMP_DIR}/${CURRENT_SAFE}.tar.gz' && docker run --rm --entrypoint aria2c -v '${HOST_TEMP_DIR}:${HOST_TEMP_DIR}' p3terx/aria2-pro --show-console-readout=false --summary-interval=30 --allow-overwrite=true --check-integrity=true --max-connection-per-server=1 --split=1 -d '${HOST_TEMP_DIR}' -o '${CURRENT_SAFE}.tar.gz' 'http://${ALI_PUBLIC_HOST}:${ALI_HTTP_PORT}/${CURRENT_SAFE}.tar.gz' && ls -lh '${HOST_TEMP_DIR}/${CURRENT_SAFE}.tar.gz'"

  CURRENT_STEP=load_on_host185
  write_state running "$CURRENT_STEP" "$img" ""
  LAST_ERROR="docker load failed for ${img} on host185"
  log "[${img}] loading compressed bundle into host185 docker"
  retry 2 remote_host "docker load -i '${HOST_TEMP_DIR}/${CURRENT_SAFE}.tar.gz'"

  CURRENT_STEP=verify_on_host185
  write_state running "$CURRENT_STEP" "$img" ""
  LAST_ERROR="verification failed for ${img} on host185"
  remote_host "docker image inspect '${img}' --format 'loaded {{.RepoTags}} {{.Id}}'"

  CURRENT_STEP=cleanup_host_temp
  write_state running "$CURRENT_STEP" "$img" ""
  log "[${img}] cleaning host185 temp bundle"
  remote_host "rm -f '${HOST_TEMP_DIR}/${CURRENT_SAFE}.tar.gz'"

  CURRENT_STEP=cleanup_ali_temp
  write_state running "$CURRENT_STEP" "$img" ""
  log "[${img}] cleaning ali-cloud temp bundle"
  remote_ali "rm -f '${BUNDLE_PATH}'"

  LAST_OK="$img"
  CURRENT_SAFE=""
  CURRENT_STEP=image_complete
  write_state running "$CURRENT_STEP" "$img" ""
  log "[${img}] image sync complete"
done

CURRENT_IMAGE=""
CURRENT_SAFE=""
CURRENT_STEP=compose_up
write_state running "$CURRENT_STEP" "" ""
log "all required images present; starting docker-compose up -d on host185"
remote_host "cd /opt/easyai && if command -v docker-compose >/dev/null 2>&1; then docker-compose up -d; else docker compose up -d; fi"

CURRENT_STEP=compose_settle
write_state running "$CURRENT_STEP" "" ""
sleep 20

CURRENT_STEP=compose_ps
write_state running "$CURRENT_STEP" "" ""
log "compose ps after startup"
COMPOSE_PS="$(remote_host "cd /opt/easyai && if command -v docker-compose >/dev/null 2>&1; then docker-compose ps; else docker compose ps; fi")"
printf '%s\n' "$COMPOSE_PS"

CURRENT_STEP=container_status
write_state running "$CURRENT_STEP" "" ""
log "docker ps -a snapshot"
DOCKER_PS="$(remote_host "docker ps -a --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}'")"
printf '%s\n' "$DOCKER_PS"

CURRENT_STEP=key_logs
write_state running "$CURRENT_STEP" "" ""
log "tailing compose logs for key services"
KEY_LOGS="$(remote_host "cd /opt/easyai && if command -v docker-compose >/dev/null 2>&1; then docker-compose logs --tail=60; else docker compose logs --tail=60; fi")"
printf '%s\n' "$KEY_LOGS"

BAD_STATUS="$(printf '%s\n' "$COMPOSE_PS" | grep -E 'Exit|Restarting|unhealthy|Created' || true)"
if [ -n "$BAD_STATUS" ]; then
  LAST_ERROR="compose has non-running containers after startup"
  write_state blocked compose_validation "" "$LAST_ERROR"
  log "compose blockers detected"
  printf '%s\n' "$BAD_STATUS"
  exit 2
fi

CURRENT_STEP=complete
write_state complete "$CURRENT_STEP" "" ""
log "easyai host185 offline sync completed successfully"