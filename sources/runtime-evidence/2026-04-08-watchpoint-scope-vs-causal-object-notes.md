# Watchpoint scope vs causal-object selection notes

Date: 2026-04-08
Branch target: runtime-evidence practical workflows / compare-run divergence isolation
Purpose: preserve a source-backed operator refinement for compare-run and watchpoint-heavy cases where a real access hit occurs, but the watched object/range is still broader than the actual causal object that predicts later behavior.

## Research intent
Strengthen the existing compare-run divergence note with a sharper separation between:
- watchable object/range truth
- real access/hit truth
- causal object selection truth
- later consequence-bearing reduction truth

## Search artifact
Raw multi-source search artifact:
- `sources/runtime-evidence/2026-04-08-1156-watch-scope-search-layer.txt`

Requested source set:
- `exa,tavily,grok`

Observed search-source reality for this run:
- Exa returned usable debugger/watchpoint surfaces
- Tavily returned usable debugger/watchpoint surfaces
- Grok was explicitly invoked and failed with repeated `502 Bad Gateway` through the configured proxy path

## Retained sources
1. GDB / ROCGDB watchpoint documentation surfaces
   - watchpoint scope, hardware/software limits, masked/ranged watchpoint caveats
2. WinDbg data-breakpoint documentation surfaces
   - break on access/write execution against bounded address ranges
3. Conservative rr / replay-query workflow surfaces retained as support for operator framing

## High-signal retained findings

### 1. A real watchpoint/data-breakpoint hit proves access to the watched location, not automatic semantic correctness of the watched scope
Debugger watchpoint/data-breakpoint materials already preserve a distinction between:
- choosing an address/range to watch
- getting a real hardware/software hit
- deciding whether that watched scope is actually the causal object for the analyst’s question

Practical consequence:
- `hit happened` is weaker than `correct causal object selected`
- do not narrate the first real hit as the first explanatory write/access if the watched object/range is still too broad

### 2. Broad watched scope can return truthful but upstream or aggregate edges
Watchpoint/query materials and replay tooling guidance both support the same field rule:
- broad ranges and broad object selections can return real accesses that are true but semantically upstream, aggregate, or wrapper-level relative to the consequence you care about

Practical consequence:
- treat watched-object/query scope as part of truth selection, not just tooling efficiency
- shrink to one field/slot/slice/reducer output before narrating causality when possible

### 3. Watchability is not the same thing as causal selection
A location can be easy to watch because it is stable, aligned, or debugger-friendly while still being the wrong semantic scope.

Practical consequence:
- the first good watchpoint candidate is not automatically the right causal boundary
- keep watchability, real-hit truth, and causal-object truth separate

## Practical synthesis worth preserving canonically
A compact stop-rule ladder for this seam is:

```text
watchable
  != real hit
  != causally selected object
  != consequence-bearing reduction
```

This keeps four different successes separate:
1. **watchable**
   - one address/range/object is easy enough to instrument or query
2. **real hit**
   - one truthful access/watchpoint/data-breakpoint event occurred
3. **causally selected object**
   - the watched scope now matches the semantic object that answers the question
4. **consequence-bearing reduction**
   - one narrower field/slot/reducer output predicts later behavior

## Best KB use of this material
This material is best used to sharpen the existing compare-run divergence workflow note.
It should not become a broad debugger-tooling page.

The operator-facing value is:
- do not overclaim from a real watchpoint/data-breakpoint hit alone
- keep watched scope selection visible as part of correctness
- shrink broad watched objects before narrating causality
- stop only when one narrower consequence-bearing object is frozen

## Search reliability note
This was a degraded-source external pass, not a fully healthy tri-source result set.
It still counts as a real external-research attempt because `exa,tavily,grok` were explicitly requested and Grok was actually invoked; its failure is recorded clearly.
