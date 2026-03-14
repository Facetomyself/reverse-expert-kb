# CDP-Guided Token Generation Analysis

Topic class: concrete methodology / workflow cookbook page
Ontology layers: browser-runtime subdomain, request-shaping workflow, runtime evidence
Maturity: structured-practical
Related pages:
- topics/browser-cdp-and-debugger-assisted-re.md
- topics/browser-fingerprint-and-state-dependent-token-generation.md
- topics/browser-side-risk-control-and-captcha-workflows.md
- topics/reese84-and-utmvc-workflow-note.md
- topics/browser-environment-reconstruction.md
- topics/js-wasm-boundary-tracing.md

## 1. Why this page exists
This page exists to capture a very practical browser-reversing move that is more actionable than generic “use DevTools” advice:

**pause at the right request-generation frame, then call the in-scope token/encrypt/decrypt function through CDP instead of immediately porting the whole algorithm out of the browser.**

This is exactly the sort of grounded methodology the KB needs more of.

It is useful when the analyst can already reach a meaningful breakpoint, but the target still depends on:
- closures
- dynamically initialized constants
- wrapper objects
- browser APIs
- page/session/challenge state
- mixed JS/Wasm execution context

## 2. Target pattern / scenario
This workflow is especially useful when a browser target has some combination of the following:
- the interesting value is attached shortly before request dispatch
- the actual callable function exists in lexical scope only at certain frames
- the algorithm is annoying to port because helpers/constants are scattered through wrappers
- the page’s runtime state matters more than pretty source recovery
- a one-shot call would already answer an important question

Representative scenarios:
- request body encryption / decryption around a live API
- anti-bot token generation just before header/body attachment
- challenge-step signature generation inside a request wrapper
- JS/Wasm-backed parameter generation where JS still owns the useful call site
- browser-side values that are easy to invoke in-frame but painful to reconstruct out-of-frame

## 3. Analyst goal
The goal is usually not “fully reverse the algorithm today.”

The immediate goal is one of:
- confirm which function generates the value
- test the function with controlled input while preserving page state
- identify the minimum arguments and constants needed
- separate the stable callable core from its volatile wrappers
- decide whether the next step should be deeper tracing or externalization

## 4. Concrete workflow

### Step 1: anchor to a real network event
Start from the request or response that matters.

Record:
- exact request carrying the token / encrypted field
- whether the value appears in header, cookie, body, or query
- whether the request happens on load, retry, challenge transition, or user action
- whether the target function seems to be called once per request or reused

Do not start from random bundle search if the network edge is already known.

### Step 2: locate the final useful breakpoint
High-yield breakpoint regions are usually:
- request builder / serializer wrappers
- header/body merge sites
- the line right before `fetch` / `XMLHttpRequest.send`
- response handlers if the server response refreshes the token
- JS wrappers immediately before a wasm export call

The best breakpoint is often not inside the deepest crypto code.
It is the highest frame where:
- the callable function exists,
- its helper objects/constants exist,
- and the call context still reflects the real request state.

### Step 3: inspect the call stack for the best frame
Once paused, walk the stack upward and ask of each frame:
- does this frame expose the function I want to call?
- does it also expose the constants/helpers/objects the function needs?
- is this frame stable across repeated requests, or only accidental?

The most useful frame is typically the nearest one where the full call contract is present, not the deepest obfuscated helper.

### Step 4: evaluate on the paused call frame
Use CDP call-frame evaluation to invoke the candidate function directly while the page is paused.

Minimal pseudocode sketch:

```text
on Debugger.paused(event):
  frame = chooseBestFrame(event.callFrames)
  result = CDP.send("Debugger.evaluateOnCallFrame", {
    callFrameId: frame.id,
    expression: "targetFn(controlledInput, maybeConstantOrCtx)"
  })
```

The point is not the exact syntax.
The point is that the browser page itself remains the harness:
- closures stay alive
- runtime state stays live
- page-initialized constants stay available
- browser APIs remain present

### Step 5: write down the call contract
For each successful in-frame call, record:
- breakpoint location
- stack frame identity / distinguishing features
- expression used
- argument shape
- required helper/constants names
- whether request/challenge/session state had to exist first
- whether the result was a final token, intermediate object, or pointer/handle

A useful compact template:

```text
call contract:
  request role: pre-dispatch token attach for /api/foo
  breakpoint: wrapper just before body encryption
  frame: caller frame above obfuscated helper
  expression: Object(ht.b)(payload, _dyn$.t(622))
  prerequisites: page initialized, login flow completed, current session alive
  output: encrypted request body string
```

This is often more valuable than a half-finished port.

### Step 6: vary one thing at a time
Once in-frame calling works, use it for controlled comparisons.

Change one axis at a time:
- input payload only
- retry count / challenge stage
- browser state baseline
- page initialization path
- presence/absence of DevTools or deeper instrumentation

Questions to answer:
- does the same frame remain valid?
- do constants/helpers drift?
- is the output stable for identical inputs?
- does the page need hidden prior state before the call works?

## 5. Where to place breakpoints / hooks

