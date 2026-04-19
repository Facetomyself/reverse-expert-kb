# Windows RPC registration / endpoint-publication / reachability notes
Date: 2026-04-20
Branch: protocol / service-contract realism
Status: retained synthesis notes for external-research-driven maintenance

## Why this batch exists
The protocol branch already preserved the stop rule:
- described != registered != reachable

What still looked under-backed in the canonical note was the concrete Windows RPC version of that seam.
In practice, analysts often flatten together:
- static interface UUIDs or MIDL-generated structures
- `RpcServerRegisterIf*` runtime registration
- `RpcServerUseProtseq*` or `RpcServerInqBindings` listen/binding truth
- `RpcEpRegister` endpoint-mapper publication
- client-side `RpcStringBindingCompose` / `RpcBindingFromStringBinding` success
- actual current reachability of the specific server/path that matters

This batch was chosen to make that ladder more explicit and more source-backed instead of creating a new broad RPC taxonomy page.

## Search posture for this run
Search was attempted via the search-layer skill with explicit requested sources:
- Exa
- Tavily
- Grok

Result quality this run:
- Exa: succeeded
- Tavily: succeeded
- Grok: invoked but returned repeated `502 Bad Gateway` errors

Saved search trace:
- `sources/protocol/2026-04-20-0450-rpc-registration-reachability-search-layer.txt`

## Retained practical support

### 1. Interface description is weaker than runtime registration
URLs:
- https://learn.microsoft.com/en-us/windows/win32/rpc/registering-interfaces
- https://learn.microsoft.com/en-us/windows/win32/api/rpcdce/nf-rpcdce-rpcserverregisterifex

Retained points:
- servers register interfaces by calling `RpcServerRegisterIf`, `RpcServerRegisterIfEx`, or `RpcServerRegisterIf2`
- those calls populate the internal interface registry table used to map interface/object UUIDs to manager EPVs
- `RpcServerRegisterIfEx` registers an interface with the RPC run time; registration can also include auto-listen behavior and per-interface security callback behavior

Operator value:
- seeing a MIDL-generated `IfSpec`, UUID, stub, or RpcView-style roster is still weaker than proving the server actually called `RpcServerRegisterIf*` in the runtime/configuration that matters
- once `RpcServerRegisterIfEx` is visible, the next question is still not automatically solved: which transport bindings, endpoint publication state, and client reachability posture correspond to that registration?

### 2. Transport/endpoint listening is weaker than endpoint-map publication or universal reachability
URLs:
- https://learn.microsoft.com/en-us/windows/win32/api/rpcdce/nf-rpcdce-rpcserveruseprotseqep
- https://learn.microsoft.com/en-us/windows/win32/api/rpcdce/nf-rpcdce-rpcserverinqbindings

Retained points:
- `RpcServerUseProtseqEp` tells the RPC run time to use a protocol sequence plus endpoint for receiving RPC requests
- a successful `RpcServerUseProtseqEp` return does not guarantee endpoints on all network interfaces; the docs explicitly point to selective binding / DHCP timing caveats and say the full list of binding handles should be obtained via `RpcServerInqBindings`
- `RpcServerInqBindings` returns the binding handles over which remote procedure calls can be received

Operator value:
- `RpcServerRegisterIf*` truth is not the same as transport-listen truth
- even transport-listen truth is not the same as “every path I care about is reachable right now”
- `RpcServerInqBindings` is the smaller truth surface when one protocol-sequence registration or one static endpoint string still feels too abstract

### 3. Endpoint-mapper publication is its own proof object
URLs:
- https://learn.microsoft.com/en-us/windows/win32/rpc/registering-endpoints
- https://learn.microsoft.com/en-us/windows/win32/api/rpcdce/nf-rpcdce-rpcepregister
- https://learn.microsoft.com/en-us/windows/win32/api/rpcdce/nf-rpcdce-rpcmgmtepeltinqbegin

Retained points:
- `RpcEpRegister` adds to or replaces server-address information in the local endpoint-map database
- the endpoint-map entry logically contains interface UUID/version, binding handle, optional object UUID, and optional annotation
- `RpcMgmtEpEltInqBegin` creates an inquiry context for viewing server-address information stored in the endpoint map, with explicit match modes by interface, object UUID, or both

Operator value:
- a server can be runtime-registered yet still require separate proof that its bindings were published into the endpoint map
- endpoint-map enumeration is publication/discovery truth, not automatically same-process dispatch truth or same-client success truth
- this gives a practical middle rung between “registration exists” and “my client can really call it now”

