# acw_sc__v2 Cookie Bootstrap and Consumer-Path Note

Topic class: concrete target-family workflow note
Ontology layers: browser-runtime subdomain, cookie-bootstrap workflow, request-path localization
Maturity: structured-practical
Related pages:
- topics/browser-parameter-path-localization-workflow-note.md
- topics/browser-side-risk-control-and-captcha-workflows.md
- topics/browser-fingerprint-and-state-dependent-token-generation.md
- topics/browser-cdp-and-debugger-assisted-re.md
- topics/browser-environment-reconstruction.md
- topics/environment-differential-diagnosis-workflow-note.md
- topics/reese84-and-utmvc-workflow-note.md

## 1. Why this page exists
This page exists because `acw_sc__v2`-style cases are exactly the kind of browser target the KB needs more of after the human correction:
- concrete
- request-adjacent
- cookie/bootstrap oriented
- breakpointable
- diagnosable through compare-runs

The practical analyst question here is usually not:
- what abstract class of anti-bot is this?

It is:
- where does the bootstrap JS enter?
- where is the cookie actually written?
- which first request really depends on it?
- is the cookie sufficient, or does another signed/sibling field travel with it?
- does instrumentation or session drift change the path?

This page is therefore a workflow note for a recurring target family, not a taxonomy page.

## 2. Target pattern / scenario
A representative `acw_sc__v2`-like shape is:

```text
page load or protected endpoint
  -> challenge/bootstrap JS delivered or triggered
  -> browser executes obfuscated logic
  -> cookie state is computed/written (`acw_sc__v2` or related)
  -> subsequent request replays with cookie present
  -> server either accepts, redirects, or escalates
```

Common analyst situations:
- a protected page loops until a JS challenge completes
- the cookie appears in DevTools, but the request still fails
- the first success seems to require both cookie state and another request parameter
- the workflow works once, then drifts on retry or reload
- heavy instrumentation changes the observed path

## 3. Analyst goal
The goal is not just “get the cookie string.”
The goal is to recover the full bootstrap-to-consumer path:

```text
bootstrap response / inline challenge
  -> local compute / wrapper logic
  -> cookie write
  -> first accepted consumer request
  -> any sibling signed/derived fields
```

A good output from this page’s workflow is something compact like:

```text
response /?foo=... returns challenge JS
  -> eval/obfuscated wrapper runs
  -> document.cookie writes acw_sc__v2=...
  -> next GET /search carries cookie and is accepted
  -> request also carries Sign field derived from same or neighboring state
```

That artifact is much more useful than a long static bundle dump.

## 4. Concrete workflow

### Step 1: anchor the first challenge/bootstrap response
Start from the network timeline.
Identify:
- which response first introduces the challenge or bootstrap logic
- whether the JS is inline, dynamically fetched, or response-embedded
- whether the cookie write happens on initial load, redirect, retry, or protected-endpoint response

Useful record format:

```text
request A: protected endpoint -> challenge HTML/JS
request B: challenge asset / inline eval path runs
cookie write: acw_sc__v2=...
request C: same protected endpoint retried with cookie
response class: challenge again / accepted / redirect
```

This already tells you more than random source search.

### Step 2: hook the cookie write path
For this family, `document.cookie` is often a first-class anchor.
Do not stop at observing cookie presence in storage panels.
Find:
- the actual write site
- the call stack leading into the write
- whether the value is final at the write site or assembled just upstream

Representative observation priorities:
- cookie setter path
- write-triggering callback or response handler
- any helper function immediately upstream of the final string assembly

### Step 3: identify the first real consumer request
The cookie is not the end of the workflow.
Find the first request that materially changes behavior because the cookie is present.
Record:
- endpoint and method
- whether the request is the same original protected endpoint or a follow-up resource/API
- whether acceptance requires only the cookie or also sibling fields
- whether the cookie value changes again before dispatch

A useful artifact is:

