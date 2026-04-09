# iOS / Apple XPC Proxy to Service-Consumer Workflow Note

Topic class: concrete workflow note
Ontology layers: mobile practical workflow, iOS runtime branch, Apple-platform service handoff consequence bridge
Maturity: practical
Related pages:
- topics/ios-practical-subtree-guide.md
- topics/ios-objc-swift-native-owner-localization-workflow-note.md
- topics/ios-xpc-reply-error-invalidation-reconnect-compare-workflow-note.md
- topics/ios-result-callback-to-policy-state-workflow-note.md
- topics/native-gui-message-pump-and-signal-slot-first-consumer-workflow-note.md
- topics/mobile-reversing-and-runtime-instrumentation.md
- topics/runtime-behavior-recovery.md
Related source notes:
- sources/ios/2026-04-10-ios-xpc-reply-error-reconnect-notes.md
- sources/ios/2026-03-26-ios-xpc-proxy-vs-service-consumer-notes.md
- sources/ios/2026-03-26-ios-xpc-lifecycle-consumer-notes.md
- sources/ios/2026-03-26-ios-xpc-lifecycle-reconnection-notes.md

## 1. When to use this note
Use this note when an iOS-shaped or Apple-platform case already narrowed far enough that one XPC / `NSXPCConnection` / Mach-service / helper seam looks relevant, but the first **service-side behavior-changing consumer** is still unclear.

Typical entry conditions:
- the case is already clearly iOS-shaped, Apple-platform-private-framework shaped, or daemon/helper shaped
- one client-side proxy call, selector family, listener, Mach service name, or `NSXPCConnection` setup path is already visible enough to freeze
- broad setup/gate work is no longer the main blocker
- the current bottleneck is no longer “does XPC exist here?” but “which service-side method or later reducer actually changes behavior?”
- compare pairs still stall because client proxy visibility looks stronger than the downstream consequence you can actually prove

Use it for cases like:
- a private framework or app-side object clearly calls through `remoteObjectProxy` / `remoteObjectProxyWithErrorHandler`, but it is still unclear which remote exported-object method matters
- `listener:shouldAcceptNewConnection:` is visible, but the important state change happens later inside the helper/service implementation
- a Mach service name or launchd registration is recovered, but that only proves routing and service lookup, not the effect you care about
- a reversed interface/protocol is plausible enough to script or hook, yet reply/error behavior still does not prove the same durable consumer or policy state
- the app-side path looks clean, but launchd restarts / interruption / invalidation / class-whitelist friction make “proxy call happened” weaker than “same remote behavior happened”

Do **not** use this note when:
- the broad bottleneck is still ordinary iOS traffic-topology, environment-normalization, or packaging/jailbreak/runtime-gate drift
- the main difficulty is still callback/block landing truth rather than cross-process service ownership
- the case is already narrower than XPC routing and the remaining problem is the first app-local policy consumer after a truthful service reply
- the target is better framed as broad native service/daemon ownership without a specifically Apple XPC / `NSXPCConnection` seam

In those cases, route to the broader or adjacent note first.

## 2. Core claim

A practical stop rule worth preserving more sharply for Apple XPC-shaped service handoffs is:

```text
client connection/proxy exists
  != listener accepted connection
  != exported-object method entry
  != interruption/invalidation/reconnection truth for this path
  != later same-service consequence or later consumer truth
```

Treat these as different proof objects until one is frozen:
- client-side proxy / connection setup
- listener acceptance
- exported-object method entry
- interruption vs invalidation vs reconnection lifecycle truth
- later consequence that answers the analyst’s real question

This keeps XPC work from silently overreading proxy visibility, connection health, or later reconnection as already-good service-consumer proof for the same meaningful path.

Once an Apple-platform case already exposes one plausible XPC client seam, the best next move is often **not** more client-side proxy tracing and **not** a broad XPC taxonomy digression.
It is to freeze the first **service-side consumer boundary**.

The central question is usually:

```text
Which remote exported-object method or later service-side reducer first turns
this visible client-side proxy route into one durable behavior I can trust?
```

A practical stop rule worth keeping explicit is:
- once one client-side proxy / selector family is already plausible, stop widening the map at connection setup by default
- instead, try to freeze one five-part proof object:
  - one client trigger and proxy/selector family
  - one listener/acceptance or connection-validity boundary if it still matters
  - one remote exported-object method entry
  - one reply/error or intermediate reducer that predicts later behavior
  - one later durable effect

