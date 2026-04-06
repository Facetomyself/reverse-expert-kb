# iOS PAC-Shaped Callback / Dispatch Failure Triage

Topic class: concrete workflow note
Ontology layers: mobile runtime practice, iOS practical ladder continuation, mitigation-aware callback/dispatch triage
Maturity: practical
Related pages:
- topics/arm64e-pac-and-mitigation-aware-ios-reversing.md
- topics/ios-practical-subtree-guide.md
- topics/ios-objc-swift-native-owner-localization-workflow-note.md
- topics/ios-chomper-owner-recovery-and-black-box-invocation-workflow-note.md
- topics/runtime-table-and-initialization-obligation-recovery-workflow-note.md
- topics/ios-result-callback-to-policy-state-workflow-note.md
- topics/observation-distortion-and-misleading-evidence.md

## 1. Why this page exists
This page exists because the KB’s iOS practical branch already had a mitigation-aware continuation page for arm64e / PAC-shaped cases, but still lacked one narrower operator note for a recurring real bottleneck:
- the case is already reduced enough that one callback, block invoke, indirect dispatch, or tail-call handoff looks like the active failure surface
- the analyst can no longer tell whether the problem is the wrong callback family, the right family in the wrong authenticated context, a lying code view, or a replay-close path missing one narrower runtime obligation

This is exactly the kind of point where iOS work can stall in noisy debates like:
- "the callback target is obviously wrong"
- "the owner must still be earlier"
- "the decompiler already shows the path clearly"
- "this is just generic corruption"

Often none of those stronger claims is justified yet.
What is actually needed is a smaller triage workflow for one authenticated callback / dispatch boundary.

## 2. When to use this page
Use this page when most of the following are true:
- the case is already clearly in the iOS practical branch
- broader setup, trust-path, and first-owner questions are no longer the only blockers
- one callback / block invoke / function-pointer dispatch / tail-call family is already visible enough to isolate
- the path fails, crashes, or diverges near that boundary on arm64e-era iOS targets
- the immediate question is no longer "what broad branch am I in?" but "what class of callback/dispatch failure is this?"

Representative entry conditions:
- a completion block or callback object looks structurally right, but invoking or replaying it crashes sharply on-device
- a tail-call or indirect branch looks statically straightforward, but the runtime landing is inconsistent with the prettiest decompiler view
- a private-framework or dyld-cache-backed callback family looks plausible, yet extracted-image and runtime views do not agree cleanly enough to support the next claim
- one reduced replay path is close enough that the last unstable edge is now a callback/dispatch handoff rather than broad owner choice

Do **not** use this page when the case is still dominated by:
- traffic-surface blindness
- environment normalization or deployment incoherence
- broad iOS runtime-gate uncertainty
- first owner-localization uncertainty
- broad PAC/arm64e confusion without one concrete callback/dispatch boundary yet

In those cases, stay with the earlier iOS ladder pages first.

## 3. Core claim
When a modern iOS case narrows into one PAC-shaped callback or dispatch boundary, the best next move is usually **not** to widen tracing.
It is to classify the boundary conservatively.

The key question is usually:

```text
Is this boundary failing because I chose the wrong callback/dispatch family,
or because the family is plausible but the authenticated pointer/context/code view
is still not truthful enough?
```

A practical continuation rule is:

```text
iOS case already reduced into one callback/dispatch edge
  -> freeze one representative failure boundary
  -> classify the failure as family / context / code-view / replay-close
  -> prove one runtime landing and one compare pair
  -> route quickly back into owner proof, replay repair, or consequence proof
```

The point of this page is not to become a PAC theory compendium.
Its job is to prevent analysts from overclaiming at exactly the moment where one authenticated callback/dispatch boundary becomes the next bottleneck.

## 4. The four failure classes to separate explicitly

### A. Wrong-family problem
The callback or dispatch boundary is simply not the right one.
Common signals:
- several sibling callbacks or dispatch edges exist
- the chosen edge is easy to see, but does not predict the later effect
- target and non-target actions hit the same edge with no meaningful difference

What to preserve:
- evidence that the edge is merely nearby, common, or decorative
- one downstream effect showing it does not own the relevant continuation

### B. Right-family, wrong authenticated context problem
The family is plausible, but the pointer/context pair is not yet truthful.
Common signals:
- the boundary looks structurally right, but replay or direct invocation crashes sharply
- the failing edge appears late enough that broad owner search feels wasteful
- object shape / slot / callback wrapper looks plausible, yet the live landing still disagrees

What to preserve:
- one reason the family still looks plausible
- one reason the exact pointer/context/object provenance is still not trusted

This is the most important class to keep separate from generic corruption storytelling.

### C. Lying code-view problem
The analysis surface itself is misleading.
Common signals:
- dyld shared cache truth and extracted image truth do not line up cleanly
- explicit PAC/auth-check scaffolding dominates the decompiler view
- the statically visible dispatch edge does not match the runtime landing well enough to trust stronger claims

