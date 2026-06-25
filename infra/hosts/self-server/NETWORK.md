# self-server / NETWORK

## Public ingress model
Same public IP hosts two separate SSH-reachable targets behind different forwarded ports:

- `211.144.221.229:44001` -> machine currently observed as hostname `181`
- `211.144.221.229:44005` -> machine currently observed as hostname `host185`

Preferred operator access from OpenClaw is via `ali-cloud` transit rather than direct access from the current OpenClaw host. Treat this as a durable routing rule for Oracle/OpenClaw-side administration of domestic servers and FRP-forwarded home endpoints.

## User-confirmed port constraints (2026-04-04)
Because public-IP resources are limited on this virtualization side, each machine only has a small TCP allocation:

### Target `:44001` (`181`)
Allowed public TCP range:
- `30011-30025`

Observed listening TCP ports during same-day read-only inspection:
- `22/tcp` - sshd
- `30011/tcp` - `1panel-core`
- `30012/tcp` - `frps`
- `30013/tcp` - `frps`

Operational note:
- The observed listeners fit inside the user-confirmed allowed allocation.
- Intended steady-state role after 2026-04-04 cleanup: keep this VM as the `1Panel + FRPS` box for this shared-IP pair.
- 2026-04-13 live validation after the FRP migration confirmed the active published payload listeners expanded to:
  - `30014/tcp` -> `home-macmini` ComfyUI
  - `30015/tcp` -> `home-nas` DSM HTTPS
  - `30016/tcp` -> `home-nas` Synology Drive
  - `30017/tcp` -> temporary `home-macmini` SSH maintenance relay
  - `30018/tcp` -> temporary `home-nas` SSH maintenance relay
- External validation from `ali-cloud` confirmed:
  - `http://211.144.221.229:30014/` served ComfyUI
  - `https://211.144.221.229:30015/` returned `HTTP/2 200`
  - `http://211.144.221.229:30015/` returned `400 Bad Request`, which is expected because the FRP target is DSM HTTPS on `5001`
  - `211.144.221.229:30017` exposed the `home-macmini` SSH banner once the corrected `frpc.toml` was launched on the Mac mini
  - `211.144.221.229:30018` became the validated `home-nas` maintenance SSH relay used from Oracle/OpenClaw via `ali-cloud`
- Final same-day outbound model is explicit rather than transparent: this VM now keeps a local `dnsmasq` listener on `127.0.0.1:53`, forwards DNS to `106.15.239.221#1053`, and uses `ali-cloud` authenticated proxy ingress on `:2081` / `:2080` for shell and Docker egress.

### Target `:44005` (`host185`)
Allowed public TCP range:
- `30001-30010`

Important path-shape note confirmed again on 2026-04-16:
- the VM itself only has private address `10.10.21.185/24` on `ens192`
- it does **not** own the public address directly inside the guest
- therefore public reachability of `211.144.221.229:30001-30010` depends on an upstream shared-IP forwarding layer outside the VM, not only on guest Docker/firewalld state

Observed listening TCP ports during initial same-day read-only inspection:
- `22/tcp` - sshd
- `5837/tcp` - sshd additional listener
- `30008/tcp` - `1panel-core`
- `9090/tcp` - `mihomo`
- `1053/tcp` - `mihomo`
- `111/tcp` - rpcbind
- `25/tcp` loopback-only / localhost-bound by postfix
- `7890/tcp` loopback-only by `mihomo`

Post-cleanup state observed later on 2026-04-04:
- `22/tcp` - sshd
- `30008/tcp` - `1panel-core`

Additional deployment observed on 2026-04-06:
- `30001/tcp` - `prompt-optimizer-studio` (Docker Compose, self-hosted Next.js app)

Read-only validation on 2026-04-08:
- actual listening ports on the VM were `22/tcp`, `30001/tcp`, and `30008/tcp`
- `firewalld` was active and already allowed `30003/tcp`, `30004/tcp`, `30005/tcp`, `30006/tcp`, `30007/tcp`, `30009/tcp`, and `30010/tcp`
- a stale `firewalld` forward-port still existed: `30007/tcp -> 9090/tcp`; this collides with the cleaner future FRP use of the `30001-30010` budget and should be removed when the FRPS role is actually deployed