Until that is proved, Apple-platform service cases often stall in three kinds of confusion:
- client proxy setup that looks like ownership even though it is only routing
- listener / Mach-service / launchd truth that looks like consumer proof even though it is only availability or gate proof
- reply/error-handler visibility that looks like durable consequence even though the real effect still lives behind one later reducer or service-side state change

## 3. The five boundaries to separate explicitly

### A. Client trigger / proxy-route truth
This is where the app or framework clearly chooses the XPC route.
Typical anchors:
- `NSXPCConnection` creation
- `remoteObjectProxy`
- `remoteObjectProxyWithErrorHandler`
- `synchronousRemoteObjectProxyWithErrorHandler`
- recovered selector/protocol names
- one private-framework method that clearly performs the proxy call

What to capture:
- one representative client action or trigger
- one proxy selector or method family only

Useful reminder:
- a proxy call is a route candidate, not yet consumer proof

### B. Listener / acceptance / routing truth
This is where the service side proves it can accept and route a connection.
Typical anchors:
- `listener:shouldAcceptNewConnection:`
- listener delegate setup
- `exportedInterface` / `remoteObjectInterface`
- `exportedObject` assignment
- Mach service / launch agent / launchd registration
- endpoint/listener-endpoint handoff

What to capture:
- the smallest service-side acceptance/routing boundary that is still relevant
- whether the connection is private-app-scoped, Mach-service-scoped, or endpoint-routed

Useful reminder:
- acceptance truth is still weaker than the remote method that later changes behavior
- Mach service lookup or launchd visibility narrows the search space, but it is still routing truth rather than first consumer truth

### C. Remote exported-object method entry
This is the first boundary where the remote side actually starts doing the semantic work.
Typical anchors:
- one exported-object selector implementation
- one service object method that receives deserialized arguments
- one handler behind a recovered interface/protocol
- one first reducer immediately behind the exported method if the exported method is just a thin adapter

What to capture:
- one exact method or adapter-to-method pair
- the first branch / enqueue / helper call / state write that makes it behaviorally relevant

Useful reminder:
- this is usually the first strong handoff from “XPC exists” to “this service-side logic owns the behavior”
- do not overread interface reconstruction or selector names as equivalent to method-entry truth

### D. Reply / error / interruption truth
This is where the service seam reveals whether the request completed, failed, or was interrupted.
Typical anchors:
- reply block execution
- error-handler execution
- interruption handler
- invalidation handler
- class-whitelist / deserialization failures
- service restart / lazy-launch timing that changes request completion shape

What to capture:
- whether the meaningful truth is successful reply, error path, interruption, or no-reply drift
- whether the failure is contract-shaped, lifecycle-shaped, or later semantic rejection

Useful reminder:
- reply or error visibility is stronger than bare proxy visibility, but it is still not automatically the durable consequence you care about
- launchd-managed lifecycle can create misleading compare pairs unless reply/error truth is kept separate from later effect truth
- Apple framework-visible interruption and invalidation surfaces are already different enough that they should not be flattened into one generic transport-failure bucket
- invalidation is especially strong stop-rule evidence because Apple explicitly warns that you may not send messages over the connection from within an invalidation handler block
- a later healthy-looking connection should therefore be treated as reconnection truth, not automatic proof that the same request family progressed to the same consumer
- `remoteObjectProxyWithErrorHandler(...)` error visibility is still weaker than proving which exported-object method ran, whether the failure was listener-rejection / contract-shape / lifecycle breakage, and whether one later durable consumer was actually bypassed or merely retried
- a useful compact lifecycle ladder for compare pairs is `accepted != replied != reconnected != consumed`, so listener acceptance, reply/error visibility, later healthy reconnection, and the first service-owned consumer stay separate

### E. Durable consequence truth
This is the first boundary where the service-side work clearly predicts later behavior.
Typical anchors:
- one service-side state write
- one filesystem or database write
- one scheduler/job creation
- one later helper invocation
- one policy verdict or object that the caller or another daemon actually consumes
- one later app-visible state change provably owned by the service call

What to capture:
- the narrowest effect that still predicts what happens next
- one later durable consequence, not every downstream artifact

Useful reminder:
- this is the actual endpoint of the workflow
- everything before it should be treated as routing, gating, or transport unless proved otherwise