### A. Pre-dispatch request wrapper
Use when:
- you know which request carries the field
- you want the highest-leverage frame with realistic request context

Why it is useful:
- token function and request context often coexist here
- you can test candidate calls without yet understanding every helper below

### B. Response-driven refresh handler
Use when:
- token changes only after server response
- retry/challenge loop appears stateful

Why it is useful:
- it reveals whether the page updates helper state or session material before the next request

### C. JS wrapper around wasm export
Use when:
- mixed JS/Wasm target
- wasm looks important but direct wasm debugging is too early

Why it is useful:
- JS often still owns the meaningful arguments and return-path interpretation
- the wrapper may expose cleaner in-frame call opportunities than the raw wasm export

### D. Cookie / storage write site
Use when:
- the interesting value is persisted before dispatch
- stateful challenge transitions are likely

Why it is useful:
- lets you distinguish generation from later attachment

## 6. Representative pseudocode and harness sketch

### CDP-side control loop sketch

```javascript
// sketch only
cdp.on('Debugger.paused', async (event) => {
  const frame = pickFrame(event.callFrames);
  const out = await cdp.send('Debugger.evaluateOnCallFrame', {
    callFrameId: frame.callFrameId,
    expression: 'candidateFn(testPayload, helperConst)'
  });
  console.log(out);
});
```

### Later-stage validation harness sketch

```python
# sketch only
import requests

def invoke_live_page(expression: str):
    return requests.post(
        'http://127.0.0.1:8002/remote',
        data={'eval': expression},
        timeout=10,
    ).json()

# Example shape: convert payload through page-resident function
resp = invoke_live_page("Object(ht.b)('demo', _dyn$.t(622))")
```

This is not the first analytical move.
It is a later-stage wrapper once the breakpoint and call contract are already trustworthy.

## 7. Likely failure modes

### Failure mode 1: expression works once, then stops working
Likely causes:
- wrong frame chosen
- helper/constants only valid in a neighboring frame
- hidden request/challenge/session prerequisites
- page state changed after the paused point

Next move:
- compare frame layout across repeated pauses
- record which upstream state transitions happened before the good call

### Failure mode 2: function returns something, but server rejects it
Likely causes:
- you called an intermediate transform, not the final request role
- missing wrapper step after the current function
- page state or request role mismatch
- output is bound to sequence/challenge context

Next move:
- inspect one frame higher and one frame lower
- compare final attachment site inputs vs your test call inputs

### Failure mode 3: debugger-visible behavior changes too much
Likely causes:
- timing-sensitive path
- debugger detection / anti-observation logic
- mixed JS/Wasm or anti-bot logic reacting to inspection

Next move:
- reduce breakpoint count
- prefer high-value final-write-site pauses over deep stepping
- compare quieter runs with and without DevTools/CDP visibility

### Failure mode 4: analyst externalizes too early
Likely causes:
- excitement after the first callable success
- underestimating hidden state and closure dependence

Next move:
- stay in-browser until the call contract is stable across repeated runs
- only externalize after you can enumerate the minimum prerequisites

## 8. Decision rule: when to stay in-browser vs externalize

### Stay in-browser if
- the function only works in a narrow lexical scope
- helper objects and constants are still poorly understood
- challenge/session state is still drifting
- the value path crosses JS/Wasm or response-driven updates you have not mapped yet

### Externalize when
- the callable core is stable across runs
- prerequisites are enumerable
- constants/helper material can be captured or reconstructed
- you can explain where in the request role the function belongs

A good rule:
**if your best artifact is still “this only works when paused at this one magical frame,” you are not ready to externalize.**

## 9. Practical checklist
- [ ] identify exact request/response role for the value
- [ ] place breakpoint at final useful wrapper, not random deep code
- [ ] inspect upward/downward frames for the best call context
- [ ] test `evaluateOnCallFrame` with controlled input
- [ ] record the call contract
- [ ] compare identical calls across repeated runs
- [ ] note debugger-visible drift if any
- [ ] only then decide on harnessing / extraction

## 10. What this page adds to the KB
This page adds a concrete method bias the KB previously lacked:
- use the browser page as a temporary live harness
- recover callable contracts before full ports
- treat frame selection as a first-class analytical choice
- shift from abstract “debugger-assisted RE” to a reusable request-shaping workflow

## 11. Source footprint / evidence note
Grounding for this page comes from:
- practitioner writeup on remote CDP invocation of breakpoint-scope functions
- official Chrome DevTools wasm/debugging documentation
- prior KB browser pages on token generation, CDP observation, environment reconstruction, and concrete target families such as Reese84 / ___utmvc

This page is intentionally a **workflow cookbook page**, not an abstract taxonomy page.

## 12. Topic summary
CDP-guided token generation analysis is a practical browser methodology for situations where the fastest path is not full deobfuscation, but pausing at the right live frame and using the page’s own execution context to call the function that matters.

It matters because many browser-side request-shaping problems become answerable as soon as the analyst can reliably identify the frame, the callable expression, the prerequisite state, and the point where the page itself is still the best harness.