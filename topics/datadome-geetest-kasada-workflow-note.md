# DataDome / GeeTest / Kasada Workflow Note

Topic class: concrete target-family workflow note
Ontology layers: browser-runtime subdomain, protected-interaction workflow, case-driven methodology
Maturity: structured-practical
Related pages:
- topics/browser-side-risk-control-and-captcha-workflows.md
- topics/browser-fingerprint-and-state-dependent-token-generation.md
- topics/browser-cdp-and-debugger-assisted-re.md
- topics/browser-environment-reconstruction.md
- topics/reese84-and-utmvc-workflow-note.md
- topics/cdp-guided-token-generation-analysis.md
- topics/protocol-state-and-message-recovery.md

## 1. Why this page exists
This page exists to stop the KB from collapsing very different browser protection families into one fuzzy label like "slider" or "captcha."

That abstraction is analytically expensive.
A DataDome-style challenge, a GeeTest-style slide flow, and a Kasada-style token family may all be discussed by practitioners in the same broad anti-bot bucket, but they often reward **different first moves**.

This page is intentionally practical.
It asks:
- what should the analyst anchor first?
- where should breakpoints or hooks go first?
- when is environment reconstruction central versus secondary?
- what kind of compare-run plan is worth doing?
- what failure mode usually means the analyst picked the wrong workflow?

## 2. Three target-family shapes

### A. DataDome-like shape
Typical practical shape:
- challenge/bootstrap request plus cookie/token state
- browser feature collection and consistency checks
- technical + behavioral signal collection
- challenge or slider state evolving across attempts
- strong dependence on real browser execution context

Representative signs:
- challenge endpoint or bootstrap request that returns or updates a protection cookie
- visible concern with browser/runtime integrity and behavior signals
- output that drifts when browser environment or interaction path changes

### B. GeeTest-like shape
Typical practical shape:
- visible image challenge is a central object rather than pure browser-state collection
- a few IDs / challenge parameters feed the flow
- encrypted validation request packaging matters
- image position solving / challenge artifact handling may matter more than environment emulation

Representative signs:
- challenge exposes image assets and coordinates/IDs that strongly structure the task
- browser fingerprint collection appears light or secondary
- the blocker is not "what browser state is missing?" so much as "how is the answer encoded/packed/validated?"

### C. Kasada-like shape
Typical practical shape:
- browser-side token family generation tied to request role
- fingerprint/state coupling and obfuscated/polymorphic wrappers
- difficult-to-port client token path despite seemingly simple request surface
- strong payoff from locating the pre-dispatch call path instead of staring at the final request

Representative signs:
- one or more token fields attached shortly before dispatch
- challenge may be silent or background rather than image-first
- main difficulty is locating the live browser-local input -> transform -> output chain

## 3. Analyst goal by family

### DataDome-like goal
Usually:
- identify the bootstrap/challenge request and resulting cookie/token update path
- determine which environment or interaction signals materially affect acceptance
- separate stable collection/format logic from changing wrapper/challenge transitions

### GeeTest-like goal
Usually:
- identify challenge parameters and image/position-solving path
- locate request packing / encryption path for validation submission
- determine whether browser-state reconstruction is actually needed or whether image/protocol analysis carries most of the load

### Kasada-like goal
Usually:
- anchor the exact request role carrying CT/CD-like fields
- locate the final attachment path and best paused call frame
- recover minimum token-generation contract before attempting a port or external harness

## 4. Concrete first-pass workflow

### Step 1: decide what the real object is
Before deobfuscating, ask which object is primary.

#### DataDome-like
Primary object is often:
- challenge bootstrap
- cookie/token refresh
- browser signal collection and challenge-transition state

#### GeeTest-like
Primary object is often:
- challenge artifact and answer encoding path
- validation request packing
- image corpus / offset / challenge-response structure

#### Kasada-like
Primary object is often:
- live token-generation path for one request role
- fingerprint/state input object
- pre-dispatch wrapper and callable contract

If you cannot answer this question yet, your next step is probably more network/timeline anchoring, not more code cleanup.

### Step 2: anchor one concrete network moment
For all three families, begin from one specific request or response transition.

Record:
- which request or response step first makes the protection logic visible
- where the interesting output lands: cookie, header, body field, query, or challenge payload
- whether the value appears on initial load, retry, or post-interaction
- whether sibling dynamic fields change at the same time