## 4. Default workflow

### Step 1: freeze one client-side XPC seam only
Pick one seam only.
Examples:
- one private-framework method -> `remoteObjectProxy` selector -> service-side method
- one protected action -> Mach service lookup -> exported-object method -> reply
- one daemon/helper interaction whose durable effect matters for the case

Avoid mixing multiple services, selectors, or helpers.

### Step 2: draft one service-consumer chain
Write the smallest plausible chain before widening the map:

```text
client trigger:
  one app/private-framework action

proxy route:
  one connection/proxy/selector family

routing or acceptance boundary:
  listener / Mach service / exported interface setup if relevant

candidate service-side consumer:
  one exported-object method or immediate reducer

candidate reply/error boundary:
  reply / interruption / invalidation / contract failure

visible durable effect:
  one state write / policy outcome / later helper action
```

This draft may be wrong.
Its purpose is to stop endless “XPC exists here too” accumulation.

### Step 3: prove whether routing truth is already good enough
Before spending more effort on proxy setup, answer:
- is the connection family already frozen strongly enough?
- do you already know the service name / endpoint / listener family well enough?
- would more connection setup detail actually change the next experimental move?

If yes, stop widening at routing.
Move to service-side method truth.

### Step 4: choose the first real service-side consumer
Good candidates include:
- the first exported-object selector implementation that deserializes and uses the arguments
- the first helper call or reducer behind the exported method that actually predicts later behavior
- the first service-side state write or queue/scheduler action behind the method

Bad default choices include:
- stopping at `remoteObjectProxy`
- stopping at Mach service discovery
- stopping at `listener:shouldAcceptNewConnection:`
- treating a recovered protocol name as if it already proves the semantic consumer
- treating connection validity as if it already proves durable effect

A source-backed discipline worth preserving here:
- Apple’s XPC architecture makes the exported object the receiver of remote proxy messages
- therefore client-side proxy visibility and service-side consumer truth are different proof objects
- listener acceptance and launchd lookup narrow the route but do not yet own the behavior

### Step 5: separate contract failure from semantic failure
When compare pairs drift, ask which bucket the drift really belongs to:
- protocol or selector guess is wrong
- interface/class whitelist is incomplete
- connection was interrupted/invalidated
- service restarted or did not keep the same request alive
- remote method executed but later semantic reduction or state write differs

This matters because the fix changes completely depending on the bucket.
Do not flatten all of them into generic “XPC failed” language.

### Step 6: prove one service-side consumer with one compare pair
Use one narrow compare pair:
- target action vs nearby non-target action
- accepted run vs degraded/error run
- same proxy call with/without one expected class/argument shape
- connection-valid run vs interrupted/restarted run
- same client proxy selector with listener-accepted vs listener-rejected / invalidated / later-reconnected behavior

What you want to learn:
- does the same client-side proxy route appear in both runs?
- does the same remote exported-object method entry appear in both runs?
- does reply/error truth differ before the same durable effect?
- is the visible drift best explained by listener rejection, interface/class contract mismatch, interruption/invalidation, or later semantic divergence?
- which first service-side consumer best predicts the downstream consequence?

A particularly useful question in Apple XPC cases is:
- does the same proxy selector fire in both runs, yet only one run reaches the same exported-object method or later durable state write?

If yes, the next proof object is usually not more client tracing.
It is one narrower service-side routing / contract / lifecycle explanation.

A second practical question now worth preserving explicitly is:
- did the run only prove `accepted`, `replied`, or `reconnected`, or did it actually prove `consumed`?

That smaller ladder prevents three common overclaims:
- listener acceptance becoming fake method-entry proof
- `remoteObjectProxyWithErrorHandler(...)` becoming fake semantic-failure proof
- later healthy reconnection becoming fake same-request/same-consumer proof

### Step 7: stop at the first durable service-owned consequence
The workflow succeeds when you can rewrite the path as:

```text
client trigger
  -> proxy/selector family
  -> listener/acceptance or routing truth if needed
  -> remote exported-object method
  -> reply/error or intermediate reducer
  -> one durable consequence
```

That chain is the practical definition of the first **service-side consumer boundary**.
Once it exists, default to treating it as the proof boundary that ends broad XPC-route widening for this stage.
Only reopen broad connection mapping if later evidence actually breaks that chain.

## 5. Practical scenario patterns

