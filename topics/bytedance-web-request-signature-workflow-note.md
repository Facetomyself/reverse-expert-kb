# Bytedance-Style Web Request-Signature Workflow Note

Topic class: concrete target-family workflow note
Ontology layers: browser-runtime subdomain, request-signature workflow, parameter-path localization
Maturity: structured-practical
Related pages:
- topics/browser-parameter-path-localization-workflow-note.md
- topics/browser-fingerprint-and-state-dependent-token-generation.md
- topics/browser-side-risk-control-and-captcha-workflows.md
- topics/browser-environment-reconstruction.md
- topics/browser-cdp-and-debugger-assisted-re.md
- topics/acw-sc-v2-cookie-bootstrap-and-consumer-path-note.md
- topics/environment-differential-diagnosis-workflow-note.md

## 1. Why this page exists
This page exists because the browser KB needed more **request-signature-family practice notes**, not more abstract token taxonomy.

A recurring real target shape in practitioner material is a browser request that carries fields like:
- `X-Bogus`
- `_signature`
- `msToken`
- `a_bogus`
- related sibling fields such as `verifyFp`, `fp`, `ttwid`, `webid`
- comparable site-specific families such as Xiaohongshu `x-s`, `x-t`, `x-s-common`

The useful analyst question in these cases is usually not:
- what brand name does this field family belong to?

It is:
- which request actually depends on the field?
- where is the field inserted into query/header/body construction?
- what sibling fields or cookie state travel with it?
- where can I capture the structured preimage before final formatting destroys meaning?
- is the failure caused by wrong math, wrong environment, wrong session state, or wrong field family coupling?

This page is therefore a practical workflow note for a common browser request-signature shape.

## 2. Target pattern / scenario
A representative target shape looks like this:

```text
browser page / API flow
  -> host-page wrapper prepares request role and context
  -> obfuscated or wrapped JS computes one or more signature-like values
  -> query/header/body/cookie state is finalized
  -> protected request is emitted
  -> backend either accepts, challenges, throttles, or changes response shape
```

Common analyst situations:
- one named field is visible in the request, but the request still fails when replayed
- a cookie-like sibling state such as `msToken` or `ttwid` appears to matter as much as the named signature field
- bundle code looks heavily wrapped, so the analyst does not know where to start
- a node-side or harness-side port seems plausible, but behavior drifts under replay
- one request family works while a nearby request family fails because the role or sibling state changed

## 3. Analyst goal
The goal is not just to "recover the algorithm."
The goal is to recover the **request-signature path**:

```text
request role / URL / body / browser-state context
  -> field insertion site
  -> immediate producer
  -> structured preimage / sibling state family
  -> final formatting / packaging
  -> first accepted protected request
```

A good output from this workflow is something like:

```text
GET /api/search?... requires X-Bogus + msToken + verifyFp
  -> request wrapper computes normalized query string
  -> immediate producer takes {query, UA, timestamp, cookie state}
  -> final insert happens in request-finalization helper
  -> retry succeeds only when cookie/session family is preserved
```

That artifact is more useful than either a vague family label or a raw deobfuscated blob.

## 4. Concrete workflow

### Step 1: anchor one concrete request role
Start from the network timeline and choose **one request that materially changes behavior**.
Do not begin with global bundle cleanup.

Record:
- endpoint and method
- whether the field is in query, header, body, or cookie-adjacent state
- whether it appears on first request, retry, or only after bootstrap/navigation
- whether neighboring fields change at the same time
- whether acceptance/challenge state changes when the field family changes

Useful note format:

```text
request role:
  GET /api/search/items
field family:
  X-Bogus in query
  msToken in cookie/query context
  verifyFp sibling present
outcome:
  accepted on baseline browser run
  challenged on altered replay
```

### Step 2: localize the final attachment site
For this family, the best first win is usually the **attachment site**, not the deepest transform function.

High-yield attachment surfaces:
- custom request wrapper
- fetch/XHR wrapper before final URL assembly
- serializer that appends query/body values
- helper that merges cookie-derived state with request params
- function that inserts one named field and nearby siblings together

Why this matters:
- once you find the final insert, the stack often reveals the producer chain quickly
- you can distinguish field insertion from earlier wrappers or later transport formatting
- you can see whether multiple anti-risk fields are emitted together

