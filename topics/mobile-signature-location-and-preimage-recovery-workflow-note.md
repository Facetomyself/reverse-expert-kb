# Mobile Signature Location and Preimage-Recovery Workflow Note

Topic class: concrete workflow note
Ontology layers: mobile-practice branch, request-shaping workflow, case-driven methodology
Maturity: structured-practical
Related pages:
- topics/mobile-signing-and-parameter-generation-workflows.md
- topics/mobile-risk-control-and-device-fingerprint-analysis.md
- topics/mobile-challenge-and-verification-loop-analysis.md
- topics/environment-state-checks-in-protected-runtimes.md
- topics/protocol-state-and-message-recovery.md
- topics/mobile-reversing-and-runtime-instrumentation.md
- topics/anti-frida-and-anti-instrumentation-practice-taxonomy.md

## 1. Why this page exists
This page exists to make the mobile subtree more operational.

The KB already has synthesis pages about mobile signing, device fingerprinting, and protected runtime analysis.
What it still needs more of is the thing analysts actually do in the middle of a case:
- anchor one target request
- locate the app-side field attachment path
- decide where to hook first
- recover the preimage before the final transform destroys structure
- separate stable transform code from volatile wrapper workflow
- explain why a reproduction attempt diverges

This page is therefore a **workflow note**, not a broad taxonomy page.

## 2. Target pattern / scenario
### Representative target shape
A mobile app sends one or more request fields that are:
- signed
- encrypted / packed / encoded
- device-state dependent
- request-role dependent
- session or challenge scoped
- partially produced in Java and partially in JNI / native code

Representative practitioner families repeatedly seen in community material include:
- x-gorgon / x-argus-like chains
- shield / wua / mssdk-style parameter families
- app-specific request signatures and anti-risk fields
- request values refreshed after challenge, retry, or session transitions

### Analyst goal
The usual goal is not “understand the whole app.”
It is one or more of:
- identify where a target field is attached to one concrete request
- recover the preimage inputs before final hashing / encryption / encoding
- determine which inputs are stable, session-bound, or environment-bound
- separate Java wrapper orchestration from native transform core
- decide whether a minimal harness is realistic or whether in-app observation must continue

## 3. The first three questions to answer
Before cleaning code or lifting crypto, answer these:

1. **Which exact request carries the field that actually matters?**
2. **At what stage is the value attached: Java request builder, JNI bridge, interceptor, or native networking layer?**
3. **Does the field drift because the algorithm changed, or because upstream state changed?**

These three questions prevent a lot of wasted static work.

## 4. Practical workflow: first pass

### Step 1: anchor one concrete request role
Start from the network side.
Do not start by grepping the APK for a parameter name unless the name is highly stable and uniquely identifying.

For one request family, record:
- endpoint and method
- whether the field is in headers, query, body, cookie-like storage, or protobuf/json members
- whether it appears on first request, retry, or only after challenge/session setup
- whether neighboring fields change together

Useful output from this step:

```text
run A: cold launch, login flow untouched
  /api/foo -> field absent
  /api/bar -> field sig present

run B: warm retry same path
  /api/bar -> field sig present but changed
  x-device / x-ts also changed

run C: altered environment or packaging
  /api/bar -> field present but server outcome changed
```

This already tells you whether the field is:
- init-coupled
- retry-sensitive
- session-sensitive
- environment-sensitive

### Step 2: find the final attachment path
Before looking for the transform core, find where the field is finally attached.

High-yield attachment surfaces include:
- OkHttp interceptors
- request builder wrappers
- header map assembly
- body/protobuf/json serialization sites
- JNI calls that return a ready-made field or packed blob
- native libraries used immediately before request dispatch

Why this is usually the best first move:
- final attachment code is easier to locate than the hidden transform core
- once the attach point is found, stack tracing often reveals the generation chain quickly
- it lets you classify whether you are seeing collection, transform, formatting, or final merge

### Step 3: classify the stage you hit
When you hit a suspicious method, ask:
- is this collecting device/session/request inputs?
- is this just formatting or encoding an already-built value?
- is this crossing Java↔JNI?
- is this the actual transform core?
- is this only attaching a value generated elsewhere?

