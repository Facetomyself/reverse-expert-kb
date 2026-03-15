# Akamai Sensor Submission and Cookie Validation Workflow Note

Topic class: concrete target-family workflow note
Ontology layers: browser-runtime subdomain, anti-bot workflow, request-boundary methodology
Maturity: structured-practical
Related pages:
- topics/browser-side-risk-control-and-captcha-workflows.md
- topics/browser-fingerprint-and-state-dependent-token-generation.md
- topics/browser-request-finalization-backtrace-workflow-note.md
- topics/browser-parameter-path-localization-workflow-note.md
- topics/browser-environment-reconstruction.md
- topics/browser-debugger-detection-and-countermeasures.md
- topics/datadome-geetest-kasada-workflow-note.md

## 1. Why this page exists
This page exists because the browser KB already had several concrete workflow notes for other anti-bot families, but it still lacked a dedicated practical entry page for a very common Akamai-shaped problem:

```text
browser script collects signals
  -> sensor payload is assembled
  -> sensor request is submitted
  -> server updates validation cookies
  -> later protected requests are judged in that state context
```

That is a more useful analyst frame than either:
- a generic taxonomy page about browser anti-bot systems, or
- a vague claim that “Akamai uses fingerprinting and cookies.”

The practical need is usually to answer:
- where is the sensor submission boundary?
- what object still contains the structured preimage before packing?
- when and why do `_abck` or `bm_sz` change?
- which later request actually consumes the validated state in a way that matters?
- why does copied cookie state fail even when the visible values look plausible?

This page is therefore a **workflow note for target-family analysis**, not a vendor overview.

## 2. Target pattern / scenario
A representative Akamai Bot Manager family workflow looks like:

```text
page load / protected navigation
  -> Akamai sensor script loads
  -> runtime decode / wrapper setup
  -> browser / device / timing / behavior / JS-environment signals are collected
  -> sensor payload is assembled
  -> POST submission to verification endpoint
  -> server accepts / rejects and updates `_abck` and related cookie state
  -> later protected requests carry cookie state and are evaluated in that context
```

Representative browser-visible signs can include:
- a large obfuscated browser-side script or sensor bundle
- verification or challenge POST traffic before the decisive protected request
- cookie state including `_abck` and `bm_sz`
- retries or request outcomes that change after a cookie refresh edge
- suspicious drift when debugging, replaying requests, or changing browser baseline

Common analyst situations:
- `_abck` appears in storage, but the target is still blocked or unstable
- a protected request succeeds in-browser yet fails when copied into a script
- the sensor script is huge, and the analyst needs a bounded first anchor instead of full deobfuscation
- visible cookies look consistent across runs, but server treatment still diverges

## 3. Analyst goal
The goal is not “understand every obfuscated function.”
The goal is to recover a bounded path such as:

```text
sensor script load
  -> signal collection object
  -> sensor payload assembly helper
  -> verification POST boundary
  -> `_abck` / `bm_sz` update
  -> first consumer request whose outcome materially changes
```

A useful result from this workflow looks like:

```text
Akamai verification POST is sent before GET /api/search
  -> one frame earlier, helper packs timing + browser-state + signal object into sensor payload
  -> successful run updates `_abck`
  -> first accepted consumer request happens only after that update
  -> copied `_abck` without the fresh browser-side path still fails or degrades
```

That is much more operationally useful than “Akamai fingerprinting is sophisticated.”

## 4. The first five questions to answer
Before deep cleanup or environment cloning, answer these:

1. **Which exact request is the sensor submission boundary?**
2. **Which request is the first protected consumer whose outcome changes after cookie validation?**
3. **Where are `_abck` and `bm_sz` written or refreshed, and by what preceding event?**
4. **At what layer are the meaningful inputs still structured rather than already encoded?**
5. **Does the first divergence appear in local execution, cookie update timing, browser state, or later request consumption?**

These questions keep the case anchored to leverage instead of code volume.

## 5. Concrete workflow

### Step 1: identify the verification POST and the first consumer request
Start from the network timeline.
Do not start by trying to beautify the entire Akamai script.

Record:
- the verification or challenge POST candidate
- whether it precedes `_abck` updates
- the first later request whose server behavior changes materially
- whether `bm_sz`, `_abck`, or sibling state changes between cold and warm runs

Useful scratch table:

```text
run A:
  page load
  sensor POST occurs
  `_abck` updated
  GET /api/search accepted

run B:
  copied cookies only
  no fresh sensor POST
  GET /api/search blocked or downgraded
```

This immediately tells you whether the real workflow is:
- cookie-anchored
- request-sequence-anchored
- freshness-anchored
- browser-state-anchored

### Step 2: hook the sensor submission boundary
This is usually the highest-yield first breakpoint family.
The strongest anchor is often not the whole script, but the moment the large signal set becomes one outgoing payload.

High-yield surfaces:
- custom request wrapper around the verification POST
- final `fetch` / XHR boundary for the sensor request
- serializer that produces the packed sensor body
- helper that gathers or merges browser-state / timing / signal objects right before encoding

Representative sketch:

```javascript
// sketch only
const origFetch = window.fetch;
window.fetch = async function(input, init) {
  const url = String(input);
  if (url.includes('/_sec/') || url.includes('challenge') || url.includes('verify')) {
    console.log('akamai-sensor-post', { input, init });
    debugger;
  }
  return origFetch.apply(this, arguments);
};
```

The exact endpoint varies by target and deployment.
The important point is to trap the **sensor submission edge**, not to assume one universal URL.

### Step 3: move one layer earlier into the structured preimage
Once the final POST boundary is known, step upward into the helper that still has structured state.

What you want to see before final packing:
- browser or device feature object
- timing and performance-derived values
- challenge/session counters or freshness state
- behavior or interaction summaries if the target uses them
- request-context or page-context data that becomes part of the payload

Recording template:

```text
verification POST:
  POST /...verify

one layer earlier:
  helper(signalState, browserState, timingState, pageCtx)

cookie effect:
  `_abck` changes after response
```

This one-layer-earlier helper is often the best leverage point for compare-runs and later bounded harness experiments.

### Step 4: trace `_abck` / `bm_sz` update semantics conservatively
Treat `_abck` and `bm_sz` as analyst-visible anchors, not magic success markers.

Important questions:
- which response or client path precedes the cookie update?
- does the cookie write happen directly in visible JS, indirectly by server response, or both?
- does `bm_sz` appear earlier than `_abck`, later than `_abck`, or as sibling support state?
- is the decisive later request accepted only after a fresh update, or merely when the cookie exists?

Practical rule:
**cookie presence is not equivalent to workflow completion.**
Analysts should verify:
- when the cookie changed,
- what request caused it,
- and which later request actually benefited.

### Step 5: compare accepted and blocked runs at the same boundaries
Use at least these comparisons:
- accepted browser-native run vs blocked replayed request
- fresh verification run vs stale-session run
- low-intrusion observation vs heavy debugging run
- same navigation path with and without the preceding verification edge

At each boundary ask:
- did the same sensor POST happen?
- did the structured preimage have the same shape?
- did `_abck` / `bm_sz` update at the same stage?
- where was the **first** divergence?

This prevents the common mistake of over-trusting the final cookie string.

## 6. Where to place breakpoints / hooks

### A. Sensor-script load edge
Use when:
- you are still orienting yourself in a noisy page
- you need to identify which script or bootstrap edge belongs to Akamai behavior

Inspect:
- script URL and load timing
- whether load immediately triggers collection or only sets wrappers
- any config object or deployment identifier exposed near bootstrap

### B. Sensor POST finalization boundary
Use when:
- you already suspect the verification request
- you need the fastest path to the payload builder

Inspect:
- request URL / method / body
- stack back into serializer or request helper
- whether the same helper is reused across retries

### C. One-layer-earlier payload assembly helper
Use when:
- the final payload is already too opaque
- you need the structured preimage for compare-runs

Inspect:
- browser-state object
- timing/performance object
- challenge/session/freshness state
- any last-minute counters, timestamps, or nonces

### D. Cookie update / consumer edge
Use when:
- cookies look right but later requests still fail
- you need to locate the first request that materially benefits from validation

Inspect:
- timing of `_abck` / `bm_sz` appearance or refresh
- first accepted or behavior-changing consumer request
- whether the consumer path also depends on broader browser or transport state

## 7. Representative code / pseudocode / harness fragments

### Boundary-recording schema
```python
# sketch only
class AkamaiBoundary:
    sensor_post = None
    payload_helper = None
    browser_state = None
    timing_state = None
    cookie_effect = None
    first_consumer_request = None
```

