# Source Notes — 2026-03-26 — call-context truth for minimal replay fixtures

## Source set
External sources consulted through explicit multi-source search (`exa,tavily,grok`):
- gRPC — *Metadata*
  - <https://grpc.io/docs/guides/metadata/>
- gRPC — *Deadlines*
  - <https://grpc.io/docs/guides/deadlines/>
- Microsoft Learn — *Using Binding Handles and Making RPC Calls*
  - <https://learn.microsoft.com/en-us/windows/win32/rpc/using-binding-handles-and-making-rpc-calls>
- Microsoft Learn — *Interface Development Using Context Handles*
  - <https://learn.microsoft.com/en-us/windows/win32/rpc/interface-development-using-context-handles>
- Microsoft Learn — *RpcBindingSetAuthInfo function*
  - <https://learn.microsoft.com/en-us/windows/win32/api/rpcdce/nf-rpcdce-rpcbindingsetauthinfo>
- IOActive — *Breaking Protocol (Buffers): Reverse Engineering gRPC Binaries*
  - <https://www.ioactive.com/breaking-protocol-buffers-reverse-engineering-grpc-binaries/>

Search trace archived at:
- `sources/protocol-and-network-recovery/2026-03-26-1216-call-context-minimal-replay-search-layer.txt`

Existing KB pages consulted for fit:
- `topics/protocol-method-contract-to-minimal-replay-fixture-workflow-note.md`
- `topics/protocol-schema-externalization-and-replay-harness-workflow-note.md`
- `topics/protocol-service-contract-extraction-and-method-dispatch-workflow-note.md`
- `topics/protocol-firmware-practical-subtree-guide.md`

## Why this batch was chosen
Recent protocol / firmware work had already preserved:
- service-contract extraction
- schema externalization
- representative method-fixture reduction
- Windows RPC binding/context comparability

What still felt under-retained was a thinner cross-family stop rule:
- analysts may already have the right body, opcode, method path, or argument bundle
- yet the replay object is still false because one decisive **call-context** contract was never frozen
- this often gets misread as broad schema doubt or generic replay-gate mystery instead of a smaller comparability failure

This batch was chosen to preserve that narrower stop rule in a source-backed way rather than opening another broad protocol taxonomy pass.

## Strong recurring ideas

### 1. The same body can still be a different practical call
The gRPC metadata and deadline documentation make one operator point explicit:
- metadata is a side channel attached to the RPC
- headers/trailers and related per-call context are not the same thing as the message body
- deadline posture changes whether the client is still willing to wait and whether the server-side path is cancelled or allowed to continue

Durable rule:
- if two runs serialize the same request body but differ in deadline, metadata, authority, or credential placement, treat that as a **different practical call-context** before reopening body semantics

### 2. Constructor truth is often earlier than transport truth
The IOActive material remains useful here because it keeps the analyst anchored on generated structure:
- service names
- methods
- stubs
- registration and constructor-adjacent boundaries

Durable rule:
- when a truthful stub/helper boundary exists, use it to preserve both body and call-context truth before jumping to raw transport recreation

### 3. Windows RPC call comparability depends on more than opnum plus arguments
The Microsoft binding, context-handle, and authentication material reinforces a practical split:
- binding handles are first-class call setup, not just noise
- auth configuration on the binding can materially change the call
- context handles have lineage and interface-validity assumptions

Durable rule:
- for Windows RPC-like replay, treat binding family / endpoint / auth posture / context-handle lineage as part of the representative call bundle when they materially affect comparability

### 4. Some replay misses are comparability misses, not acceptance-gate misses
This batch supports a narrower workflow distinction already present in the branch:
- method-contract truth
- call-context truth
- replay-gate truth
- pending-owner lifetime truth
are related but not interchangeable

Durable rule:
- if the same body or argument bundle still diverges before a stable like-for-like call has even been reproduced, fix comparability first instead of overclaiming a later acceptance-gate diagnosis

## Concrete operator takeaways worth preserving

### A. Body-identical but call-context-different compare rule
When a fixture looks structurally right, freeze a narrow compare pair:
1. same body / same opnum / same route core
2. one truthful live call-context
3. one altered or ambiently different call-context
4. later outcome difference (deadline, auth, route, timeout, cancellation, wrong server path, invalid context lineage)

That compare pair is often more valuable than reopening broad field semantics.

### B. gRPC call-context checklist
If the family is gRPC-like, preserve separately:
- route identity: `/{package}.{Service}/{Method}`
- request/response type pairing
- stream shape
- metadata/header set that materially changes the call
- deadline/timeout posture
- authority/host routing assumptions
- credential placement when it lives outside the body

### C. Windows RPC call-context checklist
If the family is Windows RPC-like, preserve separately:
- interface / binding target / endpoint family
- opnum identity
- representative argument bundle
- authn level / auth service / principal expectations when relevant
- context-handle lineage and interface-validity assumptions

### D. Constructor-boundary preference rule
Prefer preserving one of these before raw transport heroics:
- generated stub or helper call site
- builder or serializer entry that still preserves the call boundary
- Windows RPC `NdrClientCall*`-adjacent constructor path
- binding-handle configuration plus one representative invocation path

## Candidate KB implications
This batch most strongly supports strengthening:
- `topics/protocol-method-contract-to-minimal-replay-fixture-workflow-note.md`

Specifically:
- make the body-identical / call-context-different compare rule more explicit
- preserve that some replay failures are best understood first as comparability failures
- keep the branch practical by reducing the problem to one smaller representative fixture truth instead of broad schema re-doubt

## Confidence / quality note
Confidence is:
- strong for the claim that gRPC metadata/deadline posture and Windows RPC binding/auth/context posture can materially change replay comparability outside the body
- strong for the workflow consequence that these should be preserved as explicit fixture components when they matter
- medium for target-specific details because concrete implementations differ widely

That is enough for a workflow-note refinement because the retained claim is narrow and practical:
- some replay failures should first be read as **missing call-context truth** rather than as bad payload reconstruction.
