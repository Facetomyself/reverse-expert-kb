# Kasada `X-KPSDK-*` Request-Attachment Workflow Note

Topic class: concrete target-family workflow note
Ontology layers: browser-runtime subdomain, protected-request workflow, request-boundary methodology
Maturity: structured-practical
Related pages:
- topics/browser-side-risk-control-and-captcha-workflows.md
- topics/browser-request-finalization-backtrace-workflow-note.md
- topics/browser-parameter-path-localization-workflow-note.md
- topics/browser-fingerprint-and-state-dependent-token-generation.md
- topics/browser-environment-reconstruction.md
- topics/browser-debugger-detection-and-countermeasures.md
- topics/cdp-guided-token-generation-analysis.md
- topics/datadome-geetest-kasada-workflow-note.md

## 1. Why this page exists
This page exists because the browser KB already had a broad comparison note that included Kasada, but it did **not** yet have a dedicated practical workflow page for how analysts actually approach a Kasada-protected browser target.

That gap matters.
Kasada is not especially well-served by generic “captcha” framing because the recurring practical object is often not a visible widget lifecycle.
It is more often a workflow shaped like:

```text
client SDK / challenge script load
  -> browser/runtime inspection + invisible challenge / PoW path
  -> request-role-specific `X-KPSDK-*` field attachment
  -> accepted or blocked server behavior
```

The useful analyst question is usually not:
- what abstract anti-bot category is this?

It is:
- which request role actually carries the Kasada-controlled fields?
- where are `X-KPSDK-*` values attached right before dispatch?
- which script or challenge transition must happen first?
- what structured object exists one layer before headers/body are flattened?
- why does copied visible state fail when replayed outside the browser or after challenge freshness drifts?

This page is therefore a concrete target-family workflow note rather than a generic vendor overview.

## 2. Target pattern / scenario
A representative Kasada browser path looks like this:

```text
page/bootstrap request
  -> client script / SDK loads (`p.js`, `ips.js`, or equivalent deployment-specific path)
  -> browser/device/runtime inspection runs
  -> invisible challenge / proof-of-work or trust-state update may occur
  -> protected request role is prepared
  -> `X-KPSDK-*` fields and related state are attached near dispatch
  -> server accepts, blocks, or escalates challenge behavior
```

Representative browser-visible signs include:
- custom headers such as `X-KPSDK-Ct` and sibling `X-KPSDK-*` fields
- challenge or SDK script names like `p.js` / `ips.js`
- cookies such as `kas.js`, `kas_challenge`, or related `_kas*` state
- a target that may have no obvious user-visible CAPTCHA while still enforcing strong browser/runtime validation

Common analyst situations:
- a request carries `X-KPSDK-*` headers, but the analyst has not yet found the real producer path
- copied headers/cookies fail in replay even though they look structurally correct
- the page appears mostly normal, yet one API/navigation request is consistently blocked without the right challenge/bootstrap sequence
- deobfuscation effort balloons because the client bundle is virtualized or noisy before one request role has been anchored

## 3. Analyst goal
The goal is not “understand the whole obfuscated client.”
The goal is to recover a bounded path such as:

```text
challenge/SDK bootstrap
  -> structured browser state / challenge result
  -> token/header attachment helper
  -> protected request role
```

A useful output from this workflow looks like:

```text
GET /api/search is the first protected request role
  -> after `p.js` loads and challenge state is fresh, request builder injects `X-KPSDK-Ct` and sibling fields
  -> one frame earlier, a helper combines request context + browser state + challenge output
  -> replay with copied headers fails when the browser never executed the fresh challenge/bootstrap path
```

That is much more useful than either:
- “Kasada uses PoW and fingerprinting,” or
- “I saw `X-KPSDK-Ct` once in DevTools.”

## 4. The first four questions to answer
Before broad devirtualization, answer these:

1. **Which exact request role is the first protected consumer of Kasada-controlled state?**
2. **Which script/load transition or challenge edge must happen before that request carries `X-KPSDK-*` fields?**
3. **At what stage are the meaningful inputs still structured rather than flattened into opaque headers/body fragments?**
4. **Is failure first visible in local execution, challenge freshness, request contract, or remote server treatment?**

These questions keep the case anchored to operational leverage instead of code volume.

## 5. Concrete workflow

### Step 1: identify the protected request role
Start from the network timeline and find the first request whose outcome changes under Kasada protection.

Record:
- endpoint and method
- whether it is page navigation, API fetch, login step, search/listing request, or another role
- whether `X-KPSDK-*` fields appear on that request or only on a precursor request
- whether the request is blocked on cold session, accepted on warm session, or refreshed only after a challenge/bootstrap edge