### Compare-run capture template
```text
run accepted:
  sensor POST observed
  payload helper reached
  `_abck` updated
  protected request accepted

run replayed:
  copied cookies only
  no fresh payload helper execution
  protected request blocked
```

### Minimal thought-model for externalization decisions
```text
browser/runtime state
  + timing / behavior / page context
  -> payload assembly helper
  -> sensor POST
  -> server validation
  -> cookie update
  -> later protected request outcome
```

The point is not to clone the full browser immediately.
The point is to decide whether the meaningful boundary can be isolated at all.

## 8. Likely failure modes

### Failure mode 1: analyst assumes `_abck` presence means success
Likely cause:
- cookie was treated as a final answer instead of one state transition in a larger workflow

Next move:
- verify which request caused the update and which consumer request actually changed behavior

### Failure mode 2: analyst tries to deobfuscate the full script before anchoring the POST
Likely cause:
- code volume hijacked the workflow

Next move:
- start from the verification request boundary and walk backward from there

### Failure mode 3: copied cookies look right, replay still fails
Likely cause:
- no fresh sensor execution
- missing browser-state or timing assumptions
- broader session or transport context still matters

Next move:
- compare browser-native accepted runs against replayed runs at the sensor POST and one-layer-earlier helper boundaries

### Failure mode 4: heavy debugging changes the outcome
Likely cause:
- timing-sensitive checks
- debugger-visible environment drift
- altered execution pacing or observation pressure

Next move:
- reduce intrusiveness
- prefer boundary hooks over long deep stepping
- compare low-intrusion and high-intrusion captures

### Failure mode 5: payload looks structurally similar, server result still differs
Likely cause:
- hidden upstream state not captured
- browser environment mismatch
- freshness or timing drift
- server-side treatment coupled to more than the visible cookies

Next move:
- locate the first divergence point rather than polishing the final payload string

## 9. Environment assumptions
This family often needs a browser-faithful path long enough to:
- load the correct sensor script
- collect the target’s expected runtime signals
- preserve timing and transient in-memory state
- reach the verification boundary without observation-induced distortion
- perform the later protected request in the same validated context

A good practical order is usually:
1. locate the verification POST and first consumer request
2. localize payload assembly and cookie update boundaries
3. compare accepted vs blocked runs there
4. only then decide how much environment rebuilding is necessary

That is usually better than trying to rebuild the entire browser upfront.

## 10. What to verify next
Once the path is localized, verify:
- whether one payload helper dominates all meaningful sensor POSTs or only one request family
- whether `_abck` and `bm_sz` move together or reflect different stages of the workflow on this target
- whether blocked runs first diverge at script load, payload assembly, cookie update, or later consumer request
- whether the next best move is quieter observation, structured preimage capture, or bounded environment reconstruction

## 11. What this page adds to the KB
This page adds a concrete Akamai family note organized around how analysts actually work:
- anchor on the sensor submission boundary
- move one layer earlier into the payload preimage
- treat `_abck` / `bm_sz` as state anchors rather than magic answers
- trace the first later request that materially benefits
- diagnose failures through compare-runs instead of over-trusting copied cookies

That is exactly the kind of practical, target-grounded material the KB needed more of.

## 12. Source footprint / evidence note
Grounding for this page comes mainly from:
- `sources/browser-runtime/2026-03-15-akamai-sensor-cookie-workflow-notes.md`
- `https://github.com/Edioff/akamai-analysis`
- `https://raw.githubusercontent.com/Edioff/akamai-analysis/main/README.md`
- supporting public discussion around `_abck` / `bm_sz` and Akamai Bot Manager workflow anchors

This page intentionally stays conservative:
- it does not claim one invariant endpoint or one universal meaning for every cookie across all deployments
- it focuses on recurring workflow boundaries and failure-diagnosis patterns
- it treats source material as family-level guidance, not exact deployment truth

## 13. Topic summary
Akamai browser-side analysis is often best approached as a validation workflow problem:

```text
sensor script load
  -> signal collection
  -> payload assembly
  -> verification POST
  -> cookie update
  -> later protected request outcome
```

It matters because analysts often stall at “I saw `_abck`” or “the page loads a huge script,” while the more useful answer is: this is the decisive submission edge, this helper assembled the payload here, this event updated the cookie state, and this is where accepted and blocked runs first diverged.
