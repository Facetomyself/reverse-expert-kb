# Source notes — async queue / callback-heavy compare-run alignment

Date: 2026-03-26
Topic: runtime evidence / compare-run design / async queue and callback-heavy alignment / first behavior-bearing delivery
Purpose: preserve a narrower practical rule for compare-run work when two nearby runs share broad setup, but early drift in queue ordering, callback scheduling, worker wakeups, or multi-thread timestamp positions makes raw event-by-event comparison misleading before the first consequence-bearing delivery is isolated

## Why this note exists
The runtime-evidence branch already preserved useful compare-run rules for:
- pair design
- invariant control
- noisy early mismatch triage
- alignment truth before causality truth
- shrinking the first meaningful divergence into a durable watched object

What still needed a sharper practical stop rule was a common async-heavy subcase:

```text
I already have a plausible compare pair
  + both runs enter the same broad async subsystem
  + queue ordering / callback timing / worker sequencing drifts early
  + raw event order no longer tells me whether the pair is still aligned
  -> stop comparing every early queue/callback event as if it were explanatory
  -> align on one delivery class or one consumer-bearing boundary
  -> ask which first delivered callback / dequeued work item / consequence-bearing consumer actually separates the runs
```

This note supports a conservative KB improvement:
- preserve **delivery-class alignment** as a narrower operator step inside compare-run work
- treat queue/callback-heavy traces as needing one context-bearing compare boundary, not blind event-order worship
- keep analysts from overexplaining early queue churn that is real but still non-explanatory for the question they actually care about

## Search intent
Queries explicitly attempted through search-layer:
- `time travel debugging async callback queue compare runs alignment divergence debugging`
- `rr pernosco async event loop callback divergence compare runs`
- `WinDbg TTD async callback queue compare trace divergence`

Search sources explicitly requested:
- exa
- tavily
- grok

## Search audit snapshot
Requested sources:
- exa
- tavily
- grok

Succeeded sources:
- exa
- tavily

Failed sources:
- grok

Configured endpoints on this host:
- Exa: `http://158.178.236.241:7860`
- Tavily: `http://proxy.zhangxuemin.work:9874/api`
- Grok: `http://proxy.zhangxuemin.work:8000/v1`

Failure note:
- search-layer explicitly invoked all three requested sources
- Grok returned repeated `502 Bad Gateway` failures during invocation
- Exa and Tavily returned enough usable material to continue conservatively

Primary raw search artifact:
- `sources/runtime-evidence/2026-03-26-0716-async-queue-callback-alignment-search-layer.txt`

## Representative sources used

### Microsoft Learn — Time Travel Debugging Overview
URL:
- https://learn.microsoft.com/en-us/windows-hardware/drivers/debuggercmds/time-travel-debugging-overview

Useful signals:
- recorded execution is valuable because it can be replayed and queried repeatedly instead of being rediscovered through repeated live repro
- traces can be large and costly, so practical use depends on choosing narrower questions against indexed execution history
- traces can be shared and revisited at specific positions, which makes bounded alignment questions feasible

Practical extraction:
- async-heavy compare work should ask smaller replay/query questions instead of narrating every event in temporal order
- the compare boundary should be chosen so the preserved trace can answer one bounded question about where behavior first stops being meaningfully shared

### Binary Ninja — Time Travel Debugging (Windows)
URL:
- https://docs.binary.ninja/guide/debugger/dbgeng-ttd.html

Useful signals:
- TTD memory and call queries become expensive when they are broad or poorly scoped
- practical use depends on small address ranges, small function families, and well-scoped queries
- reverse navigation and bounded query tooling are strongest when the analyst already knows what smaller event/object family to ask about

Practical extraction:
- queue/callback-heavy compare work should not widen immediately into whole-trace call or memory queries
- choose one delivery family, one queue owner, one callback slot, or one watched object before asking the tooling for help
- query scope is part of correctness because broad queue/callback surfaces mix unrelated semantic roles