What to preserve:
- which code view was used
- what makes it potentially misleading
- what runtime anchor disagrees with it

### D. Replay-close / missing-obligation problem
The callback/dispatch family is probably right, and the code view may already be good enough, but one narrower runtime obligation is still missing.
Common signals:
- replay is close enough that broad owner work should stop
- the unstable edge smells like one missing image/table/init/context obligation
- the callback or dispatch object exists, but not with the same truthful runtime materialization as the live path

What to preserve:
- the smallest still-missing obligation hypothesis
- why this looks cheaper to test than broadening callback coverage again

## 5. Truth surfaces to trust first

### A. Runtime landing beats pretty dispatch pseudocode
If the decompiler shows a neat callback or tail target but runtime landing evidence disagrees, prefer the runtime anchor first.
Useful anchors:
- one landing address or callee family
- one before/after compare around the failing dispatch
- one on-device/no-crash vs crash pair
- one callback registration site plus one actual invocation landing

### B. Cache-truthful system code beats stale extracted views
If the path crosses system/private framework code, treat dyld shared cache truth as primary.
If the cache/build/image relationship is unclear, stronger callback-family claims should pause.

### C. Decluttered decompiler views are routing aids, not proof by themselves
PAC/auth-check cleanup can be useful for readability.
It is not a license to forget the raw auth-bearing sequence.
For triage, preserve both:
- the decluttered route view
- the raw sequence needed for failure classification

## 6. Default workflow

### Step 1: freeze one representative boundary
Pick one only:
- one completion block invoke
- one callback-object dispatch
- one indirect branch / tail-call handoff
- one vtable-like or slot-based call edge

Do not widen into every PAC-looking site nearby.

### Step 2: write a four-bucket draft before deeper tracing
Use a compact draft like this:

```text
candidate family:
  callback / block / dispatch edge X

current best failure class:
  wrong-family | wrong-context | lying-code-view | replay-close

runtime anchor:
  one observed landing / crash boundary / compare pair

later effect of interest:
  callback consequence / next request / policy state / next scheduler edge
```

This draft can be wrong.
Its purpose is to stop uncontrolled speculation.

### Step 3: prove family first, then context
Ask first:
- does this edge predict the relevant later effect better than sibling edges do?

Only after that ask:
- if the family is plausible, is the exact object/pointer/context still untrusted?

This ordering matters.
Otherwise analysts can waste time diagnosing PAC-shaped context issues on a boundary that never owned the case.

### Step 4: classify the code view explicitly
For the chosen boundary, freeze:
- live device or debugger view
- cache/extracted-image view
- any decompiler cleanup that hides explicit auth scaffolding
- the specific reason one view is being trusted over another

Minimal success condition:
- future-you can answer which exact view supported the callback/dispatch claim

### Step 5: use one narrow compare pair
Good compare pairs include:
- target action vs nearby non-target action
- live path vs reduced replay path
- no-crash landing vs crash landing at the same boundary
- one callback registration path vs one actual invocation path

What you want to learn:
- is the chosen boundary family-specific?
- does the runtime landing remain stable?
- is the difference better explained by wrong family, wrong context, or missing runtime obligation?

### Step 6: stop at the first useful classification
The workflow is successful once you can rewrite the case as one of these:

```text
chosen callback/dispatch edge was the wrong family
```

```text
chosen family is plausible, but the authenticated pointer/context is still not truthful
```

```text
the static code view was misleading; runtime-first proof should dominate
```

```text
the path is replay-close and the remaining gap is one narrower runtime obligation
```

At that point, leave this page.

## 7. Practical scenario patterns

### Scenario A: block invoke looks right, but direct replay dies immediately
Pattern:

```text
visible block/callback object exists
  -> reduced invocation seems plausible
  -> on-device invoke crashes sharply
```

Best move:
- do not jump straight to "wrong owner"
- first separate wrong-family from right-family/wrong-context
- preserve one live registration or materialization edge before deeper replay work

### Scenario B: decompiler shows one obvious tail target, runtime says otherwise
Pattern:

```text
tail-call/auth-check sequence cleaned up nicely
  -> pseudocode suggests one target
  -> runtime landing or effect does not agree
```

Best move:
- downgrade the pseudocode from proof to routing aid
- classify this first as a possible lying-code-view problem

### Scenario C: private-framework callback family is plausible, but extracted image is untrustworthy
Pattern:

```text
system/private framework path seems involved
  -> extracted image looks readable
  -> cache-backed truth and live addresses do not line up cleanly
```

Best move:
- freeze the cache/build/image relationship before stronger callback-family claims
- do not use stale extraction confidence as dispatch proof

### Scenario D: replay is almost right, but the final dispatch edge still fails
Pattern:

```text
owner already plausible
  -> most setup appears sufficient
  -> last unstable edge is callback/dispatch handoff
```

Best move:
- treat this as replay-close until proven otherwise
- bias toward one missing table/image/init/context obligation instead of reopening broad owner search

