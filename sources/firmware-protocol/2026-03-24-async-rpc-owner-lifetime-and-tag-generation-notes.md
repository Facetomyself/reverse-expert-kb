# Async RPC owner lifetime and tag/generation realism notes
Date: 2026-03-24
Branch: protocol / firmware practical continuation
Status: retained synthesis notes for KB maintenance

## Why this note exists
The protocol/firmware branch already had two good practical leaves for this area:
- `topics/protocol-pending-request-correlation-and-async-reply-workflow-note.md`
- `topics/protocol-pending-request-generation-epoch-and-slot-reuse-workflow-note.md`

What this run needed was not another broad wording pass and not a brand-new overlapping leaf.
It needed a sharper external-research-backed maintenance pass that preserves one practical operator lesson more concretely:
- **queue-visible completion is not the same thing as live-request completion**
- broad correlation can already be right while the waiting side still ignores the event because the logical owner is stale, replaced, retired, or now attached to a different generation

This matters in cases that look like:
- gRPC async C++ / completion-queue style delivery
- Thrift or callback/future style RPC continuations
- request tables or pending-slot maps where timeout/cancel/reconnect retires the owner
- descriptor/ring systems where slot equality is weaker than phase/owner/generation equality

## External support consulted this run
Search was explicitly attempted via `search-layer` with `--source exa,tavily,grok`.
Observed source state:
- Exa: succeeded
- Tavily: succeeded
- Grok: attempted but failed with gateway-side 502 behavior

Useful fetched support:
- gRPC C++ async tutorial: async RPCs are completed through `CompletionQueue`; tags identify operation completions on the queue
- gRPC C++ `CompletionQueue` reference: `Next`/`AsyncNext` return the user-supplied tag and status, reinforcing that queue delivery preserves per-operation identity rather than only broad transport correctness
- gRPC internal `CompletionQueueTag` reference: `FinalizeResult` is the point where core-side completion becomes C++ API-observable tag/status, making it a useful conceptual boundary for “framework saw something” versus “user-observable completion happened”
- Apache Thrift features page: asynchronous invocations may execute in parallel/out of order, reinforcing that broad transport arrival does not by itself identify the logical request owner
- Apache Thrift `AsyncMethodCallback` interface page: callback-oriented completion surfaces provide a useful practical comparison family for owner-specific completion rather than broad reply arrival
- IOActive “Breaking Protocol (Buffers): Reverse Engineering gRPC Binaries”: useful practical context for treating gRPC RE as more than protobuf field recovery and for localizing the implementation and async ownership surfaces around real service logic

These sources are being used conservatively.
They do **not** justify a universal claim that all RPC frameworks behave identically.
They do justify a recurring operator lesson:
- the important proof target is often the smallest still-live per-request state carrier, not merely the broad queue/channel/family.

## Practical synthesis retained from this run
### 1. Broad queue correctness is a weak milestone
A completion reaching the right `CompletionQueue`, callback family, or reply-handling path does not yet prove that the current request will advance.
The real deciding surface can still be:
- current call-state object
- current pending entry
- current generation / epoch
- still-live callback/future owner
- still-current slot/tag storage rather than stale reused storage

### 2. Completion identity and lifetime need separate language
Useful operator split:
- **identity**: slot/tag/correlation/call object/value that names the event family
- **lifetime**: whether that identifier still names the currently live owner

This gives better working language than vague statements like:
- “the completion arrives but does nothing”
- “the response looks right but is ignored”

### 3. Good concrete compare pairs for this seam
Strong compare pairs include:
- same tag family before timeout vs after timeout cleanup
- same slot/index before reuse vs after reuse with a new generation
- same broad correlation field when callback/future owner is still live vs already retired
- same queue-delivered event when the original per-call object still exists vs when it has already been destroyed/replaced

### 4. gRPC-specific practical lesson worth preserving
The gRPC C++ references reinforce a good RE stop rule:
- do not stop after proving that the target uses a `CompletionQueue`
- do not stop after seeing that a tag appears on the queue
- keep going until the **current per-call state** that turns that delivery into user-visible completion is localized

This is exactly the kind of seam that can otherwise get flattened into generic “async response handling.”

### 5. Thrift/callback family gives a useful adjacent comparison
Thrift’s async/callback framing is useful here not because it is identical to gRPC internals, but because it reinforces the same workflow discipline:
- out-of-order async execution means broad arrival order is weak evidence
- callback/future/call-specific owner surfaces matter
- the first meaningful consumer is often the first owner-specific continuation, not the broad transport edge

### 6. Replay fixtures often fail on owner realism, not bytes
A recurring practical continuation from this run:
- request/reply bytes can already be “good enough” structurally
- the failure can still be that the replay lacks the right pending-owner state, timeout ordering, generation/phase value, or current callback/future owner

That means this seam remains a practical continuation of both:
- `protocol-method-contract-to-minimal-replay-fixture-workflow-note`
- `protocol-pending-request-generation-epoch-and-slot-reuse-workflow-note`

## KB maintenance conclusion from this run
The main KB improvement justified by this run is:
- strengthen source-backed support for the existing pending-owner / generation seam
- make parent-page routing remember this seam explicitly instead of leaving it mostly in leaf pages and subtree guide language
- preserve that the branch should not collapse async ownership into generic replay-gate or generic parser-success wording

## Best next continuation if future evidence pressure grows
If future runs gather stronger case material, a still-practical child page could be justified around:
- streaming RPC / long-lived async conversation ownership
- distinguishing per-message correctness from per-stream liveness and current-stream ownership

That would only be worthwhile if it stays concrete and case-driven rather than reopening generic RPC taxonomy.