A useful minimal staging model is:

```text
request role / session context / device state
    -> wrapper collection layer
    -> optional Java normalization
    -> JNI/native transform or local crypto/packing
    -> final formatting / encoding
    -> request attachment
```

## 5. High-yield breakpoint / hook families

### A. Request builder and interceptor boundary
Use when:
- you know which request carries the target field
- the app uses OkHttp / Retrofit / custom builders
- you need the fastest route to the final attachment site

What to inspect:
- header/body map right before dispatch
- stack leading to field insertion
- whether a single helper populates multiple anti-risk fields together

### B. Java↔JNI bridge
Use when:
- Java code looks thin and suspiciously orchestration-only
- the final field appears right after a native method call
- native libraries are likely doing the transform work

What to inspect:
- native method arguments
- Java-side objects flattened into byte arrays / strings / maps before the call
- whether the native return is final output, packed blob, or intermediate handle

### C. Preimage assembly points
Use when:
- the final signature looks opaque but upstream values are still structured
- several small values are combined, sorted, packed, or concatenated before a transform

What to inspect:
- timestamp / nonce / request path / body digest / device-id inputs
- whether values are normalized or canonicalized before hashing / encryption
- whether challenge or server-issued values are inserted upstream

### D. Response-driven refresh points
Use when:
- the field changes after login, challenge, token refresh, or retry
- the same endpoint behaves differently after one server response

What to inspect:
- response handlers updating local state
- token/session stores
- challenge outcome handlers
- whether the next request uses updated state without changing the visible transform code

## 6. Preimage-recovery workflow
A lot of mobile signing work is won or lost here.

### The practical goal
Try to capture the value **before** it enters the irreversible or structure-destroying stage.
That may be:
- a concatenated canonical string
- a sorted key-value map
- a protobuf / JSON object before packing
- a byte buffer right before native call
- a struct-like object flattened from request + device + session inputs

### Why preimage matters
If you only capture the final output, you may know that a field changed without knowing why.
If you capture the preimage, you can often explain:
- which component changed
- whether the drift is request-, session-, or device-driven
- whether the native transform core is actually stable

### Practical recovery order
A good default order is:
1. final attached field
2. immediate producer
3. Java↔JNI boundary args/return
4. structured preimage assembly
5. upstream sources feeding the preimage

This order tends to preserve meaning while keeping the search bounded.

## 7. Compare-run methodology
One run is almost never enough.

### Minimum useful compare axes
Change one axis at a time:
- cold launch vs warm launch
- pre-login vs post-login
- first request vs retry
- no challenge vs post-challenge
- baseline environment vs altered packaging/runtime state
- in-app execution vs partial external harness attempt

### What to record
For each run, record:
- whether the target field is present
- what neighboring dynamic fields changed with it
- whether the same attachment path fired
- whether the same JNI call fired
- whether the preimage shape changed
- what server-visible outcome changed

### Why this matters
Many failures are misdiagnosed because analysts do not distinguish:
- transform drift
- session drift
- challenge-state drift
- environment/trust drift
- observation-induced distortion

## 8. Java / native split: how to reason about it
A very common mobile pattern is:
- Java/Kotlin owns request orchestration and state gathering
- native code owns the compact transform / crypto / packing stage

When this happens, do not ask only “where is the algorithm?”
Ask:
- what exactly is Java feeding into native?
- what structure is lost at the boundary?
- what state is added before the boundary versus inside native?
- is the native return already final, or does Java still post-process it?

A useful mental split is:

```text
Java side: request role, state collection, canonicalization, field routing
Native side: compact transform, packing, local crypto, anti-analysis-sensitive logic
Java side again: encoding, final merge, dispatch
```

That model often explains why a native-only lift still fails.

## 9. Externalization decision rules

### Stay in-app first if
- you still do not know the minimum required preimage
- response-driven refresh logic is not understood
- environment-sensitive drift is still unexplained
- Java/native responsibilities are still blurred

### Consider a minimal harness when
- one field path has been isolated end-to-end
- the preimage schema is enumerable
- native inputs are capturable and stable enough
- session/challenge coupling has been bounded

### Prefer minimal harnesses
Aim for one verified path, not a full app clone.

