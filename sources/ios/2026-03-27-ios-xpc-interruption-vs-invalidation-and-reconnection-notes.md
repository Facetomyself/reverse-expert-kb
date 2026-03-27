# Apple XPC / NSXPC lifecycle seam — interruption vs invalidation vs reconnection vs consumer truth

Date: 2026-03-27
Branch target: iOS practical workflows / Apple-platform service-handoff seam
Purpose: preserve a sharper, source-backed operator stop rule for `NSXPCConnection` cases where temporary interruption, terminal invalidation, and later healthy-looking reconnection can all be mistaken for the same thing.

Related canonical pages:
- `topics/ios-xpc-proxy-to-service-consumer-workflow-note.md`
- `topics/ios-practical-subtree-guide.md`
- `index.md`

## Research intent
Tighten an already-existing Apple XPC practical seam instead of broadening the branch.

The branch already preserved:
- client-side proxy truth vs service-side consumer truth
- acceptance / reply / invalidation / reconnection distinctions
- invalidation as a stronger stop-rule boundary than generic lifecycle drift

What still needed a sharper practical wording pass was:
- **interruption** should not remain only a vague member of `reply/error` noise
- analysts often need to separate a potentially recoverable interruption-like boundary from a stronger invalidation boundary and from a later reconnected/new-connection boundary
- compare pairs often lie exactly because these three lifecycle objects are flattened together too early

The narrower operator question is therefore:

```text
proxy / route truth is already plausible;
which lifecycle boundary actually happened:
interrupted, invalidated, or later reconnected,
and which later exported-object entry or durable consumer proves real progress?
```

## Search artifact
Raw multi-source search artifact:
- `sources/ios/2026-03-27-1416-ios-xpc-invalidation-vs-reconnection-search-layer.txt`

Requested source set:
- `exa,tavily,grok`

Observed search-source reality for this run:
- Tavily returned usable Apple documentation and supporting discussion surfaces
- Exa was explicitly invoked and the backend returned `402 Payment Required`; merged output still included some Exa-carried Apple documentation hits, so treat Exa as attempted but degraded/unhealthy
- Grok was explicitly invoked and failed with repeated `502 Bad Gateway`

## Retained sources
### Apple documentation surfaces retained conservatively via search results
- `NSXPCConnection`
  - <https://developer.apple.com/documentation/foundation/nsxpcconnection?language=objc>
- `interruptionHandler`
  - <https://developer.apple.com/documentation/foundation/nsxpcconnection/interruptionhandler>
- `invalidationHandler`
  - <https://developer.apple.com/documentation/foundation/nsxpcconnection/invalidationhandler>
- `invalidate()`
  - <https://developer.apple.com/documentation/foundation/nsxpcconnection/invalidate()>
- `exportedObject`
  - <https://developer.apple.com/documentation/foundation/nsxpcconnection/exportedobject?language=objc>

### Supporting ecosystem discussion retained only as field signal
- Stack Overflow: interruption vs invalidation debugging discussion
  - <https://stackoverflow.com/questions/47418944/nsxpcconnection-debugging-interruption-invalidation>
- Stack Overflow: launchd kill / interruption discussion
  - <https://stackoverflow.com/questions/17263490/is-an-xpc-interruption-handler-called-when-launchd-kills-the-process>

## High-signal retained findings

### 1. Apple exposes interruption and invalidation as distinct framework-visible surfaces
Even from the search-visible Apple documentation surface, the distinction is explicit enough to preserve canonically:
- `NSXPCConnection` exposes an `interruptionHandler`
- `NSXPCConnection` exposes an `invalidationHandler`
- Apple also names invalid/interrupt-related error/status surfaces separately

Practical consequence:
- do **not** flatten interruption and invalidation into one generic transport-failure bucket
- they are already distinct enough at the API surface to deserve separate proof-object slots in the KB

