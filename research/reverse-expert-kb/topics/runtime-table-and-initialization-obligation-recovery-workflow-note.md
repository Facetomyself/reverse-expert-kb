# Runtime-Table and Initialization-Obligation Recovery Workflow Note

Topic class: concrete workflow note
Ontology layers: protected-runtime practice branch, execution-assisted reduction, runtime-artifact trust recovery
Maturity: structured-practical
Related pages:
- topics/protected-runtime-practical-subtree-guide.md
- topics/anti-tamper-and-protected-runtime-analysis.md
- topics/trace-guided-and-dbi-assisted-re.md
- topics/mobile-reversing-and-runtime-instrumentation.md
- topics/mobile-signing-and-parameter-generation-workflows.md
- topics/decrypted-artifact-to-first-consumer-workflow-note.md
- topics/packed-stub-to-oep-and-first-real-module-workflow-note.md
- topics/runtime-behavior-recovery.md

## 1. Why this page exists
This page exists for a recurring protected-runtime / execution-assisted case that sits between several already-strong KB notes.

The KB already had:
- packed/bootstrap handoff guidance
- decrypted-artifact -> first-consumer guidance
- trace-guided simplification guidance
- mobile signing / parameter-generation guidance

What it still lacked was a compact workflow for the specific middle-state where:
- static dumps or repaired artifacts are visibly incomplete, misleading, or too damaged to trust fully
- runtime memory, initialized tables, or post-init images appear truer than the static view
- emulation or replay is **close but wrong**
- the real remaining bottleneck is not broad algorithm identification, but one missing initialization chain, side-condition command, runtime table family, or environment obligation

A compact operator shape for this problem is:

```text
static artifact looks damaged or under-initialized
  -> live/runtime state contains truer tables, buffers, or initialized images
  -> replay or emulation is almost correct but still drifts
  -> recover the smallest missing initialization obligation or runtime artifact family
  -> externalize one truthful smaller reproduction target
```

This is not the same as:
- generic unpacking
- generic decrypted-artifact recovery
- generic trace collection
- generic mobile signing analysis

It is the practical task of deciding when **executed state is more trustworthy than the repaired static artifact**, and then reducing the case into one missing init/table obligation instead of a larger diary of partial dumps.

## 2. Target pattern / scenario
### Representative target shape
Use this note when most of the following are true:
- a static dump, unpacked image, repaired SO, or decompiled function family exists, but still looks damaged, incomplete, or semantically slippery
- runtime memory, emulator state, live process state, or post-init images expose cleaner tables, arrays, constants, decoded buffers, or object graphs than the static view does
- the analyst can already identify a likely transform family, request-signing path, protected routine, or SDK command family
- offline replay, unidbg-style invocation, emulator reproduction, or partial reimplementation produces outputs that are near-correct, unstable, or only correct under one narrow condition
- the likely missing piece is one smaller runtime obligation such as:
  - one init command sequence
  - one file / process / thread / environment precondition
  - one runtime table or key schedule
  - one initialized image region
  - one side-condition callback or registration step

Representative cases include:
- protected Android crypto where white-box or table-driven transforms become legible only after runtime table extraction
- SDK command-router work where the target command exists, but earlier init commands are still required before outputs become truthful
- Android Flutter or mixed-runtime cases where one Dart/object owner is already plausible, but unidbg- or emulator-shaped replay stays close-but-wrong until one prerequisite command/state bucket, runtime table, or initialized-image boundary is recovered explicitly
- packed or protected native targets where runtime memory contains a truer initialized image than the repaired static dump
- trace-assisted standard-algorithm recognition where memory constants fingerprint the family before control-flow reconstruction is clean
- mobile signing cases where the math looks right, but outputs drift because init state, runtime tables, or side conditions are still missing

### Analyst goal
The goal is **not** to collect every live artifact.
It is to:
- identify which runtime artifact family is currently more trustworthy than the static view
- isolate the smallest initialization obligation still missing from truthful replay or reproduction
- prove one downstream effect depends on that obligation
- hand back one smaller externalizable target such as a reproducible function, dump boundary, table family, or init chain

