# Source notes — compare-run divergence isolation to watched-object reduction

Date: 2026-03-25
Topic cluster: runtime evidence / compare-run design / first meaningful divergence / watched-object reduction / rr / WinDbg TTD / Binary Ninja TTD

## Scope
This pass focused on a thin runtime-evidence seam that was still easy to under-explain in the KB:

- a compare pair already exists
- early noise has already been reduced enough to isolate one **first meaningful divergence**
- but the analyst still risks stopping at a broad divergence description instead of shrinking it into the **smallest durable watched object** that supports reverse watchpoint, memory-query, or reducer localization work

The goal was not to restate replay or compare-run basics.
The goal was to preserve one smaller operator bridge between:
- compare-run divergence isolation
- and first-bad-write / decisive-reducer localization

## Search mode used in this run
Multi-source search was explicitly attempted via search-layer with:
- `--source exa,tavily,grok`

Queries used:
- `reverse engineering compare run first bad write watchpoint time travel debugging`
- `rr reverse watchpoint first changed value compare runs debugging`
- `WinDbg TTD memory write watchpoint first divergence reverse engineering`

Saved raw search artifact:
- `sources/runtime-evidence/2026-03-25-compare-to-watched-object-search-layer.txt`

## Sources used in this pass
Primary retained sources fetched or validated in this pass:
- Microsoft Learn — Time Travel Debugging Overview
  - https://learn.microsoft.com/en-us/windows-hardware/drivers/debuggercmds/time-travel-debugging-overview
- Microsoft Learn — TTD Memory Objects
  - https://learn.microsoft.com/en-us/windows-hardware/drivers/debuggercmds/time-travel-debugging-memory-objects
- Sean Heelan — Tracking Down Heap Overflows with rr
  - https://sean.heelan.io/2016/05/31/tracking-down-heap-overflows-with-rr/
- Binary Ninja blog — Having Fun with Flare-on Using Time-Travel Debugging (TTD)
  - https://binary.ninja/2024/12/16/flareon-ttd.html

Continuity source reused from yesterday’s runtime-evidence pass:
- `sources/runtime-evidence/2026-03-24-first-bad-write-tool-patterns-notes.md`

## High-signal findings

### 1. Time-travel tools reward smaller questions, not just better traces
Microsoft’s TTD overview and memory-object docs reinforce that the practical value is not merely being able to record and replay a run.
The real leverage comes from querying a **bounded address range** or revisiting a **specific moment** in the trace.

That matters for the KB because once a compare-run divergence is already known, the next operator move should often be:
- stop describing the divergence at subsystem level
- choose the smallest field, slot, or slice whose value actually predicts the divergent behavior
- then use reverse watchpoint / memory-query style workflows on that smaller target

### 2. Heelan’s rr example is really a watched-object reduction story
The rr heap-overflow writeup is often remembered as “reverse watchpoints are powerful.”
But the more reusable workflow lesson is narrower:
- a late bad value is visible
- the analyst identifies the exact location backing that bad value
- a watchpoint is placed on that specific location
- reverse execution then localizes the earlier write

This is stronger than a generic reverse-debugging lesson because it shows that the winning move is not “diff more of the run.”
It is “reduce the problem to one durable location that the debugger can answer well.”

### 3. Binary Ninja TTD query practice favors scoped execution and memory surfaces
The Binary Ninja TTD article is useful because it shows a practical query-first workflow:
- query executed instructions or memory events in a bounded region
- jump to one returned position
- inspect the smaller pattern from there

That supports a KB rule that should be explicit:
- once a compare-run note has isolated the first semantic split, do not stay at broad trace-diff language if a smaller memory/query target is now obvious
- convert the divergence into one queryable object whenever possible

### 4. “First meaningful divergence” and “watched object” are different proof objects
This pass sharpened a distinction the KB already partly implied but had not yet stated plainly enough:

- **first meaningful divergence** answers:
  - where do the good and bad runs first separate in a behavior-bearing way?
- **watched object** answers:
  - what exact field / slot / slice / reducer output should I now monitor to localize the upstream write or reducer boundary efficiently?

Often they are adjacent, but they are not identical.
A divergence can still be too rich, too aggregate, or too narrative-heavy for efficient reverse-causality work.

Examples:
- divergence = callback family differs
  - watched object = one queue slot or registration bit that predicts the callback difference
- divergence = request object differs
  - watched object = one freshness field, token slot, or reduced mode bit inside the request object
- divergence = policy bucket differs
  - watched object = the local enum/slot that stores the reduced bucket

### 5. The bridge is especially valuable when compare-run work is already “good enough”
The runtime-evidence branch already had a strong alignment-truth rule inside compare-run work.
This pass suggests the next canonical reminder should be:
- once the compare pair is trustworthy and the first meaningful divergence is small enough,
- the main bottleneck may no longer be compare-run design at all,
- but rather shrinking the divergence into the narrowest durable watched object.

That prevents a recurring mistake:
- analysts keep improving the diff even after the pair is good enough,
- instead of switching to the object that would let reverse watchpoint / TTD memory-query work answer the next question faster.

### 6. Query scope is part of correctness here, not just speed
The TTD memory-query model and BN TTD article both reinforce that broad memory/event searches become less useful when the target is still too wide.
That aligns with yesterday’s first-bad-write tooling note.

The practical rule worth preserving is:
- if the divergence is already bounded, but the query target is still huge,
- reduce the target before widening the search.

That is a correctness issue because oversized watched objects mix unrelated semantic roles and return noisy upstream edges.

## Practical synthesis
A strong cross-source operator bridge from this pass is:

```text
compare pair becomes trustworthy
  -> first meaningful divergence becomes visible
  -> ask whether that divergence is already a good watched object
  -> if not, shrink it into one field / slot / slice / reducer output
  -> use reverse watchpoint / memory-query / bounded backward search there
  -> localize one first useful write or decisive reducer
```

## KB implications from this pass
This pass supports tightening the runtime-evidence branch in four specific ways:

1. refine `compare-run-design-and-divergence-isolation-workflow-note.md`
   - explicitly say that one first meaningful divergence is often still a bridge object, not yet the watched object
   - add a stop rule telling analysts to leave broad compare-run work once the divergence can be reduced into one durable watched object

2. reinforce `runtime-evidence-practical-subtree-guide.md`
   - add routing language for the bridge from compare-run isolation into watched-object / first-bad-write work
   - make the distinction between divergence boundary and watched-object boundary explicit

3. lightly strengthen `first-bad-write-and-decisive-reducer-localization-workflow-note.md`
   - remind readers that a good watched object often comes from a previously isolated compare-run divergence

4. preserve top-level branch memory in `index.md`
   - the runtime-evidence branch should not stop at “first meaningful divergence” language alone
   - it should preserve the handoff into smaller watched-object reduction when that is the real next move

## Best next continuation after this note
A future runtime-evidence pass could usefully add a thinner concrete note around:
- when the first semantic divergence is still too aggregate for reverse watchpoints
- and how to choose the best reducer/slot/field inside it without reopening broad trace diffing
