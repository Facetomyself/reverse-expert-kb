# Oracle -> self-server transfer test — 2026-05-25 14:58 GMT+8

## Scope

User requested a large-file transfer test from an Oracle server to the domestic `self-server`.

Target used: `self-server` / `211.144.221.229:44001` / hostname `181`.

Source used: `oracle-proxy` / `158.178.236.241`.

## Method

Because `oracle-proxy` could not directly SSH to `self-server` and did not have the local OpenClaw `ali-cloud` jump-host aliases/keys, the test used a pull shape:

1. Generate a temporary file on `oracle-proxy`.
2. Serve it via a temporary Python HTTP server on `oracle-proxy:18080`.
3. Download it from `self-server` into `/tmp/oracle-to-self-test/`.
4. Verify SHA256 when the transfer completed.
5. Remove temporary files and stop the temporary HTTP server.

No permanent service was left running.

## Pre-checks

- `oracle-proxy` direct TCP to `211.144.221.229:44001` and `:44005` timed out.
- OpenClaw could access `self-server` reliably through `ProxyJump ali-cloud`.
- `self-server` had proxy environment variables pointing at `ali-cloud:2081` / `:2080`.

## Initial 512 MiB direct-through-environment attempt

Initial attempt: `512 MiB`, downloaded by `self-server` with its normal shell proxy environment still active.

Observation:

- after ~96 seconds it had transferred only about `37.7 MiB`
- average speed was about `394 KiB/s`
- projected total time was roughly `22 minutes`

This run was intentionally interrupted to avoid waiting ~20+ minutes for a low-signal result.

Interpretation:

- The default environment/proxy path was bad for Oracle -> domestic large-file transfer.
- This looked consistent with the `self-server` shell proxy variables forcing the transfer through `ali-cloud`'s current selector/default egress rather than using the direct domestic path.

## 64 MiB comparison tests

Source file:

```text
size: 64 MiB / 67108864 bytes
sha256: 3b6a07d0d404fab4e23b6d34bc6696a6a312dd92821332385e5af7c01c421351
```

### A. Direct no-proxy path

Command shape: run curl on `self-server` with proxy environment unset for the single transfer.

Result 1:

```text
http=200 total=9.229s speed=7271688 B/s size=67108864
sha256 OK
```

Result 2 after cleanup/restart confirmation:

```text
http=200 total=6.677s speed=10050666 B/s size=67108864
sha256 OK
```

Effective throughput:

- ~6.9 MiB/s on the first direct run
- ~9.6 MiB/s on the second direct run

### B. Normal shell proxy environment path

Command shape: normal curl on `self-server`, inheriting `http_proxy` / `https_proxy` / `all_proxy` pointing at `ali-cloud`.

Observed during interrupted 64 MiB run:

- one visible progress burst reached normal speed briefly, then another connection/path progressed at roughly `220–230 KiB/s`
- run was interrupted because the slow path was clearly worse and would take several minutes

### C. Ali selector temporarily switched to `hk-http`

Action:

- saved current selector: `oracle-egress`
- switched `ali-cloud-proxy-select hk-http`
- attempted the 64 MiB transfer through normal proxy environment
- restored selector to `oracle-egress`

Observation:

- transfer progressed around `380 KiB/s`
- projected completion ~2m50s
- run was interrupted once it was clearly worse than direct no-proxy

## Cleanup verification

After tests:

```text
ali-cloud selector: oracle-egress
oracle-proxy temporary directory: removed
self-server temporary directory: removed
oracle-proxy temporary HTTP server: stopped
```

## Conclusion

For Oracle -> `self-server` large-file movement, **do not use the domestic host's default shell proxy environment**. It can force the transfer through a poor proxy path and reduce throughput by an order of magnitude or more.

The direct no-proxy pull from `self-server` to `oracle-proxy` was much better:

- direct no-proxy: ~6.9–9.6 MiB/s
- proxy/default env path: initially ~0.39 MiB/s for the 512 MiB attempt
- proxy via temporary `hk-http` selector: ~0.37 MiB/s in the interrupted comparison

Recommended operational pattern:

```bash
env -u http_proxy -u https_proxy -u all_proxy \
    -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY \
    curl -L -o <target-file> http://<oracle-host>:<temporary-port>/<file>
```

Or add the relevant Oracle host/IPs to `NO_PROXY` for deliberate bulk transfers if this workflow becomes common.

## Caveats

- This test used `oracle-proxy` as the Oracle source and `self-server:44001` as the domestic target.
- It tested a pull model over temporary HTTP, not SSH push from Oracle.
- Because direct SSH from `oracle-proxy` to `self-server` timed out and Oracle-side jump-host aliases/keys were absent, HTTP pull was the cleanest low-impact method for this run.
