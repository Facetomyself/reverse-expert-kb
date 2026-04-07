# Apple XPC / NSXPC reply-error-reconnect notes — accepted vs replied vs reconnected vs consumed

Date: 2026-04-08
Branch target: iOS practical workflows / Apple-platform service handoff seam
Purpose: preserve a source-backed operator refinement for Apple XPC cases where reply/error visibility and later healthy reconnection look stronger than the actual service-owned consumer.

## Research intent
Strengthen the existing iOS XPC workflow note with a narrower lifecycle-and-reply-aware stop rule.

The practical operator problem is not merely:
- did the client route into XPC?

It is:
- which smaller proof object is actually strong enough to predict later behavior when listener rejection, reply/error handling, interruption/invalidation, or later reconnection noise is present?

## Search artifact
Raw multi-source search artifact:
- `sources/ios/2026-04-08-0451-ios-xpc-search-layer.txt`

Requested source set:
- `exa,tavily,grok`

Observed search-source reality for this run:
- Exa returned usable Apple documentation hits
- Tavily returned usable Apple documentation hits and useful forum/discussion surfaces
- Grok was explicitly invoked and failed with repeated `502 Bad Gateway` through the configured proxy path

## Retained sources
1. Apple Developer Documentation — `NSXPCConnection`
   - <https://developer.apple.com/documentation/Foundation/NSXPCConnection>
2. Apple Developer Documentation — `invalidationHandler`
   - <https://developer.apple.com/documentation/foundation/nsxpcconnection/invalidationhandler>
3. Apple Developer Documentation — `interruptionHandler`
   - <https://developer.apple.com/documentation/foundation/nsxpcconnection/interruptionhandler>
4. Apple Developer Documentation — `remoteObjectProxyWithErrorHandler(_:)`
   - <https://developer.apple.com/documentation/foundation/nsxpcconnection/remoteobjectproxywitherrorhandler(_:)> 
5. Apple Developer Documentation — `listener(_:shouldAcceptNewConnection:)`
   - <https://developer.apple.com/documentation/foundation/nsxpclistenerdelegate/listener(_:shouldacceptnewconnection:)>
6. Apple Technote — TN3113: Testing and debugging XPC code with an anonymous listener
   - <https://developer.apple.com/documentation/technotes/tn3113-testing-xpc-code-with-an-anonymous-listener>
7. Conservative discussion surface retained only as support for operator questions, not as primary truth
   - <https://stackoverflow.com/questions/47418944/nsxpcconnection-debugging-interruption-invalidation>
   - Apple Developer Forums thread surfaced by search on listener rejection / invalidation behavior

## High-signal retained findings

### 1. Apple keeps listener acceptance, connection lifecycle, and invalidation semantics distinct at the framework surface
The search-visible Apple documentation already exposes separate surfaces for:
- `listener(_:shouldAcceptNewConnection:)`
- `interruptionHandler`
- `invalidationHandler`
- `remoteObjectProxyWithErrorHandler(_:)`

Practical consequence:
- acceptance, reply/error, interruption/invalidation, and later consumer truth should stay separate proof objects
- do not flatten them into one generic “XPC request outcome” bucket

### 2. Invalidation is a stronger end-of-life boundary than ordinary reply/error or interruption noise
The Apple `invalidationHandler` documentation explicitly warns that messages may not be sent over the connection from within the invalidation handler block.

Practical consequence:
- invalidation is not just another weak transport symptom
- a later healthy-looking connection is a reconnection fact, not proof that the same request family progressed to the same consumer
- this makes `reconnected` weaker than `consumed`

### 3. `remoteObjectProxyWithErrorHandler(...)` visibility is still weaker than exported-object method truth
Apple’s API surfaces make proxy creation/error handling and listener acceptance first-class concepts, but these are still route/lifecycle surfaces.

Practical consequence:
- visible error-handler activity does not by itself tell you whether the failure was:
  - listener rejection
  - interface/class contract mismatch
  - interruption/invalidation / service-lifecycle breakage
  - later semantic rejection after real method entry
- freeze one exported-object method or one later reducer before overclaiming about service-owned behavior

### 4. Anonymous-listener and listener-rejection test surfaces matter as compare tools, not just API trivia
Search surfaced Apple’s newer debugging technote for anonymous listeners and a useful listener-rejection discussion surface.

Practical consequence:
- in tricky compare pairs, it can be operationally useful to preserve a narrower question: did the run really get past acceptance into exported-object work, or did it only prove route formation and then fail at listener/contract/lifecycle level?
- this is more valuable than widening the map with more generic client-side proxy tracing

## Practical synthesis worth preserving canonically
The compact lifecycle-aware rule for this seam is:

```text
accepted != replied != reconnected != consumed
```

Where:
1. **accepted**
   - listener accepted the connection / route exists
   - still only routing or gate truth

2. **replied**
   - reply, error-handler, interruption, or invalidation became visible for the request family
   - stronger than raw route truth, but still weaker than durable semantic consequence

3. **reconnected**
   - a later connection appears healthy again or the service becomes reachable again
   - this is lifecycle recovery truth, not automatic same-request or same-consumer truth

4. **consumed**
   - one exported-object method or later reducer/state write actually predicts the downstream effect
   - this is the service-owned proof boundary the workflow should stop at

## Best KB use of this material
This material is best used to sharpen the existing iOS XPC workflow note.
It should not become a broad new Apple XPC taxonomy page.

The operator-facing value is:
- do not overclaim from listener acceptance
- do not overclaim from `remoteObjectProxyWithErrorHandler(...)`
- do not overclaim from interruption/invalidation visibility
- do not overclaim from later healthy reconnection
- stop only when one service-owned consumer or later durable reducer is frozen

## Search reliability note
This was a degraded-source external pass, not a fully healthy tri-source result set.
It still counts as a real external-research attempt because `exa,tavily,grok` were explicitly requested and Grok was actually invoked; its failure is recorded clearly.