### Robert O'Callahan — How To Track Down Divergence Bugs In rr
URL:
- https://robert.ocallahan.org/2016/06/how-to-track-down-divergence-bugs-in-rr.html

Useful signals:
- divergence is often caught near where behavior truly leaves the recorded path
- reverse reasoning is useful once one bad value or narrow divergence object is known
- more frequent checking or narrower targeted observation can catch divergence earlier when visible failure appears later
- when replay visibility is too sparse, changing observation density near the suspected boundary is better than broadly narrating the whole run

Practical extraction:
- in async queue/callback cases, increase density only around the suspected delivery boundary instead of explaining every early scheduling difference
- once one callback family or queue-owned object is plausibly the split, walk backward from that narrower object rather than from the whole event loop transcript

### Raymond Chen — Is there any meaningful way to compare two Time Travel Debugging positions?
URL:
- https://devblogs.microsoft.com/oldnewthing/20220905-00/?p=107107

Useful signals:
- TTD positions can be ordered chronologically by sequence and step, but cross-thread/multiprocess chronology is still fuzzy at fine granularity
- sequence boundaries are affected by synchronization, kernel transitions, and debugger discretion
- multiprocessing can yield apparently contradictory observations when unsynchronized access is involved

Practical extraction:
- raw position order across threads is weaker than proving one shared semantic boundary in async-heavy compare work
- early queue/callback order drift can be structurally real without yet deciding which run first left the behaviorally shared path
- analysts should align on one delivery class, consumer family, or synchronization-bearing boundary rather than overreading cross-thread micro-order

## Working synthesis
A stable practical rule emerges:

1. **broad async entry is weaker than delivery-class alignment**
   - two runs can both enter the same event loop, queue family, or callback registration region while still drifting in non-explanatory early scheduling details
2. **event order is not automatically the compare boundary**
   - early queue pops, worker wakeups, or callback timestamps may be real yet still too weak to answer the actual operator question
3. **choose one context-bearing async boundary**
   - better boundaries include:
     - first delivered callback family with downstream effect
     - first dequeued work item carrying the target object/session/request id
     - first queue-owner handoff that makes a later consumer inevitable
     - first reducer from many ready events into one specific consumer family
4. **cross-thread chronology is weaker than synchronized semantic continuity**
   - if cross-thread order looks fuzzy, compare one consumer-bearing boundary, one queue-owned object, or one synchronization-bearing handoff instead of raw mixed-thread step order
5. **only then shrink into the watched object**
   - once the first behavior-bearing delivery is bounded, reduce it into one callback slot, queue node, state bit, reducer output, or object field for later reverse-causality / first-bad-write work

## Practical KB rule
The compare-run branch should preserve this compact async-heavy continuation:

```text
good compare pair exists
  -> early queue/callback order drifts
  -> do not treat raw event order as the compare boundary by default
  -> align on one delivery class / consumer-bearing boundary
  -> isolate the first behavior-bearing delivered callback / dequeued work item / reducer output
  -> shrink that into one watched object
  -> only then widen into reverse-causality or branch-specific proof
```

This is not a new broad taxonomy object.
It is a practical refinement inside compare-run work that prevents analysts from:
- confusing broad async subsystem entry with behavioral alignment
- overreading thread interleaving or queue order churn as explanation
- asking whole-trace TTD/rr queries before naming one narrower delivery boundary

## Suggested maintenance use
Use this note to justify:
- strengthening the compare-run workflow note with explicit async queue/callback-heavy alignment language
- strengthening the runtime-evidence subtree guide and parent runtime page so this stop rule survives as branch memory
- updating top-level index memory so runtime-evidence compare work preserves one practical route from noisy async delivery to watched-object reduction

Use it conservatively.
It supports a narrower operator refinement inside an already-established compare-run branch rather than a new top-level topic.