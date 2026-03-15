# Run Report — 2026-03-16 05:00 Asia/Shanghai

## 1. Scope this run
This run focused on strengthening the browser anti-bot branch with a more concrete, operator-usable routing model instead of creating another abstract topic page.

The work centered on two goals:
1. normalize an explicit practical routing chain in the browser parent page
2. sharpen the PerimeterX / HUMAN concrete workflow note using stronger callback-to-consumer evidence from official docs/sample material

Files reviewed at the start of this run included:
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- `topics/browser-runtime-subtree-guide.md`
- `topics/browser-side-risk-control-and-captcha-workflows.md`
- `topics/perimeterx-human-cookie-collector-workflow-note.md`
- `topics/akamai-sensor-submission-and-cookie-validation-workflow-note.md`
- `sources/browser-runtime/2026-03-15-perimeterx-human-cookie-collector-notes.md`
- recent run reports through `runs/2026-03-16-0400-perimeterx-bootstrap-solve-consumer.md`

## 2. New findings
The main new finding this run is that the browser subtree is ready for a shared **four-boundary operator-routing model**:

```text
bootstrap anchor
  -> state write or state exposure boundary
  -> validation / refresh / solve boundary
  -> first accepted consumer request
```

This improves the KB because it gives a concrete decision frame for real targets instead of routing only by family labels such as captcha / anti-bot / signature.

Concrete findings added this run:

1. **The first accepted consumer request is still the most commonly missed boundary.**
   Recent concrete pages repeatedly show that analysts stop too early at visible cookies, callback success, or token generation.

2. **PerimeterX / HUMAN challenge success is better modeled as a host-page handoff boundary.**
   Official HUMAN docs and official PerimeterX sample material around `_pxOnCaptchaSuccess` support treating callback success as a bridge into the next request-producing code path, not just as a UI event.

3. **Browser parent pages can now route analysts by workflow stage, not just topic family.**
   The browser risk-control parent page now explicitly links Akamai, PerimeterX / HUMAN, Reese84 / `___utmvc`, widget families, and request-signature families through the same practical chain.

4. **The PerimeterX / HUMAN note is stronger when it explicitly asks what the callback does next.**
   The important question is not only whether `_pxOnCaptchaSuccess` exists, but whether it reloads, refreshes state, unlocks UI only, or directly causes the first accepted consumer request.

## 3. Sources consulted
### Existing KB material
- `research/reverse-expert-kb/index.md`
- `topics/browser-runtime-subtree-guide.md`
- `topics/browser-side-risk-control-and-captcha-workflows.md`
- `topics/perimeterx-human-cookie-collector-workflow-note.md`
- `topics/akamai-sensor-submission-and-cookie-validation-workflow-note.md`
- `sources/browser-runtime/2026-03-15-perimeterx-human-cookie-collector-notes.md`
- `sources/browser-runtime/2026-03-15-akamai-sensor-cookie-workflow-notes.md`

### External / search material
Search-layer query batch executed this run:
- `PerimeterX _pxOnCaptchaSuccess first consumer request reverse engineering`
- `HUMAN Security first party init.js xhr collector _px3 reverse engineering`
- `PerimeterX challenge success callback later request cookie refresh reverse engineering`

Most useful surfaced sources:
- official sample repo: <https://github.com/PerimeterX/perimeterx-abr-samples>
- official sample/demo README: <https://github.com/PerimeterX/perimeterx-chrome-extension-demo/blob/master/README.md>
- HUMAN first-party/CDN docs: <https://docs.humansecurity.com/applications/generic-cdn-first-party-config>
- HUMAN first-party config docs: <https://docs.humansecurity.com/applications/first-party-configuration-nginx-lua>
- HUMAN challenge customization docs: <https://docs.humansecurity.com/applications/customize-challenge-page>
- HUMAN challenge integration testing docs: <https://docs.humansecurity.com/applications/human-challenge-integration-testing-process>
- HUMAN cookie/storage docs: <https://docs.humansecurity.com/applications/use-of-cookies-web-storage>

