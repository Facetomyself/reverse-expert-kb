# Run Report — 2026-03-14 20:16 Asia/Shanghai

## 1. Scope this run
Continue the KB’s practical/case-driven correction by adding another concrete browser protection-family workflow note rather than expanding abstract taxonomy.

This run focused on Arkose / FunCaptcha as a lifecycle-heavy target where the analyst’s real problem is often not a hidden algorithm, but the path from client setup to callback/iframe message, session-token handoff, backend verification, and reset/retry semantics.

## 2. New findings

### A. Arkose is best modeled as a client/session lifecycle, not just a visible challenge
The official docs make the key browser-side edges explicit:
- `myArkose.setConfig(...)`
- `myArkose.run()`
- `myArkose.reset()`
- `onReady`
- `onCompleted`
- `onSuppress`
- `onFailed`
- `onReset`
- `onError`

That makes Arkose a strong example of a target where workflow boundaries matter more than vague "captcha" classification.

### B. Session-token handoff is the highest-value practical boundary
The most useful concrete handoff surfaces are:
- `onCompleted(response)` with `response.token`
- suppression/completion callbacks in no-challenge or detect-only paths
- hosted iframe `challenge-complete` messages carrying `payload.sessionToken`
- the host-page request that forwards the token into backend verification

This aligns well with the human’s instruction to emphasize parameter-path localization and transition-boundary tracing.

### C. Hosted iframe/lightbox integrations create a separate message-boundary problem
Arkose’s iframe docs make `postMessage` part of the normal integration surface.
That means a practical Arkose workflow should explicitly include:
- `challenge-open` outbound trigger
- inbound `message` events such as `challenge-loaded`, `challenge-show`, `challenge-shown`, `challenge-complete`, `challenge-hide`, `challenge-failed`, and `challenge-error`
- separation between visibility events and token-bearing events

This is exactly the sort of grounded site/protection-family-specific structure the KB needed more of.

### D. Backend verification is a distinct boundary from client-side completion
The Verify API docs clearly show that:
- verification is always server-side
- it happens whether or not a visible challenge was shown
- client-side token visibility should not be conflated with verified success

This gives a concrete explanation for a common analyst failure mode: thinking the problem is solved as soon as a session token appears in browser-side callbacks.

### E. Reset and suppression deserve first-class treatment
`reset()` creates a new session, and `onSuppress` means the session completed without a visible challenge.
Those two lifecycle details materially change how compare-run experiments should be designed.

## 3. Sources consulted
- `sources/browser-runtime/2026-03-14-arkose-funcaptcha-lifecycle-notes.md`
- Official Arkose Labs docs:
  - `https://developer.arkoselabs.com/docs/client-api`
  - `https://developer.arkoselabs.com/docs/callbacks`
  - `https://developer.arkoselabs.com/docs/response-object-oncompleted-onerror-onfailed-onresize`
  - `https://developer.arkoselabs.com/docs/verify-api-v4`
  - `https://developer.arkoselabs.com/docs/iframe-setup-guide`
- Search-layer exploratory query cluster over Arkose / FunCaptcha client lifecycle, callbacks, verify API, and iframe integration

## 4. Reflections / synthesis
This run continued the browser subtree’s shift from abstract grouping toward practical scenario coverage.

The browser subtree now has several genuinely different concrete workflow surfaces:
- Reese84 / ___utmvc -> request-shaping / token attachment / state drift
- DataDome / GeeTest / Kasada -> family-differentiated first-pass workflow
- Turnstile -> widget render/execute/handoff/redemption lifecycle
- Arkose / FunCaptcha -> config/callback/message/verify lifecycle with explicit iframe/lightbox branch

That is healthier than adding more general theory pages because it gives analysts repeatable starting points for real families.

A useful broader synthesis from this run:
some browser protection targets are best understood by localizing the transition where protection-managed state becomes host-page-controlled state.
For Arkose, that transition often sits at callback or iframe-message boundaries rather than deep inside visible challenge internals.

## 5. Candidate topic pages to create or improve
Created this run:
- `topics/arkose-funcaptcha-session-and-iframe-workflow-note.md`

Created source note this run:
- `sources/browser-runtime/2026-03-14-arkose-funcaptcha-lifecycle-notes.md`

Improved this run:
- `index.md`
- `topics/browser-runtime-subtree-guide.md`
- `topics/browser-side-risk-control-and-captcha-workflows.md`
- `topics/browser-fingerprint-and-state-dependent-token-generation.md`

Candidate future practical pages:
- a browser note specifically about host-page callback-to-request consumer tracing across widget families
- a compare note on suppression/no-challenge completion vs interactive challenge completion across Arkose and Turnstile-like flows
- a concrete page on iframe/message-boundary tracing for protected browser widgets

## 6. Next-step research directions
1. Continue filling missing high-value browser families with workflow notes that emphasize actual observation boundaries.
2. Add more practical pages where the central task is to locate a token/parameter path into host-page submission logic.
3. Consider a concrete workflow page for widget-family compare patterns:
   - callback edge
   - hidden input edge
   - iframe message edge
   - backend verify edge
4. Keep resisting the temptation to add new abstract pages unless multiple concrete notes genuinely need consolidation.

## 7. Concrete scenario notes or actionable tactics added this run
Added actionable tactics through the Arkose workflow note, including:
- first classify:
  - direct client API vs hosted iframe/lightbox integration
  - suppressed/no-challenge path vs visible challenge path
- anchor `myArkose.setConfig(...)` before doing broad code cleanup
- hook/log:
  - `myArkose.setConfig`
  - `myArkose.run`
  - `myArkose.reset`
  - `onCompleted`
  - `onSuppress`
  - `onFailed`
  - `onError`
- in iframe/lightbox cases, hook/log:
  - outbound `postMessage` challenge-open trigger
  - inbound `challenge-complete`, `challenge-failed`, `challenge-hide`, and related events
- separate four layers explicitly:
  - client setup
  - token/session handoff
  - host-page consumer logic
  - backend verification request
- treat reset/new-session behavior and suppression paths as compare-run axes rather than noise

## 8. Sync / preservation status
Local KB changes were preserved in the workspace this run.
They should be committed and subtree-synced so the public `reverse-expert-kb` archive keeps pace with the concrete-practice pivot.