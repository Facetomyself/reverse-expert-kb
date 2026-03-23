# Source Notes — 2026-03-23 — opnum / timeout-lifecycle minimal replay continuation

## Source set
External sources consulted through explicit multi-source search (`exa,tavily,grok`):
- Trail of Bits — *Introducing RPC Investigator*
  - <https://blog.trailofbits.com/2023/01/17/rpc-investigator-microsoft-windows-remote-procedure-call/>
- Shelltrail — *ManageEngine ADAudit - Reverse engineering Windows RPC to find CVEs - part 2*
  - <https://shelltrail.com/research/manageengine-adaudit-reverse-engineering-windows-rpc-to-find-cve-2024-36036-and-cve-2024-36037-part2>
- Zero Day Initiative — *Down the Rabbit Hole - A Deep Dive into an attack on an RPC interface*
  - <https://www.thezdi.com/blog/2018/6/7/down-the-rabbit-hole-a-deep-dive-into-an-attack-on-an-rpc-interface>
- gRPC blog — *gRPC and Deadlines*
  - <https://grpc.io/blog/deadlines>

Search trace archived at:
- `sources/protocol-and-network-recovery/2026-03-23-protocol-minimal-replay-fixture-search-layer.txt`

Existing KB pages consulted for fit:
- `topics/protocol-method-contract-to-minimal-replay-fixture-workflow-note.md`
- `topics/protocol-service-contract-extraction-and-method-dispatch-workflow-note.md`
- `topics/protocol-replay-precondition-and-state-gate-workflow-note.md`
- `topics/protocol-pending-request-correlation-and-async-reply-workflow-note.md`

## Why this batch was chosen
Recent protocol / firmware work already covered:
- service-contract extraction
- schema externalization
- method-contract -> minimal replay fixture
- streaming / half-close and Windows RPC opnum-level call bundles

But there was still one practical gap in the protocol branch:
- once analysts freeze an opnum-level or method-level fixture, they still often misread timeout/cancel/late-reply behavior as argument-shape failure
- that is especially common in async RPC and completion-shaped request flows where the fixture package preserves payload shape but not lifecycle truth

This batch was chosen to sharpen that seam without widening back into broad RPC taxonomy.

## Strong recurring ideas

### 1. Windows RPC tooling is strongest when it narrows to one callable interface object
The Trail of Bits RPC Investigator material is useful because it reinforces a practical operator move:
- enumerate interfaces, procedures, and endpoint-bearing objects
- then pivot into one generated client / one callable procedure surface
- not just a broad inventory of interfaces

Durable rule:
- interface discovery becomes replay-useful only after it is reduced to one representative callable object
- for Windows RPC that usually means one interface/endpoint target plus one opnum-level call bundle

### 2. IDL / stub recovery is only halfway to a truthful replay object
The ZDI write-up is valuable because it keeps the workflow grounded in classic RPC reversing:
- reverse the interface definition
- recover the method stub
- trace input through the service
- construct one custom client path

Durable rule:
- stub/IDL recovery is a route to one replay-worthy call object, not the end state by itself
- the minimal fixture should preserve the stub-visible call contract and the few ambient obligations still needed to make that call meaningful

### 3. The first replay-worthy object for Windows RPC is usually opnum + arguments + ambient assumptions
The Shelltrail case study is especially useful because it shows the reduction clearly:
- identify the right RPC entry
- map argument shape against decompiled server code
- refine input from invalid string to JSON-shaped content
- preserve the hidden server-side prerequisite (`AgentUID`) separately from the basic call shape

Durable rule:
- a useful first Windows RPC replay fixture is usually:
  - interface/binding target
  - opnum identity
  - representative argument bundle
  - explicit statement of ambient assumptions such as auth, endpoint, context, or server-side IDs
- do not confuse "we can invoke the opnum" with "we have a truthful fixture"

### 4. Timeout and deadline posture can belong to fixture identity
The gRPC deadlines material contributed a cross-protocol practical rule:
- client and server make local, independent judgments about whether the RPC succeeded
- the server can finish work while the client still reports `DEADLINE_EXCEEDED`
- a timeout can therefore mean "lifecycle mismatch" rather than "wrong request shape"

Durable rule:
- for async or completion-shaped method families, a minimal replay fixture sometimes needs an explicit lifecycle statement:
  - expected deadline / timeout posture
  - whether cancellation is part of the observed path
  - whether success is immediate reply, deferred completion, or a late reply that may arrive after caller patience expires

### 5. Late-reply and stale-reply interpretation should stay separate from payload-shape interpretation
This batch reinforces a branch-balance point already emerging in the protocol notes:
- payload identity
- pending-request ownership
- timeout posture
- late/stale completion interpretation
are related, but they are not the same question

Durable rule:
- if a call appears structurally right but the observed difference is timeout, cancel, or late reply, preserve that as lifecycle evidence first
- only then decide whether the next page should be:
  - method-contract -> minimal replay fixture
  - pending-request correlation / async reply
  - replay precondition / state gate

## Concrete operator takeaways worth preserving

### A. Windows RPC representative call-bundle rule
For a replay-worthy Windows RPC fixture, preserve:
1. interface UUID / endpoint or binding target if known
2. opnum identity
3. one representative argument bundle
4. explicit ambient assumptions:
   - authn / authz posture
   - context handles
   - server-side IDs or registry-backed prerequisites
   - transport / endpoint assumptions

### B. Timeout-lifecycle rule
For async or completion-sensitive methods:
1. record whether the original path expected immediate reply, deferred completion, or eventual late reply
2. record deadline / timeout / cancellation posture if visible
3. hold that posture constant in the first compare pair
4. do not immediately reinterpret timeout as payload-shape failure

### C. Provenance rule for method fixtures
Fixture provenance should preserve not only layer, but also lifecycle role:
- request-only
- request/response
- request/completion-derived
- timeout-observed
- late-reply-observed

That keeps later replay debugging honest.

## Candidate KB implications
This batch most strongly supports small practical reinforcement inside:
- `topics/protocol-method-contract-to-minimal-replay-fixture-workflow-note.md`

Specifically:
- preserve the opnum-level call bundle framing
- add timeout/deadline/cancel posture as a sometimes-required part of fixture identity for async/completion-shaped methods
- keep the branch practical instead of widening into abstract RPC transport discussion

## Confidence / quality note
Confidence is:
- strong for the Windows RPC reduction from interface discovery to one opnum-level call bundle
- medium-to-strong for the timeout/deadline lifecycle rule because the gRPC source states the client/server success split clearly and it generalizes conservatively to other async RPC-shaped work
- intentionally conservative about framework-specific replay tooling details

That is enough for a workflow note update because the claim is not that all protocols share one timeout model.
The claim is narrower:
- some representative replay fixtures are incomplete unless they preserve the lifecycle boundary that decides whether a "failure" is really a payload mismatch, a timeout posture mismatch, or a late-completion interpretation problem.