### Scenario A: proxy call is visible, but the real effect still hides behind the exported object
Pattern:

```text
client method clearly gets remoteObjectProxy
  -> selector call looks stable
  -> analysts still cannot explain later effect
```

What usually helps:
- stop adding more proxy-side hooks
- freeze the exported-object method or immediate reducer behind it
- prove one later state write / queue action / helper call that predicts the effect

### Scenario B: listener acceptance looks important, but it is only gate truth
Pattern:

```text
listener:shouldAcceptNewConnection: is easy to see
  -> exportedInterface/exportedObject setup is obvious
  -> later consumer is still unclear
```

What usually helps:
- record listener acceptance once
- then move immediately to the exported method family
- avoid treating “accepts connections” as if it already proves semantic ownership

### Scenario C: recovered protocol looks callable, but reply/error drift still dominates
Pattern:

```text
selector/protocol reconstruction looks plausible
  -> proxy call can be made or hooked
  -> reply fails, error-handler fires, or classes are rejected
```

What usually helps:
- separate contract-shape problems from service-side semantic problems
- treat allowed-classes / interface configuration as one distinct proof object
- only claim service-side consequence once the same method or later effect is actually frozen

### Scenario D: service lifecycle causes misleading compare pairs
Pattern:

```text
service launches on demand
  -> connection seems valid again after interruption/restart
  -> analysts overread that as same behavior having happened
```

What usually helps:
- freeze request send attempt, reply/error path, and later durable effect separately
- keep launch/restart/interruption truth as lifecycle evidence, not direct consequence evidence
- preserve the narrower stop rule `accepted != replied != invalidated != reconnected != consumed`
- treat "connection became valid again" or "service relaunched" as weaker than proving the same exported-object method or later service-owned reducer actually ran again
- when compare pairs diverge around invalidation/restart, ask whether the first stable proof object is the reply/error class, the exported-object method re-entry, one explicit invalidation boundary, or one later durable effect rather than more client-side proxy inventory

A narrower Apple-platform lifecycle reminder now worth keeping explicit is:
- launchd-managed restart, interruption, and invalidation frequently create compare-pair noise that looks like progress
- acceptance truth, reply/error truth, invalidation truth, reconnection truth, and durable service-owned consequence are often five different proof objects
- invalidation is especially strong stop-rule evidence because Apple documents that the connection may not be re-established and that you may not send messages over that connection from within an invalidation handler block
- the analyst should therefore stop at the smallest one that actually predicts later behavior instead of overreading any generic "XPC recovered" event

### Scenario E: service reply is visible, but the real policy consequence lives one hop later
Pattern:

```text
exported-object method clearly replies
  -> app receives object or status
  -> actual allow/retry/degrade decision still hides later
```

What usually helps:
- stop at the service-owned consequence only if the service itself is the analysis target
- otherwise hand off into `ios-result-callback-to-policy-state-workflow-note.md` and keep the service reply as the upstream result boundary

## 6. Hand-off rules
Route forward:
- to `topics/ios-xpc-reply-error-invalidation-reconnect-compare-workflow-note.md` when one exported-object method or immediate service-side reducer is already good enough, but same-request completion truth still lies across reply/error/interruption/invalidation/reconnect surfaces
- to `topics/ios-result-callback-to-policy-state-workflow-note.md` when the service seam is already truthful enough and the real remaining gap is the first app-local policy consumer of the service result
- to `topics/ios-objc-swift-native-owner-localization-workflow-note.md` when the XPC seam turned out to be only one candidate among several ownership routes and you still need the first consequence-bearing owner
- to `topics/native-gui-message-pump-and-signal-slot-first-consumer-workflow-note.md` when the case is really a broader desktop/macOS Cocoa/XPC/dispatch ownership problem rather than an iOS practical leaf
- to broader runtime-evidence work when the real bottleneck is now compare-run truth rather than service-side consumer localization

Do not keep this page open once the first service-side consumer boundary is no longer the bottleneck.

## 7. Practical reminders worth preserving
- `remoteObjectProxy` is a routing anchor, not the endpoint
- `listener:shouldAcceptNewConnection:` is gate proof, not effect proof
- Mach service / launchd visibility is routing truth, not consumer truth
- reply/error-handler truth is not automatically the same as durable semantic consequence
- protocol reconstruction improves reachability, but not necessarily ownership proof
- when in doubt, freeze the exported-object method and one later durable effect before widening again
