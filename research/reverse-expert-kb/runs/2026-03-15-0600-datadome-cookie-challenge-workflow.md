# Run Report — 2026-03-15 06:00 Asia/Shanghai

## 1. Scope this run
This run started by reading the KB root files, current browser-runtime structure, recent practical browser workflow notes, and the latest run reports to stay aligned with the human correction: **less abstract taxonomy growth, more concrete target-family workflow material**.

The browser subtree already had dedicated practical notes for:
- Turnstile
- Arkose FunCaptcha
- hCaptcha
- GeeTest v4
- Akamai sensor/cookie workflows
- Kasada request attachment
- PerimeterX / HUMAN collector/cookie-refresh paths
- request-finalization backtrace and parameter-path localization

A remaining practical gap was that **DataDome still existed mainly as one branch inside a broader comparison page**:
- `topics/datadome-geetest-kasada-workflow-note.md`

That comparison note remained useful, but it was no longer the best primary entry for actual analyst work.
The KB still lacked a dedicated DataDome page focused on:
- JS-tag or first-party bootstrap
- `/js/` signal submission boundaries
- `datadome` / `dd*` cookie-storage lifecycle
- challenge / device-check / interstitial handoff
- first behavior-changing consumer-request diagnosis
- compare-runs that distinguish stale visible state from a real accepted transition

This run therefore focused on creating a **dedicated DataDome practical workflow page** and integrating it into the browser subtree.

Primary outputs:
- `topics/datadome-cookie-challenge-workflow-note.md`
- `sources/browser-runtime/2026-03-15-datadome-cookie-challenge-workflow-notes.md`
- navigation updates in `index.md`, `topics/browser-runtime-subtree-guide.md`, and `topics/browser-side-risk-control-and-captcha-workflows.md`

This run explicitly chose a **concrete target-family workflow note** over any new abstract anti-bot synthesis page.

## 2. New findings
- Official DataDome JS-tag docs provide a strong lifecycle map around:
  - `tags.js` or first-party `/tags.js`
  - early script loading to intercept protected XHR/fetch requests
  - signal submission through `/js/` or reverse-proxied equivalent
  - read/write dependence on the `datadome` cookie
- Official cookie/storage docs provide a concrete outward state family:
  - `datadome` cookie
  - transient `dd_testcookie`
  - `ddSession` local-storage mirror when `sessionByHeader` is enabled
  - `ddOriginalReferrer` in session storage when Device Check or CAPTCHA flows trigger
- Official slider docs reinforce that DataDome analysis is not merely about a visible slider artifact; browser/environment/behavior/consistency signals matter materially.
- The practical analyst framing that emerged is:

```text
JS-tag / first-party bootstrap
  -> `/js/` signal submission
  -> `datadome` cookie and sibling state update
  -> device-check / slider / response-page handoff if risk escalates
  -> first later protected request whose treatment changes
```

- The main workflow trap is clear:
  - analysts can waste time watching only the visible challenge/interstitial
  - or they can over-trust cookie capture alone
  - when the highest-leverage boundaries are often the **signal-submission edge**, the **last structured signal object before packing**, and the **first later consumer request whose server treatment changes**
- Existing practitioner material already in the KB remains useful as family-shape evidence:
  - DataDome behaves more like a browser sensor + state-transition + challenge workflow than a pure image/artifact family
  - it is meaningfully distinct from GeeTest-style answer-packing and Kasada-style request-role token attachment

## 3. Sources consulted
### Existing KB material
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- `topics/browser-runtime-subtree-guide.md`
- `topics/browser-side-risk-control-and-captcha-workflows.md`
- `topics/datadome-geetest-kasada-workflow-note.md`
- `topics/reese84-and-utmvc-workflow-note.md`
- `topics/perimeterx-human-cookie-collector-workflow-note.md`
- recent browser practical run reports
- `sources/browser-runtime/2026-03-14-datadome-geetest-kasada-notes.md`

### External / search material
Official docs fetched:
- `https://docs.datadome.co/docs/javascript-tag`
- `https://docs.datadome.co/docs/cookie-session-storage`
- `https://docs.datadome.co/docs/datadome-captcha`

Search-layer queries:
- `DataDome slider interstitial dd payload cookie workflow`
- `DataDome captcha delivery interstitial javascript tag documentation`
- `DataDome dd parameter captchaUrl cookie reverse workflow`

High-signal search results inspected or used as family-shape confirmation:
- DataDome official JS-tag docs
- DataDome cookie/session-storage docs
- DataDome slider docs
- existing practitioner repositories already captured in the earlier KB source cluster

