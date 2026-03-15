# hCaptcha Callback, Submit, and Siteverify Workflow Note

Topic class: concrete target-family workflow note
Ontology layers: browser-runtime subdomain, protected-interaction workflow, validation-lifecycle analysis
Maturity: structured-practical
Related pages:
- topics/browser-side-risk-control-and-captcha-workflows.md
- topics/browser-parameter-path-localization-workflow-note.md
- topics/browser-request-finalization-backtrace-workflow-note.md
- topics/cloudflare-turnstile-widget-lifecycle-workflow-note.md
- topics/arkose-funcaptcha-session-and-iframe-workflow-note.md
- topics/browser-cdp-and-debugger-assisted-re.md

## 1. Why this page exists
This page exists because hCaptcha is a recurring browser protection shape where analysts often stop too early at one of three misleading milestones:
- the widget rendered
- the token became visible
- the hidden field exists

In practice, the more useful object is the workflow boundary chain:
- render mode and widget options
- execute timing or passive challenge start
- callback or hidden-field token handoff
- host-page submit / AJAX consumer path
- first accepted consumer request
- backend siteverify or app verification outcome
- expiration / retry / local-validation transitions

That makes hCaptcha a good concrete scenario page for the KB’s practical pivot.

## 2. Target pattern / scenario
### Typical target shape
An hCaptcha-protected page often has some combination of:
- script load from `https://js.hcaptcha.com/1/api.js`
- implicit widget embed using `.h-captcha`
- explicit/invisible flow using `hcaptcha.render(...)`
- submit-triggered execution using `hcaptcha.execute(widgetId)`
- token surfaced through:
  - callback argument
  - hidden form parameter `h-captcha-response`
- callback-controlled form submission or AJAX submission
- backend verification using `https://api.hcaptcha.com/siteverify`
- lifecycle callbacks such as:
  - `callback`
  - `error-callback`
  - `expired-callback`

### Analyst goal
The practical goal is usually one of:
- identify whether the page uses passive form integration or explicit execute-on-submit logic
- determine where the token first becomes app-consumable
- localize whether the host page consumes callback data, hidden input state, or a later store/request wrapper
- explain why a visible token still fails, expires, or never reaches the request that matters
- separate local form-validation gating from hCaptcha lifecycle gating

## 3. What matters first
Before beautifying large bundles, answer these questions:
1. Is the page using implicit form embedding or explicit `hcaptcha.render(...)`?
2. Is the challenge run automatically, or only after `hcaptcha.execute(widgetId)`?
3. Does the host page rely on callback submission, hidden-field submission, or both?
4. Which request actually carries the token?
5. Does failure happen before execute, after callback, at host-page submit, or during backend verification?
6. Is delayed submit causing expiration or stale state?

Those six answers usually produce more leverage than broad cleanup.

## 4. Concrete workflow: first pass

### Step 1: classify render and execution shape
Start by locating how hCaptcha is instantiated.

High-yield clues:
- implicit form flow:
  - `.h-captcha` container inside a form
  - token expected in `h-captcha-response`
- explicit render flow:
  - code calls `hcaptcha.render(...)`
- invisible/manual flow:
  - widget configured with invisible size
  - submit handler calls `hcaptcha.execute(widgetId)`
  - local validation may run before execute

Why this matters:
- execute-on-submit flows hide the important boundary later in the host page
- implicit form flows often make the hidden field visible earlier, but that still does not prove the real consumer path

### Step 2: anchor the first handoff edge
Do not stop at widget presence.
Find where token material first exits widget-managed state.

Common handoff edges:
- `callback(token, key)` or similar callback body
- hidden field `h-captcha-response`
- app state/store updated from callback
- submit handler that waits for token availability before continuing

Representative run log sketch:

```text
run A: page load only
  widget present
  no token

run B: submit click
  local validation passes
  execute() called
  callback receives token
  form submit begins

run C: delayed submit or retry
  expired callback fires or backend rejects
```

This separates token generation from token redemption.

### Step 3: find the true host-page consumer
Once token handoff is visible, answer:
- who reads the token next?
- is the callback itself submitting the form?
- does the page read the hidden field later?
- does an AJAX wrapper package the token with sibling fields?

Useful consumer edges:
- submit handler
- form serializer
- AJAX/fetch wrapper
- store/state update that later feeds request construction

Why this matters:
- many pages expose both callback and hidden-field surfaces, but only one is operationally authoritative

### Step 4: anchor the request that matters
Identify the request that actually redeems the token.

