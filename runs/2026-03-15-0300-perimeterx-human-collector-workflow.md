# Run Report — 2026-03-15 03:00 Asia/Shanghai

## 1. Scope this run
This run started by loading the current KB structure, recent browser workflow pages, and the newest run reports so the work would stay on the corrected direction: **more concrete, case-driven, code-adjacent workflow material; less abstract taxonomy growth**.

The browser subtree already had practical notes for:
- Turnstile
- Arkose FunCaptcha
- hCaptcha
- `acw_sc__v2`
- Reese84 / `___utmvc`
- ByteDance-style request-signature families
- Akamai sensor / cookie-validation workflows
- request-boundary backtracing and parameter-path localization

A missing concrete family entry this run was:
- **PerimeterX / HUMAN browser workflows centered on collector routes, `_px*` cookie/state family, challenge-success handoff, and the first application request whose server behavior changes**

The main outputs were therefore:
- `topics/perimeterx-human-cookie-collector-workflow-note.md`
- `sources/browser-runtime/2026-03-15-perimeterx-human-cookie-collector-notes.md`
- navigation updates in `index.md`, `topics/browser-runtime-subtree-guide.md`, and `topics/browser-side-risk-control-and-captcha-workflows.md`

This run explicitly chose a **real target-family workflow page** over any new abstract anti-bot synthesis page.

## 2. New findings
- Official HUMAN docs provide enough concrete analyst-facing structure to justify a workflow note:
  - first-party route family such as `/<app>/init.js` and `/<app>/xhr/*`
  - cookie/storage family such as `_px`, `_px2`, `_px3`, `_pxvid`, `pxcts`, `_pxhd`, and `_pxff_*`
  - challenge/custom-block handoff surfaces such as `blockScript` and `_pxOnCaptchaSuccess`
- A practical analyst framing for this family is:

```text
bootstrap script
  -> collector request
  -> cookie/state refresh
  -> challenge-success handoff if present
  -> first application request whose server behavior changes
```

- The most important practical trap is clear:
  - analysts often see `_px3` / `_pxvid` and stop there
  - but visible `_px*` state does not prove the **collector-to-consumer path** is understood
- The docs also make a useful diagnostic point explicit:
  - verification/API paths are invoked when a risk cookie does not exist, is expired, or is invalid
  - that makes cookie freshness / validity transitions more important than cookie-name visibility alone
- Public reversing repositories around PerimeterX are noisy and version-specific, but they still reinforce a stable practical workflow shape:
  - loaded client script
  - payload/counter/session family
  - challenge/collector boundary
  - accepted-state update
- This makes PerimeterX / HUMAN a good fit for a concrete note focused on:
  - collector localization
  - cookie refresh timing
  - challenge callback handoff
  - first behavior-changing consumer request

## 3. Sources consulted
### Existing KB material
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- `topics/browser-runtime-subtree-guide.md`
- `topics/browser-side-risk-control-and-captcha-workflows.md`
- `topics/browser-request-finalization-backtrace-workflow-note.md`
- `topics/browser-parameter-path-localization-workflow-note.md`
- `topics/akamai-sensor-submission-and-cookie-validation-workflow-note.md`
- `topics/reese84-and-utmvc-workflow-note.md`
- `topics/acw-sc-v2-cookie-bootstrap-and-consumer-path-note.md`
- recent browser practical run reports

### External / search material
- Search-layer multi-query run for:
  - `PerimeterX Human Security browser token workflow reverse engineering`
  - `PerimeterX _px3 _pxvid cookie request workflow`
  - `Imperva bot management browser cookie sensor workflow`
- Official HUMAN docs:
  - `https://docs.humansecurity.com/applications/nginx-lua-configuration-options`
  - `https://docs.humansecurity.com/applications/use-of-cookies-web-storage`
- Public practitioner repositories:
  - `https://github.com/Pr0t0ns/PerimeterX-Reverse`
  - `https://github.com/Pr0t0ns/PerimeterX-Solver`

### Source-quality judgment
- HUMAN docs were the strongest source for:
  - route family
  - cookie/storage names
  - challenge/ABR callback boundaries
