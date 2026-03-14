# PerimeterX / HUMAN browser cookie and collector workflow notes

Date: 2026-03-15
Topic: browser-runtime practical source notes
Focus: PerimeterX / HUMAN Security browser workflow around sensor script load, `_px*` cookie family, first-party collector routes, challenge/ABR flow, and request-side validation boundaries

## Source set consulted

### Existing KB pages
- `topics/browser-side-risk-control-and-captcha-workflows.md`
- `topics/browser-request-finalization-backtrace-workflow-note.md`
- `topics/browser-parameter-path-localization-workflow-note.md`
- `topics/akamai-sensor-submission-and-cookie-validation-workflow-note.md`
- `topics/reese84-and-utmvc-workflow-note.md`
- `topics/acw-sc-v2-cookie-bootstrap-and-consumer-path-note.md`

### Search-layer result cluster
Queries:
- `PerimeterX Human Security browser token workflow reverse engineering`
- `PerimeterX _px3 _pxvid cookie request workflow`
- `Imperva bot management browser cookie sensor workflow`

High-signal results used:
- `https://github.com/Pr0t0ns/PerimeterX-Reverse`
- `https://github.com/Pr0t0ns/PerimeterX-Solver`
- `https://docs.humansecurity.com/applications/nginx-lua-configuration-options`
- `https://docs.humansecurity.com/applications/use-of-cookies-web-storage`
- search hit/snippet for `perimeterx-nginx-plugin/README.md`

## Practical facts extracted

### 1. Browser-visible cookie family is an analyst entry surface, not the whole answer
The HUMAN cookie/storage documentation gives a concrete browser-facing state family:
- `_px`, `_px2`, `_px3` for short-lived session/risk state
- `_pxvid` as a long-lived visitor identifier
- `pxcts` as cross-tab session state
- `_pxhd` as server-side detection related state
- various `_pxff_*` feature-flag cookies

Analyst implication:
- seeing `_px3` or `_pxvid` appear is useful, but does not by itself explain which later request actually consumes the accepted state
- cookie observation should be paired with request-boundary tracing and accepted-vs-failed compare-runs

### 2. First-party deployments expose a concrete route family worth tracing
The HUMAN NGINX/Lua docs describe first-party mode with routes like:
- `/<APPID-without-PX-prefix>/init.js`
- `/<APPID-without-PX-prefix>/xhr/*`

The docs also show proxying to a collector host and forwarding `pxvid` into the collector path.

Analyst implication:
- a practical family entry is often:
  1. identify sensor/client script load (`init.js` or equivalent)
  2. identify collector/XHR submission route
  3. correlate cookie updates and challenge state around that route
  4. find the first later application request whose server behavior changes because the cookie/risk state changed

### 3. Collector verification can be triggered when a risk cookie is absent/expired/invalid
The configuration docs explicitly say the API is called when a risk cookie does not exist, is expired, or is invalid.

Analyst implication:
- useful compare-runs include:
  - no-cookie / expired-cookie / fresh-cookie
  - first navigation vs repeat navigation
  - light instrumentation vs heavy instrumentation
- the key diagnosis question is often not “what is the cookie format?” but “which collector or verification path is invoked when the state is considered unusable?”

### 4. Challenge flows and ABR JSON expose host-page handoff boundaries
The docs for Advanced Blocking Response describe JSON fields like:
- `appId`
- `jsClientSrc`
- `firstPartyEnabled`
- `vid`
- `uuid`
- `hostUrl`
- `blockScript`

They also mention `_pxOnCaptchaSuccess` as a host-page callback edge.

Analyst implication:
- for interactive challenge cases, a practical path is:
  challenge bootstrap JSON / block script
    -> host-page callback or message edge
    -> cookie or state update
    -> next application request that stops being blocked
- this creates a clean bridge between challenge-page analysis and later application request analysis

### 5. Practitioner repos reinforce a collector/payload/cookie framing
The public reverse/solver repos are uneven in quality and should not be treated as authoritative truth, but they still reinforce a recurring practical framing:
- locate the loaded PX challenge/client script
- identify payload fields sent to the solve/collector path
- treat values such as app/site id, sequence/request counters, visitor/session identifiers, and cookie-bound state as a family rather than a single parameter

Conservative analyst takeaway:
- for KB purposes, these repos are more useful as evidence for workflow shape than for exact field semantics
- the repeatable workflow is still strong enough to justify a concrete note centered on:
  sensor script -> collector submission -> cookie/state update -> first behavior-changing consumer request

## Resulting synthesis for KB integration
A dedicated practical workflow page is justified for PerimeterX / HUMAN because the source cluster supports a specific analyst entry pattern:
- cookie family visible (`_px3`, `_pxvid`, `pxcts`, `_pxhd`)
- collector/first-party routes identifiable
- challenge/ABR host-page handoff boundaries available
- public reverse material suggests payload-family and counter/state coupling

The page should stay conservative and workflow-centered, not claim universal field semantics for all versions or deployments.

## Provenance / caution
- Official vendor docs are strong for deployment shape, cookie/storage names, first-party collector routing, and ABR callback boundaries.
- Public reversing repos are helpful for target-family workflow hints, but field-level claims should be treated as version-specific and potentially noisy.
- This source cluster is strong enough for a practical workflow note, but not for overconfident universal claims about every PX/HUMAN deployment.
