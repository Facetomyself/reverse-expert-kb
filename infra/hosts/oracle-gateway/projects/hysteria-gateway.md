# hysteria + derp on oracle-gateway

## 1. Summary
`oracle-gateway` is now a focused small-footprint gateway host.

Current live public split:
- `derper`
  - `TCP 80/443`
  - `UDP 3478`
  - domain: `derp.zhangxuemin.work`
- `hysteria`
  - `UDP 443`
  - domain: `backup.zhangxuemin.work`
- retained host `caddy`
  - local helper only
  - currently on `TCP 8080/8443`

The historical docker/registry-proxy identity of this host is retired and should not drive current operational decisions.

## 2. DERP runtime
- binary: `/usr/local/bin/derper`
- systemd unit: `derper.service`
- unit path: `/etc/systemd/system/derper.service`
- cert storage: `/var/lib/derper/certs`
- working dir: `/var/lib/derper`
- current flags:
  - `-hostname derp.zhangxuemin.work`
  - `-a :443`
  - `-http-port 80`
  - `-stun`
  - `-stun-port 3478`
  - `-certdir /var/lib/derper/certs`
  - `-verify-clients`

## 3. Hysteria runtime
- protocol role: public UDP relay / gateway
- public listener: `UDP 443`
- deployment dir: `/opt/hysteria`
- config file: `/opt/hysteria/config.yaml`
- compose file: `/opt/hysteria/docker-compose.yml`
- masquerade upstream: `https://dreamhorse.eu.cc/`

## 4. Retained Caddy behavior
- service: `caddy.service`
- config file: `/etc/caddy/Caddyfile`
- admin API: `127.0.0.1:2019`
- current purpose: retained helper for legacy `backup.zhangxuemin.work` content path, no longer the primary public front door
- current alternate ports:
  - `TCP 8080`
  - `TCP 8443`

## 5. Quick checks
```bash
ssh oracle-gateway
systemctl status derper --no-pager
systemctl status caddy --no-pager
ss -ltnup | egrep ':(80|443|3478|8080|8443)\b'
curl -kI https://derp.zhangxuemin.work
curl -k https://derp.zhangxuemin.work/debug/ | head
```

## 6. Operational cautions
- This host is RAM-constrained (`~952 MiB` total), so avoid putting unrelated services back on it.
- `derper` must bind public `80/443` directly; do not put it behind a normal HTTP reverse proxy.
- Keep `tailscaled` and `derper` on aligned versions when using `-verify-clients`.
- Treat `oracle-gateway` as the only active identity for this host in current docs and operations.
