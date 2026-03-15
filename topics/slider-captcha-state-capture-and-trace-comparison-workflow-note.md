# Slider / Canvas Challenge State-Capture and Trace-Comparison Workflow Note

Topic class: concrete workflow note
Ontology layers: browser-runtime subdomain, protected-interaction workflow, challenge-state and trace-analysis practice
Maturity: structured-practical
Related pages:
- topics/browser-side-risk-control-and-captcha-workflows.md
- topics/geetest-v4-w-parameter-and-validate-workflow-note.md
- topics/datadome-cookie-challenge-workflow-note.md
- topics/cloudflare-turnstile-widget-lifecycle-workflow-note.md
- topics/arkose-funcaptcha-session-and-iframe-workflow-note.md
- topics/browser-parameter-path-localization-workflow-note.md
- topics/browser-request-finalization-backtrace-workflow-note.md
- topics/browser-environment-reconstruction.md

## 1. Why this page exists
The KB already has several family-specific browser notes.
What it still lacked was a **cross-family but still concrete** workflow page for a common real-world situation:
- a site/app uses a slider, canvas, or image-backed challenge
- the analyst can see the visible challenge, but the useful leverage is hidden in state transitions, movement traces, answer assembly, and final redemption

This page exists to cover that practical gap.

The wrong move here would be creating another generic anti-bot taxonomy page.
The useful move is to describe how analysts actually approach this class of target:
- where challenge execution begins
- where puzzle assets and metadata appear
- where trajectory / answer state is still structured
- where the path becomes packed or encrypted
- where challenge success is redeemed and can still fail

## 2. Target pattern / scenario
A representative slider/canvas workflow often looks like:

```text
page or app triggers challenge
  -> challenge assets / metadata fetched
  -> visible puzzle or drag UI appears
  -> local movement / answer trace assembled
  -> trace + challenge context packed / encrypted
  -> submit request sent
  -> token / validate object returned
  -> host page or backend redeems success
```

Representative signs include:
- canvas or SVG-backed puzzle rendering
- challenge image / background / cutout assets
- movement arrays or encoded drag traces
- submit payloads that contain one opaque field plus a few readable siblings
- a returned token or validate object that is consumed by a later request

Common analyst situations:
- the analyst can see the slider but does not know where the real challenge state starts
- the final request is visible, but its main payload is already packed or encrypted
- the challenge appears solved, but the page still fails later
- accepted and failed runs diverge, but the first divergence point is unclear

## 3. Analyst goal
The goal is not “fully understand this captcha family.”
The goal is to recover a bounded, usable path like:

```text
challenge trigger
  -> assets / metadata
  -> movement or answer object
  -> pack/encrypt boundary
  -> token/result object
  -> final redemption request
```

A useful output from this workflow looks like:

```text
challenge only starts after submit precheck
  -> assets fetched from challenge endpoint
  -> movement trace becomes structured in buildTrace(...)
  -> one helper packs trace + challenge context into an opaque blob
  -> submit returns token
  -> later backend verify rejects delayed redemption
```

That is more valuable than either:
- “I found the slider images,” or
- “I found one encrypted field.”

## 4. The first six questions to answer
Before broad deobfuscation or patching, answer these:

1. **What event actually starts the challenge?**
2. **Which requests fetch challenge assets or metadata?**
3. **Where is the movement / answer object last readable before packing?**
4. **Which request carries the packed challenge submission?**
5. **What object proves local challenge success: token, validate object, callback result, or cookie/state update?**
6. **Which later request actually redeems that success, and where do accepted and failed runs first diverge?**

These questions keep the workflow grounded.

## 5. Concrete workflow

### Step 1: find the real challenge-start edge
Do not equate “widget visible” with “challenge started.”
Find what actually begins the meaningful flow.

High-yield start edges:
- precheck request after username / email submit
- explicit `show` / `execute` / `run` call
- callback after form gating succeeds
- visible challenge rendered only after a server response classifies the session as risky

Why this matters:
- some targets have an earlier risk-classification layer before the visible puzzle
- challenge timing often explains why replay or capture attempts seem inconsistent

### Step 2: anchor challenge asset and metadata fetches
Once the start edge is known, identify the requests that fetch:
- background or sprite images
- puzzle cutout assets
- challenge IDs, salts, signatures, or session IDs
- variant / difficulty / mode indicators

