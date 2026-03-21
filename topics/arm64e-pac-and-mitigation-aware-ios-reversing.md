# arm64e / PAC and Mitigation-Aware iOS Reversing

Topic class: concrete workflow note
Ontology layers: mobile runtime practice, iOS practical ladder continuation, mitigation-aware analysis
Maturity: structured-practical
Related pages:
- topics/mobile-reversing-and-runtime-instrumentation.md
- topics/mobile-protected-runtime-subtree-guide.md
- topics/ios-practical-subtree-guide.md
- topics/ios-packaging-jailbreak-and-runtime-gate-workflow-note.md
- topics/ios-trust-path-and-pinning-localization-workflow-note.md
- topics/ios-objc-swift-native-owner-localization-workflow-note.md
- topics/ios-chomper-owner-recovery-and-black-box-invocation-workflow-note.md
- topics/runtime-table-and-initialization-obligation-recovery-workflow-note.md
- topics/observation-distortion-and-misleading-evidence.md
- topics/trace-guided-and-dbi-assisted-re.md

## 1. Why this page exists
This page exists because the KB already recognized a recurring modern iOS operator gap:
- the case is clearly iOS-shaped
- ordinary packaging / jailbreak / trust-path / owner-localization work has already reduced the broad uncertainty
- but the remaining instability or crash behavior now intersects with arm64e-era mitigation behavior rather than ordinary owner/path confusion

The branch had repeated references to PAC/arm64e-aware continuation as an area worth its own page, but it did not yet have a practical workflow note.

That gap matters because modern iOS reversing increasingly hits cases where the next useful question is not just:
- which method owns the behavior?
- which trust callback fires?
- which request serializer writes the field?

Instead it becomes:
- is the current failure actually a PAC-auth failure or a signed-pointer corruption symptom?
- is the static view lying because authenticated stubs, tail-call auth checks, dyld cache extraction choices, or mitigation-aware decompiler cleanup distorted the visible control flow?
- is replay almost correct, with the remaining error being one missing init/context obligation that only becomes visible once authenticated pointers are respected?

This page is therefore about the narrower practical continuation:
- **when a modern iOS case has already become mitigation-aware enough that PAC / arm64e behavior must be treated as part of the workflow, not as abstract background theory**

## 2. When to use this page
Use this page when most of the following are true:
- the case is already clearly in the iOS practical branch
- one representative target path, crash site, or replay path is already visible enough to study
- the remaining confusion increasingly looks like authenticated-pointer or arm64e-era runtime behavior rather than broad environment uncertainty
- the static view and the runtime view disagree in ways that ordinary owner/path explanations no longer resolve cleanly
- tail-call / thunk / trampoline / dyld-cache reality now matters to whether the next proof is trustworthy
- a near-correct replay, patch, or hook keeps failing at an indirect-branch / return / callback / vtable-like boundary

Representative cases:
- a call path looks straightforward statically, but the runtime keeps dying near an authenticated branch or return boundary
- a recovered function pointer, callback, selector-adjacent target, or vtable-like slot appears right structurally, but using it still yields pointer-auth-style failure
- a dyld shared cache function family is clearly involved, but the current extraction / symbol / address workflow is not trustworthy enough to support the next mitigation-aware step
- decompiler output is cluttered by explicit auth-check sequences before tail calls, and the analyst is at risk of mistaking mitigation scaffolding for business logic
- replay or black-box invocation is close enough that the remaining problem is likely one missing runtime-table / init-context obligation interacting with signed pointers

Do **not** use this page when the case is still dominated by:
- traffic visibility problems
- environment normalization or deployment incoherence
- broad jailbreak / packaging gate uncertainty
- basic trust-path localization uncertainty
- first owner-localization uncertainty

In those cases, stay with the earlier iOS ladder pages first.

## 3. Core claim
On modern iOS, PAC / arm64e awareness is an analysis-discipline issue before it becomes a deep hardware-research issue.

The practical goal is usually **not**:
- fully reverse Apple’s PAC implementation
- explain every architectural detail of signed pointers
- turn each PAC-bearing function into a mitigation paper

The practical goal is:
- keep dyld-cache / stub / thunk reality truthful
- separate mitigation scaffolding from business logic
- stop misclassifying signed-pointer failures as generic memory corruption or generic owner bugs
- prove one consequence-bearing continuation that survives PAC-aware reality

The workflow usually looks like:

