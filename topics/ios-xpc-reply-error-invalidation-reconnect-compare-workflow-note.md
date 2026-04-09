# iOS / Apple XPC Reply-Error-Invalidation-Reconnect Compare Workflow Note

Topic class: concrete workflow note
Ontology layers: mobile practical workflow, iOS runtime branch, Apple-platform service-handoff compare continuation
Maturity: practical
Related pages:
- topics/ios-practical-subtree-guide.md
- topics/ios-xpc-proxy-to-service-consumer-workflow-note.md
- topics/ios-result-callback-to-policy-state-workflow-note.md
- topics/runtime-behavior-recovery.md
- topics/mobile-reversing-and-runtime-instrumentation.md
Related source notes:
- sources/ios/2026-04-10-ios-xpc-reply-error-reconnect-notes.md
- sources/ios/2026-03-26-ios-xpc-lifecycle-consumer-notes.md
- sources/ios/2026-03-26-ios-xpc-lifecycle-reconnection-notes.md

## 1. When to use this note
Use this note when an Apple-platform / iOS-shaped case is already narrow enough that one XPC route and one service-side method family are plausible, but compare pairs still lie about **same-request completion truth**.

Typical entry conditions:
- one client-side `remoteObjectProxy...` path is already frozen strongly enough
- one exported-object method or immediate service-side reducer is already visible enough to compare
- the current bottleneck is no longer “which service owns this?”
- the remaining confusion is whether one request really reached reply, error, interruption, invalidation, reconnection, or durable consequence truth
- later healthy-looking connections or retries keep getting overread as if they proved the same request completed
- local send progress, callback-queue movement, or absence of immediate errors looks stronger than it really is

Use it for cases like:
- the same exported-object method seems to run in both compare pairs, but only one run produces a meaningful reply or later effect
- `remoteObjectProxyWithErrorHandler(...)` is visible, but it is unclear whether an error callback, reply callback, interruption, or invalidation actually explains the divergence
- the service crashes or exits and later comes back, but it is unclear whether that proves retry truth only or same-request completion truth
- `scheduleSendBarrierBlock(...)`, local callback ordering, or “send returned” gets mistaken for remote receipt
- listener rejection, invalid service name, or endpoint invalidation may be causing early invalidation before the interesting semantic work even begins

Do **not** use this note when:
- the broad bottleneck is still ordinary iOS setup/gate drift, traffic-topology drift, or trust-path uncertainty
- the first real problem is still which XPC service-side method or reducer owns the behavior at all
- the case has already moved past the service seam and the real remaining gap is one app-local policy consumer after a stable reply/result

In those cases, use the broader Apple XPC note or the downstream result-to-policy note first.

## 2. Core claim
A narrower Apple XPC compare rule worth preserving explicitly is:

```text
exported-object method entry
  != local barrier-drained or callback-queue progress truth
  != exactly-one reply-or-error callback truth
  != interruption truth
  != invalidation truth
  != later reconnection or resend truth
  != same-request durable consequence
```

Treat these as different proof objects until one is frozen:
- service-side method entry
- local send/barrier progress
- exact-one reply-vs-error callback outcome
- interruption truth
- invalidation truth
- later reconnection or retry truth
- durable same-request consequence

The practical goal is not merely to prove that “XPC still works somehow.”
It is to answer:

```text
Which smallest completion-shaped proof object actually predicts whether this specific
request completed, failed, restarted, or reached one durable consumer?
```

## 3. The proof objects to separate explicitly

### A. Service-side method-entry truth
This is the first strong boundary for the request itself.
Typical anchors:
- one exported-object selector implementation
- one immediate reducer behind the exported method
- one service-side state write or helper enqueue directly behind the method

Useful reminder:
- this note assumes method-entry truth is already plausible enough to be worth comparing
- if method entry is still unclear, route back to the broader XPC service-consumer note

