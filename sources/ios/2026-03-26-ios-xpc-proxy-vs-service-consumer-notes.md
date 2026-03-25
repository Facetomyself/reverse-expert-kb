# Apple XPC / NSXPC sources note — proxy setup vs service-side consumer truth

Date: 2026-03-26
Branch target: iOS practical workflows / Apple-platform service handoff seam
Purpose: preserve source-backed operator rules for cases where visible `NSXPCConnection` or XPC client activity is still weaker than the service-side method or later durable effect the analyst actually cares about.

## Why these sources were retained
These sources were retained because they support one practical stop rule the KB did not yet preserve cleanly in the iOS branch:
- `NSXPCConnection` setup, `remoteObjectProxy`, listener creation, and Mach/XPC service lookup are usually **routing / delivery scaffolding**
- the first behavior-bearing proof object is often one **service-side exported-object method** or one later reducer / durable state change behind it
- launchd-managed lifecycle and interruption / invalidation behavior can make analysts overread connection validity or proxy visibility as proof that the target consequence actually happened

## Retained sources
1. Apple archive — Creating XPC Services
   - <https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingXPCServices.html>
2. objc.io — XPC
   - <https://www.objc.io/issues/14-mac/xpc>
3. Tony Gorez — Attacking macOS XPC Helpers: Protocol Reverse Engineering
   - <https://tonygo.tech/blog/2025/how-to-attack-macos-application-xpc-helpers>
4. R. Derik — Creating a Launch Agent that provides an XPC service on macOS using Swift
   - <https://rderik.com/blog/creating-a-launch-agent-that-provides-an-xpc-service-on-macos/>

## High-signal findings from the sources

### 1. Proxy calls relay to the remote side’s exported object, not to abstract “XPC”
Apple’s archive documentation makes the clearest architectural statement:
- each side has an `NSXPCConnection`
- the connection has an `exportedInterface` and `exportedObject`
- when the client calls a method on a proxy object, the remote side’s `NSXPCConnection` dispatches that method to the object stored in `exportedObject`

Practical consequence:
- a visible client-side `remoteObjectProxy` call is still weaker than the service-side exported-object method that actually runs
- preserve separate truth for:
  - connection creation / lookup
  - remote interface selection
  - proxy acquisition
  - actual remote exported-object method entry
  - later durable effect

### 2. Listener acceptance and connection setup are only gate proof, not consequence proof
Apple archive material and reversing-oriented examples both show the service-side acceptance shape:
- listener receives a new connection
- service sets interfaces / exported object
- service resumes the connection
- only then do later remote method calls become meaningful

Practical consequence:
- `listener:shouldAcceptNewConnection:` or listener setup proves only that the connection family exists and may accept traffic
- it does **not** prove which service method later changed behavior
- keep acceptance truth separate from method-entry truth

### 3. launchd-managed lifecycle can make “service exists” look stronger than it is
Apple archive docs and objc.io both emphasize:
- XPC services are launched on demand by `launchd`
- they may be terminated when idle
- interruption / invalidation can happen even when the higher-level connection object still exists or is recreated
- if a service crashes while a reply is outstanding, the request may need to be resent

Practical consequence:
- do not flatten these into one generic “XPC worked/failed” bucket
- preserve separate truth for:
  - service lookup / launch opportunity
  - connection validity / interruption state
  - request send attempt
  - reply-vs-error-handler outcome
  - remote method-side durable consequence

### 4. Interface / class whitelisting and reply contracts can fail after the proxy boundary
The reversing-oriented source from Tony Gorez gives a useful operator reminder:
- a reversed protocol can look callable
- but real execution may still fail because the interface or allowed classes are incomplete
- proxy error visibility is therefore weaker than the remote semantic contract being correct

Practical consequence:
- separate:
  - guessed selector/protocol truth
  - interface/class whitelist truth
  - remote method entry truth
  - reply-material truth
- do not treat `remoteObjectProxyWithErrorHandler` or a connection-level error alone as enough to classify the service-side behavior

### 5. Mach service / launch-agent visibility is also still only routing truth
The launch-agent walkthrough usefully preserves the lower-level path:
- `NSXPCListener(machServiceName: ...)`
- plist `MachServices`
- launchd lookup and on-demand start

Practical consequence:
- Mach service name recovery and launchd plumbing narrow the search space
- but they are still routing truth, not first consumer truth
- the first behavior-bearing proof object still lives at one exported-object method or one later reducer behind it

## Practical operator rules worth preserving canonically

### Rule A: do not stop at `remoteObjectProxy`
A visible proxy call proves a route candidate, not necessarily a service-owned consequence.
Prefer freezing:
- one client trigger
- one proxy selector or method family
- one service-side exported-object method
- one later durable state write / helper invocation / reply object / filesystem or policy effect

### Rule B: keep acceptance, method entry, and durable effect separate
Recommended buckets:
1. listener / accept-new-connection truth
2. connection / proxy setup truth
3. remote exported-object method entry truth
4. reply/error-handler truth
5. later durable effect truth

### Rule C: treat launchd lifecycle as a replay/comparison hazard
Because services may start lazily, restart, or terminate when idle:
- compare pairs should avoid overreading “service process exists” as equivalent to “same method/effect happened”
- interruption / invalidation / reply timing can change without the same durable behavior happening

### Rule D: keep protocol reconstruction and consumer proof separate
Recovered interfaces and method names improve reachability.
They do not by themselves prove:
- same object instance
- same exported object implementation
- same downstream state change
- same durable effect

## Best KB use of this material
This material is best used to support a thinner practical continuation page, not a broad XPC taxonomy page.
The valuable continuation is:
- when Apple-platform / iOS-shaped analysis already reached a private-framework / daemon / helper seam
- and a client-side proxy call is visible
- but the real question is still which service-side method or later state write actually owns the behavior

That continuation should preserve:
- client proxy visibility vs exported-object method truth
- listener acceptance vs method-entry truth
- reply/error-handler truth vs durable consequence truth
- Mach service / launchd routing truth vs first consumer truth
