# Post-cleanup verification - 2026-03-17

## Outcome
After removing the historical leftover project directories from `oracle-proxy`, a fresh stable run and a fresh entity-level reconciliation run were executed.

## Verified results
### Stable watch path
Current filtered alert state:
- P1: none
- P2:
  - `oracle-docker-proxy: undocumented hints -> reg-`
  - `oracle-proxy: undocumented hints -> camoufox`

Interpretation:
- the previous noisy oracle-proxy compose-era leftovers are gone from the stable path
- oracle-proxy now only retains the `camoufox` hint mismatch, which is much narrower and likely tied to Tavily/Grok support stacks rather than generic forgotten projects

### Entity analysis path
`oracle-proxy` now shows:
- matched documented projects: 7
- missing documented projects: 0
- undocumented candidates: 0

Interpretation:
- cleanup succeeded
- previously detected leftover compose projects no longer appear as active undocumented project candidates

## Remaining follow-up targets
1. `oracle-docker-proxy`
   - `registry-ui`
   - `hubcmd-ui`
   These are currently best understood as documented-but-missing/inactive components.

2. `oracle-proxy`
   - `camoufox` still appears in hint-level drift output and should be normalized into the appropriate documented project topology, rather than treated as a leftover project.

## Recommendation
The next documentation/cleanup work should pivot away from historical leftover deletion and toward:
- normalizing `camoufox` ownership on `oracle-proxy`
- reconciling `registry-ui` / `hubcmd-ui` status on `oracle-docker-proxy`
