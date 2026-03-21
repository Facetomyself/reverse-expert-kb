# Source Notes — 2026-03-22 — Service-contract / dispatch recovery canonical sync for protocol branch

## Source set
Search mode and policy:
- explicit multi-source search via `search-layer` with `--source exa,tavily,grok`
- queries centered on RPC/service-contract extraction, protobuf schema recovery, and dispatch-table-oriented workflow selection

Primary retained sources reviewed this run:
- <https://www.ioactive.com/breaking-protocol-buffers-reverse-engineering-grpc-binaries/>
- <https://arkadiyt.com/2024/03/03/reverse-engineering-protobuf-definitiions-from-compiled-binaries/>
- <https://clearbluejar.github.io/posts/surveying-windows-rpc-discovery-tools/>
- <https://github.com/marin-m/pbtk>
- <https://github.com/mildsunrise/protobuf-inspector>

Existing KB materials consulted for fit:
- `topics/protocol-service-contract-extraction-and-method-dispatch-workflow-note.md`
- `topics/protocol-firmware-practical-subtree-guide.md`
- `topics/protocol-state-and-message-recovery.md`
- `topics/firmware-and-protocol-context-recovery.md`
- `index.md`

## Why this pass was needed
The KB already had a dedicated workflow note for service-contract extraction and method-dispatch recovery, plus a prior source note on the same family.

But the branch’s canonical memory was still uneven:
- the protocol parent pages did not consistently list or route to that note
- the branch-level compact ladders still over-compressed the path from layer peeling straight into schema externalization or consequence proof
- this created a practical maintenance risk where a real operator bottleneck existed in the KB, but was still easy to forget unless one already knew the exact leaf note name

So this run was not about inventing a new branch.
It was about validating that the service-contract / dispatch seam is source-backed enough to deserve canonical retention in the protocol branch’s parent-page memory.

## Strong recurring ideas revalidated this run

### 1. Service-shell recovery is often the first operationally useful object after layer peeling
The IOActive gRPC write-up again reinforces that once the outer framing is understood, the next useful pivot is often:
- `RegisterService`-like registration
- service constructors
- method-bearing vtables
- service implementation classes

This matters because it turns “protobuf-shaped traffic exists” into a callable, enumerable surface.

### 2. Schema recovery and method-surface recovery are adjacent, but not identical
Arkadiy Tetelman’s protobuf descriptor recovery write-up is strong support for extracting embedded descriptor material from binaries.
But it also clarifies an important boundary for the KB:
- descriptor extraction can recover message definitions
- it does not by itself tell the analyst which service shell or method slot is the right next operational target

That makes the service-contract / dispatch note a necessary bridge rather than redundant with schema externalization.

### 3. Runtime/server-root and dispatch-table pivots remain strong in RPC-shaped targets
The Windows RPC discovery survey remains useful because it shows stable interface and dispatch pivots even when high-level names are sparse:
- runtime server roots
- interface structures
- dispatch tables
- procedure rosters

This supports keeping dispatch-bearing objects as first-class contract-bearing artifacts in the protocol branch, not just as a Windows-specific curiosity.

### 4. Tooling is most useful when it ties schema to endpoint/method identity
PBTK and protobuf-inspector together reinforce a useful split:
- one tool family helps recover or inspect message structure
- the analyst still needs one endpoint, method, slot, or callable surface to make that structure operational for replay, editing, fuzzing, or trace targeting

This is exactly the seam the workflow note preserves.

## KB-facing synthesis
A more stable protocol/firmware branch memory should explicitly preserve this order:
1. choose the right boundary
2. peel one visible object into one smaller contract
3. if the family is service-oriented or RPC-shaped, recover one service shell or representative method-bearing contract
4. externalize that contract into one reusable schema or harness target when analyst-private understanding is now the blocker
5. then prove consequence, acceptance, output, or hardware-side edges

Without step 3, the branch risks collapsing two different analyst bottlenecks into one:
- “I can decode the payload”
- “I know which callable surface this payload belongs to”

Those are not the same proof.

## Concrete maintenance implication
The service-contract / dispatch seam should remain visible in:
- `topics/protocol-firmware-practical-subtree-guide.md`
- `topics/protocol-state-and-message-recovery.md`
- `topics/firmware-and-protocol-context-recovery.md`
- `index.md`

This is a branch-memory repair, but it is grounded in real external-source pressure rather than purely internal wording churn.

## Confidence / quality note
Confidence is high that this seam is worth canonical retention because multiple source families converge on the same practical lesson:
- recover one callable contract-bearing surface before overinvesting in detached schema polish or premature handler semantics

The run remains conservative about universality:
- not every protocol family exposes a clean dispatch table
- not every service shell is explicit in stripped or proprietary targets
- not every schema-first case requires a separate service-contract step

But when the target already looks RPC-like or service-oriented, the KB should remember this seam explicitly rather than rely on analyst memory.