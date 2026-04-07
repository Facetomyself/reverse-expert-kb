# eBPF / seccomp / SVC Tracing for Mobile RE

Topic class: concrete workflow note
Ontology layers: mobile practical workflow, protected-runtime observation surfaces, syscall/boundary tracing
Maturity: practical
Related pages:
- topics/mobile-protected-runtime-subtree-guide.md
- topics/android-linker-binder-ebpf-observation-surfaces.md
- topics/android-observation-surface-selection-workflow-note.md
- topics/protected-runtime-observation-topology-selection-workflow-note.md
- topics/anti-instrumentation-gate-triage-workflow-note.md
- topics/environment-differential-diagnosis-workflow-note.md

## 1. When to use this note
Use this note when a mobile reversing case has already narrowed to a **protected-runtime or anti-instrumentation setting** where ordinary app-layer hooks are too weak, too noisy, or too detectable, and the next useful move is to observe behavior closer to the syscall / kernel-boundary surface.

Typical entry conditions:
- user-space hooks are missing events, being actively detected, or producing distorted evidence
- the protected app/runtime appears to gate behavior around syscall use, thread/process control, memory permissions, seccomp filters, or trap/syscall boundaries
- the analyst needs one lower-observability, harder-to-spoof boundary before reopening broader app logic
- the real question is no longer “what Java/ObjC method exists?” but “which kernel-adjacent action actually happens?”

Use it for cases like:
- anti-Frida / anti-debug flows where ptrace/prctl/seccomp/process-control behavior is suspected but user-space hooks are untrustworthy
- protected loaders or unpackers where `mmap` / `mprotect` / `memfd` / thread creation / signal behavior matters more than app-layer call names
- JNI/native-heavy Android targets where Binder, linker, syscall, or seccomp-adjacent behavior provides a better truth boundary than framework hooks
- iOS or Android cases where SVC/syscall-level reality is needed to separate real kernel-boundary behavior from user-space deception or trampoline noise

Do **not** use this note when:
- normal app/network/runtime hooks already provide one trustworthy boundary
- the real bottleneck is still broad owner/path localization rather than boundary truth selection
- the target question can already be answered at a cheaper and less invasive user-space surface

## 2. Core claim
A recurring protected-runtime mistake is to jump straight from “user-space hooks feel untrustworthy” to “I need full kernel magic.”

The practical ladder is usually:

```text
user-space hook is weak or noisy
  != syscall / SVC boundary is the right next surface
  != eBPF / seccomp / SVC observation actually sees the behavior you care about
  != observed kernel-boundary event is already the behavior-bearing consequence
```

This note exists to keep those steps separate.

## 3. What these surfaces are good for
High-value use cases:
- proving one syscall-family truth when user-space wrappers lie or fragment the story
- reducing anti-instrumentation suspicion into one concrete process-control / memory-permission / signal / tracer-check boundary
- proving whether a behavior crosses Binder, linker, syscall, or page-permission boundaries at all
- finding one lower, more trustworthy anchor before returning to higher-level ownership work

Useful but often too early:
- generic “use eBPF” folklore
- tracing every syscall with no bounded question
- broad SVC dumping without a target behavior or compare pair
- assuming seccomp presence alone explains behavior

## 4. Default workflow

### Step 1: Freeze one question first
Good starting questions:
- is the app really calling `ptrace`, `prctl`, `seccomp`, or a related process-control family?
- is executable memory actually being created or permissions changed at the time that matters?
- is one suspicious behavior crossing Binder/syscall boundary at all, or is it still userspace-only folklore?
- is one crash/gate tied to a real signal/trap/syscall path or only to a user-space wrapper artifact?

Bad starting question:
- “What does the app do at the kernel level?”

### Step 2: Choose the cheapest truthful lower surface
Prefer the smallest lower surface that can answer the current question:
- syscall / SVC trace when you need boundary truth around process control, memory, files, or signals
- eBPF when you need lower-overhead or lower-distortion observation of selected syscall/kernel events
- seccomp-focused inspection when the question is filter/policy/gating rather than generic runtime behavior

