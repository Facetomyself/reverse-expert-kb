# macOS XPC client identity / code requirement notes — 2026-05-20

Scope: source-backed sharpening for `topics/native-macos-servicemanagement-xpc-helper-consumer-workflow-note.md`.

## Sources consulted

- Search artifact: `sources/native/2026-05-20-0450-macos-xpc-client-identity-search-layer.json`
- Apple Developer Forums, XPC Resources — https://developer.apple.com/forums/thread/708877
- Apple Developer Documentation, `NSXPCListener` — https://developer.apple.com/documentation/foundation/nsxpclistener
- Apple Developer Documentation, `NSXPCConnection` — https://developer.apple.com/documentation/foundation/nsxpcconnection
- Apple Developer Documentation, `setConnectionCodeSigningRequirement(_:)` — https://developer.apple.com/documentation/foundation/nsxpclistener/setconnectioncodesigningrequirement(_:)
- Apple Developer Documentation, `setCodeSigningRequirement(_:)` — https://developer.apple.com/documentation/foundation/nsxpcconnection/setcodesigningrequirement(_:)
- Apple Developer Forums, Validating Signature Of XPC Process — https://developer.apple.com/forums/thread/681053
- Apple archived SMJobBless sample readme — https://developer.apple.com/library/archive/samplecode/SMJobBless/Listings/ReadMe_txt.html

## Practical extraction

The durable operator point is not just that a macOS helper can be registered with ServiceManagement or contacted with XPC.  The sharper proof boundary is that **client identity and request ownership are their own evidence objects**.

Observed / source-backed anchors:

- Apple's XPC resources distinguish the high-level `NSXPCConnection` API, low-level XPC APIs, ServiceManagement installation state, and daemon/service programming material as separate surfaces.  That supports keeping service registration, connection construction, listener acceptance, and method handling separate during reverse analysis.
- The archived SMJobBless sample frames privileged-helper installation around least privilege, launchd-owned daemon execution, one-time authorization, and code-signing requirements that associate an app with the helper.  Those are install / association boundaries, not proof that a later behavior-bearing request was accepted or executed.
- Search results surfaced `NSXPCListener.setConnectionCodeSigningRequirement(_:)`, `NSXPCConnection.setCodeSigningRequirement(_:)`, and low-level `xpc_connection_set_peer_code_signing_requirement` as relevant identity-gate APIs.  For reversing, their presence should be treated as a **candidate trust gate** that must be placed relative to listener acceptance and method dispatch.
- Developer-forum and practitioner material repeatedly point at the audit-token / code-signing-requirement problem: PID, process name, or client-side proxy evidence is weaker than a server-side accepted identity check tied to the connection or to the specific request/message.

## Workflow implication

When the helper is privileged, security-sensitive, or policy-sensitive, do not collapse these claims:

```text
client proxy created
  != listener accepted the connection
  != code requirement / audit-token / entitlement gate passed
  != the accepted client sent this behavior-bearing message
  != exported method entered with validated arguments
  != helper-owned effect happened under that trust decision
```

Useful compact stop rule:

```text
proxy-visible != accepted != identity-gated != request-owned != method-entered != effect-owned
```

## Tactics to preserve in the KB

- Treat `setConnectionCodeSigningRequirement(_:)`, `setCodeSigningRequirement(_:)`, `xpc_connection_set_peer_code_signing_requirement`, entitlement checks, audit-token reads, `SecCode` / `SecRequirement` checks, and authorization references as **identity-gate candidates**.
- Freeze where the gate is applied: before listener acceptance, after connection acceptance but before method dispatch, inside a specific method, or only on a privileged sub-operation.
- In compare pairs, a working `remoteObjectProxy` or even an error-free reply is not enough; prove whether the same accepted/gated client owned the request whose effect is under analysis.
- Prefer request/message-derived identity evidence over PID/name-only evidence when the source permits it; PID/name evidence is reduction evidence, not final trust proof.
- If the target has reconnection or helper-restart behavior, re-prove identity binding after the new connection rather than carrying trust from a previous instance.
