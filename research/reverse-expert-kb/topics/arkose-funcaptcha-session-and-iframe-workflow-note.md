# Arkose / FunCaptcha Session and Iframe Workflow Note

Topic class: concrete target-family workflow note
Ontology layers: browser-runtime subdomain, protected-interaction workflow, validation-lifecycle analysis
Maturity: structured-practical
Related pages:
- topics/browser-side-risk-control-and-captcha-workflows.md
- topics/browser-fingerprint-and-state-dependent-token-generation.md
- topics/cloudflare-turnstile-widget-lifecycle-workflow-note.md
- topics/browser-cdp-and-debugger-assisted-re.md
- topics/browser-environment-reconstruction.md
- topics/datadome-geetest-kasada-workflow-note.md

## 1. Why this page exists
This page exists because Arkose / FunCaptcha is a recurring browser protection family where analysts often waste time if they treat the whole problem as only:
- a visible puzzle/game,
- a token string,
- or a generic "captcha reverse" label.

In practice, the valuable object is usually the workflow boundary chain:
- client setup,
- callback registration,
- challenge shown or suppressed,
- session token handoff,
- iframe/lightbox message flow if present,
- backend verification or update request,
- first accepted consumer request,
- reset / retry / failure transitions.

That makes Arkose a strong fit for the KB’s concrete, case-driven pivot.

## 2. Target pattern / scenario
### Typical target shape
An Arkose / FunCaptcha protected flow often has some combination of:
- Arkose client script loaded into the page
- `myArkose.setConfig(...)` with callback registration
- explicit or selector-driven `myArkose.run()` start
- session-level callbacks such as:
  - `onReady`
  - `onCompleted`
  - `onSuppress`
  - `onFailed`
  - `onReset`
  - `onError`
- hosted iframe or lightbox flow using `postMessage`
- session token surfaced as `response.token` or iframe `payload.sessionToken`
- backend verification step that consumes the session token server-side
- reset/retry behavior creating a new session

### Analyst goal
The practical goal is usually one of:
- identify where Arkose is configured and started
- determine whether the target uses inline, lightbox, or hosted iframe mode
- locate where the session token exits Arkose-managed state and enters host-page logic
- distinguish suppressed/no-challenge completion from interactive challenge completion
- explain why a captured token or apparently successful completion still fails at backend verification or on retry

## 3. What matters first
Before beautifying minified code, answer these questions:
1. Where is `myArkose.setConfig(...)` called, and which callbacks matter on this page?
2. Does the challenge run automatically, on user selector, or via explicit `myArkose.run()`?
3. Is this integration inline in the page, or is it hosted through an iframe/lightbox boundary?
4. Where does the session token first become visible to host-page code?
5. Which request actually sends that token to backend verification?
6. If failures happen, are they challenge failures, reset/retry effects, iframe-message issues, or backend verification issues?

Those six answers usually give more leverage than broad source cleanup.

## 4. Concrete workflow: first pass

### Step 1: classify the integration shape
Start by deciding which Arkose surface you are actually looking at.

Common shapes:
- direct client API integration in the host page
- selector/lightbox mode where host page triggers challenge later
- hosted iframe flow with `postMessage` event exchange
- detection or suppressed flow where no visible challenge appears but a token/session still completes

Why this matters:
- lightbox/iframe flows reward message-boundary tracing
- direct client API flows reward callback-registration tracing
- suppression/detection flows reward backend-handoff tracing rather than puzzle-UI tracing

### Step 2: find config registration and start edge
A high-yield first anchor is usually `myArkose.setConfig(...)`.

What to record:
- which callbacks are registered
- whether `onCompleted`, `onSuppress`, `onFailed`, and `onError` are wired
- whether configuration names a selector or expects programmatic `run()`
- whether `reset()` is used after completion or failure

Then find what starts the workflow:
- auto start after `onReady`
- selector click
- explicit `myArkose.run()`
- iframe `postMessage` such as `challenge-open`

### Step 3: anchor the session-token handoff edge
Do not stop at the visible challenge.
Find the first place Arkose-managed session state becomes host-page-consumable state.

Common handoff edges:
- `onCompleted(response)` receiving `response.token`
- `onSuppress(response)` receiving a token-bearing response in no-challenge cases
- hosted iframe `message` event with `eventId: 'challenge-complete'` and `payload.sessionToken`
- host-page function that forwards the token into a form, request wrapper, or verification endpoint

