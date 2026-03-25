# Exception-Handler-Owned Control-Transfer Workflow Note

Topic class: concrete workflow note
Ontology layers: protected-runtime practice branch, anti-debug/anti-tamper continuation, control-transfer recovery
Maturity: structured-practical
Related pages:
- topics/anti-tamper-and-protected-runtime-analysis.md
- topics/protected-runtime-practical-subtree-guide.md
- topics/anti-instrumentation-gate-triage-workflow-note.md
- topics/protected-runtime-observation-topology-selection-workflow-note.md
- topics/integrity-check-to-tamper-consequence-workflow-note.md
- topics/runtime-behavior-recovery.md
- topics/native-binary-reversing-baseline.md

## 1. Why this page exists
This page exists for a recurring protected-runtime bottleneck where the analyst has already localized anti-debug, anti-tamper, or odd breakpoint behavior far enough to suspect that the real ownership of control transfer sits inside an exception or signal path.

The KB already had useful coverage for:
- broad anti-instrumentation gate triage
- broader observation-topology selection
- integrity-check-to-consequence reduction

What it still lacked was one compact continuation for the narrower case where:
- the decisive branch is not an ordinary direct call edge
- breakpoints, traps, access violations, guard faults, or signal delivery are being used as the real dispatch surface
- normal linear control-flow reading keeps looking incomplete or misleading
- the next useful move is to prove one exception-owned transfer boundary and one downstream consequence-bearing handler outcome

A compact operator shape for this case is:

```text
odd trap/fault/breakpoint behavior appears
  -> decide whether the exception/signal path is real dispatch or only noise
  -> recover the first handler-registration, dispatcher-side landing, or ownership boundary
  -> recover the first context rewrite / resume / branch consequence
  -> hand back one ordinary post-handler target
```

A Windows/Linux-specific refinement worth preserving is:
- do not stop at proving that VEH/SEH exists, or that `sigaction`/signal registration exists
- the smallest truthful boundary is often one of:
  - vectored registration that already predicts the later branch
  - dispatcher-side landing in `KiUserExceptionDispatcher`
  - `RtlDispatchException` / `RtlLookupFunctionEntry` / dynamic-function-table lookup into one concrete region
  - one runtime-installed function-table callback that explains why static unwind ownership stays incomplete
  - one `SA_SIGINFO` handler whose `ucontext_t` edits or resume target already predict the later branch
- once one of those boundaries plus one consequence-bearing resume/state action is good enough, leave broad exception theory and hand the case back to ordinary route/state proof, integrity consequence proof, or observation-topology repair
- practical stop rule: dispatcher landing by itself is still infrastructure; `sigaction` registration by itself is still infrastructure; stop only once one owning lookup/registered range or one concrete context/resume mutation is preserved well enough to predict later behavior

This is not the same as:
- a general SEH/VEH tutorial
- a debugger-usage note
- a full anti-debug taxonomy
- a generic crash triage page

It is the practical task of reducing handler-owned control transfer into one re-findable boundary that makes later behavior ordinary enough to continue elsewhere in the KB.

## 2. Target pattern / scenario
### Representative target shape
Use this note when most of the following are true:
- control flow looks incomplete because visible direct branches do not explain later execution
- `int3`, single-step, page-guard, access-violation, illegal-instruction, or similar exception-triggering mechanisms appear relevant
- Windows SEH/VEH, dispatcher-side landing, dynamic unwind metadata, or Linux signal handlers look like they may own the meaningful branch
- hardware-breakpoint or trap-driven hooks appear in the target or in the observed protection behavior
- the useful next output is one proved handler-owned transfer path, not a catalog of all exception APIs

Representative cases include:
- Windows targets that deliberately route anti-debug or hidden dispatch through VEH/SEH and resume execution after context edits
- protected code that uses `int3`, page-guard, or debug-register-triggered traps as an indirect dispatcher surface
- Windows cases where registration is known but the first stable practical anchor is `KiUserExceptionDispatcher` or `RtlDispatchException`
- Linux targets where `SIGTRAP`, `SIGSEGV`, or similar signal delivery is part of the anti-debug or concealed control-transfer story
- cases where ordinary breakpointing makes behavior look broken because the target itself is using exception delivery as a control mechanism

