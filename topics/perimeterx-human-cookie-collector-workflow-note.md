# PerimeterX / HUMAN Cookie-Collector Workflow Note

Topic class: concrete target-family workflow note
Ontology layers: browser-runtime subdomain, anti-bot cookie/state workflow, request-boundary methodology
Maturity: structured-practical
Related pages:
- topics/browser-side-risk-control-and-captcha-workflows.md
- topics/browser-request-finalization-backtrace-workflow-note.md
- topics/browser-parameter-path-localization-workflow-note.md
- topics/akamai-sensor-submission-and-cookie-validation-workflow-note.md
- topics/reese84-and-utmvc-workflow-note.md
- topics/acw-sc-v2-cookie-bootstrap-and-consumer-path-note.md
- topics/browser-environment-reconstruction.md
- topics/environment-differential-diagnosis-workflow-note.md

## 1. Why this page exists
This page exists because the browser KB needed another **concrete anti-bot family workflow note**, not another generic taxonomy page.

A recurring PerimeterX / HUMAN target shape is visible across official deployment docs and public practitioner material:
- a browser-side sensor/client script is loaded
- short-lived and long-lived `_px*` state appears in cookies or storage
- collector / verification routes run in third-party or first-party mode
- challenge or block flows hand state back into host-page logic
- one later request stops being blocked only when the right cookie/state family is accepted

The useful analyst question is usually not:
- what abstract anti-bot category is this?

It is:
- which script or route initializes the PX/HUMAN path?
- where do `_px3`, `_pxvid`, `pxcts`, or `_pxhd` become relevant?
- which collector/XHR boundary updates accepted state?
- where does the challenge-success handoff re-enter host-page logic?
- which first later application request actually benefits from the state transition?

This page is therefore a practical workflow note centered on:

```text
sensor/client script
  -> collector / XHR submission
  -> cookie or state update
  -> challenge-success handoff if present
  -> first behavior-changing consumer request
```

## 2. Target pattern / scenario
A representative target shape looks like this:

```text
page bootstrap
  -> PX/HUMAN client script loads (3rd-party or first-party route)
  -> browser collects signals / state and calls collector path
  -> `_px*` cookie/storage family is created or refreshed
  -> challenge / ABR flow may run if risk is high
  -> later app/API request is allowed, challenged less, or changes response shape
```

Representative browser-visible artifacts include:
- routes such as `/<app-id-without-PX-prefix>/init.js` and `/<app-id-without-PX-prefix>/xhr/*` in first-party mode
- cookie/storage family such as `_px`, `_px2`, `_px3`, `_pxvid`, `pxcts`, `_pxhd`, and `_pxff_*`
- challenge or custom block flow boundaries such as `blockScript` and `_pxOnCaptchaSuccess`

Common analyst situations:
- `_px3` or `_pxvid` appears, but the protected application request still fails under replay
- an interactive “press/hold” or challenge flow is visible, but the analyst cannot identify the first successful post-challenge consumer request
- first-party collector routes exist, but it is unclear whether the real analytical boundary is cookie update, callback handoff, or later application request
- a request seems accepted only in a real browser session, and the analyst needs to distinguish cookie-state success from broader environment/trust success

## 3. Analyst goal
The goal is not merely to “get the cookie.”
The goal is to recover the **collector-to-consumer path**:

```text
sensor/client bootstrap
  -> collector submission boundary
  -> cookie/storage update boundary
  -> challenge callback or block-page handoff (if present)
  -> first application request whose server behavior changes materially
```

A good output from this workflow looks like:

```text
first-party init.js bootstraps HUMAN client
  -> collector POST on /<app>/xhr/ refreshes short-lived `_px3` state and uses `_pxvid`
  -> challenge success triggers host-page callback
  -> next GET /api/listing stops returning hold/challenge behavior
  -> replay fails when collector state refresh is stale, even though `_pxvid` is still visible
```

That is more useful than either:
- a loose statement that “PX uses cookies,” or
- a brittle one-off cookie capture with no consumer map

## 4. Concrete workflow

### Step 1: identify the deployment edge
Start by deciding which deployment surface you are actually looking at:
- third-party client/script path
- first-party `init.js` + `xhr/*` collector routes
- challenge/block-page or ABR JSON flow

Record:
- the script URL or route family
- whether the page embeds an app/site identifier
- whether first-party routes sit under the protected site origin
- whether challenge/block behavior appears immediately or only after a later request

Useful note format:

```text
deployment surface:
  first-party collector mode
script/bootstrap:
  /<appid>/init.js
collector:
  /<appid>/xhr/
challenge:
  only on elevated-risk path
```

### Step 2: map the cookie/storage family, but do not stop there
Record when these change:
- `_px`, `_px2`, `_px3`
- `_pxvid`
- `pxcts`
- `_pxhd`
- relevant local/session storage keys if present

