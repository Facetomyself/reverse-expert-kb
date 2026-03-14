# Source Notes — Arkose / FunCaptcha client lifecycle, iframe flow, and verification boundaries

Date: 2026-03-14
Collector: OpenClaw autonomous KB maintenance run
Scope: gather concrete lifecycle and target-shape signals for Arkose / FunCaptcha that support a practical browser workflow note focused on session-token handoff, iframe/message edges, callback timing, and verification boundaries.

## Sources consulted

### 1. Arkose Labs — Client API
URL: https://developer.arkoselabs.com/docs/client-api
Type: official product documentation
Observed via: `web_fetch`

Key usable signals:
- The browser integration exposes a `myArkose` object with public functions including:
  - `setConfig`
  - `run`
  - `reset`
  - `getConfig`
- `setConfig` is required because it defines callback behavior.
- `onReady` is the key edge showing the client is loaded and ready.
- `onCompleted` is the critical handoff edge because it includes `response.token`, which must be sent to the customer backend for verification.
- `reset()` creates a new session.

Usefulness for KB:
- Strongly supports treating Arkose as a lifecycle/state-machine target rather than as only a visible challenge widget.
- Suggests high-value hooks at `setConfig`, `run`, `reset`, and callback registration / firing.

Reliability note:
- Official and useful for lifecycle boundaries; not a reversing source for internals.

---

### 2. Arkose Labs — Callbacks
URL: https://developer.arkoselabs.com/docs/callbacks
Type: official product documentation
Observed via: `web_fetch`

Key usable signals:
- Enumerates callback sequence edges including:
  - `onReady`
  - `onShow`
  - `onShown`
  - `onSuppress`
  - `onCompleted`
  - `onHide`
  - `onFailed`
  - `onReset`
  - `onResize`
  - `onError`
  - `onWarning`
- `onCompleted` fires both when no challenge is needed and when a challenge is answered correctly.
- `onSuppress` means the session was classified as not needing a challenge.
- `onFailed` reflects exhausted retry thresholds / unrecoverable challenge failure.
- `onReset` fires on programmatic reset and after correct challenge completion.

Usefulness for KB:
- Strong evidence that Arkose analysis should distinguish:
  - suppressed/no-challenge completion
  - shown/interactive enforcement flow
  - reset/failure/retry transitions
- Very useful for practical failure diagnosis and compare-run planning.

Reliability note:
- Official lifecycle description; excellent for callback-state modeling.

---

### 3. Arkose Labs — Response Object
URL: https://developer.arkoselabs.com/docs/response-object-oncompleted-onerror-onfailed-onresize
Type: official product documentation
Observed via: `web_fetch`

Key usable signals:
- `response.token` is the token to send to backend verification.
- `response.completed`, `response.suppressed`, and `response.recoverable` help classify outcome state.
- `onFailed` and `onWarning` can still carry recovery-relevant information.
- `onShown`, `onSuppress`, and `onResize` expose sizing/session visibility state useful for iframe and lightbox flows.

Usefulness for KB:
- Gives practical structured fields analysts can log during runtime observation.
- Supports a workflow where token visibility is separated from broader session outcome state.

Reliability note:
- Official and good for concrete observation plans.

---

### 4. Arkose Labs — Verify API v4
URL: https://developer.arkoselabs.com/docs/verify-api-v4
Type: official product documentation
Observed via: `web_fetch`

Key usable signals:
- Verification is always performed server-side with the private key plus the session token from the client API.
- Verification is called whether or not an enforcement challenge was presented.
- Detect-only and challenge-served flows both end in Verify API processing.
- Response may be simple or full JSON and may receive additive new fields over time.
- Docs explicitly discuss handling of HTTP 5xx vs HTTP 400 differently.

Usefulness for KB:
- Strongly supports separating:
  - client-side token/session lifecycle
  - backend verification outcome
- Prevents the common analyst mistake of equating `response.token` capture with successful redemption semantics.

Reliability note:
- Official and highly useful for boundary conditions and integration semantics.

---

### 5. Arkose Labs — Iframe Setup Guide
URL: https://developer.arkoselabs.com/docs/iframe-setup-guide
Type: official product documentation
Observed via: `web_fetch`

Key usable signals:
- Arkose can be hosted in iframe form, including lightbox mode.
- The parent page and iframe communicate through `postMessage` with JSON payloads.
- Representative event IDs include:
  - `challenge-loaded`
  - `challenge-suppressed`
  - `challenge-complete`
  - `challenge-show`
  - `challenge-shown`
  - `challenge-hide`
  - `challenge-iframeSize`
  - `challenge-failed`
  - `challenge-error`
  - `challenge-warning`
- `challenge-complete` payload carries `sessionToken`.
- Lightbox mode explicitly uses `postMessage` to trigger `challenge-open` and listens for lifecycle events back from the iframe.

Usefulness for KB:
- Very strong support for an Arkose workflow note centered on iframe/message boundaries, token handoff, and challenge-visibility state.
- Suggests concrete hooks: `window.addEventListener('message', ...)`, `postMessage`, iframe size/show/hide transitions, and session-token extraction point.

Reliability note:
- Official and especially useful for concrete host-page/iframe workflow structure.

## Cross-source synthesis

### Concrete workflow shape that matters analytically
Arkose / FunCaptcha is best treated as a client-lifecycle + session-token + backend-verification problem, often with an iframe or lightbox boundary in the middle.

A practical decomposition is:
- client load / configuration
- callback registration
- optional explicit `run()` trigger
- challenge shown or suppressed
- session token emitted through callback or iframe message
- backend Verify API call
- reset / retry / failed / warning / hide transitions

### Practical implication for analysts
A good first move is usually not beautifying all of `client_api.js`.
It is to determine:
- whether the integration is inline, lightbox, or hosted iframe
- where `myArkose.setConfig(...)` registers callbacks
- whether the challenge is manually triggered via `run()` or a selector
- where the session token exits Arkose-managed state and enters host-page or backend-bound logic
- whether the interesting failure is in challenge completion, suppression logic, iframe messaging, or backend verification

### High-value observation surfaces implied by the docs
- `myArkose.setConfig`
- `myArkose.run`
- `myArkose.reset`
- `onCompleted`, `onSuppress`, `onFailed`, `onError`, `onReset`
- `window.addEventListener('message', ...)` for hosted iframe flows
- `postMessage` calls with `challenge-open`
- request from host application that forwards `response.token` or `sessionToken` to backend verification

### Reusable KB insight
Arkose-like cases are a good reminder that some browser protection targets are best modeled around the path:

```text
widget/client lifecycle
  -> callback or iframe message edge
  -> host-page consumer logic
  -> backend verification
```

not just around the visible challenge UI.

## Candidate KB actions justified by this source cluster
- Create a concrete workflow note for Arkose / FunCaptcha session-token and iframe-lifecycle analysis.
- Emphasize breakpoint/hook placement around config registration, callbacks, `run/reset`, `postMessage`, and backend verification handoff.
- Cross-link with Turnstile lifecycle and broader browser risk-control pages.
- Treat Arkose as another browser family where the key problem is often transition-boundary localization rather than only token-string capture.

## Evidence limitations
- Current material is mostly official integration documentation, not practitioner reversing casework.
- It is strong on lifecycle semantics and message boundaries, but weak on deep internal algorithm or telemetry-object detail.
- That is still useful because the KB currently needs more operational workflow notes around real integration boundaries and failure diagnosis.