### Analyst goal
The goal is **not** to document every handler.
It is to:
- decide whether exception/signal delivery is actually owning a meaningful branch
- isolate one registration/lookup/landing boundary plus one first consequence-bearing handler action
- prove how execution resumes or diverts afterward
- hand back one quieter post-handler target for ordinary static or runtime follow-up

## 3. The first five questions to answer
Before broadening into more trace collection or more anti-debug folklore, answer these:

1. **What is the smallest symptom suggesting handler-owned control transfer: invisible branch, odd resume address, swallowed breakpoint, fake crash, or trap-only path?**
2. **What family likely owns the dispatch: Windows VEH, Windows SEH/unwind metadata, dispatcher-side landing plus lookup, dynamic function-table callback, Linux signal handler, or debugger-register/page-guard trap logic?**
3. **Where is the first ownership boundary: handler registration, dispatcher-side landing, exception-directory/unwind lookup, signal registration, or handler callback installation?**
4. **What exact consequence matters: context rewrite, instruction-pointer skip, state-flag write, alternate callback, or later integrity verdict?**
5. **What should this pass return: a post-handler ordinary target, an anti-debug continuation, an integrity continuation, or a broader observation-topology change?**

If these remain vague, the case usually degenerates into either endless exception-mechanism reading or brittle breakpoint experiments.

## 4. Core claim
When protection or hidden dispatch is exception-owned, the right unit of progress is often:
- one first handler-ownership boundary
- plus one first consequence-bearing context or state change

A practical sequence is:

```text
anchor the smallest trap/fault symptom
  -> classify the handler family
  -> find the first registration, landing, or lookup boundary
  -> prove one context/state consequence
  -> continue from the resumed or redirected ordinary target
```

The key distinction is:
- **seeing exception APIs** is not enough
- **seeing a trap instruction** is not enough
- **knowing the program crashes under breakpoints** is not enough

The useful milestone is one proved handler-owned transfer path.

## 5. Common handler-owned families
### A. VEH-first dispatch on Windows
Use when:
- vectored handlers are registered early and appear to see the exception before ordinary structured handlers
- the case looks like a global dispatch layer rather than a local function-scoped exception block

Typical clues:
- `AddVectoredExceptionHandler` / `SetUnhandledExceptionFilter`
- early handler registration before protected activity
- resume decisions driven by `ContextRecord`

Why it helps:
- it separates process-wide exception-routing logic from ordinary local cleanup-style exception use

### B. Dispatcher-side landing and unwind lookup on Windows
Use when:
- registration alone is too abstract and the next truthful object is the dispatcher-side landing where user-mode exception ownership becomes re-findable
- the analyst keeps seeing trap or fault arrival, but still needs one stable landing before arguing about which handler or unwind region matters
- `KiUserExceptionDispatcher`, `RtlDispatchException`, `RtlLookupFunctionEntry`, or related unwind lookup surfaces explain the case better than more API-name collection

Typical clues:
- recurring arrival at `KiUserExceptionDispatcher`
- a useful breakpoint or trace boundary at `RtlDispatchException`
- one `RUNTIME_FUNCTION` or dynamic-function-table lookup that narrows the owning region
- runtime-specific stack/layout handling that makes dispatcher-side landing more truthful than broad handler enumeration

Why it helps:
- it gives the analyst one smaller re-findable landing between vague “VEH/SEH exists” wording and a concrete handler-owned branch proof
- it is often the best stop point when registration is known but handler ownership is still too diffuse

### C. SEH / unwind-metadata-owned local transfer
Use when:
- visible try/except style control is present or unwind metadata points to handler-owned behavior
- x64 exception-directory / unwind entries or x86 frame-linked handlers appear to explain an otherwise missing branch

Typical clues:
- exception directory / `RUNTIME_FUNCTION` / `UNWIND_INFO`
- handler lookup through unwind metadata
- one specific function region whose exceptional path owns the real decision

Why it helps:
- it focuses the analyst on the exact function-region ownership boundary instead of wider process-global handler noise

### D. Dynamic-function-table or generated-code exception ownership
Use when:
- ordinary static exception metadata is incomplete, but the runtime appears to install dynamic function tables or callbacks
- generated or relocated code owns the meaningful exception path
- dispatcher-side lookup keeps succeeding for PCs that have no convincing static ownership in the original image

