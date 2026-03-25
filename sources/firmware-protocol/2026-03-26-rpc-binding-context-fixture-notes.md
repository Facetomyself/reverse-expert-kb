# Source Notes — 2026-03-26 — Windows RPC binding/context-handle replay-fixture continuation

## Source set
External sources consulted through explicit multi-source search (`exa,tavily,grok`):
- Microsoft Learn — *Strict and Type Strict Context Handles*
  - <https://learn.microsoft.com/en-us/windows/win32/rpc/strict-and-type-strict-context-handles>
- Microsoft Learn — *Using Binding Handles and Making RPC Calls*
  - <https://learn.microsoft.com/en-us/windows/win32/rpc/using-binding-handles-and-making-rpc-calls>
- Microsoft Learn — *RpcBindingFromStringBinding function*
  - <https://learn.microsoft.com/en-us/windows/win32/api/rpcdce/nf-rpcdce-rpcbindingfromstringbinding>
- Microsoft Learn — *NdrClientCall2 function*
  - <https://learn.microsoft.com/en-us/windows/win32/api/rpcndr/nf-rpcndr-ndrclientcall2>
- Shelltrail — *ManageEngine ADAudit - Reverse engineering Windows RPC to find CVEs - part 1 / RPC*
  - <https://shelltrail.com/research/manageengine-adaudit-reverse-engineering-windows-rpc-to-find-cve-2024-36036-and-cve-2024-36037-part1>
- SpecterOps — *Uncovering RPC Servers through Windows API Analysis*
  - <https://specterops.io/blog/2023/10/18/uncovering-rpc-servers-through-windows-api-analysis/>

Search trace archived at:
- `sources/firmware-protocol/2026-03-26-rpc-context-handle-fixture-search-layer.txt`

Existing KB pages consulted for fit:
- `topics/protocol-method-contract-to-minimal-replay-fixture-workflow-note.md`
- `topics/protocol-service-contract-extraction-and-method-dispatch-workflow-note.md`
- `topics/protocol-replay-precondition-and-state-gate-workflow-note.md`
- `topics/protocol-firmware-practical-subtree-guide.md`

## Why this batch was chosen
Recent protocol / firmware runs had already preserved:
- service-contract extraction
- schema externalization
- method-contract -> minimal replay fixture
- opnum-level fixture thinking
- generic call-context truth
- timeout / late-reply lifecycle realism

What still felt under-frozen was a thinner Windows RPC-specific seam:
- analysts can already know the interface, endpoint family, opnum, and apparent argument shape
- yet still fail to produce a truthful replay object because the live call also depended on one narrower binding/auth/context contract
- that failure often gets misfiled as “arguments still unclear” or “need more IDL recovery”

This batch was chosen to preserve a more practical stop rule for Windows RPC-like replay work without widening into broad RPC taxonomy.

## Strong recurring ideas

### 1. Binding handles are part of replay identity, not just setup noise
The Microsoft binding material is useful because it keeps one practical point explicit:
- `RpcBindingFromStringBinding` creates a binding handle from a string representation
- the result may still be partial, nil-object, local-host, or endpoint-bearing depending on the supplied string
- success of handle construction does not itself prove server availability or equivalence to the original call path

Durable rule:
- if replay depends on one narrower endpoint, object UUID, host, or transport family, freeze that as fixture identity rather than treating “some binding handle exists” as good enough

### 2. Context handles are not interchangeable ambient tokens
The strict/type-strict context-handle guidance is valuable because it states directly that:
- context handles are operationally associated with interface and sometimes type expectations
- cross-interface or mismatched context use is exactly the sort of mistake that can break or change behavior

Durable rule:
- if the live call used a context handle, the representative replay object is not just `opnum + arguments`; it also includes the context-handle lineage and interface-validity assumptions that made the call comparable in the first place

### 3. `NdrClientCall*`-adjacent recovery is useful because it preserves the smallest honest call bundle
The `NdrClientCall2` documentation is thin by itself, but together with field writeups it reinforces a practical analyst move:
- do not start from raw transport recreation when a stub/helper boundary already preserves stub descriptor, procedure format, and call-argument shape
- treat the marshalling stub or nearby invocation helper as the cheapest truthful constructor boundary for a first fixture

Durable rule:
- if a Windows RPC call site is already visible through generated/client helper code, prefer preserving one `NdrClientCall*`-adjacent constructor path over rebuilding the whole transport stack too early

### 4. Interface/opnum recovery is only halfway to a truthful replay object
The Shelltrail and SpecterOps material is useful because it reinforces the operator ladder:
- recover interface/service surface
- identify callable procedure or opnum-bearing path
- tie it to one client/helper/invocation boundary
- then narrow to one representative live call object

Durable rule:
- once one callable opnum is already plausible, the next useful output is usually not broader interface inventory
- it is one representative call bundle that freezes binding target, opnum, argument family, and any required auth/context assumptions separately

### 5. A replay miss can be a call-comparability miss before it is an acceptance-gate miss
This batch reinforces a practical split already present in the branch:
- method-contract truth
- call-context truth
- acceptance-gate truth
- pending-owner / late-reply truth
are related, but they are not the same question

Durable rule:
- if a replay fixture still lies about binding/auth/context posture, it is too early to overinterpret later accept/reject behavior as proof that the payload or IDL is wrong

## Concrete operator takeaways worth preserving

### A. Windows RPC representative call-bundle rule
For a replay-worthy Windows RPC fixture, preserve:
1. interface UUID / binding target / endpoint family if known
2. opnum identity
3. one representative argument bundle
4. one explicit call-context note covering only what is actually decisive:
   - binding-handle family / endpoint / object UUID assumptions
   - authn level / auth service / principal posture when relevant
   - context-handle lineage, validity, and interface ownership assumptions

### B. Windows RPC stop rule for context-handle cases
If the case includes a context handle, do not keep widening argument semantics first.
Instead ask:
1. where was the handle created?
2. under which interface/binding family was it valid?
3. is the replay fixture reusing the same handle lineage or inventing one?
4. is the replay failure better explained by invalid context posture than by wrong scalar/string arguments?

### C. Constructor-boundary rule
Prefer preserving one of these as the first replay constructor boundary:
- generated client/helper call site
- `NdrClientCall*`-adjacent wrapper
- binding-handle construction/configuration path plus one stub invocation path

Prefer these before:
- whole-interface inventory expansion
- hand-built packet recreation
- a giant generic client shell that drags hidden ambient state along

## Candidate KB implications
This batch most strongly supports a narrower reinforcement inside:
- `topics/protocol-method-contract-to-minimal-replay-fixture-workflow-note.md`

Specifically:
- strengthen the Windows/custom RPC scenario so it explicitly separates argument folklore from binding/auth/context comparability
- add a practical stop rule around context-handle lineage and interface-validity assumptions
- keep the branch practical by reducing Windows RPC replay to one smaller representative call bundle rather than widening back into generic interface recovery

## Confidence / quality note
Confidence is:
- strong for the claim that binding handles and context handles are first-class parts of Windows RPC call comparability
- medium-to-strong for the workflow consequence that a representative replay fixture should freeze those assumptions separately from the argument bundle
- medium for target-specific details such as exact authn service, object UUID use, or server-side context allocation behavior, because concrete RPC families vary widely

That is sufficient for a workflow-note refinement because the claim is narrow:
- some Windows RPC replay failures are best understood first as binding/context comparability failures, not as generic argument-shape uncertainty or later acceptance-gate failures.
