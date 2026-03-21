# Compare-run design and divergence-isolation notes

Date: 2026-03-21
Topic: runtime evidence / compare-run design / divergence isolation / replay-supported diffing
Purpose: source-backed practical notes for designing useful compare pairs and isolating the first meaningful divergence before deeper reverse-causality work

## Why this note exists
The runtime-evidence branch already had pages on:
- record/replay and omniscient debugging
- representative execution and trace-anchor choice
- reverse-causality localization

What still needed more explicit practical treatment was a step that often occurs between those pages:
- how to choose or design a useful compare pair
- how to avoid noisy accepted-vs-rejected or crash-vs-no-crash comparisons
- how to isolate the first meaningful divergence without diffing the entire execution indiscriminately

The source families below converge on the same operator lesson:
- compare value depends heavily on pair design
- traces should be compared at the right level, not the deepest level by default
- the target is usually one bounded divergence that narrows the next proof step, not a maximal catalog of all differences

## Sources consulted

### Tetrane — Reverse engineering through trace diffing: several approaches
URL:
- https://blog.tetrane.com/2021/reverse-engineering-through-trace-diffing-several-approaches.html

Useful signals:
- the article compares nearby scenarios rather than unrelated runs: crash vs non-crash / changed input vs baseline.
- it explicitly discusses choosing the comparison level: calls, coverage, instructions, or custom context-bearing mixes.
- it warns that diffing everything too early produces too many results.
- it shows practical value in beginning with broader comparison surfaces, then narrowing once the right region is identified.
- custom compare views become much more useful when they embed context such as call arguments, returned buffer bytes, or data-bearing features instead of raw instruction churn alone.

Practical extraction:
- design the pair before diffing it
- compare at the shallowest level that still isolates the right region
- only deepen after a smaller divergence-bearing region is already visible
- the first useful divergence is often one call family, data-return difference, or coverage region, not the full instruction diff

### Binary Ninja docs — Time Travel Debugging (Windows)
URL:
- https://docs.binary.ninja/guide/debugger/dbgeng-ttd.html

Useful signals:
- TTD queries can be expensive and broad queries are explicitly warned against.
- TTD Calls and TTD Memory widgets are described as query surfaces that need to be scoped appropriately.
- the tooling highlights query design, symbol families, return-address ranges, and memory-access ranges as practical ways to keep the search bounded.

Practical extraction:
- compare work should start from scoped event families and bounded address/query ranges when possible
- the first compare boundary should usually be chosen to reduce search volume, not after the fact
- large trace capability does not remove the need for a smaller intended boundary

### Pernosco vision page
URL:
- https://pernos.co/about/vision/

Useful signals:
- omniscient debugging is framed as turning debugging into a data-analysis problem over all program states.
- the value comes from queryable, indexed state and time-crossing views, not from raw possession of execution history.

Practical extraction:
- compare-run value depends on formulating the query and bounded question well
- when the execution history is queryable, the operator still needs one smaller compare question to avoid wandering

### rr project page
URL:
- https://rr-project.org/

Useful signals:
- rr emphasizes repeated deterministic replay of one recorded execution.
- reverse execution and watchpoints are valuable because they let analysts walk from visible bad state toward the responsible earlier write.

Practical extraction:
- if compare-run work already isolates one meaningful divergence, rr-style reverse/debug workflows can then take over for deeper causality
- compare-run design should therefore aim to hand off one bounded divergence, not a huge uncontrolled difference set

## Lower-confidence / partial-use signals

### MIT omniscient-debugging PDF fetch
URL:
- https://dspace.mit.edu/bitstream/handle/1721.1/124243/1145019144-MIT.pdf?sequence=1&isAllowed=y

Status:
- direct fetch degraded to raw PDF bytes in this environment

Usefulness:
- not used as a quote-bearing source in this note

## Working synthesis
A good compare-run workflow separates four operator choices that are easy to blur together:

1. **pair design**
   - choose two nearby executions that differ in one intended way
2. **invariant control**
   - hold as much non-target setup constant as practical
3. **compare boundary selection**
   - choose the first surface where alignment is still believable and downstream divergence is likely to matter
4. **divergence isolation**
   - find the first meaningful difference, not the first textual difference and not the fullest possible difference list

This matters because weak compare-run design creates two kinds of waste:
- the diff becomes dominated by setup drift and incidental noise
- later reverse-causality work is spent explaining the wrong differences

## Candidate compare boundaries
Useful first compare boundaries often include:
- first shared request-finalization or send boundary
- first parser entry or smaller validated object
- first callback fire after shared registration/setup
- first queue insertion or wakeup after a common trigger
- first module load or artifact consumer after shared initialization
- first state reduction / policy bucket assignment near the visible outcome
- first call family whose arguments or returns already expose the relevant input contrast

## Practical rule for the KB
The runtime-evidence branch should preserve a distinct step between:
- representative run / anchor choice
- and full reverse-causality localization

That distinct step is:
- design one useful compare pair
- choose one first compare boundary
- isolate one first meaningful divergence

This is what the new workflow note should encode.