- Public reverse repos were used conservatively:
  - useful for workflow shape
  - not strong enough for overconfident universal field semantics
- Imperva-specific result quality was weaker for this run, so the run stayed focused on the better-supported PerimeterX / HUMAN family rather than forcing an Imperva page with thin evidence

## 4. Reflections / synthesis
This run stayed aligned with the human correction.

The weak move would have been:
- write another broad “anti-bot vendor comparison” page
- or create a generic cookie-taxonomy page detached from analyst action

The stronger move was:
- identify a concrete missing browser family
- anchor it around a practical route/state/consumer sequence
- write it as a workflow note with:
  - target pattern / scenario
  - analyst goal
  - concrete workflow
  - breakpoint / hook placement
  - likely failure modes
  - environment assumptions
  - representative sketches and recording templates
  - what to verify next

This gives the browser subtree another realistic analyst entry surface:
- widget lifecycle families
- request-signature families
- cookie-bootstrap families
- sensor submission / cookie validation families
- **collector / cookie-refresh / first-consumer families**

That is a much healthier direction than growing more abstract browser anti-bot structure.

## 5. Candidate topic pages to create or improve
### Created this run
- `topics/perimeterx-human-cookie-collector-workflow-note.md`

### Improved this run
- `index.md`
- `topics/browser-runtime-subtree-guide.md`
- `topics/browser-side-risk-control-and-captcha-workflows.md`

### New source note added
- `sources/browser-runtime/2026-03-15-perimeterx-human-cookie-collector-notes.md`

### Candidate future creation/improvement
- improve `topics/browser-environment-reconstruction.md` with a compact section on when collector/cookie-refresh families should delay full environment rebuild until collector and first-consumer boundaries are known
- improve `topics/browser-debugger-detection-and-countermeasures.md` with a small section on observation-pressure during anti-bot collector flows
- possible future concrete family note if source quality strengthens enough:
  - Imperva / Incapsula practical workflow centered on challenge/bootstrap / `reese84` / consumer-path evidence, but only if the evidence cluster becomes stronger than this run’s Imperva results

## 6. Next-step research directions
1. Continue filling **missing concrete browser target-family notes** where the practical boundary is strong enough to guide breakpoints and compare-runs.
2. Keep improving the browser subtree around analyst entry boundaries, not just vendor names:
   - widget/session handoff
   - callback/message handoff
   - request finalization backtrace
   - cookie bootstrap
   - sensor submission / cookie validation
   - collector / cookie refresh / first-consumer mapping
3. Look for source clusters that support practical additions such as:
   - accepted-vs-failed compare-run checklists
   - request sequencing maps
   - stale-visible-state vs accepted-state diagnosis
   - minimal harness rules for one verified request role
4. Continue refusing to create thin abstract pages when a stronger concrete family/workflow page is available instead.

## 7. Concrete scenario notes or actionable tactics added this run
- Added a concrete PerimeterX / HUMAN workflow centered on:
  - bootstrap script identification
  - collector/XHR localization
  - `_px*` cookie/storage state observation
  - challenge-success callback / host-page handoff
  - first application request whose server behavior changes materially
- Added breakpoint families for:
  - sensor/bootstrap script load edge
  - collector / XHR submission boundary
  - cookie/state update observation
  - challenge-success callback edge
  - first behavior-changing consumer request
- Added explicit failure diagnosis for:
  - visible `_px3` / `_pxvid` mistaken for solved workflow
  - challenge success without identified app consumer path
  - replay with copied cookies but no collector refresh
  - whole-bundle deobfuscation started before route family was localized
  - same consumer request shape with different server result because freshness/session/trust changed

## 8. Sync / preservation status
- Local KB progress was preserved in:
  - `topics/perimeterx-human-cookie-collector-workflow-note.md`
  - `sources/browser-runtime/2026-03-15-perimeterx-human-cookie-collector-notes.md`
  - navigation updates in the browser subtree
  - this run report
- Next operational steps after writing this report:
  - commit workspace changes
  - run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
  - if sync fails, record the failure while preserving local KB state