### B. Local send / barrier / callback-queue progress truth
This is where local instrumentation can look deceptively strong.
Typical anchors:
- `remoteObjectProxy...` call returns
- local callback queue drains work
- `scheduleSendBarrierBlock(...)` runs
- no immediate local exception or error appears

Useful reminder:
- Apple’s public comments explicitly warn that a send barrier does **not** guarantee the remote process received the message
- local progress is therefore weaker than reply/error truth
- do not treat local queue motion as same-request completion proof

### C. Exactly-one reply-or-error callback truth
This is the first strong completion-shaped surface for one request.
Typical anchors:
- reply block for the proxied method fires
- `remoteObjectProxyWithErrorHandler(...)` error handler fires
- synchronous proxy call returns or fails with one clear error path

Useful reminder:
- Apple’s public comments preserve a useful exactness rule: when a message has a reply handler, either the error handler or the reply handler is called exactly once
- that exact-one surface is already valuable compare truth
- but it is still weaker than proving the later durable service-owned or app-consumed effect

### D. Interruption truth
This is lifecycle disruption that may still allow later communication.
Typical anchors:
- `interruptionHandler`
- connection-level interrupted error surfaces
- remote process exit/crash with later possible recovery

Useful reminder:
- Apple’s public comments preserve that another message may re-establish the connection after interruption
- interruption is therefore not the same thing as invalidation and not the same thing as same-request failure permanence
- also keep in mind that Apple documents no guaranteed ordering between interruption callbacks and other handler/reply callbacks

### E. Invalidation truth
This is the stronger end-of-life boundary for the current connection object.
Typical anchors:
- `invalidationHandler`
- explicit `invalidate()`
- invalid service name or endpoint/listener invalidation
- listener rejection cases that invalidate after `shouldAcceptNewConnection:` returns `NO`

Useful reminder:
- invalidation means the connection may not be re-established
- Apple also documents that you may not send messages over the connection from within the invalidation handler block
- later healthy communication should therefore be treated as new route / retry truth, not silent continuation of the old request

### F. Reconnection / retry / resend truth
This is later recovery, not proof that the earlier request completed.
Typical anchors:
- a fresh connection becomes healthy after interruption/invalidation
- the same client action resends a request
- `launchd` restarts a helper and later communication works again

Useful reminder:
- Apple’s XPC lifecycle is launchd-managed and can be on-demand / crash-recovery shaped
- “it works again later” is weaker than “the same request completed”
- keep reconnection truth separate from same-request completion truth whenever compare pairs get noisy

### G. Durable same-request consequence truth
This is the endpoint of the continuation.
Typical anchors:
- one service-side state/object write owned by the request
- one persistent artifact or scheduler action owned by the request
- one reply object or downstream reducer that the caller actually consumes
- one later effect that is provably owned by this request, not just by a later retry

Useful reminder:
- this is the only boundary that should close the question “did this request really matter?”

## 4. Default compare workflow

### Step 1: freeze one request-shaped compare pair
Choose one pair only:
- good run vs degraded/error run
- same client trigger with/without one expected class/argument shape
- same route before vs after service restart/crash
- same exported-object method family with stable-vs-missing later effect

Do not mix several selectors, services, or retries in the same pass.

### Step 2: mark the strongest service-side entry point first
Write the smallest truthful service-side anchor:

```text
client trigger
  -> proxy selector family
  -> one exported-object method or immediate reducer
```

If you cannot write that much confidently, you are still too early for this continuation.

### Step 3: separate local send progress from remote completion
Ask explicitly:
- did I only prove that local sends drained?
- did I only prove that a callback queue advanced?
- did I actually see reply/error truth for this request?

If the best evidence is only local send/barrier progress, stop calling it completion.

### Step 4: classify the terminal callback for this request
Prefer one of these exact buckets:
- reply handler ran
- error handler ran
- interruption surfaced
- invalidation surfaced
- no completion-shaped callback surfaced yet