For each state element, record:
- when it first appears
- whether it rotates often or stays long-lived
- whether it appears before or after collector activity
- whether it changes after challenge success

Why this matters:
- the state family tells you **which transitions to compare**
- but visible presence of `_px3` or `_pxvid` is not enough to prove the workflow is solved

### Step 3: localize the collector submission boundary
This is usually the most useful first practical hook.
Look for:
- first-party `/<app>/xhr/*`
- third-party collector calls
- challenge solve or risk verification POSTs
- custom block / ABR fetches returning challenge parameters

At this boundary, inspect:
- request role and endpoint
- associated cookie state before and after the request
- whether request counters, UUID/session identifiers, or challenge identifiers travel with the request
- whether response side effects update cookies, local state, or host-page flow flags

This boundary is often more informative than deep early deobfuscation.

### Step 4: find the first behavior-changing consumer request
After the collector or challenge-success edge, identify the **first later request whose server behavior changes materially**.
Examples:
- page data starts returning instead of hold/challenge
- checkout/login/add-to-cart path stops hard-blocking
- API response body class changes from blocked to normal
- retry path disappears after successful state refresh

Record:
- endpoint and method
- whether the request itself carries any explicit PX/HUMAN fields or only cookies/session state
- whether the request works with old visible cookies but fails without a fresh collector transition

A common trap is to stop at cookie update and never identify the real consumer request.

### Step 5: challenge/ABR case — trace the host-page handoff
If the target uses challenge pages or Advanced Blocking Response, trace:

```text
challenge JSON / blockScript / iframe or page event
  -> host-page callback such as `_pxOnCaptchaSuccess`
  -> cookie or state refresh
  -> next consumer request
```

Useful questions:
- does the challenge success callback trigger a new collector request?
- does the host page issue the next application request directly or merely unlock UI state?
- which request actually proves the challenge-success path worked?

### Step 6: compare accepted and failed runs at the collector-to-consumer boundary
Compare at least:
- no-cookie vs fresh-cookie run
- expired-cookie vs refreshed-cookie run
- baseline browser run vs replayed request-only run
- challenge-solved vs challenge-unsolved path
- light observation vs heavier instrumentation

Ask:
- did the collector request differ?
- did the cookie family differ only in freshness/rotation, not presence?
- did the first consumer request stay structurally identical but receive different server treatment?
- is the drift execution-related, trust-related, session-related, or observation-related?

## 5. Where to place breakpoints / hooks

### A. Sensor / bootstrap script load edge
Use when:
- you need to identify app/site id and route family quickly
- you are not yet sure whether the deployment is first-party or third-party

Inspect:
- script URL and load order
- any app-id-like values or config blobs
- whether the script prepares first-party `init.js` / `xhr/*` style routes

### B. Collector / XHR submission boundary
Use when:
- cookie/state is visible but the actual refresh/verification step is unclear
- you need the fastest path to accepted-vs-failed compare-runs

Inspect:
- final request contract
- request counter / UUID-like arguments
- cookie state before and after submission
- whether response handling updates page flags or challenge state

Representative sketch:
```javascript
// sketch only
const origFetch = window.fetch;
window.fetch = async function(input, init) {
  if (String(input).includes('/xhr/') || String(input).includes('perimeterx')) {
    console.log('px-collector-boundary', { input, init, cookie: document.cookie });
    debugger;
  }
  return origFetch.apply(this, arguments);
};
```

### C. Cookie/state update observation
Use when:
- `_px3`, `_pxvid`, `pxcts`, or `_pxhd` appear to drive later success
- you need to know whether a visible cookie is fresh, stale, or merely diagnostic

Inspect:
- write timing relative to collector/challenge requests
- whether state is updated after challenge success
- whether the same visible cookie name persists while underlying server acceptance changes

### D. Challenge-success callback or host-page handoff
Use when:
- interactive challenge or ABR JSON flow is present
- you need to connect challenge completion to later application traffic

Inspect:
- `_pxOnCaptchaSuccess`-style callback edges
- message/callback payloads passed into host-page code
- whether callback success directly triggers a consumer request or only unlocks UI state

### E. First behavior-changing consumer request
Use when:
- collector and cookie logic are already visible
- you still do not know which application request actually depends on accepted state

Inspect:
- final request contract
- server response class on accepted vs failed runs
- whether the request consumes only cookies or also hidden/session fields established upstream

## 6. Representative code / pseudocode / harness fragments

### Collector-to-consumer recording template
```text
bootstrap:
  /<appid>/init.js

collector boundary:
  POST /<appid>/xhr/
  before cookies: _pxvid present, _px3 old
  after cookies: _px3 refreshed

challenge handoff:
  _pxOnCaptchaSuccess(true)

first consumer request:
  GET /api/listings
  accepted only after fresh collector transition
```