Representative run log sketch:

```text
run A: low-risk / suppressed path
  onReady
  onSuppress(response)
  token visible
  backend verify request

run B: interactive challenge path
  onShow / onShown
  challenge-complete message or onCompleted(response)
  token visible
  backend verify request

run C: failure/reset path
  onFailed or onError
  reset()
  new session starts
```

This separates token generation, token handoff, and token redemption.

### Step 4: anchor the backend verification or update request
Once the token handoff edge is visible, identify the request that actually consumes the session token.

What to record:
- endpoint and request shape carrying the token
- whether the host page bundles other app/session state with it
- whether verification happens immediately after callback or later
- whether challenge suppression and visible challenge completion both hit the same backend path
- whether the request is the final allow/deny edge or only a verification/update edge
- whether failure occurs before or after reset/hide transitions

Why this matters:
- a visible token is not the whole story
- backend verification is a distinct boundary and may be where the real failure sits
- some targets treat this request as a trust-update step rather than the first request whose acceptance materially changes app behavior

### Step 4A: identify the first accepted consumer request
Do not stop at `onCompleted(response)`, `challenge-complete`, or even the first backend request carrying the session token.
A recurring practical boundary is the **first later request, redirect, route transition, or session/data fetch that becomes accepted only after the Arkose transition succeeds**.

What to record:
- whether the token-carrying verify/update request itself returns the final allow/deny decision or only refreshes trust state
- which later request, redirect, SPA route, or session fetch first stops failing, degrading, or looping
- whether accepted and failed runs diverge first at token visibility time, verify/update time, or only one step later
- whether suppressed and visible-challenge paths converge on the same first accepted downstream consumer

Representative compare-run sketch:

```text
run A: suppressed path
  challenge-suppressed / onSuppress(response)
  POST /verify-session carries sessionToken
  GET /account/bootstrap accepted

run B: visible challenge path
  challenge-complete / onCompleted(response)
  POST /verify-session carries sessionToken
  GET /account/bootstrap accepted

run C: still-broken path
  challenge-complete / onCompleted(response)
  POST /verify-session carries sessionToken
  GET /account/bootstrap still challenged / degraded / empty

practical reading:
  token visibility and verify submission were not enough;
  the first accepted consumer request localized the real acceptance boundary
```

Why this matters:
- Arkose docs are strong on callback/message and verify semantics, but the real app consequence can still appear only in the next downstream consumer
- this is often the cleanest compare-run anchor when callback/message behavior looks identical
- it aligns Arkose with the KB-wide four-boundary chain used across the other browser widget-family notes

### Step 5: map lifecycle transitions as a state machine
Treat Arkose as a small session machine.

Useful states to record:
- client loaded / ready
- challenge shown
- challenge suppressed
- challenge completed
- warning / error
- failed / retries exhausted
- reset
- hidden / closed
- backend verified / rejected

Minimal state sketch:

```text
setConfig
  -> onReady
  -> run() or selector/postMessage trigger
  -> shown OR suppressed
  -> onCompleted / challenge-complete message
  -> backend verify request
  -> accepted OR rejected
  -> optional reset() -> new session
```

## 5. Where to place breakpoints / hooks

### A. `myArkose.setConfig(...)`
Use when:
- you need to classify the integration quickly
- you want callback registration, selector config, and execution assumptions

Inspect:
- callback names and function bodies
- selector/lightbox settings
- whether completion/suppress/failure callbacks share a common consumer

Representative hook sketch:

```javascript
// sketch only
const origSetConfig = myArkose.setConfig;
myArkose.setConfig = function(cfg) {
  console.log('arkose.setConfig', cfg);
  return origSetConfig.apply(this, arguments);
};
```

### B. `myArkose.run()` and `myArkose.reset()`
Use when:
- challenge execution is deferred
- you need to see what actually starts a session or creates a new session

Inspect:
- which user action or app event triggers `run()`
- whether `reset()` happens automatically after completion/failure
- whether retries actually reuse or replace the previous session

### C. Callback boundaries: `onCompleted`, `onSuppress`, `onFailed`, `onError`
Use when:
- you need the first structured result object
- you want to classify success, suppression, recoverability, or failure