What to record:
- endpoint and method
- whether token travels in form body, JSON body, or another wrapper
- whether the request goes to the app backend first and only later to `siteverify`
- whether sibling fields or local validation state travel with the token

A compact artifact should look like:

```text
visible token surface:
  callback(token)

first consumer:
  onSubmit(token) -> form.submit()

request role:
  POST /login
  form field: h-captcha-response

backend verify:
  server calls /siteverify with response=<token>
```

### Step 4A: identify the first accepted consumer request
Do not stop at the first form submit or AJAX request that merely carries the token.
A recurring practical boundary is the **first later request, redirect, or state refresh that becomes accepted only after the hCaptcha transition succeeds**.

What to record:
- whether the token-carrying request itself returns the final allow/deny decision or only refreshes trust state
- which later request, route, or AJAX family first stops failing, degrading, or looping
- whether accepted and failed runs diverge first at token submission time or only one step later
- whether local validation, callback success, and backend verify all look correct while the protected action still fails downstream

Representative compare-run sketch:
```text
run A:
  callback(token)
  POST /login carries h-captcha-response
  redirect to /account succeeds

run B:
  callback(token)
  POST /login carries h-captcha-response
  redirect to /account returns challenge / degraded state

practical reading:
  callback and submit visibility were not enough;
  the first accepted consumer request localized the real acceptance boundary
```

Why this matters:
- some targets use the token-carrying submit as a validation/update edge rather than the true protected consumer
- the first accepted downstream consumer often gives the cleanest compare-run evidence
- this keeps the workflow aligned with the KB-wide four-boundary chain rather than stopping at token appearance or submission

### Step 5: map failure transitions
Treat hCaptcha as a small state machine.

Useful states:
- widget rendered
- local validation blocked submit
- execute triggered
- token available
- error callback
- expired callback
- host-page submit
- backend accepted / rejected

Minimal sketch:

```text
rendered
  -> local validation passes
  -> execute()
  -> callback(token)
  -> form/AJAX submit
  -> app backend
  -> siteverify
  -> accepted OR rejected
```

## 5. Where to place breakpoints / hooks

### A. `hcaptcha.render(...)`
Use when:
- you need to classify widget mode quickly
- you want callback registration and widget options

Inspect:
- sitekey
- size / invisible mode
- callback registration
- error / expired handlers
- container identity / widget id

Representative sketch:
```javascript
// sketch only
const origRender = hcaptcha.render;
hcaptcha.render = function(container, opts) {
  console.log('hcaptcha.render', { container, opts });
  debugger;
  return origRender.apply(this, arguments);
};
```

### B. `hcaptcha.execute(widgetId)`
Use when:
- the page may defer challenge start until submit
- token never appears during passive observation

Inspect:
- which submit path or button click triggers execute
- whether local validation can prevent execution entirely
- whether sibling form fields are already frozen at this point

### C. Callback body / `data-callback`
Use when:
- token visibility is the first stable edge
- you need the immediate downstream consumer

Inspect:
- token argument
- whether the callback submits the form directly
- whether the callback updates state and a later function submits
- whether callback fires again on retry or reset

### D. Hidden-field read site
Use when:
- the page visibly creates `h-captcha-response`
- it is unclear whether the host page actually consumes that field

Inspect:
- when `.value` is read
- whether the form serializer reads the field directly
- whether callback and hidden-field paths diverge

### E. Host-page submit / AJAX wrapper
Use when:
- token visibility is already solved
- the real unknown is why the request succeeds or fails

Inspect:
- exact request carrying token
- sibling fields bundled with token
- whether the app backend path or verify timing changes between accepted and failed runs

## 6. Practical compare-run methodology
A single visible token is often misleading.
Use controlled comparisons.

### Minimum useful axes
Change one axis at a time:
- implicit form flow vs explicit render flow
- page load only vs submit-triggered execute
- local validation failure vs valid local form state
- immediate submit vs delayed submit
- first callback path vs retry/expired path

### What to record
For each run, record:
- render mode
- execute trigger
- whether callback fired
- whether hidden field was populated
- who consumed the token first
- request carrying token
- whether expiration/error callbacks fired
- backend outcome

### Why this matters
hCaptcha-like targets can create false conclusions such as:
- “the widget is broken” when local validation prevented execute
- “the hidden field is the answer” when the real path is callback-driven AJAX submission
- “the token format is wrong” when delayed submit caused expiry
- “the request path is solved” when the callback path and request path were conflated

## 7. Failure modes and what they usually mean

