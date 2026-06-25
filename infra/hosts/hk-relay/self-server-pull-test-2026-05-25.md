# hk-relay -> self-server pull test — 2026-05-25 16:12 GMT+8

## Scope

Test whether `hk-relay` is a good large-file staging relay for `self-server` to pull from China-side without using the domestic host's default proxy environment.

This follows two prior findings:

- `self-server` no-proxy pull from `oracle-proxy` reached about `6.9–9.6 MiB/s`.
- `oracle-proxy` could not directly reach a temporary `self-server:30019` dufs service, and proxy-shaped uploads via `ali-cloud` were slow / unreliable.

## Test shape

Existing `hk-relay` service used:

- service: `dufs-drop.service`
- public direct dufs port: `154.86.30.10:8088`
- Caddy/domain path was intentionally bypassed; this tested raw HK dufs over HTTP with dufs authentication.

Temporary test files were created under:

```text
/srv/drop/_transfer-test-20260525/
```

Files:

```text
test512.bin  512 MiB  sha256 9acca8e8c22201155389f65abbf6bc9723edc7384ead80503839f49dcc56d767
test2g.bin    2 GiB   sha256 a7c744c13cc101ed66c29f672f92455547889cc586ce6d44fe76ae824958ea51
```

The `self-server` command shape explicitly unset proxy variables:

```bash
env -u http_proxy -u https_proxy -u all_proxy \
    -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY \
    curl -fL -u '<dufs-auth>' -o <file> \
    http://154.86.30.10:8088/_transfer-test-20260525/<file>
```

Credentials are intentionally not stored here.

## 512 MiB complete transfer

Initial 512 MiB pull was capped at `--max-time 300` and timed out before completion:

```text
http=200 ip=154.86.30.10 total=300.000 speed=1318039 B/s size=395411152
curl: operation timed out after 300 seconds with 395411152 / 536870912 bytes received
```

The partial file was then resumed with HTTP Range / `curl -C -`:

```text
resume_http=206 ip=154.86.30.10 total=124.623 speed=1135097 B/s size=141459760
sha256: 9acca8e8c22201155389f65abbf6bc9723edc7384ead80503839f49dcc56d767
```

Interpretation:

- resume works against the HK dufs endpoint
- final hash matched
- effective end-to-end speed was roughly `1.1–1.3 MiB/s`, with visible fluctuation
- full 512 MiB required about `424.6 seconds` across initial + resumed transfers, i.e. roughly `1.2 MiB/s`

## 2 GiB capped sample

A 2 GiB pull was intentionally capped at `--max-time 180` to avoid spending unnecessary HK monthly transfer budget once speed was clearly below the Oracle direct-pull baseline.

Result:

```text
sample_http=200 ip=154.86.30.10 total=180.000 speed=1005702 B/s size=181026064
partial file size on disk: 173 MiB
curl: operation timed out after 180 seconds with 181026064 / 2147483648 bytes received
```

Projected full 2 GiB time at sampled speed: roughly `35–36 minutes`.

## Cleanup

Removed after test:

- `self-server:/tmp/hk-transfer-test`
- `hk-relay:/srv/drop/_transfer-test-20260525`

Post-cleanup disk snapshots:

```text
self-server root: 50G total / 2.6G used / 48G free
hk-relay root:    49G total / 4.9G used / 44G free
```

`vnstat` after the test showed current-day `hk-relay` traffic at about:

```text
rx 780.34 MiB / tx 1.27 GiB / total 2.03 GiB
```

## Conclusion

`hk-relay -> self-server` pull is functional and resumable, but **not fast enough to be the preferred large-file relay path** for this specific Oracle-to-domestic use case.

Compared with previous direct no-proxy Oracle pull:

```text
self-server no-proxy pull from oracle-proxy: ~6.9–9.6 MiB/s
self-server no-proxy pull from hk-relay:     ~1.0–1.3 MiB/s
```

That makes HK staging roughly `5–9x` slower than direct Oracle serving in the measured environment.

Recommended stance:

- keep `hk-relay` dufs as a functional fallback / convenience drop
- do not make HK the default bulk-transfer bridge for Oracle -> `self-server`
- prefer source-side serving on the Oracle/foreign host and `self-server` no-proxy pull
- use `curl -C -` / Range resume for interruption safety

## Practical operator pattern retained

For Oracle/foreign -> `self-server` large transfer:

1. create a temporary HTTP/dufs/SFTP source on the foreign host
2. from `self-server`, pull with proxy variables unset
3. use `curl -C -` for resume if needed
4. verify SHA256
5. clean up source and destination temporary files
