# TikTok Web Signature Workflow Note

Topic class: concrete site-specific workflow note
Ontology layers: browser-runtime subdomain, request-signature workflow, site-specific practical analysis
Maturity: structured-practical
Related pages:
- topics/bytedance-web-request-signature-workflow-note.md
- topics/browser-request-finalization-backtrace-workflow-note.md
- topics/browser-parameter-path-localization-workflow-note.md
- topics/browser-environment-reconstruction.md
- topics/browser-fingerprint-and-state-dependent-token-generation.md
- topics/jsvmp-and-ast-based-devirtualization.md
- topics/environment-differential-diagnosis-workflow-note.md

## 1. Why this page exists
This page exists because the KB already had a family-level note for ByteDance-style browser signatures, but still lacked a dedicated **TikTok web** workflow page.

That gap mattered because TikTok is one of the clearest cases where analysts repeatedly face the same practical problem shape:
- one concrete protected request role matters
- `X-Bogus` is visible, but not sufficient as the whole explanation
- `msToken` and related browser/session state travel with the request
- a monkey-patched request wrapper and obfuscated `webmssdk`/`secsdk` path sit between analyst and answer
- blindly deobfuscating the whole VM is often slower than localizing the request-finalization path first

The useful analyst question is usually not:
- what is the abstract taxonomy of TikTok signatures?

It is:
- which request actually changes behavior?
- where is the final request attachment boundary?
- what structured inputs become `X-Bogus` and sibling fields?
- is failure caused by bad canonicalization, stale `msToken`, environment drift, or backend trust classification?

This page therefore focuses on the practical TikTok workflow analysts actually need.

## 2. Target pattern / scenario
A representative TikTok web path looks like:

```text
page action / feed / search / detail request
  -> page/request wrapper builds telemetry-rich query params
  -> monkey-patched fetch / request client passes through `secsdk` / `webmssdk`
  -> signer path derives `X-Bogus` and possibly sibling fields
  -> `msToken` and browser/session/runtime context travel with the request
  -> server returns accepted data, empty/zero-length body, or other degraded behavior
```

Common analyst situations:
- a request visibly carries `X-Bogus`, but replay still fails
- removing `_signature` appears less important than removing `msToken` or `X-Bogus`
- a browser baseline returns data, while replay returns empty or zero-length output
- the bundle is VM-heavy enough that the analyst is tempted into full devirtualization too early
- a node-side or harness-side port generates signatures but still drifts at the response layer

## 3. Analyst goal
The goal is not merely to “compute `X-Bogus`.”
The goal is to recover the **TikTok request-signature path**:

```text
request role / canonical query + body context
  -> final request wrapper
  -> immediate signer producer
  -> `X-Bogus` + sibling request/session state
  -> first accepted data-bearing request
```

A useful output from this workflow looks like:

```text
GET /api/search/user/full/
  -> wrapper builds canonical query + telemetry set
  -> signer path consumes query/body/UA/timestamp context
  -> `X-Bogus` attached here; `msToken` travels as sibling state
  -> browser baseline accepted
  -> replay with stale session/trust context returns empty body
```

That is more valuable than a raw deobfuscated chunk or one captured header string.

## 4. Concrete workflow

### Step 1: anchor one concrete request role
Start from one request that materially changes server behavior.
Good anchors include:
- search
- feed/list fetch
- note/video detail
- comment/list fetch

Record:
- endpoint and method
- whether the request is baseline browser-successful
- whether `X-Bogus`, `msToken`, and `_signature` are present
- whether the request returns full data, empty data, or zero-length output when altered

Useful scratch template:

```text
request role:
  GET /api/search/user/full/
field family:
  X-Bogus, msToken, _signature
outcome:
  browser baseline -> real data
  replay -> zero-length or degraded response
```

### Step 2: localize the final request boundary first
Before touching the deeper VM, find the latest trustworthy boundary before dispatch.
High-yield surfaces:
- monkey-patched `window.fetch`
- request client/interceptor layer
- serializer that finishes the query string
- helper that appends `X-Bogus` or merges query params before transport

Why this matters:
- it reveals the exact request contract at dispatch time
- it shows which fields travel together
- it gives the fastest route into the immediate producer chain