```text
visible surface: document.cookie write
first consumer: GET /protected/list
server effect: no longer serves challenge page
sibling fields: query Sign present and changes with cookie/session context
```

### Step 4: test the cookie-only hypothesis against sibling-field hypotheses
Do not assume `acw_sc__v2` alone is the whole contract.
At least some real-site discussions pair it with another signed field.
So explicitly test:
- cookie only
- cookie + original query/body/header fields
- cookie + same session/navigation timing
- cookie + same redirect/retry order

This keeps you from overfitting to the first visible artifact.

### Step 5: classify what layer your current breakpoint hit
When you land in code, ask whether you are seeing:
- challenge-response unpacking
- input collection
- transform/mix logic
- final cookie string formatting
- request-finalization logic after the cookie already exists

Minimal chain model:

```text
challenge/bootstrap response
  -> wrapper / decode / eval layer
  -> transform or state-assembly layer
  -> cookie string assembly
  -> consumer request
```

This prevents confusing a formatter or attach site for the algorithmic core.

### Step 6: compare first pass vs retry / reload / new session
This family can look stable until you compare runs.
At minimum, compare:
- cold session vs warm session
- first success vs second attempt
- light instrumentation vs heavy instrumentation
- same path with and without sibling sign field changes

Record the first divergence point, not just the final failure.
If divergence first appears in the remote response while local execution looks similar, you may be in trust/session drift rather than pure execution drift.

## 5. Where to place breakpoints / hooks

### A. Bootstrap response handler or inline challenge entry
Use when:
- the challenge is delivered by the protected page itself
- you still do not know what code path actually starts the cookie workflow

Inspect:
- where inline JS is evaluated or invoked
- whether a redirect/retry callback is scheduled
- whether the response immediately seeds state used by cookie generation

### B. `document.cookie` write path
Use when:
- the cookie is the clearest visible artifact
- bundle search is noisy

Inspect:
- upstream helper frames
- final assembled cookie string
- whether the cookie is written once or multiple times

Representative sketch:

```javascript
// sketch only
const cookieDesc = Object.getOwnPropertyDescriptor(Document.prototype, 'cookie')
  || Object.getOwnPropertyDescriptor(HTMLDocument.prototype, 'cookie');
Object.defineProperty(document, 'cookie', {
  set(v) {
    console.log('cookie write', v);
    debugger;
    return cookieDesc.set.call(document, v);
  },
  get() {
    return cookieDesc.get.call(document);
  }
});
```

### C. Request-finalization boundary for the first accepted request
Use when:
- you know which request becomes accepted after cookie generation
- you need to test whether sibling values matter

Inspect:
- query/body/header assembly
- whether another `Sign`-like field changes at the same time
- whether the cookie is read explicitly or just allowed to flow implicitly with the browser request

### D. Retry / redirect / reload handlers
Use when:
- first run works, second run drifts
- the page may challenge, redirect, or refresh state between attempts

Inspect:
- whether a new bootstrap runs
- whether the cookie is rewritten
- whether the consumer request changes role or sibling fields

## 6. Representative code / pseudocode / harness fragments

### Cookie-write capture sketch
```javascript
// sketch only
(function() {
  const proto = Document.prototype;
  const desc = Object.getOwnPropertyDescriptor(proto, 'cookie');
  Object.defineProperty(document, 'cookie', {
    configurable: true,
    set(v) {
      console.log('[cookie-write]', v);
      debugger;
      return desc.set.call(document, v);
    },
    get() {
      return desc.get.call(document);
    }
  });
})();
```

### Consumer-path recording template
```text
bootstrap origin:
  response: GET /protected/search -> challenge payload

write site:
  artifact: acw_sc__v2 cookie
  frame: obfuscated helper -> cookie formatter -> setter

first consumer:
  request: GET /protected/search?page=1
  effect: accepted after cookie exists
  sibling fields: Sign, timestamp

compare-run note:
  cold session: success
  retry with altered instrumentation: challenge repeats
```

