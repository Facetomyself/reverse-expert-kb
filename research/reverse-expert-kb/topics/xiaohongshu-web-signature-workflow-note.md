# Xiaohongshu Web Signature Workflow Note

Topic class: concrete site-specific workflow note
Ontology layers: browser-runtime subdomain, request-signature workflow, site-specific practical analysis
Maturity: structured-practical
Related pages:
- topics/bytedance-web-request-signature-workflow-note.md
- topics/browser-parameter-path-localization-workflow-note.md
- topics/browser-request-finalization-backtrace-workflow-note.md
- topics/browser-environment-reconstruction.md
- topics/browser-fingerprint-and-state-dependent-token-generation.md
- topics/browser-cdp-and-debugger-assisted-re.md
- topics/environment-differential-diagnosis-workflow-note.md

## 1. Why this page exists
This page exists because the KB already had a **family-level** browser request-signature note, but still lacked a **site-specific** practical page for one of the most frequently discussed Chinese web targets: Xiaohongshu / RED / XHS.

That gap mattered because this target is exactly the kind of case the human asked the KB to prioritize:
- real site
- real request family
- practical breakpoint and hook placement
- environment reconstruction relevance
- failure diagnosis that goes beyond “find one parameter”

Public practitioner material repeatedly centers the browser-side header family:
- `x-s`
- `x-t`
- `x-s-common`
- plus sibling cookie/session/browser state such as `a1`, `webid`, and `web_session`

The useful analyst question is usually not:
- what is the abstract taxonomy of this signature family?

It is:
- which request role actually needs the header family?
- where is the signer call boundary?
- what normalized request object is passed into signing?
- what sibling cookie/session state must match for the response to contain real data?
- is the failure a hard invalid-signature reject, or a softer success-without-data / degraded-response state?

This page therefore focuses on the XHS workflow analysts actually need.

## 2. Target pattern / scenario
A representative XHS browser path looks like:

```text
page / feed / note / comment request
  -> host-page request wrapper builds canonical request path + params
  -> wrapped signer (`window._webmsxyw` or equivalent) consumes request data
  -> headers such as `x-s`, `x-t`, `x-s-common` are inserted
  -> sibling cookie/session state (`a1`, `webid`, `web_session`, login cookie family) travels with the request
  -> server returns reject, soft-success-no-data, or real data
```

Common analyst situations:
- the request visibly carries `x-s` / `x-t`, but replay still fails
- the request returns a nominally successful shell response yet no real data
- a signing entry is found, but it is unclear which request fields are canonicalized before signing
- environment reconstruction starts sprawling because the signing path depends on browser globals/prototypes/cookie state
- one API role works while another fails because `x-s-common` or session coupling differs

## 3. Analyst goal
The goal is not merely to “recover `x-s`.”
The goal is to recover the **XHS request-signature path**:

```text
request role / canonicalized request object
  -> signer call boundary
  -> `x-s` / `x-t` / `x-s-common` insertion
  -> sibling cookie/session state
  -> first data-bearing accepted response
```

A useful output from this workflow looks like:

```text
GET /api/sns/web/v1/search/notes
  -> request wrapper normalizes query/body/path
  -> signer entry consumes canonical URL + request params
  -> headers `x-s` and `x-t` inserted here; `x-s-common` added for this role
  -> request also requires current `a1` / `web_session` context
  -> invalid signature => hard reject
  -> valid headers but stale session => success shell / empty data
```

That artifact is far more useful than a deobfuscated blob or a single captured header string.

## 4. Concrete workflow

### Step 1: anchor one concrete request role
Do not start from the whole site.
Choose one request that materially matters:
- feed fetch
- search notes
- note detail
- comments
- like / interaction request

Record:
- endpoint and method
- whether `x-s`, `x-t`, and/or `x-s-common` are present
- whether the role is anonymous or login/session-bound
- whether the response state is hard reject, soft success without data, or real accepted data

Useful scratch template:

```text
request role:
  GET /api/sns/web/v1/search/notes
header family:
  x-s, x-t, x-s-common
cookie/session family:
  a1, web_session, login cookie set
outcome:
  browser baseline -> real data
  replay -> success shell but empty data
```

### Step 2: localize the final header attachment site
The fastest win is usually the boundary where the request wrapper inserts the headers.

High-yield surfaces:
- custom request wrapper
- final `fetch` / XHR wrapper before dispatch
- helper that merges signed headers into a common header object
- code path that calls `window._webmsxyw` or an equivalent wrapped signer and then writes `x-s` / `x-t`