### 2. Invalidation is a stronger end-of-life boundary than interruption-style drift
The retained Apple documentation surface for `invalidationHandler` and `invalidate()` supports a stronger stop rule:
- invalidation is the boundary where the current connection should be treated as no longer usable
- Apple warns that you may not send messages over the connection from within an invalidation handler block
- explicit `invalidate()` also causes outstanding reply/error/invalidation blocks to be called on the message-handling queue

Practical consequence:
- interruption may still be lifecycle turbulence
- invalidation is closer to terminal loss of that specific connection instance
- a later good-looking connection is therefore a **new reconnection proof object**, not retroactive proof that the interrupted/invalidated request progressed

### 3. Reconnected truth is still weaker than same-consumer truth
The retained Apple/XPC surfaces plus field discussion are enough for a conservative operator rule:
- launchd-managed or on-demand service behavior can make a service look alive again
- a new or recovered connection can appear healthy after interruption/invalidation/restart
- that still does **not** prove the same exported-object method or later reducer actually ran again for the request family you care about

Practical consequence:
- keep `reconnected` separate from both lifecycle-failure surfaces and later consumer truth
- when compare pairs drift, the next useful proof object is often one of:
  - first interruption boundary,
  - first invalidation boundary,
  - first exported-object method re-entry,
  - or first later durable service-owned effect

### 4. Exported-object visibility still matters more than route/lifecycle chatter
The Apple documentation surface explicitly keeps these concepts separate:
- connection construction / service lookup / endpoint routing
- proxy retrieval
- exported object
- interruption/invalidation lifecycle handlers

Practical consequence:
- route truth, lifecycle truth, and consumer truth are different layers
- the durable proof boundary remains the first exported-object method or later service-owned reducer/state write that predicts later behavior

## Practical synthesis worth preserving canonically
The sharper compact rule for this seam is:

```text
accepted != interrupted != invalidated != reconnected != consumed
```

And an equally useful companion reminder is:

```text
proxy-visible != lifecycle-visible != exported-method-re-entry != durable-effect
```

Where:
1. **accepted**
   - listener accepted the connection or route/setup truth is established
   - still only routing/gate truth
2. **interrupted**
   - the current connection or reply flow suffered interruption-style drift
   - stronger than bare route truth, but still weaker than terminal loss and weaker than durable consequence
3. **invalidated**
   - the current connection instance hit the stronger unusable/end-of-life boundary
   - do not treat this as just another reply/error flavor
4. **reconnected**
   - a later connection or relaunched service appears usable again
   - this is lifecycle-recovery truth, not automatic same-request or same-consumer truth
5. **consumed**
   - one exported-object method or later reducer/state write actually predicts the later effect
   - this is the service-owned proof boundary the workflow should stop at

## Operator guidance retained
When a compare pair diverges around Apple XPC lifecycle noise:
- do **not** widen client-side proxy inventory by default
- first ask which of these is actually the first stable differing proof object:
  - acceptance truth
  - interruption truth
  - invalidation truth
  - reconnection truth
  - exported-object method re-entry
  - later durable service-owned effect
- treat “the connection came back” as strictly weaker than proving the same exported-object method or later consumer actually ran again
- if interruption is all you can prove, do not narrate it as if invalidation or reconnection were already known

A useful anti-drift wording set:
- `remoteObjectProxy` = route truth
- listener acceptance = gate truth
- interruption = temporary lifecycle disturbance truth
- invalidation = stronger end-of-life truth for that connection instance
- reconnection = later route recovery truth
- exported-object method / later reducer = consumer truth

## Why this belongs in the KB
This is a practical operator refinement, not just API taxonomy.
It prevents a common Apple-platform reversing mistake:
- overclaiming from healthy-looking lifecycle recovery events
- narrating interruption/invalidation/reconnection as if they were one thing
- treating reply/lifecycle chatter as if it already proved the same service-owned consumer

The KB should therefore preserve this seam as a thinner lifecycle-aware continuation inside the iOS practical branch rather than letting it dissolve back into generic “XPC happened / recovered” language.

## Search reliability note
This was a degraded-source external pass, not a healthy tri-source success.
It still counts as a real external-research attempt because `exa,tavily,grok` were explicitly requested and the degraded/failing sources were recorded clearly.