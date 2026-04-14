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

- `derp.zhangxuemin.work`
  - DNS resolves directly to `129.150.61.78` (Cloudflare proxy removed before DERP cutover)
  - TCP `80/443` serves `derper`
  - UDP `3478` serves DERP STUN
  - deployed on 2026-04-03 as the host's primary public TCP front door

- `backup.zhangxuemin.work`
  - DNS resolves to `129.150.61.78`
  - UDP `443` continues to serve Hysteria 2 traffic
  - historical TCP `443` Caddy service was displaced on 2026-04-03 by the DERP cutover
  - host-local Caddy content path was retained on alternate ports `8080/8443` instead of public `80/443`

Additional currently observed public surfaces on the host itself:
- a temporary `python3` distribution endpoint is still listening on public `:18733`

Historical DNS/Caddy names formerly associated with this host but no longer served after the 2026-03-21 cleanup:

- `elastic.zhangxuemin.work`
- `gcr.zhangxuemin.work`
- `hubcmd.zhangxuemin.work`
- `k8sgcr.zhangxuemin.work`
- `nvcr.zhangxuemin.work`
- `quay.zhangxuemin.work`
- `ui.zhangxuemin.work`

## 3. Interpretation
This host is now best understood as a small gateway box with a live Hysteria + DERP split, a reduced helper Caddy path, and a small amount of temporary distribution/upload residue — not a pure Hysteria-only surface and not the earlier broader registry/front-door role.

## 4. Current confirmed gateway exposure
Observed listener surface at the 2026-04-13 19:04 UTC recurring check:
- `derp.zhangxuemin.work` / `derper` remains the primary public TCP entrypoint on this host
- host `derper` is active and listening on TCP `80/443`
- `derper` STUN remains active on UDP `3478`
- Hysteria remains active on UDP `443`
- Tailscale remains joined with IPv4 `100.116.171.76`
- host `caddy` remains on alternate local/helper ports `8080/8443` with admin on `127.0.0.1:2019`
- temporary public `python3` distribution endpoint still present on `:18733`
- the old temporary upload helper backend still exists as local residue on `127.0.0.1:18081`

## 5. Reusable temporary upload pattern
A validated ad-hoc upload pattern now exists for this host when the user needs browser-based file transfer without SSH on the sender side:
- front door: `backup.zhangxuemin.work`
- auth UX: browser-native HTTP Basic Auth popup
- Caddy path route: `/tmp-upload/`
- backend shape: local Python upload app bound to `127.0.0.1:18081`
- retained host-side notes/scripts: `~/.tmp-upload-gateway/`
- retained upload directory from the 2026-03-27 run: `~/tmp-upload-drop`

This pattern should be treated as reusable but normally disabled; only re-enable it for explicit short-lived transfer windows, then remove the public route afterward.

## 6. To Be Confirmed
- whether `backup.zhangxuemin.work` should later gain additional routed content beyond the current Clash Verge config distribution path
- exact long-term retention expectations for any future gateway-side config artifacts
- any future nginx/traefik/cloudflared involvement if the host role expands again
