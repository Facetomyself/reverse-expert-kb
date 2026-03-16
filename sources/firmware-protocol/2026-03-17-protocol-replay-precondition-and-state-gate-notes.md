# Source Notes — Protocol replay precondition and state-gate workflow

Date: 2026-03-17
Purpose: support a practical protocol workflow note for the recurring case where message families, parsers, and even some field roles are already visible, but replay, mutation, or stateful experimentation still fails because the first hidden session precondition, transition gate, or capability-state reduction has not yet been localized.

## Scope
This note does not try to survey protocol state machines in the abstract.
It consolidates practical signal already present in the KB into one operator-facing workflow frame for a common bottleneck:

- one message family is already isolated
- parser or dispatch visibility already exists
- some field or opcode semantics are already plausible
- yet replay, mutation, or fuzzing still fails inconsistently
- the real missing edge is often not more field labeling, but the first local state gate such as:
  - a phase/epoch/session enum check
  - a capability/authentication bit reduction
  - a sequence/window/counter acceptance gate
  - a pending-request / nonce / token ownership check
  - a handshake-complete or mode-ready transition test

## Supporting source signals

### 1. Existing protocol-state synthesis already separates message recovery from state recovery
From:
- `topics/protocol-state-and-message-recovery.md`

High-signal points reused here:
- protocol understanding is incomplete without interaction-structure reasoning
- field visibility and state visibility are distinct analyst milestones
- downstream value depends on whether the recovered model supports replay, fuzzing, generation, and explanation

Why it matters:
- a protocol case can look structurally well understood while still failing operationally because one hidden state precondition remains unproved

### 2. Existing parser-to-state workflow logic already separates parse visibility from consequence visibility
From:
- `topics/protocol-parser-to-state-edge-localization-workflow-note.md`

High-signal points reused here:
- parser visibility is not the same as behavior-changing consequence visibility
- one representative compare pair is better than wider but shallower trace collection
- the first reduction from parsed material into a smaller local action bucket is usually more valuable than more broad field labeling

Why it matters:
- some protocol cases do not stall at parser-to-state localization anymore; they stall one step later, where the analyst already suspects the parser and even one state edge, but still does not know which specific precondition makes replay succeed, reject, degrade, or silently no-op

### 3. Existing runtime-evidence material reinforces compare-run and proof-of-effect discipline
From:
- `topics/runtime-behavior-recovery.md`
- `topics/record-replay-and-omniscient-debugging.md`
- `topics/causal-write-and-reverse-causality-localization-workflow-note.md`

High-signal points reused here:
- the useful move is often to localize one causally predictive edge rather than narrating the whole subsystem
- runtime evidence should collapse the cheapest uncertainty that changes the next decision
- selective compare pairs beat indiscriminate logging

Why it matters:
- replay-precondition cases are exactly the kind of uncertainty that should be collapsed through one narrow compare pair and one proved downstream acceptance/rejection difference

### 4. Existing mobile/browser challenge-loop notes show a transferable pattern: token visibility is not the same as consumer acceptance
From:
- `topics/mobile-challenge-and-verification-loop-analysis.md`
- `topics/post-validation-state-refresh-and-delayed-consequence-workflow-note.md`
- `topics/browser-request-finalization-backtrace-workflow-note.md`

High-signal points reused here:
- visible tokens or parsed values are often one layer too early
- the decisive edge is often the first local consumer or policy reduction that turns visible material into accepted behavior
- compare-run diagnosis is most useful when anchored on acceptance/rejection or advance/stall boundaries

Why it matters:
- protocol replay failures often have the same shape even outside browser/mobile targets: visible message structure exists, but the first local acceptance gate still hides behind state normalization, mode checks, freshness checks, or pending-request ownership

## Distilled practical pattern
A useful workflow pattern for protocol replay / mutation failures is:

```text
message family visible
  -> parser / dispatch / field roles partly visible
  -> replay or mutation still fails
  -> one local state/precondition gate decides accept / reject / degrade / no-op
  -> one later reply, transition, or state advance proves that gate mattered
```

## Operator heuristics to preserve
- Do not assume a correct parser or plausible field labels mean the case is ready for replay or fuzzing.
- Treat these as separate milestones:
  - message-family visibility
  - parse visibility
  - consequence visibility
  - acceptance/precondition gate visibility
  - downstream proof-of-advance or proof-of-rejection
- Prefer one narrow compare pair such as:
  - accepted vs rejected replay of the same message family
  - same message shape before vs after one handshake step
  - same opcode with one counter/token/session field changed
  - same mutation under two local mode/state settings
- Useful local gate anchors include:
  - first branch that checks session phase / mode / epoch
  - first reduction from parsed fields into a smaller capability or permission bucket
  - first nonce/sequence/window/pending-request ownership check
  - first helper that maps parsed message + current state into reject / retry / challenge / queue / accept
  - first state advance or reply-serialization path that only exists on accepted runs
- If multiple parsed fields differ but only one later acceptance branch correlates with behavior, prefer the acceptance branch as the proof target rather than fully solving every field meaning first.
- If replay seems structurally correct but still stalls silently, suspect hidden state freshness, ownership, pending-request, or phase alignment before assuming deeper parser incompleteness.

## Candidate canonical KB mapping
This note most directly supports:
- `topics/protocol-replay-precondition-and-state-gate-workflow-note.md`

It also strengthens:
- `topics/protocol-state-and-message-recovery.md`
- `topics/protocol-parser-to-state-edge-localization-workflow-note.md`
- `topics/runtime-behavior-recovery.md`

## Bottom line
Some protocol cases do not really unblock when the analyst finds the parser or even the first parser-to-state consequence edge.
They unblock when the analyst proves which local session/state precondition actually decides whether replay, mutation, or stateful interaction is accepted, rejected, degraded, retried, or silently ignored.