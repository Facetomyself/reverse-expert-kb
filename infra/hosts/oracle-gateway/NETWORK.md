# oracle-gateway / NETWORK

## 1. Public Network Identity
- Public IP: `129.150.61.78`
- Provider: Oracle Cloud
- Domain group label from historical export comments: `docker_proxy`

## 2. Domains currently mapped here
No primary live public domains should now be treated as served by this host after the 2026-03-25 migration.

The following names historically lived here but were migrated to `oracle-registry` (`140.245.33.114`) and should now be treated as served there instead:
- `hub.zhangxuemin.work`
- `ghcr.zhangxuemin.work`
- `k8s.zhangxuemin.work`
- `mcr.zhangxuemin.work`

Additional active DNS names currently pointed at this host's public IP:

- `backup.zhangxuemin.work`
  - DNS resolves to `129.150.61.78`
  - UDP `443` continues to serve Hysteria 2 traffic
  - host-local Caddy content path is retained on alternate ports `8080/8443`

Historical DNS/Caddy names formerly associated with this host but no longer served after the 2026-03-21 cleanup:

- `elastic.zhangxuemin.work`
- `gcr.zhangxuemin.work`
- `hubcmd.zhangxuemin.work`
- `k8sgcr.zhangxuemin.work`
- `nvcr.zhangxuemin.work`
- `quay.zhangxuemin.work`
- `ui.zhangxuemin.work`

## 3. Interpretation
This host is now best understood as a small gateway/Hysteria box with a reduced helper Caddy path, not the earlier broader historical domain surface.

## 4. Current confirmed gateway exposure
Current documented public surface:
- Hysteria active on UDP `443`
- host `caddy` retained on alternate local/helper ports `8080/8443`
- the old temporary upload helper backend on `127.0.0.1:18081` may still exist as local residue behind Caddy config, but is not part of the primary public front door

## 5. Reusable temporary upload pattern
A validated ad-hoc upload pattern now exists for this host when the user needs browser-based file transfer without SSH on the sender side:
- front door: `backup.zhangxuemin.work`
- auth UX: browser-native HTTP Basic Auth popup
- Caddy path route: `/tmp-upload/`
- backend shape: local Python upload app bound to `127.0.0.1:18081`
- retained host-side notes/scripts: `~/.tmp-upload-gateway/`
- retained upload directory from the 2026-03-27 run: `~/tmp-upload-drop`

This pattern should be treated as reusable but normally disabled; only re-enable it for explicit short-lived transfer windows, then remove the public route afterward.