What to record:
- endpoint and method
- whether the same request also seeds later submit fields
- whether accepted and failed runs fetch the same challenge class
- whether challenge type escalates after repeated failures

Representative run sketch:

```text
run A:
  precheck -> slider assets -> submit -> token -> redeem success

run B:
  precheck -> alternate challenge assets -> submit -> token absent -> retry
```

### Step 3: locate the last structured movement / answer object
This is often the most useful boundary in the whole workflow.

What to hunt for:
- movement arrays / `[x, y, t]` samples
- answer offsets / target positions
- structured trace builders
- objects that combine challenge metadata with movement or answer state
- helper right before serialization / encryption / flattening

Why this matters:
- once the trace is flattened into an opaque string, it is much harder to reason about
- the leverage point is usually one or two frames earlier, while the object is still readable

Representative thought model:

```text
movement samples + challenge context
  -> normalized trace object
  -> serializer / encrypt helper
  -> opaque submit payload
```

### Step 4: anchor the packed submit boundary
Once the structured object is known, find the request that carries it.

Record:
- endpoint and method
- packed field name / request body class
- readable sibling fields next to the packed blob
- whether the page receives a token, validate object, or immediate acceptance/rejection

This boundary helps answer whether your real problem is:
- wrong trace assembly
- wrong challenge context
- wrong encryption/packing path
- or a later redemption failure

### Step 5: separate local challenge success from final acceptance
A solved challenge is often not the same as an accepted business flow.

Useful outward truth surfaces:
- callback result object
- token string
- validate object
- cookie/state update
- challenge hidden / marked complete

Then ask:
- does a later request redeem this success?
- does that later request have stricter timing or session assumptions?
- does the app treat “challenge solved” and “request accepted” as separate phases?

### Step 6: compare accepted and failed runs at the same boundaries
Do not compare whole sessions vaguely.
Compare the same workflow edges:
- start edge
- asset / metadata fetch
- last readable movement / answer object
- packed submit request
- token/result object
- final redemption request

Useful compare axes:
- accepted vs failed attempt
- immediate submit vs delayed submit
- baseline environment vs modified environment
- light hooks vs heavy instrumentation
- first attempt vs retry / reset path

## 6. Where to place breakpoints / hooks

### A. Challenge-start edge
Use when:
- challenge timing is unclear
- there may be a hidden precheck before the visible UI

Inspect:
- who triggered challenge start
- whether risk classification or form gating came first
- whether alternate challenge modes appear under different conditions

### B. Asset / metadata fetch boundary
Use when:
- you need the earliest stable object tied to this challenge instance
- the visible UI is too late in the flow

Inspect:
- challenge IDs, salts, mode flags, image paths
- whether the same metadata later reappears in submit logic
- whether retries rotate or reuse challenge identifiers

### C. Trace / answer builder
Use when:
- the final request payload is too opaque
- you need the last readable movement or answer object

Inspect:
- raw movement samples
- normalization steps
- target offset / answer fields
- merge point between trace and challenge metadata

Representative sketch:
```javascript
// sketch only
function tap(label, value) {
  console.log(label, JSON.parse(JSON.stringify(value)));
  debugger;
  return value;
}
```

### D. Final serializer / encrypt helper
Use when:
- the trace builder is known and you need the exact boundary where structure is lost
- compare-runs suggest packing or encryption may be the first divergence

Inspect:
- packed field inputs
- call stack into request code
- whether retries alter only challenge context or also trace shape

### E. Token / validate / success callback boundary
Use when:
- you need the first stable proof of local success
- the app may later fail even after the challenge appears complete

Inspect:
- token / validate object shape
- whether it is consumed immediately or stored for later
- whether retries rotate this outward success object

### F. Final redemption request boundary
Use when:
- challenge completion is already visible
- the remaining unknown is why the business action still fails

Inspect:
- exact request carrying the success object
- timing relative to challenge completion
- whether the request adds additional session or app fields
- whether acceptance vs rejection diverges here rather than at challenge submit

## 7. Representative code / pseudocode / harness fragments

### Workflow scratch schema
```python
# sketch only
class SliderChallengeRun:
    start_edge = None
    asset_request = None
    challenge_metadata = None
    trace_object = None
    packed_submit = None
    success_object = None
    redeem_request = None
```