## 8. Breakpoint / hook placement guidance
Useful anchors include:
- one callback registration or install site
- one actual invocation landing site
- one state/object materialization edge before the dispatch
- one later effect showing whether the boundary mattered
- one compare pair separating crash from no-crash

If the path is noisy, prefer:
- one boundary over many sibling callbacks
- one runtime landing over many static guesses
- one object provenance question over many surface-level hooks
- one downstream effect over many local helper names

## 9. Common mistakes this page prevents

### 1. Treating every arm64e callback crash as generic corruption
This erases the useful distinction between wrong-family and wrong-context cases.

### 2. Treating every sharp callback crash as PAC proof
That overclaims far beyond what most operator evidence supports.

### 3. Treating decompiler cleanup as semantic proof
Decluttering helps reading; it does not automatically prove the real landing or owner.

### 4. Reopening broad owner search when the case is already replay-close
That often wastes the strongest evidence the case already produced.

### 5. Hooking every nearby callback instead of freezing one boundary
This turns a narrow classification problem back into noisy exploration.

## 10. Relationship to nearby pages
- `topics/arm64e-pac-and-mitigation-aware-ios-reversing.md`
  - use first when the case is broadly mitigation-aware but not yet reduced to one callback/dispatch boundary
- `topics/ios-objc-swift-native-owner-localization-workflow-note.md`
  - use first when the real bottleneck is still which boundary owns the consequence at all
- `topics/ios-chomper-owner-recovery-and-black-box-invocation-workflow-note.md`
  - use first when the owner is already plausible and the real next question is minimal truthful invocation rather than failure classification at one dispatch edge
- `topics/runtime-table-and-initialization-obligation-recovery-workflow-note.md`
  - use next when this page classifies the case as replay-close / missing-obligation rather than wrong-family
- `topics/ios-result-callback-to-policy-state-workflow-note.md`
  - use next when the callback/dispatch boundary succeeds well enough and the remaining gap is the first behavior-changing consumer or policy state
- `topics/observation-distortion-and-misleading-evidence.md`
  - use when the central lesson is really that the code view or tooling cleanup distorted what the analyst believed

## 11. Minimal operator checklist
Use this note best when you can answer these in writing:
- what exact callback/dispatch boundary am I freezing?
- what later effect makes this boundary worth caring about?
- is my best current explanation wrong-family, wrong-context, lying-code-view, or replay-close?
- what one runtime landing or compare pair do I trust most?
- what narrower page should take over once this classification is done?

If you cannot answer those, the case probably still needs the broader PAC/iOS continuation or an earlier iOS ladder page.

## 12. Source footprint / evidence quality note
This note is intentionally narrow and conservative.

It is grounded by:
- `topics/arm64e-pac-and-mitigation-aware-ios-reversing.md`
- `topics/ios-practical-subtree-guide.md`
- `sources/mobile-runtime-instrumentation/2026-03-21-arm64e-pac-mitigation-aware-ios-notes.md`
- `sources/mobile-runtime-instrumentation/2026-03-22-ios-pac-callback-dispatch-triage-notes.md`
- Apple pointer-authentication documentation
- NowSecure dyld shared cache reversing material
- Binary Ninja arm64e PAC cleanup material
- practical iOS reversing training material that reinforces runtime-first async/callback tracing discipline

The evidence base is sufficient for a practical workflow note because the claims are limited to:
- callback/dispatch failures on arm64e are easy to misclassify
- truthful code-view and runtime-landing discipline matter more than broader PAC theorizing here
- one small classification workflow is more useful than more callback accumulation

## 13. Bottom line
When a modern iOS case narrows into one PAC-shaped callback or dispatch failure, the next best move is usually not broader tracing.
Freeze one boundary, classify it conservatively as family/context/code-view/replay-close, prove one runtime landing with one compare pair, and then route back out quickly.
That keeps mitigation-aware callback confusion from swallowing the rest of the case.


## Practical arm64e/PAC triage reminders added in the 2026-04-07 external pass

A sharper stop rule worth preserving here is:

```text
callback/dispatch crash
  != PAC-shaped callable-pointer failure
  != generic selector/signature mismatch
  != block-lifetime / capture / object-ownership failure
  != later consumer/state consequence problem
```

Useful practical split:
- selector/ABI/signature mismatch
- block layout / invoke-pointer / capture-lifetime mistake
- stale or wrongly reconstructed function pointer under arm64e/PAC expectations
- later queue/actor/UI consumer problem after callback delivery is already fine

Practical reminders:
- not every arm64e callback crash is a PAC problem
- keep callback landing truth separate from callable-pointer truth
- keep callable-pointer truth separate from later resume/delivery truth
- keep delivery truth separate from later consumer/state consequence truth
- analyst-built trampolines, copied block objects, stale function pointers, or reinterpreted callable storage are better treated as narrower candidate causes than broad “PAC broke it” folklore until one boundary is proved

This branch now explicitly preserves the operator split between ordinary lifetime/layout mistakes and genuinely PAC-shaped callable-pointer failures on arm64e.
