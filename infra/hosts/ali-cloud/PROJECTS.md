# ali-cloud / PROJECTS

## 1. 1Panel
Confirmed:
- systemd unit: `1panel.service`
- binary: `/usr/local/bin/1panel`
- state/data path: `/opt/1panel`
- DB: `/opt/1panel/db/1Panel.db`
- logs: `/opt/1panel/log/`
- host port `80` currently owned by `1panel`

Operational implication:
- this host is not “just Docker”; 1Panel is the machine-level app/control plane and may manage app deployment metadata and lifecycle.

## 2. EasyImages
Confirmed:
- container name: `easyimage`
- image: `ddsderek/easyimage:v2.8.6`
- published port: `10086 -> 80`
- compose project: `easyimage2`
- compose path: `/opt/1panel/apps/easyimage2/easyimage2/docker-compose.yml`
- data mounts:
  - `/opt/1panel/apps/easyimage2/easyimage2/data/i` -> `/app/web/i`
  - `/opt/1panel/apps/easyimage2/easyimage2/data/config` -> `/app/web/config`
- lifecycle labels suggest it was created by 1Panel Apps

## 3. camoufox-remote
Confirmed:
- container name: `camoufox-remote`
- image: `apify/actor-python-playwright-camoufox:latest`
- published port: `39222 -> 39222`
- env indicates websocket/browser service on `0.0.0.0:39222`
- deployment clue path: `/opt/camoufox-remote/run_camoufox_server_compat.py`

Operational implication:
- this service looks separate from 1Panel-managed apps and may be a manually maintained automation endpoint.

## 4. Hysteria egress (persistent local outbound path)
Confirmed on 2026-04-04:
- deployment root: `/opt/hysteria-egress`
- runtime shape: Docker Compose via legacy `/usr/bin/docker-compose`
- compose file: `/opt/hysteria-egress/docker-compose.yml`
- config file: `/opt/hysteria-egress/client.yaml`
- container name: `hysteria-client`
- image pinned by digest: `tobyxdd/hysteria@sha256:f66cda11f8e72e70bbf6f623d51ac6a09be878933850e0425c0253d7d756015e`
- network mode: `host`
- local SOCKS5 listener: `127.0.0.1:18080`
- systemd wrapper: `hysteria-egress.service`

Validated behavior:
- egress IP through the SOCKS5 listener was `129.150.61.78`
- `https://registry-1.docker.io/v2/` returned expected `401` via SOCKS5
- this shape is intentionally local-only for now: it improves this host's outbound access but does not yet expose a general-purpose public gateway service

## 5. Docker daemon outbound proxying
Confirmed on 2026-04-04:
- drop-in path: `/etc/systemd/system/docker.service.d/proxy.conf`
- configured env:
  - `HTTP_PROXY=socks5://127.0.0.1:18080`
  - `HTTPS_PROXY=socks5://127.0.0.1:18080`
  - `NO_PROXY=localhost,127.0.0.1,::1`
- Docker daemon no longer treats `hub.zhangxuemin.work` as a required registry mirror; same-day follow-up removed `registry-mirrors` from `/etc/docker/daemon.json` after validation showed the mirror could return manifests while still failing some Docker Hub blobs with `blob unknown`

Operational implication:
- Docker pulls on this host now rely primarily on the local Hysteria SOCKS5 path to reach official foreign registry endpoints
- `hub.zhangxuemin.work` is now considered an optional accelerator only, not a life-support dependency
- this primary path was validated with successful pulls for `hello-world`, `tobyxdd/hysteria:latest`, and post-cutover repulls of `busybox` plus `hello-world`

## 6. sing-box gateway ingress (first public transit entrypoint)
Confirmed on 2026-04-04:
- deployment root: `/opt/sing-box-gateway`
- runtime shape: Docker Compose via `/usr/bin/docker-compose`
- compose file: `/opt/sing-box-gateway/docker-compose.yml`
- config file: `/opt/sing-box-gateway/config.json`
- systemd wrapper: `sing-box-gateway.service`
- container name: `sing-box-gateway`
- image pinned by digest: `ghcr.io/sagernet/sing-box@sha256:8772c662c8e349d3afb0c233ccc3864d7df69ce840d5aa25db4c248d5bcb44f7`
- public SOCKS5 listener: `0.0.0.0:2080`
- public HTTP proxy listener: `0.0.0.0:2081`
- upstream outbound target: local Hysteria SOCKS5 at `127.0.0.1:18080`

Authentication currently enabled:
- username: `gateway`
- password: stored in `/opt/sing-box-gateway/config.json`

Validated behavior:
- SOCKS5 access through `106.15.239.221:2080` reached egress IP `129.150.61.78`
- HTTP proxy access through `106.15.239.221:2081` also reached egress IP `129.150.61.78`
- official Docker Hub registry probe via the public SOCKS5 listener returned expected `401`
- GitHub via the public HTTP proxy returned `HTTP/2 200`