```text
iOS case already reduced into one representative path
  -> confirm this is now a mitigation-aware boundary, not a broad branch-selection problem
  -> choose the truthful code view (dyld cache / extracted image / debugger / decompiler settings)
  -> classify whether the failure is auth-boundary, signed-pointer corruption, or missing-init / wrong-context drift
  -> reduce one authenticated target or callback path conservatively
  -> only then continue into owner proof, replay repair, or narrower init-obligation recovery
```

## 4. First decide what kind of PAC-shaped problem this is

### A. View problem
The code view itself is not truthful enough yet.
Common signals:
- important system code only exists meaningfully in the dyld shared cache, not as ordinary on-disk files
- symbols, addresses, or call edges disagree across extracted images, debugger state, and the cache
- decompiler output is polluted by mitigation scaffolding that obscures the real tail target or semantic edge

Typical next move:
- fix the code view before making stronger ownership or crash claims

### B. Failure classification problem
The runtime dies or diverges near an authenticated boundary, but the actual class of failure is still unclear.
Common signals:
- EXC_BAD_ACCESS / data-abort-like behavior appears near indirect branches, returns, callbacks, or virtual dispatch
- the same structural path “should work,” yet the real device rejects it in a way that looks sharper than ordinary argument mismatch
- a pointer-bearing slot appears plausibly correct but behaves as though context/diversifier/signing assumptions are wrong

Typical next move:
- classify whether the problem is really PAC-auth / signed-pointer corruption / wrong-context use, rather than generic corruption handwaving

### C. Replay-is-close problem
Replay, black-box invocation, or reduced calling is nearly working.
Common signals:
- the target function family is probably correct
- the failure happens late enough that broad owner search should stop
- the remaining gap feels like one missing init obligation, loaded image, table entry, or authenticated context boundary

Typical next move:
- use this page only long enough to stop misdiagnosing the failure, then move into `runtime-table-and-initialization-obligation-recovery-workflow-note`

## 5. Truth surfaces to trust first

### A. Dyld shared cache first for system truth
Modern iOS system code often lives meaningfully in the dyld shared cache rather than as ordinary standalone binaries. Practical dyld-cache guidance and current iOS reversing material both reinforce that cache-first reality.

Operational consequence:
- if the path crosses system libraries, private frameworks, closures, trampolines, or cache-backed images, treat the dyld shared cache as a primary truth surface
- do not overtrust stale extracted copies or partial symbol views when cache-backed truth is the real object

What to preserve:
- which cache / firmware / OS build the analysis refers to
- which extracted image or tooling view came from that cache
- which address translation or slide assumptions were used

### B. Runtime anchors beat pretty decompilation
If the decompiler view and runtime behavior disagree, prefer the cheapest truthful runtime anchor:
- one branch target
- one callback registration site
- one authenticated return boundary
- one before/after compare pair near the failure site

Do not let a clean-looking pseudo-C path outrank a runtime anchor just because the mitigation scaffolding was hidden.

### C. Keep tool cleanup separate from semantic proof
Recent tooling and community material show that explicit arm64e PAC checks before tail calls may sometimes be removable analysis clutter rather than analyst-relevant business logic.

That does **not** mean:
- all PAC-related sequences are irrelevant
- the decompiler should be trusted blindly after cleanup

It means:
- use cleanup to reduce clutter
- but preserve a path back to the original auth-bearing sequence when crash classification or edge proof depends on it

## 6. Practical workflow

### Step 1: freeze one representative failing or unstable path
Pick one path that is already good enough to study.
Examples:
- one callback path that crashes only on-device
- one reduced invocation that is nearly correct
- one indirect call edge where static and runtime views disagree
- one tail-call / thunk family where the visible target may be distorted by auth logic

Do not widen immediately into all PAC-looking sites.

### Step 2: decide whether the current blocker is view, failure class, or replay-close
Ask:
- is the code view still untrustworthy?
- is the failure class itself unclear?
- or is replay already close, with one narrower context/init gap left?

This keeps the page from becoming a PAC-tourism detour.

### Step 3: make the code view truthful enough
For the chosen path, freeze:
- the exact firmware / iOS build / cache source
- the image or framework family involved
- the address/slide relationship used by the debugger or extracted view
- any decompiler setting or cleanup that changes whether PAC scaffolding is shown

Minimal goal:
- future-you can answer “which exact code view was trusted for this claim?”

### Step 4: classify the failure conservatively
Use the smallest claim that the evidence supports.

