# TLS Callback to First Payload Consumer Workflow Note

Topic class: concrete workflow note
Ontology layers: protected-runtime practical workflow, packed/bootstrap startup truth, TLS callback ownership, first payload-bearing consumer proof
Maturity: structured-practical
Related pages:
- topics/protected-runtime-practical-subtree-guide.md
- topics/packed-stub-to-oep-and-first-real-module-workflow-note.md
- topics/decrypted-artifact-to-first-consumer-workflow-note.md
- topics/runtime-table-and-initialization-obligation-recovery-workflow-note.md
- topics/anti-tamper-and-protected-runtime-analysis.md
Related source notes:
- sources/protected-runtime/2026-04-04-tls-callback-first-payload-consumer-notes.md
- sources/protected-runtime/2026-04-24-tls-callback-replay-reason-and-payload-ownership-notes.md

## 1. Why this note exists
The packed/bootstrap branch already preserves an important stop rule:

```text
raw_entry != pre_entry_startup != unpack_transfer != payload_handoff != consumed
```

But in Windows/native packed or protected cases there is a thinner recurring seam after that reminder:
- the analyst already knows the ambiguity is specifically **TLS-callback-shaped**
- broad OEP naming is no longer the real question
- the next useful output is one **callback slot / replay / reason / startup-owned work / first payload consumer** proof object

The overclaim this note prevents is:

```text
TLS directory or callback array exists
  == this callback already explains the interesting behavior
  == this callback already replayed on the path that matters
  == this is already payload proof
```

The smaller truthful ladder is:

```text
callback slot listed
  != callback slot replayed in this run
  != replay reason matches DLL_PROCESS_ATTACH
  != callback-owned startup work is characterized honestly
  != first payload-bearing consumer truth
```

A second practical reminder worth keeping explicit is that the PE/TLS model is not only about early pre-entry execution:
- TLS callback functions also support **per-thread initialization and termination**
- so one callback hit can still belong to thread lifecycle, detach, or runtime cleanup rather than the startup path the analyst actually cares about

## 2. When to use this note
Use this note when most of these are true:
- the case is Windows/native enough that PE/TLS startup surfaces are relevant
- the broad packed-stub / OEP handoff has already been reduced enough to say “the remaining ambiguity is now TLS-callback-shaped”
- a TLS directory, callback array, or one concrete callback slot is already visible statically or dynamically
- a debugger or trace has already shown at least one callback replay, but it is still unclear whether that replay is process-start proof, thread-lifecycle proof, startup-owned runtime proof, or the first payload-bearing consumer
- the next useful output is one smaller proof object showing where TLS-owned startup stops and payload-bearing code actually begins

Representative cases include:
- a breakpoint at the ordinary entry point keeps missing meaningful behavior and a TLS callback lands first
- a packed or protected sample clearly leaves stub churn, but the next region is still dominated by callback-array replay, CRT/runtime setup, constructors, or another startup scaffold
- a sample has multiple TLS callback slots and the analyst still needs to decide which slot merely prepares runtime state and which later consumer actually carries payload behavior
- a runtime-heavy target such as a Rust, C++, or other constructor-rich sample uses a TLS callback for legitimate initialization, but the analyst still needs to find the first payload-bearing consumer after that setup

Do **not** use this note when:
- the main uncertainty is still the broad post-unpack handoff or dump boundary (use the packed-stub note)
- runtime tables / constructors / CRT startup remain equally plausible and TLS is not yet the best discriminant
- the first readable artifact already exists and the real missing edge is its ordinary consumer
- the branch is no longer callback-shaped at all because one quieter post-startup consumer is already good enough

## 3. Conservative doc-backed anchors
### A. TLS directory and callback-array truth
The PE format specification preserves several durable facts:
- the `.tls` section supports static TLS initialization data, callback routines for per-thread initialization and termination, and a TLS index
- the TLS directory has an **Address of Callbacks** field
- that field points to a **null-terminated** array of TLS callback functions
- if more than one callback exists, each callback is called in the order in which its address appears in the array
- an empty callback list is still represented by a null terminator

The `/TLS` tool documentation reinforces a smaller practical point:
- tooling can display the TLS structure and the addresses of the TLS callback functions
- if a program does not use TLS, its image will not contain a TLS structure

Operator consequence:
- callback-array listing is real startup surface truth
- but it is still only **structure truth**
- it is weaker than one proved replay on the run that matters

### B. Replay-reason truth is explicit in the PE specification
The PE format documentation gives the TLS callback prototype directly and states that it has the same parameters as a DLL entry-point function:

```C
typedef VOID
(NTAPI *PIMAGE_TLS_CALLBACK) (
    PVOID DllHandle,
    DWORD Reason,
    PVOID Reserved
    );
```

