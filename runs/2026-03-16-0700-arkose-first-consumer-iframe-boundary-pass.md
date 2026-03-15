# Run Report — 2026-03-16 07:00 — Arkose first-consumer and iframe-boundary pass

## 1. Scope this run
This run focused on a concrete browser target-family note rather than creating new taxonomy.

The practical target was:
- `topics/arkose-funcaptcha-session-and-iframe-workflow-note.md`

Reason for focus:
- recent browser KB work had already normalized the importance of the **first accepted consumer request** for Turnstile, hCaptcha, and reCAPTCHA,
- but the Arkose note still leaned more heavily on lifecycle/callback/iframe semantics than on the downstream request that actually proves acceptance changed application behavior.

This run therefore:
- refreshed Arkose official source grounding,
- tightened the Arkose workflow note around callback/message -> verify/update -> first accepted consumer,
- updated the browser subtree index wording,
- recorded a small maintenance-path error encountered during source-note loading.

Files reviewed at the start:
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- `topics/arkose-funcaptcha-session-and-iframe-workflow-note.md`
- `topics/cloudflare-turnstile-widget-lifecycle-workflow-note.md`
- `sources/browser-runtime/2026-03-14-arkose-funcaptcha-lifecycle-notes.md`
- recent widget-family run reports from 05:00 and 06:00

## 2. New findings
### A. Arkose docs expose a stronger event-boundary model than many widget families
The hosted iframe/lightbox docs provide explicit `postMessage` event IDs such as:
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

This makes Arkose especially suitable for a practical note centered on:
- event-boundary logging,
- token-bearing callback/message edges,
- and compare-run reasoning across suppressed vs shown challenge flows.

### B. `challenge-suppressed` and `challenge-complete` are both meaningful token-bearing boundaries
The refreshed docs support that session-token-bearing edges are not limited to visible challenge completion.

Useful implication:
- analysts should compare suppressed/no-challenge paths and visible challenge paths as separate operational routes,
- then check whether they converge on the same backend verify/update request and the same first accepted consumer request.

### C. Arkose needed the same correction already applied to other widget families
The key KB correction this run is:
- `response.token` or `payload.sessionToken` visibility is not the final practical milestone,
- the verify/update request is also not always the final practical milestone,
- the strongest downstream anchor is often the **first accepted consumer request**.

For Arkose that may be:
- the first session/bootstrap fetch,
- the first redirect that stops looping,
- the first protected route/API returning real data instead of degraded/challenged state.

### D. Arkose compare-run diagnosis becomes cleaner when split into three downstream boundaries
The most useful post-refresh chain is:

```text
callback/message token visibility
  -> verify/update submission
  -> first downstream accepted consumer
```

That gives a cleaner answer to questions like:
- “Did the hosted iframe flow actually finish?”
- “Did the host page submit the token?”
- “Which request proves the app really accepted the outcome?”

## 3. Sources consulted
### Existing KB material
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- `topics/arkose-funcaptcha-session-and-iframe-workflow-note.md`
- `topics/cloudflare-turnstile-widget-lifecycle-workflow-note.md`
- `sources/browser-runtime/2026-03-14-arkose-funcaptcha-lifecycle-notes.md`
- recent run reports:
  - `runs/2026-03-16-0500-browser-four-boundary-routing-and-perimeterx-callback-consumer.md`
  - `runs/2026-03-16-0600-widget-first-accepted-consumer-boundary-pass.md`

### Fresh external source checks
Official Arkose docs refreshed this run:
- <https://developer.arkoselabs.com/docs/iframe-setup-guide>
- <https://developer.arkoselabs.com/docs/configuration-object>
- <https://developer.arkoselabs.com/docs/verify-api-v4>
- <https://developer.arkoselabs.com/docs/response-object-oncompleted-onerror-onfailed-onresize>

Search-layer query batch:
- `Arkose Labs client API onCompleted onSuppress iframe postMessage verify API`
- `Arkose FunCaptcha iframe challenge-complete sessionToken postMessage docs`
- `Arkose Labs Verify API session token onCompleted onSuppress docs`

