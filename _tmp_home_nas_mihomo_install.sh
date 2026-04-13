#!/bin/sh
set -eu

BIN_DIR=/usr/local/bin
CONF_DIR=/usr/local/etc/mihomo
RUN_DIR=/usr/local/etc/mihomo/run
LOG_FILE=/var/log/mihomo.log
RC_SCRIPT=/usr/local/etc/rc.d/S98mihomo.sh
BIN_PATH="$BIN_DIR/mihomo"

install -d -m 755 "$BIN_DIR" "$CONF_DIR" "$RUN_DIR"

cat > "$RC_SCRIPT" <<'SH'
#!/bin/sh
case "$1" in
  start)
    mkdir -p /usr/local/etc/mihomo/run
    nohup /usr/local/bin/mihomo -d /usr/local/etc/mihomo -f /usr/local/etc/mihomo/config.yaml >>/var/log/mihomo.log 2>&1 &
    ;;
  stop)
    pkill -f '/usr/local/bin/mihomo -d /usr/local/etc/mihomo -f /usr/local/etc/mihomo/config.yaml' || true
    ;;
  restart)
    "$0" stop
    sleep 1
    "$0" start
    ;;
  status)
    pgrep -af '/usr/local/bin/mihomo -d /usr/local/etc/mihomo -f /usr/local/etc/mihomo/config.yaml' || true
    ;;
  *)
    echo "Usage: $0 {start|stop|restart|status}" >&2
    exit 1
    ;;
esac
SH
chmod +x "$RC_SCRIPT"

echo "Prepared directories and rc.d launcher skeleton: $RC_SCRIPT"
echo "Next steps: place mihomo binary at $BIN_PATH and write $CONF_DIR/config.yaml"