### Minimal harness thought model
```text
inputs:
  challenge payload / page state / maybe time or sibling params

stages:
  decode/unwrap
  transform/build cookie value
  attach cookie
  replay first consumer request with stable sibling fields
```

The point of the harness is to test separability, not to prematurely port the whole browser.

## 7. Likely failure modes

### Failure mode 1: analyst proves cookie presence but not request acceptance
Likely cause:
- cookie visibility mistaken for a complete solve
- first real consumer request not yet localized
- sibling fields were ignored

Next move:
- identify the first accepted request and inspect concurrent query/body/header fields

### Failure mode 2: analyst over-focuses on static deobfuscation
Likely cause:
- bundle cleanup outran evidence collection
- formatter/wrapper layers are being studied without knowing which request matters

Next move:
- return to bootstrap response, cookie write, and first consumer request boundaries

### Failure mode 3: cookie replay works once, then fails
Likely cause:
- session drift
- challenge refresh
- response-coupled rewrite
- hidden navigation/order dependency

Next move:
- compare first and second runs, especially rewrite timing and first divergence point

### Failure mode 4: instrumentation seems to change the workflow itself
Likely cause:
- observation drift or integrity-sensitive behavior
- hook pressure on fetch/XHR/globals/prototypes

Next move:
- compare no-hook vs minimal-hook runs
- move hooks outward toward cookie-write and request-finalization boundaries
- downgrade trust in deep-hook evidence if only instrumented runs drift

### Failure mode 5: algorithm port looks right but site still rejects
Likely cause:
- the cookie was only one member of a coupled family
- request order or sibling sign field remained wrong
- browser/runtime assumptions are still missing

Next move:
- treat the case as cookie-bootstrap-plus-consumer-path analysis, not pure arithmetic porting

## 8. Environment assumptions
This family often rewards a moderate environment model:
- enough browser semantics for the challenge/bootstrap JS to run correctly
- stable session/cookie handling
- trustworthy observation with minimal distortion

It may not always require the heaviest browser-fingerprint reconstruction up front.
But it often requires more than static math extraction, especially when request ordering or sibling fields matter.

## 9. What to verify next
Once you localize the cookie bootstrap path, verify:
- whether another signed field travels with the accepted request
- whether the cookie is regenerated across retry or redirect
- whether the first accepted request is the real target or only an intermediate unlock step
- whether the minimal harness can recreate the cookie under preserved bootstrap inputs
- whether instrumentation changes the path enough to force a quieter observation surface

## 10. What this page adds to the KB
This page adds a concrete browser family note that the KB was missing:
- a cookie-bootstrap-centric workflow
- explicit separation between cookie visibility and request acceptance
- breakpoint placement around bootstrap response, cookie write, and first consumer request
- failure diagnosis that treats sibling fields and observation drift as first-class concerns

That is exactly the kind of practical, target-grounded material the KB needs more of.

## 11. Source footprint / evidence note
Grounding for this page comes from:
- `sources/browser-runtime/2026-03-14-acw-sc-v2-cookie-bootstrap-notes.md`
- practitioner/search-layer evidence around `acw_sc__v2` cookie reversing
- concrete title-level evidence tying `acw_sc__v2` to real-site search-interface reversing and coexisting signed parameters
- existing KB workflow notes on parameter-path localization, browser token generation, and environment-differential diagnosis

This page intentionally stays workflow-centered and avoids overclaiming undocumented internals where extraction quality was weak.

## 12. Topic summary
`acw_sc__v2` cookie bootstrap analysis is a practical browser-reversing workflow where the real task is to trace the challenge/bootstrap response into a cookie write, then into the first request that actually changes server behavior.

It matters because analysts often stop at “the cookie exists,” when the more useful answer is “this bootstrap path writes the cookie, this next request consumes it, these sibling fields matter too, and this is where the workflow drifts across retries or instrumentation.”
