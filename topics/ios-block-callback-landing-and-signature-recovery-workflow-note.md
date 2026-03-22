# iOS Block / Callback Landing and Signature-Recovery Workflow Note

Topic class: concrete workflow note
Ontology layers: mobile practical workflow, iOS runtime branch, mitigation-aware callback proof
Maturity: practical
Related pages:
- topics/ios-practical-subtree-guide.md
- topics/arm64e-pac-and-mitigation-aware-ios-reversing.md
- topics/ios-pac-shaped-callback-and-dispatch-failure-triage.md
- topics/ios-objc-swift-native-owner-localization-workflow-note.md
- topics/ios-result-callback-to-policy-state-workflow-note.md
- topics/runtime-table-and-initialization-obligation-recovery-workflow-note.md

## 1. When to use this note
Use this note when a modern iOS case has already narrowed far enough that one callback, block, closure, or dispatch-like landing family looks plausible, but the landing itself is still not trustworthy enough to support owner, replay, or policy claims.

Typical entry conditions:
- the case is already clearly iOS-shaped and at least partly reachable
- one callback/block family is already plausible enough to freeze
- PAC / arm64e / dyld-cache truthfulness is now part of the uncertainty
- the current bottleneck is no longer broad setup/gate diagnosis or broad owner search
- the analyst still cannot cleanly answer whether the visible landing site and parameter contract are real enough to trust

Use it for cases like:
- a block/closure looks like the right callback boundary, but replay or hook results keep drifting
- a decompiler shows an invoke target, but arm64e/PAC-era code truthfulness still feels suspect
- `CDUnknownBlockType` or equivalent placeholder signatures still hide whether the visible block fits the behavior under study
- several wrappers or dispatch helpers run near one callback family and it is still unclear which landing is behaviorally meaningful
- a callback/dispatch failure looks PAC-shaped, but it is still unclear whether the real issue is wrong family, wrong context, or a lying code view

Do **not** use this note when:
- the broad bottleneck is still traffic topology, deployment coherence, or packaging/jailbreak/runtime-gate drift
- the owner path is still too broad and you do not yet have one plausible callback family to freeze
- the callback/result is already trustworthy enough and the real remaining gap is the first policy-bearing consumer
- the remaining replay gap has already narrowed into one runtime-table or initialization obligation rather than callback-landings truth

In those cases, route to the broader or narrower page first.

## 2. Core claim
Once a modern iOS case has already narrowed into one plausible callback/block family, the best next move is often **not** more broad tracing and **not** immediate policy interpretation.
It is to prove one truthful landing boundary and one usable parameter contract.

The central question is usually:

```text
Is this callback/block landing actually the truthful control-transfer boundary
for the behavior I care about, and is its contract narrow enough to trust?
```

A more operational way to phrase the same stop rule is:
- once one callback/block family is already plausible, stop widening broad owner search by default
- instead, try to freeze the **first runtime-backed block contract**

In this note, that means a four-part proof object:
- one plausible block/callback family
- one dyld/cache-truthful invoke landing
- one runtime-visible or tightly constrained signature shape
- one downstream effect worth handing off

Until that is proved, modern iOS work often stalls in three kinds of confusion:
- PAC-era code views that look more certain than they really are
- block-shaped objects whose signatures are still too vague to interpret safely
- wrappers and dispatch helpers that all appear near the real landing but do not own it

## 3. The four boundaries to separate explicitly

### A. Block object vs invoke landing
A block object being present is **not** the same thing as proving the invoke landing that later transfers control.

What to separate:
- where the block object is created or passed
- where the block pointer is stored or forwarded
- where the block is actually invoked

Useful reminder:
- block presence proves a possible callback family
- invoke landing proves an actual transfer boundary

### B. Static code view vs truthful runtime view
Modern iOS callback work is often distorted by cache extraction quality, symbolization gaps, PAC-era pointer handling, and replay-side simplifications.

What to separate:
- what the decompiler suggests
- what the dyld/cache-backed image layout really supports
- what runtime observation actually confirms

Useful reminder:
- odd disassembly or weird target edges do not automatically mean anti-analysis
- sometimes the code view is simply not truthful enough yet

### C. Parameter placeholder vs usable contract
A callback that is visible but still typed as `CDUnknownBlockType` or another vague placeholder is often not ready to support strong claims.

What to separate:
- broad "there is a block here"
- concrete argument shape / type encoding / calling contract
- the smaller contract that can be compared across runs or against a replay attempt

Useful reminder:
- a recovered runtime signature is often a better proof object than another broad hook near the same family

