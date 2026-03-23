# Source notes — compare-run alignment under nondeterminism and noisy early divergence

Date: 2026-03-23
Topic: runtime evidence / compare-run design / nondeterminism masking / first meaningful divergence isolation
Purpose: source-backed practical notes for the runtime-evidence branch on what to do when early compare noise is dominated by scheduler churn, background tasks, timing variance, checksums, handles, or other non-semantic drift before the first behavior-bearing divergence

## Why this note exists
The runtime-evidence branch already had a useful compare-run workflow note.
What still needed sharper practical preservation was a recurring subcase:

```text
I already have a plausible compare pair
  + but the earliest textual or event-level differences are noisy
  + and scheduler/timing/randomness/environment churn may be masking the first real divergence
  -> reclassify early differences as alignment noise or candidate semantic split
  -> move to a more truthful compare level or boundary
  -> isolate the first behavior-bearing divergence, not the first raw mismatch
```

This note supports a conservative KB improvement:
- do not treat the first mismatch as the first useful divergence by default
- when early compare surfaces are noisy, preserve a practical alignment step before deeper reverse-causality
- remember that compare-run quality depends not only on pair design, but also on choosing the right comparison level and filtering known nondeterministic churn

## Search intent
Queries explicitly attempted through search-layer:
- `reverse engineering compare runs nondeterminism first divergence rr pernosco trace diff`
- `time travel debugging compare execution nondeterministic noise first meaningful divergence replay debugging`
- `trace diff debugging nondeterminism alignment compare runs scheduler noise`

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
- ACM Queue article fetch was blocked by Cloudflare during direct follow-up
- one PDF follow-up degraded to raw PDF bytes and was not used as quote-grade evidence

## Representative sources used

### Tetrane — Reverse engineering through trace diffing: several approaches
URL:
- https://blog.tetrane.com/2021/reverse-engineering-through-trace-diffing-several-approaches.html

Useful signals:
- trace-diff value depends on comparing nearby scenarios and choosing the comparison level on purpose
- diffing all instructions too early is explicitly described as yielding too many results
- broader surfaces such as call-level views can isolate the meaningful region before finer diffing
- custom compare views get more useful when they carry context like call arguments, return values, or data-bearing bytes instead of raw instruction churn
- some early differences are visible but obviously irrelevant to the analyst question, such as checksum variation

Practical extraction:
- first visible differences may be real but not yet meaningful
- early compare work should classify obvious protocol/checksum/address churn as likely alignment noise unless it predicts later behavior
- when noise dominates, move to a compare level that preserves semantic continuity better: calls, filtered instruction regions, taint-relevant slices, or context-enriched views
- compare-run success often comes from narrowing the region before deepening the diff

### Robert O'Callahan — How To Track Down Divergence Bugs In rr
URL:
- https://robert.ocallahan.org/2016/06/how-to-track-down-divergence-bugs-in-rr.html

Useful signals:
- divergence bugs often stem from nondeterminism that differs between recording and replay
- rr usually detects divergence soon after it is caused because control-flow changes perturb counters quickly
- when the divergence is only in a few register values, reasoning backward from the bad value is useful
- disabling syscall buffering can catch divergence earlier by increasing observation density
- more aggressive scheduling/check frequency can expose earlier divergence, though at heavy cost
- memory checksumming can catch earlier state divergence when visible failure appears later

Practical extraction:
- when compare noise hides the first real split, increase observation density near the suspected boundary instead of narrating the whole run
- if the visible divergence is late, use narrower instrumentation or checksumming around candidate objects to catch an earlier causal mismatch
- treat scheduler/context-switch behavior as a practical noise source and control it when the target question is smaller than whole-run behavior
- compare-run work should aim to catch the earliest behavior-bearing divergence that remains stable under replay or controlled reruns

### Pernosco vision page
URL:
- https://pernos.co/about/vision/

Useful signals:
- omniscient debugging turns execution history into a queryable data-analysis problem rather than a raw transcript
- the benefit comes from asking smaller questions against preserved state and time, not from drowning in total history

Practical extraction:
- noisy compare cases need better query framing, not broader trace narration
- when many early mismatches exist, the next move is often to re-ask a narrower question at a better compare boundary

## Working synthesis
A stable practical rule emerges from these sources:

1. **pair design is necessary but not sufficient**
   - even a good near-neighbor pair may still show early noise from checksums, handles, scheduler churn, or background effects
2. **the first mismatch is not automatically the first meaningful divergence**
   - early differences should be triaged into:
     - expected nondeterministic churn
     - setup drift that invalidates the pair
     - true semantic split candidates
3. **alignment is a real operator step**
   - if instruction-level or broad event diff is noisy, move upward or sideways to a compare level that preserves semantic continuity better
4. **observation density can be changed on purpose**
   - more frequent state checks, narrower traces, or watched-object checksumming can reveal the first useful divergence earlier
5. **the target remains one smaller trustworthy divergence boundary**
   - once one behavior-bearing split is found, hand off to reverse-causality or branch-specific proof instead of continuing broad alignment work

## Practical KB rule
The compare-run branch should preserve a small but important continuation:

```text
good compare pair exists
  -> early mismatches appear
  -> classify likely nondeterministic noise vs semantic split candidates
  -> move to a more truthful compare boundary or level if needed
  -> increase observation density only around the narrowed region
  -> isolate the first behavior-bearing divergence
```

This is not a new giant taxonomy object.
It is a practical refinement inside compare-run work that prevents analysts from:
- overreacting to the first raw mismatch
- explaining checksum/handle/timing churn as if it were the root cause
- abandoning compare work when the real problem is compare-level choice

## Suggested maintenance use
Use this note to justify:
- strengthening the compare-run workflow note with explicit nondeterminism/alignment handling
- adding routing language about reclassifying early differences before widening into reverse-causality
- strengthening the runtime-evidence subtree guide so compare-run work does not silently assume that the first mismatch is the meaningful one

Use it conservatively.
It supports a practical workflow refinement, not a claim that all noisy compare problems reduce to one universal method.