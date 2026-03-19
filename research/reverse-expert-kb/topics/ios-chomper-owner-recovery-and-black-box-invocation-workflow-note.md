# iOS Chomper Owner-Recovery and Black-Box Invocation Workflow Note

Topic class: concrete workflow note
Ontology layers: mobile practical workflow, iOS execution-assisted analysis, owner-recovery continuation
Maturity: practical
Related pages:
- topics/ios-objc-swift-native-owner-localization-workflow-note.md
- topics/ios-flutter-cross-runtime-owner-localization-workflow-note.md
- topics/ios-packaging-jailbreak-and-runtime-gate-workflow-note.md
- topics/mobile-protected-runtime-subtree-guide.md
- topics/mobile-reversing-and-runtime-instrumentation.md
- topics/trace-guided-and-dbi-assisted-re.md
- topics/runtime-table-and-initialization-obligation-recovery-workflow-note.md

## 1. When to use this note
Use this note when an iOS case is already reachable enough to study and the analyst has a plausible owner path, but deeper progress now depends less on prettier static recovery and more on **controlled execution of the real owner inside a reconstructed runtime**.

Typical entry conditions:
- one target artifact or output is already frozen, such as a sign field, token, blob, digest, or encoded request part
- one ObjC / Swift / native owner path is already plausible enough to target
- static reduction is still messy, heavily protected, or too slow relative to the question being asked
- the case appears to require framework load, setup objects, init sequence, token/context preparation, or request-wrapper reconstruction before the owner becomes callable
- live tracing has already exposed enough setup/call-chain truth that execution-assisted replay now looks cheaper than more static cleanup

Use it for cases like:
- Chomper-style invocation of an iOS SDK or framework method after reconstructing the real init/setup path
- sign or shield generation where the decisive method is known, but only after context objects, tokens, or request wrappers are rebuilt
- protected iOS routines where black-box execution plus intermediate-state capture is more practical than full deobfuscation
- cases where live Frida traces reveal the true owner and init sequence, but the next bottleneck is replaying that path in a controlled runtime

Do **not** use this note when:
- the first bottleneck is still traffic-observation topology
- broad packaging / jailbreak / runtime-gate uncertainty still dominates the case
- the real owner across ObjC / Swift / native boundaries is still unclear
- the best next move is still narrow trace-guided semantic reduction rather than controlled replay

In those cases, route to the earlier or narrower page instead.

## 2. Core claim
A recurring iOS analyst mistake is to treat execution-assisted invocation as a tool choice made too early, or as a glamorous replacement for owner recovery.

The stronger practical move is:

```text
freeze one target artifact
  -> recover one plausible owner path from live runtime truth
  -> stop broad owner-localization work once that owner is already good enough
  -> reconstruct only the minimal init/context obligations
  -> invoke the true owner in a controlled runtime
  -> prove that one replayed path yields the real artifact
  -> only then decide whether deeper static reduction is still worth it
```

The central practical question is:

```text
Do I still need more code readability,
or do I already know enough to make the real owner callable? 
```

This note exists because many iOS practical cases stop being mainly about decompilation quality once the owner path is known. They become **initialization-obligation and controlled-invocation** problems instead.

## 3. The five boundaries to separate explicitly

### A. Live owner-discovery boundary
This is where the likely owning method or object becomes visible from live traces.
Typical anchors:
- Frida-traced ObjC selector path
- Swift wrapper that funnels into one narrower owner
- native export or framework-local method that repeatedly produces the target artifact
- request-wrapper builder immediately upstream of the target result

What to capture:
- one candidate owner only
- one representative target action only

Do not carry several competing owners into replay work unless the case truly cannot be narrowed further.

### B. Initialization / setup obligation boundary
This is where the owner becomes callable only after earlier runtime state is satisfied.
Typical anchors:
- framework/module load
- singleton or manager initialization
- token/session/context preparation
- request-object construction
- environment/bootstrap checks that must succeed for the owner to stay alive

What to capture:
- the smallest earlier state that makes the owner truthful enough to call

This boundary usually matters more than the final call signature.

### C. Invocation contract boundary
This is the minimal argument/object contract required to call the owner meaningfully.
Typical anchors:
- `NSString` / `NSData` / dictionary payloads
- request-wrapper objects
- builder-produced context structs or objects
- fixed side tables, salts, or headers packed into the call path

What to capture:
- one reduced call contract, not every possible wrapper class in the app