## 3. The first five questions to answer
Before collecting more dumps or traces, answer these:

1. **What exactly is damaged or untrustworthy in the static view: tables, control flow, code bytes, decoded buffers, object fields, or post-load image state?**
2. **Which live/runtime artifact looks truer: one table family, one initialized region, one command-sequenced state object, one memory-resident key schedule, or one post-init object graph?**
3. **What symptom says the core logic is close but not yet truthful: near-correct output, one wrong branch bucket, one mismatched field, one failed command, or one drift only after init?**
4. **Which missing obligation is most plausible: earlier init command, runtime table extraction, environment precondition, registration side effect, or one file/thread/process assumption?**
5. **What smaller target do I want back from this pass: one truthful runtime table set, one minimal init chain, one initialized-image dump point, one side-condition checklist, or one externally reproducible transform core?**

If these remain vague, the workflow usually degenerates into more repair work on the static artifact even though executed state is already the better evidence surface.

## 4. Core claim
When static artifacts are damaged or under-initialized, the right unit of progress is often:
- one runtime artifact family that is more trustworthy than the static view
- plus one missing initialization obligation that explains why replay is still drifting

A practical sequence is:

```text
damaged / misleading static artifact
  -> choose one runtime artifact family to trust
  -> classify one near-correct or drift symptom
  -> isolate one missing initialization obligation
  -> prove one downstream output/effect depends on it
  -> externalize one smaller truthful target
```

The key distinction is:
- **algorithm family recognition** is not enough
- **artifact visibility** is not enough
- **almost-correct replay** is not enough

The useful milestone is one truthful runtime artifact plus one proved init obligation.

## 5. What counts as a trustworthy runtime artifact
A trustworthy runtime artifact is the smallest live-state object that predicts later truthful behavior better than the static artifact does.

Good artifact families include:
- one table family actually read during the live transform
- one memory-resident key schedule or derived array used after init
- one initialized image region that stays stable enough to dump and reuse
- one decoded/configured object graph reachable only after the right init chain
- one command-router state bucket that becomes valid only after prerequisite calls

Bad artifact choices usually are:
- a huge indiscriminate memory dump with no narrow consumer plan
- a damaged repaired binary treated as truth because it is easier to read offline
- one runtime blob captured too early, before the relevant init chain completes
- one almost-correct offline result treated as proof that nothing important is missing

## 6. Practical workflow

### Step 1: anchor the drift symptom first
Start from one concrete symptom such as:
- output is almost correct but one field, round, or branch family is wrong
- target command returns a result only after some hidden earlier call sequence in the app
- repaired static tables disagree with live memory reads
- decompiled logic looks plausible, but execution uses memory-resident constants not visible statically
- one initialized object or image region exists in memory but not in the dump

Good scratch note:

```text
drift symptom:
  external replay matches structure but one trailing field family is wrong

working suspicion:
  missing init command or runtime table family, not wrong core transform family
```

### Step 2: choose one runtime artifact family to trust
Do not collect all live state.
Pick one artifact family such as:
- lookup tables
- round constants
- initialized image or code region
- decoded config / object graph
- command-router/session state
- one file-backed or environment-derived init object

Practical rule:
- prefer the artifact family that is directly consumed near the drift symptom
- prefer artifacts that can be re-read, dumped, or watchpointed narrowly

### Step 3: classify the missing obligation
Force the case into one obligation class first:
- **init-sequence obligation**: prerequisite commands/functions must run first
- **runtime-table obligation**: live tables or arrays differ from the static view
- **initialized-image obligation**: correct bytes only exist after loader/decrypt/init work
- **environment obligation**: file, process name, thread, timing, device, or other side condition is still missing
- **registration/callback obligation**: one listener/registration side effect is required before truthful behavior appears

This prevents endless mixed hypotheses.

### Step 4: cut one narrow proof window
Choose the smallest window that still contains:
- one relevant init step or live artifact materialization
- one consumer boundary
- one drift symptom or later output comparison