### Step 3: capture the structured preimage before final packing
Once the final boundary is known, move one step upstream and capture the last meaningful structured inputs.
For TikTok-style flows, useful preimage components often look like:
- canonical query string
- request body or body digest
- user-agent or UA-derived digest input
- timestamp/counter inputs
- `msToken` / cookie/session context
- browser-derived values used by the signer path

Representative thought model:

```text
request_ctx = {
  path,
  query,
  body,
}

state_ctx = {
  msToken,
  cookies,
  session_state,
}

runtime_ctx = {
  ua,
  ts,
  browser_values,
}
```

This boundary is usually more explanatory than the final `X-Bogus` text alone.

### Step 4: treat `msToken` as first-class evidence
Do not treat `msToken` as incidental clutter.
At least in readable practitioner material and implementation repos, `msToken` repeatedly appears as part of the request/session contract around protected web requests.

Check:
- whether `msToken` is merely transported or also refreshed/derived earlier in the flow
- whether the same visible `X-Bogus` with a different `msToken` changes outcome
- whether empty-body or degraded responses line up with session-state drift rather than pure signature drift

### Step 5: distinguish signature correctness from request acceptance
A major trap in this family is equating “I generated `X-Bogus`” with “the request is operational.”
Use at least three buckets:
- **hard reject / obviously invalid**
- **soft failure / empty or zero-length response**
- **true accepted data-bearing response**

Why this matters:
- older practical material explicitly notes cases where missing core fields cause zero-length responses
- implementation-oriented material also hints that trust, environment, and runtime context matter beyond raw field generation

### Step 6: compare baseline browser run vs replay or harness run
Compare at the same boundary across:
- baseline browser run vs instrumented browser run
- baseline browser run vs node-side harness
- fresh session vs older session
- same query/body with changed runtime/session assumptions

At each boundary ask:
- did the same final wrapper fire?
- did the same canonical query/body reach the signer?
- were `X-Bogus` and sibling state attached in the same place?
- was `msToken` the same or meaningfully different?
- did the first divergence appear as invalid request, empty response, or later data degradation?

This keeps the workflow grounded in actual behavior.

## 5. Where to place breakpoints / hooks

### A. Monkey-patched fetch / final request wrapper
Use when:
- you already know which request role matters
- you need the fastest path to the final request contract

Inspect:
- final URL/query/body
- whether `X-Bogus` is already attached here or one step earlier
- which fields travel with `msToken`
- call stack into `secsdk` / `webmssdk`

Representative sketch:
```javascript
// sketch only
const origFetch = window.fetch;
window.fetch = async function(input, init) {
  console.log('tiktok final request', { input, init });
  debugger;
  return origFetch.apply(this, arguments);
};
```

### B. Query/body canonicalization helper
Use when:
- `X-Bogus` appears to depend on canonical query/body formatting
- the transport wrapper is too late and values are already flattened

Inspect:
- sorted/normalized params
- body digest inputs
- whether one request role includes extra telemetry fields before signing

### C. Immediate signer producer
Use when:
- you already have the final boundary
- you want the structured preimage rather than only the final token

Inspect:
- raw inputs to the signer
- whether one helper returns multiple related artifacts
- whether UA/timestamp/browser-derived values are read nearby

### D. Session / cookie / `msToken` read boundary
Use when:
- replay reproduces visible fields but still degrades
- you suspect the request contract is drifting at the session layer

Inspect:
- where `msToken` is sourced or refreshed
- whether the signer consumes it directly or it merely travels with the request
- whether session-visible state changed between accepted and empty-response runs

### E. Environment reconstruction edge
Use when:
- a harness or externalized execution path is being attempted
- generated fields look plausible but response behavior drifts

Inspect:
- browser globals/prototypes touched near signer execution
- whether runtime values only gate execution or directly feed the signed contract
- whether browser-generated values such as canvas/static environment artifacts are consumed near the final producer chain

## 6. Representative code / pseudocode / harness fragments

### Final-boundary recording template
```text
request role:
  GET /api/search/user/full/

field family:
  X-Bogus, msToken, _signature

observed insertion boundary:
  requestWrapper -> secsdk -> fetch()

immediate producer inputs:
  canonical query, body digest, ua context, ts, session state

outcome:
  browser baseline -> accepted data
  replay -> empty body
```

