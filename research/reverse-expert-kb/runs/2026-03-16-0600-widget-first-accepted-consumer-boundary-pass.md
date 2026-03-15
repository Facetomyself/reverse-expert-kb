# Run Report — 2026-03-16 06:00 — Widget first-accepted-consumer boundary pass

## 1. Scope this run
This run focused on a narrow, practical browser-runtime gap rather than creating another abstract synthesis page.

I reviewed the current browser widget-family notes and recent run history, then concentrated on one recurring analyst failure mode:
- the KB already stressed token/cookie visibility and callback/handoff boundaries,
- but several concrete widget-family pages still risked letting the reader stop too early at “token visible” or “submit observed”.

The practical correction for this run was to normalize one stronger concrete boundary across existing pages:
- **the first accepted consumer request**

This boundary means:
- not just the callback,
- not just the hidden field,
- not just the request carrying the token,
- but the first later request / redirect / route / state refresh whose behavior actually changes because the earlier solve/verification step was accepted.

Pages updated this run:
- `topics/cloudflare-turnstile-widget-lifecycle-workflow-note.md`
- `topics/hcaptcha-callback-submit-and-siteverify-workflow-note.md`
- `topics/recaptcha-v3-and-invisible-workflow-note.md`
- `topics/browser-runtime-subtree-guide.md`
- `index.md`

## 2. New findings
### A. Official docs across Turnstile, hCaptcha, and reCAPTCHA support the same practical chain
The official integration/verification docs repeatedly reinforce a common workflow shape:

```text
widget/render/execute
  -> callback / hidden-field / direct-token exposure
  -> token-carrying request
  -> server verification
  -> later accepted or still-blocked consumer behavior
```

This matters because a real analyst often sees the early stages clearly but still does not know where the target meaningfully transitions from blocked/degraded to accepted.

### B. “Request carrying the token” is often not the same as “request proving success mattered”
The strongest practical insight this run sharpened is:
- a token-carrying request may only update validation state,
- while the **next** request, redirect, SPA route, session fetch, or protected API call is what proves the challenge transition actually had effect.

This is especially useful in:
- form submissions that redirect into a protected page,
- SPA login/account bootstrap flows,
- v3 score-based flows where syntax looks fine but later policy still differs,
- hybrid challenge/update flows where validation is a gate and not the final consumer.

### C. Compare-run diagnosis is cleaner when anchored at the first accepted consumer request
A practical compare-run tactic emerged clearly:
- if accepted and failed runs look identical through callback visibility and token submission,
- the best divergence point may be the first downstream consumer request rather than the solve request itself.

That is a better operator-facing diagnostic rule than more generic “trace the lifecycle” advice.

## 3. Sources consulted
Primary KB sources read:
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- recent run report:
  - `research/reverse-expert-kb/runs/2026-03-16-0500-browser-four-boundary-routing-and-perimeterx-callback-consumer.md`
- concrete and parent topic pages:
  - `topics/browser-side-risk-control-and-captcha-workflows.md`
  - `topics/cloudflare-turnstile-widget-lifecycle-workflow-note.md`
  - `topics/hcaptcha-callback-submit-and-siteverify-workflow-note.md`
  - `topics/recaptcha-v3-and-invisible-workflow-note.md`
  - `topics/browser-runtime-subtree-guide.md`

Existing source notes read:
- `sources/browser-runtime/2026-03-14-turnstile-lifecycle-and-validation-notes.md`
- `sources/browser-runtime/2026-03-15-hcaptcha-callback-submit-and-siteverify-notes.md`
- `sources/browser-runtime/2026-03-15-recaptcha-v3-and-invisible-workflow-notes.md`

Fresh external source checks this run:
- Cloudflare Turnstile docs:
  - `https://developers.cloudflare.com/turnstile/get-started/client-side-rendering/`
- hCaptcha docs:
  - `https://docs.hcaptcha.com/`
- Google reCAPTCHA verify docs:
  - `https://developers.google.com/recaptcha/docs/verify`