Typical clues:
- `RtlInstallFunctionTableCallback`
- `RtlAddFunctionTable` / `RtlAddGrowableFunctionTable`
- `RtlLookupFunctionEntry` repeatedly resolving into callback-owned or runtime-added regions
- code regions whose unwind ownership appears only at runtime
- debugger or stack-unwind behavior only making sense after the dynamic table range is installed

Why it helps:
- it explains why static PE metadata alone cannot fully account for exception-owned transfer
- it gives a concrete stop rule: once one runtime-installed range plus one later resume/consequence edge is proved, do not keep expanding broad unwind theory

### E. Signal-handler-owned control transfer on Linux
Use when:
- `SIGTRAP`, `SIGSEGV`, `SIGILL`, or similar signals appear as meaningful execution steps rather than mere crashes
- signal registration and handler-side context edits explain later behavior better than ordinary call flow
- `SA_SIGINFO` delivery exposes a usable `ucontext_t` boundary where the resume target or register edits can be compared directly

Typical clues:
- `sigaction` or related registration
- `SA_SIGINFO` handlers with a third-argument context pointer
- `ucontext_t`/context edits in the handler
- traced-vs-untraced or breakpoint-vs-no-breakpoint divergence through signal delivery
- a faulting instruction that only becomes behaviorally meaningful after the handler changes RIP/PC-like resume state or a small state bucket

Why it helps:
- it separates real signal-owned dispatch from generic crash handling or generic ptrace stories
- it preserves the practical stop rule that `sigaction` visibility alone is not consumer proof; the useful boundary is one resume-target or state mutation that predicts later behavior

### F. Trap-triggered hook or anti-debug dispatch
Use when:
- page-guard, debug-register, single-step, or `int3`-style events are themselves the transfer surface
- the target or a surrounding protection layer turns hardware/debug events into its own indirect branch mechanism

Typical clues:
- debug registers / page-guard / single-step setup
- handler logic that rewrites the resume address or skips bytes
- swallowed or repurposed breakpoints

Why it helps:
- it keeps the analyst from reading the trigger instruction as the whole story when the real ownership sits in the follow-on handler and resume logic

## 6. Practical workflow
### Step 1: anchor the smallest non-ordinary symptom
Write one explicit sentence such as:

```text
Earliest symptom:
  the expected direct call edge never appears, but an `int3`/trap fires and execution later resumes at a non-fallthrough address.
```

Good symptom shapes:
- invisible branch explained only after an exception
- breakpoint swallowed or misdirected
- fake crash that actually resumes into real work
- resume address skip or context rewrite
- protected action only happening when the handler path is intact

### Step 2: choose one handler family first
Force the case into the smallest plausible family:
- VEH-first global dispatch
- dispatcher-side landing / unwind lookup
- SEH / unwind-local transfer
- dynamic function-table ownership
- Linux signal-handler ownership
- trap-triggered hook / anti-debug dispatch

Do this before reading every exception mechanism in the platform.

### Step 3: isolate one ownership boundary
Choose the smallest object that proves who owns the path, such as:
- one `AddVectoredExceptionHandler` registration
- one dispatcher-side landing at `KiUserExceptionDispatcher` or one useful breakpoint/trace boundary at `RtlDispatchException`
- one `RUNTIME_FUNCTION` / `UNWIND_INFO` region or `RtlLookupFunctionEntry` result
- one `RtlInstallFunctionTableCallback` site or one `RtlAddFunctionTable` / `RtlAddGrowableFunctionTable` registration that truthfully owns the generated-code region
- one `sigaction` registration
- one debug-register/page-guard setup site plus the first consuming handler

Practical rule:
- prefer the earliest boundary that still predicts the later odd control transfer
- if registration exists but still feels too broad, drop to dispatcher-side landing or one concrete unwind lookup rather than collecting more exception APIs
- if static exception metadata looks incomplete but dispatcher-side lookup keeps recurring, treat dynamic-function-table ownership as a first-class explanation instead of as a documentation footnote
- prefer one concrete ownership site over a broad list of exception-adjacent helpers

### Step 4: prove one consequence-bearing handler action
Choose the smallest action that turns the handler from infrastructure into behavior:
- instruction pointer / resume address rewrite
- state flag or verdict bucket write
- first alternate callback or worker handoff
- byte skip / trampoline-like continuation
- integrity-result reduction or debugger verdict propagation