### D. Controlled-runtime replay boundary
This is where the owner and its obligations are replayed in Chomper or a similar execution-assisted runtime.
Typical anchors:
- framework load in the replay environment
- recreated objects and init sequence
- narrow patches/hooks only where needed to keep the path alive
- direct method/function invocation and output extraction

What to capture:
- whether the replay stays truthful enough to produce the target artifact
- which small missing obligation still explains failure if outputs are close-but-wrong

### E. First proof-of-truth boundary
This is the first concrete proof that replayed invocation is good enough.
Typical anchors:
- returned bytes/string/object match the app output family
- one compare run shows the replay tracks a real input variation correctly
- intermediate state lines up well enough that remaining drift is narrow and explainable

This is the real end point of the workflow.
Until this boundary is proved, replay is still just a hopeful harness.

## 4. Default workflow

### Step 1: freeze one target artifact and one owner candidate
Pick one artifact only.
Examples:
- one sign field
- one shield/blob output
- one encoded request part
- one token returned by a framework method

Write a compact chain:

```text
artifact:
  target field X

live owner candidate:
  ObjC selector / Swift wrapper / native method Y

observed upstream obligations:
  framework load / token init / request wrapper / context builder
```

### Step 2: separate owner discovery from replay obligation recovery
Do not mix these together.
Classify each observed boundary as:
- owner
- setup/init
- contract/input
- worker/helper
- proof output

A useful local label set is:
- discover
- init
- contract
- replay
- prove

This prevents the common failure mode where every helper seen in a live trace gets dragged into the replay harness.

### Step 3: reconstruct the smallest truthful init chain
Prefer a narrow init ladder such as:
- load framework/module
- run one setup method
- build one context/request object
- supply one token or fixed parameter family
- call the owner

Do **not** try to rebuild the whole app environment unless the minimal chain fails for a specific reason.

### Step 4: treat close-but-wrong output as an obligation problem first
When replay outputs are near-correct but still drift, suspect:
- missing earlier setup call
- missing token/session object
- wrong request-wrapper shape
- missing fixed side table / salt / header material
- a small environment check or init return that still changes later output

Only after those are ruled out should you revisit the core transform theory.

### Step 5: prove replay with one compare pair
Use one narrow compare pair:
- two real input variants from live traces
- one accepted/working input and one nearby changed input
- one app output vs one replay output under the same contract

What you want to learn:
- does replay preserve the same input/output relationship as the app?
- is the remaining drift narrow enough to point to one missing obligation?
- is controlled invocation now cheaper than more static reduction?

### Step 6: stop once one truthful callable path exists
The workflow succeeds when you can rewrite the case as:

```text
live owner path known
  -> minimal init/context obligations known
  -> replay contract reduced
  -> controlled invocation works
  -> output family is trustworthy enough for the next task
```

At that point, route forward:
- if the callable path already solves the operator goal, stop
- if remaining drift is narrow, continue into runtime-table/init-obligation recovery
- if replay proves the owner but not the underlying semantics, continue into trace-guided reduction only where needed
- if replay already exposes visible callbacks, result wrappers, or policy-relevant state, continue into result/callback-to-policy consequence work instead of keeping the harness broad

Do not keep expanding the harness after one truthful path exists.

## 5. Practical handoff rule
Stay on this page while the missing proof is still:
- one truthful callable path for one already-plausible owner
- one reduced invocation contract for that owner
- or one small replay-side setup/init debt that can still be paid without reframing the case

Leave broad replay / harness work here once one truthful callable path is already good enough.
Once that replay proof is already good enough, the next bottleneck is usually one of:
- `topics/runtime-table-and-initialization-obligation-recovery-workflow-note.md` when replay is close-but-wrong and the remaining gap has narrowed into one runtime table family, initialized-image boundary, side-condition, or minimal init/context obligation
- `topics/ios-result-callback-to-policy-state-workflow-note.md` when replay or live invocation already exposes result material and the real missing proof is now the first behavior-changing local policy state
- narrower request/signature, native-proof, or trace-guided reduction pages when the callable path is already trustworthy enough and the remaining gap is no longer broad replay itself

A recurring failure mode is to keep broad Chomper/runtime-harness work alive after the real bottleneck has shifted into one smaller init-obligation repair, one result-to-policy consequence proof, or one narrower downstream technical page.

## 6. Practical scenario patterns

## 5. Practical scenario patterns

### Scenario A: sign method is known, but direct replay still fails
Pattern:

```text
owner method identified
  -> replay call returns wrong/empty output
  -> live traces show earlier setup or token path was skipped
```

Best move:
- treat this as a missing-init problem first
- recover the smallest earlier setup sequence rather than redoing broad static analysis