The same documentation explicitly assigns the following `Reason` values:
- `DLL_PROCESS_ATTACH` -> a new process has started, including the first thread
- `DLL_THREAD_ATTACH` -> a new thread has been created, for all but the first thread
- `DLL_THREAD_DETACH` -> a thread is about to terminate, for all but the first thread
- `DLL_PROCESS_DETACH` -> a process is about to terminate, including the original thread

Operator consequence:
- a callback hit is **not** automatically the same thing as pre-entry process-start truth
- thread-lifecycle replay and detach-side replay are different analyst objects from startup-owned process-attach replay
- the callback question is often not just “did it fire?” but “**which reason fired on the path that matters?**”

### C. Load-path and loader-context caution still matter
The PE format documentation preserves another useful caveat for static TLS data:
- before Windows Vista, statically declared TLS data objects were only reliable in statically loaded image files
- beginning with Windows Vista, the loader improved support for dynamically loaded DLLs with static TLS

That makes load path a practical truth selector in some cases:
- `callback slot listed on disk != same runtime replay assumptions on every OS/load path`
- if a case depends on `LoadLibrary` or other dynamic-load behavior, OS/version/load-path realism can still matter

A second conservative caution comes from Microsoft’s `DllMain` and DLL best-practices pages:
- entry-point-style initialization runs under loader-managed constraints
- the loader lock is held during entry-point initialization
- initialization in that context should stay minimal when possible
- broad runtime setup in that phase is not the same as a later ordinary payload consumer

These are not TLS-callback specs, so they should not be overread into one-to-one callback rules.
They are still useful as a startup-context reminder:
- callback-visible work can still be loader-managed initialization, constructor/destructor support, TLS slot/index setup, runtime bootstrap, or other startup-owned work rather than payload ownership

### D. Practitioner reality keeps early execution separate from payload ownership
Practitioner material retained for this branch keeps two truths visible at once:
- Hex-Rays and Ring Zero preserve the debugger reality that TLS callbacks can execute before a breakpoint at the ordinary entry point, so break-at-OEP is weaker than break-on-TLS/system-entry
- a recent malware-analysis writeup showed a real Rust sample whose TLS callback replay mainly initialized runtime components and dependencies rather than acting as the first durable malware-owned payload consumer

That second pattern is especially valuable:
- callback replay can still be only **startup-owned runtime truth**
- the first payload-bearing consumer may still be one hop later

## 4. Boundary objects to keep separate
### A. TLS structure / callback-slot truth
Freeze:
- whether the image really has a TLS directory and callback array
- one callback pointer or array-slot identity
- callback-array order when more than one slot exists

### B. Replay truth
Ask:
- did this specific slot replay in the run that matters?
- was the replay observed directly, or only inferred from structure presence?
- if several callbacks exist, which slot actually replayed first?

### C. Reason / lifecycle truth
Ask:
- was the replay on `DLL_PROCESS_ATTACH`, `DLL_THREAD_ATTACH`, `DLL_THREAD_DETACH`, or `DLL_PROCESS_DETACH`?
- is the analyst really looking at process-start behavior, or at later thread lifecycle?
- if the hit is not on `DLL_PROCESS_ATTACH`, is it still relevant to the startup ambiguity the case is about?

### D. Startup-owned callback-body truth
Even when the slot replayed on the path that matters, the body can still be mostly:
- runtime normalization
- constructor/destructor support
- CRT/language startup work
- TLS slot/index setup
- import/runtime environment stabilization
- callback-array fan-out or wrapper logic

That is still **startup-owned truth**, not yet **payload proof**.

### E. First payload-bearing consumer truth
The stronger question is:
- what first consumer exists downstream of TLS-owned startup that actually carries payload-bearing parsing, config use, request shaping, state reduction, unpacked artifact use, or other ordinary target behavior?

This consumer may be:
- one later routine called from the callback body
- one downstream module/object/import family that survives startup scaffolding
- one consumer reached after the callback completes rather than inside it

## 5. Default workflow
### Step 1: freeze one callback slot, not “TLS exists” in general
Pick one representative callback pointer/slot.
If there are multiple slots, record the array order.
Do not widen to every callback immediately unless the case forces it.

Scratch form:

```text
callback array:
  [0] = ...
  [1] = ...
  ...
focus slot:
  ...
```

### Step 2: separate listing from replay
Write the smaller ladder explicitly:

```text
slot listed
  -> slot replayed
  -> replay reason
  -> startup-owned work
  -> first payload-bearing consumer
```

This prevents stopping at `.tls` inventory or an IDA entry-point list alone.

