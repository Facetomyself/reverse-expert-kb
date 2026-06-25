# dufs relay test on self-server — 2026-05-25 15:55 GMT+8

## Scope

Temporary validation of `dufs` as a domestic file-drop service for foreign/Oracle -> domestic large-file transfer.

Target:

- domestic host: `self-server` / `211.144.221.229:44001` / hostname `181`
- temporary public port: `30019/tcp`
- temporary data dir: `/srv/filedrop-dufs`
- temporary service: `dufs-filedrop-test.service`

The service was removed after the test.

## Setup

`self-server` could not download the dufs GitHub release directly when proxy variables were unset; GitHub timed out from the domestic host.

Workaround:

- downloaded `dufs-v0.46.0-x86_64-unknown-linux-musl.tar.gz` from the OpenClaw side
- verified release archive SHA256:

```text
817769f726613194bcff9d0e3e481eaccc86ac11208857614f36a8c02f410977
```

- copied it to `self-server`
- installed `/usr/local/bin/dufs`
- confirmed `dufs 0.46.0`

Temporary service shape:

```text
dufs /srv/filedrop-dufs --bind 0.0.0.0 --port 30019 --auth drop:<random>@/:rw --allow-upload --allow-hash --log-file /var/log/dufs-filedrop-test.log
```

Firewall opened `30019/tcp` only for the temporary test.

## Reachability

- `self-server -> 127.0.0.1:30019`: OK, HTTP 200
- `ali-cloud -> 211.144.221.229:30019`: OK, HTTP 200
- `oracle-proxy -> 211.144.221.229:30019`: timed out

Interpretation:

- The dufs service and domestic public forwarding are usable from domestic/ali-cloud side.
- The shared domestic IP/port is not directly reachable from the tested Oracle source.
- This matches earlier direct SSH/TCP failures from Oracle to `self-server` public ports.

## Upload tests

### ali-cloud -> self-server dufs, small file

Small authenticated `PUT` from `ali-cloud` to `self-server:30019` succeeded:

```text
http=201 total=0.016358 speed_upload=305
```

`self-server` log:

```text
106.15.239.221 "PUT /hello.txt" 201
```

### oracle-proxy -> self-server dufs direct

Direct Oracle upload could not connect because Oracle -> `211.144.221.229:30019` timed out.

### oracle-proxy -> self-server dufs via ali-cloud HTTP proxy

Oracle upload through the existing `ali-cloud` HTTP proxy path reached only around the same slow rate previously observed for proxy-shaped bulk movement:

- after ~58 seconds, only about `24.3 MiB` of a `512 MiB` file had uploaded
- average stabilized around `~0.42 MiB/s`
- projected completion was around `20 minutes`

This run was intentionally killed as low-signal / not production-worthy.

A previous 64 MiB proxy upload attempt sent the request body to the proxy at a bursty apparent rate but ended with HTTP `502`, and no file was created on dufs. That indicates this existing proxy path is not reliable as an upload relay for dufs.

## Cleanup

Removed after test:

- `dufs-filedrop-test.service`
- `/root/.dufs-filedrop-test-auth`
- `/srv/filedrop-dufs`
- `/tmp/dufs-fetch`
- temporary upload/download files
- `30019/tcp` firewalld opening

Post-cleanup public port set returned to:

```text
30012/tcp 30011/tcp 30013/tcp 30014/tcp 30015/tcp 30016/tcp 30017/tcp 30018/tcp
```

No `:30019` listener remained.

## Conclusion

`dufs` itself is fine as a lightweight authenticated file-drop service, but **placing it on `self-server` does not solve Oracle -> domestic transfer for this network shape** because the Oracle source cannot directly reach the domestic shared-IP service port.

The existing `ali-cloud` HTTP proxy path is also not a good large-file upload relay:

- slow: roughly `0.4 MiB/s`
- one 64 MiB upload attempt ended in `502` with no resulting file

For the current topology, the better-performing direction remains:

1. expose/serve the file on the foreign/Oracle side, or use an overseas relay that domestic can reach
2. from `self-server`, pull the file with proxy variables unset
3. verify SHA256

Previous direct no-proxy pull from `self-server` to `oracle-proxy` reached roughly `6.9–9.6 MiB/s`, which is an order of magnitude better than proxy-shaped uploads.

## Recommended next design

Do not use `self-server`-hosted dufs as the primary Oracle->domestic ingress unless Oracle reachability changes.

Prefer one of these:

1. **Oracle-side dufs/SFTPGo + domestic no-proxy pull**
   - Most aligned with measured fast path.
   - Domestic machine initiates connection outward, avoiding the inbound reachability problem.

2. **hk-relay as a bridge only if domestic can pull from HK quickly**
   - Needs a separate HK -> self-server no-proxy speed test.
   - Could support staged transfer: Oracle -> HK, self-server -> HK.

3. **SFTPGo/dufs on ali-cloud only as an explicitly measured relay**
   - Current ali-cloud proxy path is bad, but a native file service on ali-cloud may be different and should be tested separately before adoption.
