# iOS / Apple XPC lifecycle-vs-consumer notes

Date: 2026-03-26
Branch: iOS practical workflows
Seam: Apple-platform XPC service handoff where lifecycle noise is stronger than the actual later service-owned consumer
Related canonical pages:
- `topics/ios-xpc-proxy-to-service-consumer-workflow-note.md`
- `topics/ios-practical-subtree-guide.md`
- `topics/mobile-reversing-and-runtime-instrumentation.md`

## Research intent
Preserve a sharper practical stop rule for Apple-platform `NSXPCConnection` / Mach-service cases where analysts can already see:
- client-side proxy creation or selector use
- listener acceptance or service lookup
- interruption / invalidation / relaunch behavior

but still do **not** yet have the first durable service-owned consequence.

The operator problem is not merely “XPC exists.”
It is distinguishing which smaller proof object actually predicts later behavior.

## Search artifact
Raw multi-source search artifact:
- `sources/ios/2026-03-26-1716-ios-xpc-lifecycle-consumer-search-layer.txt`

Requested source set:
- `exa,tavily,grok`

Observed search-source reality for this run:
- Exa returned usable Apple/XPC documentation hits
- Tavily returned usable Apple/XPC documentation hits
- Grok was invoked but failed with repeated `502 Bad Gateway`

## Sources retained
### Apple archival guide — Creating XPC Services
- <https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingXPCServices.html>

Useful retained points:
- XPC services are managed by `launchd`
- `launchd` launches them on demand, restarts them on crash, and may terminate them when idle
- this is mostly transparent **except** when a service crashes while handling a message that requires a response, where the application can observe that the XPC connection becomes invalid until restart
- the service should be designed to hold minimal state
- `NSXPCConnection` is an RPC-style API around proxy objects and exported objects
- listener objects and `NSXPCListenerDelegate` acceptance are part of route setup, not the same thing as later service-owned semantic consequence

### Apple `NSXPCConnection` documentation surface
- <https://developer.apple.com/documentation/foundation/nsxpcconnection?language=objc>
- search-result-visible related surfaces:
  - `exportedObject`
  - `interruptionHandler`
  - `invalidate()`
  - `listener(_:shouldAcceptNewConnection:)`

Useful retained points from search/result surfaces:
- `NSXPCConnection` exposes both `interruptionHandler` and `invalidationHandler`
- `exportedObject` / remote object proxy are explicit API concepts, which helps preserve client-side proxy visibility vs remote exported-object consumer truth as distinct proof objects
- listener acceptance is an explicit object-level boundary and should be preserved separately from later remote method entry or effect

## Practical synthesis
The main practical refinement worth preserving:

```text
accepted != replied != reconnected != consumed
```

Why this matters:
- Apple XPC cases often produce **lifecycle-looking** evidence before they produce **behavior-owning** evidence
- because `launchd` can restart crashed or idle services, a connection that becomes valid again is not the same thing as proving the same remote exported-object method or later service-owned reducer actually ran again
- listener acceptance, proxy visibility, reply/error visibility, interruption/invalidation, and later durable effect all sit at different layers of truth

## Smaller proof objects to keep separate
1. **accepted**
   - listener accepted the connection
   - service lookup / route exists
   - connection family is plausible
   - still only route/gate truth

2. **replied**
   - success reply, error reply, or interruption/invalidation signal occurred
   - stronger than raw proxy visibility
   - still weaker than durable service-owned semantic consequence

3. **reconnected**
   - after interruption or invalidation, the service/connection appears live again
   - this is lifecycle recovery truth, not automatic repeat-of-behavior truth

4. **consumed**
   - one exported-object method or later reducer/state write/helper handoff actually predicts the later effect
   - this is the practical endpoint that should stop broad XPC-route widening

## Operator guidance retained
When a compare pair drifts around service restarts, interruption, or invalidation:
- do **not** widen client-side proxy tracing by default
- ask whether the first stable next proof object is:
  - reply/error class,
  - exported-object method re-entry,
  - or one later durable service-owned effect
- treat generic “connection is valid again” or “service relaunched” as weaker than proving one same consumer-bearing remote method or later reducer

Useful anti-drift wording:
- `remoteObjectProxy` is route truth
- `listener:shouldAcceptNewConnection:` is acceptance truth
- interruption/invalidation/restart is lifecycle truth
- only the exported-object method or later service-owned reducer is consumer truth

## Why this belongs in the KB
This is not just XPC taxonomy.
It helps with real operator mistakes in Apple-platform reversing:
- overclaiming from visible proxy calls
- overclaiming from listener/service lookup visibility
- overclaiming from interruption/restart recovery
- mistaking reply/error observation for the same thing as the later service-owned consequence

The KB should therefore preserve Apple-platform service work as a narrower lifecycle-aware reduction problem rather than a vague “XPC happened” story.
