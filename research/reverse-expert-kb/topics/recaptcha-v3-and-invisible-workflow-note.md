# reCAPTCHA v3 and Invisible Workflow Note

Topic class: concrete target-family workflow note
Ontology layers: browser-runtime subdomain, protected-interaction workflow, validation-lifecycle analysis
Maturity: structured-practical
Related pages:
- topics/browser-side-risk-control-and-captcha-workflows.md
- topics/browser-parameter-path-localization-workflow-note.md
- topics/browser-request-finalization-backtrace-workflow-note.md
- topics/cloudflare-turnstile-widget-lifecycle-workflow-note.md
- topics/hcaptcha-callback-submit-and-siteverify-workflow-note.md
- topics/browser-cdp-and-debugger-assisted-re.md

## 1. Why this page exists
This page exists because reCAPTCHA is one of the most common browser protection families, but it is also one of the easiest to misunderstand if the analyst stops at the wrong milestone.

The weak milestones are usually:
- the script loaded
- the widget appeared
- `grecaptcha.execute(...)` returned a token
- the hidden field existed

The more useful object is the full workflow boundary chain:
- render / ready / execute timing
- callback, hidden-field, or direct-token handoff
- first real host-page consumer
- request carrying the token
- backend `siteverify` outcome
- expiry, duplicate-use, score, and action mismatch diagnosis

This page is therefore not a generic reCAPTCHA overview.
It is a practical workflow note for the two most common browser-side analyst shapes:
- **reCAPTCHA v3 score/action flow**
- **Invisible reCAPTCHA callback/submit flow**

## 2. Target pattern / scenario
### Typical target shapes
A representative v3 flow looks like:

```text
page action or sensitive event
  -> grecaptcha.ready(...)
  -> grecaptcha.execute(sitekey, { action: 'login' })
  -> token returned in promise continuation
  -> app request carries token
  -> backend siteverify checks success + action + score + hostname
  -> app accepts, escalates, or rejects
```

A representative invisible flow looks like:

```text
user submit or app-triggered validation
  -> grecaptcha.render(...) or auto-bound button
  -> grecaptcha.execute(widgetId) or implicit trigger
  -> callback(token) / hidden field / getResponse()
  -> form or AJAX consumer
  -> backend siteverify
  -> accepted / expired / duplicate / error / reset
```

### Analyst goal
The practical goal is usually one or more of:
- determine where reCAPTCHA actually executes
- localize where the token first becomes app-consumable
- distinguish callback-driven submit from hidden-field or `getResponse()`-driven submit
- identify the request that actually redeems the token
- explain whether failure comes from host-page wiring, stale token reuse, backend verification mismatch, or v3 score/action policy

## 3. What matters first
Before cleaning large bundles, answer these questions:
1. Is this mainly a **v3 action/score** flow or an **invisible callback/widget** flow?
2. What event really triggers execution: page load, click, local validation pass, or a later AJAX boundary?
3. Where does the token first exit widget/runtime-managed state?
4. Which request actually carries the token to the application backend?
5. Is backend verification sensitive to **action**, **score**, **hostname**, timing, or duplicate use?
6. Is failure happening before execute, after callback, at host-page submit, or at `siteverify`/server-policy evaluation?

Those answers usually create more leverage than broad deobfuscation.

## 4. Concrete workflow: first pass

### Step 1: classify v3 vs invisible family first
Do not treat all reCAPTCHA pages as the same.

#### Case A: v3 action/score flow
High-yield signs:
- `grecaptcha.execute(sitekey, { action: '...' })`
- no obvious visible challenge widget
- token appears in promise continuation rather than a classic widget callback
- backend verification logic likely checks `action` and score

#### Case B: invisible callback/widget flow
High-yield signs:
- `.g-recaptcha`
- `data-size="invisible"`
- `data-callback`
- explicit `grecaptcha.render(...)`
- `grecaptcha.execute(widgetId)` and/or `grecaptcha.getResponse(widgetId)`
- `g-recaptcha-response` hidden-field path

This split matters because the most useful breakpoint surfaces differ.

### Step 2: anchor the real execute edge
The script being loaded is not the interesting boundary.
The interesting boundary is when the page actually asks reCAPTCHA for a token.

Representative run notes:

```text
run A: page load only
  api.js loaded
  no execute
  no token

run B: submit click with valid local state
  grecaptcha.execute(...) runs
  token returned
  request immediately dispatched

run C: submit click with local validation failure
  execute never runs
```

This prevents the classic mistake of blaming reCAPTCHA when the host page never reached the execution path.

