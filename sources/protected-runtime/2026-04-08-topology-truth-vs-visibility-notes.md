# Protected-runtime observation topology — truth vs visibility notes

Date: 2026-04-08
Branch target: protected-runtime practical workflows / observation-topology selection
Purpose: preserve a source-backed operator refinement for cases where earlier or richer user-space instrumentation improves visibility, but a lower-surface boundary may still provide truer evidence more cheaply.

## Research intent
Strengthen the existing protected-runtime observation-topology workflow note with a narrower comparison rule:
- better user-space visibility is not automatically better evidence
- lower-surface truth can beat richer in-process comfort when anti-instrumentation distortion dominates

## Search artifact
Raw multi-source search artifact:
- `sources/protected-runtime/2026-04-08-0751-topology-search-layer.txt`

Requested source set:
- `exa,tavily,grok`

Observed search-source reality for this run:
- Exa returned usable Frida, DBI, and tracing surfaces
- Tavily returned usable Frida / DBI / tracing surfaces
- Grok was explicitly invoked and failed with repeated `502 Bad Gateway` through the configured proxy path

## Retained sources
1. Frida documentation surfaces
   - Gadget / early instrumentation / injected-vs-embedded posture
2. eBPF / uprobe tracing documentation surfaces
   - lower-overhead, lower-surface tracing near syscall/user-kernel boundaries
3. DynamoRIO / Intel Pin documentation surfaces
   - rich DBI visibility with nontrivial overhead and instrumentation presence

## High-signal retained findings

### 1. Earlier Frida/Gadget access improves posture, but not automatically truth
Frida Gadget and other earlier-load postures can solve attach/spawn timing problems and improve in-process reach.

Practical consequence:
- this often buys better user-space visibility
- but it does not automatically solve target-shaped distortion or anti-instrumentation churn
- treat earlier load as a topology option, not an automatic truth upgrade

### 2. DBI can increase visibility while still changing the case economics
Rich DBI surfaces like DynamoRIO / Pin can expose broad control structure and execution detail.

Practical consequence:
- they are often the right choice when control structure is the missing object
- but they are not automatically the cheapest truth-preserving move when the real question lives at a lower boundary and anti-instrumentation churn is already dominating

### 3. Lower-surface boundaries can be cheaper truth objects when user-space evidence is too distorted
Syscall-adjacent, transport-adjacent, and similar lower-surface tracing surfaces can sacrifice some semantic comfort while preserving a truer event boundary.

Practical consequence:
- when the question is about whether one request, IPC handoff, or kernel-adjacent event really happened, a lower-surface boundary may answer the question more directly than richer in-process tracing
- do not choose visibility comfort over evidence quality by habit

## Practical synthesis worth preserving canonically
A compact comparison ladder for this seam is:

```text
visibility improved
  != distortion reduced
  != lower-surface truth gained
  != useful semantic consequence recovered
```

This keeps four different successes separate:
1. **visibility improved**
   - you can see more user-space events, hooks, or trace detail
2. **distortion reduced**
   - the new posture actually removes anti-instrumentation churn or compare-run contamination
3. **lower-surface truth gained**
   - a syscall/transport/boundary-adjacent surface now answers the question more directly
4. **useful semantic consequence recovered**
   - the new topology has already yielded one smaller next target or one later trustworthy effect

## Best KB use of this material
This material is best used to sharpen the existing protected-runtime observation-topology workflow note.
It should not become a broad tooling-comparison page.

The operator-facing value is:
- do not treat earlier Frida/Gadget posture as automatic truth improvement
- do not treat richer DBI visibility as automatic proof that the better topology has been chosen
- ask whether a lower-surface boundary would answer the actual question more directly and more honestly
- stop once one smaller next target or later consequence is made trustworthy

## Search reliability note
This was a degraded-source external pass, not a fully healthy tri-source result set.
It still counts as a real external-research attempt because `exa,tavily,grok` were explicitly requested and Grok was actually invoked; its failure is recorded clearly.
