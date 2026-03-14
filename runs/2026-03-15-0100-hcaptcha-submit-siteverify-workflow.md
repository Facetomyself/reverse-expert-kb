# Run Report — 2026-03-15 01:00 Asia/Shanghai

## 1. Scope this run
This run started by reviewing the current browser-runtime subtree, recent practical browser workflow additions, and the latest run/source material to keep the KB aligned with the human correction away from abstract taxonomy and toward concrete target-solving knowledge.

A practical browser gap was selected rather than creating another high-level synthesis page:
- the browser subtree already had concrete notes for Turnstile and Arkose
- it already had cross-target workflow notes for parameter-path localization and request-finalization backtrace
- but it did **not** yet have a dedicated concrete note for **hCaptcha flows where the important boundary is execute/callback/hidden-field handoff into host-page submit logic and then backend siteverify**

The main outputs of this run were therefore:
- `topics/hcaptcha-callback-submit-and-siteverify-workflow-note.md`
- `sources/browser-runtime/2026-03-15-hcaptcha-callback-submit-and-siteverify-notes.md`
- navigation updates in `index.md`, `topics/browser-runtime-subtree-guide.md`, and `topics/browser-side-risk-control-and-captcha-workflows.md`

## 2. New findings
- hCaptcha is a good concrete family not because of undocumented internals this run, but because the official docs already expose a strong practical workflow shape that analysts repeatedly need:
  - widget render
  - optional invisible/manual `execute()`
  - callback or hidden-field token handoff
  - host-page submit or AJAX consumer path
  - backend `siteverify` verification boundary
- The family differs in a useful practical way from already-covered browser notes:
  - Turnstile emphasizes widget lifecycle, reset/expiry, and one-shot redemption
  - Arkose emphasizes callback/session/iframe message boundaries
  - hCaptcha strongly emphasizes **submit-path tracing**, especially when local form validation gates whether `execute()` ever runs
- A recurring practical failure pattern is that analysts stop at one of these milestones:
  - widget visible
  - hidden field present
  - callback token logged
  None of those proves that the token reached the request path that matters.
- Another useful concrete distinction surfaced this run:
  - some failures that look like “captcha problems” are really **local validation problems** because page logic prevents `hcaptcha.execute()` from firing at all.
- Community results found through search were noisier and weaker than the official docs for trustworthy synthesis this run, so the page was intentionally grounded mostly in official lifecycle/integration behavior plus light practitioner signal about callback vs hidden-field confusion.

## 3. Sources consulted
### Existing KB material
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- `topics/browser-runtime-subtree-guide.md`
- `topics/browser-side-risk-control-and-captcha-workflows.md`
- `topics/cloudflare-turnstile-widget-lifecycle-workflow-note.md`
- `topics/arkose-funcaptcha-session-and-iframe-workflow-note.md`
- `topics/browser-parameter-path-localization-workflow-note.md`
- `topics/browser-request-finalization-backtrace-workflow-note.md`
- `sources/browser-runtime/2026-03-14-turnstile-lifecycle-and-validation-notes.md`

### External / search material
- hCaptcha Developer Guide — `https://docs.hcaptcha.com/`
- hCaptcha Invisible mode docs — `https://docs.hcaptcha.com/invisible/`
- Search-layer exploratory queries around:
  - Akamai sensor workflows
  - hCaptcha token/callback/hidden-input workflows
- Light practitioner/community signal from search results indicating recurring callback-vs-hidden-field-vs-request confusion

### Failed or weak source attempts
- A raw GitHub fetch attempted during broader exploration returned 404.
- This did not block the run because the official hCaptcha docs were already strong enough to justify a practical workflow page.

## 4. Reflections / synthesis
This run stayed aligned with the human correction.

The weak old-mode move would have been:
- add another generic browser anti-bot taxonomy page
- or add another broad “captcha comparison” page with little operational value

The stronger move was:
- identify a missing concrete family/workflow entry surface in an already-practical subtree
- add a page that explains how analysts actually localize execution and submission boundaries
- keep the page code-adjacent and breakpoint-oriented

The resulting hCaptcha page is practical because it is organized around:
- target pattern / scenario
- analyst goal
- concrete workflow
- breakpoint/hook placement
- likely failure modes
- environment assumptions
- representative code/pseudocode fragments
- what to verify next

That structure fits the KB’s corrected direction much better than abstract-first synthesis.

It also strengthens the browser subtree as a coordinated set of concrete entry surfaces:
- Turnstile for widget lifecycle / redemption timing
- Arkose for iframe/session-token/message boundaries
- hCaptcha for callback-driven submit and execute timing
- parameter-path localization for handoff tracing
- request-finalization backtrace for consumer-path-first analysis

## 5. Candidate topic pages to create or improve
### Created this run
- `topics/hcaptcha-callback-submit-and-siteverify-workflow-note.md`

### Improved this run
- `index.md`
- `topics/browser-runtime-subtree-guide.md`
- `topics/browser-side-risk-control-and-captcha-workflows.md`

### Candidate future creation/improvement
- improve `topics/browser-cdp-and-debugger-assisted-re.md` with a compact section on callback-to-submit tracing in browser widget families
- possible future concrete page on Akamai browser sensor submission and cookie-validation workflow if source quality becomes strong enough for practical breakpoint guidance without devolving into vague theory
- possible future improvement to browser subtree navigation so concrete family notes are grouped by their main analyst boundary:
  - widget lifecycle
  - callback/message handoff
  - request-boundary backtrace
  - cookie bootstrap / consumer path

## 6. Next-step research directions
1. Continue favoring missing concrete browser family/workflow entry pages over new abstract browser taxonomy pages.
2. Look for additional families where the practical leverage point is clear and source quality is sufficient, especially around:
   - request-signature families
   - cookie bootstrap families
   - widget/session verify families
   - challenge/retry state diagnosis
3. If a stronger Akamai browser source cluster emerges, create a workflow page centered on:
   - sensor submission boundary
   - `_abck` / `bm_sz` lifecycle observations
   - accepted-vs-failed compare-run discipline
4. Keep updating subtree navigation when a new page changes how an analyst should enter the browser branch.

## 7. Concrete scenario notes or actionable tactics added this run
- Added a concrete hCaptcha workflow centered on:
  - implicit vs explicit/invisible render mode
  - `hcaptcha.execute(widgetId)` as a decisive observation edge
  - callback vs hidden-field handoff classification
  - host-page submit / AJAX consumer localization
  - backend `siteverify` boundary reasoning
- Added breakpoint families for:
  - `hcaptcha.render(...)`
  - `hcaptcha.execute(...)`
  - callback / `data-callback` bodies
  - hidden-field read sites
  - host-page submit or request wrappers
- Added explicit failure diagnosis for:
  - local validation blocking execute
  - token visible but not truly redeemed
  - hidden field present but not authoritative
  - delayed submit / stale token confusion
  - over-focus on widget internals instead of submit-path tracing

## 8. Sync / preservation status
- Local KB progress was preserved in:
  - `topics/hcaptcha-callback-submit-and-siteverify-workflow-note.md`
  - `sources/browser-runtime/2026-03-15-hcaptcha-callback-submit-and-siteverify-notes.md`
  - this run report
- A related GitHub raw fetch attempt returned 404 during exploration; the failure was non-blocking and did not materially affect the run outcome.
- Next operational steps after this report:
  - commit workspace changes
  - run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
  - if sync fails, keep local state and record the failure