### Step 3: capture the first token handoff edge
Once execute is known, capture the first application-visible token edge.

Common handoff surfaces:
- promise continuation from `grecaptcha.execute(...).then(function(token) { ... })`
- callback named in `data-callback` or render parameters
- hidden field `g-recaptcha-response`
- `grecaptcha.getResponse(widgetId)` read site
- app store/state write that later feeds request assembly

Useful scratch artifact:

```text
execute edge:
  click submit -> grecaptcha.execute(sitekey, { action: 'login' })

handoff:
  then(token) -> loginRequest({ recaptchaToken: token })

alternate surface:
  hidden field present but not authoritative
```

### Step 4: identify the true consumer request
Token visibility is not the end of the workflow.
Find the first request that materially redeems the token.

What to record:
- endpoint and method
- whether token is sent in form body, JSON, header wrapper, or another field name
- whether the app backend verifies directly against `siteverify` or gates additional policy first
- whether other fields travel together with the token

Compact artifact:

```text
visible token surface:
  execute(...).then(token)

first consumer:
  POST /api/login with body.recaptchaToken

backend expectations:
  siteverify success
  action='login'
  score >= threshold
```

### Step 5: classify backend verification failure mode
This family especially rewards separating client-side success from backend acceptance.

Common backend-side causes:
- token older than two minutes
- duplicate or replayed token
- hostname mismatch
- action mismatch for v3
- score below policy threshold
- malformed or missing token packaging in the app request

This is where many apparently “correct” client traces stop being enough.

## 5. Where to place breakpoints / hooks

### A. `grecaptcha.ready(...)`
Use when:
- page scripts may race the library load
- it is unclear which code path is waiting for reCAPTCHA availability

Inspect:
- registration timing
- which sensitive actions are wrapped by ready
- whether multiple execute sites exist on the same page

### B. `grecaptcha.execute(...)`
Use when:
- the real question is when token generation actually occurs
- v3 or invisible mode is execute-driven
- host-page validation may gate execution

Inspect:
- sitekey or widget id
- `action` for v3
- exact user/page event that triggers execute
- whether execute happens once or repeatedly across retries

Representative sketch:
```javascript
// sketch only
const origExecute = grecaptcha.execute;
grecaptcha.execute = function() {
  console.log('grecaptcha.execute', arguments);
  debugger;
  return origExecute.apply(this, arguments);
};
```

### C. Callback / promise continuation boundary
Use when:
- token generation is known
- the next unknown is who consumes the token first

Inspect:
- callback argument or promise `token`
- whether the callback submits immediately
- whether the continuation stores state and a later helper submits
- whether UI-only work happens before the operational consumer

### D. `grecaptcha.getResponse(...)` or hidden-field read site
Use when:
- the page visibly exposes `g-recaptcha-response`
- it is unclear whether that surface is authoritative

Inspect:
- first read site of `g-recaptcha-response`
- whether callback and hidden-field paths converge or diverge
- whether `getResponse()` is called only at submit time

### E. Host-page request-finalization boundary
Use when:
- token visibility is already solved
- the real unknown is why backend acceptance differs

Inspect:
- field name used to carry the token
- sibling fields that travel with it
- whether action/context is implicitly encoded elsewhere in the request
- timing from token creation to dispatch

## 6. Practical compare-run methodology
A single successful-looking token is often misleading.
Use controlled comparisons.

### Minimum useful axes
Change one axis at a time:
- page load only vs sensitive-action trigger
- local validation fail vs validation pass
- immediate submit vs delayed submit
- first submit vs replay/duplicate submit
- v3 action `login` vs `register` / `checkout`
- callback path vs hidden-field read path

### What to record
For each run, record:
- family: v3 or invisible
- execute trigger
- action name if v3
- token handoff surface
- first consumer request
- time between token creation and redemption
- whether the result was accepted, low-score-routed, expired, or duplicate-rejected

### Why this matters
This family produces common false conclusions such as:
- “execute is broken” when local validation never allowed it to run
- “the token format is wrong” when the token simply expired
- “the callback path is solved” when the real consumer is a later request wrapper
- “the backend rejected a valid token” when `action` mismatched expected context

## 7. Failure modes and what they usually mean

### Failure mode 1: token is visible, but the app still fails
Likely causes:
- token was not attached to the real request
- backend verification expects a specific v3 `action`
- token expired or was reused
- score was below the app’s threshold

Next move:
- inspect the actual consumer request
- capture verification-sensitive fields and timing
- compare first redemption vs replay

