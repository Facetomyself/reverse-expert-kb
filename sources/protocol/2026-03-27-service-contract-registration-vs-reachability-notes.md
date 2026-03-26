# Service-contract registration vs reachability notes

Date: 2026-03-27
Branch: protocol / firmware practical workflows
Focus: service-contract extraction stop rules; registration truth vs descriptor/reflection visibility vs callable reachability

## Why this note exists
A recurring protocol-RPC failure mode is overreading whatever looks like a service roster:
- embedded descriptors
- generated reflection metadata
- reflection-exposed method lists
- interface UUIDs or dispatch tables seen statically

Those surfaces are still valuable, but they do **not** all prove the same thing.
For practical RE, the branch needs a sharper stop rule around what is merely describable versus what is actually registered, dispatchable, and reachable in the current runtime.

## Source-backed findings

### 1. gRPC reflection is optional and can describe exported APIs, not necessarily your currently proven callable surface
Source:
- https://grpc.io/docs/guides/reflection/

High-signal points:
- reflection is a protocol servers **can** use; it is **not** automatically enabled
- server authors must explicitly add the reflection service
- tooling like grpcurl depends on this visibility surface
- if reflection is not routed/exposed, tooling can fail even when the application RPC service exists

Why it matters for RE:
- reflection presence is a strong schema/service shortcut, but absence does **not** prove the service/method family is unimplemented
- conversely, reflection visibility is still a metadata/discovery surface and should not be overread as full proof that the analyst already froze the exact live registration/binding path they care about

### 2. Practitioner signal suggests reflection-visible descriptions can overstate current runtime registration truth
Source:
- https://github.com/grpc/grpc-go/issues/6152

Observed practitioner concern:
- a user reported that `grpcurl` + reflection appeared to list methods for service descriptors compiled into the binary even when the implementation might not have been registered to the concrete server instance

Why it matters for RE:
- this is exactly the practical trap the KB should warn about: **descriptor/reflection-visible != proven live registration on the target instance**
- reflection-backed rosters remain useful as candidate surfaces, but the analyst should still freeze one builder/register/server-install anchor before treating a method as the operative replay target

Confidence note:
- this issue is practitioner signal, not a formal language-agnostic proof
- use it as a conservative warning and workflow stop rule, not as a universal statement about all gRPC runtimes

### 3. Windows RPC documentation makes registration and dispatch ownership more explicit
Sources:
- https://learn.microsoft.com/en-us/windows/win32/rpc/registering-interfaces
- https://learn.microsoft.com/en-us/windows/win32/api/rpcdcep/ns-rpcdcep-rpc_dispatch_table

High-signal points:
- servers register interfaces with `RpcServerRegisterIf` / `RpcServerRegisterIfEx` / `RpcServerRegisterIf2`
- those calls populate internal runtime tables used to map interface/object UUIDs to manager EPVs
- manager EPVs are arrays of function pointers, one per interface procedure
- `RPC_DISPATCH_TABLE` is part of the private runtime/stub interface and encodes dispatch-count plus dispatch-function table

Why it matters for RE:
- Windows RPC gives a clean model for separating:
  - interface/descriptor identity
  - registration truth
  - dispatch-slot truth
  - later semantic consequence truth
- that supports a practical stop rule for protocol/service-contract work: once one interface UUID/dispatch shell plus one registration anchor is frozen, the analyst can move on without demanding perfect names for every procedure

## Practical synthesis for the KB
The protocol branch should preserve a three-way distinction:

1. **descriptor / reflection truth**
   - service or method names, types, file descriptors, generated metadata, interface descriptors
2. **registration / dispatch truth**
   - builder/register/install anchor, interface-registration call, EPV/dispatch-table ownership, bound endpoint path, callable slot roster
3. **reachability / consequence truth**
   - the representative method actually accepts traffic in the live runtime, reaches parser/handler logic, or produces a state/output consequence worth replaying

Useful shorthand:
- **described != registered != reachable**

## Workflow impact
Use this note to sharpen `protocol-service-contract-extraction-and-method-dispatch-workflow-note`:
- if the analyst already has descriptor/reflection metadata, do not stop there by default
- freeze one registration/binding/dispatch anchor that proves why the representative method belongs to the currently relevant callable shell
- only then hand off into schema externalization, minimal replay fixtures, parser consequence, or replay-gate work

## Search audit input
Requested sources via search-layer:
- exa
- tavily
- grok

Observed search-layer outcome for this run:
- exa: invoked but returned `402 Payment Required` errors during the run
- tavily: returned usable results
- grok: invoked but returned `502 Bad Gateway` errors during the run

Endpoint context observed on this host:
- Exa endpoint: `http://158.178.236.241:7860/search`
- Tavily endpoint: `http://proxy.zhangxuemin.work:9874/api`
- Grok endpoint: `http://proxy.zhangxuemin.work:8000/v1`

Interpretation:
- this run attempted the required multi-source pass
- effective research quality for this run was degraded to Tavily-backed retrieval plus direct page fetches for confirmation
