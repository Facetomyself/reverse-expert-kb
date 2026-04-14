# Watchpoint-Location vs Object-Incarnation Workflow Note

Topic class: concrete workflow note
Ontology layers: runtime-evidence practice branch, watchpoint/query continuation, object-identity and lifetime truth
Maturity: practical
Related pages:
- topics/runtime-evidence-practical-subtree-guide.md
- topics/runtime-behavior-recovery.md
- topics/compare-run-design-and-divergence-isolation-workflow-note.md
- topics/first-bad-write-and-decisive-reducer-localization-workflow-note.md
- topics/causal-write-and-reverse-causality-localization-workflow-note.md
- topics/runtime-evidence-package-and-handoff-workflow-note.md
- topics/analytic-provenance-and-evidence-management.md
- sources/runtime-evidence/2026-04-15-watchpoint-location-vs-object-incarnation-notes.md
- sources/runtime-evidence/2026-04-15-0450-object-incarnation-search-layer.txt

## 1. When to use this note
Use this note when a case has already narrowed past broad observation choice, past broad compare-pair design, and often even past the first watched-object choice.

Typical entry conditions:
- one late object or one watched field/range is already plausible enough to query repeatedly
- one real watchpoint or memory-query hit already exists, or is easy to reproduce
- the remaining confusion is no longer “can I see the write?”
- the remaining confusion is whether the same address/range still belongs to the same semantic object and the same consequence-bearing incarnation
- allocation, copy, move, rebinding, owner swap, free/reuse, slot reuse, or thread/worker reuse can happen in the current window

Use it for cases like:
- one late buffer slice is readable, but the live object may have moved through temporary storage before the visible consequence
- one queue slot or handle table entry is easy to watch, but the same slot may be reused by a different request/incarnation before the later effect
- one owner pointer, context pointer, or callback state object is visible, but the live owner may swap to a new allocation behind the same higher-level role
- one TTD or replay memory query keeps finding the same address range, but the important question is whether that address still belongs to the same object, thread, or owner context across time

Do **not** use this note when:
- the watched object is still obviously too broad
- the compare pair is still noisy or misaligned
- the main missing step is still the first watched object / first bad write itself
- the case has already moved past object identity and the real gap is now the first downstream consumer or later consequence

In those cases start with:
- `topics/compare-run-design-and-divergence-isolation-workflow-note.md`
- `topics/first-bad-write-and-decisive-reducer-localization-workflow-note.md`
- `topics/causal-write-and-reverse-causality-localization-workflow-note.md`

## 2. Core claim
A practical stop rule worth preserving for this narrower seam is:

```text
same address/range visible
  != same storage contract still matters
  != same semantic object
  != same consequence-bearing incarnation
  != first-bad-write truth
```

A second compact split is often the one that saves the run:

```text
real hit at watched location
  != current owner still points there
  != copy/rebind/reuse has not happened
  != later consequence still belongs to that incarnation
```

Treat these as different proof objects until one is frozen:
- address/range query or watchpoint truth
- still-relevant storage truth
- semantic object identity truth
- current incarnation truth
- first-bad-write or decisive-reducer truth
- later consumer/consequence truth

The point is not to deny that watchpoints and memory queries are useful.
It is to stop flattening **location fact**, **same object**, and **same meaningful incarnation** into one vague “the watchpoint fired again” story.

## 3. Target pattern
The recurring pattern is:

```text
one watched location already looks good
  -> real read/write/access hit occurs there
  -> allocation/copy/rebind/reuse can still happen mid-window
  -> later visible object still looks structurally similar
  -> analyst narrates continuity too early
  -> first-bad-write story silently follows stale storage or stale ownership
```

The key discipline is:
- separate **location truth** from **identity truth**
- separate **identity truth** from **current-incarnation truth**
- separate **current-incarnation truth** from **later consequence truth**

## 4. What counts as a good identity anchor
Prefer at least one anchor that is stronger than raw address alone.

Good anchors include:
- one allocator / free / heap-object lifetime event
- one owner pointer that should keep pointing at the current object
- one container slot plus generation/epoch/count field
- one request/context handle whose lifecycle is already bounded
- one copy/rebinding point where old storage and new storage both become visible
- one thread/work-item identity with a stable lifetime object rather than raw TID alone
- one time-pinned object/position in a trace system that otherwise answers range queries by address only

A useful rule:
- if your whole identity story still reduces to “it was the same address,” you usually do **not** yet have a strong enough anchor

## 5. Practical workflow

### Step 1: Freeze the current consequence-bearing object in one line
Write the thing you actually care about now, not the first historical storage you happened to find.

Examples:

```text
current object of interest:
  session->policy_mode inside the live session object that still drives retry scheduling
```

or:

```text
current object of interest:
  the queue slot incarnation whose completion still wakes the current waiter
```

### Step 2: Choose one identity anchor stronger than raw address
Ask explicitly:
- what would convince me that the object currently living at this role is still the same one?

