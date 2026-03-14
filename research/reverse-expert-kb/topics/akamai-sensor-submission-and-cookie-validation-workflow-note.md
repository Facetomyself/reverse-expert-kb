# Akamai Sensor Submission and Cookie-Validation Workflow Note

Topic class: concrete target-family workflow note
Ontology layers: browser-runtime subdomain, anti-bot sensor workflow, request-boundary methodology
Maturity: structured-practical
Related pages:
- topics/browser-side-risk-control-and-captcha-workflows.md
- topics/browser-request-finalization-backtrace-workflow-note.md
- topics/browser-parameter-path-localization-workflow-note.md
- topics/browser-fingerprint-and-state-dependent-token-generation.md
- topics/browser-environment-reconstruction.md
- topics/browser-debugger-detection-and-countermeasures.md
- topics/environment-differential-diagnosis-workflow-note.md
- topics/acw-sc-v2-cookie-bootstrap-and-consumer-path-note.md
- topics/reese84-and-utmvc-workflow-note.md

## 1. Why this page exists
This page exists because the browser subtree still had a practical gap.
It already covered:
- cookie-bootstrap cases like `acw_sc__v2`
- widget/session families like Turnstile, Arkose, and hCaptcha
- request-signature families like ByteDance web signatures
- generic request-boundary and parameter-path workflows

What it did **not** yet have was a dedicated workflow note for a recurring anti-bot family where the strongest analyst anchors are:
- sensor payload assembly
- verification POST submission
- `_abck` / `bm_sz` cookie lifecycle
- first accepted consumer-request tracing

That is a concrete, recurring workflow shape.
It is more useful to document directly than to create yet another abstract anti-bot taxonomy page.

## 2. Target pattern / scenario
### Representative target shape
A representative Akamai-family browser path looks like:

```text
page load / protected navigation
  -> obfuscated client script loads
  -> signal collection runs across browser/device/behavior/environment state
  -> sensor payload is assembled
  -> browser submits sensor/verification request
  -> server validates and updates `_abck` / related cookie state
  -> later protected requests either succeed, challenge again, or escalate
```

Common analyst situations:
- a protected site loads a large obfuscated sensor script and later sets `_abck`
- `_abck` is visible in storage, but later requests still fail or get challenged
- `bm_sz` and/or related cookie state appears, but it is unclear which request actually matters
- the script is huge, but the real leverage point is the sensor POST and subsequent cookie-consuming request
- instrumentation changes behavior enough that visible evidence becomes hard to trust

### Analyst goal
The practical goal is not “understand every function in the sensor bundle.”
It is one or more of:
- identify the exact sensor submission boundary
- localize the payload assembly path before it is fully packed
- identify where `_abck` or sibling cookie state is written/updated
- determine which later request actually benefits from that cookie state
- explain why apparently similar runs diverge despite seeing the same visible cookies

## 3. The first four questions to answer
Before broad deobfuscation, answer these:

1. **Which request is the sensor/verification submission?**
2. **What is the first request whose server behavior changes after `_abck` or related cookie state updates?**
3. **At what stage do meaningful inputs still remain structured rather than flattened into an opaque payload?**
4. **Is the divergence between runs first visible in local execution, cookie state, final request contract, or remote response?**

These four questions keep the case anchored to workflow boundaries instead of bundle size.

## 4. Concrete workflow

### Step 1: anchor the sensor submission request
Start from the network timeline.
You want the request that turns browser-side collection into a verification event.

Record:
- endpoint and method
- whether it appears on page load, redirect, retry, or challenge transition
- payload class: form, JSON, packed blob, query parameter, or hybrid
- whether the request is one-shot or repeated
- what cookies or state change immediately after the response

Useful scratch output:

```text
run A:
  script loads
  sensor POST fires
  response updates `_abck`
  next navigation accepted

run B:
  script loads
  sensor POST fires
  `_abck` visible
  next navigation still challenged
```

That already tells you that cookie presence alone may not explain success.

### Step 2: hook the final sensor payload assembly boundary
Do not start by fully cleaning the entire obfuscated script.
Start where the payload becomes final enough to inspect.

