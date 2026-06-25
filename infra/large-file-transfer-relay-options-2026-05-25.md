# Large-file transfer relay options — 2026-05-25 15:17 GMT+8

## Question

Find reliable large-file transfer / relay options for moving files from foreign/Oracle machines to domestic machines.

This follows the `oracle-proxy -> self-server` test where:

- direct no-proxy HTTP pull from `self-server` to `oracle-proxy` reached about `6.9–9.6 MiB/s`
- the same transfer through `self-server`'s default proxy environment was only about `0.2–0.4 MiB/s`

## Sources checked

Search layer:

- Exa + Tavily searches around self-hosted large-file relay, resumable upload, SFTP/WebDAV/S3, croc/wormhole, Syncthing/Resilio, rsync/lftp/aria2.
- Grok source returned repeated `502` and was not used as evidence.

Primary project/docs pages fetched:

- rclone `serve sftp` docs
- sigoden/dufs README
- tus/tusd README
- schollz/croc README
- Syncthing FAQ
- SFTPGo docs/search results
- MinIO/S3 multipart references from search results

## Shortlist

### 1. dufs on the receiving domestic side

Fit: **best first experiment for this infra**.

Why:

- Already used on `hk-relay` for simple file ingress/egress.
- Single binary / container, low operational overhead.
- Supports static serving, upload, access control, WebDAV, HTTPS, hash query, and resumable/partial uploads/downloads according to the README and changelog results.
- Easy CLI workflows via `curl`.

Recommended shape:

- Run dufs on `self-server:44001` behind an assigned TCP port in the allowed `30011-30025` range, or run it only internally and reach it through SSH jump when needed.
- For foreign -> domestic transfer, push from Oracle to domestic dufs with proxy variables unset on the domestic side if doing pull, or with direct upload if the domestic port is reachable.
- Keep it credentialed and preferably path-scoped.

Caveat:

- For very large multi-GB uploads, test resume behavior under interruption before trusting it as the only path.

### 2. SFTPGo on domestic side

Fit: **best durable service if this becomes a recurring workflow with users/quotas/audit**.

Why:

- Mature managed file-transfer server.
- Supports SFTP, FTP/S, HTTP/S, WebDAV, users/permissions, storage backends including local FS and S3-compatible storage.
- Better long-term access control and audit posture than ad-hoc HTTP servers.

Recommended shape:

- Deploy on `self-server:44001` if a long-lived domestic file drop is wanted.
- Use SFTP/WebDAV clients from Oracle/foreign boxes.
- Keep a dedicated user with chroot/quota and restricted upload/download path.

Caveat:

- Heavier than dufs.
- Need to test large-file resume behavior with the exact client path; WebDAV clients vary.

### 3. rclone serve sftp / serve webdav

Fit: **good operator tool, less ideal as a permanent public service**.

Why:

- `rclone serve sftp` can expose a local/remote backend over SFTP and supports auth, checksums, stats, bandwidth limits, and socket activation.
- Very useful when the data source/sink is already an rclone remote.

Recommended shape:

- Use for temporary maintenance windows or wrapping cloud/object storage.
- Do not expose widely without a service wrapper, auth policy, and logs.

Caveat:

- rclone SFTP resume behavior depends on backend/client semantics; some forum results show resume surprises for certain backends.

### 4. tusd / tus protocol

Fit: **best if browser/web resumable uploads are the requirement**.

Why:

- tus is explicitly a resumable HTTP upload protocol.
- `tusd` is the official Go reference server.
- It can store locally, on GCS, or S3-compatible storage.
- Designed for interruption-resume semantics.

Recommended shape:

- Use if building a web upload/drop system or if non-technical users need browser-based resumable uploads.
- Pair with an authenticated frontend or tightly restricted endpoint.

Caveat:

- Less convenient than `curl/scp/rsync` for pure server-to-server operator flows unless a tus client is standardized.

### 5. MinIO / S3-compatible object storage

Fit: **good if you want a real object-storage relay and multipart uploads**.

Why:

- S3-compatible APIs have broad client support.
- Multipart upload/download is the standard shape for large objects.
- Tools like rclone, awscli, s5cmd can target it.

Recommended shape:

- Deploy MinIO/Garage only if this becomes a storage service, not just a transfer tool.
- Better suited when files should remain available after transfer.

Caveat:

- Heavier operational footprint and credential model.
- Multipart limits/part sizes matter.

### 6. croc / Magic Wormhole

Fit: **good ad-hoc human-to-human transfer, not best for persistent infra relay**.

Why:

- croc supports relay, end-to-end encryption, resume, cross-platform use, no port-forwarding.
- Magic Wormhole is well-regarded for safe one-off transfer and can use relay/transit servers.

Recommended shape:

- Keep as a toolbox option for occasional manual transfers between weird networks.
- Consider self-hosted relay only if ad-hoc cross-network human transfer is common.

Caveat:

- Less natural for automated recurring Oracle -> domestic server logistics.

### 7. Syncthing / Resilio-style sync

Fit: **good for continuous folder sync, not one-shot transfer relay**.

Why:

- Handles ongoing bidirectional or one-way sync semantics.
- Can survive intermittent connectivity.

Recommended shape:

- Use only if the desired product is “these directories stay synchronized.”

Caveat:

- More stateful than necessary for deliberate single bulk transfers.
- Initial sync and relay path behavior need testing.

## Recommendation for this infra

### Best immediate path

Use **dufs on `self-server:44001`** as the first domestic file drop experiment.

Why:

- Lowest complexity.
- Matches existing dufs usage on `hk-relay`.
- Supports the operations we need: upload/download/auth/WebDAV/resume/hash.
- Lets us test real Oracle -> domestic push/pull without designing a full storage platform.

Suggested deployment shape:

- allocate one `self-server:44001` port from `30011-30025` if available
- bind dufs to a dedicated data directory, e.g. `/srv/filedrop`
- require auth
- log transfers
- do not inherit the domestic host proxy env for local download/pull scripts
- provide explicit commands for:
  - Oracle pushes file to domestic dufs
  - domestic pulls file from Oracle no-proxy
  - checksum verification

### More durable second path

If dufs proves useful but too lightweight, move to **SFTPGo**.

Use SFTPGo when you want:

- named users
- per-user directories/quotas
- auditability
- SFTP/WebDAV/browser-ish access
- storage backend abstraction

### Avoid as primary for this problem

- Do not make `ali-cloud` proxy the default path for Oracle -> domestic bulk transfer; current tests show it can be much slower.
- Do not start with MinIO unless we actually need object storage semantics.
- Do not start with croc/wormhole unless the need is ad-hoc human transfer rather than service-to-service transfer.

## Next practical test

1. Deploy a temporary authenticated dufs instance on `self-server:44001` using an unused port in `30011-30025`.
2. From `oracle-proxy`, upload 512 MiB and 2 GiB test files to it.
3. Test interruption/resume.
4. Verify SHA256.
5. Compare against the already-measured direct no-proxy HTTP pull.
