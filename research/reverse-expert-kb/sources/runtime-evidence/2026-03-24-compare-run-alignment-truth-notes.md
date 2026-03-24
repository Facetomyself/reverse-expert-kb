# Source notes — compare-run alignment truth and non-explanatory early divergence

Date: 2026-03-24
Topic: runtime evidence / compare-run design / alignment truth / first meaningful divergence isolation
Purpose: preserve a narrower practical rule for compare-run work when early mismatches are real but still not explanatory for the analyst's actual question

## Why this note exists
The runtime-evidence branch already preserved several useful compare-run rules:
- design the compare pair on purpose
- hold invariants steady
- choose a first compare boundary instead of diffing whole traces blindly
- do not confuse the first mismatch with the first meaningful divergence

What still needed a sharper practical stop rule was a common subcase:

```text
I already have a plausible compare pair
  + I can see early differences
  + some of those differences are real, but may still be non-explanatory
  + I still do not know whether to tolerate them, redesign the pair, or treat one as the first semantic split
  -> separate alignment truth from causality truth
  -> classify early differences before narrating causes
  -> only then widen into reverse-causality or branch-specific proof
```

This note supports a conservative KB improvement:
- preserve an explicit **alignment truth** step inside compare-run work
- distinguish:
  - tolerated early variation
  - pair-breaking misalignment
  - first behavior-bearing divergence
- keep analysts from overexplaining early but non-explanatory differences

## Search intent
Queries explicitly attempted through search-layer:
- `reverse engineering compare run first meaningful divergence noisy early mismatch trace diff deterministic replay`
- `rr pernosco divergence debugging first divergence compare runs reverse engineering`
- `time travel debugging reverse engineering trace diff noise first meaningful divergence`

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
- grok

Failed sources:
- none in the search-layer attempt itself

Configured endpoints on this host:
- Exa: `http://158.178.236.241:7860`
- Tavily: `http://proxy.zhangxuemin.work:9874/api`
- Grok: `http://proxy.zhangxuemin.work:8000/v1`

Additional fetch status during source follow-up:
- Tetrane trace-diffing article fetched successfully
- rr divergence-debugging article fetched successfully
- Microsoft Learn TTD overview fetched successfully
- Pernosco vision page fetched successfully

Primary raw search artifact:
- `sources/runtime-evidence/2026-03-24-compare-run-noisy-early-divergence-search-layer.txt`

## Representative sources used

### Tetrane — Reverse Engineering through trace diffing: several approaches
URL:
- https://blog.tetrane.com/2021/reverse-engineering-through-trace-diffing-several-approaches.html

Useful signals:
- diffing value depends on comparing nearby scenarios on purpose
- diffing all instructions too early is explicitly described as yielding too many results
- broader comparison levels such as call-level views, coverage, and context-enriched comparisons can narrow the region before finer diffing
- some early differences are visible but intentionally ruled out as irrelevant to the analyst question, such as checksum variation

Practical extraction:
- an early mismatch can be real without yet being explanatory
- compare-run work should preserve a step that asks whether early differences are merely tolerated variation at the current boundary
- when that is not enough, move to a compare level that preserves semantic continuity better before narrating cause

### Robert O'Callahan — How To Track Down Divergence Bugs In rr
URL:
- https://robert.ocallahan.org/2016/06/how-to-track-down-divergence-bugs-in-rr.html

Useful signals:
- many replay divergences are detected near the point where control flow or register state truly leaves the recorded path
- when divergence is only in a few register values, reasoning backward can work
- when visibility is too sparse, disabling syscall buffering or increasing recorded state frequency can catch divergence earlier
- memory checksumming can help when visible failure appears later than the earlier state mismatch that predicts it

Practical extraction:
- if the current compare level catches mismatches too late or too noisily, increase observation density near the suspected boundary instead of broadening the whole explanation
- early differences must be triaged before they are treated as causal leads
- some early mismatches indicate the pair is not comparable enough at the current level rather than revealing the root split directly

### Microsoft Learn — Time Travel Debugging Overview
URL:
- https://learn.microsoft.com/en-us/windows-hardware/drivers/debuggercmds/time-travel-debugging-overview

Useful signals:
- time-travel debugging is valuable because it preserves execution for repeated query and replay instead of repeated repro effort
- indexed trace/query workflows help answer smaller questions against preserved execution rather than re-running broad live sessions
- traces are costly and can be large, so practical use depends on scoping and choosing useful query targets

Practical extraction:
- compare-run work should ask smaller, queryable alignment questions rather than widening into giant transcript narration
- a useful compare boundary is one that supports repeated, scoped checking of where behavior first stops being meaningfully shared

### Pernosco vision page
URL:
- https://pernos.co/about/vision/

Useful signals:
- omniscient debugging turns execution history into a queryable data-analysis problem
- compare value is especially strong for closely related executions where one passes and the other fails
- the hard problem is not just storing history, but choosing interfaces and queries that explain why something did or did not happen

Practical extraction:
- compare-run work benefits from treating alignment as a query-framing problem
- when early mismatches are plentiful, the next useful move is often to ask a narrower alignment question at a better boundary rather than to widen the causal story

## Working synthesis
A stable practical rule emerges:

1. **alignment truth comes before causality truth**
   - before asking what caused a divergence, first decide what kind of divergence you are looking at
2. **early mismatches split three ways**
   - tolerated early variation
   - pair-breaking misalignment
   - first behavior-bearing divergence
3. **real does not automatically mean explanatory**
   - a checksum change, handle drift, queue-order perturbation, or bookkeeping mismatch can be perfectly real without answering the analyst's actual question
4. **comparison level is part of the method**
   - if instruction-level or raw event-level diff is too noisy, move to calls, validated objects, reducer outputs, queue ownership, or other context-bearing boundaries
5. **observation density should be local, not indiscriminate**
   - increase checks or trace detail around the suspected boundary rather than broadening the whole trace narrative

## Practical KB rule
The compare-run branch should preserve this compact continuation:

```text
good compare pair exists
  -> early differences appear
  -> ask the alignment-truth question first
  -> separate tolerated variation vs pair-breaking misalignment vs first explanatory split
  -> repair the compare level/boundary if needed
  -> only then widen into reverse-causality or domain-specific proof
```

This is a practical refinement, not a new giant taxonomy object.
It improves how analysts decide whether the current pair is:
- good enough
- misaligned
- or already pointing at the right next causal target

## Suggested maintenance use
Use this note to justify:
- strengthening the compare-run workflow note with explicit alignment-truth language
- strengthening the runtime-evidence subtree guide so branch routing preserves this stop rule canonically
- updating top-level branch memory so this practical distinction does not live only in one leaf

Use it conservatively.
It supports a narrower operator refinement inside an already-established compare-run branch.
