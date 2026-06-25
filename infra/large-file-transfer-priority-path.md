# Large-file transfer priority path

Updated: 2026-05-25

## Decision

For foreign/Oracle -> domestic `self-server` large-file movement, the default priority path is:

```text
foreign/Oracle source serves file temporarily
self-server pulls it directly with proxy variables unset
curl resume enabled via HTTP Range / -C -
SHA256 verification
cleanup on both sides
```

This is now the preferred operational path unless a future test proves another route faster or more reliable.

## Why this is the priority path

Measured on 2026-05-25:

| Path | Result | Interpretation |
|---|---:|---|
| `self-server` no-proxy pull from `oracle-proxy` | ~`6.9–9.6 MiB/s` | Best measured path |
| `self-server` default proxy env pull from Oracle | ~`0.2–0.4 MiB/s` | Avoid |
| Oracle upload through existing `ali-cloud` HTTP proxy to domestic dufs | ~`0.4 MiB/s`, one 64 MiB test ended `502` | Avoid for bulk transfer |
| `self-server` no-proxy pull from `hk-relay` dufs | ~`1.0–1.3 MiB/s`, resumable | Functional fallback, not default |
| Oracle direct to `self-server` service port | timeout | Not usable in current topology |

The main discriminant is directionality:

- Oracle/foreign -> domestic inbound often fails or is forced through slow proxy paths.
- Domestic `self-server` -> Oracle/foreign outbound direct pull works substantially better when proxy variables are disabled.

## Standard workflow

### 1. On the foreign/Oracle source, prepare file and checksum

```bash
cd /path/to/source-dir
sha256sum big-file > big-file.sha256
```

### 2. Start an authenticated temporary file source

Preferred helper on Oracle/foreign hosts where installed:

```bash
openclaw-transfer-serve-dufs.sh /path/to/source-dir 18080
```

The helper prints:

- auth credential for this run
- source URL
- receiver command example

Do **not** leave this running after the transfer completes.

If the helper is unavailable, a temporary Python HTTP server is acceptable for low-risk private material only, but it has no auth and is not preferred:

```bash
cd /path/to/source-dir
python3 -m http.server 18080
```

### 3. On `self-server`, pull with proxy variables unset and resume enabled

Preferred helper:

```bash
openclaw-transfer-pull-no-proxy.sh \
  'http://<foreign-ip>:18080/big-file' \
  '/target/path/big-file' \
  '<expected-sha256>' \
  '<user:pass>'
```

Raw equivalent:

```bash
env -u http_proxy -u https_proxy -u all_proxy \
    -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY \
    curl -fL -C - -u '<user:pass>' \
    -o '/target/path/big-file' \
    'http://<foreign-ip>:18080/big-file'

sha256sum /target/path/big-file
```

### 4. Cleanup

After checksum verification:

- stop the temporary source service on Oracle/foreign side
- remove temporary staging files if no longer needed
- remove partial/failed files on `self-server`

## Installed helper scripts

Repo copies:

```text
infra/scripts/openclaw-transfer-serve-dufs.sh
infra/scripts/openclaw-transfer-pull-no-proxy.sh
```

Host installs as of 2026-05-25:

```text
oracle-proxy:/usr/local/sbin/openclaw-transfer-serve-dufs.sh
self-server:/usr/local/sbin/openclaw-transfer-pull-no-proxy.sh
```

Also installed on `oracle-proxy`:

```text
/usr/local/bin/dufs 0.46.0
```

The helper scripts are intentionally not long-running services. They codify the tested path without permanently exposing a new public file-transfer endpoint.

## Fallbacks

### Fallback A: hk-relay dufs

Use only when Oracle/source serving is unavailable or when convenience matters more than speed.

Measured:

```text
self-server no-proxy pull from hk-relay: ~1.0–1.3 MiB/s
```

Useful property:

- HTTP Range resume works (`curl -C -` returned `206` and completed a 512 MiB file with SHA256 verified)

Caution:

- `hk-relay` has a bidirectional monthly traffic cap of `800G`; do not silently burn it for large recurring transfers.

### Fallback B: SFTPGo / formal file service

Consider only if this becomes a persistent multi-user/audited workflow. It is operationally heavier than the tested helper-based dufs path.

## Anti-patterns

Do not use these as the default bulk path:

```text
Oracle -> self-server public service port
Oracle -> ali-cloud HTTP proxy -> self-server
self-server pull while inheriting http_proxy/all_proxy
```

Those paths were either unreachable or much slower in testing.

## Related reports

- `hosts/self-server/oracle-transfer-test-2026-05-25.md`
- `hosts/self-server/dufs-relay-test-2026-05-25.md`
- `hosts/hk-relay/self-server-pull-test-2026-05-25.md`
- `large-file-transfer-relay-options-2026-05-25.md`


## Helper smoke verification (2026-05-25)

After installing the helper scripts, a 1 MiB smoke transfer was completed through the intended path:

```text
oracle-proxy dufs helper on :18080
self-server no-proxy pull helper
sha256 OK
```

Observed pull result:

```text
http=200 ip=158.178.236.241 total=0.775 speed=1352933 B/s size=1048576
sha256 OK: 9bb3197ca466e30251cc018334bb9c20b61791afd69b0f1d5daeda9c7a0f48bc
```

The temporary dufs process and smoke-test files were removed after verification. No long-running file-transfer service was left on `oracle-proxy`.