Live validation on 2026-04-11 after AstrBot deployment:
- host listeners included `30005/tcp`, `30006/tcp`, `30007/tcp`, `10000/tcp`, `10001/tcp`, and `10002/tcp` via Docker proxy for the 1Panel-managed `astrbot` container
- confirmed container/host mapping:
  - `30007/tcp` -> AstrBot WebUI (`6185/tcp` in container)
  - `10000/tcp` -> `6194/tcp`
  - `10001/tcp` -> `6195/tcp`
  - `30006/tcp` -> `6196/tcp`
  - `30005/tcp` -> `6199/tcp`
  - `10002/tcp` -> `11451/tcp`
- host-local verification:
  - `curl http://127.0.0.1:30007/` returned `200 OK`
  - `curl http://127.0.0.1:6185/` failed with connection refused because `6185` is not bound on the host
- transit-side verification from `ali-cloud`:
  - public `211.144.221.229:30007` responded `200 OK`
  - public `211.144.221.229:30005` and `:30006` still returned connection refused at probe time, so do not assume all AstrBot auxiliary ports are currently reachable externally just because Docker is listening locally

Operational note:
- `30008/tcp`, `30001/tcp`, and now `30007/tcp` fit inside the user-confirmed allowed allocation.
- historical listeners `5837`, `9090`, `1053`, and `111` were removed from active service during the same-day cleanup pass to bring this VM closer to a true 1Panel-only shape, but the later 2026-04-08 firewall check showed residual allow/forward rules still remain and should be normalized during FRPS rollout.
- 2026-04-13 migration decision moved the active FRPS relay role off `:44005` and back onto `:44001`, so this VM should no longer be treated as the long-term FRP relay host.
- Effective application-focused public TCP allocation after the later EasyAI bring-up is now intended to be:
  - `30001/tcp` -> `NapCat WebUI`
  - `30002/tcp` -> `ruyipage 151-ruyi` static release mirror
  - `30003/tcp` -> free/unassigned after EasyAI removal
  - `30004/tcp` -> free/unassigned after EasyAI removal
  - `30005/tcp` -> `AstrBot` / QQ personal / OneBot v11 host publish
  - `30006/tcp` -> `AstrBot` auxiliary publish
  - `30007/tcp` -> `AstrBot WebUI`
  - `30008/tcp` -> `1panel-core`
  - `30009/tcp` -> free/unassigned after EasyAI removal
  - `30010/tcp` -> `ChatGpt Image Studio`
- Historical note:
  - `:44005` did temporarily host the live FRPS relay and business-service mappings on 2026-04-08 through 2026-04-12
  - those mappings were migrated on 2026-04-13 to the cleaner `:44001` FRPS layout using `30012` control and payload ports beginning at `30014`
- Protocol caution:
  - the documented forwarding allocation for this VM is currently TCP-only; do not assume extra UDP budget for FRP features such as KCP/QUIC without separate confirmation
- Live validation on 2026-04-16 after EasyAI bring-up and runtime cleanup:
  - Docker now binds host ports `30002/tcp`, `30003/tcp`, `30004/tcp`, and `30009/tcp` for the EasyAI stack under `/opt/easyai`
  - concrete runtime mismatch fixes were applied:
    - `ws-gateway`: keep host `30004`, but force container-internal `CONFIG_WS_PORT=3002`
    - `easyai-asg`: keep host `30009`, but force container-internal `ASG_PORT=3003`
  - transit-side probe from `ali-cloud` confirmed:
    - `30002/tcp` reachable and returning `302 -> /home`
    - `30003/tcp` reachable and returning `200 OK`
    - `30004/tcp` reachable and returning `426 Upgrade Required` on a plain HTTP probe
    - `30009/tcp` reachable and returning `200 OK` from `/health`
  - practical interpretation:
    - the earlier `30004` failure was caused by local container-port/config mismatch, not a durable upstream forwarding defect
    - `30004` is now externally reachable but should still be treated as a real WebSocket endpoint, not a normal HTTP page
  - same-day public-port snapshot from `ali-cloud` against the shared public IP after the fix showed the currently effective external-open subset on `:44005` is at least:
    - open: `30001`, `30002`, `30003`, `30004`, `30005`, `30007`, `30008`, `30009`
    - closed/refused: `30006`, `30010`
