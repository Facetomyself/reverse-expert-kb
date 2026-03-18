# Runtime-Evidence Practical Subtree Guide

Topic class: subtree guide
Ontology layers: runtime-evidence practice branch, replay/causality routing, operator ladder
Maturity: structured-practical
Related pages:
- topics/runtime-behavior-recovery.md
- topics/record-replay-and-omniscient-debugging.md
- topics/causal-write-and-reverse-causality-localization-workflow-note.md
- topics/analytic-provenance-and-evidence-management.md
- topics/notebook-and-memory-augmented-re.md

## 1. Why this guide exists
This guide exists because the KB’s runtime-evidence branch already has a strong synthesis page and two useful practical leaves, but it is still easier to read as a short conceptual cluster than as a usable operator ladder.

The branch already had practical entry surfaces for:
- broad runtime answerability and observability framing
- record/replay and execution-history tradeoffs
- reverse-causality localization when one suspicious late effect is already visible

What was missing was the compact routing rule that answers:
- when should I stay at broad runtime-observation strategy versus dropping into a narrower practical note?
- when is the case really about capture stability and revisitable evidence rather than ordinary live hooks?
- when is the next useful move to walk backward from one late effect instead of collecting more trace?

This page makes the branch read more like the native, protocol, malware, and protected-runtime practical subtrees:
- a branch entry surface
- a small set of recurring bottleneck families
- a compact ladder for moving from broad runtime uncertainty toward one smaller causal target

## 2. Core claim
Runtime-evidence practical work is easiest to navigate when the analyst first classifies the current bottleneck into one of three recurring families:

1. **observability / layer-selection uncertainty**
   - the analyst still does not know what to observe, at which layer, or which live evidence would collapse the uncertainty fastest
2. **capture-stability / replay-worthiness uncertainty**
   - the interesting behavior is transient, expensive to reproduce, or too painful to keep rediscovering live, so the real question is whether to stabilize one representative execution for later revisits
3. **late-effect to causal-boundary localization**
   - one suspicious late effect is already visible and revisitable enough, but the first causal write, branch, queue edge, or state reduction that predicts it is still unknown

A compact operator ladder for this branch is:

```text
choose the current runtime-evidence bottleneck
  -> secure the most trustworthy observation or replay surface
  -> reduce one visible effect into one causal boundary question
  -> hand back one smaller next target for static, protocol, malware, mobile, or provenance work
```

The subtree is strongest when read as:
- **observe** the right behavior at the right layer
- **stabilize** one representative execution when live reruns are too fragile
- **walk backward** from one visible late effect to one causal boundary that predicts it

## 3. How to choose the right entry note
### Start with `runtime-behavior-recovery`
Use:
- `topics/runtime-behavior-recovery.md`

Start here when:
- the main uncertainty is still what to observe
- several observation surfaces are plausible and the analyst does not yet know which one will produce the next trustworthy object
- the case still needs broad framing around runtime answerability, observability, hook placement, or trace usefulness
- the analyst is still deciding whether dynamic validation or dynamic discovery is the real next move

Do **not** start here when:
- the main bottleneck is already whether one execution should be captured for stable revisits
- a suspicious late effect is already visible and the real next move is backward causality reduction
- the case has already narrowed to one replay/query/watchpoint-style proof target

### Start with `record-replay-and-omniscient-debugging`
Use:
- `topics/record-replay-and-omniscient-debugging.md`

Start here when:
- the behavior is transient, delayed, or expensive to reproduce
- repeated live debugging is wasting effort
- the analyst needs to decide whether deterministic replay, time-travel debugging, or indexed execution history would make the case materially easier
- the real uncertainty is about capture cost versus evidence stability rather than about one specific causal boundary

Do **not** start here when:
- live observation is already stable enough and replay tradeoffs are no longer the main question
- the effect boundary and one promising causal window already exist, making reverse-causality localization the clearer next step
- the case is mainly about provenance packaging after the causal boundary is already known

### Start with `causal-write-and-reverse-causality-localization-workflow-note`
Use:
- `topics/causal-write-and-reverse-causality-localization-workflow-note.md`

Start here when:
- one suspicious late state, value, event, branch, or delayed consequence is already visible
- replay, reverse execution, indexed query support, or at least one stable compare-run pair exists
- the next useful milestone is the first causal write, branch, queue edge, reducer, or state slot that predicts the visible effect
- the workflow can now be reduced into one effect boundary, one backward search window, and one proof-of-dependency boundary

Do **not** start here when:
- observation itself is still too noisy or distorted to trust
- the case still needs broad layer-selection or runtime-surface choice
- the target is better framed first as protocol parser-to-state proof, native interface-path proof, VM trace reduction, or mobile ownership diagnosis

## 4. Compact ladder across the branch
A useful way to read the branch is as three common runtime-evidence bottleneck families that often chain into one another.

### A. Observation uncertainty -> informative runtime surface
Typical question:
- what should I observe next, and at what layer, to collapse uncertainty fastest?

Primary note:
- `topics/runtime-behavior-recovery.md`

Possible next handoff:
- `topics/record-replay-and-omniscient-debugging.md` when live reruns are too fragile or expensive
- domain-specific branches once one observation surface becomes clearly best, such as:
  - `topics/mobile-protected-runtime-subtree-guide.md`
  - `topics/browser-runtime-subtree-guide.md`
  - `topics/firmware-and-protocol-context-recovery.md`

