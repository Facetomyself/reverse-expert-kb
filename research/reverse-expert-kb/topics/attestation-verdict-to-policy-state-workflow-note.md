# Attestation Verdict to Policy-State Workflow Note

Topic class: concrete workflow note
Ontology layers: mobile-practice branch, attestation/result interpretation, policy-state transition methodology
Maturity: structured-practical
Related pages:
- topics/mobile-response-consumer-localization-workflow-note.md
- topics/mobile-challenge-and-verification-loop-analysis.md
- topics/mobile-risk-control-and-device-fingerprint-analysis.md
- topics/environment-differential-diagnosis-workflow-note.md
- topics/android-network-trust-and-pinning-localization-workflow-note.md
- topics/protocol-state-and-message-recovery.md

## 1. Why this page exists
This page exists because many Android reversing cases now stall at a specific middle layer:
- the app clearly performs device/app integrity or attestation work
- the analyst can often see token acquisition, attestation API usage, or backend verification traffic
- but the first local branch that turns the verdict into **allow / degrade / retry / block / challenge** is still unclear

In practice, the hard part is often not:
- finding the attestation API call
- recognizing that a Play Integrity / key attestation / device-verdict family is present
- or proving that a server verification step exists

The hard part is usually this narrower path:

```text
attestation request or token acquisition
  -> verdict material or verification response arrives
  -> decode / normalize / map result codes
  -> local policy state or gate is selected
  -> retry / fallback / challenge / reduced-mode / allow path fires
```

Analysts often stop too early at the first visible attestation callback or backend response parser.
This page exists to make the next step explicit:
**localize the first behavior-changing verdict-to-policy transition.**

## 2. Target pattern / scenario
### Representative target shape
A recurring Android pattern looks like:

```text
protected action requested
  -> app requests integrity token / attestation material
  -> app forwards token or request blob for verification
  -> backend or platform returns a verdict / result category / error
  -> app maps verdict into local business or risk state
  -> app allows, retries, downgrades, blocks, or escalates challenge
```

Common analyst situations:
- the attestation or verdict callback is visible, but the real gating branch is not
- several booleans, enums, or result codes appear after verification and it is unclear which one matters
- the app seems to keep running, but later API behavior changes without an obvious local branch
- retry logic and trust-policy logic are interleaved and easy to confuse
- the same protected action behaves differently across device state, packaging, or session conditions even though the attestation family is already known

### Analyst goal
The practical goal is one or more of:
- identify the first local consumer that turns verdict material into a meaningful policy state
- separate verdict mapping from transient retry/error handling
- determine whether the consequence is allow, degrade, challenge, block, or delayed retry
- prove which state write, gate, or scheduler actually changes later behavior
- route cleanly into challenge-loop, environment-differential, or deeper mobile risk-control analysis

## 3. The first five questions to answer
Before hooking every attestation callback, answer these:

1. **What exact user action or protected request causes the attestation path to run?**
2. **Where does verdict material first become structured enough to compare across runs?**
3. **Which local helper maps raw verdict labels / result codes into business or risk categories?**
4. **What is the first state write, gate decision, or scheduler action after that mapping?**
5. **What later consequence proves that this branch mattered?**

These questions keep the work consequence-driven instead of API-driven.

## 4. Practical workflow

### Step 1: anchor one protected action and one downstream consequence
Do not reason about all attestation usage in the app.
Pick one protected action whose later consequence is visible.

High-value downstream consequences include:
- request allowed vs blocked
- limited-mode / degraded-mode entry
- login refresh or device rebind forced
- retry/backoff path triggered
- captcha / challenge branch triggered
- server-side protected endpoint family changes behavior

Scratch note template:

```text
protected action:
  submit transfer

visible attestation family:
  integrity token requested before submit

later consequence:
  same request family becomes challenge_required on altered device

initial question:
  which local policy state changed between verdict handling and challenge_required?
```

### Step 2: separate four attestation-side boundaries
Keep these boundaries distinct.
That is the core discipline of this page.

#### Boundary A: request / token acquisition
Examples:
- integrity-token request builder
- platform/service callback registration
- native helper that prepares attestation blob

#### Boundary B: verdict or verification-response decode
Examples:
- backend verification response parser
- decrypted/decoded verdict object
- result wrapper built from raw fields

#### Boundary C: local policy mapping
Examples:
- enum mapping helper
- boolean/label-to-state conversion
- risk-tier or gate-category selection
- error-class vs policy-class split

#### Boundary D: first behavior-changing consumer
Examples:
- feature gate
- controller state write
- retry scheduler
- challenge trigger
- downstream request dispatcher

A lot of wasted effort comes from stopping at B when the meaningful branch lives at C or D.