Good answers often look like:
- owner pointer still points at it
- heap lifetime still covers the window
- slot generation did not change
- copy/rebinding boundary has not happened yet
- thread/work item still has the same trace-unique identity

Bad answers often look like:
- the address still exists
- the bytes still look similar
- the debugger kept the watchpoint alive

### Step 3: Mark the identity transitions, not only the writes
Before chasing the earliest write, mark the points where identity could have changed:
- allocation / first materialization
- publication into current owner/container
- copy or move to new storage
- owner pointer swap / context rebinding
- free / reuse / slot reclaim
- late thread/work-item reuse under the same broad subsystem story

If one of these transitions is still unmarked, the watchpoint story is often too optimistic already.

### Step 4: Build one compare slice around the transition
Do **not** compare the whole trace first.
Prefer one bounded slice where one of these is visible:
- before-copy vs after-copy
- before-rebind vs after-rebind
- before-slot-reuse vs after-slot-reuse
- before-free vs after-reuse
- before-thread death vs later recycled TID use

This keeps the operator question honest:
- am I still tracking the same meaningful incarnation,
- or only the same address/range?

### Step 5: Use location-oriented tools honestly
These tools are still useful, but only for the claim they actually support.

Useful examples:
- GDB `watch` / `watch -location` when the address or expression is already stable enough to monitor
- LLDB variable watchpoints when variable identity is good enough, or expression watchpoints when one address is the current best location target
- WinDbg `ba` when one aligned address range and access size freeze the local write/read question tightly enough
- TTD `Memory(...)` / `MemoryForPositionRange(...)` when the question is truly “who touched this range in this time window?”

Practical rule:
- treat the returned hit as proof that **the range was touched**
- do **not** treat it as proof that the same semantic object still owns that range unless your separate identity anchor says so

### Step 6: Stop at the first rebinding/copy/reuse boundary when location truth fails
If one of these becomes true:
- the owner pointer now points somewhere else
- the heap object covering the old address died
- the slot generation changed
- the current waiter/request/owner lives in a new allocation
- the thread/work item is only TID-equal, not lifetime-equal

then stop narrating one continuous watchpoint story.

Rename the result honestly as:
- old-storage write boundary
- pre-copy materialization boundary
- stale-slot write boundary
- pre-rebind mutation boundary

Then reopen the search on the **current meaningful incarnation**.

### Step 7: Prove one downstream dependency on the current incarnation
Useful proofs include:
- only the new incarnation is read by the consumer that matters
- only the current slot generation wakes the waiter or advances the state machine
- only the rebinding after owner swap predicts the later effect
- the good/bad pair diverges at the identity transition, not only at a nearby write to stale storage

### Step 8: Hand off narrowly
Once object identity is frozen again, hand the case to one next task only:
- back to `topics/first-bad-write-and-decisive-reducer-localization-workflow-note.md` if the real next question is now the first causally useful write on the current incarnation
- to a narrower native/protocol/mobile/malware/protected-runtime consumer note if the remaining gap is now the first downstream consumer
- to evidence packaging if the proof is already good enough and now mainly needs preservation

## 6. Source-backed reminders worth preserving

### Reminder A: GDB already distinguishes expression truth from memory-location truth
GDB’s watchpoint docs explicitly separate:
- watch an expression
- or `watch -location` to watch the memory referred to by the expression

They also make three practical traps explicit:
- a watched expression such as `*global_ptr` can be set before it is valid
- the expression may only become valid later
- local-variable watchpoints are deleted when scope ends

For operator purposes, the reduction is:
- expression validity is one truth object
- memory-location watching is another truth object
- current semantic object lifetime is still a third

### Reminder B: LLDB also distinguishes variable watchpoints from memory-location watchpoints
LLVM/Apple command-map material explicitly separates:
- watch a variable
- watch a memory location returned by an expression

It also notes that a memory-location watchpoint defaults to pointer-sized monitoring unless a different size is specified.

For operator purposes, the reduction is:
- if the live object moves or is replaced, the debugger may still be faithfully watching the old location
- that is useful location truth, but not automatic incarnation truth

### Reminder C: WinDbg `ba` is an address-range claim with processor-shaped overlap rules
Microsoft’s `ba` docs define the breakpoint over:
- one aligned address
- one explicit size
- one access type

They further warn that overlap behavior can be processor-dependent.

For operator purposes, the reduction is:
- `ba` is excellent for proving access to a bounded range
- it is weaker than proving who semantically owns the bytes across a longer lifecycle story

### Reminder D: TTD already exposes the tools needed to escape raw-address overclaim
Microsoft’s TTD docs explicitly expose:
- `Memory(startAddress, endAddress)`
- `MemoryForPositionRange(...)`
- `PinObjectPosition(...)`
- thread `UniqueId`
- thread `Lifetime` / `ActiveTime`
- range objects with `MinPosition` / `MaxPosition`

For operator purposes, the reduction is:
- address-range queries are often the right first move
- but TTD itself already teaches that time-pinned identity and lifetime matter
- pair address-range queries with one stronger anchor instead of narrating continuity from address alone

