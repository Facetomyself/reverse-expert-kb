# Result-Code and Enum-to-Policy Mapping Workflow Note

Topic class: concrete workflow note
Ontology layers: mobile-practice branch, response/result interpretation, code-to-policy reduction methodology
Maturity: structured-practical
Related pages:
- topics/mobile-response-consumer-localization-workflow-note.md
- topics/attestation-verdict-to-policy-state-workflow-note.md
- topics/mobile-challenge-trigger-and-loop-slice-workflow-note.md
- topics/environment-differential-diagnosis-workflow-note.md
- topics/protocol-state-and-message-recovery.md

## 1. Why this page exists
This page exists because many mobile reversing cases stall one step after a useful parser or callback hook.

The analyst can already see:
- a parsed response object
- an attestation or challenge callback
- one or more result codes / enums / booleans
- maybe even a generated protobuf or JSON model

But the app’s real next move is still unclear.
The missing layer is often this narrower reduction path:

```text
parsed response / verdict object
  -> raw result codes / enums / sibling flags visible
  -> helper reduces them into fewer policy buckets
  -> switch / ordinal map / branch selects a policy category
  -> state write / scheduler / gate makes the category operational
  -> later allow / retry / degrade / challenge / block consequence appears
```

Analysts often stop too early at “I can see the code field now.”
This page exists to make the next step explicit:
**localize the first reduction from visible result codes into a behavior-changing local policy state.**

## 2. Target pattern / scenario
### Representative target shape
A recurring Android/mobile path looks like:

```text
request or protected action
  -> response / verdict object built
  -> fields like status, code, type, mode, reason, or enum become visible
  -> helper maps combinations of fields into fewer business/risk categories
  -> branch / switch / state update selects what happens next
  -> app retries, downgrades, challenges, blocks, or proceeds
```

Common analyst situations:
- one integer or enum is clearly visible, but many later branches still exist
- decompiled Java output looks flattened or misleading around the decisive switch
- several sibling fields appear, and it is unclear which one is truly policy-driving
- retry/error classification and trust/policy classification are mixed together
- compare-runs show similar visible codes but different downstream behavior

### Analyst goal
The practical goal is one or more of:
- identify the first helper that reduces raw codes/enums into a smaller local policy space
- distinguish raw code visibility from meaningful policy-state visibility
- reconstruct the branch boundary even when JADX output is flattened or misleading
- prove which state write, gate, or scheduler actually operationalizes the mapping
- route cleanly into challenge-loop, attestation, or environment-differential analysis

## 3. The first five questions to answer
Before tracing every getter and callback, answer these:

1. **Which specific action or request family produces the result code or enum of interest?**
2. **Where does that code first become stable enough to compare across runs?**
3. **Is the app branching directly on the raw code, or on a reduced category built from several fields?**
4. **Does the decisive mapping live in decompiled Java/Kotlin, smali switch code, or a later state controller?**
5. **What later consequence proves that the mapping mattered?**

These questions keep the work consequence-driven instead of field-driven.

## 4. Practical workflow

### Step 1: anchor one code family and one consequence
Do not chase every visible integer.
Pick one code family that clearly precedes a meaningful later effect.

High-value downstream consequences include:
- request allowed vs challenged
- silent retry vs hard block
- reduced mode / degraded feature set
- extra verification bootstrap
- forced session refresh or rebind

Scratch note template:

```text
protected action:
  submit order

visible result fields:
  code=17, type=TEMP_FAIL, retryable=true

visible later consequence:
  app enters challenge_pending instead of immediate retry on altered device

question:
  which local helper reduced these fields into CHALLENGE_PENDING?
```

### Step 2: separate four boundaries
Keep these boundaries distinct.
That is the main discipline of this page.

#### Boundary A: raw code visibility
Examples:
- parsed protobuf enum field
- JSON `status` / `reason` / `mode`
- callback parameter carrying an int or enum

#### Boundary B: code normalization
Examples:
- raw service codes mapped into app-local constants
- enum ordinal or synthetic switch array used to normalize branching
- multiple booleans collapsed into one category helper

#### Boundary C: policy mapping
Examples:
- `mapCodeToPolicy(...)`
- `toRiskMode(...)`
- `resolveChallengeState(...)`
- error-vs-policy split helper

#### Boundary D: first behavior-changing consumer
Examples:
- `setMode(...)`
- `setRequiresChallenge(...)`
- retry/backoff scheduler
- feature gate / route redirect
- follow-up request dispatcher

A lot of wasted effort comes from stopping at A or B when the meaningful branch lives at C or D.

### Step 3: find the reduction helper, not just the raw field
Once one code field is visible, ask whether the app is still reducing it further.
Often it is.