- search-layer query cluster for practical callback/hidden-field/request-consumer patterns:
  - `Cloudflare Turnstile token callback hidden field first request siteverify`
  - `hCaptcha callback hidden field execute submit siteverify`
  - `reCAPTCHA v3 execute action token first consumer request siteverify`

## 4. Reflections / synthesis
This run stayed aligned with the human correction: move the KB away from empty taxonomy growth and toward concrete operator value.

The useful move here was **not** to create a fresh top-level abstract page like “token redemption boundary theory”.
That would have repeated the old failure mode.

Instead, the right move was to:
- identify a recurring practical bottleneck,
- verify it against existing concrete pages plus official docs,
- normalize it directly inside the concrete notes analysts are likely to use first.

This also fits the recently established browser-side “four-boundary” direction, but makes it more concrete for widget-heavy families.
In practice, the chain now reads more usefully as:

```text
visible widget / execute boundary
  -> visible token handoff boundary
  -> token-carrying request boundary
  -> first accepted consumer request boundary
```

That last boundary is what helps an analyst answer:
- “What actually changed after solve?”
- “Which request proves acceptance mattered?”
- “Where do accepted and failed runs first diverge in a way that explains real behavior?”

## 5. Candidate topic pages to create or improve
High-confidence improvements after this run:
- improve `topics/arkose-funcaptcha-session-and-iframe-workflow-note.md`
  - add the same first-accepted-consumer emphasis for iframe/session token flows
- improve `topics/browser-side-risk-control-and-captcha-workflows.md`
  - strengthen the operator chain from visible solve artifact to first accepted downstream consumer
- improve `topics/browser-request-finalization-backtrace-workflow-note.md`
  - add a short section on when the first request carrying a value is still not the first request whose acceptance matters

Possible new concrete page if enough target evidence accumulates:
- `topics/first-accepted-consumer-request-compare-run-workflow-note.md`

But this should only be created if multiple target families produce enough grounded case material; otherwise the concept should stay embedded in existing concrete pages.

## 6. Next-step research directions
1. Extend the same practical boundary correction to Arkose / GeeTest / DataDome-family pages where appropriate.
2. Strengthen the browser parent workflow page so it explicitly routes analysts from:
   - visible solve artifact
   - to carrier request
   - to first accepted consumer request.
3. Look for target-grounded case material where:
   - token submission succeeds syntactically,
   - but only a later request or route reveals the true trust/policy outcome.
4. Continue biasing browser subtree work toward:
   - compare-run diagnostics,
   - request ownership,
   - policy consequence localization,
   - concrete request/route transitions,
   rather than additional abstract family taxonomies.

## 7. Concrete scenario notes or actionable tactics added this run
### Added across widget-family notes
- A new explicit operator question:
  - **What is the first accepted consumer request after solve/submit?**
- New compare-run sketches showing:
  - token visibility can match,
  - token-carrying submit can match,
  - but the first downstream consumer request can still diverge.
- New practical warning:
  - do not equate “request carries token” with “request proves acceptance mattered”.

### Turnstile-specific practical tactic added
- Compare runs at:
  - callback(token)
  - token-carrying submit
  - first later protected request
- This is useful when the submit step only refreshes trust state and the real proof is a later accepted API call or route transition.

### hCaptcha-specific practical tactic added
- Treat callback-driven form submission and redirect/API follow-on as separate boundaries.
- If callback and form POST look correct, localize the first downstream request or route that actually changes from challenged/degraded to accepted.

### reCAPTCHA-specific practical tactic added
- For v3 especially, separate:
  - `execute(...).then(token)` success,
  - token-carrying request visibility,
  - later policy consequence on session fetch / route / protected API.
- This is the cleanest place to diagnose action/score policy effects that are invisible if the analyst stops at token submission.

## Sync / preservation status
- KB files were modified locally.
- A git commit and archival sync should be performed after this report.
- If sync fails, local preservation still remains the primary success condition for the run.
