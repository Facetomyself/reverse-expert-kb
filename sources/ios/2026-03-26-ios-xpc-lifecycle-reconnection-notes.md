# Apple XPC / NSXPC lifecycle-reconnection notes — accepted vs replied vs reconnected vs consumed

Date: 2026-03-26
Branch target: iOS practical workflows / Apple-platform service handoff seam
Purpose: preserve source-backed operator rules for Apple XPC cases where connection recovery, interruption, or invalidation can look stronger than the actual service-owned consequence.

## Research intent
Strengthen the practical Apple XPC continuation with a narrower lifecycle-aware stop rule.

The key operator problem is not merely:
- did the XPC route exist?

It is:
- which smaller proof object is actually stable enough to predict later behavior when interruption, invalidation, lazy launch, or restart noise is present?

## Search artifact
Raw multi-source search artifact:
- `sources/ios/2026-03-26-2216-ios-xpc-lifecycle-reconnection-search-layer.txt`

Requested source set:
- `exa,tavily,grok`

Observed search-source reality for this run:
- Tavily returned usable Apple documentation and discussion surfaces
- Exa was explicitly invoked but the backend reported `402 Payment Required`; merged output still contained some Exa-carried result items, so Exa was treated as attempted but degraded/unhealthy
- Grok was explicitly invoked and failed with repeated `502 Bad Gateway`

## Retained sources
1. Apple Developer Documentation — `NSXPCConnection`
   - <https://developer.apple.com/documentation/foundation/nsxpcconnection?language=objc>
2. Apple Developer Documentation — `invalidationHandler`
   - <https://developer.apple.com/documentation/foundation/nsxpcconnection/invalidationhandler>
3. Apple Developer Documentation — `NSXPCConnectionInterrupted`
   - <https://developer.apple.com/documentation/foundation/nsxpcconnectioninterrupted-c.enum.case?changes=_8&language=objc>
4. Apple archive / ecosystem-facing discussion retained conservatively via search results
   - Stack Overflow discussion on interruption vs invalidation
   - <https://stackoverflow.com/questions/47418944/nsxpcconnection-debugging-interruption-invalidation>

## High-signal retained findings

### 1. Apple exposes interruption and invalidation as distinct connection states
Even the search-visible Apple documentation surface is enough to preserve a practical distinction:
- `NSXPCConnection` explicitly exposes interruption and invalidation related surfaces
- `NSXPCConnectionInterrupted` is a named error/state surface
- `invalidationHandler` is a separate handler surface

Practical consequence:
- do not flatten interruption, invalidation, and ordinary success-reply handling into one generic “connection trouble” bucket
- they are already separate enough at the framework surface that the KB should preserve them as separate proof objects

### 2. Invalidated connections have a stricter stop rule than interrupted ones
The Apple `invalidationHandler` surface explicitly warns:
- you may not send messages over the connection from within an invalidation handler block

Practical consequence:
- invalidation is not merely “some error callback happened”
- it is a stronger end-of-life / unusable-connection condition than a generic momentary delivery disturbance
- this makes `reconnected` or `new connection created later` a different proof object from `same request family actually progressed`

### 3. Framework-visible routing surfaces are still weaker than remote consumer truth
The Apple `NSXPCConnection` surface explicitly names:
- `exportedObject`
- remote object proxy retrieval
- connection construction to a listener/service/endpoint

Practical consequence:
- Apple already makes route setup and remote exported-object concepts distinct in the API surface
- client-side proxy visibility is therefore weaker than one proved exported-object method entry or later service-owned reducer
- listener/route truth should not be collapsed into consumer truth

### 4. Lifecycle recovery can make compare pairs lie
The retained interruption/invalidation discussion surfaces consistently support the conservative field rule:
- a service/backend can disappear, restart, or leave the current request unrecoverable
- a later apparently healthy connection does not automatically prove the same remote method or same durable effect happened

Practical consequence:
- when compare pairs diverge around crash/restart/interruption/invalidation, the strongest next proof object is often one of:
  - reply/error class
  - exported-object method re-entry
  - one later durable service-owned effect
- not more broad client-side proxy inventory

## Practical synthesis worth preserving canonically
The compact rule for this seam is:

```text
accepted != replied != reconnected != consumed
```

Where:
1. **accepted**
   - listener accepted the connection or the route is live enough to exist
   - still only routing/gate truth

2. **replied**
   - reply, error, interruption, or invalidation became visible for the request family
   - stronger than raw route truth, but still weaker than durable semantic consequence

3. **reconnected**
   - a later connection or relaunched service appears usable again
   - lifecycle recovery truth, not automatic same-behavior truth

4. **consumed**
   - one exported-object method or later reducer/state write actually predicts the later effect
   - this is the service-owned proof boundary the workflow should stop at

## Best KB use of this material
This material is best used to sharpen the existing iOS XPC workflow note and subtree guide, not to grow a broad new Apple XPC taxonomy page.

The practical value is operator-facing:
- do not overclaim from visible `remoteObjectProxy`
- do not overclaim from listener acceptance
- do not overclaim from interruption/restart/recovery
- do not overclaim from reply/error visibility
- freeze the smallest truth object that actually predicts later behavior

## Search reliability note
This was a degraded-source external pass, not a healthy tri-source run.
It still counts as a real external-research attempt because `exa,tavily,grok` were explicitly requested and both degraded/failing sources were recorded clearly.