If the result is only “the target uses SEH/VEH,” the pass is incomplete.

### Step 5: define one minimal compare pair
Useful compare pairs include:
- trap-triggering input vs neighboring non-triggering input
- with breakpoint vs without breakpoint
- handler active vs registration suppressed/altered in a controlled experiment
- faulting path vs non-faulting path
- traced vs untraced when signal/trap ownership is suspected
- page-guard first hit vs re-armed next-step behavior when the visible trigger is not yet the meaningful branch
- hardware-breakpoint-fired path vs same path after debug-register state changes when the handler appears to rewrite resume context rather than merely observe the event

Scratch form:

```text
compare pair:
  ...
first ownership boundary to watch:
  ...
resume or downstream effect to compare:
  ...
```

### Step 6: hand back one ordinary post-handler target
Once one handler-owned transfer path is proved, route the case deliberately:
- to **anti-instrumentation / anti-debug continuation** when the handler result is still basically debugger detection or observation rejection
- to **integrity consequence continuation** when the handler reduces into a tamper verdict or consequence bucket
- to **ordinary native route/state proof** when the resumed target is now a quieter ordinary consumer or worker
- to **broader observation-topology selection** only when the current posture still fundamentally distorts the case even after the handler path is understood

## 7. Representative scenario families
### A. VEH rewrites `ContextRecord` and resumes after a trap
Use when:
- the program appears to break or fault, but the real protected action only becomes visible after the vectored handler edits the saved context and resumes elsewhere

Why it helps:
- it turns a spooky anti-debug impression into one explicit resume-edge proof problem

### B. Dispatcher-side landing is the first truthful Windows anchor
Use when:
- handler registration is already known or strongly suspected, but the analyst still needs one re-findable arrival point that turns exception ownership into a practical breakpoint, trace, or compare boundary
- `KiUserExceptionDispatcher` / `RtlDispatchException` keeps appearing as the first place where trap arrival, context shape, and later unwind/handler decisions line up cleanly
- pseudocode signatures or shallow API labels look convincing, but the actual dispatcher-side stack/context layout still appears to own whether unwind lookup and resume behavior make sense at all

Why it helps:
- it prevents the case from stalling at vague “VEH/SEH exists” wording
- it often yields a smaller stop rule: once dispatcher-side landing plus one consequence-bearing lookup/handler action is good enough, leave broad exception theory
- it preserves a practical caution from recent practitioner material: on Windows, a wrong mental model of dispatcher-side calling / stack-layout realism can make later unwind or resume reasoning look falsely broken, so the truthful analyst object is often the landing layout plus one later lookup/resume consequence, not an IDA-style guessed prototype alone

Practical reminder:
- if `KiUserExceptionDispatcher` keeps recurring but later unwind ownership still looks nonsensical, verify that your model preserves dispatcher-side stack/context realism before broadening into more handler-family theory
- a good stop rule is not “I know the name of the dispatcher”; it is “this landing layout now explains one `RtlLookupFunctionEntry`/unwind decision or one later resume edge well enough to predict behavior”
- an even better stop rule is to separate **landing truth** from **resume truth**:
  - dispatcher landing proves where exceptional ownership becomes re-findable
  - it does **not** yet prove which resumed target or context mutation actually owns the behavior that matters

Concrete compare pair ideas:
- guessed register-argument model vs observed dispatcher-side stack-layout model
- dispatcher landing with implausible unwind ownership vs dispatcher landing after correcting the landing/context layout assumptions
- same trap family with stable dispatcher landing but different later lookup region or resume target
- same dispatcher arrival with the same lookup family but different `ContextRecord` / `ucontext_t` resume target, instruction-pointer edit, or skip length

Common payoff:
- this often turns a vague Windows exception case back into one smaller ownership question: which looked-up region, handler action, or resumed target actually owns the next ordinary branch?
- it also prevents a recurring mistake: treating the first truthful dispatcher landing as if it were already the behavior-bearing consumer, when the real proof object is still one later resume target or context mutation

### B1. Dispatcher landing is infrastructure; resume target is often the first behavior truth
Use when:
- `KiUserExceptionDispatcher`, `RtlDispatchException`, or a Linux `SA_SIGINFO` landing is already stable enough to breakpoint, trace, or compare reliably
- the remaining ambiguity is no longer where exception/signal ownership becomes visible, but which resume target, instruction-pointer rewrite, skip length, or small state mutation actually predicts later behavior
- analysts keep over-crediting dispatcher arrival itself even though multiple later outcomes are still possible from the same landing family

