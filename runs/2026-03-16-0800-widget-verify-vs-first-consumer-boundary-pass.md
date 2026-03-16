# Run Report — 2026-03-16 08:00 — Widget verify-vs-first-consumer boundary pass

## 1. Scope this run
This run stayed deliberately concrete.

Instead of creating another abstract browser methodology page, it focused on tightening an existing practical workflow note that sits in the middle of several concrete widget-family pages:
- `topics/browser-request-finalization-backtrace-workflow-note.md`

The practical problem targeted this run was:
- cases where callback/hidden-field/message token visibility is already known,
- and the token-carrying submit/verify request is also visible,
- but analysts still need a stronger workflow for following through to the **first downstream accepted consumer request**.

Files reviewed at the start included:
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- `topics/browser-request-finalization-backtrace-workflow-note.md`
- `topics/browser-side-risk-control-and-captcha-workflows.md`
- `topics/cloudflare-turnstile-widget-lifecycle-workflow-note.md`
- `topics/hcaptcha-callback-submit-and-siteverify-workflow-note.md`
- `topics/arkose-funcaptcha-session-and-iframe-workflow-note.md`
- recent browser run reports, especially:
  - `runs/2026-03-16-0500-browser-four-boundary-routing-and-perimeterx-callback-consumer.md`
  - `runs/2026-03-16-0700-arkose-first-consumer-and-iframe-boundary-pass.md`

## 2. New findings
### A. The request-finalization backtrace page needed an explicit widget-family bridge section
The existing page was already strong for request-boundary-first work, but it still under-emphasized a recurring practical case:
- the token/callback/message edge is already known,
- the token-carrying request is also known,
- but the strongest compare-run boundary is still one request later.

This run added that bridge explicitly.

### B. Official widget-family docs are strong on token visibility and verify boundaries, but weaker on downstream consumer behavior
Fresh source refreshes confirmed a stable pattern across:
- Cloudflare Turnstile docs
- hCaptcha docs
- Arkose docs

All three document, in different forms:
- token visibility via callback / hidden field / message event
- a distinct verify or submit boundary

But they are much weaker on:
- which later request first proves acceptance changed actual app behavior
- how to reason when callback success and token submission both look correct but the app still loops, degrades, or stays blocked

That gap is exactly where the KB can add practical value.

### C. The right practical normalization is now:

```text
callback / hidden-field / message token visibility
  -> token-carrying submit or verify request
  -> first downstream accepted consumer request
```

This is now better anchored in the KB as a concrete operator rule rather than an implicit theme scattered across widget-family notes.

### D. Turnstile, hCaptcha, and Arkose now read more symmetrically through the bridge note
The concrete widget pages already had first-consumer language, but this run made the shared bridge note (`browser-request-finalization-backtrace-workflow-note`) explain when and why analysts should continue past a visible submit/verify edge.

That makes the browser subtree more coherent for real-case routing.

## 3. Sources consulted
### Existing KB material
- `research/reverse-expert-kb/index.md`
- `topics/browser-request-finalization-backtrace-workflow-note.md`
- `topics/browser-side-risk-control-and-captcha-workflows.md`
- `topics/cloudflare-turnstile-widget-lifecycle-workflow-note.md`
- `topics/hcaptcha-callback-submit-and-siteverify-workflow-note.md`
- `topics/arkose-funcaptcha-session-and-iframe-workflow-note.md`
- `topics/perimeterx-human-cookie-collector-workflow-note.md`
- `topics/cloudflare-clearance-cookie-and-js-challenge-workflow-note.md`
- `sources/browser-runtime/2026-03-15-perimeterx-human-cookie-collector-notes.md`
- recent run reports:
  - `runs/2026-03-16-0500-browser-four-boundary-routing-and-perimeterx-callback-consumer.md`
  - `runs/2026-03-16-0700-arkose-first-consumer-and-iframe-boundary-pass.md`