High-yield surfaces:
- custom request client / wrapper that submits the verification request
- `fetch` / XHR boundary if the payload is still interpretable there
- one layer earlier serializer/helper if final transport is already too opaque
- helper that joins many signal fragments into one packed value

What to inspect:
- call stack into payload assembly
- whether one helper collects many browser/environment signals together
- whether timing or event-derived values are inserted late
- whether the final transport boundary is already too flattened to explain drift

### Step 3: localize the `_abck` write/update path
Seeing `_abck` in DevTools is not enough.
Find the actual write/update path and its immediate producer.

Inspect:
- whether the cookie is set directly by response semantics, by client JS, or by both being observable at different layers
- whether `_abck` is written once or updated across multiple steps
- whether `bm_sz` or sibling cookie state changes at the same time
- whether local JS still consumes/update-checks this state before later requests

The key practical question is:

```text
what exact event turns visible sensor submission into later usable cookie state?
```

### Step 4: identify the first real consumer request
The first request after cookie update is not always the important one.
Find the first request whose server behavior materially changes.

Record:
- endpoint and method
- accepted vs challenged vs redirected outcome
- whether `_abck` alone appears sufficient
- what sibling dynamic fields, headers, or timing assumptions travel with it
- whether replay with “same cookie” still diverges

Representative artifact:

```text
sensor POST -> `_abck` updated
next image/asset requests irrelevant
first meaningful consumer = GET /protected/catalog
same `_abck` visible in failed replay, but request contract and outcome differ
```

### Step 5: compare accepted run vs challenged run at the same boundaries
Compare the same boundaries across runs:
- accepted baseline vs challenged run
- low-intrusion vs heavy-intrusion observation
- fresh session vs warm/retry session
- stable browser baseline vs altered browser/runtime baseline

At each boundary ask:
- did the same sensor submission fire?
- did the same cookie state update happen?
- did the same consumer request fire?
- where was the **first** divergence?

This keeps the analysis from collapsing into “I saw `_abck`, therefore the workflow is solved.”

## 5. Where to place breakpoints / hooks

### A. Final verification-request boundary
Use when:
- you already recognize the candidate sensor POST in the network log
- the bundle is too large to enter blindly

Inspect:
- final payload shape
- sibling headers/query fields
- call stack into the request builder

Representative sketch:
```javascript
// sketch only
const origFetch = window.fetch;
window.fetch = async function(input, init) {
  if (String(input).includes('verify') || String(input).includes('challenge')) {
    console.log('akamai-verify-request', { input, init });
    debugger;
  }
  return origFetch.apply(this, arguments);
};
```

### B. One-layer-earlier payload helper
Use when:
- the transport payload is already packed or unreadable
- you need the last structured preimage before packing

Inspect:
- aggregated signal object or array
- late-added timing/environment fields
- whether multiple modules feed one payload-builder helper

### C. Cookie state write/update observation
Use when:
- `_abck` / `bm_sz` are the clearest visible artifacts
- you need to know whether cookie state really changed or only appeared to

Inspect:
- exact update timing
- immediate call path or response boundary
- whether later code reads sibling cookie state locally

### D. First consumer request boundary
Use when:
- cookie update is visible but acceptance still unclear
- you suspect broader request-context or environment coupling

Inspect:
- full request contract
- whether sibling fields changed
- whether the request role or sequence changed between runs

## 6. Representative code / pseudocode / harness fragments

### Sensor-to-cookie boundary recording template
```text
script entry:
  akamai bundle loaded from ...

sensor request:
  POST /...verify...
  payload class: packed string/blob
  insertion boundary: buildSensorPayload() -> fetch()

cookie update:
  `_abck` updated after response
  sibling state: `bm_sz` also present

consumer request:
  GET /protected/page
  outcome: accepted in baseline, challenged in altered run
```

### Structured preimage capture sketch
```javascript
// sketch only
function tap(label, value) {
  console.log(label, JSON.parse(JSON.stringify(value)));
  debugger;
  return value;
}
```

