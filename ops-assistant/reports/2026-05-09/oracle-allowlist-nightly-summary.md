# Oracle Allowlist Nightly Summary

- Time: 2026-05-09 03:00 Asia/Shanghai / 2026-05-08 19:00 UTC
- Scope: `oracle-open_claw` local maintenance plus remote checks for `oracle-proxy`, `oracle-gateway`, `oracle-mail`, `oracle-registry`, `oracle-reverse-dev` only.

## Local `oracle-open_claw`
- Root filesystem remained non-critical but higher than older baselines: `45G total / 32G used / 14G free` (`70%`).
- Memory remained comfortable: `5.8Gi` total, `4.6Gi` available, no swap.
- Existing local nightly cleanup removed only stale `/tmp` audit/probe artifacts; pressure cleanup was skipped.

## Remote Allowlist
- `oracle-proxy`: reachable; expected long-lived containers remained up; root `51%`; memory comfortable; no new listener delta found.
- `oracle-gateway`: reachable and stable; meaningful cleanup delta observed — previously tracked helper endpoints on public `:18733` and localhost `127.0.0.1:18081` were no longer present.
- `oracle-mail`: reachable; `outlook-email-plus-caddy` and healthy app remained up; public `80/443` only for the web app; no classic mail protocol revival observed.
- `oracle-registry`: reachable; four registry containers remained up; local helper confirmed backend and public `/v2/` responses healthy.
- `oracle-reverse-dev`: reachable and resource-comfortable; no Docker containers; public `:631` CUPS/snap listener was again present while `:18080` upload listener remained absent.

## Writeback
- Updated `infra/hosts/oracle-gateway/{HOST.md,NETWORK.md,CHANGELOG.md}` for the cleared temporary helper endpoints.
- Did not modify `oracle-reverse-dev` docs in this pass because that changelog already had unrelated pre-existing uncommitted edits; the `:631` observation is captured here instead.