Typical windows:
- last prerequisite command -> target command
- table materialization -> first table-consuming round/function
- initialized image creation -> first ordinary consumer routine
- environment setup -> first behavior divergence

If the window spans whole-app startup or giant memory snapshots, it is probably too broad.

### Step 5: label regions by role before exact semantics
Reduce the window into roles such as:
- static artifact failure surface
- live artifact materialization
- init obligation boundary
- first consumer of live artifact
- drift symptom or corrected output boundary

Example reduction:

```text
region A = damaged static AES-like tables in repaired SO
region B = live memory table materialization during startup
region C = prerequisite SDK init command family
region D = target command consumer of table/state bundle
region E = output comparison boundary
```

### Step 6: force one missing-obligation hypothesis
Pick the single smallest hypothesis that could explain the drift.
Typical examples:
- one earlier command ID must run first
- one file read populates a runtime table family
- one thread/process name affects later initialization
- one constructor/init callback registers the real state object
- one live table extraction is required because the static dump is incomplete

Practical rule:
- prefer the hypothesis that explains **why outputs are close** instead of why everything is broken
- “close but wrong” usually points to missing init/side conditions before wrong core math

### Step 7: prove one downstream dependency
Use one narrow proof move such as:
- compare replay before/after the suspected init chain
- compare static-table output vs runtime-table output on the same input
- watch one consumer argument/object after the init step and confirm it changes only when the obligation is satisfied
- dump one initialized image/table family after the relevant boundary and confirm reuse becomes truthful
- align one near-correct and one corrected run to show the first stable divergence disappears once the obligation is satisfied

The goal is not a perfect emulator.
It is one proof that the chosen runtime artifact and init obligation explain the behavioral drift.

### Step 8: hand back one smaller truthful target
The workflow should end with one or more of:
- one runtime table family worth preserving and reusing
- one minimal init chain worth documenting and replaying
- one initialized-image dump point worth standardizing
- one side-condition checklist for truthful reproduction
- one smaller externalized transform core that now works because the missing obligation was isolated

If the result is only “runtime looked different from static,” the reduction is incomplete.

## 7. Common obligation families

### A. Runtime-table extraction obligation
Use when:
- static tables/arrays are damaged, obfuscated, or incomplete
- live memory exposes the real values actually consumed

Why it helps:
- it converts vague deobfuscation or crypto reconstruction into one concrete artifact-recovery task

### B. Minimal init-command chain obligation
Use when:
- large SDK/router entrypoints are callable, but outputs stay wrong or inert until earlier commands run

Why it helps:
- it reframes “the emulator is broken” into one smaller sequencing problem

### C. Initialized-image dump obligation
Use when:
- the repaired static image is less truthful than the post-init mapped memory state

Why it helps:
- it yields a reusable static target without pretending the original dump was enough

### D. Environment/side-condition obligation
Use when:
- almost-correct execution depends on one file, process, timing, thread, or registration condition

Why it helps:
- it prevents wasting time rewriting core logic that was already mostly right

### E. Memory-fingerprint-first algorithm recognition obligation
Use when:
- control flow is still messy, but memory constants and live access patterns already fingerprint the algorithm family

Why it helps:
- it allows a truthful reduction path before full CFG cleanup exists

## 8. Representative scratch schemas

### Minimal runtime-artifact reduction note
```text
drift symptom:
  ...

static artifact failure:
  ...

trusted runtime artifact family:
  ...

missing obligation class:
  ...

first consumer boundary:
  ...

next truthful target:
  ...
```

### Init-chain comparison note
```text
baseline run missing:
  ...

added init obligation:
  ...

first stable corrected boundary:
  ...

remaining drift:
  ...
```

### Tiny thought model
```python
class RuntimeArtifactInitReduction:
    drift_symptom = None
    static_failure = None
    runtime_artifact_family = None
    missing_obligation = None
    first_consumer = None
    next_truthful_target = None
```

## 9. Failure modes