### Step 3: find the earliest stable structured verdict object
If the attestation path is still opaque, first localize the earliest point where verdict material becomes structured.
This might be:
- a backend verification response model
- a decoded object with booleans/enums/labels
- a repository callback carrying a verification result
- a wrapper that combines verdict and error state

Why this matters:
- it gives you stable fields to compare across runs
- it reveals whether the app is branching on trust labels, on transient error classes, or both
- it gives you consumer edges to follow without overfitting to transport details

Representative shape:

```text
verifyIntegrityResponse(...)
  -> VerificationResult(verdict, errorCode, retryable)
  -> mapVerdictToPolicy(...)
  -> policyState = REQUIRE_CHALLENGE
  -> challenge bootstrap request enqueued
```

### Step 4: split verdict mapping from retry/fallback mapping
This is the most important practical distinction for this family.

Many attestation-heavy apps mix together:
- trust verdict interpretation
- transient service failure handling
- backoff or retry scheduling
- fallback to reduced or challenge mode

Keep them separate.

Useful role labels:
- **verdict mapping** — turns trust labels / booleans / categories into policy
- **error mapping** — classifies service/network/platform failures
- **retry mapping** — decides transient retry/backoff behavior
- **business gate mapping** — decides allow / block / limited-mode / challenge

If you collapse these together, a retry scheduler can look like a trust-policy branch and waste hours.

### Step 5: localize the first policy-state write or gate decision
Once mapping helpers are visible, find the first consumer that actually changes app behavior.
Useful targets include:
- state repositories or managers
- controller flags
- challenge-needed booleans
- reduced-privilege mode writes
- feature-enable / feature-disable gates
- schedulers that only run after a bad or ambiguous verdict

Representative artifact:

```text
verification result received
  -> mapVerdictToPolicy() returns DEVICE_UNTRUSTED
  -> riskController.setMode(CHALLENGE_REQUIRED)
  -> transfer flow redirected to verification bootstrap
```

That `setMode(CHALLENGE_REQUIRED)` step is usually more valuable than the raw verdict callback.

### Step 6: prove consequence, not just reachability
A hook firing is not enough.
You still need to prove the branch mattered.

Useful proof points:
- state changes immediately before a later challenge or block
- a request scheduler fires only for one policy category
- accepted vs challenged runs differ at the same state write
- the same verdict family reaches multiple consumers, but only one predicts later behavior

A good minimal proof chain looks like:

```text
structured verdict differs or maps differently
  -> policy state / gate differs
  -> later request or flow consequence differs
```

## 5. Where to place breakpoints / hooks

### A. Attestation request / token-acquisition boundary
Use when:
- you still need to anchor the family to one protected action
- you need the earliest proof that this action really triggers attestation

Inspect:
- which protected action triggers it
- whether multiple request families share the same token path
- whether the app already carries policy state into the request stage

### B. Verification-response / verdict-object boundary
Use when:
- the family is known, but the verdict is still opaque
- you need the first structured result object

Inspect:
- verdict labels / booleans / enums
- transient error or retry flags
- whether the response already includes a policy-like category

Representative sketch:
```javascript
// sketch only
Java.perform(function () {
  const Result = Java.use('com.example.security.VerificationResult');
  Result.$init.overloads.forEach(function (ov) {
    ov.implementation = function () {
      const out = ov.apply(this, arguments);
      console.log('VerificationResult created', out);
      return out;
    };
  });
});
```

### C. Verdict-to-policy mapping helper
Use when:
- result objects are visible but still too low-level
- multiple booleans/codes exist and you need the app’s own reduction step

Inspect:
- enum conversions
- boolean aggregation
- mapping into business/risk states
- whether retryable/fatal/service-error classification is mixed into the same helper

### D. State-write / gate boundary
Use when:
- the app is clearly stateful
- you need the first local effect that predicts later behavior

Inspect:
- `setMode(...)`, `updateRiskState(...)`, `setRequiresVerification(...)`
- feature gate booleans
- account/session flags
- degraded-mode / safe-mode / rebind-required writes

### E. Retry / scheduler boundary
Use when:
- the app keeps delaying or re-running the action
- it is unclear whether the path reflects policy denial or transient retry

Inspect:
- backoff timers
- retry counters
- fallback-mode entry
- whether the scheduler outcome is tied to error class or verdict class

## 6. Representative code / pseudocode / harness fragments

### Verdict-to-policy recording template
```text
protected action:
  submit payment

attestation family:
  integrity token -> backend verify

structured verdict object:
  fields / enums / booleans observed

mapping helper:
  verdict/error -> policy category

first behavior-changing consumer:
  state write / gate / retry scheduler / challenge trigger

proof of consequence:
  later request family / challenge / allow-block difference
```

### Minimal thought model
```python
# sketch only
class VerdictPath:
    action = None
    structured_verdict = None
    mapping_helper = None
    policy_state = None
    first_consumer = None
    consequence = None
```