Useful scratch output:

```text
run A:
  bootstrap loads
  SDK script loads
  GET /api/search has `X-KPSDK-*`
  accepted

run B:
  copied cookies only
  GET /api/search missing or malformed `X-KPSDK-*`
  blocked
```

### Step 2: anchor the script / challenge bootstrap edge
Once the protected request role is known, identify what must happen before it.

Common anchors:
- script loads such as `p.js`, `ips.js`, or deployment-specific Kasada client paths
- invisible challenge / proof-of-work response boundaries
- state/cookie updates such as `kas.js`, `kas_challenge`, or related `_kas*` material
- early bootstrap API calls that refresh trust or challenge state before the protected request fires

Record:
- whether the bootstrap edge happens on first load, retry, or only after a server rejection
- whether it updates cookies, local state, or only in-memory request context
- whether the protected request can fire before bootstrap completes

### Step 3: hook the final `X-KPSDK-*` attachment boundary
This is usually the highest-yield first breakpoint family.
Do not start by cleaning the whole bundle.
Trap the request right before it goes on the wire.

High-yield surfaces:
- custom request wrapper
- final `fetch` / XHR boundary
- header merge helper
- serializer that produces final request headers/body pair

What to inspect:
- which `X-KPSDK-*` fields are attached at the last moment
- what request context object is still available one frame earlier
- whether challenge or session objects are passed down separately
- whether the request role changes which helper path is used

Representative sketch:
```javascript
// sketch only
const origFetch = window.fetch;
window.fetch = async function(input, init) {
  const headers = init && init.headers;
  const text = JSON.stringify(headers || {});
  if (text.includes('X-KPSDK') || String(input).includes('/api/')) {
    console.log('kasada-request-boundary', { input, init });
    debugger;
  }
  return origFetch.apply(this, arguments);
};
```

### Step 4: move one layer earlier and capture the structured preimage
The final request boundary is useful, but many fields are already too flattened there.
The next move is often one frame upward into the helper that still has:
- request role
- browser/runtime state object
- challenge or freshness state
- counters, nonces, or timestamps before final packing

This is often the best leverage point for later compare-runs or bounded harness work.

Representative recording template:

```text
request role:
  GET /api/search

final attachment:
  request builder adds `X-KPSDK-Ct` + sibling fields

one layer earlier:
  helper takes requestCtx + challengeState + browserState

challenge dependency:
  values differ between fresh challenge and stale replay
```

### Step 5: compare accepted and blocked runs at the same boundaries
Use at least:
- accepted browser-native run vs blocked replayed request
- fresh bootstrap/challenge run vs stale session run
- low-intrusion observation vs heavy debugging run
- same request role across first load vs retry

At each boundary ask:
- did the same script/bootstrap edge happen?
- did the same `X-KPSDK-*` family appear?
- was the one-layer-earlier structured object still the same shape?
- where was the **first** divergence?

This is how you avoid collapsing into “the header was present, therefore the workflow is solved.”

## 6. Where to place breakpoints / hooks

### A. SDK / challenge script load edge
Use when:
- you are not yet sure which Kasada client path matters
- the protected request seems to depend on an earlier load/refresh step

Inspect:
- script URL / load order
- any bootstrap config values or app identifiers
- whether load triggers immediate state/challenge requests

### B. Final request-boundary hook
Use when:
- you know which request role matters
- you need the fastest path to the attachment helper

Inspect:
- final headers/body
- presence and timing of `X-KPSDK-*`
- stack into request-finalization helper

### C. One-layer-earlier helper
Use when:
- the final headers are already too opaque
- you need the structured preimage before flattening

Inspect:
- request context
- browser-state/fingerprint object
- challenge freshness / session material
- late-added timing or counter values

### D. Challenge or state update boundary
Use when:
- copied headers/cookies fail despite appearing correct
- you suspect challenge freshness or in-memory trust state matters

Inspect:
- cookie or local state updates
- whether challenge/PoW result is stored or only consumed transiently
- whether blocked runs skipped a refresh edge

### E. First consumer request after challenge/refresh
Use when:
- several requests carry noise, but only one really changes outcome
- you need to separate bootstrap noise from the first meaningful protected request

Inspect:
- accepted vs blocked outcome
- role of cookies vs transient headers
- whether the request contract differs structurally or only semantically

## 7. Representative code / pseudocode / harness fragments

### Request-role scratch schema
```python
# sketch only
class KasadaBoundary:
    request_role = None
    sdk_script = None
    challenge_state = None
    browser_state = None
    attached_headers = None
```