Representative sketch:

```python
# sketch only: not target-specific exploit code
class RequestCtx:
    path = None
    method = None
    body_digest = None

class SessionCtx:
    token = None
    counters = None

class DeviceCtx:
    build = None
    ids = None
    locale = None


def collect_preimage(request_ctx, session_ctx, device_ctx):
    # recovered canonicalization placeholders
    return {
        "path": request_ctx.path,
        "body_digest": request_ctx.body_digest,
        "token": session_ctx.token,
        "locale": device_ctx.locale,
    }


def native_transform(preimage):
    # recovered native/crypto placeholder
    raise NotImplementedError
```

The point is to test whether the chain is really separable, not to prematurely rebuild the app.

## 10. Failure modes and what they usually mean

### Failure mode 1: you found the output field but cannot explain drift
Likely causes:
- upstream session or challenge inputs changing
- response-driven refresh
- environment-dependent values entering the preimage
- multiple neighboring fields forming one coupled family

Next move:
- compare structured preimages across runs
- inspect response handlers and local state updates between requests

### Failure mode 2: native function lifted, but reproduced output is rejected
Likely causes:
- wrong or incomplete preimage
- missing canonicalization step on Java side
- missing request-role context
- session/challenge state omitted
- environment/trust inputs omitted

Next move:
- diff in-app boundary args against harness inputs
- verify Java-side preprocessing before blaming the native core

### Failure mode 3: hook points work once, then become noisy or crashy
Likely causes:
- anti-instrumentation or integrity pressure
- racing multi-threaded request path
- attaching too deep in a hot path
- classloader / overload / JNI-signature mismatch

Next move:
- move outward to quieter attachment surfaces
- reduce hook count
- prefer request-boundary evidence over blanket deep instrumentation

### Failure mode 4: field looks valid, but server behavior still changes
Likely causes:
- field is only one member of a coupled trust family
- backend score depends on more than the visible signature
- packaging/device-state changed backend interpretation
- challenge state drifted even though the field format looks right

Next move:
- inspect sibling dynamic fields and request role
- compare server outcome across controlled environment changes

## 11. Practical analyst checklist

### Phase A: pin the request
- [ ] identify exact request carrying the field
- [ ] record when it first appears
- [ ] compare first run vs retry / post-login / post-challenge

### Phase B: locate the attachment path
- [ ] identify request builder / interceptor / serializer site
- [ ] inspect stack at field insertion
- [ ] classify current method as collect / transform / format / attach

### Phase C: recover preimage
- [ ] identify immediate producer of the field
- [ ] inspect Java↔JNI boundary if present
- [ ] capture structured inputs before irreversible transform
- [ ] identify upstream request/session/device sources

### Phase D: compare runs
- [ ] compare cold vs warm
- [ ] compare pre-login vs post-login
- [ ] compare no-challenge vs post-challenge
- [ ] compare baseline vs altered environment

### Phase E: choose next move
- [ ] continue in-app observation
- [ ] reduce intrusiveness
- [ ] isolate Java/native split more clearly
- [ ] build minimal harness for one verified path

## 12. What this page adds to the KB
This page adds the grounded material the mobile subtree needs more of:
- request-role-first workflow
- attachment-path-first strategy
- Java↔JNI boundary reasoning
- preimage-recovery discipline
- compare-run methodology
- concrete failure-diagnosis heuristics

It is intentionally more like a working analyst note than a taxonomy page.

## 13. Source footprint / evidence note
This workflow note is grounded mainly by the manually curated practitioner cluster around:
- mobile signing families
- app-side parameter generation
- device/fingerprint-coupled request shaping
- mobile risk-control and challenge workflows
- protected mobile runtime observation

It remains a synthesis workflow note, not a target-lab notebook for one app family.
Its value is in giving a reusable working method for recurring cases.

## 14. Topic summary
Mobile signature location and preimage recovery is a practical workflow for cases where request validity depends on app-side generation chains rather than packet format alone.

It matters because analysts often get stuck by staring at final signatures, while the real leverage lies in locating the attachment path, recovering the preimage before structure is destroyed, separating Java wrapper logic from native transform logic, and comparing runs carefully enough to explain drift instead of merely observing it.