### State-family scratch schema
```python
# sketch only
class PxState:
    px3 = None
    pxvid = None
    pxhd = None
    pxcts = None

class BoundaryObservation:
    bootstrap_url = None
    collector_url = None
    consumer_url = None
    before_state = None
    after_state = None
```

### Compare-run checklist
```text
run A: baseline browser
  collector reached? yes
  cookie refresh? yes
  consumer accepted? yes

run B: replayed request with visible old cookies
  collector reached? no
  cookie refresh? no
  consumer accepted? no
```

The important thing is to preserve the **boundary sequence**, not just raw cookie strings.

## 7. Likely failure modes

### Failure mode 1: analyst stops at `_px3` or `_pxvid` visibility
Likely cause:
- cookie-presence thinking
- no identified collector or consumer boundary

Next move:
- localize the collector request and the first later consumer request
- compare freshness/rotation, not only cookie names

### Failure mode 2: challenge solved, but protected app request still fails
Likely cause:
- host-page handoff not understood
- challenge callback succeeded but required refresh/consumer request did not happen
- stale collector state after visible challenge success

Next move:
- trace callback/message edge into host-page logic
- identify the first request that should benefit from challenge success

### Failure mode 3: replay copies cookies but still gets blocked
Likely cause:
- collector step omitted
- risk cookie expired or was never refreshed under current session
- broader trust/environment drift remains

Next move:
- compare baseline vs replay at the collector boundary
- classify the drift before adding more environment patches

### Failure mode 4: analyst deobfuscates huge script before identifying route family
Likely cause:
- VM/obfuscation pressure hijacked the workflow
- no concrete bootstrap/collector anchor was chosen

Next move:
- return to `init.js`, `xhr/*`, challenge JSON, or the first consumer request
- map boundary sequence first

### Failure mode 5: same consumer request shape, different server result
Likely cause:
- cookie freshness difference
- hidden session/UUID/counter drift from collector path
- trust reclassification rather than request-shape drift

Next move:
- compare accepted and failed runs with cookie writes and collector responses included
- do not overfocus on the visible request shape alone

## 8. Environment assumptions
This family often needs a realistic browser session long enough to:
- load the client/bootstrap script
- complete at least one collector transition
- preserve cookie/storage state
- reach the first consumer request

A good default assumption is:
- use browser-native observation first
- delay aggressive environment reconstruction until the collector-to-consumer path is clear
- treat cookie freshness and challenge-success sequencing as first-class variables

## 9. What to verify next
Once the collector-to-consumer path is localized, verify:
- whether the deployment is truly first-party or only appears so at the edge
- whether challenge completion directly refreshes cookies or only toggles local state
- which cookie/storage fields are long-lived identifiers versus short-lived acceptance state
- whether a minimal harness can reproduce one collector transition before attempting full consumer replay
- whether the real blocker is cookie/state freshness, host-page handoff, or broader trust/environment drift

## 10. What this page adds to the KB
This page adds a missing practical anti-bot family entry in the browser subtree:
- a concrete workflow centered on cookie/state family plus collector boundary
- explicit connection between challenge-success handoff and later consumer request
- compare-run discipline focused on freshness, sequencing, and first behavior-changing request
- a target-family page that sits cleanly beside Akamai, Reese84/`___utmvc`, `acw_sc__v2`, ByteDance, Turnstile, Arkose, and hCaptcha notes

That is more useful for the current KB direction than another abstract anti-bot overview page.

## 11. Source footprint / evidence note
Grounding for this page comes from:
- `sources/browser-runtime/2026-03-15-perimeterx-human-cookie-collector-notes.md`
- official HUMAN documentation on:
  - cookie and storage names (`_px`, `_px2`, `_px3`, `_pxvid`, `pxcts`, `_pxhd`, `_pxff_*`)
  - first-party routes (`/<app>/init.js`, `/<app>/xhr/*`)
  - challenge/ABR boundaries and `_pxOnCaptchaSuccess`
- public practitioner repositories around PerimeterX reverse/solver work, used conservatively for workflow-shape evidence rather than universal field semantics

This page intentionally avoids overclaiming exact internals for every version or deployment.

## 12. Topic summary
PerimeterX / HUMAN browser analysis is often best approached as a collector-to-consumer workflow problem:

```text
bootstrap script
  -> collector request
  -> cookie/state refresh
  -> challenge-success handoff if present
  -> first application request whose server behavior changes
```

It matters because analysts often stop at visible `_px*` cookies or challenge pages, while the more useful answer is: this is the bootstrap route, this collector transition refreshes the meaningful state, this callback hands success back to the app, and this is the first request where accepted vs blocked behavior actually diverges.