That classification is usually more useful than broad “the XPC path failed” wording.

### Step 5: decide whether later healthy behavior is retry truth or same-request truth
Ask:
- is the later healthy connection obviously a new connection object?
- did the original connection already invalidate?
- did the original request ever produce its own reply/error outcome?
- is the later effect clearly tied to a resent request rather than the original one?

If you cannot answer these, do **not** narrate the later effect as completion of the original request.

### Step 6: stop at the first durable same-request consequence
The continuation succeeds when you can rewrite the request as:

```text
method entry
  -> reply-or-error classification
  -> interruption/invalidation/reconnect classification if needed
  -> one durable same-request consequence
```

If reply/result delivery is already stable and the remaining gap is now the first app-local policy consumer, hand off downstream instead of staying in XPC lifecycle analysis.

## 5. Practical scenario patterns

### Scenario A: method entry appears in both runs, but only one run gets a meaningful reply
Pattern:

```text
same exported-object method looks reachable
  -> one run replies
  -> one run drifts into error/interruption/invalidation/no-reply
```

What usually helps:
- classify the exact completion bucket for each run
- avoid widening client-side routing again
- ask whether the divergent run only proved local send progress or real completion truth

### Scenario B: the error handler fires once, but durable effect is still unclear
Pattern:

```text
remoteObjectProxyWithErrorHandler(...) is visible
  -> error callback fires once
  -> analysts overread that as fully explained failure
```

What usually helps:
- keep exact-one error truth separate from durable consequence truth
- ask whether the interesting effect is still owned by a later retry, fallback, or alternate route
- ask whether the error happened before method entry, after method entry, or after later reduction already began

### Scenario C: interruption occurs and later communication succeeds
Pattern:

```text
request appears to trigger interruption
  -> later message or later connection works
  -> analysts narrate “the request recovered”
```

What usually helps:
- treat later healthy communication as reconnection/retry truth first
- require one explicit same-request completion proof before calling it recovery of the original request
- remember that Apple documents interruption as potentially recoverable by sending another message

### Scenario D: invalidation fires early and the real semantic work never started
Pattern:

```text
resume() or listener connection setup happens
  -> invalidation fires quickly
  -> analysts narrate semantic rejection by the target method
```

What usually helps:
- check invalid service-name, endpoint, or listener-rejection explanations first
- keep route/setup invalidation separate from method-level semantic failure
- remember that `listener:shouldAcceptNewConnection:` returning `NO` invalidates the connection after return

### Scenario E: local send/barrier evidence looks good, but no reply arrives
Pattern:

```text
send path returns cleanly
  -> local barrier or queue progress is visible
  -> no trustworthy reply/error outcome appears
```

What usually helps:
- stop at local progress truth and do not overclaim receipt
- Apple’s public comments already warn that send-barrier completion is weaker than remote receipt
- wait for reply/error truth or a stronger service-side consequence boundary

## 6. Hand-off rules
Route backward:
- to `topics/ios-xpc-proxy-to-service-consumer-workflow-note.md` when method-entry truth or first service-side consumer truth is still not good enough

Route forward:
- to `topics/ios-result-callback-to-policy-state-workflow-note.md` when reply/result delivery is already trustworthy enough and the remaining gap is now app-local policy consequence
- to broader runtime-evidence compare work when callback ordering, replay-worthiness, or compare-pair design is still the actual blocker rather than Apple XPC semantics

Do not keep this page open once same-request completion truth is no longer the bottleneck.

## 7. Practical reminders worth preserving
- method entry is not completion
- send/barrier/local queue progress is not receipt
- exact-one reply-or-error callback is stronger than vague completion language
- interruption is not invalidation
- invalidation is not reconnection
- reconnection is not same-request completion
- reply/error truth is still weaker than durable same-request consequence
- when in doubt, freeze one request, one callback classification, and one durable same-request effect before widening again