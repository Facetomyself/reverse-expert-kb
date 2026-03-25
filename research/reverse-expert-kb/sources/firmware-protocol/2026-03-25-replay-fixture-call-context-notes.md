# Replay Fixture Call-Context Notes

Date: 2026-03-25
Branch: protocol / firmware practical subtree
Seam: method-contract -> minimal replay-fixture, with explicit separation between message/body truth and call-context truth

## Why this note exists
The protocol/firmware branch already preserved strong practical guidance for:
- service-contract extraction
- schema externalization
- minimal replay fixtures
- replay-precondition / acceptance gating

But the minimal-fixture branch still risked one practical flattening error:
- treating a truthful serialized body or argument bundle as the whole replay object
- when some families also carry decisive **per-call semantics outside the body**

That gap is small but operationally expensive.
It shows up when analysts say things like:
- “the protobuf body matches, so replay should be equivalent”
- “the opnum and arguments look right, so the RPC call is reproduced”

…while the original live call also depended on one narrower call-context contract.

## Narrow rule worth preserving
For some method/call families, the representative replay object is not just:
- route identity
- body / arguments
- likely gate-bearing fields inside the payload

It also includes **call-context truth**.

That means preserving the per-call semantics that may live outside the serialized body but still materially change whether the call is comparable.

## Source-backed cues retained conservatively
### gRPC-side cues
From gRPC metadata/deadlines documentation:
- metadata is a side channel associated with an RPC and is carried via HTTP/2 headers/trailers rather than the serialized message body
- metadata commonly carries authentication credentials, tracing information, and other call-associated control information
- deadlines are part of the call contract; by default gRPC does not set one, and a deadline can cause client-side `DEADLINE_EXCEEDED` or server-side cancellation behavior even when the request body itself is unchanged
- server-side and downstream-call behavior can depend on deadline propagation/cancellation posture, not only on payload content

Conservative workflow consequence:
- the same method path and protobuf body can still be a **different practical replay object** when deadline posture, metadata/header set, authority routing, or attached credentials differ

### Windows RPC-side cues
From Microsoft RPC binding/auth docs:
- binding handles and context handles are first-class parts of the RPC model, not incidental transport trivia
- strict/type-strict context handle guidance exists specifically because context-handle validity and interface ownership matter operationally
- authentication level/service and principal info are queryable on the binding/call context, meaning call semantics can depend on more than opnum plus arguments

Conservative workflow consequence:
- the same interface/opnum/argument bundle can still be a **different practical replay object** when binding family, endpoint, authn posture, or context-handle state differs

## Practical stop rule
When one representative method-bearing contract is already externalized and replay still fails, do not immediately widen back out into broad payload/schema doubt if:
- the body/arguments already look stable enough
- but per-call semantics outside the body are still under-frozen

Instead ask:
1. what is the route/body identity we already trust?
2. what call-context semantics were present in the live call?
3. which of those semantics are plausibly decisive rather than decorative?
4. has the fixture package frozen them explicitly, or only hand-waved them as ambient state?

## Good examples of call-context truth to preserve
### gRPC-like
- deadline / timeout posture
- request metadata / header set
- authority / host-routing assumption
- credential or auth-token attachment outside the body
- call lifecycle posture relevant to cancel / timeout / late completion

### Windows RPC-like
- binding handle family / endpoint assumption
- authn level / auth service posture
- context-handle validity / ownership posture
- interface/binding assumptions that make one opnum call comparable to the live case

## Not the same as later acceptance gating
This note is intentionally narrower than replay-precondition / acceptance-gate work.

Difference:
- **call-context truth** = what must be frozen so the representative replay object is honestly comparable to the original call
- **acceptance-gate truth** = the later local precondition that decides accepted/rejected/deferred behavior once the call is already comparable enough

If the fixture still lies about the call itself, it is too early to overinterpret later accept/reject behavior.

## Sources consulted
- gRPC Metadata guide — https://grpc.io/docs/guides/metadata/
- gRPC Deadlines guide — https://grpc.io/docs/guides/deadlines/
- Microsoft Learn: Binding and Handles — https://learn.microsoft.com/en-us/windows/win32/rpc/binding-and-handles
- Microsoft Learn: Using Binding Handles and Making RPC Calls — https://learn.microsoft.com/en-us/windows/win32/rpc/using-binding-handles-and-making-rpc-calls
- Microsoft Learn: RpcBindingInqAuthClientEx — https://learn.microsoft.com/en-us/windows/win32/api/rpcdce/nf-rpcdce-rpcbindinginqauthclientex

## Search-source note
This note was produced from an explicit `search-layer --source exa,tavily,grok` attempt.
The run should record exact source success/failure in the run report’s Search audit section.