### 4. Interface inquiry and endpoint-map inquiry do not prove the same thing
URLs:
- https://learn.microsoft.com/en-us/windows/win32/api/rpcdce/nf-rpcdce-rpcmgmtinqifids
- https://learn.microsoft.com/en-us/windows/win32/rpc/finding-endpoints
- https://learn.microsoft.com/en-us/windows/win32/api/rpcdce/nf-rpcdce-rpcmgmtepeltinqbegin

Retained points:
- `RpcMgmtInqIfIds` returns the identifiers of the interfaces offered by the server
- the docs explicitly say the server must be listening for remote procedure calls for `RpcMgmtInqIfIds` to succeed
- `Finding Endpoints` explains that clients can use `RpcMgmtInqIfIds`, `RpcMgmtEpEltInqBegin`, and related calls to determine whether a server has registered the interface it needs in the endpoint map
- `Finding Endpoints` also distinguishes well-known endpoints, dynamic endpoints, partially bound handles, and explicit endpoint-map searches

Operator value:
- interface roster truth and endpoint-map publication truth are related, but not interchangeable
- when one roster-enumeration tool or endpoint-mapper view already exists, keep asking which specific rung it proves: offered interface IDs, published endpoint-map entries, or actual later call reachability

### 5. Client-side binding-object construction is weaker than server availability or live reachability
URLs:
- https://learn.microsoft.com/en-us/windows/win32/api/rpcdce/nf-rpcdce-rpcstringbindingcompose
- https://learn.microsoft.com/en-us/windows/win32/api/rpcdce/nf-rpcdce-rpcbindingfromstringbinding
- https://learn.microsoft.com/en-us/windows/win32/rpc/finding-endpoints

Retained points:
- `RpcStringBindingCompose` only constructs a string representation of a binding handle
- `RpcBindingFromStringBinding` converts a string binding into a binding handle; if the string lacks an endpoint, the result is only a partially bound binding handle
- the docs explicitly say creation of a string binding by this method does not involve contact with the server and success/failure of the API will not indicate server availability
- `Finding Endpoints` says partially bound binding handles are the preferred path for dynamic endpoints, with endpoint resolution happening later

Operator value:
- successful binding-object construction is not the same proof object as “the intended server is up and listening on the path that matters”
- this gives a clean practical warning for RE cases where a client helper or replay harness can build a perfectly valid binding handle yet still says little about current endpoint-map truth, server listening truth, auth posture, or opnum comparability

## Cross-source synthesis
A durable workflow ladder from this batch is:

```text
recovered interface / stub / UUID
  != RpcServerRegisterIf* runtime registration
  != RpcServerUseProtseq* or RpcServerInqBindings transport-listen truth
  != RpcEpRegister endpoint-map publication
  != RpcStringBindingCompose / RpcBindingFromStringBinding binding-object construction
  != same server/path currently reachable for the client that matters
  != meaningful method dispatch or later consequence truth
```

A second compact split worth preserving is:

```text
endpoint-map entry visible
  != same process is listening the way you think
  != same client can bind comparably
  != same opnum will dispatch comparably
```

A third compact split worth preserving is:

```text
binding handle created
  != server contacted
  != endpoint resolved the way you think
  != server available
```

Useful cross-source reminders to preserve:
- interface description is weaker than runtime registration
- runtime registration is weaker than actual listening bindings
- listening bindings are weaker than endpoint-mapper publication
- endpoint-mapper publication is weaker than client reachability on the intended path
- client-side binding-object construction is weaker than server availability

## What this batch does *not* justify
Do not overclaim from this source set.
It does **not** prove that every endpoint-map entry corresponds to the exact server/process/path your current client run will use.
It also does **not** replace the narrower auth/context-lineage continuation for Windows RPC:
- security callback or secure-only posture can still reject the client even after interface registration and listening exist
- context-handle lineage and binding auth-info can still decide comparability after registration/publication questions are solved

The narrower justified claim is:
- the canonical protocol service-contract note should preserve a sharper Windows RPC ladder where description, registration, binding/listen truth, endpoint publication, binding-object construction, and live reachability are different proof objects.

## KB maintenance conclusion from this batch
This batch justified:
- materially extending `topics/protocol-service-contract-extraction-and-method-dispatch-workflow-note.md`
- sharpening the protocol subtree guide and top-level index so the Windows RPC seam does not collapse back to a shorter `described != registered != reachable` slogan
- keeping the narrower auth/context-lineage continuation separate rather than pretending this batch solved all later Windows RPC comparability questions