### D. Landing boundary vs later consequence
A proved landing is not yet the same thing as a proved owner or policy consumer.

What to separate:
- truthful landing boundary
- immediate wrapper / adapter work
- first owner or policy-bearing consumer downstream

Useful reminder:
- this page ends once the landing is trustworthy enough to hand back into owner, replay, or policy work

## 4. Default workflow

### Step 1: freeze one callback/block family only
Pick one family only.
Examples:
- one completion handler attached to one protected request family
- one block passed into one attestation/check path
- one closure/callback handoff associated with one challenge or verification step

Avoid mixing multiple callback families.

### Step 2: write one landing hypothesis
Draft the narrow chain before touching more hooks:

```text
block/callback object source:
  where it is created or passed

candidate invoke landing:
  where it seems to transfer control

current contract confidence:
  known / placeholder / partially recovered

current truth risk:
  wrong family / wrong context / code-view drift / missing obligation

visible later effect:
  one downstream state, request, or policy consequence
```

This draft is allowed to be wrong.
Its purpose is to stop uncontrolled callback accumulation.

### Step 3: verify the code view is truthful enough
Before over-interpreting the landing, check whether the current image/disassembly view is trustworthy enough.

Practical checks:
- is the relevant image coming from dyld shared cache context that has been extracted/read coherently?
- do the surrounding regions, imports, and symbolization look consistent with the runtime family you think you are studying?
- are strange targets or gaps possibly explained by cache-truth or symbolization issues rather than target intent?

A good discipline rule:
- downgrade confidence in any callback-landing claim when the image view itself may still be lying

### Step 4: recover the narrowest usable block signature
If the callback is still structurally vague, prefer narrowing the parameter contract before adding more semantic claims.

Useful tactics:
- stop near the call site that passes the block
- capture the concrete block object address
- inspect runtime-visible signature/type-encoding information when possible
- compare recovered shape across accepted/degraded or target/non-target runs

Source-backed structural reminder worth preserving here:
- the Apple/Clang Block ABI treats a block as a callable object with an `invoke` pointer and, when available, a descriptor-carried signature field
- that means the analyst should explicitly distinguish:
  - block object presence
  - invoke landing truth
  - signature-contract truth

What you want:
- enough contract to distinguish the real callback family from nearby adapters/wrappers
- enough contract to know whether replay attempts are even shape-compatible
- enough runtime-backed structure to say you now have the first trustworthy contract, rather than another static guess near the same wrapper family

### Step 5: prove one landing boundary with one compare pair
Use one narrow compare pair:
- target action vs nearby non-target action
- truthful run vs degraded/challenged run
- correct context vs missing-obligation replay attempt

What you want to learn:
- does the same block family land at the same boundary in both runs?
- does contract shape differ?
- does the landing predict one later effect better than nearby wrappers do?

### Step 6: stop once landing truth is good enough to hand off
The workflow succeeds when you can rewrite the path as:

```text
block/callback family
  -> truthful invoke landing
  -> usable parameter contract
  -> one downstream effect worth handing off
```

That chain is the practical definition of the **first runtime-backed block contract**.
Once it exists, default to treating it as the proof boundary that ends broad callback/owner widening for this stage.
Only reopen broad owner search if later evidence actually breaks that contract.

At that point, route forward:
- to `topics/ios-pac-shaped-callback-and-dispatch-failure-triage.md` when the main question is still how to classify a callback/dispatch failure conservatively
- to `topics/ios-objc-swift-native-owner-localization-workflow-note.md` when the landing is now trustworthy enough and the real question becomes which downstream boundary owns the consequence
- to `topics/ios-result-callback-to-policy-state-workflow-note.md` when landing truth already exists and the real remaining gap is the first policy-bearing consumer
- to `topics/runtime-table-and-initialization-obligation-recovery-workflow-note.md` when replay remains close-but-wrong and the callback family is now trustworthy enough to blame one narrower runtime obligation

Do not keep this page open once landing truth is no longer the bottleneck.

## 5. Practical scenario patterns

### Scenario A: block is visible, but invoke landing is still untrusted
Pattern:

```text
block object clearly present
  -> likely invoke target visible in static view
  -> runtime behavior still drifts
  -> analyst not sure if the landing is real
```

Best move:
- stop arguing from the decompiler alone
- first verify dyld/cache truth and recover the narrowest usable runtime contract

### Scenario B: callback failure looks PAC-shaped, but wrong-family confusion is still plausible
Pattern:

```text
modern iOS case
  -> authenticated-pointer or weird-target feel
  -> callback does not behave as expected
  -> several similar callback families exist nearby
```

Best move:
- classify conservatively first
- do not assume PAC is the whole story before excluding wrong-family and wrong-context explanations

### Scenario C: `CDUnknownBlockType` blocks policy or replay reasoning
Pattern:

```text
callback family looks right
  -> signature still vague
  -> replay attempts or semantic claims remain speculative
```

Best move:
- treat signature recovery as the next proof object
- use runtime-visible block signature/type shape to reduce ambiguity before more owner/policy claims

### Scenario D: invoke landing is known, but later policy meaning is still not
Pattern:

```text
landing boundary now trustworthy
  -> wrappers and consumers still compete
  -> analyst starts interpreting policy too early
```

Best move:
- leave this note
- hand off into owner-localization or result-to-policy work

## 6. Breakpoint / hook placement guidance
Useful anchors include:
- the call site that passes the block/callback object
- the suspected invoke landing, not only the wrapper around it
- the smallest runtime-visible contract surface for the block signature
- one downstream effect that proves the chosen landing mattered

If evidence is noisy, prefer:
- one callback family and one compare pair
- one landing boundary, not every nearby dispatch helper
- one recovered parameter shape, not every guessed wrapper type

## 7. Failure patterns this note helps prevent

### 1. Treating block presence as proof of the landing
A block object is a candidate family, not yet a proved transfer boundary.

### 2. Treating a PAC-shaped weird edge as automatically decisive
Modern iOS weirdness may still be wrong-family, wrong-context, or cache-truth drift.

### 3. Treating placeholder signatures as good enough for replay claims
A vague callback contract often means the next useful move is signature recovery, not more policy interpretation.

### 4. Treating landing truth as the same thing as consequence ownership
A truthful landing is still only an intermediate proof boundary.

## 8. Relationship to nearby pages
- `topics/arm64e-pac-and-mitigation-aware-ios-reversing.md`
  - use first when the case is broadly mitigation-aware and the current problem is still code-view truth, PAC-era confidence calibration, or routing the case back toward owner or replay work
- `topics/ios-pac-shaped-callback-and-dispatch-failure-triage.md`
  - use when one authenticated callback/dispatch boundary is already frozen and the current job is classifying the failure as wrong-family, wrong-context, lying-code-view, or replay-close missing-obligation drift
- `topics/ios-objc-swift-native-owner-localization-workflow-note.md`
  - use when the landing is now trustworthy enough and the real bottleneck is the first consequence-bearing owner downstream
- `topics/ios-result-callback-to-policy-state-workflow-note.md`
  - use when truthful result/callback visibility already exists and the current bottleneck is the first policy-bearing consumer
- `topics/runtime-table-and-initialization-obligation-recovery-workflow-note.md`
  - use when replay remains close-but-wrong and the missing proof is now one narrower runtime table family, initialized-image boundary, or init/context obligation

## 9. Minimal operator checklist
Use this note best when you can answer these in writing:
- what single callback/block family am I freezing?
- where is the candidate invoke landing?
- is my current image/disassembly view truthful enough to trust that landing?
- what contract detail is still missing from the callback signature?
- what one compare pair could prove the landing is real?
- which downstream note should take over once landing truth is proved?

If you cannot answer those, the case likely still needs broader iOS routing, owner reduction, or replay repair first.

## 10. Source footprint / evidence quality note
This note is intentionally workflow-first and conservative.

It is grounded by:
- `topics/mobile-reversing-and-runtime-instrumentation.md`
- `topics/ios-practical-subtree-guide.md`
- `topics/arm64e-pac-and-mitigation-aware-ios-reversing.md`
- `topics/ios-pac-shaped-callback-and-dispatch-failure-triage.md`
- `sources/mobile-runtime-instrumentation/2026-03-22-ios-block-callback-landing-and-signature-recovery-notes.md`

The evidence base is sufficient for this claim because it stays modest:
- PAC and dyld-cache truth issues can distort confidence in callback landings
- runtime-visible block signature recovery can narrow callback ambiguity materially
- proving one truthful landing boundary is a real practical step before stronger owner, replay, or policy claims

## 11. Bottom line
When a modern iOS case has already narrowed into one plausible block/callback family, the next best move is often not broader tracing and not immediate policy interpretation.
First prove the code view is truthful enough, recover the narrowest usable callback contract, and confirm one landing boundary with one compare pair.
That single proof usually turns a PAC-shaped or callback-shaped tangle into a tractable next step.