- Live validation on 2026-04-24 after ChatGpt Image Studio bring-up:
  - Docker now binds `30010/tcp -> 7000/tcp` for container `chatgpt-image-studio` from `/opt/chatgpt-image-studio`
  - host-local `curl http://127.0.0.1:30010/health` returned `{"status":"ok"}`
  - transit-side validation from `ali-cloud` confirmed public `211.144.221.229:30010/health` returned `200 OK`
  - additional ali-cloud-side functional probes also confirmed:
    - `POST /auth/login` succeeds with the configured app auth key
    - `GET /v1/models` succeeds with the configured app API key
  - local runtime validation on `host185` confirmed the service can talk to the oracle-proxy CPA stack and the first deployment ended with `26` synced local accounts available to the UI/API
  - practical interpretation:
    - `30010/tcp` is no longer a spare FRPS-era leftover; it is now an actively assigned application slot on `:44005`

- Live validation on 2026-06-08 after EasyAI removal and ruyipage deployment:
  - EasyAI stack under `/opt/easyai` was removed without archive by user request
  - former EasyAI listeners were confirmed freed: `30003`, `30004`, `30009`, plus helper ports `8080`, `8888`, `8000`, `5672`, `15672`, `27017`, and `3004`
  - `30002/tcp` is now assigned to `ruyipage-151.service` (`python3 -m http.server`) serving `/opt/ruyipage-151`
  - current effective application subset on `:44005` observed after the change:
    - `30001` -> `NapCat WebUI`
    - `30002` -> `ruyipage 151-ruyi` static release mirror
    - `30003` -> `proxy_pool` API (`/opt/proxy_pool`, Docker Compose; added 2026-06-16 after disabling temporary `textdrop.service`)
    - `30004` -> free/unassigned
    - `30005` -> `AstrBot` / QQ personal / OneBot v11 host publish
    - `30006` -> `AstrBot` auxiliary publish
    - `30007` -> `AstrBot WebUI`
    - `30008` -> `1Panel`
    - `30009` -> free/unassigned
    - `30010` -> `ChatGpt Image Studio`
  - transit-side probe from `ali-cloud` confirmed `http://211.144.221.229:30002/` and the Linux package URL return `200 OK`; package `Content-Length` was `103125296`
  - cleanup follow-up: user explicitly confirmed at 2026-06-08 14:41 GMT+8 that `crawl4ai_redis_data`, `linovel_scrapy_redis_data`, and `mailu_api_redis_data` should also be cleaned; follow-up checks confirmed all three Docker volumes are removed
- Live validation on 2026-06-16 after proxy_pool deployment:
  - Docker Compose project under `/opt/proxy_pool` now runs `proxy_pool_server`, `proxy_pool_scheduler`, and internal Redis container `proxy_pool_redis`
  - published mapping is `30003/tcp -> proxy_pool_server:5010`
  - host-local `GET http://127.0.0.1:30003/` returned the ProxyPool API index
  - host-local and ali-cloud transit-side `GET http://211.144.221.229:30003/count/` returned JSON successfully
  - machine health after deployment: root filesystem about `25%` used, memory headroom about `13G` available, Docker services including NapCat/AstrBot/ChatGpt Image Studio restarted and were running after a Docker daemon restart used to clear a stuck first-attempt `proxy_pool` container

- Live validation on 2026-06-17 after AstrBot upgrade:
  - `astrbot` now runs image `soulter/astrbot:v4.26.0-beta.4` with the existing port mappings preserved.
  - host-local `GET http://127.0.0.1:30007/` returned `200`; public transit-side `GET http://211.144.221.229:30007/` from `ali-cloud` returned `200`.
  - `HEAD /` returned `405` on the upgraded WebUI, so future health checks should use `GET` rather than assuming HEAD support.