Compact comparison template:

```text
run A: cold load / first attempt
  step 1 -> challenge bootstrap
  step 2 -> token/cookie absent or initial
  step 3 -> validation request carries value V1

run B: retry / post-challenge
  step 2 -> cookie refreshed
  step 3 -> validation request carries value V2

run C: altered browser or altered challenge handling
  step 3 -> value malformed / missing / accepted differently
```

### Step 3: choose the right first breakpoint family

#### DataDome-like first breakpoints
Start with:
- challenge/bootstrap response handlers
- cookie write/update sites
- environment/signal collection sites immediately upstream of challenge submission
- final attachment point for the protection cookie or challenge payload

Why:
- the practical question is usually "which browser signals and state transitions feed the accepted cookie/challenge flow?"

#### GeeTest-like first breakpoints
Start with:
- challenge parameter extraction and image asset handling
- answer packing / encryption / validation-request construction
- the line where solved offset / challenge answer enters the encrypted payload

Why:
- heavy browser-environment tracing may be lower-yield than locating how the challenge answer becomes the submitted validation object

#### Kasada-like first breakpoints
Start with:
- request finalization wrapper
- header/body merge site right before dispatch
- callable token-generation frame above obfuscated helpers
- JS wrapper around any mixed JS/Wasm token path

Why:
- the practical question is often "what exact live function and input object produce this token for this request role?"

## 5. Where to place hooks and what to inspect

### DataDome-like: inspect stateful sensor assembly
High-yield observations:
- object holding browser feature collection results
- challenge bootstrap response fields
- cookie values before and after update
- whether timing, canvas, codecs, plugins, renderer, or interaction data are gathered before the challenge result is attached

Representative pseudocode sketch:

```javascript
// sketch only
const origFetch = window.fetch;
window.fetch = async (...args) => {
  const [url, init] = args;
  if (String(url).includes('/js/') || String(url).includes('captcha')) {
    console.log('challenge request', { url, init });
  }
  const resp = await origFetch(...args);
  return resp;
};
```

This kind of hook is not the final answer.
It is useful for proving where the workflow actually turns state into challenge traffic.

### GeeTest-like: inspect answer-to-payload conversion
High-yield observations:
- challenge IDs and challenge metadata
- image URLs / offsets / challenge instance IDs
- structured object holding the solved answer before encryption
- AES/RSA or other pack/encrypt boundary right before validation dispatch

Representative pseudocode sketch:

```javascript
// sketch only
function packValidation(answerObj, challengeCtx) {
  // inspect here before encryption destroys structure
  return encrypt(JSON.stringify({ answerObj, challengeCtx }));
}
```

The leverage point is usually the structured pre-encryption object, not the final ciphertext.

### Kasada-like: inspect pre-dispatch token contract
High-yield observations:
- request-role-specific token fields
- the immediate producer of CT/CD-like values
- lexical scope where token function plus helpers/constants coexist
- browser state/fingerprint object being passed downstream

Representative pseudocode sketch:

```text
on Debugger.paused:
  frame = chooseBestFrame(callFrames)
  evaluateOnCallFrame(frame, "candidateTokenFn(requestCtx, stateObj)")
```

The leverage point is usually the paused live frame where the page is still the best harness.

## 6. Compare-run methodology by family

### DataDome-like compare axes
Change one axis at a time:
- cold load vs warm challenge state
- no interaction vs minimal interaction
- baseline browser vs altered browser features
- clean browser state vs partially missing state

What you want to learn:
- which browser and challenge-state assumptions materially affect cookie or token acceptance

### GeeTest-like compare axes
Change one axis at a time:
- different challenge instances with same solving method
- same answer path before and after altering image-artifact handling
- identical answer with changed packaging/encryption path
- browser baseline changes only after the answer path is already stable

What you want to learn:
- whether failures come from image/offset solving, from validation packing, or from hidden state you have not yet modeled

### Kasada-like compare axes
Change one axis at a time:
- same request role across retries
- same request role across browser-state changes
- identical input payload with different session/challenge state
- in-browser call-frame invocation vs partial external harness call

What you want to learn:
- whether the token drift comes from state wrapper changes, helper drift, or an actually changing transform contract

## 7. Externalization decision rules

