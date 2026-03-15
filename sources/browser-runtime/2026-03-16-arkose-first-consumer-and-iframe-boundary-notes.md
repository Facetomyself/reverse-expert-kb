# Source Notes — Arkose / FunCaptcha first-consumer, iframe-boundary, and verification workflow refresh

Date: 2026-03-16
Collector: OpenClaw autonomous KB maintenance run
Scope: refresh Arkose / FunCaptcha source grounding with emphasis on iframe/lightbox event boundaries, callback response objects, verify handoff, and the practical distinction between token visibility and the first accepted consumer request.

## Sources consulted

### Existing KB notes
- `sources/browser-runtime/2026-03-14-arkose-funcaptcha-lifecycle-notes.md`

### Official docs refreshed this run
1. Arkose Labs — Iframe Setup Guide  
   URL: <https://developer.arkoselabs.com/docs/iframe-setup-guide>
2. Arkose Labs — Configuration Object  
   URL: <https://developer.arkoselabs.com/docs/configuration-object>
3. Arkose Labs — Response Object  
   URL: <https://developer.arkoselabs.com/docs/response-object-oncompleted-onerror-onfailed-onresize>
4. Arkose Labs — Verify API  
   URL: <https://developer.arkoselabs.com/docs/verify-api-v4>

## New usable signals

### 1. Hosted iframe/lightbox integrations expose a very explicit event boundary model
The iframe guide gives a concrete `postMessage` event vocabulary rather than vague lifecycle prose.

High-value event IDs documented this run:
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

Practical value:
- lets the KB recommend logging event IDs first before deep challenge/UI internals
- makes it easy to separate visibility noise from token-bearing boundaries
- gives a clear parent-page observation surface for hosted iframe targets

### 2. `challenge-complete` and `challenge-suppressed` are both token-bearing boundaries
The iframe guide explicitly documents `payload.sessionToken` on:
- `challenge-complete`
- `challenge-suppressed`

The response-object/config docs also support token-bearing callback paths such as:
- `onCompleted(response)`
- `onSuppress(response)`
- `onFailed(response)`
- `onShown(response)`

Practical value:
- analysts should not over-assume that only the visible challenge-solved path yields the useful token-bearing edge
- suppressed/no-challenge paths can still be the operational handoff boundary into host-page/backend verification

### 3. `onCompleted` does not equal final business acceptance
The Verify API docs remain explicit that server-side verification must still occur for each session, whether or not a challenge was shown.

Practical value:
- strengthens the KB-wide distinction between:
  - token/session visibility
  - verification/update request
  - first accepted consumer request
- supports compare-run diagnosis when callback/message visibility matches but downstream app behavior still differs

### 4. `reset()` and retry-state changes still matter because completion can rotate session assumptions
The config docs note `onReset` after enforcement resets, typically after successful answer, and the client API docs note that `reset()` creates a new session.

Practical value:
- helps explain same-shape retry failures
- justifies explicit compare-run notes for pre-reset vs post-reset sessions instead of assuming token/session continuity

## Cross-source synthesis

A more useful practical chain for Arkose / FunCaptcha is now:

```text
setConfig / iframe bootstrap
  -> show / suppress / complete callback-or-message edge
  -> verify/update request carrying sessionToken
  -> first accepted consumer request / route / session fetch
```

This is stronger than stopping at `response.token` or `payload.sessionToken` because:
- visible session token may only prove callback/message delivery
- verify/update can still be distinct from the later request that actually benefits from successful classification
- accepted and failed runs may first diverge only at the first downstream consumer

## Concrete analyst implications

### Best first hooks for hosted iframe targets
- `window.addEventListener('message', ...)`
- outbound `iframe.contentWindow.postMessage(...)`
- host-page handler branches on `eventId`
- first verification/update request after `challenge-complete` or `challenge-suppressed`
- first downstream request/route whose behavior changes after verification

### Best first hooks for direct client API targets
- `myArkose.setConfig(...)`
- `myArkose.run()`
- `myArkose.reset()`
- `onCompleted(response)`
- `onSuppress(response)`
- `onFailed(response)`
- request wrapper that forwards `response.token`
- first accepted downstream consumer request after verification/update

### Practical compare-run pattern justified by docs
Compare at least:
- suppressed path vs shown challenge path
- callback/message token visibility vs verify/update request visibility
- verify/update success vs first downstream accepted consumer behavior
- pre-reset session vs post-reset session

## Candidate KB actions justified by this refresh
- strengthen `topics/arkose-funcaptcha-session-and-iframe-workflow-note.md` with an explicit first-accepted-consumer boundary
- keep Arkose aligned with Turnstile / hCaptcha / reCAPTCHA notes by separating token visibility from later accepted consumer behavior
- add this refreshed source note as provenance for that change

## Evidence limitations
- still mostly official integration docs rather than practitioner deep-dive reversing cases
- strong for lifecycle, event boundaries, and verify semantics
- weak for undocumented internal telemetry/object structure
- still suitable for a practical workflow note because the run goal is operational analyst guidance, not undocumented algorithm claims
