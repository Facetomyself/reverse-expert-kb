# Project Reconciliation - 2026-03-17

## oracle-proxy
- documented hints: 1panel, cliproxy, exafree, grok, openai, tavily
- runtime hints: anticap, camoufox, cliproxy, exafree, flaresolverr, grok, proxycat, tavily
- undocumented/drift candidates:
  - anticap
  - camoufox
  - flaresolverr
  - proxycat
- stale/possibly outdated doc hints:
  - 1panel
  - openai

## oracle-docker-proxy
- documented hints: harbor, hubcmd, registry, registry-ui
- runtime hints: reg-
- undocumented/drift candidates:
  - reg-
- stale/possibly outdated doc hints:
  - harbor
  - hubcmd
  - registry
  - registry-ui

## ali-cloud
- documented hints: 1panel, camoufox, easyimage
- runtime hints: camoufox, easyimage
- undocumented/drift candidates: none
- stale/possibly outdated doc hints:
  - 1panel

## oracle-mail
- documented hints: mailu, moemail
- runtime hints: none
- stale hints consistent with retired status:
  - mailu
  - moemail

## Initial interpretation
- `oracle-proxy` already shows clear value from drift detection: several compose-era projects appear on disk/runtime but are not normalized into current project docs.
- `oracle-docker-proxy` needs deeper mapping from current `reg-*` runtime naming to documented registry/hubcmd/registry-ui concepts.
- `ali-cloud` appears relatively aligned except that 1Panel is a machine-level service and may deserve stronger infra-vs-project distinction.
- `oracle-mail` stale hints are expected because it is retired; this should later be classified as retired-known rather than warning noise.
