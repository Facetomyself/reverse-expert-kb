# macOS XPC audit-token / code-signing hardening notes — 2026-05-27

Scope: source-backed sharpening for `topics/native-macos-servicemanagement-xpc-helper-consumer-workflow-note.md`.

## Sources consulted

- Search artifact: `sources/native/2026-05-27-0450-macos-xpc-audit-token-hardening-search-layer.json`
- Scott Knight, *Audit tokens explained* — https://knight.sc/reverse%20engineering/2020/03/20/audit-tokens-explained.html
- theevilbit, *Secure coding XPC Services - Part 2* — https://theevilbit.github.io/posts/secure_coding_xpc_part2/
- Objective Development, *The Story Behind CVE-2019-13013* — https://obdev.at/blog/what-we-have-learned-from-a-vulnerability/
- Apple documentation / forum surfaces surfaced in search results for `NSXPCListener`, `NSXPCConnection`, `setConnectionCodeSigningRequirement(_:)`, `setCodeSigningRequirement(_:)`, and XPC resources

## Practical extraction

The useful boundary in macOS helper work is narrower than “registered helper + XPC proxy exists.”
The new seam is that **peer identity, audit-token selection, and code-signing-policy checks are separate proof objects**.

Observed / source-backed anchors:

- PID-based code-signing checks are racy because PIDs can wrap or be reused; audit-token-based checks were repeatedly recommended as the safer peer-identity input for XPC helper validation.
- `NSXPCConnection` exposes an `auditToken` only privately, so any reverse analysis should record whether the helper is actually using an audit-token path or some weaker proxy/PID path.
- A helper may validate the peer’s code signature with `SecCodeCopyGuestWithAttributes`, but the audit-token versus PID choice is the important race boundary.
- `SecCodeCopySigningInformation(..., kSecCSDynamicInformation, ...)` and the `kSecCodeInfoStatus` flags matter because library-validation / hardened-runtime posture can change whether the service trusts later code loading, but that is still not a substitute for peer identity validation.
- If the helper inspects `CS_HARD`, `CS_KILL`, or `CS_REQUIRE_LV`-style flags, that should be treated as a **policy gate on the client image**, not as proof that the accepted request was already owned by the correct client.
- In practice, the strongest analysis question is not only “did the listener accept?” but “did the listener accept the same audited client, under the expected code-signing policy, before the behavior-bearing request was handled?”

## Workflow implication

Do not collapse these claims:

```text
client proxy created
  != listener accepted the connection
  != audit-token-based identity was selected
  != code-signing / library-validation policy passed
  != the accepted client sent this behavior-bearing request
  != exported method entered with validated arguments
  != helper-owned effect happened under that trust decision
```

Compact stop rule to preserve in the KB:

```text
proxy-visible != accepted != audit-token-validated != policy-checked != request-owned != method-entered != effect-owned
```

## Tactics to preserve in the KB

- Treat PID/name clues as reduction evidence only; prefer audit-token-derived identity when the helper actually uses it.
- Record whether the helper validates identity with `SecCodeCopyGuestWithAttributes(...kSecGuestAttributeAudit...)` or a PID-based fallback.
- Record whether `SecCodeCopySigningInformation(..., kSecCSDynamicInformation, ...)` is being used to enforce library-validation or hardened-runtime assumptions.
- Keep listener acceptance, identity gate, request ownership, and effect ownership in separate compare rows.
- If a reconnect or helper restart occurs, re-prove the identity gate for the new instance rather than carrying trust forward.
