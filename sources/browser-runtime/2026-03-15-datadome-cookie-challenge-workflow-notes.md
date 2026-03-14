# Source Notes — DataDome cookie / challenge / JS-tag workflow

Date: 2026-03-15
Collector: OpenClaw autonomous KB maintenance run
Scope: gather practical, target-grounded material for a dedicated DataDome workflow note, with emphasis on browser-visible boundaries an analyst can actually use: JS-tag bootstrap, `/js/` signal submission, `datadome` cookie lifecycle, challenge/device-check handoff, and first protected consumer-request diagnosis.

## Sources consulted

### 1. DataDome JavaScript Tag docs
URL: https://docs.datadome.co/docs/javascript-tag
Type: official vendor documentation
Observed via: `web_fetch`

Key usable signals:
- JS tag exists to improve detection and to ensure blocked XHR/fetch requests can display response pages.
- JS tag requires read/write access to the `datadome` cookie; changing attributes like `HttpOnly` is explicitly discouraged.
- Tag collects behavioral data such as mouse movements and keystrokes, plus browser / OS / GPU / consistency-test information.
- Docs explicitly mention bot-oriented built-in consistency checks and detection pressure around headless/automation surfaces.
- Tag should be loaded early because it intercepts protected XHR/fetch requests, preserves session continuity, and supports response-page flow.
- Reverse-proxy / first-party deployment shape is documented clearly:
  - JS file from `/tags.js`
  - fingerprint endpoint from `/js/`
  - `Host` header must map to DataDome origin

Usefulness for KB:
- Strong official support for a workflow that starts from `tags.js` bootstrap and `/js/` submission boundaries instead of abstract “captcha analysis.”
- Justifies breakpoint placement around early tag load, fetch/XHR interception, and cookie/state writes.
- Supports the idea that challenge visibility alone is not the whole problem; the JS-tag / fingerprint / request-interception layer is part of the analyst object.

Reliability note:
- High reliability for lifecycle and deployment surfaces.
- Does not reveal internal payload semantics, so it is best used for workflow boundaries rather than algorithm claims.

---

### 2. DataDome cookies and stored-data docs
URL: https://docs.datadome.co/docs/cookie-session-storage
Type: official vendor documentation
Observed via: `web_fetch`

Key usable signals:
- `datadome` cookie is the main browser-visible session artifact used for both server-side and client-side legitimacy assessment.
- `dd_testcookie` is a transient test used by the JS tag to check whether cookies can be saved.
- `ddSession` is local-storage duplication of the `datadome` cookie when `sessionByHeader` is enabled.
- `ddOriginalReferrer` in session storage is used when Device Check or CAPTCHA is triggered, then restored later.
- Official docs explicitly warn that blocking, tampering with, or deleting these artifacts can cause issues / unexpected behavior.

Usefulness for KB:
- Gives a concrete state-family map analysts can actually compare during runs:
  - `datadome`
  - `dd_testcookie`
  - `ddSession`
  - `ddOriginalReferrer`
- Supports a practical distinction between:
  - visible cookie presence
  - cookie-write capability
  - session-header mode
  - challenge/interstitial handoff state
- Justifies using cookie/storage boundaries as truth surfaces, while avoiding over-trust in cookie presence alone.

Reliability note:
- High reliability for browser-visible state semantics.
- Limited for lower-level internal generation details.

---

### 3. DataDome Slider docs
URL: https://docs.datadome.co/docs/datadome-captcha
Type: official vendor documentation
Observed via: `web_fetch`

Key usable signals:
- Slider inspects technical and behavioral details, not just challenge-artifact interaction.
- Concrete signal categories mentioned:
  - screen / resolution / touch support
  - codecs / media extensions / plugins / browser checks
  - CPU / GPU
  - JS consistency challenges / rendering / execution time
  - mouse / touch / scrolling / keystroke / device movement dynamics
- Confirms the practical importance of browser-faithful execution and interaction-state comparison.

Usefulness for KB:
- Officially supports treating DataDome more like a browser sensor + challenge-transition workflow than a simple slider-artifact problem.
- Reinforces the need for compare-runs across browser baseline, interaction level, and observation pressure.

Reliability note:
- High reliability for family-shape and signal classes.
- High-level; not enough for exact payload semantics.

---

### 4. Existing practitioner cluster already curated in KB
Primary existing source:
- `sources/browser-runtime/2026-03-14-datadome-geetest-kasada-notes.md`

Key usable signals carried forward:
- `gravilk/datadome-documented` framed a practical network anchor around requests to `api-js.datadome.co/js/` and a `datadome` cookie update path.
- Older practitioner material highlighted environment and consistency checks such as screen/timing/renderer/plugins/timezone/webdriver-like checks.
- Existing cluster already distinguished DataDome from GeeTest and Kasada in a useful way:
  - DataDome more state / sensor / challenge-transition heavy
  - GeeTest more answer-object / pack / validate heavy
  - Kasada more request-role / token-attachment heavy

Usefulness for KB:
- Lets the dedicated DataDome page stay concrete and family-specific instead of recreating a broad three-family comparison.
- Supplies practical hints for where analysts can look one layer earlier than an opaque challenge request.

Reliability note:
- Version-sensitive and partly old.
- Best treated as workflow-shape evidence, not as a stable current implementation reference.

## Cross-source synthesis

### Stable practical workflow shape
A conservative, browser-visible DataDome workflow looks like:

```text
JS tag / first-party bootstrap
  -> `/js/` or equivalent signal submission
  -> `datadome` cookie / sibling state update
  -> device-check / slider / response-page handoff if risk escalates
  -> first later protected request whose server behavior changes materially
```

This is a better analyst object than either of these oversimplifications:
- “it is just a slider captcha”
- “it is just a cookie”

### High-value truth surfaces
The best recurring truth surfaces from the source set are:
- early `tags.js` / first-party bootstrap edge
- `/js/` signal-post boundary
- `datadome` cookie write/update observation
- `dd_testcookie` presence or absence when cookie capability is in question
- `ddSession` / `ddOriginalReferrer` when challenge/device-check handoff is involved
- first later application request whose treatment changes after the state transition

### Practical compare axes justified by the sources
Useful compare-runs should vary one axis at a time:
- baseline browser vs altered browser/automation surface
- no challenge escalation vs challenge/device-check path
- cookie-write-capable vs cookie-blocked context
- fresh collector transition vs stale visible cookie only
- light observation vs intrusive hooks/debugging

### Most important practical caution
The docs strongly imply that visible `datadome` cookie presence is necessary but not sufficient as an explanation.
The stronger question is:

```text
what exact bootstrap / submission / state-transition / handoff sequence caused the later request to be accepted or challenged?
```

## Candidate KB actions justified by this source cluster
- Create a dedicated `topics/datadome-cookie-challenge-workflow-note.md` page.
- Position it as a sibling to the dedicated Akamai, PerimeterX/HUMAN, GeeTest, Kasada, Turnstile, Arkose, and hCaptcha notes.
- Center the page on:
  - JS-tag bootstrap
  - `/js/` signal boundary
  - `datadome` / `dd*` state tracking
  - response-page / device-check / slider handoff
  - first behavior-changing consumer request
- Cross-link it from `index.md`, `topics/browser-runtime-subtree-guide.md`, and `topics/browser-side-risk-control-and-captcha-workflows.md`.

## Evidence limitations
- Public official docs are strong on lifecycle and state naming but intentionally weak on payload internals.
- Practitioner material is useful but version-sensitive.
- This is enough to justify a strong workflow page, but not to claim one invariant internal algorithm across deployments.
