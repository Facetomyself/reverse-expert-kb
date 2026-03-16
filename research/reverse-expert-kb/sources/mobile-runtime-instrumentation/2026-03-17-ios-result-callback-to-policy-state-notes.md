# Source Notes — iOS result / callback to policy-state workflow

Topic: iOS reversing, delegate / closure / result-object handling, policy-state consequence localization

Purpose: support a practical iOS workflow note for the recurring case where an iOS target has already passed broad environment-gate triage and often even owner-localization, but the analyst still cannot tell which callback/result reduction actually turns visible result material into a behavior-changing local policy state.

This note does not try to summarize all iOS runtime instrumentation.
It consolidates the practical gap now visible in the KB:
- the iOS branch now has a first-gate note
- it also has a post-gate owner-localization note across ObjC / Swift / native boundaries
- but it still lacks a concrete follow-on note for the common case where one or more delegate callbacks, completion blocks, Swift `Result`-like wrappers, or native-return wrappers are already visible, yet the first allow / retry / degrade / challenge / block consequence is still hidden

## 1. Existing iOS practical work now naturally points to this missing step
The KB’s current iOS sequence already implies a repeated middle-state:

```text
iOS flow is reachable enough to study
  -> selectors / delegates / Swift wrappers / native helpers are visible
  -> one likely owner boundary may already be localized
  -> callback or result objects are now visible
  -> but the first policy-changing reduction is still unclear
```

That middle state appears naturally after:
- `topics/ios-packaging-jailbreak-and-runtime-gate-workflow-note.md`
- `topics/ios-objc-swift-native-owner-localization-workflow-note.md`

Practical implication:
- the iOS branch now needs a narrower note for the step where visibility exists, but consequence ownership is still mixed across callbacks, wrappers, reducers, and later state writes

## 2. Existing mobile result / response pages already cover the logic, but not the iOS-shaped entry surface
The current mobile subtree already has strong practical pages for:
- `topics/mobile-response-consumer-localization-workflow-note.md`
- `topics/result-code-and-enum-to-policy-mapping-workflow-note.md`
- `topics/attestation-verdict-to-policy-state-workflow-note.md`

High-signal patterns reused here:
- the first visible parsed object is not yet the useful proof target
- raw result fields, normalization, policy mapping, and first behavior-changing consumer should be separated
- one later effect should prove that the reduction mattered

Why a separate iOS note is justified:
- iOS analysts often enter this problem through different practical surfaces than Android-heavy examples do:
  - delegate callbacks
  - block-based completions
  - Swift `async`/continuation wrappers
  - ObjC-to-Swift bridge objects
  - `NSError` + enum / wrapper co-reduction
  - native-return wrappers that only become app-meaningful after Swift/ObjC mapping
- the logic is similar, but the navigation and failure modes are iOS-shaped enough that the branch benefits from one dedicated bridge note

## 3. Existing mobile synthesis already says iOS is a multi-layer runtime problem
`topics/mobile-reversing-and-runtime-instrumentation.md` already frames iOS as:
- Objective-C / Swift / runtime observation
- native-library and platform-mediation interplay
- environment-control and mitigation-aware reasoning

The newer iOS owner-localization note already makes one important move:
- separate trigger, reducer, worker, and first consequence-bearing owner across ObjC / Swift / native boundaries

What still remains after that note in many cases is narrower:
- the owner is partly visible
- a completion or callback already fires
- result material or enum-like categories are observable
- but the first local policy state is still hidden behind reducers, wrappers, and scheduler/controller logic

## 4. A useful iOS operator model is callback/result visibility vs policy-state ownership
A compact recurring workflow shape is:

```text
request / protected action / attestation / validation flow
  -> delegate callback / completion block / Swift result wrapper fires
  -> result object, status enum, NSError, or wrapper fields become visible
  -> helper reduces raw outcome into fewer app-local policy categories
  -> controller / store / coordinator writes one policy state
  -> later retry / degrade / challenge / allow / block consequence appears
```

The repeated analyst mistake is to stop at:
- the first delegate method
- the first Swift closure
- the first `NSError`
- the first native return helper

Those are often visibility surfaces, not yet the first durable policy consequence.

## 5. The four ownership layers worth keeping separate in iOS-shaped cases
A practical iOS note should explicitly separate:

### A. callback / completion surface
Examples:
- delegate methods
- completion handlers
- Swift async continuation resumptions
- notification callbacks
- ObjC block invocation shims

Why it matters:
- this is often the first easy hook point
- but it frequently only exposes result visibility, not consequence ownership

### B. result normalization boundary
Examples:
- enum wrappers
- `NSError` + status co-reduction
- ObjC model to Swift struct/class adapters
- `Result.success` / `Result.failure` wrappers
- helper methods that collapse several backend/platform result shapes into one app-local object

Why it matters:
- several noisy outcomes may shrink here into a much smaller app-local decision surface

### C. policy mapping boundary
Examples:
- status-to-mode helper
- verdict-to-flow-state mapper
- retryability classifier vs business-policy classifier
- trust / challenge / degrade bucket selectors

Why it matters:
- this is often the first point where app-local meaning becomes reusable and predictive

### D. first behavior-changing consumer
Examples:
- controller/coordinator state write
- feature/route gate
- retry/backoff scheduler
- challenge-needed flag
- request family switch or follow-up task selection

Why it matters:
- this is the boundary the workflow should end on
- earlier callback visibility matters only insofar as it routes into this consumer

## 6. Good scenario shapes for this note
This note is especially justified for:
- visible delegate or completion callbacks where the target still behaves differently later
- Swift-facing result wrappers where `success/failure` is visible but app-local policy category is not
- native-return helpers that are easy to hook, yet still only expose one low-level verdict before ObjC/Swift mapping
- attestation / trust / challenge paths where one callback already fires but the first app-local state change still hides behind reducer helpers
- request/validation flows where `NSError` handling and business-policy handling are mixed together

## 7. Relationship to nearby KB pages
This note would bridge naturally between:
- `topics/ios-objc-swift-native-owner-localization-workflow-note.md`
- `topics/mobile-response-consumer-localization-workflow-note.md`
- `topics/result-code-and-enum-to-policy-mapping-workflow-note.md`
- `topics/attestation-verdict-to-policy-state-workflow-note.md`
- `topics/mobile-challenge-trigger-and-loop-slice-workflow-note.md`

Its value is to make the iOS branch less dependent on Android-shaped examples once the case has already moved past environment gating and broad owner selection.

## Compact operator framing

```text
iOS result surface is already visible
  -> freeze one protected action or validation flow
  -> separate callback surface, result normalization, policy mapping, and first consumer
  -> prove one policy-state write or scheduler edge
  -> continue from that consequence, not from the first visible callback
```

## Bottom line
The iOS practical branch now needs a post-owner note for the common case where callback/result visibility already exists but the first behavior-changing policy-state reduction is still unclear.
The intended claim is conservative:
- visible delegate / closure / result handling is not yet enough
- iOS analysis still needs one narrower workflow for turning visible result material into one proved local consequence
- adding that note would make the branch more practical and internally complete.