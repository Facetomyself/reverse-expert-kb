# Run Report — 2026-03-14 19:16 Asia/Shanghai

## 1. Scope this run
Continue the KB’s concrete/case-driven pivot by adding a browser target-family workflow note that is practical without collapsing back into abstract taxonomy.

This run focused on Cloudflare Turnstile as a lifecycle-oriented browser protection case.
The aim was not to produce another generic anti-bot page, but to capture a concrete analyst workflow around:
- widget rendering mode
- challenge execution timing
- token handoff to page/application logic
- redemption/validation timing
- retry/reset/timeout/expiry transitions

## 2. New findings

### A. Turnstile is best approached as a widget-lifecycle and redemption-contract problem
The official docs make the lifecycle explicit:
- render widget
- run challenge
- generate token
- hand token to application code or hidden field
- redeem/validate via backend Siteverify

This is practically important because many analyst mistakes happen at the boundaries between these stages rather than inside any exotic token algorithm.

### B. Render mode and execution mode are high-value first distinctions
A useful first split is:
- implicit rendering vs explicit rendering
- automatic execution at render time vs manual `turnstile.execute()` later

This directly changes where an analyst should anchor:
- implicit/auto flows often expose token state earlier
- explicit/manual flows often hide the meaningful transition near submit or another user-action gate

### C. Token handoff edges are usually more valuable than widget UI internals
The best practical observation points are often:
- success callback
- hidden input `cf-turnstile-response`
- `turnstile.getResponse(widgetId)` read sites
- the request that actually redeems the token

This is exactly the kind of “parameter path” thinking the human asked the KB to emphasize.

### D. Failure diagnosis becomes clearer once token generation is separated from redemption
The official docs confirm three practical constraints that matter immediately:
- token redemption is single-use
- token lifetime is five minutes
- retry / timeout / expired / error are distinct lifecycle events

This provides a grounded explanation for common misleading observations:
- got a token once, replay failed later
- callback worked but backend rejected
- repeated errors are really retry-loop artifacts

## 3. Sources consulted
- `sources/browser-runtime/2026-03-14-turnstile-lifecycle-and-validation-notes.md`
- Official Cloudflare Turnstile docs:
  - `https://developers.cloudflare.com/turnstile/get-started/client-side-rendering/`
  - `https://developers.cloudflare.com/turnstile/get-started/client-side-rendering/widget-configurations/`
  - `https://developers.cloudflare.com/turnstile/turnstile-analytics/token-validation/`
  - `https://developers.cloudflare.com/turnstile/troubleshooting/client-side-errors/`
- Search-layer exploratory query cluster over Turnstile lifecycle / callback / validation behavior

## 4. Reflections / synthesis
This run was useful because it added another practical browser note without drifting back into empty ontology-building.

Turnstile complements the existing browser workflow notes well:
- Reese84 / ___utmvc note -> request-shaping and state-dependent token family workflow
- DataDome / GeeTest / Kasada note -> family-differentiated first-pass workflow
- CDP-guided token analysis -> paused-frame callable-contract workflow
- Turnstile note -> widget lifecycle, token handoff, and redemption/expiry workflow

That mix is healthier than adding more top-level abstractions.

A useful broader lesson from this run:
for some browser protection families, the analyst’s real target is not a hidden algorithm but a transition boundary:
- where a widget starts executing
- where a token becomes visible to page logic
- where it is redeemed
- where it expires or is reset

That is practical RE knowledge, not just taxonomy.

## 5. Candidate topic pages to create or improve
Created this run:
- `topics/cloudflare-turnstile-widget-lifecycle-workflow-note.md`

Created source note this run:
- `sources/browser-runtime/2026-03-14-turnstile-lifecycle-and-validation-notes.md`

Improved this run:
- `index.md`
- `topics/browser-runtime-subtree-guide.md`
- `topics/browser-side-risk-control-and-captcha-workflows.md`
- `topics/browser-fingerprint-and-state-dependent-token-generation.md`

Candidate future practical pages:
- a Cloudflare Turnstile + host-page submit-wrapper note if more app-side patterns accumulate
- a Cloudflare / challenge-transition compare note spanning Turnstile vs other widget lifecycle families
- a browser workflow note specifically about hidden-field / callback / request-wrapper parameter-path localization

## 6. Next-step research directions
1. Continue adding target-grounded browser notes where the key problem is a concrete lifecycle or parameter path, not general theory.
2. Look for another family where reset/retry/challenge-transition state is the real source of analyst confusion.
3. Add more code-adjacent notes that show where to hook, what to log, and what failure modes imply.
4. Avoid broad new topic pages unless they clearly consolidate multiple concrete workflow notes.

## 7. Concrete scenario notes or actionable tactics added this run
Added actionable tactics through the Turnstile workflow note, including:
- first classify:
  - implicit vs explicit rendering
  - auto execution vs manual execute-on-submit
- anchor the token handoff edge before doing heavy code cleanup:
  - success callback
  - hidden `cf-turnstile-response` field
  - `getResponse()` read sites
- anchor the real redemption request separately from token visibility
- place hooks at:
  - `turnstile.render`
  - `turnstile.execute`
  - `turnstile.reset`
  - success/error/timeout/expired callbacks
- diagnose failures using lifecycle semantics:
  - one-time redemption
  - five-minute expiry window
  - retry-loop callback repetition
  - reset/re-render after failure