### Boundary-sequence recording template
```text
bootstrap:
  p.js loaded
  challenge state refreshed

request boundary:
  GET /api/search
  headers: X-KPSDK-Ct + siblings present

one layer earlier:
  helper(requestCtx, browserState, challengeState)

outcome:
  browser-native accepted
  copied-header replay blocked
```

### Minimal thought-model for externalization decisions
```text
browser/runtime state
  + challenge freshness
  + request role/context
  -> attachment helper
  -> final X-KPSDK-* fields
  -> protected request
```

The point is not to clone the whole browser immediately.
The point is to decide whether one verified attachment path is separable at all.

## 8. Likely failure modes

### Failure mode 1: analyst treats Kasada as just a visible captcha problem
Likely cause:
- workflow anchored on surface challenge language instead of protected request role

Next move:
- identify the first request whose outcome changes
- trace its header/body attachment boundary directly

### Failure mode 2: analyst copies `X-KPSDK-*` headers and cookies, but replay still fails
Likely cause:
- fresh challenge/bootstrap path never ran
- in-memory state or request-role-specific context omitted
- trust/browser state drift remains

Next move:
- compare browser-native accepted run against replay at bootstrap and one-layer-earlier helper boundaries

### Failure mode 3: analyst starts deep devirtualization before anchoring one request role
Likely cause:
- code volume hijacked the workflow
- no stable request boundary selected

Next move:
- return to the protected request and walk backward from final attachment

### Failure mode 4: same request shape, different server result
Likely cause:
- challenge freshness difference
- browser trust classification changed
- hidden timing/counter input changed
- observation pressure distorted execution

Next move:
- compare first divergence point, not only final header strings
- reduce intrusiveness and repeat the same boundary capture

### Failure mode 5: minimal harness reproduces some fields but not accepted behavior
Likely cause:
- structured preimage still incomplete
- request role or session prerequisites omitted
- challenge/PoW coupling is still unresolved

Next move:
- return to accepted-vs-failed compare-runs before extending the harness

## 9. Environment assumptions
This family often needs a browser-faithful path long enough to:
- load the correct SDK/client script
- complete the invisible challenge or freshness update path
- preserve transient in-memory state
- reach the protected request role with the expected context

A good practical order is usually:
1. locate the protected request role
2. localize final attachment and one-layer-earlier helper boundaries
3. determine whether challenge freshness or transient state matters
4. only then decide how much environment rebuilding is necessary

That is usually better than rebuilding the whole browser environment before one request role is understood.

## 10. What to verify next
Once the path is localized, verify:
- whether one helper dominates `X-KPSDK-*` attachment across multiple request roles or only one
- whether blocked runs skipped a specific challenge/bootstrap edge
- whether accepted vs blocked runs first diverge at script load, challenge refresh, structured preimage, or final request consumption
- whether the next best move is deeper helper tracing, quieter observation, or bounded environment reconstruction

## 11. What this page adds to the KB
This page adds a concrete browser anti-bot family note organized around how analysts actually work on Kasada-like targets:
- anchor the protected request role
- identify the SDK/challenge bootstrap edge
- trap the final `X-KPSDK-*` attachment boundary
- move one layer earlier into the structured preimage
- compare accepted and blocked runs without over-trusting copied visible headers

That is exactly the kind of practical, target-grounded material the KB needed more of.

## 12. Source footprint / evidence note
Grounding for this page comes mainly from:
- `sources/browser-runtime/2026-03-15-kasada-request-role-and-pow-workflow-notes.md`
- Kasada vendor material on client-side installation, invisible challenges, fingerprinting, proof-of-work, and code virtualization
- public practitioner/bypass material that repeatedly surfaces `X-KPSDK-*`, `p.js`, `ips.js`, and challenge/cookie anchors
- existing KB pages on request-boundary backtracing, parameter-path localization, environment reconstruction, and token-generation analysis

This page intentionally stays conservative:
- it does not claim one invariant meaning for every `X-KPSDK-*` field across all deployments
- it focuses on recurring workflow boundaries and failure-diagnosis patterns instead of undocumented internals

## 13. Topic summary
Kasada browser analysis is often best approached as a protected-request workflow problem:

```text
SDK/challenge bootstrap
  -> browser/runtime + challenge state
  -> request-role-specific `X-KPSDK-*` attachment
  -> protected request outcome
```

It matters because analysts often stall at “I saw the header” or “the site uses invisible challenges,” while the more useful answer is: this is the protected request role, this edge refreshed the relevant state, this helper attached the fields here, and this is where accepted and blocked runs first diverged.
