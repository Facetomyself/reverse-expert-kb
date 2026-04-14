# Watchpoint location vs object-incarnation notes

Date: 2026-04-15
Branch target: runtime-evidence practical workflows / watched-object continuation
Purpose: preserve a source-backed operator refinement for watchpoint / memory-query-heavy cases where a real hit exists on the same address or address range, but allocator/copy/rebinding/reuse churn means the analyst still has not proved they are looking at the same semantic object or the same consequence-bearing incarnation.

## Research intent
Strengthen the runtime-evidence branch with a sharper separation between:
- location/range visibility truth
- same-storage or same-address truth
- semantic object identity truth
- current consequence-bearing incarnation truth
- first-bad-write truth

## Search artifact
Raw multi-source search artifact:
- `sources/runtime-evidence/2026-04-15-0450-object-incarnation-search-layer.txt`

Requested source set:
- `exa,tavily,grok`

Observed search-source reality for this run:
- Exa returned usable official GDB, LLDB, and Microsoft WinDbg/TTD surfaces
- Tavily returned usable official GDB, Apple/LLDB, and Microsoft WinDbg/TTD surfaces
- Grok was explicitly invoked and failed with repeated `502 Bad Gateway` through the configured proxy path

## Retained sources
1. GDB watchpoint documentation
   - expression watchpoints versus `-location`
   - dynamic-pointer / expression-validity caveats
   - automatic deletion for out-of-scope local-variable watchpoints
2. LLDB command-map material
   - variable watchpoints versus memory-location / expression watchpoints
   - raw-address / pointer-expression semantics and default watched size
3. WinDbg `ba` documentation
   - aligned address-range monitoring with explicit size
   - overlap-trigger caveats and processor-dependent range behavior
4. Microsoft Time Travel Debugging object-model, thread-object, and range-object documentation
   - `TTD.Memory(...)` and `TTD.MemoryForPositionRange(...)` are address-range/time-range queries
   - `PinObjectPosition(...)` exists specifically to pin an object to a time position
   - thread `UniqueId`, `Lifetime`, and `ActiveTime` provide stronger identity anchors than raw TID alone

## High-signal retained findings

### 1. Location-oriented watch/query tools answer an address question first
The GDB, LLDB, and WinDbg materials all preserve the same practical shape:
- watch an expression
- or watch a memory location / address range
- then break when that watched location is read/written/accessed

Practical consequence:
- a truthful watchpoint or memory-query hit is still a **location fact** first
- it is weaker than proof that the same semantic object still lives there

### 2. Expression validity and scope are separate from object lifetime truth
GDB’s docs are especially useful because they make two subtle problems explicit:
- a watched expression may only become valid later (for example around pointer initialization / malloc-adjacent state)
- local-variable watchpoints disappear when scope ends

Practical consequence:
- expression validity, variable scope, and object lifetime should not be collapsed together
- “the watchpoint still exists” or “the expression became valid” is weaker than “the current meaningful object is still the same one”

### 3. Memory-location watchpoints are narrower than object identity
LLDB’s command-map material explicitly distinguishes:
- watch a variable
- watch a memory location returned by an expression

Practical consequence:
- if the live object moves, is copied, or is replaced behind the same higher-level role, a raw memory-location watch can remain truthful while silently following the wrong incarnation

### 4. Range-based breakpoints and trace queries make address truth explicit, not lifetime truth
WinDbg `ba` is defined over an aligned address plus size and even documents overlap-trigger behavior as processor-dependent.
Microsoft TTD memory queries are likewise defined over start/end addresses and optional time ranges.

Practical consequence:
- these surfaces are excellent for localizing reads/writes around a candidate location
- but they do not, by themselves, prove that the address still belongs to the same semantic object, owner, or incarnation across the whole window

### 5. TTD already exposes stronger identity anchors than raw address alone
Microsoft’s TTD docs expose:
- `PinObjectPosition(...)`
- trace/object `Lifetime` ranges
- thread `UniqueId`
- `ActiveTime`
- heap-object collections

Practical consequence:
- the right operator move is often to pair address-range queries with one stronger identity anchor such as heap-object lifetime, owner pointer, thread `UniqueId`, container slot/generation, or one pinned position around the rebinding point

## Practical synthesis worth preserving canonically
A compact stop-rule ladder for this seam is:

```text
same address/range visible
  != same storage contract still matters
  != same semantic object
  != same consequence-bearing incarnation
  != first-bad-write truth
```

A second compact split worth preserving is:

```text
real hit at watched location
  != current owner still points there
  != copy/rebind/reuse has not happened
  != later consequence still belongs to that incarnation
```

## Best KB use of this material
This material is best used as a thinner continuation in the runtime-evidence branch:
- after broad compare-run design already isolated one watched object candidate
- or after first-bad-write work already narrowed the search far enough that the main liar is now object identity / incarnation drift rather than watchpoint availability

The operator-facing value is:
- do not overclaim from “same address hit again”
- freeze one stronger identity anchor before narrating first-bad-write truth across realloc/copy/rebind/reuse cases
- stop at the first rebinding/copy/reuse boundary when location truth and object truth diverge
- then resume first-bad-write work on the current meaningful incarnation only

## Search reliability note
This was a degraded-source external pass, not a fully healthy tri-source result set.
It still counts as a real external-research attempt because `exa,tavily,grok` were explicitly requested and Grok was actually invoked; its failure is recorded clearly.