Good:
- the path fails at an authenticated indirect-boundary and the current pointer/context pair is not yet trusted
- the crash pattern is PAC-consistent enough that generic owner/path claims should pause
- the replay path is probably correct up to the final authenticated callback handoff

Weak:
- PAC is definitely the whole problem
- the hardware mitigation proves the target owner
- every nearby corruption symptom must be pointer authentication

A useful practical distinction is:
- **ordinary owner/path bug** — wrong function family, wrong callback, wrong serializer, wrong state owner
- **signed-pointer/context bug** — the family is plausibly right, but the exact pointer/context/initialization state still is not
- **tool/view bug** — the analyst is arguing from an untrustworthy code view

### Step 5: reduce one authenticated boundary
Choose one only:
- one callback target
- one virtual/indirect dispatch boundary
- one authenticated return/tail-call handoff
- one cache-backed branch target family

For that boundary, preserve:
- the visible static site
- the runtime landing evidence
- the failure/no-failure compare condition
- the current best explanation of what remains missing

### Step 6: route out of this page quickly
Once the mitigation-aware confusion is reduced, leave this page.
Typical exits:
- back to `ios-objc-swift-native-owner-localization-workflow-note` if the real owner is still not proved
- to `ios-chomper-owner-recovery-and-black-box-invocation-workflow-note` if the path is already owner-plausible and callable proof is next
- to `runtime-table-and-initialization-obligation-recovery-workflow-note` if the path is replay-close but one narrower init/context/table gap remains
- to `observation-distortion-and-misleading-evidence.md` if tooling cleanup or mitigation scaffolding is making the evidence itself misleading

## 7. Concrete operator heuristics

### A. Do not confuse signed-pointer failure with ordinary memory-corruption storytelling by default
A PAC-shaped crash near an indirect control boundary should raise the possibility that:
- the target family is correct but the pointer is not valid in this context
- the callback/slot was copied, replayed, or reconstructed outside the context that authenticates it
- one missing init/image/table obligation means the final pointer-bearing object is structurally plausible but still wrong

### B. Do not confuse PAC scaffolding with the business owner
If explicit auth-check sequences dominate the decompiler output, resist the temptation to promote them into semantic ownership.
The real owner may still be:
- the caller that installed the callback
- the state writer that selected the target
- the runtime table or init path that materialized the authenticated object
- the downstream consumer after the auth boundary succeeds

### C. Do not prove replay too broadly
When replay is almost correct, avoid building a giant harness because the last failure smells mitigation-aware.
Prefer:
- one narrower missing table family
- one loaded-image dependency
- one callback/context materialization edge
- one authenticated-object provenance check

### D. Preserve the exact build context
arm64e/PAC observations age badly if detached from build context.
Freeze at least:
- OS / firmware version
- cache source or image source
- architecture slice assumptions
- whether the result came from simulator, device, extracted cache, or live debugger view

## 8. Common mistakes this page prevents
This page is meant to prevent several recurring mistakes:
- treating PAC/arm64e as abstract background and then making overly strong claims from untrustworthy static views
- treating every crash near an indirect boundary as generic corruption without testing signed-pointer/context explanations
- treating mitigation scaffolding as the real owner of behavior
- widening into hardware-theory reading when one narrower code-view or init-obligation fix would unblock the case
- continuing broad owner search after the case has already become a replay-close mitigation-aware problem

## 9. Stop rule
Leave this page once one of the following becomes true:
- one truthful code view now exists and the real blocker is again ordinary owner localization
- one authenticated boundary is reduced enough that the next bottleneck is controlled replay or init-obligation repair
- the evidence is strong enough to say the static view was misleading and a runtime-first path should dominate

Do **not** keep expanding this page into a full PAC theory compendium.
Its job is to keep the iOS practical ladder honest once mitigation-aware boundaries become the immediate bottleneck.

## 10. Source-backed practical takeaways used here
This page is grounded conservatively in a small practical source set:
- Apple’s pointer-authentication documentation confirms the arm64e / PAC baseline and why authenticated pointers are normal on modern Apple platforms
- current dyld shared cache tooling/docs and practitioner reversing material reinforce that cache-backed system truth matters operationally for modern iOS work
- current iOS dyld/reversing practice notes reinforce that DSC navigation and extraction choices are part of basic workflow, not exotic add-ons
- current Binary Ninja arm64e PAC cleanup material reinforces that some explicit auth-check sequences before tail calls are analysis clutter rather than the analyst’s real target

This is enough for a practical workflow note.
It is **not** used here to overclaim hidden hardware internals or universal crash semantics.