### B. Fragile live behavior -> stable execution history
Typical question:
- should I keep poking this behavior live, or capture one representative execution so evidence stops evaporating?

Primary note:
- `topics/record-replay-and-omniscient-debugging.md`

Possible next handoff:
- `topics/causal-write-and-reverse-causality-localization-workflow-note.md` when one suspicious late effect is now stable enough to walk backward from
- `topics/analytic-provenance-and-evidence-management.md` when the replay artifact now needs stronger evidence linkage or team handoff discipline

### C. Visible late effect -> first causal boundary
Typical question:
- what first earlier write, branch, reduction, queue edge, or ownership handoff actually predicts the late effect I care about?

Primary note:
- `topics/causal-write-and-reverse-causality-localization-workflow-note.md`

Possible next handoff:
- `topics/native-interface-to-state-proof-workflow-note.md`
- `topics/protocol-parser-to-state-edge-localization-workflow-note.md`
- `topics/staged-malware-execution-to-consequence-proof-workflow-note.md`
- `topics/vm-trace-to-semantic-anchor-workflow-note.md`
- `topics/analytic-provenance-and-evidence-management.md`

## 5. The branch’s practical routing rule
When a case is clearly runtime-evidence shaped, ask these in order:

1. **Do I still not know what to observe or at what layer?**
   - if yes, start with broad runtime-behavior recovery framing
2. **Do I already know the interesting behavior, but reruns are too fragile or expensive?**
   - if yes, start with replay / execution-history stabilization
3. **Is one suspicious late effect already visible and revisitable enough?**
   - if yes, start with reverse-causality localization

If more than one feels true, prefer the earliest bottleneck that still blocks later work.
That usually means:
- solve observation-surface choice before arguing about reverse causality
- solve capture stability before assuming the visible effect can be revisited reliably
- solve the first causal boundary before broadening back into more generic trace collection

## 6. What this branch is strongest at
This branch is currently strongest at practical guidance for:
- deciding whether runtime evidence is the right next move at all
- distinguishing live-observation questions from execution-history questions
- turning one visible late effect into one causal-boundary question instead of a larger trace tour
- bridging runtime evidence into smaller next tasks in native, protocol, malware, and protected-runtime branches

That makes the branch good at cases where the main problem is not raw tooling availability, but choosing the most decision-relevant runtime-evidence move.

## 7. What this branch is still weaker at
This branch is still weaker than browser/mobile in some areas:
- it has fewer concrete child notes than the denser practical branches
- hook-placement and observation-surface selection still live mostly inside broader synthesis rather than in a dedicated workflow note
- runtime-evidence externalization and provenance linkage are still more adjacent than fully laddered inside this subtree
- there is still room for a later branch pass focused specifically on hook-placement / observability workflow or runtime-evidence packaging

That means the right near-term maintenance pattern is usually:
- branch-shape repair
- conservative navigation strengthening
- new practical leaves only when a real operator gap appears

## 8. Common mistakes this guide prevents
This guide is meant to prevent several recurring branch-level mistakes:
- collecting more trace before deciding what uncertainty the runtime work is supposed to collapse
- treating record/replay like a generic debugger feature instead of a stability decision
- widening into full execution-history browsing when one narrow causal boundary would already shrink the task
- forcing runtime-evidence work to stay abstract even after one late effect is already visible
- drifting back into browser/mobile growth simply because those branches have denser source pressure

## 9. How this guide connects to the rest of the KB
Use this subtree when the case is best described as:
- uncertainty about what runtime evidence would matter most
- uncertainty about whether execution should be captured for stable revisits
- uncertainty about the first causal boundary behind a visible late effect

Then route outward as soon as the case becomes more specific:
- to `topics/mobile-protected-runtime-subtree-guide.md` when platform/runtime resistance on mobile becomes the real branch entry problem
- to `topics/browser-runtime-subtree-guide.md` when the decisive observation surfaces are browser/runtime and token/session/widget shaped
- to `topics/firmware-and-protocol-context-recovery.md` when the issue is mainly protocol or environment-context recovery
- to `topics/native-practical-subtree-guide.md` when the runtime question has already reduced into a quieter native semantic or route-to-consequence problem
- to `topics/analytic-provenance-and-evidence-management.md` when the main remaining bottleneck is preserving, packaging, or handing off the evidence cleanly

## 10. Topic summary
This subtree guide turns the runtime-evidence branch into a clearer operator ladder.

The compact reading is:
- choose the right observation surface
- place one smaller hook family at the right truth boundary
- stabilize execution history when live evidence is too fragile
- walk backward from one visible late effect to one causal boundary

That makes the branch easier to enter, easier to sequence, and less dependent on already knowing whether the right next move is more observation, more replay, or narrower reverse-causality proof.
arrower reverse-causality proof.
makes the branch easier to enter, easier to sequence, and less dependent on already knowing whether the right next move is more observation, more replay, or narrower reverse-causality proof.
ttleneck is preserving, packaging, or handing off the evidence cleanly

## 10. Topic summary
This subtree guide turns the runtime-evidence branch into a clearer operator ladder.

The compact reading is:
- choose the right observation surface
- stabilize execution history when live evidence is too fragile
- walk backward from one visible late effect to one causal boundary

That makes the branch easier to enter, easier to sequence, and less dependent on already knowing whether the right next move is more observation, more replay, or narrower reverse-causality proof.
easier to enter, easier to sequence, and less dependent on already knowing whether the right next move is more observation, more replay, or narrower reverse-causality proof.