### Scenario B: framework owner is clear, but object contract is under-reduced
Pattern:

```text
framework/module load succeeds
  -> target method can be called
  -> wrapper objects still differ from real app state
  -> output drifts or crashes
```

Best move:
- reduce the invocation contract to one smaller truthful object family
- stop dragging unrelated wrappers into the harness

### Scenario C: static protection is ugly, but live trace already exposed enough truth
Pattern:

```text
OLLVM / VM / mixed runtime still looks noisy statically
  -> live traces reveal owner + init + output path
  -> full semantic cleanup would cost more than controlled replay
```

Best move:
- pivot to execution-assisted owner recovery
- let replay answer the operator question before demanding perfect static beauty

### Scenario D: replay output is close but wrong
Pattern:

```text
artifact family roughly matches
  -> exact bytes still drift
  -> static theory seems plausible already
```

Best move:
- suspect missing init/session/side-table obligations first
- treat this as a narrow environment-reconstruction problem, not immediate algorithm failure

## 6. Breakpoint / hook placement guidance
Useful anchors include:
- one live owner selector/function
- one framework load or manager init edge
- one request/context builder that feeds the owner
- one token/session object creation edge
- one controlled invocation return boundary
- one compare-run output boundary proving truthfulness

If evidence is noisy, anchor on:
- one target artifact and one owner only
- one init sequence only
- one returned object/byte family only
- one compare pair only

## 7. Failure patterns this note helps prevent

### 1. Choosing execution-assisted replay before the owner is narrowed enough
Replay without owner recovery usually turns into harness sprawl.

### 2. Rebuilding too much environment at once
The right target is usually the minimal truthful init chain, not the whole app.

### 3. Treating close-but-wrong replay as immediate algorithm failure
Many near-miss cases are still missing setup/state obligations.

### 4. Treating Chomper as a generic emulator tutorial topic
The practical point is controlled owner invocation, not tool tourism.

### 5. Keeping the replay harness open after the operator question is already answered
Once one truthful callable path exists, more harness work often has diminishing returns.

## 8. Relationship to nearby pages
- `topics/ios-packaging-jailbreak-and-runtime-gate-workflow-note.md`
  - use first when broad setup/gate uncertainty still dominates the case
- `topics/ios-objc-swift-native-owner-localization-workflow-note.md`
  - use first when the real owner across ObjC / Swift / native layers is still unclear
- `topics/ios-flutter-cross-runtime-owner-localization-workflow-note.md`
  - use when the live owner search itself is still cross-runtime and Dart execution is part of the unresolved ownership problem
- `topics/trace-guided-and-dbi-assisted-re.md`
  - use when trace-guided semantic reduction is still the better next move than controlled replay
- `topics/runtime-table-and-initialization-obligation-recovery-workflow-note.md`
  - use when replay already nearly works and the remaining gap is one runtime table, side-condition, or init obligation

## 9. Minimal operator checklist
Use this note best when you can answer these in writing:
- what single artifact am I trying to reproduce?
- what is my best current live owner candidate?
- what earlier init/setup obligations does that owner appear to require?
- what is the smallest invocation contract I can reconstruct?
- what one output comparison would prove replay is truthful enough?
- which narrower page should take over if replay is close-but-wrong rather than fully correct?

If you cannot answer those, the case likely still needs owner-localization or broader iOS gate work first.

## 10. Source footprint / evidence quality note
This note is intentionally workflow-first.

It is grounded by:
- `topics/ios-objc-swift-native-owner-localization-workflow-note.md`
- `topics/ios-flutter-cross-runtime-owner-localization-workflow-note.md`
- `topics/mobile-reversing-and-runtime-instrumentation.md`
- `topics/trace-guided-and-dbi-assisted-re.md`
- `topics/runtime-table-and-initialization-obligation-recovery-workflow-note.md`
- `sources/ios-runtime-and-sign-recovery/2026-03-17-sperm-ios-batch-1-notes.md`
- `sources/ios-runtime-and-sign-recovery/2026-03-17-sperm-ios-batch-2-notes.md`

The evidence base is sufficient because the claim is conservative:
- many iOS sign/protected-runtime cases become execution-assisted once the owner path is visible
- Chomper-shaped work is most valuable as minimal truthful replay of a recovered owner path
- initialization-obligation recovery matters more than tool hype

## 11. Bottom line
When an iOS target already has a plausible live owner path, the next best move is often not broader static cleanup.
It is to recover the smallest truthful init/context obligations, invoke the real owner in a controlled runtime, and stop once one callable path reproduces the artifact well enough for the next task.