### Step 3: classify the stage you hit
When a function looks promising, ask whether it is:
- collecting request context
- reading cookie/browser state
- normalizing URL/query/body inputs
- performing final transform / packing
- formatting a field already produced elsewhere
- attaching the final value into the request

A useful minimal staging model is:

```text
request role + browser/cookie/session state
  -> normalization / canonicalization layer
  -> transform / wrapped compute layer
  -> final field formatting
  -> request insertion
```

This prevents mistaking a formatter for the true preimage boundary.

### Step 4: capture the structured preimage, not just the final value
A major trap in this family is logging the final field and learning very little.

Try to capture one stage earlier:
- canonical query string
- normalized body digest / body text
- timestamp / nonce set
- cookie-derived state (`msToken`, `ttwid`, `webid`, etc.)
- browser-state inputs such as UA or fingerprint-adjacent values
- object/map of fields before final packing or encoding

Representative preimage thought model:

```text
request_ctx = {
  url_path,
  sorted_query,
  body_digest,
}

state_ctx = {
  msToken,
  verifyFp,
  ttwid,
  webid,
}

runtime_ctx = {
  ua,
  ts,
  feature_flags,
}
```

The exact schema is target-specific, but this shape is usually more explanatory than the opaque output field alone.

### Step 5: test the field-only hypothesis against field-family hypotheses
Do not assume one named field is the whole contract.
At least practitioner material repeatedly suggests field families such as:
- `X-Bogus` + `msToken`
- `_signature` + cookie/browser state
- `x-s` + `x-t` + `x-s-common`
- field + `verifyFp` / `fp` / `ttwid` / `webid`

Explicitly test whether the request only works when:
- named field is correct but sibling cookie state is also preserved
- named field and timestamp family drift together
- same request role and navigation/session order are preserved
- same environment assumptions are preserved

### Step 6: compare baseline browser run vs altered replay
This family often fails because the *path* is correct but the *conditions* changed.
Compare at least:
- baseline browser run vs instrumented run
- cold session vs warm session
- first request vs retry
- same field output vs altered cookie/session family
- in-browser request vs harness/external replay

Record the first divergence point.
If local path looks similar but remote outcome changes first, you may be seeing trust/session drift rather than pure algorithm drift.

## 5. Where to place breakpoints / hooks

### A. Request-finalization wrapper
Use when:
- you already know which request matters
- you need the fastest path to field insertion

Inspect:
- final URL/body/header before dispatch
- call stack at the moment the field is appended
- whether sibling fields are added in the same helper

### B. Serializer / canonicalization helper
Use when:
- final field likely depends on normalized query/body content
- request data is transformed before field generation

Inspect:
- sorted query params
- body serialization output
- whether path/query/body is canonicalized before compute

### C. Cookie/state read boundary
Use when:
- `msToken` / `ttwid` / `webid` / `verifyFp`-like state appears in the family
- replay fails despite apparently correct visible field generation

Inspect:
- which state is read from cookie/storage vs passed as parameter
- whether the state is refreshed earlier in the navigation chain
- whether stale-but-visible state differs from accepted state

### D. Immediate producer of the named field
Use when:
- you have the insertion site and need one step upstream
- you want the preimage, not just the output

Inspect:
- raw arguments
- whether one helper emits multiple fields
- whether the function returns final text or intermediate structure

### E. Environment reconstruction edge
Use when:
- node-side reuse or harness replay is attempted
- browser execution fails unless enough APIs/prototypes/state are preserved

Inspect:
- missing DOM/prototype/storage assumptions
- whether browser-specific globals are consumed before compute
- whether environment-sensitive feature checks only gate execution or also feed the field

## 6. Representative code / pseudocode / harness fragments

### Request-finalization capture sketch
```javascript
// sketch only
const origFetch = window.fetch;
window.fetch = async function(input, init) {
  debugger;
  console.log('request-finalization', { input, init });
  return origFetch.apply(this, arguments);
};
```

### Field-family recording template
```text
request role:
  GET /api/search/items

named field:
  X-Bogus

sibling family:
  msToken, verifyFp

insertion site:
  requestWrapper -> appendSignedQuery()

immediate producer inputs:
  sortedQuery, ua, ts, cookieState

outcome:
  accepted in baseline browser run
  rejected in replay when cookie family drifted
```