### Failure mode 1: endless static repair, little behavioral improvement
Likely cause:
- executed state is already the better evidence surface, but the workflow still trusts the repaired artifact first

Next move:
- force one runtime artifact family choice and one drift symptom before more static cleanup

### Failure mode 2: giant memory dumps, little leverage
Likely cause:
- live-state collection was not tied to one consumer boundary or one obligation class

Next move:
- narrow to one artifact family and one first consumer

### Failure mode 3: replay is close but wrong, and the core math keeps being rewritten
Likely cause:
- missing initialization or side conditions are being mistaken for wrong algorithm identification

Next move:
- test init-sequence, runtime-table, and environment obligations before rewriting the transform again

### Failure mode 4: extracted runtime artifact still fails offline
Likely cause:
- artifact captured too early or without the true prerequisite state

Next move:
- move the capture boundary later and re-check the init chain

### Failure mode 5: init sequence grows endlessly
Likely cause:
- prerequisite calls are being collected without proving which one changes later behavior

Next move:
- reduce the chain to the smallest step that corrects the drift symptom or first stable divergence

## 10. How this page connects to the rest of the KB
Use this page when the bottleneck is:
- **runtime state is truer than the static artifact, and the remaining task is isolating one missing initialization or side-condition obligation**

Then route outward based on what remains hard:
- to `topics/packed-stub-to-oep-and-first-real-module-workflow-note.md` when the main uncertainty is still the post-unpack handoff or dump boundary
- to `topics/decrypted-artifact-to-first-consumer-workflow-note.md` when the runtime artifact is already trustworthy and the missing step is now the first ordinary consumer
- to `topics/trace-guided-and-dbi-assisted-re.md` when trace/DBI surface choice or trace-slice strategy is still the real problem
- to `topics/mobile-signing-and-parameter-generation-workflows.md` when the broader target is mobile request shaping and the isolated init/table issue should be folded back into a generation-chain model
- to `topics/runtime-behavior-recovery.md` when broader evidence-trust strategy still dominates

## 11. What this page adds to the KB
This page adds a missing practical bridge for a recurring operator bottleneck:
- not just artifact recovery
- not just packed-runtime handoff
- not just trace collection
- not just mobile signing theory

Instead it emphasizes:
- trust live/runtime artifacts over damaged static views when justified
- treat near-correct replay as an init-obligation clue
- recover one truthful runtime artifact family
- prove one missing init/side-condition obligation
- externalize one smaller working target

That strengthens the protected-runtime branch with a concrete execution-assisted workflow rather than another abstract family label.

## 12. Source footprint / evidence note
Grounding for this page comes from:
- `topics/protected-runtime-practical-subtree-guide.md`
- `topics/anti-tamper-and-protected-runtime-analysis.md`
- `topics/trace-guided-and-dbi-assisted-re.md`
- `topics/mobile-reversing-and-runtime-instrumentation.md`
- `topics/mobile-signing-and-parameter-generation-workflows.md`
- `topics/decrypted-artifact-to-first-consumer-workflow-note.md`
- `topics/packed-stub-to-oep-and-first-real-module-workflow-note.md`
- `sources/mobile-runtime-instrumentation/2026-03-17-sperm-android-protected-runtime-batch-7-notes.md`
- `sources/protected-runtime/2026-03-17-decrypted-artifact-to-first-consumer-notes.md`

The page intentionally stays conservative:
- it does not claim runtime state always beats the static artifact
- it does not assume near-correct replay always means missing init
- it treats runtime-artifact trust recovery as a workflow for finding one smaller truthful target when static evidence is currently the weaker surface

## 13. Topic summary
Runtime-table and initialization-obligation recovery is a practical workflow for cases where static artifacts are damaged or under-initialized, but live/runtime state reveals truer tables, initialized images, or prerequisite state.

It matters because many hard protected-runtime and mobile-signing cases are not blocked by unknown core math anymore.
They are blocked by one missing runtime artifact or one missing init obligation that explains why the analysis is close, but not yet truthful.