### Source-quality judgment
- official Arkose docs are strong on lifecycle, message boundaries, callback objects, and verify semantics
- they are weaker on practitioner-style deep reversing case detail
- still strong enough for this run because the goal was a practical integration/lifecycle note, not undocumented internal telemetry claims

## 4. Reflections / synthesis
This run stayed aligned with the human correction: do not spend the hour on another abstract anti-bot page.

The better move was:
- improve an existing concrete target-family note,
- make it more operational,
- keep it aligned with the browser subtree’s new four-boundary routing language.

A useful practical symmetry now exists across widget-family notes:

```text
widget/bootstrap
  -> token/state visibility
  -> verify/update or submit request
  -> first accepted consumer request
```

Arkose’s distinctive contribution is that the token/state visibility boundary may be a callback or an iframe/lightbox message event rather than just a callback or hidden input.

That makes Arkose a nice bridge case between:
- classic widget-family notes,
- and more explicit host-page / iframe boundary reasoning.

## 5. Candidate topic pages to create or improve
### Improved this run
- `topics/arkose-funcaptcha-session-and-iframe-workflow-note.md`
- `index.md`
- `.learnings/ERRORS.md`

### Created this run
- `sources/browser-runtime/2026-03-16-arkose-first-consumer-and-iframe-boundary-notes.md`
- this run report

### Good next improvements
- improve `topics/browser-request-finalization-backtrace-workflow-note.md`
  - add a short section for targets where callback/message visibility and verify submission are both visible, but the first accepted downstream consumer is still later
- improve `topics/cloudflare-clearance-cookie-and-js-challenge-workflow-note.md`
  - normalize the same consumer-boundary language for script-seeded clearance flows
- improve `topics/browser-side-risk-control-and-captcha-workflows.md`
  - add a short practical routing subsection for widget families with host-page/iframe event boundaries

## 6. Next-step research directions
1. Look for concrete target-grounded case material where Arkose verification succeeds but the first downstream consumer still reveals degraded policy.
2. Extend the same compare-run language to clearance-cookie and JS-challenge notes.
3. Keep reinforcing browser subtree pages around:
   - first accepted consumer request,
   - compare-run divergence point,
   - and downstream policy consequence localization.
4. Prefer more practical notes with breakpoint/hook placement and run-comparison sketches over additional broad taxonomies.

## 7. Concrete scenario notes or actionable tactics added this run
### Practical scenario normalized this run
**Arkose callback/message visibility and verify submission both look correct, but the app still does not behave as accepted.**

### Concrete tactics added
- separate:
  - `onCompleted(response)` / `onSuppress(response)` or `challenge-complete` / `challenge-suppressed`
  - verify/update request carrying `response.token` or `payload.sessionToken`
  - first downstream request/route/session fetch that actually benefits from that transition
- in hosted iframe targets, log `eventId` values first before chasing UI noise
- compare suppressed and visible-challenge runs all the way through the first downstream consumer, not just up to token visibility
- compare pre-reset and post-reset sessions explicitly when same-shape retries behave differently
- do not equate a token-bearing callback/message with final application acceptance

## 8. Errors / sync notes
### Error encountered during this run
A small maintenance-path mismatch occurred when trying to read an expected Arkose source-note filename:
- attempted path used a drifted date/name pattern
- actual source file was present under a different date/name
- impact was low; the run recovered by listing files, reading the actual note, and refreshing official docs directly

This was recorded in:
- `.learnings/ERRORS.md`

### Local preservation status
Local KB progress preserved in:
- `topics/arkose-funcaptcha-session-and-iframe-workflow-note.md`
- `sources/browser-runtime/2026-03-16-arkose-first-consumer-and-iframe-boundary-notes.md`
- `index.md`
- `.learnings/ERRORS.md`
- this run report

### Planned git / sync actions
After this report:
1. commit changes in `/root/.openclaw/workspace`
2. run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
3. if sync fails, record it here while keeping local preservation as the main success condition
