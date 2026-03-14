# Run Report — 2026-03-15 02:00 Asia/Shanghai

## 1. Scope this run
This run started by reading the current KB structure, recent practical browser and mobile workflow pages, and the latest run reports to avoid sliding back into abstract taxonomy work.

A concrete browser-family gap was selected for this run:
- the KB already had practical notes for Turnstile, Arkose, hCaptcha, `acw_sc__v2`, ByteDance web signatures, request-boundary backtracing, and parameter-path localization
- but it did **not** yet have a dedicated practical note for **Akamai-family browser workflows centered on sensor submission, `_abck` / `bm_sz` cookie lifecycle, and the first behavior-changing consumer request**

The main outputs were therefore:
- `topics/akamai-sensor-submission-and-cookie-validation-workflow-note.md`
- `sources/browser-runtime/2026-03-15-akamai-sensor-cookie-workflow-notes.md`
- navigation updates in `index.md`, `topics/browser-runtime-subtree-guide.md`, and `topics/browser-side-risk-control-and-captcha-workflows.md`

This stayed aligned with the human correction: concrete workflow page first, not another broad anti-bot synthesis page.

## 2. New findings
- A useful Akamai-family workflow can be framed conservatively and practically around recurring analyst-visible boundaries:
  - sensor script load
  - signal collection / payload assembly
  - verification or challenge POST boundary
  - `_abck` / `bm_sz` cookie state update
  - first later request whose server behavior changes materially
- Public case-study-style material was sufficient to justify a **workflow page**, even if it was not strong enough to justify sweeping universal claims about every deployment.
- The practical mistake to guard against is very clear:
  - analysts see `_abck` in storage and stop there
  - but that does **not** prove the first behavior-changing consumer request is understood
- The source cluster reinforced several KB-consistent workflow principles:
  - request-boundary-first tracing beats whole-bundle cleanup early on
  - visible cookie state is not the same thing as accepted session state
  - compare-run discipline matters because accepted and challenged runs can still share obvious visible artifacts
  - instrumentation/timing pressure can distort conclusions on this family
- One useful family-level distinction emerged:
  - `acw_sc__v2`-style cases are often best entered through cookie bootstrap and consumer-path tracing
  - Akamai-family cases are often best entered through **sensor submission boundary -> cookie update -> first consumer request**

## 3. Sources consulted
### Existing KB material
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- `topics/browser-runtime-subtree-guide.md`
- `topics/browser-side-risk-control-and-captcha-workflows.md`
- `topics/browser-request-finalization-backtrace-workflow-note.md`
- `topics/browser-parameter-path-localization-workflow-note.md`
- `topics/acw-sc-v2-cookie-bootstrap-and-consumer-path-note.md`
- `topics/reese84-and-utmvc-workflow-note.md`
- recent run reports including:
  - `runs/2026-03-15-0000-browser-request-finalization-backtrace.md`
  - `runs/2026-03-15-0100-hcaptcha-submit-siteverify-workflow.md`

### External / search material
- Search-layer multi-query run for Akamai Bot Manager workflow, `_abck`, `bm_sz`, and sensor-data / verification boundary
- GitHub case-study repository page and raw README for:
  - `https://github.com/Edioff/akamai-analysis`
  - `https://raw.githubusercontent.com/Edioff/akamai-analysis/main/README.md`
- GitHub repository page for redirected result:
  - `https://github.com/botswin/Akamai-Privacy-Research`

### Failed or weak source attempts
- `web_search` (Brave-backed) was unavailable because the Brave API key is not configured in this environment.
- `web_fetch` against the Stack Overflow `_abck` / `bm_sz` discussion returned a 403 interstitial.
- a raw README fetch for `botswin/Akamai-Privacy-Research` returned 404.

These failures were recorded and did not block the run, because the search-layer path and the Edioff case-study material were enough to support a conservative workflow page.

## 4. Reflections / synthesis
This run stayed on the corrected path.

The weak old-mode move would have been:
- create another generic browser anti-bot comparison page
- or write a broad Akamai taxonomy page with little breakpoint value

The stronger move was:
- identify the missing concrete family entry surface
- anchor the page around sensor submission and cookie-validation boundaries
- write it as a practical workflow note with:
  - target pattern / scenario
  - analyst goal
  - concrete workflow
  - breakpoint/hook placement
  - likely failure modes
  - environment assumptions
  - representative code/pseudocode fragments
  - what to verify next

That gives the browser subtree a clearer practical spread:
- widget/session families (Turnstile, Arkose, hCaptcha)
- cookie-bootstrap family (`acw_sc__v2`)
- request-signature family (ByteDance)
- request-boundary tracing pages
- sensor-submission / cookie-validation family (Akamai)

This is a healthier direction than adding more ontology layers.

## 5. Candidate topic pages to create or improve
### Created this run
- `topics/akamai-sensor-submission-and-cookie-validation-workflow-note.md`

### Improved this run
- `index.md`
- `topics/browser-runtime-subtree-guide.md`
- `topics/browser-side-risk-control-and-captcha-workflows.md`

### Candidate future creation/improvement
- improve `topics/browser-environment-reconstruction.md` with a compact section on when sensor-workflow cases should delay full environment rebuild until request/cookie boundaries are localized
- improve `topics/browser-debugger-detection-and-countermeasures.md` with a short section on timing-trap / observation-distortion diagnosis in large anti-bot sensor bundles
- possible future concrete family note if source quality becomes strong enough for workflow-level synthesis:
  - Imperva / PerimeterX / PX-style browser workflow
  - stronger Akamai v3-specific note if evidence matures beyond current family-level boundary guidance

## 6. Next-step research directions
1. Continue adding missing **family workflow notes** where the practical boundary is clear enough to guide breakpoints and compare-runs.
2. Strengthen browser subtree navigation around analyst entry boundaries, not just vendor/family names:
   - widget lifecycle
   - callback/message handoff
   - request finalization backtrace
   - cookie bootstrap
   - sensor submission / cookie validation
3. Look for additional source clusters where practical details are strong enough to support:
   - request sequencing maps
   - preimage capture points
   - accepted-vs-failed compare-run artifacts
   - minimal-harness decision rules
4. Keep treating tool/source failures as non-blocking unless they remove all provenance.

## 7. Concrete scenario notes or actionable tactics added this run
- Added a concrete Akamai-family workflow centered on:
  - localizing the sensor/verification POST
  - stepping one layer earlier to the last structured payload stage
  - localizing `_abck` / `bm_sz` update boundaries
  - tracing the first request whose server behavior actually changes
- Added breakpoint families for:
  - final verification-request boundary
  - one-layer-earlier payload assembly helper
  - cookie write/update observation
  - first consumer request boundary
- Added explicit failure diagnosis for:
  - `_abck` visible but workflow still unsolved
  - whole-bundle cleanup started too early
  - accepted and challenged runs both showing visible cookie state
  - instrumentation/timing pressure distorting evidence
  - harness reproducing shape but not server outcome

## 8. Sync / preservation status
- Local KB progress was preserved in:
  - `topics/akamai-sensor-submission-and-cookie-validation-workflow-note.md`
  - `sources/browser-runtime/2026-03-15-akamai-sensor-cookie-workflow-notes.md`
  - this run report
- Tooling failures were recorded in `.learnings/ERRORS.md` and in this run report:
  - missing Brave API key for `web_search`
  - 403 interstitial for one Stack Overflow fetch
  - 404 for one raw GitHub README attempt
- Next operational steps after this report:
  - commit workspace changes
  - run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
  - if sync fails, keep local state and record the failure