## 7. CoreDNS DNS forwarder (public helper for domestic consumer hosts)
Confirmed on 2026-04-04:
- deployment root: `/opt/coredns-gateway`
- runtime shape: Docker-managed CoreDNS listener
- public listeners:
  - `0.0.0.0:1053/tcp`
  - `0.0.0.0:1053/udp`
- current purpose:
  - provide a simple stable DNS forwarder for domestic hosts that keep local `dnsmasq`
- validated consumers:
  - `self-server :44001` (`181`)
  - `self-server :44005` (`185`)

Validated consumer pattern:
- consumer `/etc/resolv.conf` -> `127.0.0.1`
- consumer local `dnsmasq` upstream -> `106.15.239.221#1053`
- with that shape in place, both consumer hosts restored stable resolution and successful Docker Hub pulls

Current role interpretation:
- this host now acts as a practical first-pass China-side transit gateway into Oracle-side egress
- present stable shape is: public DNS helper (`1053`) + public explicit proxies (`2080` / `2081`) + local Oracle-side Hysteria egress (`127.0.0.1:18080`)
- for Docker on this host, the primary dependable path is now official registries over the local Hysteria proxy, not the self-hosted Docker Hub mirror
- current shape is still explicit-proxy ingress, not transparent routing / subnet routing / full gateway mode yet

## 8. Temporary large-file distribution helper for `host185` NapCat bootstrap (2026-04-12)
Confirmed on 2026-04-12:
- purpose: serve `/root/napcat-transfer/napcat.tar` to `self-server-44005` during NapCat image bootstrap
- initial ad-hoc Python `http.server` source on `:18081` worked for single-stream transfer but did not support the Range behavior needed for efficient `aria2` multi-connection downloading
- stable final shape moved the tarball to `/srv/napcat-transfer/napcat.tar` and served it via:
  - container: `napcat-http-nginx`
  - image: `nginx:alpine`
  - published port: `18082 -> 80`
- validated behavior from `self-server-44005`:
  - `HEAD /napcat.tar` -> `200 OK`
  - `Range: bytes=0-1023` -> `206 Partial Content`
  - `Accept-Ranges: bytes`

Operational implication:
- for future large one-off transfers from `ali-cloud` to domestic hosts, prefer a proper static file server with Range support (for example `nginx`) over Python `http.server` when `aria2` multi-connection resume/splitting is desired.

## 9. zcode2api (retired mistaken first placement)
Confirmed on 2026-06-22:
- upstream: `https://github.com/liu5269/zcode2api`
- initial deployment root: `/opt/zcode2api`
- initial runtime shape: manually maintained Docker Compose deployment outside 1Panel
- initial container name: `zcode2api`
- initial public port mapping: `18084/tcp -> container 3000`
- this placement was corrected the same day: the live source now runs on `oracle-proxy:/root/containers/zcode2api` with origin `127.0.0.1:18770`, public entry `https://zcode.zhangxuemin.work`, and HK edge `https://zcode-cn.zhangxuemin.work`
- the ali-cloud container was stopped on 2026-06-22 after migration; do not route zcode2api traffic through `ali-cloud`

Access control:
- admin password was generated at deployment time and delivered to the user out-of-band in the chat result
- gateway API key was generated at deployment time, stored in the app SQLite settings, and delivered to the user out-of-band in the chat result
- login page supports `?token=<admin-key>` one-click admin login as of 2026-06-22; the page verifies the token through `/admin/api/verify`, stores it through the existing frontend `adminKey` localStorage helper, and redirects with `location.replace` to remove the token from the visible URL
- this one-click login mode is intended for trusted/private automation links only because query-string tokens may still appear in browser history, reverse-proxy access logs, and upstream request logs
- do not commit these keys into `infra/`; retrieve/reset via the on-host app settings/admin flow if needed

Build/deploy notes:
- the first BuildKit attempt did not use the host's Docker proxy and failed against Docker Hub metadata
- the successful initial ali-cloud build used legacy Docker builder with `--network host` and the host-local HTTP proxy exposed by `sing-box-gateway` on `127.0.0.1:2081`
- this host should not be used as the zcode2api origin for the user's dual-entry topology; keep HK as edge-only and Oracle as business source

Validation before retirement on 2026-06-22:
- local `GET /admin/api/status` with the admin bearer key returned status JSON with `gateway_key_set: true`
- unauthenticated local/public `GET /v1/models` returned `401`
- authenticated local/public `GET /v1/models` returned the built-in GLM model list
- after migration, `ali-cloud` is no longer part of the live validation path

Operational commands for historical inspection only:
- `cd /opt/zcode2api && /usr/bin/docker-compose ps`
- `cd /opt/zcode2api && /usr/bin/docker-compose logs zcode2api`
- do not restart this container unless intentionally rolling back from the Oracle deployment

## Next operational step
- inspect 1Panel status/routes/config further
- inspect EasyImages compose and health model
- inspect camoufox-remote deployment wrapper and intended consumers
- later decide whether to keep explicit-proxy ingress only, or evolve this host toward transparent/TUN/subnet-style gateway behavior
