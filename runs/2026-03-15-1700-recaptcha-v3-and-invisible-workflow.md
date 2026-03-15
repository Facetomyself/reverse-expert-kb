# Run Report — 2026-03-15 17:00 Asia/Shanghai

## 1. Scope this run
This run continued the KB’s browser-side practical expansion and deliberately chose a high-value concrete target-family gap instead of creating another abstract synthesis page.

The starting review covered:
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- current browser/mobile subtree structure
- the most recent hybrid/mobile workflow note from the prior run
- adjacent browser workflow notes including Turnstile, hCaptcha, and `acw_sc__v2`
- recent run reports and source-note inventory

The concrete gap was clear:
- the browser subtree already had practical notes for Turnstile, hCaptcha, Arkose, GeeTest, DataDome, Kasada, PerimeterX, Akamai, `acw_sc__v2`, and several request-signature families
- but it still lacked a practical workflow note for one of the most common browser validation families: **reCAPTCHA**

This run therefore focused on creating a concrete workflow note for:
- reCAPTCHA v3 action/score flows
- Invisible reCAPTCHA callback/submit flows
- `grecaptcha.execute(...)` timing
- callback / hidden-field / `getResponse()` handoff
- first real consumer request
- backend `siteverify` acceptance boundaries

## 2. New findings
- The missing practical gap in the browser branch was not “another captcha taxonomy page,” but a concrete reCAPTCHA workflow page.
- A durable operational split was added explicitly:
  - **reCAPTCHA v3 action/score flow**
  - **Invisible reCAPTCHA callback/widget flow**
- The most reusable practical distinction added this run is:
  - **token visibility is not the same as token redemption**
- For v3, `action` was elevated as a first-class analyst object rather than a cosmetic label, because backend verification is expected to validate the action name and frequently policy-check the score as well.
- For invisible flows, client-side validation was made explicit as a common hidden cause of “reCAPTCHA never ran” confusion, because `execute()` often sits behind page validation or submit orchestration.
- The page now treats short lifetime and duplicate use as central failure axes:
  - tokens are short-lived
  - tokens are single-use
  - replay-style conclusions are therefore particularly easy to misread

## 3. Sources consulted
### Existing KB material
- `research/reverse-expert-kb/index.md`
- `topics/browser-runtime-subtree-guide.md`
- `topics/browser-side-risk-control-and-captcha-workflows.md`
- `topics/cloudflare-turnstile-widget-lifecycle-workflow-note.md`
- `topics/hcaptcha-callback-submit-and-siteverify-workflow-note.md`
- `topics/acw-sc-v2-cookie-bootstrap-and-consumer-path-note.md`

### External / search material
Official documentation fetched directly:
- Google Developers — reCAPTCHA v3
  - `https://developers.google.com/recaptcha/docs/v3`
- Google Developers — Invisible reCAPTCHA
  - `https://developers.google.com/recaptcha/docs/invisible`
- Google Developers — Verifying the user's response
  - `https://developers.google.com/recaptcha/docs/verify`

Search-layer query cluster:
- `reCAPTCHA v3 execute callback action token workflow siteverify`
- `grecaptcha execute callback submit token first consumer request`
- `reCAPTCHA invisible callback siteverify workflow action parameter`

Useful returned result classes:
- official Google reCAPTCHA docs
- directionally useful developer/tutorial material reinforcing execute-on-submit and backend action verification

### Source-quality judgment
- Official Google docs were strong enough to anchor the page’s key workflow claims:
  - v3 `execute(..., {action})`
  - hidden-field / callback / `getResponse()` token surfaces
  - backend `siteverify`
  - short token lifetime and duplicate-use rejection
- Search-layer supplementary results were noisier, but still useful for choosing practical workflow emphasis.
- One search backend degraded during the run:
  - Grok returned empty/non-JSON output while Tavily still returned usable results
  - the failure was logged under `.learnings/ERRORS.md`

## 4. Reflections / synthesis
This run stayed aligned with the human correction by explicitly choosing the stronger move.

The weaker move would have been:
- another broad anti-bot/captcha synthesis page
- a generic “Google protections” taxonomy page
- or more abstract splitting of captcha families by formal labels