### Minimal harness thought model
```python
# sketch only
class RequestCtx:
    path = None
    query = None
    body = None

class StateCtx:
    ms_token = None
    verify_fp = None
    ttwid = None

class RuntimeCtx:
    ua = None
    ts = None


def collect_preimage(request_ctx, state_ctx, runtime_ctx):
    return {
        "path": request_ctx.path,
        "query": request_ctx.query,
        "body": request_ctx.body,
        "msToken": state_ctx.ms_token,
        "verifyFp": state_ctx.verify_fp,
        "ttwid": state_ctx.ttwid,
        "ua": runtime_ctx.ua,
        "ts": runtime_ctx.ts,
    }
```

The point of the harness is to test whether the path is truly separable, not to prematurely rebuild the whole site.

## 7. Likely failure modes

### Failure mode 1: analyst focuses on one named field and ignores the family
Likely cause:
- field-only thinking
- cookie/browser-state siblings ignored
- wrong assumption that output field alone determines acceptance

Next move:
- map sibling fields and state reads around the insertion site

### Failure mode 2: analyst deobfuscates wrappers before localizing request role
Likely cause:
- JSVMP / obfuscation pressure hijacked the workflow
- no clear target request yet

Next move:
- return to one concrete request and find the final insert boundary first

### Failure mode 3: replay reproduces the field but request still fails
Likely cause:
- stale `msToken` / cookie state
- missing `verifyFp` / `ttwid` / related siblings
- request role or navigation order changed
- environment assumptions changed

Next move:
- compare field family and request role across baseline and replay, not just the named output

### Failure mode 4: environment patching grows without bound
Likely cause:
- analyst trying to recreate the whole browser before bounding which APIs actually matter
- failure is partly session/trust drift rather than pure environment absence

Next move:
- capture actual environment reads near the immediate producer and insertion site
- reduce to minimum necessary assumptions

### Failure mode 5: output changes across retries and analyst assumes algorithm drift
Likely cause:
- session drift
- cookie refresh
- timestamp/counter dependence
- backend-side trust reclassification

Next move:
- compare first accepted request vs retry and record the first divergence point

## 8. Environment assumptions
This family often needs more than pure arithmetic extraction but less than a full browser clone at the beginning.
A good default assumption is:
- preserve realistic cookie/storage/browser state long enough to localize the path
- capture environment reads near the immediate producer
- do not expand the harness until the request role and field-family coupling are clear

## 9. What to verify next
Once the path is localized, verify:
- whether the same helper emits multiple sibling fields
- whether cookie/state refresh occurs before the target request
- whether the named field changes because request inputs changed or because state changed
- whether the minimal harness can recreate the preimage under preserved state assumptions
- whether failures are mostly execution drift, trust drift, session drift, or observation drift

## 10. What this page adds to the KB
This page adds the missing browser counterpart to the mobile signature/preimage workflow pages:
- request-role-first analysis for browser request-signature families
- emphasis on attachment path before deep transform recovery
- field-family rather than field-only reasoning
- structured preimage capture
- practical failure diagnosis for replay and environment drift

That is exactly the kind of practical, case-driven browser material the KB needed more of.

## 11. Source footprint / evidence note
Grounding for this page comes from:
- `sources/browser-runtime/2026-03-14-bytedance-web-signature-family-notes.md`
- search-layer result cluster around `X-Bogus`, `_signature`, `msToken`, `x-s`, `x-t`, and related open-source/practitioner material
- existing KB pages on browser parameter-path localization, browser fingerprint/state-dependent tokens, and environment-differential diagnosis

This page intentionally stays workflow-centered and avoids overclaiming undocumented internals of any one live target.

## 12. Topic summary
Bytedance-style web request-signature analysis is a practical browser workflow where the key task is usually not naming one signature field, but tracing how request role, cookie/browser state, and normalized request inputs become a coupled field family at the final insertion boundary.

It matters because analysts often stop at "I found X-Bogus" or "I can compute x-s," while the more useful answer is "this request wrapper inserts the family here, these sibling states are required, this is the structured preimage, and this is where replay begins to drift."