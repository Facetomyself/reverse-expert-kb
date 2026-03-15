# Run Report — 2026-03-15 13:00 Asia/Shanghai

## 1. Scope this run
This run continued the KB’s deliberate pivot away from abstract taxonomy and toward concrete, target-grounded reverse-engineering workflow material.

The run started with a KB state refresh across:
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- current browser-runtime subtree navigation
- recent browser and mobile workflow pages
- recent run reports and source notes

A practical gap surfaced immediately:
- the browser subtree navigation already referenced an Akamai sensor/cookie workflow note
- the source notes for that topic already existed
- but the actual topic page was missing

That made this run a good fit for consolidation-oriented work: turn the existing Akamai source cluster into a real, actionable KB page instead of creating another abstract synthesis page.

The scope for this hour therefore became:
- validate the Akamai source cluster
- create a dedicated practical workflow note centered on sensor submission, `_abck` / `bm_sz`, and first-consumer tracing
- preserve the case-driven/browser-practical direction rather than expanding taxonomy

## 2. New findings
- The existing source cluster was sufficient to justify a dedicated Akamai workflow page rather than another generic anti-bot synthesis page.
- The strongest reusable analyst frame is:
  - **sensor submission boundary**
  - **cookie update / validation state**
  - **first later consumer request whose outcome materially changes**
- A key practical distinction worth normalizing in the KB is:
  - seeing `_abck` is **not** equivalent to solving the workflow.
- The higher-value analyst move is to verify:
  - what request caused `_abck` / `bm_sz` to change,
  - what structured object existed one layer before payload packing,
  - and which later request actually consumed the validated state.
- The best initial breakpoint surfaces for this family are usually boundary-oriented rather than full-bundle-first:
  - verification POST finalization
  - one-layer-earlier payload assembly helper
  - cookie update edge
  - first accepted consumer request after validation

## 3. Sources consulted
### Existing KB material
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- `topics/browser-runtime-subtree-guide.md`
- `topics/reese84-and-utmvc-workflow-note.md`
- `topics/kasada-x-kpsdk-request-attachment-workflow-note.md`
- `sources/browser-runtime/2026-03-15-akamai-sensor-cookie-workflow-notes.md`

### External / search material
Search-layer queries:
- `Akamai Bot Manager _abck bm_sz sensor workflow`
- `Edioff akamai analysis _abck bm_sz`

Primary externally consulted materials:
- `https://github.com/Edioff/akamai-analysis`
- `https://raw.githubusercontent.com/Edioff/akamai-analysis/main/README.md`
- search-layer results also surfaced:
  - `https://stackoverflow.com/questions/57121107/what-is-the-purpose-of-abck-and-bm-sz`
  - `https://github.com/xiaoweigege/akamai2.0-sensor_data`
  - `https://www.akamai.com/products/bot-manager`

### Source-quality judgment
- The strongest usable grounding was the Edioff case-study material because it described the workflow as:
  - script load
  - signal collection
  - sensor payload generation
  - verification POST
  - `_abck` update
  - later cookie-backed validation
- Search results were good enough to corroborate family-level workflow anchors, but not strong enough to justify target-specific or deployment-specific claims.
- The resulting page therefore stayed conservative and workflow-centered.

## 4. Reflections / synthesis
This was a good example of the KB’s new preferred operating mode.

The weak move would have been:
- write a fresh abstract page on “browser anti-bot cookie workflows”
- or leave the Akamai material stranded in a source note
- or continue widening the ontology without closing an obvious concrete gap

The stronger move was:
- notice that a concrete page was already implied by the subtree and source notes
- create that page directly
- center it on operational analyst questions:
  - where is the sensor POST,
  - what is the preimage helper,
  - what changed `_abck`,
  - and which request actually benefited

The best synthesis from this run is:

**Akamai-family browser analysis is usually more tractable when framed as a validation-boundary workflow, not as a giant deobfuscation problem.**

That matters because it changes the analyst’s first move.
Instead of cleaning a huge bundle first, the KB now recommends:
- trap the verification POST,
- move one frame earlier,
- correlate cookie updates,
- and compare accepted vs blocked runs at the same boundary.

## 5. Candidate topic pages to create or improve
### Created this run
- `topics/akamai-sensor-submission-and-cookie-validation-workflow-note.md`

### Improved this run
- the browser-runtime subtree now has one less dangling reference and better practical coverage for a major anti-bot family

### Candidate future creation/improvement
- improve `topics/browser-side-risk-control-and-captcha-workflows.md` with a compact subsection pointing readers toward concrete “collector / validator / consumer” workflow families
- future concrete note on **Akamai compare-run diagnosis under timing/debug pressure** if stronger case material accumulates
- future note on **request-consumer localization after cookie validation** if several vendor families show the same recurring bottleneck strongly enough to justify a cross-family practical page

## 6. Next-step research directions
1. Keep scanning the browser subtree for other implied-but-missing concrete pages rather than defaulting to brand-new abstractions.
2. Continue strengthening concrete notes that explain:
   - where to place breakpoints
   - what to compare between runs
   - how to identify the first decisive boundary
   - how to avoid over-trusting visible cookies or headers
3. Good adjacent browser-family targets include:
   - practical collector / validator / consumer separation across anti-bot systems
   - compare-run diagnosis under debugger/timing pressure
   - mixed JS / transport / session-state failure diagnosis when visible browser state seems right but server treatment diverges
4. Maintain the pattern of turning source clusters into operational playbook pages instead of leaving them as isolated source dumps.

## 7. Concrete scenario notes or actionable tactics added this run
- Added a dedicated workflow page for **Akamai sensor submission and cookie validation**.
- Added practical guidance to anchor on:
  - sensor submission boundary
  - one-layer-earlier payload assembly helper
  - `_abck` / `bm_sz` update edge
  - first later consumer request whose outcome changes materially
- Added an explicit warning that:
  - cookie presence is not equivalent to workflow completion.
- Added concrete failure diagnosis for:
  - copied cookies that still fail
  - huge-bundle-first analysis that never localizes the decisive boundary
  - debugging pressure that changes timing or classification
  - structurally similar payloads with divergent server treatment
- Added small representative code/pseudocode fragments for:
  - request-boundary hooking
  - boundary-recording schema
  - compare-run capture

## 8. Sync / preservation status
- Local KB progress was preserved in:
  - `topics/akamai-sensor-submission-and-cookie-validation-workflow-note.md`
  - this run report
- Next operational steps after writing this report:
  - commit the KB changes in `/root/.openclaw/workspace`
  - run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
  - if sync fails, preserve local state and record the failure locally