### Failure mode 1: widget renders, but no token ever appears
Likely causes:
- execute is manual and never triggered
- local validation blocked the submit path before execute
- the analyst is observing page load instead of the real submit transition

Next move:
- break on submit handler
- check whether `hcaptcha.execute()` is called
- separate local validation failure from captcha lifecycle failure

### Failure mode 2: token is visible in callback, but request still fails
Likely causes:
- callback path is not the real request consumer path
- delayed submit caused token expiry
- host-page request is missing sibling fields or state
- backend verification rejects despite token visibility

Next move:
- inspect the actual request carrying the token
- compare immediate submit vs delayed submit
- inspect callback-to-request handoff, not just callback visibility

### Failure mode 3: hidden field exists, but app behavior still does not match
Likely causes:
- hidden field is diagnostic or compatibility-oriented, not the authoritative consumer
- the app submits via callback-driven JS path instead of raw form serialization

Next move:
- find the first read site of `h-captcha-response`
- compare hidden-field path against callback/body request path

### Failure mode 4: first run succeeds, later run fails
Likely causes:
- expiration or stale token state
- retry path changed lifecycle or app state
- the submit sequence changed after an earlier failure

Next move:
- compare first callback/submit vs second callback/submit
- log expired/error callbacks
- record whether a fresh execute precedes the later request

### Failure mode 5: analyst over-focuses on widget internals
Likely causes:
- the real leverage point is the host-page consumer path and backend verification boundary

Next move:
- shift focus outward to callback, hidden-field read, submit wrapper, and request-finalization boundaries

## 8. Environment assumptions
hCaptcha analysis often depends on preserving:
- realistic submit timing
- local form state required before execute
- same-page state until request submission
- host-page orchestration around callback handling

Compared with iframe-heavy families, the first useful move here is often not message tracing.
It is usually **submit-path tracing**: what conditions cause execute, how the callback hands off the token, and which request actually consumes it.

## 9. Representative code / pseudocode / harness fragments

### Render/execute instrumentation sketch
```javascript
// sketch only
const hookHCaptcha = () => {
  const origRender = hcaptcha.render;
  const origExecute = hcaptcha.execute;

  hcaptcha.render = function(container, opts) {
    console.log('render', { container, opts });
    return origRender.apply(this, arguments);
  };

  hcaptcha.execute = function(widgetId) {
    console.log('execute', { widgetId });
    return origExecute.apply(this, arguments);
  };
};
```

### Callback wrapping sketch
```javascript
// sketch only
function wrapCallback(fn) {
  return function(token, key) {
    console.log('hcaptcha callback', { token, key });
    debugger;
    return fn && fn.apply(this, arguments);
  };
}
```

### Compact run log template
```text
run:
  render mode: explicit invisible
  execute edge: submit click after local validation
  handoff: callback(token)
  consumer: onSubmit -> fetch('/login')
  request field: JSON body captchaToken
  outcome: immediate submit accepted, delayed submit rejected
```

## 10. What to verify next
Once the first-pass lifecycle map exists, verify:
- whether callback and hidden-field paths are redundant or semantically different
- whether multiple widgets or multiple submit paths exist on the page
- whether the app backend transforms token packaging before verification
- whether delayed submit or retry creates stale-token confusion
- whether the next best move is:
  - parameter-path localization
  - request-finalization backtrace
  - compare-run diagnosis
  - minimal externalization of a verified submit path

## 11. What this page adds to the KB
This page adds another concrete browser scenario pattern the KB needed:
- how to analyze callback-controlled submit flows
- how to separate widget visibility from request redemption
- how to diagnose local-validation, execute-timing, expiration, and hidden-field confusion
- how to move from token appearance to the actual request and verification path

## 12. Source footprint / evidence note
Primary grounding for this page comes from:
- `sources/browser-runtime/2026-03-15-hcaptcha-callback-submit-and-siteverify-notes.md`
- official hCaptcha docs on widget integration, invisible mode, callback handling, execute flow, and siteverify

This page is intentionally a practical workflow note built from documented lifecycle and integration behavior.
It is not an exploit recipe and does not claim undocumented internals.

## 13. Topic summary
hCaptcha callback, submit, and siteverify workflow note is a concrete browser workflow page for cases where the real job is to map render/execute timing, callback or hidden-field handoff, host-page submit behavior, and backend verification boundaries without confusing those layers.

It matters because many hCaptcha investigations fail not from lack of a token string, but from misunderstanding when execute actually runs, who consumes the token first, whether the hidden field is authoritative, and where the host page truly redeems the token.
