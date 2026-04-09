# Apple XPC / `NSXPCConnection` reply-error-reconnect compare notes

Date: 2026-04-10
Branch: iOS practical workflows
Seam: Apple-platform XPC cases where service method entry is already plausible enough, but same-request completion truth still lies
Related canonical pages:
- `topics/ios-xpc-proxy-to-service-consumer-workflow-note.md`
- `topics/ios-xpc-reply-error-invalidation-reconnect-compare-workflow-note.md`
- `topics/ios-practical-subtree-guide.md`
- `topics/mobile-reversing-and-runtime-instrumentation.md`

## Research intent
Tighten the iOS / Apple-platform XPC branch around a thinner compare seam:
- not whether the XPC route exists
- not whether one exported-object method is broadly plausible
- but whether one specific request actually reached reply, error, interruption, invalidation, reconnection, or durable consequence truth

The practical operator problem is that Apple XPC cases often yield strong-looking lifecycle evidence before they yield trustworthy same-request completion evidence.

## Search artifact
Raw multi-source search artifact:
- `sources/ios/2026-04-10-0450-ios-xpc-reply-reconnect-search-layer.txt`

Requested source set:
- `exa,tavily,grok`

Observed search-source reality for this run:
- Exa returned usable Apple documentation surfaces
- Tavily returned usable Apple documentation snippets and archive links
- Grok was explicitly invoked and failed with repeated `502 Bad Gateway` errors through the configured proxy path

## Retained sources
1. Apple Developer Documentation — `NSXPCConnection`
   - <https://developer.apple.com/documentation/foundation/nsxpcconnection>
2. Apple Developer Documentation — `interruptionHandler`
   - <https://developer.apple.com/documentation/foundation/nsxpcconnection/interruptionhandler>
3. Apple Developer Documentation — `invalidationHandler`
   - <https://developer.apple.com/documentation/foundation/nsxpcconnection/invalidationhandler>
4. Apple Developer Documentation — `invalidate()`
   - <https://developer.apple.com/documentation/foundation/nsxpcconnection/invalidate()>
5. Apple Developer Documentation — `remoteObjectProxyWithErrorHandler(_:)`
   - <https://developer.apple.com/documentation/foundation/nsxpcproxycreating/remoteobjectproxywitherrorhandler(_:)> 
6. Apple archive — *Creating XPC Services*
   - <https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingXPCServices.html>
7. Public Foundation SDK header mirror — `NSXPCConnection.h`
   - <https://raw.githubusercontent.com/xybp888/iOS-SDKs/master/iPhoneOS13.0.sdk/System/Library/Frameworks/Foundation.framework/Headers/NSXPCConnection.h>

Use source 7 conservatively: not as independent authority over Apple docs, but as a wording-level mirror for public SDK comments when Apple’s JS-heavy pages extracted poorly. Its retained comments matched Apple search-result snippets closely enough to preserve practical stop rules.

## High-signal findings

### 1. Reply-vs-error is exact-one callback truth, not durable consequence truth
The public `NSXPCConnection.h` comments state that for `remoteObjectProxyWithErrorHandler(...)`, if the sent message has a reply handler, then either the error handler or the reply handler will be called exactly once.

Practical consequence:
- an observed reply-vs-error callback is already a stronger proof object than vague “the request probably completed” language
- but exact-one callback truth is still weaker than the later durable consumer or policy consequence
- the branch should keep `replied/errored` separate from `consumed`

### 2. Interruption is weaker than invalidation
The header comments and Apple documentation surfaces preserve a real distinction:
- `interruptionHandler`: remote process exited or crashed; it may be possible to re-establish the connection by simply sending another message
- `invalidationHandler`: the connection could not be formed or has terminated and may not be re-established

Practical consequence:
- do not flatten interruption and invalidation into one generic transport-failure bucket
- interruption often means lifecycle noise plus possible retry/reconnect reality
- invalidation is a stronger end-of-life boundary for the current connection

### 3. Invalidation has a strict stop rule
The retained Apple surfaces and header wording preserve two practical rules:
- you may not send messages over the connection from within an invalidation handler block
- after `invalidate()`, no more messages may be sent or received

Practical consequence:
- invalidation is not just another error callback
- it is a real stop boundary for the current connection object
- later healthy communication should therefore be treated as reconnection or new-request truth, not silent proof that the same request completed

### 4. Local send progress is weaker than remote receipt
The retained `scheduleSendBarrierBlock(...)` header comment states that the barrier runs after outstanding sends complete, but this does not guarantee the messages were received by the remote process; waiting for a reply is the best option when receipt matters.

Practical consequence:
- local queue drain, send-barrier completion, or absence of immediate error are weaker than reply/error truth
- do not overread “send finished locally” as same-request service completion

### 5. `launchd` restart creates recovery truth, not same-request completion truth
Apple’s *Creating XPC Services* archive preserves several lifecycle rules:
- XPC services are launched on demand by `launchd`
- they may be restarted after crashes
- if a service crashes while processing a message that requires a response, the client can observe the connection becoming invalid until restart
- services should keep minimal state because they can be terminated suddenly

Practical consequence:
- a later healthy connection or relaunched helper is weaker than proving the same request actually reached reply or durable consequence
- stateless-or-minimal-state guidance also means “service came back” is not automatic proof of same-request continuity

### 6. Some invalidation happens before meaningful work begins
The retained header comments also preserve two easy-to-overread cases:
- `resume()` does not launch the service immediately; the service starts on demand when the first message is sent
- if the configured service name is invalid, the invalidation handler may be called immediately after `resume()`
- if `listener:shouldAcceptNewConnection:` returns `NO`, the connection object is invalidated after that method returns

Practical consequence:
- invalidation can be pure route/setup failure rather than service-side semantic failure
- do not overread early invalidation as proof that the target service method ran and rejected the request semantically

## Practical synthesis worth preserving canonically
A narrower Apple XPC compare rule is now worth preserving:

```text
exported-object method entry
  != local barrier-drained or callback-queue progress truth
  != replied-or-errored exactly-once truth
  != interrupted truth
  != invalidated truth
  != later reconnected/new-request truth
  != same-request durable consequence
```

This is the useful operator ladder:
1. **entered**
   - one exported-object method or immediate service-side reducer was reached
2. **barrier-drained**
   - local sends drained or local callback ordering advanced
   - still weaker than remote receipt
3. **replied-or-errored**
   - one exact-one reply/error outcome became visible for this request
4. **interrupted**
   - the current connection saw remote-exit/crash style lifecycle disruption
5. **invalidated**
   - the current connection ended and may not be re-established
6. **reconnected/new-request**
   - later healthy route/retry truth exists, but not necessarily same-request completion truth
7. **consumed**
   - one same-request durable service-owned effect or downstream consumer was proved

## Best KB use of this material
This material is best used to support a **thinner continuation page** under the existing Apple XPC workflow note, not to grow a broad XPC taxonomy page.

The value is practical and compare-oriented:
- keep barrier/local-send truth separate from reply/error truth
- keep reply/error truth separate from interruption/invalidation truth
- keep interruption/invalidation truth separate from later reconnection truth
- keep all of those separate from same-request durable consequence

## Search reliability note
This was a degraded-source external pass, not a healthy tri-source run.
It still counts as a real external-research attempt because `exa,tavily,grok` were explicitly requested and Grok was actually invoked and failed visibly.