Why it helps:
- it preserves a practical three-part split that the branch still needed more explicitly:
  - **landing truth** -> where exceptional ownership becomes re-findable
  - **lookup/range truth** -> which handler-owned region or callback-owned range is actually in play
  - **resume truth** -> which concrete resumed target or context mutation first predicts the behavior that matters
- this keeps exception-owned work from stalling at infrastructure proof
- it also aligns Windows and Linux cases under the same stop rule: registration/landing alone is still infrastructure; one resumed target or context mutation is the first practical consumer-level proof object

Practical stop rule:
- do not leave the branch merely because dispatcher-side landing is now understandable
- leave once one of the following is preserved well enough to predict the next ordinary behavior:
  - one resumed target / resume IP
  - one instruction skip or trap-family-specific resume delta
  - one concrete context/register mutation
  - one small state write that reliably accompanies the resumed path

Concrete compare pair ideas:
- same dispatcher landing, different resumed RIP/PC
- same signal family, handler present vs handler altered, with the resumed target compared directly
- same lookup-owned region, but different resume delta after `int3`, guard-page, or single-step delivery

Common payoff:
- this reduces a broad exception case into a smaller practical question: is the real next task ordinary route proof, integrity consequence proof, or anti-debug continuation from the resumed target rather than from dispatcher infrastructure itself?

### C. x64 unwind metadata hides the real local branch
Use when:
- disassembly of a function looks like the exceptional path cannot be reached directly, but the exception directory and unwind data explain the hidden ownership

Why it helps:
- it localizes the missing branch to one function-region boundary instead of widening to whole-program mystery

### D. Dynamic function-table callback owns generated-code exceptions
Use when:
- protected or generated code lacks useful static exception metadata, yet runtime callback registration makes the exceptional path valid only after installation
- traces keep landing in dispatcher-side machinery, but the owning code range only becomes explainable after `RtlInstallFunctionTableCallback` / `RtlAddFunctionTable` / growable-table installation is correlated with the generated region

Why it helps:
- it explains why static analysis stays close-but-wrong until runtime-installed ownership is considered
- it keeps the analyst from overcommitting to broken static unwind assumptions when the real ownership is created at runtime
- it preserves a more practical split inside the exception-owned branch:
  - **landing truth** -> where exceptional ownership becomes re-findable
  - **range ownership truth** -> which runtime-installed or callback-owned unwind range actually owns the current PC
  - **resume truth** -> which later resumed target, unwind consequence, or handler-owned edge first predicts behavior

Practical stop rule:
- do not stop at `KiUserExceptionDispatcher` / `RtlDispatchException` alone
- do not stop at `RtlInstallFunctionTableCallback` / `RtlAddFunctionTable` / growable-table registration alone either
- leave this subcase once one runtime-installed range plus one later resume/consequence edge are both preserved well enough to predict the next ordinary behavior

Practical caution:
- when generated-code or hook stubs are involved, treat direct unwind-aware evidence (`RtlLookupFunctionEntry`, debugger/ETW-visible unwind success, callback-owned range correlation) as stronger than one convenience stack-capture surface that appears to ignore dynamic tables
- a misleading backtrace alone is weaker than one proved runtime-installed range

### E. Linux signal handler converts trap/fault into hidden continuation
Use when:
- a signal appears to indicate failure, but the handler mutates context or state and resumes into real work or anti-debug consequence

Why it helps:
- it reframes the case from generic crashing into one handler-owned continuation problem

### F. Debug-register or page-guard trigger feeds a handler-owned hook
Use when:
- the trigger mechanism is visible, but the real analyst task is proving which handler-side branch or trampoline owns the meaningful continuation

Why it helps:
- it keeps the focus on the first consequence-bearing resume edge rather than on the trigger primitive alone

## 8. Representative scratch schemas
### Minimal handler-owned-transfer note
```text
earliest symptom:
  ...

suspected handler family:
  ...

first ownership boundary:
  ...

first consequence-bearing handler action:
  ...

post-handler ordinary target:
  ...

next route if confirmed:
  ...
```

