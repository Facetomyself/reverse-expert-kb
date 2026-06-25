#!/bin/sh
set -eu
mkdir -p "$HOME/hysteria-client/bin" "$HOME/hysteria-client/conf" "$HOME/hysteria-client/log"
cd "$HOME/hysteria-client/bin"
if [ ! -x ./hysteria ]; then
  curl -L --fail --retry 20 --retry-delay 3 -C - -o hysteria https://download.hysteria.network/app/latest/hysteria-linux-amd64
  chmod +x hysteria
fi
pkill -f "$HOME/hysteria-client/bin/hysteria client -c $HOME/hysteria-client/conf/client.yaml" 2>/dev/null || true
nohup "$HOME/hysteria-client/bin/hysteria" client -c "$HOME/hysteria-client/conf/client.yaml" > "$HOME/hysteria-client/log/client.log" 2>&1 < /dev/null &
echo $! > "$HOME/hysteria-client/log/client.pid"
sleep 3
printf 'BIN='; wc -c < "$HOME/hysteria-client/bin/hysteria" || true
printf '\nPID='; cat "$HOME/hysteria-client/log/client.pid" || true
printf '\nPORTS\n'; (netstat -ltn 2>/dev/null | egrep ':(10808|10809)\b') || true
printf '\nLOG\n'; tail -n 30 "$HOME/hysteria-client/log/client.log" 2>/dev/null || true