The stronger move was:
- identify a conspicuous missing concrete family in an already practical browser subtree
- build a workflow note around how analysts actually get stuck
- separate v3 action/score policy from invisible callback/widget submission
- make execute timing, token handoff, consumer request, and backend acceptance the main objects

The best synthesis from this run is:

**For reCAPTCHA, the decisive explanation usually lives at the boundary between token generation and token redemption, not at the mere presence of the widget or token string.**

That changes breakpoint choice.
Instead of stopping at widget render or token presence, the KB now recommends:
- classify v3 vs invisible first
- capture the real execute edge
- capture the first token handoff surface
- localize the first real request consumer
- classify backend-side rejection as expiry, duplicate use, action mismatch, score policy, hostname mismatch, or bad packaging

That is much closer to real browser workflow diagnosis than generic captcha description.

## 5. Candidate topic pages to create or improve
### Created this run
- `topics/recaptcha-v3-and-invisible-workflow-note.md`

### Improved this run
- `topics/browser-runtime-subtree-guide.md`
- `topics/browser-side-risk-control-and-captcha-workflows.md`
- `index.md`

### New source note added
- `sources/browser-runtime/2026-03-15-recaptcha-v3-and-invisible-workflow-notes.md`

### Candidate future creation/improvement
- a future concrete note on **reCAPTCHA enterprise / site-specific policy layering** once enough grounded examples accumulate
- a future note on **callback-visible token but hidden real consumer path** across multiple captcha families, if cross-family evidence gets denser
- improve `topics/browser-side-risk-control-and-captcha-workflows.md` with a compact subsection mapping:
  - render/execute edge
  - token handoff edge
  - first consumer request
  - backend validation edge
  across Turnstile / hCaptcha / reCAPTCHA families

## 6. Next-step research directions
1. Continue filling obvious practical target-family gaps in the browser branch rather than broadening taxonomy.
2. High-value adjacent browser topics now include:
   - reCAPTCHA enterprise / policy-layer notes when evidence quality supports it
   - cross-family token-handoff vs redemption comparison notes
   - first-consumer localization for widget-light or callback-light pages
   - compare-run diagnosis where identical-looking client traces still diverge at backend policy
3. Keep preferring pages that include:
   - target pattern / scenario
   - analyst goal
   - concrete workflow
   - execute / handoff / consumer / redemption boundaries
   - likely failure modes
   - representative code/pseudocode/hook fragments
4. Maintain the browser subtree as a practical playbook for common protected browser families, not as a generic anti-bot glossary.

## 7. Concrete scenario notes or actionable tactics added this run
- Added a dedicated workflow page for **reCAPTCHA v3 and invisible** browser analysis.
- Added explicit operational separation of:
  - v3 action/score flow
  - invisible callback/widget flow
- Added concrete guidance to separate:
  - script/widget presence
  - execute timing
  - first token handoff
  - first consumer request
  - backend `siteverify` and policy outcome
- Added practical advice to treat these as first-class failure axes:
  - token expiry
  - duplicate/single-use rejection
  - action mismatch
  - score threshold mismatch
  - host-page validation preventing execute
- Added breakpoint placement centered on:
  - `grecaptcha.ready(...)`
  - `grecaptcha.execute(...)`
  - callback / promise continuation
  - hidden-field or `getResponse()` read site
  - host-page request-finalization boundary

## 8. Sync / preservation status
- Local KB progress was preserved in:
  - `topics/recaptcha-v3-and-invisible-workflow-note.md`
  - `sources/browser-runtime/2026-03-15-recaptcha-v3-and-invisible-workflow-notes.md`
  - navigation updates in `topics/browser-runtime-subtree-guide.md`, `topics/browser-side-risk-control-and-captcha-workflows.md`, and `index.md`
  - this run report
- Search-layer degradation encountered this run and recorded separately:
  - Grok backend returned empty/non-JSON output while Tavily still returned usable results
- Next operational steps after writing this report:
  - commit the KB changes in `/root/.openclaw/workspace`
  - run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
  - if sync fails, preserve local state and keep the failure recorded in this run report