Inspect:
- `response.token`
- `response.completed`
- `response.suppressed`
- `response.recoverable`
- any host-page code immediately consuming the response

Representative sketch:

```javascript
// sketch only
const wrapCb = (name, fn) => function(resp) {
  console.log('arkose callback', name, resp);
  return fn && fn.apply(this, arguments);
};
```

### D. Iframe / `postMessage` boundaries
Use when:
- the integration uses hosted iframe or lightbox mode
- challenge state is crossing frame boundaries

Inspect:
- `window.addEventListener('message', ...)`
- outbound `postMessage` carrying `challenge-open`
- inbound events such as:
  - `challenge-loaded`
  - `challenge-show`
  - `challenge-shown`
  - `challenge-complete`
  - `challenge-failed`
  - `challenge-hide`
- whether `payload.sessionToken` is immediately consumed

Representative hook sketch:

```javascript
// sketch only
window.addEventListener('message', (event) => {
  try {
    const msg = typeof event.data === 'string' ? JSON.parse(event.data) : event.data;
    console.log('arkose message', msg);
  } catch (_) {}
});
```

### E. Host-page verification request wrapper
Use when:
- token visibility is already solved
- the remaining unknown is why verification succeeds, fails, or differs between suppressed and interactive paths

Inspect:
- exact request carrying token to backend
- sibling fields added by the host page
- timing relative to completion or suppression callback
- whether this request is itself the decisive allow/deny boundary or only a trust-update edge before a later consumer request

### F. First accepted consumer request boundary
Use when:
- callback/message visibility and verify/update request visibility already look correct
- the application still behaves differently across accepted and failed runs
- the real question is which later route, session fetch, or protected API first benefits from successful Arkose classification

Inspect:
- first downstream request after verify/update whose response/body/state materially changes
- first redirect or SPA route transition that only succeeds after the Arkose path completes
- whether suppressed and visible-challenge paths converge on the same downstream consumer
- whether pre-reset and post-reset sessions diverge here rather than at token visibility time

## 6. Practical compare-run methodology
A single successful observation is often misleading.
Use controlled comparisons.

### Minimum useful axes
Change one axis at a time:
- suppressed path vs visible challenge path
- inline/direct integration vs iframe/lightbox path
- first completion vs post-reset completion
- immediate backend verify vs delayed verify
- verify/update success vs first downstream accepted consumer behavior
- recoverable warning/error path vs hard failure path

### What to record
For each run, record:
- integration shape
- start trigger (`run`, selector, or message)
- whether challenge was shown or suppressed
- token handoff surface
- backend verification/update request timing
- first downstream request or route that actually changed behavior
- whether `reset()` happened
- whether session appeared new after reset

### Why this matters
Arkose-like targets can easily mislead analysts into conclusions such as:
- “the token path is solved” when only the callback edge was found
- “the challenge failed” when the real issue is backend verification handling
- “this is an iframe problem” when the real issue is reset/new-session behavior
- “same flow, same token semantics” when suppressed and interactive paths differ in host-page handling

## 7. Failure modes and what they usually mean

### Failure mode 1: token is visible in callback/message, but application still rejects flow
Likely causes:
- backend verification request is missing expected app/session context
- host-page consumer is transforming or routing token differently than assumed
- verification path differs between suppressed and interactive sessions
- the verify/update request succeeds syntactically but the first downstream consumer request still remains blocked or degraded

Next move:
- inspect the exact host-page request that consumes the token
- compare suppressed vs challenge-complete verification requests
- localize the first downstream request or route whose behavior should have changed if acceptance really took effect

### Failure mode 2: visible challenge never appears, but flow still completes
Likely causes:
- suppression/detection-only path
- low-risk classification
- analyst is looking for UI when the meaningful edge is backend handoff

Next move:
- focus on `onSuppress` and backend verify request rather than visual challenge instrumentation

### Failure mode 3: flow works once, then behaves differently after retry
Likely causes:
- `reset()` created a new session
- retries exhausted / failure thresholds changed lifecycle path
- host page is re-binding callbacks or reusing stale token state incorrectly

Next move:
- compare pre-reset vs post-reset token and callback sequences
- inspect whether a new session object is created