Common reduction shapes:
- multiple raw codes collapsed into `ALLOW`, `RETRY`, `CHALLENGE`, `BLOCK`
- error and verdict fields combined into one local mode
- service-specific enums converted into app-specific enums
- nullable or missing fields normalized into fallback states

Representative shape:

```text
VerificationResult(code, retryable, riskLabel)
  -> normalizeCode(...)
  -> mapToPolicyBucket(...)
  -> policy = REQUIRE_CHALLENGE
  -> stateController.setMode(policy)
```

That `mapToPolicyBucket(...)` step is usually more valuable than the first visible `code` field.

### Step 4: reconstruct switch ownership when decompiler output lies
If JADX output looks suspiciously flat or synthetic, move down one level.

Useful things to inspect:
- `packed-switch`
- `sparse-switch`
- synthetic ordinal-mapping arrays for enums
- helper methods that convert service enums before the switch
- Kotlin/Java compiler-generated wrappers that hide the real branch owner

Practical rule:
- if you can see the field but cannot explain the branch, the next move is often **switch reconstruction**, not more parser hooks

### Step 5: separate policy mapping from retry/error mapping
This split matters a lot.
Many real paths mix together:
- service/network error classes
- trust/risk verdict classes
- retry eligibility
- final business gate selection

Useful role labels:
- **raw result code** — direct value from parser/callback
- **normalized code** — app-local version of the value
- **policy bucket** — allow / retry / challenge / degrade / block class
- **scheduler decision** — when/how to reattempt or continue
- **business gate** — what the app actually allows or denies

If these are collapsed together, a retry helper can look like a policy branch and waste hours.

### Step 6: localize the first operational state write or scheduler
Once the mapping helper is visible, find the first consumer that actually changes behavior.

Useful targets include:
- risk or challenge state controllers
- `setMode(...)`, `updateState(...)`, `setNextAction(...)`
- retry/backoff managers
- request dispatchers
- feature gates and route selectors

Representative artifact:

```text
result object observed
  -> mapToPolicyBucket() returns RETRY_LATER
  -> backoffManager.schedule(30s)
```

or:

```text
result object observed
  -> mapToPolicyBucket() returns CHALLENGE_REQUIRED
  -> flowState.setRequiresChallenge(true)
  -> challenge bootstrap request emitted
```

The first operational write or scheduler step is usually where the analysis becomes explainable.

### Step 7: prove consequence, not just branch reachability
A hook firing on the mapping helper is not enough.
You still need to prove the branch mattered.

Useful proof points:
- the same action maps to different policy buckets across compare-runs
- only one bucket predicts a later challenge or retry family
- the state write changes immediately before a visible flow transition
- the scheduler only fires for one mapped outcome

A good minimal proof chain looks like:

```text
raw code / sibling field pattern differs
  -> policy bucket differs
  -> state write or scheduler differs
  -> later request or flow consequence differs
```

## 5. Where to place breakpoints / hooks

### A. Parsed object / getter boundary
Use when:
- you need to confirm which raw code or enum fields are actually present
- field names are available but their operational meaning is not

Inspect:
- field combinations, not just one favorite field
- whether multiple code families coexist in the same object
- whether fields vary across compare-runs

### B. Normalization helper boundary
Use when:
- raw fields are visible but too low-level
- service-specific names are converted into app-local constants or enums

Inspect:
- argument combinations
- whether missing/null values are normalized into fallback categories
- whether enum ordinal handling is synthetic or explicit

### C. Switch / branch boundary
Use when:
- decompiler output looks flattened, synthetic, or implausibly simple
- you need to reconstruct branch ownership

Inspect:
- `packed-switch` / `sparse-switch`
- synthetic enum-switch arrays
- helper methods that feed the switch
- which case labels actually lead to state changes

### D. State-write / gate boundary
Use when:
- you need the first local effect that predicts later behavior
- several branches exist but only one becomes operational

Inspect:
- mode flags
- challenge-required booleans
- retry counters / timers
- route selectors / follow-up request triggers

### E. Scheduler / follow-up request boundary
Use when:
- the mapping helper is visible, but the real consequence is delayed or async
- you need to distinguish retry from challenge or degrade behavior

Inspect:
- enqueue / post / delay helpers
- request-family selection
- timing differences across policy buckets

## 6. Representative code / pseudocode / harness fragments

### Mapping-recording template
```text
protected action:
  ...

raw result fields:
  code / enum / type / retryable / sibling flags

normalization helper:
  ...

policy mapping helper:
  ...

first operational consumer:
  state write / scheduler / gate

proof of consequence:
  later request / challenge / allow-block difference
```

