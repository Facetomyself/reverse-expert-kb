# self-server / CHANGELOG

- 2026-04-04: Clarified likely current SSH entrypoint as `root@211.144.221.229:44001` based on user-provided access detail. Same-day verification showed this host still timed out from the current OpenClaw host on the direct path, but TCP connection to `211.144.221.229:44001` succeeded from `ali-cloud`. OpenClaw-side SSH config was updated so alias `self-server` now prefers `ProxyJump ali-cloud`, while `self-server-direct` remains available for direct-path diagnostics. Password was intentionally not written into `infra/`.
