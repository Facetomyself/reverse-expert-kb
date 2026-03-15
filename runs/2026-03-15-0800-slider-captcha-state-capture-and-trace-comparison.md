# Run Report — 2026-03-15 08:00 Asia/Shanghai

## 1. Scope this run
This run began by rereading the KB root files, browser subtree, recent browser practical workflow notes, and recent run reports to stay aligned with the human correction: **shift away from abstract/taxonomy-heavy growth and toward concrete, case-driven, code-adjacent reverse-engineering knowledge**.

The browser subtree already had several concrete target-family notes:
- GeeTest v4 `w` / validate
- DataDome cookie / challenge
- Turnstile widget lifecycle
- Arkose / FunCaptcha session + iframe
- hCaptcha callback / submit / siteverify
- Akamai sensor / cookie validation
- PerimeterX collector / cookie refresh
- Kasada `X-KPSDK-*` request attachment

A remaining gap was a **cross-family but still highly practical workflow page** for slider/canvas-style challenge analysis itself.
The KB had family notes that touched pieces of this problem, but not a focused playbook for:
- locating the actual challenge start edge
- capturing challenge assets and metadata
- finding the last readable movement / answer object before packing
- distinguishing challenge success from later redemption success
- comparing accepted and failed runs at bounded lifecycle edges

This run therefore focused on creating:
- `topics/slider-captcha-state-capture-and-trace-comparison-workflow-note.md`
- `sources/browser-runtime/2026-03-15-slider-captcha-state-capture-and-trace-comparison-notes.md`
- navigation updates in `index.md`, `topics/browser-runtime-subtree-guide.md`, and `topics/browser-side-risk-control-and-captcha-workflows.md`

This was intentionally chosen over creating another abstract browser-risk-control synthesis page.

## 2. New findings
- Official and practitioner material together support a durable workflow model for slider/canvas targets:

```text
challenge trigger
  -> challenge assets / metadata
  -> movement / answer object
  -> pack/encrypt boundary
  -> token/result object
  -> final redemption request
```

- The most useful technical leverage point is often **not** the final opaque request payload, but the **last structured movement / answer object one or two frames earlier**.
- A recurring practical mistake is to treat a visible solved challenge as equivalent to final acceptance. Real targets often split:
  - local challenge success
  - token / validate object issuance
  - final backend or app redemption
- A strong compare-run strategy for this family should be organized around the same lifecycle boundaries each time:
  - start edge
  - asset/metadata fetch
  - structured trace object
  - packed submit
  - success object
  - redemption request
- The Castle analysis of a Binance custom slider family was especially useful because it exposes the full chain:
  - precheck trigger
  - challenge fetch
  - encrypted submit data
  - decrypted payload containing movement and fingerprint data
  - later token verification request
- Open-source GeeTest v4 slide material was useful as **workflow evidence**, not as proof of stable internals. The durable lesson is to anchor on challenge artifacts and readable structures before bundle-wide deobfuscation.

## 3. Sources consulted
### Existing KB material
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- `topics/browser-side-risk-control-and-captcha-workflows.md`
- `topics/geetest-v4-w-parameter-and-validate-workflow-note.md`
- `topics/datadome-cookie-challenge-workflow-note.md`
- `topics/cloudflare-turnstile-widget-lifecycle-workflow-note.md`
- `topics/arkose-funcaptcha-session-and-iframe-workflow-note.md`
- `topics/browser-runtime-subtree-guide.md`
- recent browser practical run reports under `runs/`

### External / newly captured material
- GeeTest official overview:
  - `https://docs.geetest.com/BehaviorVerification/overview/overview`
- GitHub:
  - `https://github.com/gravilk/geetest-v4-slide-documented`
- Castle defender analysis:
  - `https://blog.castle.io/what-a-binance-captcha-solver-tells-us-about-todays-bot-threats`
- search-layer queries around:
  - GeeTest slider reverse engineering workflow
  - slider captcha canvas movement trace workflow
  - GeeTest v4 slide / `w` practical analysis

### Source-quality judgment
- Vendor docs were useful for lifecycle/product grounding, not internals.
- Open-source and practitioner material were useful for workflow shape and analyst leverage, but version-sensitive.
- The Castle article was high-value because it explicitly exposed a trigger → trace → packed submit → token → verify chain.
- Because the source cluster was mixed, this run wrote a **conservative workflow page** instead of overclaiming product-specific invariants.

## 4. Reflections / synthesis
This run followed the corrected KB direction well.

The weak move would have been:
- create another high-level “slider captcha taxonomy” page
- or further widen the generic browser anti-bot synthesis page

The stronger move was:
- identify a concrete recurring analyst problem
- use a small source cluster to derive durable operational boundaries
- produce a workflow page that analysts could actually apply while debugging a real target

The most useful synthesis from this run is that slider/canvas families should be modeled as **state/trace/redeem workflows** rather than only as image problems or encrypted-parameter problems.
That framing helps decide:
- where to place breakpoints
- what to compare across runs
- how to separate local success from final acceptance
- when deeper deobfuscation is worth the cost

## 5. Candidate topic pages to create or improve
### Created this run
- `topics/slider-captcha-state-capture-and-trace-comparison-workflow-note.md`

### Improved this run
- `index.md`
- `topics/browser-runtime-subtree-guide.md`
- `topics/browser-side-risk-control-and-captcha-workflows.md`

### New source note added
- `sources/browser-runtime/2026-03-15-slider-captcha-state-capture-and-trace-comparison-notes.md`

### Candidate future creation/improvement
- improve `topics/browser-side-risk-control-and-captcha-workflows.md` with a short section on challenge-start-edge vs visible-widget confusion
- improve `topics/browser-request-finalization-backtrace-workflow-note.md` with a compact note about stepping upward from opaque challenge submit blobs into structured trace builders
- consider a future practical page on **challenge retry / escalation / reset comparison workflows** if enough families keep showing the same pattern

## 6. Next-step research directions
1. Continue filling practical browser gaps with workflow notes that sit between broad family pages and target-specific pages.
2. Look for repeated scenario patterns such as:
   - retry / reset / escalation diagnosis
   - hidden precheck before visible challenge
   - local success vs final redemption drift
   - movement-trace builder localization
3. Prefer notes that include:
   - breakpoint placement
   - compare-run templates
   - structured object boundaries
   - concrete failure diagnosis
4. Keep using mixed-source evidence conservatively: workflow-first, not brittle algorithm snapshots.

## 7. Concrete scenario notes or actionable tactics added this run
- Added a dedicated workflow for slider/canvas challenge analysis centered on:
  - challenge start edge
  - challenge asset/metadata fetch
  - last structured movement/answer object
  - pack/encrypt boundary
  - success object
  - final redemption request
- Added practical breakpoint families for:
  - challenge start
  - asset/metadata request
  - trace/answer builder
  - serializer/encrypt helper
  - token/validate callback boundary
  - final redemption request
- Added explicit failure diagnosis for:
  - overfocusing on image assets only
  - overfocusing on final encrypted payload only
  - confusing local challenge success with final acceptance
  - comparing whole sessions instead of bounded lifecycle edges
  - letting heavy instrumentation distort behavior before outward boundaries are stable

## 8. Sync / preservation status
- Local KB progress was preserved in:
  - `topics/slider-captcha-state-capture-and-trace-comparison-workflow-note.md`
  - `sources/browser-runtime/2026-03-15-slider-captcha-state-capture-and-trace-comparison-notes.md`
  - browser navigation updates
  - this run report
- Next operational steps after writing this report:
  - commit workspace changes
  - run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
  - if sync fails, record the failure while preserving local KB state
