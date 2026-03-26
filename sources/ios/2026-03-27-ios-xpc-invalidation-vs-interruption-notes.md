# Apple XPC / NSXPC invalidation-vs-interruption notes

Date: 2026-03-27
Branch target: iOS practical workflows / Apple-platform service handoff seam
Purpose: preserve a narrower lifecycle-aware stop rule for Apple XPC cases where interruption, invalidation, and later reconnection are easy to overread as if they already proved the same service-owned behavior.

## Research intent
Strengthen the existing Apple XPC practical leaf with a smaller but operator-meaningful distinction:
- interruption truth
- invalidation truth
- later reconnection truth
- durable service-owned consumer truth

The key problem is not merely whether one `NSXPCConnection` route exists.
It is whether the analyst has frozen the smallest proof object that still predicts later behavior.

## Search artifact
Raw multi-source search artifact:
- `sources/ios/2026-03-27-0116-ios-xpc-invalidation-search-layer.txt`

Requested source set:
- `exa,tavily,grok`

Observed search-source reality for this run:
- Tavily returned usable Apple documentation and discussion surfaces
- Exa was explicitly invoked but the backend reported `402 Payment Required`; merged output still contained some Exa-carried result items, so Exa was attempted but degraded/unhealthy
- Grok was explicitly invoked and failed with repeated `502 Bad Gateway`

## Retained sources
1. Apple Developer Documentation — `invalidationHandler`
   - <https://developer.apple.com/documentation/foundation/nsxpcconnection/invalidationhandler>
2. Apple Developer Documentation — `NSXPCConnection`
   - <https://developer.apple.com/documentation/foundation/nsxpcconnection>
3. Apple Developer Documentation — `listener(_:shouldAcceptNewConnection:)`
   - <https://developer.apple.com/documentation/foundation/nsxpclistenerdelegate/listener(_:shouldacceptnewconnection:)>
4. Apple Developer Documentation — `exportedObject`
   - <https://developer.apple.com/documentation/foundation/nsxpcconnection/exportedobject>
5. search-visible ecosystem discussion retained conservatively
   - <https://stackoverflow.com/questions/47418944/nsxpcconnection-debugging-interruption-invalidation>
   - <https://stackoverflow.com/questions/17263490/is-an-xpc-interruption-handler-called-when-launchd-kills-the-process>

## High-signal retained findings

### 1. Apple already exposes invalidation as a stronger connection end-state than generic interruption
The Apple `invalidationHandler` surface explicitly states two things that matter for operator stop rules:
- it is called if the connection cannot be formed or has terminated and may not be re-established
- you may not send messages over the connection from within an invalidation handler block

Practical consequence:
- invalidation is not just one more error callback
- it is stronger end-of-life evidence than ordinary interruption-style noise
- later success on a fresh or recovered connection must therefore be treated as a different proof object from “this same request family progressed through the same consumer again”

### 2. Listener acceptance is still route truth, not consumer truth
Apple’s `listener(_:shouldAcceptNewConnection:)` documentation surface preserves a small but useful rule:
- to accept the connection, configure it, call `resume()`, then return `true`

Practical consequence:
- acceptance proves route/gate truth only
- it still does not prove the later exported-object method or the later durable effect that actually matters

### 3. Exported-object truth is distinct from proxy and lifecycle truth
Apple’s `NSXPCConnection` and `exportedObject` documentation surfaces preserve:
- an exported object exists as an explicit API concept
- the proxy object is the remote side’s exported object from the caller’s point of view

Practical consequence:
- client proxy visibility, listener acceptance, interruption/invalidation, and actual exported-object method entry should remain separate proof objects
- the first service-owned consumer usually still lives at one exported-object method or immediate reducer behind it

### 4. Reconnection is a lifecycle recovery fact, not automatic same-behavior truth
The retained discussion surfaces consistently support the conservative field rule:
- services may be stopped, restarted, or unavailable transiently
- a later healthy-looking connection or successful reconnection does not by itself prove the same remote method or same durable effect happened again

Practical consequence:
- do not flatten “connection is back” into “same request family consumed again”
- after invalidation, treat later activity as new route/recovery evidence until one narrower exported-method or later durable effect is re-proved

## Practical synthesis worth preserving canonically
The smaller stop rule for this Apple XPC seam is now:

```text
accepted != replied != invalidated != reconnected != consumed
```

Where:
1. **accepted**
   - listener accepted the connection
   - route/gate truth only

2. **replied**
   - success reply, error reply, interruption, or another request-completion surface became visible
   - stronger than raw route truth, still weaker than durable service-owned consequence

3. **invalidated**
   - connection can no longer be used as the same live route
   - stronger end-of-life evidence than generic interruption-style drift
   - should stop analysts from silently treating later traffic as continuity of the same proof object

4. **reconnected**
   - a later connection or relaunched service appears usable again
   - lifecycle recovery truth, not automatic same-behavior truth

5. **consumed**
   - one exported-object method or later reducer/state write actually predicts the later effect
   - this is the service-owned proof boundary the workflow should stop at

## Best KB use of this material
This material is best used to sharpen the existing iOS XPC workflow note and subtree guide, not to create a broader Apple XPC taxonomy page.

The practical value is narrow and case-driven:
- do not overclaim from listener acceptance
- do not overclaim from a reply surface
- do not overclaim from interruption/invalidation noise
- do not overclaim from later reconnection
- freeze the smallest truth object that actually predicts later behavior

## Search reliability note
This was a degraded-source external pass, not a healthy tri-source run.
It still counts as a real external-research attempt because `exa,tavily,grok` were explicitly requested and the degraded/failing sources were recorded clearly.