- Firewall caution:
  - do not broadly open `30001-30010` just because the VM owns that range; only keep the ports that are actually assigned to running services
  - after the ChatGpt Image Studio reassignment, `30010` should be treated as live application exposure rather than cleanup residue
- Final outbound model remains explicit rather than transparent: this VM keeps a local `dnsmasq` listener on `127.0.0.1:53`, forwards DNS to `106.15.239.221#1053`, and uses `ali-cloud` authenticated proxy ingress on `:2081` / `:2080` for shell and Docker egress; the short-lived transparent TUN experiment was removed after proving unstable for general HTTPS traffic.


## Oracle -> self-server bulk transfer note (2026-05-25)

A transfer test from `oracle-proxy` to `self-server:44001` showed that the domestic host's default shell proxy environment is bad for this direction of large-file movement.

Summary:

- `oracle-proxy` direct SSH/TCP to `self-server` public SSH ports timed out, so the practical test shape was HTTP pull from `self-server`.
- A 512 MiB attempt with the normal shell proxy environment was interrupted after ~96s at only ~37.7 MiB transferred (~394 KiB/s).
- 64 MiB direct no-proxy pull from `self-server` to `oracle-proxy` completed successfully at ~6.9–9.6 MiB/s with SHA256 verified.
- Temporarily switching `ali-cloud` selector to `hk-http` did not help this direction; the proxied path still sat around ~380 KiB/s and was interrupted.

Operational rule:

For deliberate bulk pulls from Oracle hosts to `self-server`, unset proxy variables for the single transfer or add the source Oracle IP to `NO_PROXY`. Do not rely on the default `http_proxy` / `all_proxy` shell environment.

Detailed report: `oracle-transfer-test-2026-05-25.md`.


## dufs domestic file-drop test note (2026-05-25)

A temporary authenticated `dufs` service was tested on `self-server:30019` and fully removed after the test.

Result:

- `self-server -> 127.0.0.1:30019`: OK
- `ali-cloud -> 211.144.221.229:30019`: OK
- `oracle-proxy -> 211.144.221.229:30019`: timed out
- `oracle-proxy -> ali-cloud HTTP proxy -> self-server:30019`: not suitable for large uploads; one 64 MiB attempt ended with HTTP `502` and no file, and a 512 MiB attempt stabilized around `~0.4 MiB/s` before being killed.

Interpretation:

- `dufs` itself is usable, but placing the file-drop on `self-server` does not solve Oracle -> domestic transfer because this Oracle source cannot directly reach the shared-IP domestic service port.
- The measured good path remains foreign-side serving plus `self-server` no-proxy pull.

Detailed report: `dufs-relay-test-2026-05-25.md`.


## hk-relay pull comparison note (2026-05-25)

A no-proxy pull from `self-server` to `hk-relay` dufs (`154.86.30.10:8088`) was tested as a possible Oracle -> HK -> domestic staging path.

Result:

- 512 MiB completed with SHA256 verified after one timeout + HTTP Range resume.
- Effective rate was roughly `1.1–1.3 MiB/s`.
- 2 GiB capped sample averaged about `1.0 MiB/s`, projecting roughly `35–36 minutes` for a full 2 GiB file.

Interpretation:

- HK staging works and is resumable, but it is significantly slower than direct `self-server` no-proxy pull from `oracle-proxy` (`~6.9–9.6 MiB/s`).
- Prefer foreign/Oracle-side serving plus `self-server` no-proxy pull for bulk movement; keep HK dufs as fallback/convenience, not default bulk bridge.


## Priority large-file transfer receiver role (2026-05-25)

This host is now prepared as the domestic receiver for the preferred large-file transfer path.

Installed helper:

```text
/usr/local/sbin/openclaw-transfer-pull-no-proxy.sh
```

Operational stance:

- receive large files by pulling from the foreign/Oracle source
- always unset `http_proxy` / `https_proxy` / `all_proxy` for the transfer
- use HTTP Range resume (`curl -C -`) and SHA256 verification
- avoid inbound Oracle -> self-server service-port designs unless reachability changes

Canonical runbook: `../../large-file-transfer-priority-path.md`.
