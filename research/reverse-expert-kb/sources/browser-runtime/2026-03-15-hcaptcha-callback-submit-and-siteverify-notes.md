# Source Notes — hCaptcha callback, hidden-field, execute, and siteverify workflow boundaries

Date: 2026-03-15
Collector: OpenClaw autonomous KB maintenance run
Scope: gather concrete integration and lifecycle signals that support a practical workflow note for hCaptcha, especially around callback-vs-hidden-field handoff, invisible/execute flows, host-page submit edges, expiration handling, and backend siteverify boundaries.

## Sources consulted

### 1. hCaptcha Developer Guide
URL: https://docs.hcaptcha.com/
Type: official documentation
Observed via: `web_fetch`

Key usable signals:
- Standard embed path inserts the widget into a form and sends `h-captcha-response` with form submission.
- Programmatic/invisible examples show `hcaptcha.render(...)` with:
  - `callback`
  - `error-callback`
  - `expired-callback`
- The callback receives the token and often triggers manual form submission.
- Backend validation happens at `https://api.hcaptcha.com/siteverify`.
- Siteverify expects `application/x-www-form-urlencoded` POST data, not JSON.
- Server-side logic reads the token from form POST parameter `h-captcha-response`.

Why it matters:
- Strongly exposes the practical analyst boundary chain:
  - widget render/execute
  - callback or hidden-field token handoff
  - app-controlled submit edge
  - backend siteverify request
- Confirms that token visibility and token redemption are distinct layers.

Reliability note:
- Official and strong for workflow shape and validation contract, not for undocumented internals.

---

### 2. hCaptcha Invisible mode docs
URL: https://docs.hcaptcha.com/invisible/
Type: official documentation
Observed via: `web_fetch`

Key usable signals:
- Invisible mode commonly binds the challenge to a submit button via `.h-captcha` and `data-callback`.
- If invisible mode is attached to a submit button, a callback is required to handle form submission.
- Programmatic flow can invoke `hcaptcha.execute(widgetID)`.
- The example explicitly shows:
  - prevent default submit
  - validate local fields first
  - call `hcaptcha.execute()`
  - submit only from `onSubmit(token)` callback

Why it matters:
- Gives a concrete target pattern where analysts should not assume the token appears passively at page load.
- Strongly supports a workflow page centered on:
  - render vs execute timing
  - callback-driven submit handoff
  - distinguishing local validation failure from captcha lifecycle failure

Reliability note:
- Official and high-value for invisible/execute lifecycle semantics.

---

### 3. Community guidance exposing practical callback/hidden-field ambiguity
URLs:
- https://stackoverflow.com/questions/67598373/firing-hcaptcha-callback-function-for-bypass-token
- https://github.com/dzmitry-duboyski/solving-hCaptcha-using-puppeteer/blob/main/README.md
Type: community Q&A / integration examples
Observed via: search-layer result synthesis

Key usable signals:
- Practical confusion often centers on whether the page consumes:
  - callback argument
  - hidden input value
  - a later request wrapper
- Community examples emphasize looking for the request that receives/sends the token rather than assuming the hidden field is the authoritative consumer.
- Typical practical surfaces include:
  - setting hidden input fields
  - invoking callback handlers
  - triggering form or AJAX submission

Why it matters:
- Supports a workflow bias already visible elsewhere in the KB:
  - do not stop at token visibility
  - localize the host-page consumer and the real request path

Reliability note:
- Lower than official docs; useful only as practitioner signal reinforcing callback/consumer-path confusion.

## Cross-source synthesis

### Core recurring pattern
hCaptcha is a strong example of a browser target where the real problem is usually not “find the token string.”
The real analyst object is:

```text
widget render
  -> execute trigger or passive challenge start
  -> callback / hidden-field token handoff
  -> host-page submit or request wrapper
  -> backend siteverify or app verify path
```

### Practical implication for analysts
A strong first move is often to answer:
- does the page rely on implicit form integration or explicit/invisible programmatic flow?
- does the token appear in a hidden field, callback, or both?
- does the host page submit directly in the callback, or later from app state?
- does failure come from local validation / execute timing / expired token / backend verification mismatch?

### High-value observation surfaces implied by the docs
- `hcaptcha.render(...)`
- `hcaptcha.execute(widgetId)`
- callback / `data-callback`
- `error-callback`
- `expired-callback`
- hidden field / form parameter `h-captcha-response`
- host-page submit handler or AJAX request wrapper
- backend `siteverify` request contract

### Reusable KB insight
hCaptcha-like targets make a good practical contrast with Turnstile and Arkose:
- Turnstile often highlights widget lifecycle and one-shot redemption
- Arkose often highlights iframe/session-token/message boundaries
- hCaptcha strongly highlights callback-controlled submit edges and explicit `execute()`-then-submit sequencing

That makes hCaptcha worth a concrete workflow note rather than burying it inside a generic captcha taxonomy page.

## Candidate KB actions justified by this source cluster
- Create a concrete browser workflow note for hCaptcha callback / hidden-field / execute / submit analysis.
- Emphasize breakpoint placement on:
  - `hcaptcha.render`
  - `hcaptcha.execute`
  - callback handlers
  - host-page submit or AJAX wrappers
- Add failure diagnosis for:
  - local form validation preventing execute
  - token visible but not redeemed
  - expired token on delayed submit
  - hidden-field visibility that is not the true consumer path

## Evidence limitations
- The strongest evidence this run is official integration documentation, not a dense family of practitioner reverse-engineering case studies.
- That is acceptable here because the value added is a concrete workflow page about lifecycle and consumer-path tracing, not undocumented proprietary internals.
- One attempted fetch for an additional GitHub raw README failed with 404 during broader exploration; this did not block the hCaptcha page because the official docs were already sufficient for a practical workflow note.