### DataDome-like
Do not externalize early if:
- accepted behavior still depends on challenge transitions or browser behavior signals
- you cannot name which collected signals are actually required
- cookie refresh logic is still response-driven and poorly understood

Externalize only when:
- the minimal signal set and state transitions are bounded enough to test cleanly

### GeeTest-like
Do not externalize early if:
- you still do not know whether the dominant blocker is image solving or request packing
- the structured pre-encryption answer object is still unclear

Externalize once:
- the challenge-answer object and validation packing boundary are clear enough to test independently

### Kasada-like
Do not externalize early if:
- your best artifact is still "this token only works when I pause at a magical browser frame"
- request-role prerequisites and helper scope are still unstable

Externalize once:
- the callable contract is stable across repeated runs
- minimum required browser/session state is enumerable

## 8. Likely failure modes and what they usually mean

### Failure mode 1: analyst applies environment-heavy workflow to a GeeTest-like case too early
Likely meaning:
- the real blocker is challenge-artifact solving or validation packing, not browser-state reconstruction

Next move:
- move upstream to the structured answer object and pre-encryption packing boundary

### Failure mode 2: analyst treats DataDome-like case as pure image/captcha problem
Likely meaning:
- browser sensor and challenge-state logic are being under-modeled

Next move:
- inspect bootstrap/challenge response handling, cookie refresh, and browser signal collection order

### Failure mode 3: analyst keeps prettifying obfuscated Kasada-like code without anchoring one request role
Likely meaning:
- the live token contract has not been localized, so static cleanup is outrunning evidence

Next move:
- return to the request finalization site and paused call frame selection

### Failure mode 4: one-off reproduction works once and then dies
Likely meaning:
- hidden retry/session/challenge state was never bounded
- the workflow captured the output but not the state transition that produced it

Next move:
- compare first-generation vs second-generation call stacks and state objects

## 9. Practical analyst checklist

### Phase A: classify the family shape
- [ ] mostly challenge/bootstrap + sensor/cookie state (DataDome-like)
- [ ] mostly image/artifact + encrypted validation packaging (GeeTest-like)
- [ ] mostly token-family / pre-dispatch request shaping (Kasada-like)

### Phase B: pin one concrete request/response moment
- [ ] identify the first meaningful challenge or token transition
- [ ] record where the value lands
- [ ] compare first attempt vs retry / post-challenge

### Phase C: choose first hooks wisely
- [ ] DataDome-like: bootstrap/cookie/sensor hooks
- [ ] GeeTest-like: answer-object / pack / encrypt hooks
- [ ] Kasada-like: request-finalization / call-frame hooks

### Phase D: capture the highest-value structured artifact
- [ ] DataDome-like: signal/state object before challenge submission
- [ ] GeeTest-like: answer object before encryption
- [ ] Kasada-like: live callable contract and input object

### Phase E: decide whether to stay in-browser or externalize
- [ ] keep browser as harness while prerequisites remain hidden
- [ ] externalize only after minimum state and role assumptions are named

## 10. What this page adds to the KB
This page adds something the KB was missing:
- a **family-differentiated first-pass workflow** for three common browser protection styles
- explicit decision rules for when to prioritize environment, artifact solving, or token-contract recovery
- concrete breakpoint/hook placement advice by family
- practical failure diagnosis when the analyst picked the wrong workflow model

This is more useful than yet another page saying that browser anti-bot analysis is "complex".

## 11. Source footprint / evidence note
Primary grounding for this page comes from:
- `sources/browser-runtime/2026-03-14-datadome-geetest-kasada-notes.md`
- official DataDome slider documentation
- practitioner repository summaries for DataDome, GeeTest V4 slide, and Kasada token-generation work
- existing KB browser pages on CDP-guided token analysis, environment reconstruction, and browser-side risk-control workflows

This page is still a synthesis workflow note rather than a target-lab notebook for one single site.
Its value is in distinguishing three recurring target-family shapes that otherwise get blurred together.

## 12. Topic summary
DataDome / GeeTest / Kasada workflow note is a practical page for deciding what kind of browser protection problem you actually have before you waste time on the wrong reversing workflow.

It matters because all three families can look like "web anti-bot" from far away, while in practice they often reward very different first moves:
- DataDome-like cases often reward state/sensor/challenge tracing
- GeeTest-like cases often reward answer-object and validation-packing recovery
- Kasada-like cases often reward pre-dispatch token-contract recovery in the live browser frame