### Resume-edge proof note
```text
baseline condition:
  ...

changed condition:
  ...

first ownership boundary:
  ...

resume / redirected target:
  ...

later effect:
  ...

decision:
  anti-debug continuation / integrity continuation / ordinary native follow-up / topology change
```

## 9. Failure modes
### Failure mode 1: exception mechanisms are documented, but no case progress happens
Likely cause:
- the work stayed at platform tutorial level and never proved one ownership boundary plus one consequence-bearing action

Next move:
- force the case into one handler family and one resume/state consequence

### Failure mode 2: the trigger is overemphasized while the real branch stays hidden
Likely cause:
- the analyst kept focusing on `int3`, page-guard, or signal generation instead of the handler-side resume logic

Next move:
- isolate the first handler-side context rewrite, byte skip, or downstream state write

### Failure mode 3: static control flow still looks wrong after likely handler APIs are found
Likely cause:
- the case is owned by dispatcher-side lookup, unwind metadata, or dynamic function-table registration, not by visible direct branches alone
- the analyst proved registration names but never proved which runtime-owned code range or lookup result actually owns the exceptional path

Next move:
- localize one dispatcher-side landing, one concrete unwind/function-table lookup result, or one runtime-installed exception table callback
- if the same generated or relocated region keeps appearing in lookup results, freeze that range as the truthful owner before widening back into broader protection theory

### Failure mode 4: every crash is treated as anti-debug
Likely cause:
- real signal/exception ownership was not separated from ordinary crash handling or integrity consequence

Next move:
- define one compare pair and prove whether the handler resumes/diverts usefully or only fails

### Failure mode 5: topology relocation starts before the handler path is reduced
Likely cause:
- the current posture was blamed too early, even though one narrower handler-owned transfer path could still be made explicit

Next move:
- return to one smallest symptom, one ownership boundary, and one post-handler target

## 10. How this page connects to the rest of the KB
Use this page when the bottleneck is:
- **exception or signal delivery appears to own the real branch, but the analyst still needs to reduce that into one registration/lookup/landing boundary, one consequence-bearing handler action, and one ordinary post-handler continuation**

Then route outward based on what becomes clearer:
- to `topics/anti-instrumentation-gate-triage-workflow-note.md` when the case is still broader anti-instrumentation family classification rather than clearly handler-owned transfer
- to `topics/protected-runtime-observation-topology-selection-workflow-note.md` when the current posture remains fundamentally too visible or distorting after the handler path is already understood
- to `topics/integrity-check-to-tamper-consequence-workflow-note.md` when the handler has already reduced into one tamper or verdict consequence path
- to native practical notes when the post-handler target is now an ordinary route/state/consumer proof problem

## 11. What this page adds to the KB
This page adds a missing practical rung for a thinner but recurring protected-runtime case:
- handler-owned dispatch that sits after broad anti-debug suspicion, but before ordinary route proof

Instead it emphasizes:
- smallest symptom first
- one handler family first
- one ownership boundary
- one consequence-bearing context or state action
- one ordinary post-handler target

That strengthens the protected-runtime branch by giving it a practical answer to a common next question:
**if the direct control flow still looks wrong, is the real branch actually owned by an exception or signal path?**

## 12. Source footprint / evidence note
Grounding for this page comes from:
- Microsoft documentation on vectored exception handling and structured exception handling functions, including the official dynamic-function-table API surface
- practitioner material on `KiUserExceptionDispatcher`, `RtlDispatchException`, and unwind lookup behavior
- x64 SEH/unwind writeups and dynamic function-table discussions
- practical demo material showing trap-triggered VEH/SEH behavior and context-based resume changes
- KB protected-runtime branch pages and practitioner-community signal synthesis

The page intentionally stays conservative:
- it does not claim exception-owned transfer is the dominant anti-debug family
- it does not promote bypass recipes
- it treats handler-owned transfer as valuable when it explains why ordinary direct control-flow reading stays incomplete or misleading

## 13. Topic summary
Exception-handler-owned control transfer is a practical workflow for cases where traps, faults, breakpoints, or signal delivery appear to own the real branch.

It matters because some protected targets hide meaningful control transfer in handler registration, dispatcher-side landing, unwind metadata, signal delivery, or resume logic rather than in ordinary visible direct calls.

The useful move is to reduce the case into one ownership boundary, one consequence-bearing handler action, and one quieter post-handler target.