Use all of these sources conservatively as operator reminders, not as a claim that every target exposes the same allocator, ownership model, or trace object model.

## 7. Breakpoint / query placement guidance
Useful anchors for this stage:
- allocator, constructor, or first materialization points
- free / destroy / reclaim sites
- owner-pointer stores and pointer-swap reducers
- container-slot generation writes
- copy/move helpers between temporary and live storage
- queue-slot publish and reclaim boundaries
- TTD `MemoryForPositionRange(...)` slices around the rebinding point rather than across the whole trace
- TTD thread `UniqueId` / `Lifetime` checks when thread or work-item identity may drift
- `PinObjectPosition(...)` or equivalent time-pinning helpers when the object view itself would otherwise drift as you query around it

If traces are noisy, anchor on:
- one current-owner pointer
- one copy/rebind boundary
- one free/reuse boundary
- one first current-incarnation consumer
- one later consequence difference

## 8. Failure patterns this note helps prevent

### 1. Treating “same address hit again” as the whole story
That often proves only that the debugger/query is honest, not that the object identity story is solved.

### 2. Following stale storage through a live-object handoff
A temporary buffer, old session object, or stale queue slot can still be highly active after the real consequence-bearing owner has moved elsewhere.

### 3. Treating scope validity or expression validity as lifetime truth
A valid dereference or surviving watchpoint is weaker than a current semantic-owner proof.

### 4. Missing slot/generation reuse
Stable slot number or handle-table position is often weaker than current generation/incarnation truth.

### 5. Trusting raw TID instead of trace-unique thread/work-item identity
In replay-heavy cases, a recycled OS thread ID can silently flatten two different lifetimes into one story.

## 9. Concrete scenario patterns

### Scenario A: copied plaintext buffer vs live consumer buffer
Pattern:

```text
one late readable slice exists
  -> watchpoint hits earlier temporary storage
  -> later live consumer reads a copied buffer elsewhere
  -> analyst overreads old-location writes as the live first-bad-write answer
```

Best move:
- freeze the copy boundary first
- reopen first-bad-write work on the live consumer buffer only

### Scenario B: queue slot reuse after timeout or completion
Pattern:

```text
slot index stays stable
  -> generation or owner changes
  -> later completion still touches same slot bytes
  -> analyst overreads slot-local activity as same-request truth
```

Best move:
- pair slot watchpoints with generation/current-owner anchors
- stop at reuse before narrating consequence

### Scenario C: owner pointer swap behind the same higher-level role
Pattern:

```text
same subsystem role exists
  -> old object remains writable
  -> current owner now points at new storage
  -> later consumer uses only the new object
```

Best move:
- freeze the pointer-swap or rebinding reducer
- treat old-storage writes as pre-rebind history, not current-incarnation proof

### Scenario D: trace query keeps a broad thread story alive after lifetime drift
Pattern:

```text
same broad worker family appears active
  -> raw TID or broad timeline looks continuous
  -> actual thread/work-item lifetime split already happened
  -> later memory/query output mixes two lifetimes
```

Best move:
- use thread/work-item lifetime or trace-unique identity before widening the causal story

## 10. Relationship to nearby pages
- `topics/compare-run-design-and-divergence-isolation-workflow-note.md`
  - use that when the pair is still too noisy and the first meaningful divergence is not yet isolated
- `topics/first-bad-write-and-decisive-reducer-localization-workflow-note.md`
  - use that when the watched object itself is still the main missing step; return there once current-incarnation truth is frozen again
- `topics/causal-write-and-reverse-causality-localization-workflow-note.md`
  - use that when the case broadens back out from one watched object into a larger causal window
- `topics/runtime-behavior-recovery.md`
  - use that when the truthful observation surface itself is still unclear or replay/query tools are still too noisy to trust
- `topics/runtime-evidence-package-and-handoff-workflow-note.md`
  - use that when the identity proof is already good enough and the main remaining value is preserving it for later reuse

## 11. Source footprint / evidence quality note
Primary retained support:
- `sources/runtime-evidence/2026-04-15-watchpoint-location-vs-object-incarnation-notes.md`
- `sources/runtime-evidence/2026-04-15-0450-object-incarnation-search-layer.txt`
- GDB watchpoint documentation
- LLVM / Apple LLDB command-map material
- Microsoft WinDbg `ba` documentation
- Microsoft Time Travel Debugging object-model, range-object, and thread-object documentation

Confidence note:
- strong for the narrow workflow lesson that location truth and object-incarnation truth must stay separate
- strong for the specific documented reminders that GDB/LLDB/WinDbg watch/query surfaces are fundamentally expression/location/range oriented
- moderate for exact cross-target vocabulary because different targets expose different ownership and lifetime cues

## 12. Bottom line
When the watchpoint or memory query keeps firing at the same address, the next useful move is often **not** to celebrate that the first-bad-write story is solved.

It is to localize the first **location-vs-object-incarnation** boundary that decides whether the bytes you are still watching belong to the same semantic object, only to stale storage, or to a newer consequence-bearing incarnation that now deserves the real first-bad-write search.