Why this matters:
- once the final attach site is found, the call stack often reveals the signer boundary quickly
- you can see whether the header family is emitted together or conditionally by request role
- you can distinguish true signing from later transport formatting

### Step 3: capture the signer call boundary, not just the final header string
Once the attach site is found, move one step earlier and capture:
- signer function arguments
- canonical URL / request path argument
- normalized query/body object
- any timestamp/counter argument
- cookie/session values read nearby

Representative thought model:

```text
request_ctx = {
  path,
  query,
  body,
  method,
}

state_ctx = {
  a1,
  webid,
  web_session,
  login_cookie_family,
}

runtime_ctx = {
  ua,
  ts,
  browser_checks,
}
```

For XHS, this pre-sign boundary is usually more informative than the final `x-s` text.

### Step 4: distinguish `x-s` / `x-t` success from full request success
A major trap in this family is treating a valid-looking signed request as complete success.

Use at least three buckets:
- **hard reject**: signature or contract clearly invalid
- **soft success / degraded**: response shape looks nominal, but data is empty or restricted
- **true accepted**: expected data/content returned

Why this matters:
- public practitioner material suggests `x-s` / `x-t` can be “right enough” to avoid obvious reject states while still failing because `web_session` or sibling state is stale or mismatched
- this makes XHS a strong case for distinguishing **signature correctness** from **request-context correctness**

### Step 5: map sibling state, especially `a1` and session context
At least in public practitioner/open-source material, XHS signing work repeatedly references sibling state such as:
- `a1`
- `webid`
- `web_session`
- login cookie family

Do not assume the headers stand alone.
Check:
- which cookie/state values are read before signing
- which ones merely travel with the request
- which request roles need `x-s-common`
- whether stale-but-visible state is enough to produce a nominal response but not real data

### Step 6: compare baseline browser run vs replay or harness run
Compare at the same boundaries:
- live browser run vs instrumented browser run
- live browser run vs node-side / harness replay
- fresh session vs warm session
- anonymous request role vs logged-in role

At each boundary ask:
- did the same request wrapper fire?
- did the same canonical request object reach signing?
- were the same headers inserted?
- were sibling cookie/session values the same?
- was the first divergence a hard reject or a softer empty-data state?

This keeps the analysis anchored to real behavior rather than output-string superstition.

## 5. Where to place breakpoints / hooks

### A. Request-finalization wrapper
Use when:
- you know which request role matters
- you need the fastest path to signed-header insertion

Inspect:
- final URL/body/header object
- whether `x-s`, `x-t`, and `x-s-common` are inserted together
- whether insertion depends on request role or login state

### B. Signer call boundary (`window._webmsxyw` or equivalent)
Use when:
- practitioner evidence points to a browser-exposed signer entry
- you want the canonical request preimage instead of only the final headers

Inspect:
- raw arguments
- whether one argument is the canonicalized request path/URL
- whether state/timestamp args are supplied alongside request data

Representative sketch:
```javascript
// sketch only
const orig = window._webmsxyw;
window._webmsxyw = function() {
  console.log('xhs signer args', arguments);
  debugger;
  return orig.apply(this, arguments);
};
```

### C. Cookie/state read boundary
Use when:
- headers look correct but responses are degraded
- you suspect `a1` / `web_session` / related state drift

Inspect:
- where `a1` is sourced
- whether `webid` is derived or read
- where `web_session` or sibling session state enters the request path

### D. First response classifier
Use when:
- you need to distinguish hard reject from soft success without data

Inspect:
- response JSON fields or status differences
- whether the request is accepted structurally but functionally degraded
- whether one role succeeds while another remains empty

### E. Environment reconstruction edge
Use when:
- browser-side signing logic is being externalized
- replay in Node or another harness produces headers but wrong outcomes

Inspect:
- browser globals/prototypes/storage reads near signer call
- whether environment checks only gate execution or also feed the signature/state
- whether request success degrades only after externalization

## 6. Representative code / pseudocode / harness fragments

### Signed-header capture sketch
```javascript
// sketch only
const origFetch = window.fetch;
window.fetch = async function(input, init) {
  console.log('xhs request', { input, init });
  debugger;
  return origFetch.apply(this, arguments);
};
```

### Field-family recording template
```text
request role:
  GET /api/sns/web/v1/search/notes

header family:
  x-s, x-t, x-s-common

sibling state:
  a1, webid, web_session

signer boundary:
  requestWrapper -> signerCall(canonicalRequest, stateCtx)

outcome:
  browser baseline -> data returned
  replay -> response success but empty items
```