### Source-quality judgment
- strongest evidence this run came from official HUMAN docs and official PerimeterX sample material
- public reverse repos remain useful for workflow shape, but this run did not need to rely on them heavily for the new claims
- the official sample material was especially useful because it strengthened the callback-to-consumer boundary without pushing the KB into brittle internals

## 4. Reflections / synthesis
This run reinforced the human correction about the KB’s direction.

The wrong move would have been:
- create another generic anti-bot overview
- split browser pages into more labels and taxonomies
- overfit one vendor family’s field semantics from noisy public repos

The stronger move was:
- improve an existing browser parent page with a practical routing heuristic analysts can actually use
- strengthen an existing concrete target-family note with a better callback-to-consumer question
- keep the work cumulative and structural while still practical-first

A useful synthesis now visible in the browser subtree is:
- many anti-bot families differ in artifacts
- but a large share of practical debugging still reduces to the same sequence:
  - what bootstraps the protected flow?
  - what state first becomes visible?
  - what request/callback actually refreshes or validates that state?
  - what later consumer request proves the workflow worked?

That is a much better organizing principle for this branch than more top-level abstraction.

## 5. Candidate topic pages to create or improve
### Improved this run
- `topics/browser-side-risk-control-and-captcha-workflows.md`
- `topics/perimeterx-human-cookie-collector-workflow-note.md`
- `sources/browser-runtime/2026-03-15-perimeterx-human-cookie-collector-notes.md`
- `index.md`

### Created this run
- this run report

### Candidate future creation/improvement
- improve `topics/cloudflare-clearance-cookie-and-js-challenge-workflow-note.md` with the same four-boundary routing language
- improve `topics/reese84-and-utmvc-workflow-note.md` with a short explicit “first accepted consumer” subsection for symmetry with PerimeterX / HUMAN and Akamai
- improve `topics/browser-runtime-subtree-guide.md` so it points readers not just to families, but to the shared operator chain across those families
- improve `topics/browser-fingerprint-and-state-dependent-token-generation.md` with a short note separating visible token generation from first accepted consumer proof

## 6. Next-step research directions
1. Continue strengthening existing browser concrete notes before adding new browser taxonomy pages.
2. Propagate the four-boundary language through the strongest browser family notes where it materially improves operator value.
3. Look for additional official docs or public code that clarify callback-to-consumer transitions, especially for challenge-widget families.
4. Keep improving parent pages only when they help route real analysis decisions rather than just expand abstract coverage.

## 7. Concrete scenario notes or actionable tactics added this run
This run added and normalized several practical tactics:

### Shared browser tactic
When a browser anti-bot target is noisy, classify evidence by:
- bootstrap anchor
- state write/exposure boundary
- validation/refresh/solve boundary
- first accepted consumer request

### PerimeterX / HUMAN callback tactic
If `_pxOnCaptchaSuccess` or equivalent callback exists, do not treat that as the endpoint.
Check whether it:
- reloads the page
- triggers collector refresh
- unlocks UI only
- directly issues the first accepted consumer request

### Parent-page routing tactic
For browser anti-bot work, route the analyst by the earliest uncertain boundary, not by family label alone.
Examples:
- if the unknown is “which script/route starts this?” -> bootstrap anchor
- if the unknown is “what state became visible?” -> state write/exposure
- if the unknown is “what refreshed it?” -> validation/refresh/solve boundary
- if the unknown is “what proves success?” -> first accepted consumer request

## 8. Sync / preservation status
### Local preservation
Local KB progress preserved in:
- `topics/browser-side-risk-control-and-captcha-workflows.md`
- `topics/perimeterx-human-cookie-collector-workflow-note.md`
- `sources/browser-runtime/2026-03-15-perimeterx-human-cookie-collector-notes.md`
- `index.md`
- this run report

### Git / sync actions
Planned after writing this report:
1. commit changes in `/root/.openclaw/workspace`
2. run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
3. if sync fails, preserve local progress and update this report with the failure
