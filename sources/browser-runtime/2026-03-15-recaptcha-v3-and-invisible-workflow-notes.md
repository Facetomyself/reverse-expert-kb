# reCAPTCHA v3 / Invisible Workflow Notes

Date: 2026-03-15
Branch: browser-runtime practical workflow expansion
Focus: concrete analyst workflow for `grecaptcha.execute(...)`, callback/action handoff, hidden-field or direct-token consumption, and backend `siteverify` boundaries

## Why this source note exists
The browser subtree already had concrete notes for Turnstile, hCaptcha, Arkose, GeeTest, DataDome, Kasada, PerimeterX, Akamai, and several signature/cookie families, but it lacked a practical workflow note for reCAPTCHA.

That left a real gap because reCAPTCHA is one of the most common browser-side validation families where analysts repeatedly confuse:
- widget presence with meaningful workflow progress
- token visibility with actual redemption
- `grecaptcha.execute(...)` timing with host-page submit timing
- token existence with backend acceptance
- v3 `action` semantics with generic token semantics

## Core workflow facts pulled from official docs
### reCAPTCHA v3
Official docs (`/recaptcha/docs/v3`) emphasize:
- v3 is score-based and can run without user friction
- it can be bound automatically or invoked programmatically
- `grecaptcha.ready(...)` should guard execute calls to avoid library race conditions
- `grecaptcha.execute(sitekey, { action: 'submit' })` returns a token through `.then(function(token) { ... })`
- the token should be sent immediately to the backend for verification
- backend verification should confirm expected `action`
- `siteverify` response can include `success`, `score`, `action`, `challenge_ts`, `hostname`, and `error-codes`
- Google suggests actions such as login / register / purchase and says action names should be verified server-side
- default threshold guidance starts around `0.5`, but real thresholds depend on traffic context

### Invisible reCAPTCHA
Official docs (`/recaptcha/docs/invisible`) emphasize:
- invisible mode can be automatically bound to a button, explicitly rendered, or programmatically invoked
- common HTML/API surfaces include:
  - `.g-recaptcha`
  - `data-sitekey`
  - `data-callback`
  - `data-size="invisible"`
  - `data-expired-callback`
  - `data-error-callback`
- JavaScript API surfaces include:
  - `grecaptcha.render(...)`
  - `grecaptcha.execute(opt_widget_id)`
  - `grecaptcha.reset(opt_widget_id)`
  - `grecaptcha.getResponse(opt_widget_id)`
- client-side validation frequently gates whether `execute()` runs at all
- callback-style submission remains a common integration shape

### Verification / redemption
Official docs (`/recaptcha/docs/verify`) emphasize:
- token sources on web are commonly:
  - `g-recaptcha-response` POST field
  - `grecaptcha.getResponse(...)`
  - callback argument from `data-callback` / `grecaptcha.render({ callback: ... })`
- backend verification endpoint is `https://www.google.com/recaptcha/api/siteverify`
- POST parameters include `secret`, `response`, optional `remoteip`
- each token is valid for **two minutes** and can be verified **once only**
- duplicate or stale use produces `timeout-or-duplicate`

## Practical workflow implications for the KB
### 1. The first useful split is v3 score-flow vs invisible callback-flow
A practical reCAPTCHA page should explicitly separate:
- **v3 action-scored token flow**
  - often `grecaptcha.execute(sitekey, { action })`
  - token passed into backend request
  - server verifies `action` + score
- **invisible widget / callback flow**
  - often rendered widget + `data-callback`
  - token reaches callback, hidden field, or `getResponse()` consumer
  - server verifies one-time/short-lived token

This split is more useful operationally than a generic “reCAPTCHA” page because analysts usually get stuck at different boundaries in these two families.

### 2. Token visibility is not enough
The practical object is:
```text
render / ready / execute edge
  -> token handoff edge
  -> first real host-page consumer
  -> request carrying token
  -> backend siteverify outcome
```
That is exactly the same correction pattern already visible in the KB’s Turnstile and hCaptcha notes.