### Preimage capture sketch
```python
# sketch only
class RequestCtx:
    path = None
    query = None
    body = None

class StateCtx:
    ms_token = None
    cookies = None
    session = None

class RuntimeCtx:
    ua = None
    ts = None
    browser_values = None


def collect_tiktok_presign(request_ctx, state_ctx, runtime_ctx):
    return {
        "path": request_ctx.path,
        "query": request_ctx.query,
        "body": request_ctx.body,
        "msToken": state_ctx.ms_token,
        "cookies": state_ctx.cookies,
        "session": state_ctx.session,
        "ua": runtime_ctx.ua,
        "ts": runtime_ctx.ts,
        "browser_values": runtime_ctx.browser_values,
    }
```

The point is not to clone the whole site immediately.
The point is to determine whether the preimage and sibling state are what actually explain success or failure.

## 7. Likely failure modes

### Failure mode 1: analyst focuses only on `X-Bogus`
Likely cause:
- field-only thinking
- `msToken` and session state ignored

Next move:
- map the full request family at the final boundary and track sibling state explicitly

### Failure mode 2: generated signature looks plausible but response is empty
Likely cause:
- session drift
- trust/environment drift
- browser-generated sibling values missing or stale
- canonical request differences hidden upstream

Next move:
- classify this as **soft failure / degraded**, not success
- compare session/runtime context against baseline browser evidence

### Failure mode 3: full VM cleanup takes over too early
Likely cause:
- obfuscated `webmssdk` path attracted attention before the request contract was stabilized

Next move:
- return to the one request that matters
- keep walking backward only from the proven request boundary

### Failure mode 4: environment patching grows without bound
Likely cause:
- trying to recreate the whole browser before identifying which reads actually matter

Next move:
- capture real environment reads near the immediate producer
- separate execution gating from true signature inputs

### Failure mode 5: one request role works while another fails
Likely cause:
- role-specific canonicalization or telemetry differences
- different trust/session expectations across endpoints

Next move:
- compare producer chains per request role instead of assuming interchangeability

## 8. Environment assumptions
TikTok web is a good example of a browser signature target where the right default assumption is:
- preserve realistic browser/session state long enough to localize the path
- treat request canonicalization and sibling state as first-class evidence
- distinguish empty/degraded responses from true accepted responses
- only then decide how much VM cleanup or environment reconstruction is truly necessary

This is usually better than immediately trying to fully rehost the signing stack.

## 9. What to verify next
Once the path is localized, verify:
- whether one signer path covers multiple high-value request roles
- whether `msToken` is direct signer input, companion session state, or both in practice
- where browser-derived values first enter the producer chain
- whether the first divergence between baseline and replay is canonicalization, session state, environment input, or backend trust classification
- whether a minimal harness can reproduce not just the visible signature, but a data-bearing accepted request under preserved state assumptions

## 10. What this page adds to the KB
This page adds exactly the kind of concrete target note the KB needed more of:
- a real site, not only a broad family abstraction
- request-boundary-first analysis
- explicit `msToken` / session coupling
- emphasis on structured preimage capture before total deobfuscation
- explicit distinction between visible signature generation and actual request acceptance

That makes it a practical operator note rather than another taxonomy page.

## 11. Source footprint / evidence note
Grounding for this page comes from:
- `sources/browser-runtime/2026-03-15-tiktok-web-signature-workflow-notes.md`
- `sources/browser-runtime/2026-03-14-bytedance-web-signature-family-notes.md`
- `https://nullpt.rs/reverse-engineering-tiktok-vm-1`
- `https://github.com/justscrapeme/tiktok-web-reverse-engineering`
- `https://github.com/tikvues/tiktok-api`

This page intentionally stays conservative:
- it avoids brittle claims about exact current live internals
- it treats implementation repositories as workflow and preimage-shape evidence, not proof of stable production behavior
- it keeps the focus on durable analyst leverage points

## 12. Topic summary
TikTok web signature analysis is a practical browser workflow where the real task is not simply generating `X-Bogus`, but tracing how a concrete request role, canonical request data, `msToken`/session state, and browser runtime inputs become a request that actually returns data.

It matters because analysts often stop at “I found the signer,” while the more useful answer is “this request wrapper finalizes here, these sibling states matter too, this is the structured preimage, and this is where a replay starts to degrade.”