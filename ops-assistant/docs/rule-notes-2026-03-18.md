# Rule notes - 2026-03-18

Additional noise-control refinements:

- `oracle-docker-proxy: reg-`
  - suppressed as a known naming artifact of the documented registry proxy stack
  - should not page as an undocumented project hint anymore

- `oracle-proxy: camoufox`
  - suppressed as an expected auxiliary runtime family belonging to historical/auxiliary registration tooling
  - should not page as undocumented project drift anymore

- fleet alert classification
  - corrected `ops-assistant` summary logic so only `host_health` failures produce P1 reachability alerts
  - non-reachability inspector failures (for example `docker_inventory`) now fall under lower-severity partial inspection handling instead of being mislabeled as host-down events
  - this was prompted by a 2026-03-18 `ali-cloud` false-positive where raw checks showed the host itself was reachable but one sub-check transiently timed out

These rules are intentionally narrow and host-scoped to avoid hiding genuinely new drift elsewhere.