### 3. `action` is a first-class recovery object in v3
For v3, `action` is not just a convenience label.
It is part of the server-side acceptance contract and should be treated as a tracked field in run notes.

Useful compact artifact:
```text
execute edge:
  grecaptcha.execute(sitekey, {action: 'login'})

handoff:
  token passed into login AJAX wrapper

verification expectations:
  backend checks success + hostname + action='login' + score>=threshold
```

### 4. Client-side validation often hides the true execute boundary
Invisible integrations frequently look broken when the real cause is:
- local form validation blocked `execute()`
- submit button path never reached the real callback
- analyst watched page load instead of submit transition

This is the same kind of “host-page orchestration matters more than widget internals” lesson already seen in hCaptcha/Turnstile.

### 5. Replay confusion should be expected
Because tokens are short-lived and single-use, analysts can easily make false conclusions such as:
- “the token format is wrong” when it was simply stale
- “the callback path is broken” when the token was already redeemed once
- “the backend rejects my request shape” when `action` mismatched expected context

## Concrete hook/breakpoint surfaces worth capturing
### v3
- `grecaptcha.ready(...)`
- `grecaptcha.execute(sitekey, { action })`
- `.then(function(token) { ... })` continuation
- first request wrapper that receives the token
- backend request payload field carrying the token

### Invisible
- `grecaptcha.render(...)`
- `grecaptcha.execute(widgetId)`
- callback function named in `data-callback` / render params
- `grecaptcha.getResponse(widgetId)` read site
- `grecaptcha.reset(widgetId)`
- hidden-field reads/writes involving `g-recaptcha-response`

## Practical compare-run axes worth preserving
- page load only vs submit-triggered execute
- local validation fail vs validation pass
- immediate submit vs delayed submit
- first redemption vs replay/duplicate redemption
- action=`login` vs action=`signup` or other named actions
- callback-driven submit vs hidden-field read path

## Search-result additions worth carrying forward conservatively
Search results outside official docs were noisier, but still directionally useful for workflow shaping:
- developer/tutorial material repeatedly reinforces that `grecaptcha.execute(...)` is often wired immediately before submit or AJAX dispatch
- v3 examples repeatedly show `action` as a meaningful backend-verified field rather than only a frontend label
- community posts suggest a common analyst bottleneck is finding the real callback/consumer path when visible widget artifacts are minimal or absent

These were useful as workflow evidence, but should not be overclaimed as normative internals.

## Conservative synthesis for the KB page
A practical KB page should:
- cover both v3 score-flow and invisible execute/callback-flow in one concrete workflow note
- center the page on analyst bottlenecks:
  - where execute really runs
  - where the token first becomes app-consumable
  - which request actually redeems it
  - how backend verification semantics explain failure
- explicitly elevate:
  - `action`
  - `score`
  - token two-minute lifetime
  - single-use / duplicate rejection
  - callback vs hidden-field vs `getResponse()` consumption
- avoid pretending the widget internals matter more than host-page orchestration and backend verification boundaries

## Candidate page title
- `topics/recaptcha-v3-and-invisible-workflow-note.md`

## Primary sources
- https://developers.google.com/recaptcha/docs/v3
- https://developers.google.com/recaptcha/docs/invisible
- https://developers.google.com/recaptcha/docs/verify

## Supplementary search traces used for orientation
- search-layer query cluster around:
  - `reCAPTCHA v3 execute callback action token workflow siteverify`
  - `grecaptcha execute callback submit token first consumer request`
  - `reCAPTCHA invisible callback siteverify workflow action parameter`
- useful result classes included:
  - official Google reCAPTCHA docs
  - directionally useful developer/tutorial discussions reinforcing execute-on-submit and backend action verification

## Evidence-quality note
This source note is grounded primarily in official Google docs and uses noisy third-party material only to help choose practical workflow emphasis. It should therefore support a conservative, workflow-centered KB page rather than speculative claims about undocumented internal implementation.