### Minimal harness thought model
```python
# sketch only
class RequestCtx:
    path = None
    query = None
    body = None
    method = None

class StateCtx:
    a1 = None
    webid = None
    web_session = None

class RuntimeCtx:
    ua = None
    ts = None
    browser_reads = None


def collect_xhs_presign(request_ctx, state_ctx, runtime_ctx):
    return {
        "path": request_ctx.path,
        "query": request_ctx.query,
        "body": request_ctx.body,
        "method": request_ctx.method,
        "a1": state_ctx.a1,
        "webid": state_ctx.webid,
        "web_session": state_ctx.web_session,
        "ua": runtime_ctx.ua,
        "ts": runtime_ctx.ts,
    }
```

The point is not to clone the whole site immediately.
The point is to test whether the signing boundary and sibling state can be separated cleanly.

## 7. Likely failure modes

### Failure mode 1: analyst focuses only on `x-s`
Likely cause:
- field-only thinking
- `x-t`, `x-s-common`, `a1`, or session state ignored

Next move:
- map the full header family and adjacent cookie/session reads around the signer boundary

### Failure mode 2: valid-looking request yields empty data
Likely cause:
- stale `web_session`
- wrong anonymous vs login state
- request role requires additional sibling state
- headers are correct enough for nominal success but not enough for real data return

Next move:
- explicitly classify this as **soft success / degraded**, not full success
- compare cookie/session family against baseline browser run

### Failure mode 3: environment patching grows without bound
Likely cause:
- replay/harness effort started before the request-signing path was bounded
- environment checks and signature inputs not separated

Next move:
- return to live request wrapper and signer boundary
- capture actual environment reads before adding more patches

### Failure mode 4: one API role works, another fails
Likely cause:
- role-specific canonicalization
- `x-s-common` needed only for some roles
- different cookie/session contract for search/feed/detail/interaction requests

Next move:
- compare the attach sites and signer arguments across roles
- treat request role as a first-class input, not as interchangeable traffic

### Failure mode 5: static deobfuscation takes over the workflow
Likely cause:
- wrapped/VMP-like code made the analyst chase structure before stabilizing the request boundary

Next move:
- return to one concrete request and the signer call edge
- use deobfuscation only after the operational path is known

## 8. Environment assumptions
XHS is a good example of a browser signature target where the right default assumption is:
- preserve realistic cookie/session/browser state long enough to localize the request path
- capture browser reads near signing
- separate hard rejects from empty-data soft accepts
- only then decide how much environment reconstruction is truly necessary

This is usually better than immediately trying to fully rehost the site in Node.

## 9. What to verify next
Once the path is localized, verify:
- which request roles emit `x-s-common`
- whether one signer entry handles all roles or multiple wrappers exist
- whether `a1` / `web_session` are merely transported or are direct signing inputs
- whether the first divergence between baseline and replay is header generation, session state, or response classification
- whether a minimal harness can reproduce not just headers, but a real data-bearing response under preserved state assumptions

## 10. What this page adds to the KB
This page adds exactly the kind of concrete, target-grounded note the KB needed more of:
- a real site rather than only a signature-family abstraction
- request-role-first analysis
- signer-boundary localization
- sibling cookie/session-state diagnosis
- explicit modeling of **success-without-data** as a distinct failure/diagnosis mode

That makes it more operational than another taxonomy page.

## 11. Source footprint / evidence note
Grounding for this page comes from:
- `sources/browser-runtime/2026-03-15-xiaohongshu-web-signature-workflow-notes.md`
- `sources/browser-runtime/2026-03-14-bytedance-web-signature-family-notes.md`
- open-source repositories such as `jobsonlook/xhs-mcp` and `wei168hua/xhs-xs-xt`
- practitioner material surfaced via search-layer, including readable Juejin excerpts around `window._webmsxyw`, `x-s`, `x-t`, `x-s-common`, `a1`, and `web_session`

This page intentionally stays conservative:
- it does not claim stable undocumented internals across XHS versions
- it focuses on workflow boundaries, request roles, and failure diagnosis patterns that appear more durable than specific algorithm details

## 12. Topic summary
Xiaohongshu web signature analysis is a practical browser workflow where the real task is not simply generating `x-s`, but tracing how a request role, a signer boundary, and sibling cookie/session state together produce a request that returns real data rather than just avoiding an obvious reject.

It matters because analysts often stop at “the headers look right,” while the more useful answer is “this request wrapper signs here, these sibling states also matter, this role needs this header family, and this is where a soft-success empty-data response begins to diverge from a real accepted run.”