### Step 3: freeze the replay reason before narrating payload
Use the PE-defined `Reason` values as part of the workflow object:
- `DLL_PROCESS_ATTACH`
- `DLL_THREAD_ATTACH`
- `DLL_THREAD_DETACH`
- `DLL_PROCESS_DETACH`

Practical rule:
- if the remaining analyst question is broad pre-entry startup, `DLL_PROCESS_ATTACH` is usually the decisive replay reason
- if the observed replay is only thread-lifecycle or detach-side activity, do not flatten it into the same startup proof object

### Step 4: decide whether the callback is still only startup proof
If the callback body or immediate downstream work is still dominated by:
- runtime/bootstrap setup
- constructor replay
- CRT/language startup
- import/runtime normalization
- callback-array fan-out

record **startup-owned truth**, not **payload truth**.

This is still success if it explains why raw entry-point expectations were misleading.

### Step 5: hand off to one first payload-bearing consumer
Look for one smaller downstream object such as:
- one parser/config/request routine
- one first consumer of a decrypted artifact
- one first post-startup module/object/import family
- one later consumer that survives compare-runs better than the callback wrapper itself

Stop when one callback -> one downstream handoff -> one first payload-bearing consumer is good enough.
Do **not** force the whole unpacking story or every callback slot.

### Step 6: route honestly after the callback question is reduced
- if the callback was only startup/runtime truth, hand back to `packed-stub-to-oep-and-first-real-module-workflow-note.md` or `runtime-table-and-initialization-obligation-recovery-workflow-note.md`
- if the callback leads into one readable recovered artifact, hand off to `decrypted-artifact-to-first-consumer-workflow-note.md`
- if the callback really does own one immediate behavior-bearing consumer, keep that smaller consumer rather than narrating “TLS” forever

## 6. Practical debugger and compare hints
### A. Break earlier than OEP when the case is TLS-shaped
If the sample seems to run before the ordinary entry-point breakpoint:
- break on TLS callbacks or system/process entry when the debugger supports it
- do not treat “the OEP breakpoint missed the behavior” as mystery by itself

### B. Keep slot order and reason in the trace notes
For multi-callback samples, write down:
- which slot replayed first
- which `Reason` value mattered
- which slot only prepared runtime state
- which downstream consumer first carried behavior

### C. Compare process-start replay against later thread-lifecycle replay when needed
If the target keeps re-entering TLS callbacks:
- separate the initial process-start replay from later thread attach/detach activity
- otherwise one later lifecycle event can impersonate the startup path you actually care about

## 7. Practical failure patterns this note prevents
- `TLS directory exists` -> therefore payload is in the callback
- `callback replayed` -> therefore the replay was the startup path that matters
- `callback replayed on some reason` -> therefore it was `DLL_PROCESS_ATTACH`
- `callback body initializes runtime` -> therefore it already owns payload behavior
- `multiple callbacks exist` -> therefore callback-array inventory alone explains the case
- `callback hit before OEP` -> therefore the callback is necessarily the first payload consumer

## 8. Sources
See:
- `sources/protected-runtime/2026-04-04-tls-callback-first-payload-consumer-notes.md`
- `sources/protected-runtime/2026-04-24-tls-callback-replay-reason-and-payload-ownership-notes.md`

Primary references retained for this note:
- `https://learn.microsoft.com/en-us/windows/win32/debug/pe-format`
- `https://learn.microsoft.com/en-us/cpp/build/reference/tls?view=msvc-170`
- `https://learn.microsoft.com/en-us/windows/win32/dlls/dllmain`
- `https://learn.microsoft.com/en-us/windows/win32/dlls/dynamic-link-library-best-practices`
- `https://learn.microsoft.com/en-us/archive/msdn-magazine/2002/march/inside-windows-an-in-depth-look-into-the-win32-portable-executable-file-format-part-2`
- `https://hex-rays.com/blog/tls-callbacks`
- `https://www.ringzerolabs.com/2019/08/analyzing-tls-callbacks.html`
- `https://mja-reversing.github.io/blog/How-Malware-Executes-Before-Entry-Point-TLS-Callbacks/`

## 9. Topic summary
TLS callback to first payload consumer is a practical workflow for cases where the broad packed/startup ambiguity is already reduced enough that the remaining lie is specifically callback-shaped.

It matters because TLS callbacks are not just “before OEP” curiosities.
They are ordered callback slots with explicit replay reasons, and the first honest analyst object is often:
- one callback slot
- one replay on the reason that matters
- one startup-owned body characterized honestly
- one first payload-bearing consumer

The durable operator shorthand is:

```text
listed != replayed != DLL_PROCESS_ATTACH replay != startup-owned work != first payload-bearing consumer
```

That keeps callback presence, early execution, and payload proof from collapsing into one vague startup story.