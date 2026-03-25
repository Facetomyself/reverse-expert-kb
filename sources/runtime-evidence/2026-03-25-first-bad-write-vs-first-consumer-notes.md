# Source notes — when to stop at the first bad write versus when to carry one more hop to the first downstream consumer

Date: 2026-03-25
Topic cluster: runtime evidence / first bad write / decisive reducer / downstream consumer / stop rule / reverse debugging

## Scope
This pass was a targeted continuation of the runtime-evidence branch’s first-bad-write work.
The specific operator question was:

- once a bad late object is already visible,
- and replay / reverse execution / TTD-style querying can localize the first bad write or decisive reducer,
- when is that boundary already enough,
- and when should the analyst carry the case one more hop to the first downstream consumer or consequence edge?

The goal was not to add another generic reverse-debugging page.
The goal was to sharpen the branch stop-rule so the KB does not encourage either:
- stopping too early at a purely local write with no operational meaning, or
- drifting into endless trace browsing after a useful boundary already exists.

## Search mode used in this run
Multi-source search was explicitly attempted via search-layer with:
- `--source exa,tavily,grok`

Queries used:
- `reverse engineering first bad write stop rule downstream consumer consequence reverse debugging`
- `rr watchpoint first bad write versus later consumer proof debugging`
- `WinDbg TTD watchpoint root cause first write versus first use workflow`

Search artifact:
- `sources/runtime-evidence/2026-03-25-first-bad-write-vs-first-consumer-search-layer-1916.txt`

## Sources used in this pass
Primary retained sources fetched or revalidated in this run:
- Microsoft Learn — Time Travel Debugging walkthrough
  - <https://learn.microsoft.com/en-us/windows-hardware/drivers/debuggercmds/time-travel-debugging-walkthrough>
- Binary Ninja TTD documentation
  - <https://docs.binary.ninja/guide/debugger/dbgeng-ttd.html>
- Meta Engineering — Reverse debugging at scale
  - <https://engineering.fb.com/2021/04/27/developer-tools/reverse-debugging/>

The search-layer run also returned lower-signal or mixed-signal material (forums, generic watchpoint explanations, product marketing, issue trackers). Those informed search direction but were not treated as canonical support for the KB wording.

## High-signal findings

### 1. Microsoft’s TTD walkthrough supports an iterative “suspect variable -> earlier variable” ladder
The clearest operator signal in Microsoft’s walkthrough is not just that TTD can go backward.
It is that the workflow is explicitly iterative:
- identify the suspicious variable at the faulting point
- set `ba` on its address
- use `g-` to run back to the last access/write
- if that location still only explains the value through an earlier variable, repeat on the earlier variable

That supports a canonical rule for the KB:
- a localized first bad write is often a **useful intermediate boundary**
- but if it still does not explain the operationally meaningful state transition, carrying the case one smaller variable or one smaller boundary upstream is legitimate

At the same time, the walkthrough is still about finding the code flaw efficiently, not reconstructing the entire history.
So the practical lesson is bounded iteration, not “keep walking forever.”

### 2. Binary Ninja’s TTD docs make scoped queries part of correctness, not just performance
The strongest signal from the BN TTD docs is the warning about broad TTD queries:
- wide call or memory queries can block the UI
- large address ranges are expensive
- you should scope the symbols/ranges tightly and test with small ranges first

For KB workflow design, this means:
- watched-object choice and query scope are part of **truth selection**
- an over-broad watched region can be technically real but still return the wrong explanatory boundary for the analyst’s actual question

This strengthens the stop-rule around first-bad-write work:
- if one small field / slot / slice / reducer output already predicts the consequence, use that
- do not widen the watched object merely because the tooling can answer larger memory questions

### 3. Meta’s reverse-debugging writeup reinforces outcome-oriented navigation
Meta’s writeup is production-oriented rather than reverse-engineering-specific, but it carries a useful workflow signal:
- preserved execution history is valuable because it lets the engineer move quickly to the function call or branch that should not have happened
- the value is not broad historical admiration; it is shorter root-cause localization

That supports a conservative operator rule in the KB:
- reverse-debugging power exists to reduce the task into one smaller actionable target
- if the first bad write/reducer already gives a branch-specific next task, stop there
- if it still leaves “who operationalizes this state?” unanswered, carry the case exactly one more hop to the first downstream consumer/consequence edge
- after that, hand off instead of continuing generic trace browsing

### 4. The right question is often “who operationalizes the localized state?”
The existing runtime-evidence branch already emphasized proving one downstream dependency.
This pass sharpens that into a more operational question:

```text
I found the first bad write or decisive reducer.
Is that already enough to pick the next branch-specific task?
If not, who is the first narrower consumer/consequence edge that actually operationalizes this state?
```

Typical “one more hop” cases:
- one policy bucket write is localized, but the first retry scheduler / request builder / callback consumer that uses it is still unknown
- one queue-state write is localized, but the first worker/dequeue/action edge that makes it behaviorally real is still unclear
- one normalized/decrypted buffer is localized, but the first parser / request / dispatch consumer that makes it matter is still missing

Typical “stop here” cases:
- the first bad write already names the smaller helper/reducer family that clearly becomes the next static target
- the localized reducer already cleanly partitions accepted vs rejected / good vs bad runs
- the write already collapses the case into a well-formed branch-specific proof question

### 5. The right stop-rule is “zero or one more hop,” not indefinite continuation
The main workflow improvement from this pass is a tighter stop-rule:
- do not stop too early at a write that is still too local to explain the behavior-bearing consumer
- but also do not drift into endless consumer chasing

A good practical rule is:
- localize one watched object and one first useful write/reducer boundary
- if that boundary already makes the next branch-specific task obvious, hand off
- if it does not, carry the case exactly **one more hop** to the first downstream consumer/consequence edge that operationalizes it
- then stop generic reverse-debugging work and hand off to the narrower branch-specific question

That keeps the runtime-evidence branch practical instead of turning it into either:
- premature-localization theater, or
- generic trace archaeology.

## Practical synthesis
A compact operator rule worth preserving is:

```text
visible bad late object
  -> narrow watched object
  -> first useful write or decisive reducer
  -> if that already makes the next branch-specific task obvious, hand off
  -> otherwise carry the case one more hop to the first downstream consumer/consequence edge
  -> then hand off
```

## KB implications from this pass
This pass supports three concrete KB moves:

1. strengthen the runtime-evidence subtree guide
   - preserve the explicit choice between:
     - stopping at the localized write/reducer, or
     - carrying the case one more hop to the first consumer/consequence edge

2. strengthen the first-bad-write workflow note
   - make the stop-rule explicit
   - keep the downstream-consumer hop bounded to one narrow operationalizing edge

3. preserve the tool-derived caution that broad query scope is not just slower, but often less truthful
   - especially in TTD/query-heavy workflows

## Search audit
Search sources requested:
- exa
- tavily
- grok

Search sources succeeded:
- exa
- tavily

Search sources failed:
- grok
  - failure observed during this run as `502 Server Error: Bad Gateway` from the configured Grok endpoint

Exa endpoint:
- `http://158.178.236.241:7860`

Tavily endpoint:
- `http://proxy.zhangxuemin.work:9874/api`

Grok endpoint:
- `http://proxy.zhangxuemin.work:8000/v1`

Degraded source-set status:
- multi-source search was explicitly attempted with `exa,tavily,grok`
- effective successful source set for this pass was `exa+tavily`
- this still counts as a real external-research-driven pass because all three sources were actually invoked and the Grok failure was recorded clearly
- Grok-only execution was not used and is still treated as degraded mode, not normal mode