### Minimal thought-model for externalization decisions
```python
# sketch only
class BrowserState:
    fingerprint = None
    timing = None
    event_state = None

class SensorSubmission:
    preimage = None
    packed_payload = None

class CookieState:
    abck = None
    bm_sz = None
```

The point is not to reproduce the whole site.
The point is to decide whether one verified path is separable at all.

## 7. Likely failure modes

### Failure mode 1: analyst sees `_abck` and assumes the case is solved
Likely causes:
- cookie visibility confused with accepted consumer-path understanding
- broader request contract still differs
- environment/session/trust drift still unresolved

Next move:
- compare the first behavior-changing consumer request, not just cookie storage

### Failure mode 2: analyst over-focuses on the giant obfuscated bundle
Likely causes:
- static cleanup started before request-boundary evidence was stabilized
- final payload and cookie boundaries were not used as anchors

Next move:
- return to sensor POST, cookie update, and first consumer request boundaries

### Failure mode 3: accepted and challenged runs both show `_abck`
Likely causes:
- stale or differently validated cookie state
- sibling cookie/request state drift
- environment or transport/TLS differences outside the visible JS payload
- observation pressure changed timing or path selection

Next move:
- compare first divergence point and downgrade confidence in cookie-only explanations

### Failure mode 4: instrumentation makes the workflow noisier or less trustworthy
Likely causes:
- timing traps
- prototype/global tamper checks
- observation distortion

Next move:
- reduce intrusiveness
- favor outward request/cookie boundaries over deep pervasive hooks
- compare minimal-hook vs heavy-hook runs explicitly

### Failure mode 5: minimal harness reproduces payload shape but not outcome
Likely causes:
- structured preimage still incomplete
- broader browser state or timing assumptions omitted
- transport / TLS / session context remains essential

Next move:
- return to accepted-vs-failed compare-runs before extending the harness

## 8. Environment assumptions
This family often requires a stronger browser-faithful environment than simple arithmetic token families.
But the right practical order is usually:
1. locate the decisive request and cookie boundaries
2. identify the minimum structured preimage
3. only then decide how much browser/runtime fidelity must be preserved

That is usually better than rebuilding a huge browser environment first.

## 9. What to verify next
Once the basic path is localized, verify:
- whether one payload helper dominates the verification submission
- whether `_abck` and `bm_sz` update together or on different edges
- whether the first accepted request is truly the key consumer request
- whether accepted and challenged runs differ first at payload assembly, cookie update, or later request consumption
- whether the next best move is deeper payload tracing, quieter observation, or bounded environment reconstruction

## 10. What this page adds to the KB
This page adds a concrete browser anti-bot family note organized around how analysts actually work:
- anchor the sensor POST
- inspect the last structured payload stage
- localize cookie updates
- trace the first consumer request
- compare accepted and challenged runs without over-trusting visible cookie state

That is exactly the kind of practical, target-grounded material the KB needed more of.

## 11. Source footprint / evidence note
Grounding for this page comes mainly from:
- `sources/browser-runtime/2026-03-15-akamai-sensor-cookie-workflow-notes.md`
- case-study-style GitHub material around Akamai Bot Manager workflow analysis
- public corroborating discussion around `_abck` / `bm_sz` as visible validation-state anchors
- existing KB pages on request-boundary tracing, browser environment reconstruction, and environment-differential diagnosis

This page intentionally stays conservative:
- it does not claim one invariant implementation across all Akamai deployments
- it focuses on recurring workflow boundaries and failure-diagnosis patterns instead of undocumented internals

## 12. Topic summary
Akamai sensor submission and cookie-validation analysis is a practical browser workflow where the real task is not merely reading a large obfuscated script, but tracing one verification request, one cookie-state transition, and one behavior-changing consumer request tightly enough to explain why a protected session is accepted, challenged, or drifts.

It matters because analysts often stop at “`_abck` exists,” while the more useful answer is “this verification request assembled the payload here, this boundary updated cookie state, this later request actually mattered, and this is where accepted and challenged runs first diverged.”