### Source-quality judgment
- Official DataDome docs were the strongest sources for:
  - deployment and bootstrap shape
  - `/js/` signal boundary
  - state-family semantics
  - challenge/device-check handoff clues
  - browser-signal categories
- Practitioner material remains useful for:
  - network-anchor-first workflow shape
  - family differentiation versus GeeTest and Kasada
  - one-layer-earlier preimage thinking
- Detailed public internal-payload claims remain noisy and version-sensitive.
  So the resulting page stayed conservative on invariant internals and focused on **workflow boundaries**.

## 4. Reflections / synthesis
This run stayed on the corrected direction.

The weak move would have been:
- expand the old three-family comparison page
- or write another abstract anti-bot summary page

The stronger move was:
- identify that DataDome was still underrepresented as a practical cookbook page
- build a dedicated workflow note around browser-visible state transitions analysts can actually use
- connect DataDome to a distinct practical identity in the browser subtree

The resulting DataDome page improves the subtree because it now sits cleanly beside neighboring practical pages:
- GeeTest emphasizes answer-object -> pack/encrypt -> `getValidate()` -> `/validate`
- Kasada emphasizes challenge/bootstrap -> `X-KPSDK-*` request attachment -> request-role outcome
- Akamai emphasizes sensor POST -> cookie validation -> first consumer request
- PerimeterX / HUMAN emphasizes collector -> `_px*` refresh -> challenge-success handoff -> first consumer request
- **DataDome now explicitly emphasizes JS-tag/bootstrap -> `/js/` signal submission -> `datadome` / `dd*` state -> challenge/device-check handoff -> first consumer request**

That is a better use of effort than more taxonomy growth.

## 5. Candidate topic pages to create or improve
### Created this run
- `topics/datadome-cookie-challenge-workflow-note.md`

### Improved this run
- `index.md`
- `topics/browser-runtime-subtree-guide.md`
- `topics/browser-side-risk-control-and-captcha-workflows.md`

### New source note added
- `sources/browser-runtime/2026-03-15-datadome-cookie-challenge-workflow-notes.md`

### Candidate future creation/improvement
- improve `topics/browser-environment-reconstruction.md` with a compact section on when to treat challenge/interstitial handoff state as part of the environment contract
- improve `topics/browser-parameter-path-localization-workflow-note.md` with a short subsection on locating one-layer-earlier structured preimages above a packed `/js/`-style browser signal submission
- improve `topics/browser-debugger-detection-and-countermeasures.md` with a brief section on minimizing observation pressure during early JS-tag/bootstrap and anti-automation consistency-check analysis

## 6. Next-step research directions
1. Continue filling **remaining browser family gaps** only where the KB still has a comparison note but not a dedicated practical cookbook page.
2. Prefer workflow notes anchored on analyst leverage such as:
   - signal-submission boundaries
   - cookie/storage truth surfaces
   - callback/redirect/handoff edges
   - first behavior-changing consumer requests
   - accepted-vs-rejected compare-runs at a concrete boundary
3. Keep strengthening the browser subtree as a set of real workflow archetypes rather than abstract anti-bot classes.
4. Look for similar gaps in the mobile/protected-runtime subtree where broad pages still need more scenario-backed workflow notes.

## 7. Concrete scenario notes or actionable tactics added this run
- Added a dedicated DataDome workflow centered on:
  - standard vs first-party JS-tag deployment classification
  - locating the decisive `/js/` signal-submission boundary
  - moving one layer earlier to the last structured signal object before packing
  - using `datadome`, `dd_testcookie`, `ddSession`, and `ddOriginalReferrer` as outward truth surfaces
  - tying challenge/device-check/interstitial flow to the first later consumer request
- Added breakpoint/hook families for:
  - JS-tag/bootstrap edge
  - final `/js/` submission boundary
  - one-layer-earlier aggregation helper
  - cookie/storage state observation
  - first consumer request boundary
- Added explicit failure diagnosis for:
  - over-trusting visible `datadome` cookie presence
  - staring at the visible slider/interstitial while missing the earlier signal-submission edge
  - accepted and challenged runs both showing `datadome` but diverging later
  - instrumentation causing timing/trust distortion
  - minimal harness reproducing request shape but not accepted behavior

## 8. Sync / preservation status
- Local KB progress was preserved in:
  - `topics/datadome-cookie-challenge-workflow-note.md`
  - `sources/browser-runtime/2026-03-15-datadome-cookie-challenge-workflow-notes.md`
  - browser navigation updates
  - this run report
- Next operational steps after writing this report:
  - commit workspace changes
  - run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
  - if sync fails, record the failure while preserving local KB state