The point is to keep the path from verdict material to behavior explicit.

## 7. Likely failure modes

### Failure mode 1: analyst proves attestation API use but still cannot explain gating
Likely causes:
- stopping at token acquisition or raw callback visibility
- the decisive branch lives in verdict mapping or a later state write

Next move:
- move forward to the first structured verdict object and the first mapping helper

### Failure mode 2: analyst mistakes retry logic for trust-policy logic
Likely causes:
- transient errors and policy categories are mixed in the same code region
- only scheduler behavior was observed, not mapping inputs

Next move:
- separate verdict mapping, error mapping, and retry mapping explicitly

### Failure mode 3: similar verdicts appear, but later behavior still differs
Likely causes:
- the app maps sibling fields or local context together
- session/device/package state alters the mapping result
- the decisive difference is in a later policy-state consumer

Next move:
- compare runs at the mapping-helper and state-write boundaries, not only at verdict-object creation

### Failure mode 4: analyst jumps straight from attestation family to final blocked request
Likely causes:
- the middle layer of local policy-state transition was skipped
- state repository or gate object was never localized

Next move:
- insert verdict-to-policy localization between attestation-family anchoring and request/challenge consequence analysis

### Failure mode 5: all trust problems are misread as local-only
Likely causes:
- backend verification outcome is only partially visible locally
- local state is a projection of a larger server-side decision

Next move:
- keep claims conservative and prove only the local mapping and first observed consequence

## 8. Environment assumptions
In attestation-heavy Android cases, these ownership layers are often different:
1. attestation request ownership
2. verification response ownership
3. verdict-to-policy mapping ownership
4. later consequence ownership

This page focuses on layers 2 through 4.
That is usually where the useful explanation reappears once the family is already known.

## 9. What to verify next
Once the first policy-state consumer is localized, verify:
- whether the next bottleneck is challenge-loop analysis, device-trust differential diagnosis, or request-family consequence tracing
- whether retry/fallback branches are independent from trust-policy branches
- whether the same mapping helper feeds multiple protected actions
- whether the app’s local state is enough to explain later behavior or only partially explains it

## 10. How this page connects to the rest of the KB
Use this page when the bottleneck is **turning known attestation/verdict material into a known local behavior-changing state**.
Then route forward based on what you find:

- if the earlier bottleneck is response parsing and first meaningful consumer in a broader sense:
  - `topics/mobile-response-consumer-localization-workflow-note.md`
- if the next bottleneck is challenge escalation or loop transitions:
  - `topics/mobile-challenge-trigger-and-loop-slice-workflow-note.md`
- if the next bottleneck is device/package/session drift changing verdict interpretation:
  - `topics/environment-differential-diagnosis-workflow-note.md`
- if the main issue is broader mobile risk / fingerprint workflow reconstruction:
  - `topics/mobile-risk-control-and-device-fingerprint-analysis.md`
- if the trust path is still blocked before useful verdict handling is visible:
  - `topics/android-network-trust-and-pinning-localization-workflow-note.md`

This page is meant to sit between attestation-family recognition and deeper consequence modeling.

## 11. What this page adds to the KB
This page adds grounded practical material the mobile subtree needed more of:
- a concrete middle-layer workflow for attestation-heavy targets
- explicit separation of request/token acquisition, verdict decode, policy mapping, and first consumer
- practical hook placement around verdict objects, mapping helpers, state writes, and retry schedulers
- a clear distinction between trust-policy logic and transient retry/fallback logic
- consequence-driven proof rules for verdict-heavy Android paths

It is intentionally closer to how analysts regain traction in real attestation-heavy apps than to a generic Play Integrity overview.

## 12. Source footprint / evidence note
Grounding for this page comes mainly from:
- `sources/mobile-runtime-instrumentation/2026-03-15-attestation-verdict-to-policy-state-notes.md`
- Android Developers material surfaced through search-layer on Play Integrity verdicts and error/retry concepts
- practical Android attestation / Key Attestation abuse discussions used conservatively as support for why API visibility is not equivalent to policy consequence
- existing KB pages on response-consumer localization, challenge loops, and environment-differential diagnosis

This page intentionally stays conservative:
- it does not claim one universal internal shape for Play Integrity or all attestation systems
- it does not assume local code fully explains server-side trust decisions
- it focuses on the local transition from structured verdict material to first observed policy consequence

## 13. Topic summary
Attestation verdict to policy-state localization is a practical workflow for Android cases where an integrity / attestation family is already visible, but the first branch that turns verdict material into allow, degrade, retry, block, or challenge behavior is still hidden.

It matters because many analysts can find the attestation path and still not explain the app’s next move. The faster route is usually to separate verdict decode from policy mapping, separate policy mapping from retry handling, and prove consequence at the first state write or gate that actually predicts later behavior.