### Failure mode 4: iframe/lightbox flow looks noisy and hard to reason about
Likely causes:
- challenge lifecycle is split across frame and host page
- multiple message events are being conflated
- show/hide/resize events are distracting from token-handoff edge

Next move:
- log only event IDs plus session-token-carrying payloads first
- separate visibility events from token-bearing events

### Failure mode 5: analyst spends too much effort inside challenge UI internals
Likely causes:
- the real leverage point is configuration, callback, or verify handoff boundary
- page-side orchestration matters more than the visible puzzle implementation

Next move:
- move outward to `setConfig`, callbacks, `postMessage`, and verification requests

## 8. Environment assumptions
Arkose analysis often depends on preserving:
- page lifecycle timing
- session continuity up to verification
- real host-page orchestration around callback handling
- iframe/frame messaging order when hosted integration is used

Compared with some heavier token-family targets, the first high-value move is often lifecycle-boundary tracing rather than deep transform recovery.
In practice, that means separating:
- callback/message token visibility,
- verify/update submission,
- and the first accepted downstream consumer request.
That said, environment drift can still matter once challenge classification, suppression, or page-side risk handling is tied to runtime context.

## 9. Representative code / pseudocode / harness fragments

### Callback-wrapping sketch
```javascript
// sketch only
const patchArkoseConfig = () => {
  const origSetConfig = myArkose.setConfig;
  myArkose.setConfig = function(cfg) {
    const wrapped = { ...cfg };
    for (const name of ['onReady', 'onCompleted', 'onSuppress', 'onFailed', 'onError', 'onReset']) {
      if (typeof wrapped[name] === 'function') {
        const fn = wrapped[name];
        wrapped[name] = function(resp) {
          console.log(name, resp);
          return fn.apply(this, arguments);
        };
      }
    }
    return origSetConfig.call(this, wrapped);
  };
};
```

### Iframe-message observation sketch
```javascript
// sketch only
window.addEventListener('message', (event) => {
  try {
    const msg = JSON.parse(event.data);
    if (msg && msg.eventId) {
      console.log('arkose event', msg.eventId, msg.payload || null);
    }
  } catch (_) {}
});
```

### Compact run log template
```text
run:
  integration: hosted iframe lightbox
  start edge: postMessage challenge-open
  token handoff: challenge-complete payload.sessionToken
  backend verify: POST /account/verify
  first accepted consumer: GET /account/bootstrap
  path: challenge shown -> complete -> verify accepted -> bootstrap accepted
  retry behavior: reset() after completion creates new session
```

## 10. What to verify next
Once the first-pass lifecycle map exists, verify:
- whether suppression and visible challenge flows share the same host-page consumer
- whether multiple Arkose instances or iframes exist on the page
- whether `reset()` creates a fully new session in the target integration
- whether callback wiring changes across navigation or SPA transitions
- whether backend verification is immediate, deferred, or wrapped in additional app logic
- which first downstream consumer request, redirect, or session fetch actually proves acceptance mattered

## 11. What this page adds to the KB
This page adds another practical browser scenario pattern the KB needed:
- how to analyze a protection family around config, callback, iframe, and backend-handoff edges
- how to distinguish visible challenge state from session-token semantics
- how to localize message boundaries, verification boundaries, and the first accepted downstream consumer
- how to diagnose suppression, reset, retry, and verification confusion

## 12. Source footprint / evidence note
Primary grounding for this page comes from:
- `sources/browser-runtime/2026-03-14-arkose-funcaptcha-lifecycle-notes.md`
- `sources/browser-runtime/2026-03-16-arkose-first-consumer-and-iframe-boundary-notes.md`
- official Arkose Labs docs on client API, callbacks, response objects, Verify API, and iframe setup

This page is intentionally a practical workflow note built from integration/lifecycle semantics.
It is not an exploit recipe and does not claim undocumented internal challenge algorithm detail.

## 13. Topic summary
Arkose / FunCaptcha session and iframe workflow note is a concrete browser workflow page for cases where the real job is to map client setup, challenge suppression/show state, session-token handoff, iframe messaging, backend verification, and reset/retry behavior without confusing those layers.

It matters because many Arkose investigations stall not from lack of a visible token, but from misunderstanding where the token becomes host-page data, how iframe/lightbox events carry session state, when reset creates a new session, where backend verification actually decides the outcome, and which later request first proves that acceptance changed real application behavior.