### Fresh external source checks
- <https://developers.cloudflare.com/turnstile/get-started/client-side-rendering/widget-configurations/>
- <https://developers.cloudflare.com/turnstile/turnstile-analytics/token-validation>
- <https://docs.hcaptcha.com/>
- <https://developer.arkoselabs.com/docs/iframe-setup-guide>

Search-layer query batch:
- `Turnstile callback token verify first protected request docs`
- `Arkose onCompleted verify session token iframe first request docs`
- `hCaptcha callback siteverify first protected request docs`

### Source-quality judgment
- strongest evidence this run came from official lifecycle/integration docs
- these docs are strong on token-visibility and verify semantics
- they are weaker on downstream consumer behavior, which is exactly why the KB synthesis here matters
- this run therefore stayed conservative: no undocumented internals, just stronger workflow framing

## 4. Reflections / synthesis
This run matched the human’s correction well.

The wrong move would have been:
- another broad browser anti-bot topic page
- more taxonomy about widget families without improving operator workflow

The stronger move was:
- improve a bridge/cookbook page that analysts can actually use when a real target gets stuck in the “token looks right but behavior still wrong” phase
- reinforce symmetry across existing concrete widget-family notes
- keep the KB cumulative and more practical per page

A useful practical distinction now made more explicit is:
- **visible token boundary** is not enough
- **token-carrying request boundary** is not always enough
- **first downstream accepted consumer request** is often the strongest proof boundary

That distinction is especially valuable because it explains a large class of failures without forcing deeper premature deobfuscation.

## 5. Candidate topic pages to create or improve
### Improved this run
- `topics/browser-request-finalization-backtrace-workflow-note.md`
- `topics/browser-side-risk-control-and-captcha-workflows.md`
- `index.md`

### Created this run
- `sources/browser-runtime/2026-03-16-widget-verify-vs-first-consumer-boundary-notes.md`
- this run report

### Good next improvements
- improve `topics/cloudflare-clearance-cookie-and-js-challenge-workflow-note.md`
  - make the validation/update-edge vs first-consumer distinction even more explicit for clearance-cookie cases
- improve `topics/perimeterx-human-cookie-collector-workflow-note.md`
  - add a short explicit compare-run subsection for collector-success vs first accepted app request
- improve `topics/browser-runtime-subtree-guide.md`
  - add one short routing sentence pointing readers from concrete widget-family pages to the request-finalization bridge note when submit/verify is visible but consequence is still unclear

## 6. Next-step research directions
1. Continue improving existing concrete browser notes where they still stop one boundary too early.
2. Look for more official or high-signal practitioner material around downstream consumer effects after successful widget verification.
3. Extend the same practical distinction to non-widget browser families where a visible validation request still is not the first decisive consumer.
4. Keep preferring bridge-note and workflow-cookbook improvements over new abstract parent pages.

## 7. Concrete scenario notes or actionable tactics added this run
### Practical scenario normalized this run
**Widget callback/message/hidden-field token visibility and token-carrying submit both look correct, but the application still behaves as if the solve did not matter.**

### Concrete tactics added
- treat the request-finalization bridge page as the place to continue once widget-family notes reach a visible submit/verify edge
- explicitly classify whether the token-carrying request is:
  - the final decision edge
  - or only a validation/update edge
- always ask which later request, redirect, SPA route, or bootstrap fetch first shows that the acceptance actually propagated
- compare accepted and failed runs at that later boundary, not only at token visibility time
- in Turnstile/hCaptcha/Arkose cases, record all three boundaries separately:
  - token visibility
  - token-carrying submit/verify
  - first downstream accepted consumer

## 8. Errors / sync notes
### Error status
No major tooling or source-path error occurred in this run.

### Local preservation status
Local KB progress preserved in:
- `topics/browser-request-finalization-backtrace-workflow-note.md`
- `topics/browser-side-risk-control-and-captcha-workflows.md`
- `sources/browser-runtime/2026-03-16-widget-verify-vs-first-consumer-boundary-notes.md`
- `index.md`
- this run report

### Planned git / sync actions
After this report:
1. commit changes in `/root/.openclaw/workspace`
2. run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
3. if sync fails, record the failure while keeping local preservation as the primary success condition
