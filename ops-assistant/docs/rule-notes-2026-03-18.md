# Rule notes - 2026-03-18

Additional noise-control refinements:

- `oracle-docker-proxy: reg-`
  - suppressed as a known naming artifact of the documented registry proxy stack
  - should not page as an undocumented project hint anymore

- `oracle-proxy: camoufox`
  - suppressed as an expected auxiliary runtime family belonging to historical/auxiliary registration tooling
  - should not page as undocumented project drift anymore

These rules are intentionally narrow and host-scoped to avoid hiding genuinely new drift elsewhere.
