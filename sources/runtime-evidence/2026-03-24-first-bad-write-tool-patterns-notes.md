# Source notes — first-bad-write and decisive-reducer localization with rr, WinDbg TTD, Pernosco, and Binary Ninja

Date: 2026-03-24
Topic cluster: runtime evidence / first bad write / decisive reducer / reverse execution / watchpoints / time-travel debugging

## Scope
This pass was intentionally narrower than the broader runtime-evidence and reverse-causality notes.
The goal was to collect practical operator guidance for the recurring situation where:

- the late bad state is already visible
- replay or time-travel support exists
- the missing step is not broad trace navigation
- the missing step is picking the right watched object and finding the first bad write or first decisive reducer behind it

This note emphasizes concrete debugger-supported moves rather than broad conceptual taxonomy.

## Search mode used in this run
Multi-source search was explicitly attempted via search-layer with:
- `--source exa,tavily,grok`

Queries used:
- `reverse engineering first bad write watchpoint time travel debugging rr Pernosco WinDbg TTD practical workflow`
- `rr reverse watchpoint practical debugging first bad write reducer localization`
- `WinDbg TTD data watchpoint reverse execution practical first bad write`

## Sources used in this pass
Primary sources fetched or revalidated in this pass:
- rr project page — https://rr-project.org/
- Microsoft Learn TTD walkthrough — https://learn.microsoft.com/en-us/windows-hardware/drivers/debuggercmds/time-travel-debugging-walkthrough
- Pernosco debugging workflow — https://pernos.co/about/workflow
- Binary Ninja Windows TTD documentation — https://docs.binary.ninja/guide/debugger/dbgeng-ttd.html
- search-layer result set captured in `sources/runtime-evidence/2026-03-24-first-bad-write-search-layer.txt`

A Red Hat rr article was also attempted via `web_fetch` but returned 403 in this environment.
That source should be treated as attempted-but-blocked, not silently omitted.

## High-signal findings

### 1. rr states the core operator move very directly
The rr project page is unusually clear about the workflow value:
- record once
- replay deterministically
- set a hardware data watchpoint on the bad field
- use reverse execution to run back to where it changed

The key practical signal is not just “reverse debugging exists.”
It is that rr treats **watchpoint + reverse execution** as the main way to go from a wrong late value to the code that set it.
That directly supports keeping the KB focused on first-bad-write localization rather than generic replay admiration.

### 2. Microsoft’s TTD walkthrough gives an explicit step-by-step first-bad-write ladder
The TTD walkthrough is valuable because it provides a concrete ordered recipe:
1. find the exception event
2. move to the faulting point
3. step backward until the suspicious variable comes into scope
4. identify the bad variable
5. determine its address
6. set `ba` on that address
7. use `g-` to run back to the last access/write
8. if that location is only an intermediate edge, repeat with the earlier variable behind it

This is stronger than vague time-travel guidance because it explicitly endorses an iterative watched-object reduction loop.
That loop maps well to the KB’s wording around:
- narrow watched object
- first useful write/reducer
- repeat only if the current boundary is still too downstream

### 3. Pernosco reinforces the “capture once, debug later” division of labor
Pernosco’s workflow page is not deep on command details, but it provides an important workflow signal:
- recording and debugging can be separated
- QA or automation can produce the rr trace
- analysis can happen later on the preserved artifact

This matters for the KB because first-bad-write work is often blocked less by theory than by the cost of reproducing the bad run.
Pernosco strengthens the argument that the real unit of progress is a stable execution artifact plus a good watched-object choice, not repeated live reruns.

### 4. Binary Ninja’s TTD integration strengthens the “query plus disassembly” workflow
Binary Ninja’s TTD docs show that a practical TTD workflow is not limited to manual stepping.
The important signals are:
- reverse controls (`g-`, `p-`, `t-`, `g-u`)
- `!tt` / position navigation
- memory and call query surfaces
- TTD.Memory / TTD.Calls-backed widgets
- strong warning that overly broad queries can stall the UI and should be scoped carefully

This is directly useful for KB maintenance because it supports a concrete caution:
- do not widen the watched object or query scope more than necessary
- broad memory-event searching is often worse than first shrinking the semantic target

### 5. The right watched object is usually smaller than the first visible late object
Across rr, TTD, and BN signals, the practical winning move is often:
- late object is visible
- but the watched object is a smaller field / slot / slice / reducer output inside it

Examples that match the docs and search results:
- one struct field instead of the whole object
- one local policy enum instead of the larger callback/result object
- one buffer slice instead of the full region
- one reducer output or derived slot instead of raw parser output

This should remain a canonical rule in the runtime-evidence branch because it determines whether reverse watchpoints return leverage or noise.

### 6. “First bad write” is often really “first causally useful reducer”
The TTD walkthrough itself models an iterative version of this:
- you watch one bad variable
- walk back to the last access/write
- then decide whether the true leverage is still one variable earlier

That means the KB should not over-literalize “first bad write.”
In practice, the good stopping boundary is often:
- the first write into a durable policy slot
- the first queue insertion that predicts later work
- the first reduction from rich result material into a smaller branch-driving bucket
- the first ownership/registration edge that makes a later callback possible

So the operator question is not “what instruction touched bytes first?”
It is “what earliest write/reducer edge changes the next decision I can make?”

### 7. Tooling supports the workflow, but scope discipline is what makes it usable
The most reusable practical cautions from this pass are:
- do not start with whole-trace archaeology
- do not watch an oversized object if only one field predicts behavior
- do not run broad TTD memory queries if you can already isolate one smaller region or slot
- do not keep iterating backward once one boundary already yields a smaller next proof target
- do not confuse first related helper with first behavior-bearing write/reducer

## Practical synthesis
A strong cross-tool operator rule from this pass is:

```text
Once a bad late state is already visible,
use replay/time-travel support to shrink that state into the smallest truthful watched object.
Then run backward to the first causally useful write or reducer behind it.
If that boundary still feels semantically too rich or too downstream,
repeat once on the smaller earlier variable behind it.
Stop as soon as one boundary yields one smaller trustworthy next target.
```

## KB implications from this pass
This pass supports making the runtime-evidence branch more practical in four specific ways:

1. keep `first-bad-write-and-decisive-reducer-localization-workflow-note.md` explicitly tool-aware
   - rr reverse watchpoint shape
   - WinDbg TTD `ba` + `g-` shape
   - Binary Ninja scoped-query shape
   - Pernosco capture-now/debug-later workflow value

2. preserve a canonical caution that **query scope is part of correctness**, not only performance
   - broad watch regions and broad memory queries often degrade operator truth

3. keep routing language pointed toward downstream consumer/consequence proof
   - first-bad-write localization should hand off quickly once the next smaller target is obvious

4. treat blocked fetches conservatively in run reports
   - attempted source != usable source
   - blocked Red Hat fetch should be recorded as degraded evidence, not silently promoted

## Best next continuation after this note
A future runtime-evidence pass could usefully add one narrower practical note about:
- when to stop at the first bad write
- versus when to keep going to the first downstream consumer/consequence edge

That would help prevent the branch from stopping too often at write-localization language alone.
