# Run Report — 2026-03-14 21:16 Asia/Shanghai

## 1. Scope this run
This run continued the KB’s concrete-practice correction by resisting another abstract browser consolidation page and instead filling a recurring practical gap:

**how to localize the actual parameter path from widget/protection output into host-page consumer logic and finally into the protected request.**

The run focused on a methodology page rather than a single protection family, because the same operational bottleneck appears across multiple concrete families already in the KB:
- Cloudflare Turnstile
- Arkose / FunCaptcha
- other browser protection flows that expose values through callback, hidden input, getter, cookie, or iframe `postMessage`

The practical theme of the run was:
- **browser parameter-path localization**
- tracing token/session values from first visible handoff edge to first consumer, request wrapper, and backend-bound request role

## 2. New findings
- A recurring analyst failure mode is stopping at “token visible” instead of recovering the full **parameter path**.
- Browser protection targets often expose multiple candidate surfaces for the same value family:
  - callback argument
  - hidden input
  - widget getter
  - cookie/storage state
  - iframe `postMessage`
- Those surfaces are not always equivalent. The important practical distinction is:
  - which surface is merely visible,
  - which surface is actually read by host-page logic,
  - and which request ultimately consumes the value.
- For iframe/lightbox families, `window.addEventListener('message', ...)` is a first-class analysis boundary, but message streams need classification because many events are lifecycle/visibility-only rather than token-bearing.
- The highest-value artifact is usually not “the token string” but a compact **consumer path** such as:

```text
callback / hidden input / iframe message
  -> host-page reader
  -> request serializer / wrapper
  -> protected request
```

- This localization step fits naturally between existing KB pages on:
  - widget lifecycle tracing
  - request-shaping / token generation
  - CDP-guided live invocation

## 3. Sources consulted
### Existing KB material
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- `topics/browser-runtime-subtree-guide.md`
- `topics/browser-side-risk-control-and-captcha-workflows.md`
- `topics/cloudflare-turnstile-widget-lifecycle-workflow-note.md`
- `topics/arkose-funcaptcha-session-and-iframe-workflow-note.md`
- prior run reports for Turnstile, Arkose, CDP-guided token analysis, and family-differentiated browser workflows

### External/documented sources used this run
- Cloudflare Turnstile docs:
  - `https://developers.cloudflare.com/turnstile/get-started/client-side-rendering/`
- MDN docs:
  - `https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage`
- Prior official Arkose docs already captured in source notes:
  - callbacks
  - iframe setup guide
  - verify API v4

### Search-layer exploratory results used for orientation
- `acw_sc__v2` family references
- `__zse_ck` mixed JS/Wasm references
- callback / hidden-input / iframe message parameter-path orientation results

### Source artifact created
- `sources/browser-runtime/2026-03-14-browser-parameter-path-localization-notes.md`

## 4. Reflections / synthesis
This run improved the KB in a very practical way.

The browser subtree already had:
- family notes for Reese84 / ___utmvc, DataDome / GeeTest / Kasada, Turnstile, and Arkose
- methodology pages for CDP-guided token analysis
- broader pages on browser-side risk-control and token generation

But there was still a missing bridge between “I can see the protection artifact” and “I know exactly how the app uses it.”

That bridge is the parameter path.

This matters because many browser investigations stall at the wrong layer:
- the analyst can already see the token,
- yet still cannot explain why the request fails,
- because the real problem is at the consumer/packaging/request-role boundary.

The new page therefore encodes a strong practical bias:
- callback visibility is not enough
- hidden-input population is not enough
- iframe message visibility is not enough
- the analyst should explicitly localize:
  - first visible handoff edge
  - first consumer edge
  - request role
  - transformation boundary
  - lifecycle drift across reset/retry/expiry

That is a concrete, reusable workflow and a better fit for the human’s correction than another abstract browser synthesis page.

## 5. Candidate topic pages to create or improve
### Created this run
- `topics/browser-parameter-path-localization-workflow-note.md`

### Source note created this run
- `sources/browser-runtime/2026-03-14-browser-parameter-path-localization-notes.md`

### Improved this run
- `index.md`
- `topics/browser-runtime-subtree-guide.md`

### Candidate future creation/improvement
- `topics/browser-request-role-mapping-and-value-attachment.md`
- `topics/browser-callback-to-submit-consumer-patterns.md`
- `topics/acw_sc_v2-cookie-bootstrap-and-consumer-path-note.md`
- `topics/zse-ck-js-wasm-signature-consumer-path-note.md`
- improve Turnstile and Arkose pages with explicit back-links to the new parameter-path workflow note

## 6. Next-step research directions
1. Continue adding pages that help analysts move from **visible artifact** to **real request role**.
2. Deepen browser-site-family notes where the practical challenge is not generation but packaging/consumer localization.
3. Add a concrete note on request-finalization tracing from the opposite direction:
   - start at the protected request
   - trace backward to callback / message / state origin
4. Consider targeted family notes for:
   - `acw_sc__v2`
   - `__zse_ck`
   once enough grounded source material supports a practical, code-adjacent workflow note rather than just another abstract summary.

## 7. Concrete scenario notes or actionable tactics added this run
- Added a concrete workflow for classifying first visible handoff surfaces:
  - callback argument
  - hidden input
  - getter/API read
  - cookie/storage write
  - iframe `postMessage`
- Added explicit guidance to trace **read sites**, not just write sites.
- Added breakpoint/hook suggestions for:
  - hidden input write and read
  - callback registration and callback body
  - `window.addEventListener('message', ...)`
  - request-finalization wrappers
  - reset/retry/expired handlers
- Added a practical distinction between:
  - visible surface
  - authoritative surface
  - request-carrying surface
- Added failure diagnosis for:
  - stopping at token visibility
  - treating the wrong surface as authoritative
  - path drift after reset/retry/expiration
  - noisy iframe lifecycle messages
  - finding the request but missing sibling fields or transformation boundaries

## 8. Sync / preservation status
- Local KB changes were integrated into canonical topic/source/index files.
- This run continued the KB’s pivot toward practical browser workflow coverage and away from abstract taxonomy expansion.
- Next required operational steps after file updates:
  - commit workspace changes
  - run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
  - if sync fails, preserve local progress and record the failure