# iOS Flutter Cross-Runtime Owner-Localization Workflow Note

Topic class: concrete workflow note
Ontology layers: mobile practical workflow, iOS runtime branch, cross-runtime owner-localization bridge
Maturity: practical
Related pages:
- topics/ios-packaging-jailbreak-and-runtime-gate-workflow-note.md
- topics/ios-objc-swift-native-owner-localization-workflow-note.md
- topics/mobile-protected-runtime-subtree-guide.md
- topics/mobile-signature-location-and-preimage-recovery-workflow-note.md
- topics/native-interface-to-state-proof-workflow-note.md
- topics/mobile-reversing-and-runtime-instrumentation.md

## 1. When to use this note
Use this note when the target is clearly **iOS + Flutter/Dart shaped** and deeper progress is blocked because several runtimes all look relevant, but you still do not know which one actually owns the artifact or behavior that matters.

Typical entry conditions:
- the app is obviously Flutter-based or mixed iOS/Flutter at runtime
- the case is already past the first broad iOS setup/gate triage
- traffic, request, field, or feature behavior is visible enough to freeze one representative flow
- static repack, reFlutter-style rewriting, or framework-patching attempts are brittle, incomplete, or no longer the best next move
- ObjC/Swift shell code is visible, Flutter engine/runtime artifacts are visible, and Dart-side ownership is plausible but not yet proved
- you can already name one target field, request family, callback family, or consequence, but the true owner still hides across runtime boundaries

Use it for cases like:
- a signature or token field appears in traffic, but the decisive preimage builder may live in Dart rather than ObjC or native glue
- iOS-side hooks show entry into Flutter/native glue, but the first consequence-bearing update still happens in Dart runtime code
- repack/rewrite workflows fail or produce unstable artifacts, while the live runtime still executes the target flow normally
- multiple method families fire across UIKit/ObjC, Flutter engine glue, and Dart code, and you need one trustworthy owner before deeper tracing

Do **not** use this note when:
- the first decisive problem is still packaging / signing / jailbreak / topology uncertainty
- the target is not meaningfully cross-runtime and already reduced to ordinary ObjC / Swift / native ownership
- the main bottleneck is later and narrower, such as one already-isolated signature preimage chain or one already-isolated callback-to-policy mapper
- the case has already become an ordinary native subsystem proof problem

In those cases, route to the narrower note instead.

## 2. Core claim
For Flutter-shaped iOS targets, the best next move is often **not** to force static rewrite or repack success.
It is to prove which runtime actually owns one consequence-bearing artifact.

The central question is usually:

```text
Which boundary first turns
UIKit / ObjC / Swift trigger state,
Flutter engine routing,
or Dart-side object state
into the artifact or consequence I care about?
```

A compact practical rule is:
- **freeze one flow** first
- **separate shell from owner** second
- **prefer the runtime that actually executes** third
- **prove one consequence-bearing owner** before demanding a perfect rebuilt artifact

Until that owner is proved, Flutter/iOS work often collapses into endless framework setup churn.

## 3. The five boundaries to separate explicitly

### A. iOS shell / trigger boundary
This is where the flow first becomes visible from UIKit, ObjC, Swift, delegates, controllers, or native app shell code.

Typical anchors:
- UI action methods
- view-controller transitions
- app lifecycle callbacks
- ObjC-visible glue into Flutter containers
- native bridge methods that package arguments for Flutter-side routing

What to capture:
- one representative trigger only
- whether this layer is merely launching the flow or already shaping the target artifact

Do not assume the visible iOS shell owns the algorithm.
It often only starts the path.

### B. Flutter engine / bridge boundary
This is where the iOS shell hands control into Flutter runtime machinery.

Typical anchors:
- Flutter method-channel or message-channel handlers
- engine/bootstrap routing helpers
- framework initialization and registration paths
- glue between app shell code and Dart isolate/runtime state

What to capture:
- the first boundary where app-shell intent becomes Flutter runtime work
- whether the bridge is only transport or already reducing arguments into a smaller family

This boundary is often overread as the owner because it looks structurally central.
Usually it is still a router.

### C. Dart owner boundary
This is where the executing Dart runtime first owns one artifact, field, digest input, policy state, or request-shaping object.

Typical anchors:
- recovered Dart method names or offsets near the target field
- update / builder / serializer helpers
- stateful object methods that accumulate request fields
- digest/hash helpers fed by higher-level object state
- model or controller methods that write the field later observed in traffic

What to capture:
- the narrowest Dart-side method/object that predicts the target consequence better than bridge visibility alone