### Boundary-sequence recording template
```text
challenge start:
  submit click -> precheck ok -> slider shows

assets:
  GET /captcha/assets?id=...

trace object:
  buildTrace(samples, challengeCtx)

packed submit:
  POST /captcha/validate data=<opaque>

success object:
  token=...

redeem request:
  POST /login/finish
```

### Compare-run skeleton
```text
run A (accepted):
  same challenge class
  trace length 48
  token returned
  redeem request accepted

run B (failed):
  same challenge class
  trace length 48
  token returned
  redeem request rejected after delay
```

## 8. Likely failure modes

### Failure mode 1: analyst treats the case as only an image-position problem
Likely cause:
- challenge asset analysis was separated from trace assembly, packing, or redemption

Next move:
- reconnect assets to the trace builder and later submit/redeem boundaries

### Failure mode 2: analyst chases only the final encrypted field
Likely cause:
- the last readable movement / answer object one frame earlier was missed

Next move:
- move upward in the call chain until the trace or answer is still structured

### Failure mode 3: challenge appears solved, but the app still fails
Likely cause:
- token/result object is only an intermediate success surface
- final redemption request has tighter timing or session assumptions

Next move:
- compare immediate vs delayed redemption
- inspect the first request that consumes the success object

### Failure mode 4: accepted and failed runs look identical at the UI level
Likely cause:
- first divergence is in challenge class, hidden metadata, trace packing, or final redemption

Next move:
- compare bounded workflow edges instead of screenshots or whole HAR files alone

### Failure mode 5: heavy hooks make behavior less trustworthy
Likely cause:
- instrumentation changed timing or triggered anti-analysis

Next move:
- reduce intrusiveness
- prefer outward lifecycle boundaries first, then move inward carefully

## 9. Environment assumptions
Slider/canvas targets often depend on preserving:
- realistic challenge timing
- session continuity from challenge start through redemption
- browser or app environment features captured alongside interaction traces
- retry/reset behavior that may rotate challenge state

A good order is usually:
1. classify start edge and challenge class
2. capture assets / metadata
3. localize the last readable trace or answer object
4. anchor token/result and redemption boundaries
5. only then decide how much environment reconstruction or deeper deobfuscation is justified

## 10. What to verify next
Once the path is localized, verify:
- whether one trace builder dominates all attempts
- whether challenge retries rotate metadata or only refresh visible assets
- whether local success and final redemption always use the same object contract
- whether the first divergence across runs happens at trace assembly, packing, token issuance, or redemption
- whether the next best move is deeper builder tracing, quieter observation, or bounded environment reconstruction

## 11. What this page adds to the KB
This page adds a missing practical workflow layer between family-specific notes and broad browser captcha synthesis:
- how to approach slider/canvas challenges as a bounded state/trace/redeem workflow
- how to localize the last readable movement/answer object
- how to compare runs at the right lifecycle boundaries
- how to distinguish local challenge success from business-flow acceptance

That is exactly the kind of concrete, case-driven material the KB needed more of.

## 12. Source footprint / evidence note
Grounding for this page comes mainly from:
- `sources/browser-runtime/2026-03-15-slider-captcha-state-capture-and-trace-comparison-notes.md`
- official GeeTest overview material on challenge types, behavioral analysis, and environment detection
- readable practitioner/open-source signal around GeeTest v4 slide solving and partially deobfuscated workflows
- defender analysis of a custom Binance slider family showing a concrete trigger -> trace -> packed submit -> token -> final verify chain

This page intentionally stays conservative:
- it does not claim one invariant internal algorithm across slider families
- it focuses on recurring workflow boundaries, comparison strategy, and failure diagnosis
- it is a research/documentation page, not an exploitation recipe

## 13. Topic summary
Slider/canvas challenge analysis is often best approached as a workflow problem:

```text
start edge
  -> assets / metadata
  -> movement or answer object
  -> pack/encrypt boundary
  -> success object
  -> final redemption request
```

It matters because analysts often stall at either the visible puzzle or the final opaque payload, while the more useful answer is: this is when the challenge really starts, this is where the trace is still structured, this is where it becomes opaque, this is what local success looks like, and this is where accepted and failed runs first diverged.
