# 2026-03-25 — Native loader/import-resolution refinement notes

Topic focus: delay-load helper hooks, forwarded exports / API-set-style indirection, and why returned-address visibility is still weaker than first retained caller-side consumer proof

## Why this note exists
The native loader/provider branch already preserved the broad distinction between **resolution truth** and **consumer truth**.

This run only needed a thinner practical refinement, not a new sibling leaf:
- analysts can now already remember that delay-load helpers, forwarded exports, and repeated `GetProcAddress` calls are not the endpoint
- but a narrower fake-finish still remains common in Windows-heavy cases
- the fake-finish is: "the helper hook overrode DLL/proc choice" or "the returned address is outside the named image, so the real owner is now proved"

That is often still too early.

## Conservative source-backed reminders
### 1. Delay-load helper hooks can redirect resolution, but they still live on the resolution side of the split
Microsoft’s delay-load helper documentation is enough to preserve the practical point that notification hooks can intercept or override library/procedure selection around:
- `dliNotePreLoadLibrary`
- `dliNotePreGetProcAddress`
- failure-hook paths

Practical RE implication:
- proving that helper-hook logic redirected which DLL or proc got returned is stronger than proving only that the default helper exists
- but it still does not prove which caller-side feature path, provider, or later dispatch actually became behaviorally relevant

### 2. Returned-address locality can reduce implementation family without proving behavioral ownership
Forwarder-oriented material and `GetProcAddress` documentation are enough to preserve a conservative reminder:
- the returned address may resolve through forwarding or API-set-style indirection
- the first returned address may therefore land outside the originally named DLL or outside the image the analyst first expected

Practical RE implication:
- this is useful **implementation-family truth**
- but address locality alone is still weaker than one retained caller-side pointer/table/provider object or one later call site that reuses the resolved target in the behavior-bearing path

### 3. Delay-import metadata and helper reachability can still overstate liveness
The existing phantom-DLL practical cue still matters here.

Practical RE implication:
- visible delay-import metadata, helper frames, or redirect-capable hooks do not by themselves prove the path is live in the current run
- keep the gate/live-path proof separate from the later first-consumer proof

## Practical operator rule preserved this run
Use this thinner stop rule in Windows-heavy loader/import cases:

```text
helper / forwarder / API-set resolution becomes visible
  -> maybe even hook override or surprising returned address is proved
  -> treat that as stronger resolution-family truth, not yet ownership truth
  -> prove one retained caller-side pointer/table/provider object or one later dispatch/call site
  -> only then treat the resolved edge as behaviorally relevant to the target question
```

## Concrete scenario shapes worth preserving
### A. `dliNotePreGetProcAddress` clearly overrides the returned proc
- do not stop at the helper frame
- prove which host-side slot, provider object, or later caller actually keeps and reuses that proc

### B. `GetProcAddress` returns an address outside the originally named image
- treat this as a useful reduction in implementation family
- do not overread it as automatic ownership proof
- prove one caller-side retained use or later dispatch edge that makes the resolved implementation matter

### C. Delay-import path is present and hookable, but feature behavior is still conditional
- prove the gate that makes the delayed path live in the current run
- then prove one retained caller-side consumer

## Likely KB consequence
The native loader/provider branch should preserve one extra practical reminder:
- **override truth** and **address-locality truth** are both stronger than "helper exists"
- but both are still weaker than one proved caller-side retained consumer
- therefore they should stay on the resolution side of the branch split until one later retained/reused consumer edge is actually grounded