### Minimal thought model
```python
# sketch only
class ResultMappingPath:
    raw_fields = None
    normalized_code = None
    policy_bucket = None
    first_consumer = None
    consequence = None
```

The point is to keep the reduction from raw fields to behavior explicit.

## 7. Likely failure modes

### Failure mode 1: analyst sees the code but not the meaning
Likely causes:
- stopping at parsed field visibility
- later reduction helper collapses several values into one local policy bucket

Next move:
- find the normalization or mapping helper that consumes the raw code

### Failure mode 2: decompiler output looks clean, but the branch explanation is wrong
Likely causes:
- enum lowering or synthetic switch arrays hide the real ownership
- only high-level decompiler output was inspected

Next move:
- reconstruct the switch boundary in smali / bytecode-level view

### Failure mode 3: retry behavior is mistaken for policy behavior
Likely causes:
- error class, retry eligibility, and policy bucket were mixed together
- only one downstream consumer was hooked

Next move:
- separate raw code, normalized code, policy bucket, and scheduler decision explicitly

### Failure mode 4: same visible code, different downstream behavior
Likely causes:
- sibling fields or local state participate in the reduction
- the decisive branch is later than the first visible code consumer

Next move:
- compare runs at the mapping-helper and state-write boundaries, not only at raw field visibility

### Failure mode 5: analyst jumps from parsed object straight to UI or blocked request
Likely causes:
- operational middle layer was skipped
- first policy-state or scheduler consumer was never localized

Next move:
- insert result-code / enum-to-policy mapping localization between response parsing and final consequence analysis

## 8. Environment assumptions
In many mobile cases, these ownership layers are different:
1. parsed object ownership
2. raw field visibility
3. normalization / mapping ownership
4. state or scheduler ownership
5. final consequence ownership

This page focuses on layers 2 through 4.
That is usually where the explanation becomes usable.

## 9. What to verify next
Once the first operational mapping is localized, verify:
- whether the same helper feeds multiple protected actions
- whether sibling fields or preexisting state change the final bucket
- whether the next bottleneck is challenge-loop analysis, attestation consequence analysis, or environment-differential diagnosis
- whether a quieter observation surface is needed if hooks distort timing or async behavior

## 10. How this page connects to the rest of the KB
Use this page when the bottleneck is **turning visible result codes or enums into a known local policy bucket**.
Then route forward based on what you find:

- if the earlier bottleneck is response parsing and first meaningful consumer localization:
  - `topics/mobile-response-consumer-localization-workflow-note.md`
- if the result family is specifically attestation / integrity verdict related:
  - `topics/attestation-verdict-to-policy-state-workflow-note.md`
- if the next bottleneck is challenge escalation and loop transitions:
  - `topics/mobile-challenge-trigger-and-loop-slice-workflow-note.md`
- if device/package/session drift changes the mapping outcome:
  - `topics/environment-differential-diagnosis-workflow-note.md`

This page is meant to sit between structured result visibility and deeper consequence modeling.

## 11. What this page adds to the KB
This page adds grounded practical material the mobile subtree needed more of:
- a concrete middle-layer workflow for enum/result-code-heavy mobile targets
- explicit separation of raw field visibility, normalization, policy mapping, and first operational consumer
- practical hook placement around getters, mapping helpers, smali switch boundaries, state writes, and schedulers
- a conservative reminder to drop from decompiler output to switch reconstruction when branch ownership stays unclear
- consequence-driven proof rules for code-heavy Android paths

It is intentionally closer to how analysts regain traction in real app logic than to a generic serialization or enum overview.

## 12. Source footprint / evidence note
Grounding for this page comes mainly from:
- `sources/mobile-runtime-instrumentation/2026-03-16-result-code-enum-to-policy-mapping-notes.md`
- protobuf structure-recovery workflow references such as `pbtk`
- descriptor/schema recovery write-ups used conservatively as support for field and enum naming recovery
- Android bytecode / switch-shape references surfaced through search-layer, used conservatively because direct fetch was limited in this environment
- existing KB pages on response-consumer localization, attestation consequence, and challenge-loop analysis

This page intentionally stays conservative:
- it does not claim all mobile apps use protobuf or enums in the same way
- it does not claim smali is always necessary
- it focuses on the local reduction from visible result fields to first observed policy consequence

## 13. Topic summary
Result-code and enum-to-policy mapping localization is a practical workflow for Android/mobile cases where structured results are already visible, but the first branch that turns those results into retry, degrade, challenge, block, or allow behavior is still hidden.

It matters because many analysts can find the code field and still not explain the app’s next move. The faster route is usually to separate raw field visibility from normalization, reconstruct the real switch or reduction boundary, and prove consequence at the first state write or scheduler that actually predicts later behavior.