This is usually the real goal of the workflow.

### D. Native helper / worker boundary
This is where lower-level crypto, encoding, or framework support routines run.

Typical anchors:
- native digest helpers
- bridge shims
- engine support routines
- reusable C/C++ helpers under Flutter or app-native code

What to capture:
- whether this code is a true owner or only a worker under Dart/object ownership
- whether multiple higher-level flows converge here

Do not reward this layer just because it looks lower-level or more “serious.”

### E. First consequence-bearing consumer
This is the first boundary that proves the owner matters behaviorally.

Typical anchors:
- request-finalization field write
- serialized object handoff into transport
- policy/state write after a Dart-side reduction
- later visible request acceptance or behavior change

What to capture:
- one downstream effect that depends on the candidate owner

This is where the workflow should stop.

## 4. Default workflow

### Step 1: freeze one representative cross-runtime flow
Pick one flow only.
Examples:
- tap action -> token field added to first protected request
- launch -> config/bootstrap object -> signature-bearing request
- page or UI event -> Dart method update -> field serialized into request body

Avoid mixing several screens, several request families, or several candidate fields.

### Step 2: draft one cross-runtime ownership chain
Write a compact draft before tracing deeper:

```text
iOS shell trigger:
  controller / selector / callback

Flutter bridge boundary:
  method channel / engine route / glue helper

candidate Dart owner:
  recovered method / state object / field updater

possible native worker:
  digest / encode / helper routine

visible effect:
  request field / serialized payload / later policy change
```

This draft may be wrong.
Its purpose is to stop framework-shaped wandering.

### Step 3: decide whether static rewrite is still paying rent
Ask a narrow question:
- is repack/rewrite/static instrumentation giving a more trustworthy path to the owner?
- or is it now only delaying direct recovery in the runtime that already executes?

If repack/rewrite attempts are:
- brittle
- hard to keep runnable
- failing before the target flow
- obscuring rather than clarifying ownership

then switch to **live-runtime owner recovery**.

This is the key practical rule.

### Step 4: recover candidate Dart owners from the live runtime
Good live-runtime moves include:
- runtime artifact dumping when static output is incomplete
- enumerating recovered Dart methods/offsets around the target field
- correlating one field or request family with one small method family
- using runtime visibility to narrow candidate owner methods before lower-level helper tracing

The point is not to dump everything.
The point is to shrink the owner search space.

### Step 5: separate owner from worker
Use simple labels:
- trigger
- bridge
- owner
- worker
- effect

Good owner candidates are usually:
- first Dart/object method that assembles or updates the target field
- first object boundary that turns general state into the exact request artifact
- first method whose output shape predicts the visible field or later consequence

Bad default choices include:
- the first visible Flutter engine helper
- every glue callback
- the lowest-level native digest helper with no direct ownership of inputs
- broad framework init chains that only make execution possible

### Step 6: prove owner vs worker with one compare pair
Use one narrow compare pair:
- target action vs nearby non-target action
- field present vs field absent
- accepted request vs rejected/degraded request
- one small input change that should alter the target field

What you want to learn:
- does the candidate owner change only with the target flow?
- does it predict the target field or consequence better than bridge/native helpers do?
- does one later effect depend on it?

### Step 7: stop at one proved owner and route onward
The workflow is successful when you can rewrite the case as:

```text
iOS shell trigger
  -> Flutter bridge/router
  -> Dart owner
  -> native worker (if any)
  -> one visible consequence
```

At that point, route forward:
- if the owner is request-field generation, continue into signature/preimage recovery
- if the owner is broader native subsystem logic, continue into native proof work
- if the owner is mostly ordinary ObjC / Swift control again, return to the iOS owner note

Do not keep this page open once the owner is proved.

## 5. Practical scenario patterns

### Scenario A: reFlutter/repack path is unstable, but live runtime still works
Pattern:

```text
static rewrite or repack attempt fails or stays fragile
  -> live app still executes target flow
  -> analyst keeps sinking time into rebuild success
```

Best move:
- stop treating rebuild success as mandatory
- dump or inspect the runtime that actually executes
- localize the owner there first

### Scenario B: ObjC shell is readable, but the target field is really Dart-owned
Pattern:

```text
iOS controller / callback visible
  -> Flutter engine routing visible
  -> target field appears later
  -> analyst overcommits to shell or engine layer
```

Best move:
- treat shell and engine as trigger/router candidates first
- prove which Dart-side object/method actually writes or shapes the field

### Scenario C: native digest helper looks decisive, but input ownership is elsewhere
Pattern:

```text
native hash / encode routine easy to see
  -> several callers converge there
  -> only one flow matters
```

Best move:
- move upward until one Dart/object boundary explains why this helper receives these exact inputs
- prefer input ownership over helper visibility

### Scenario D: Flutter target is mixed enough that no single runtime feels trustworthy
Pattern:

```text
iOS shell visible
  -> bridge visible
  -> Dart names partly recovered
  -> native helper also active
  -> analyst cannot tell where to commit
```

Best move:
- choose the boundary that best predicts one visible consequence
- ask which layer first explains the exact field, object, or policy effect you care about
- accept that the answer may still be a Dart owner plus native worker chain rather than a single-layer winner

## 6. Breakpoint / hook placement guidance
Useful anchors include:
- one representative iOS trigger
- one engine/bridge routing point
- one candidate Dart method family near the target field
- one object/state update that narrows inputs
- one native helper only after the owner search space is already small
- one later visible effect proving the chain mattered

If evidence is noisy, anchor on:
- one target field
- one target request family
- one target action and one nearby non-target action
- one visible consequence, not every helper call

## 7. Failure patterns this note helps prevent

### 1. Treating repack success as the goal
Repack/rewrite success is only useful if it shortens the path to a trustworthy owner.

### 2. Treating Flutter engine routing as the owner by default
The engine often routes or hosts the path without owning the decisive artifact.

### 3. Treating the lowest-level native digest helper as the owner
Lower-level helpers frequently consume inputs they do not own.

### 4. Staying trapped in framework setup instead of proving one consequence-bearing method
Framework familiarity can feel like progress while still failing to explain the target field.

### 5. Dumping the live runtime without a frozen flow
Without one target flow and one target artifact, runtime dumps become another swamp.

### 6. Mixing shell, bridge, owner, and worker into one blob
If those roles are collapsed, compare-run reasoning gets much weaker.

## 8. Relationship to nearby pages
- `topics/ios-packaging-jailbreak-and-runtime-gate-workflow-note.md`
  - use first when topology, install/signing path, or runtime gate stability is still unclear
- `topics/ios-objc-swift-native-owner-localization-workflow-note.md`
  - use for the broader iOS owner problem when Flutter/cross-runtime structure is not the decisive complication
- `topics/mobile-signature-location-and-preimage-recovery-workflow-note.md`
  - use when the owner is already narrowed to a request/signature field path
- `topics/native-interface-to-state-proof-workflow-note.md`
  - use when the case has effectively become an ordinary native subsystem proof problem
- `topics/mobile-reversing-and-runtime-instrumentation.md`
  - use for the broader mobile runtime synthesis and execution-assisted replay context

## 9. Minimal operator checklist
Use this note best when you can answer these in writing:
- what single cross-runtime flow am I trying to explain?
- what visible iOS shell trigger starts it?
- what is the first Flutter bridge/router boundary?
- what is my best current Dart owner candidate?
- which native helper is only a worker unless proved otherwise?
- what one later effect would prove the owner mattered?
- which narrower note should take over after the owner is proved?

If you cannot answer those, the case likely still needs broader iOS gate or owner-localization triage first.

## 10. Source footprint / evidence quality note
This note is intentionally workflow-first.

It is grounded by:
- `topics/ios-packaging-jailbreak-and-runtime-gate-workflow-note.md`
- `topics/ios-objc-swift-native-owner-localization-workflow-note.md`
- `topics/mobile-reversing-and-runtime-instrumentation.md`
- `sources/ios-runtime-and-sign-recovery/2026-03-17-sperm-ios-batch-1-notes.md`
- `sources/ios-runtime-and-sign-recovery/2026-03-17-sperm-ios-batch-2-notes.md`
- `runs/2026-03-17-1420-sperm-ios-batch-1.md`
- `runs/2026-03-17-1420-sperm-ios-batch-2.md`
- `runs/2026-03-17-1435-ios-branch-balance-and-ladder-consolidation.md`

The evidence base is sufficient because the claim is conservative:
- repeated iOS Flutter cases show the same owner-localization bottleneck
- static rewrite/repack workflows are useful but not always the best next move
- the durable expert move is to prefer the runtime that actually executes and reduce the case to one consequence-bearing owner

## 11. Bottom line
When a Flutter-shaped iOS target becomes messy, the best next move is often not broader framework surgery.
It is to freeze one flow, separate shell from bridge from Dart owner from native worker, then prove one consequence-bearing owner in the runtime that actually executes.
That single proof usually turns a cross-runtime swamp into a tractable next task.