### Failure mode 2: no token appears even though api.js loaded
Likely causes:
- `grecaptcha.ready(...)` path never progressed to execute
- local validation blocked the submit path
- the analyst observed page load rather than the sensitive action boundary

Next move:
- break on the submit/action handler
- confirm whether `grecaptcha.execute(...)` is actually called

### Failure mode 3: hidden field exists, but behavior still does not match
Likely causes:
- hidden field is not the authoritative consumer path
- callback/promise continuation drives AJAX submission directly
- page reads token later through `getResponse()` instead

Next move:
- find the first read site of the hidden field or `getResponse()`
- compare that against callback/continuation-driven request assembly

### Failure mode 4: first run succeeds, second run fails with the same shape
Likely causes:
- single-use token rule
- two-minute token lifetime exceeded
- page reset or duplicate submission path changed state

Next move:
- compare first redemption vs second redemption explicitly
- record whether a fresh execute happened before the second request

### Failure mode 5: v3 flow looks correct, but server outcome still differs unexpectedly
Likely causes:
- action mismatch
- threshold/score policy, not raw token validity
- hostname mismatch or backend policy layered above `siteverify`

Next move:
- treat v3 as a policy-sensitive flow, not only a token-presence flow
- record expected action and decision threshold in run notes

## 8. Environment assumptions
reCAPTCHA analysis often depends on preserving:
- realistic user/page event timing
- the host page’s validation and submit orchestration
- same-page state between execute and redemption
- prompt token use after generation

Compared with some heavier anti-bot families, the first useful move is often not deep deobfuscation.
It is usually **execution and redemption tracing**: what triggers execute, where the token first becomes meaningful to the app, and which request actually redeems it under backend policy.

## 9. Representative code / pseudocode / harness fragments

### Execute/continuation instrumentation sketch
```javascript
// sketch only
const origExecute = grecaptcha.execute;
grecaptcha.execute = function() {
  const ret = origExecute.apply(this, arguments);
  console.log('execute args', arguments);
  if (ret && typeof ret.then === 'function') {
    return ret.then(token => {
      console.log('recaptcha token', token);
      debugger;
      return token;
    });
  }
  return ret;
};
```

### Invisible callback wrapping sketch
```javascript
// sketch only
function wrapRecaptchaCallback(fn) {
  return function(token) {
    console.log('recaptcha callback token', token);
    debugger;
    return fn && fn.apply(this, arguments);
  };
}
```

### Compact run log template
```text
run:
  family: v3
  execute edge: login button click
  action: login
  handoff: execute().then(token)
  consumer: POST /api/login
  backend expectation: action=login, score>=0.5
  outcome: immediate submit accepted, delayed replay timeout-or-duplicate
```

## 10. What to verify next
Once the first-pass lifecycle map exists, verify:
- whether multiple execute sites or multiple widgets exist on the page
- whether callback, hidden-field, and `getResponse()` surfaces are redundant or semantically different
- whether the app backend transforms token packaging before verification
- whether v3 policy branches depend on action/score rather than only `success`
- whether the next best move is:
  - request-finalization tracing
  - parameter-path localization
  - compare-run diagnosis
  - minimal externalization of a verified submit path

## 11. What this page adds to the KB
This page adds a concrete browser workflow pattern the KB was missing:
- a reCAPTCHA-specific execution/redemption workflow
- explicit separation of v3 action-score flow from invisible callback flow
- breakpoint placement around `ready`, `execute`, callback/continuation, hidden-field or `getResponse()`, and request-finalization boundaries
- failure diagnosis that treats duplicate use, short token lifetime, and action/score policy as first-class issues

That is much closer to how analysts actually get stuck on real targets than a generic taxonomy page.

## 12. Source footprint / evidence note
Primary grounding for this page comes from:
- `sources/browser-runtime/2026-03-15-recaptcha-v3-and-invisible-workflow-notes.md`
- official Google reCAPTCHA docs for v3, invisible mode, and verification

This page intentionally stays workflow-centered:
- it does not claim undocumented internal algorithm details
- it treats third-party developer material as directional support rather than normative proof
- it focuses on real analyst boundaries: execute, handoff, consumer request, and backend acceptance

## 13. Topic summary
reCAPTCHA v3 and invisible workflow analysis is a concrete browser workflow for cases where the real task is to map execution timing, token handoff, host-page consumption, and backend verification boundaries without confusing those layers.

It matters because many reCAPTCHA investigations fail not from lack of a token string, but from misunderstanding when execute actually runs, whether the token is consumed by callback or request wrapper, how short-lived and single-use the token is, and how v3 action/score policy changes backend acceptance.