Do not treat all three as the same tool or proof object.

### Step 3: Keep four proof objects separate
A compact operator ladder:

```text
lower surface selected
  != target behavior visible there
  != observed event is the decisive gate or consequence
  != broader mechanism is solved
```

More concrete splits:
- suspected syscall family != actual syscall observed
- syscall observed != policy/gate meaning understood
- seccomp filter presence != filter actually deciding the current path
- SVC/syscall boundary truth != later app-owned consequence truth

### Step 4: Prefer one compare pair or one narrow event family
Good narrow families:
- `ptrace` / `prctl` / anti-debug-related process-control calls
- `mmap` / `mprotect` / executable-memory transitions
- thread creation / signal / trap boundaries
- Binder transaction adjacency when app/service boundary truth matters
- file/open/read patterns only when they answer a narrower gate question

Do not start with a kitchen-sink trace unless the cheaper discriminant has already failed.

### Step 5: Route back upward once one boundary is truthful enough
The goal is usually not to stay at the lower surface forever.
The goal is to recover one trustworthy boundary and then return to the most useful owner/consumer path above it.

Good handoffs:
- back to anti-instrumentation gate triage once one real process-control gate is proved
- back to protected-runtime observation-topology selection once one lower anchor clarifies which upper surface is now safe
- back to app/native owner localization once one kernel-boundary fact removes the main uncertainty

## 5. Practical scenario patterns

### Scenario A: Anti-Frida suspicion, but user-space evidence is noisy
Pattern:

```text
app behaves differently under instrumentation
  -> user-space hooks are untrustworthy or obviously detected
  -> one lower process-control boundary is needed
  -> one syscall/trap family proves whether the suspicion is real
```

Best move:
- trace one narrow anti-debug / process-control family first
- do not start with full-spectrum tracing

### Scenario B: Protected loader / unpacker around memory-permission changes
Pattern:

```text
loader behavior is visible only indirectly
  -> app-layer ownership is unclear
  -> one lower mmap/mprotect-style boundary is more truthful
  -> later owner/consumer work becomes easier after one boundary fact
```

Best move:
- prove the memory-permission transition first
- then route back upward into the owner that requested it

### Scenario C: seccomp is present, but its meaning is overstated
Pattern:

```text
seccomp policy/filtering is visible
  -> analyst is tempted to narrate the whole gate from presence alone
  -> actual current-path effect is still unproved
```

Best move:
- keep filter presence separate from actual deciding behavior in the run that matters

## 6. What to record
Keep the evidence package bounded:
- exact question being answered
- chosen lower surface and why it was chosen
- one narrow event family or compare pair
- what was directly observed
- what that observation does not yet prove
- which higher-level note/task it should hand back to next

## 7. Exit conditions and handoffs
Stay on this note while the main problem is still **choosing and using one lower syscall/kernel-adjacent observation surface to recover one trustworthy boundary**.

Leave once one of these is already good enough:
- one syscall/trap/policy boundary is proved and the next question is owner/consumer work above it
- one lower surface is ruled out and the observation-topology choice should move elsewhere
- the remaining work is now branch-specific anti-debug, loader, Binder, or app-owned consequence analysis

Common next moves:
- `topics/anti-instrumentation-gate-triage-workflow-note.md`
- `topics/protected-runtime-observation-topology-selection-workflow-note.md`
- `topics/android-observation-surface-selection-workflow-note.md`
- `topics/environment-differential-diagnosis-workflow-note.md`
- `topics/trace-slice-to-handler-reconstruction-workflow-note.md`

## 8. Why this page exists
The mobile/protected-runtime subtree guide already advertised this seam as a natural next expansion, but the canonical leaf was missing.

This page repairs that gap by preserving one smaller practical ladder:

```text
weak user-space evidence
  != lower surface chosen correctly
  != behavior visible there
  != decisive mechanism solved
```

That is the durable operator value here.
