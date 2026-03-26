# Call-Context Truth for Minimal Replay Fixtures — 2026-03-26

Branch: protocol / firmware practical workflows
Focus: method-contract -> minimal replay-fixture continuation
Question: when one representative method/opnum contract is already externalized, what smaller replay object should be preserved before widening back out into schema doubt if the same body or argument bundle still behaves differently?

## Short answer
Do not flatten **body truth** and **call-context truth**.

For some RPC-shaped families, the smallest truthful replay object is not only:
- route / method / opnum identity
- serialized body or argument bundle

It also includes one narrower per-call context contract that lives outside the body, such as:
- gRPC metadata/header set
- deadline / timeout posture
- authority / host routing assumptions
- credential placement outside the serialized message
- Windows RPC binding-handle family
- authentication level / service assumptions
- context-handle lineage

Practical shorthand worth preserving:
- **same body != same call**
- or more narrowly:
- **body-identical != call-identical**

## Why this seam matters
A recurring operator failure appears after contract extraction already succeeded:
- service/method/opnum identity is known
- request body or argument bundle is already good enough to serialize
- replay still returns timeout, auth failure, wrong server path, invalid handle, or apparently unrelated behavior

At that point, analysts often reopen broad payload semantics too early.
The more truthful next question is often:
- did replay preserve the same call-context contract?

## Conservative source-backed anchors
### 1. gRPC metadata is outside the message body
Source:
- gRPC docs — Metadata
  - <https://grpc.io/docs/guides/metadata/>

Useful retained point:
- metadata is a side channel associated with an RPC
- it is implemented using HTTP/2 headers/trailers
- it commonly carries authentication credentials, tracing information, and custom headers
- headers are sent before the initial request data message

Operator consequence:
- if authentication, routing, tracing, or feature selection depends on metadata/header state, then the protobuf body alone is not the whole replay object

### 2. gRPC deadlines change call behavior without changing the body
Source:
- gRPC docs — Deadlines
  - <https://grpc.io/docs/guides/deadlines/>

Useful retained point:
- clients may set deadlines for calls
- clients can observe `DEADLINE_EXCEEDED`
- servers can cancel work when the deadline has passed
- deadline propagation can affect downstream calls and behavior

Operator consequence:
- two runs with the same body can still represent practically different calls if deadline/timeout posture differs
- deadline posture belongs in fixture identity for timeout- or async-shaped cases

### 3. Windows RPC calls are made through binding handles
Source:
- Microsoft Learn — Using Binding Handles and Making RPC Calls
  - <https://learn.microsoft.com/en-us/windows/win32/rpc/using-binding-handles-and-making-rpc-calls>

Useful retained point:
- RPC calls are made through binding-handle-backed call setup rather than through argument blobs alone
- call success/failure behavior can depend on that live binding context

Operator consequence:
- opnum + argument bundle is weaker than a replay object that also preserves the binding family / endpoint assumptions under which the call was made

### 4. Windows RPC context handles preserve server-side session/state lineage
Source:
- Microsoft Learn — Context Handles
  - <https://learn.microsoft.com/en-us/windows/win32/rpc/context-handles>

Useful retained point:
- servers may maintain per-client state across calls using context handles
- the client holds an opaque token naming server-maintained context
- the token is meaningful only within the valid context lineage

Operator consequence:
- if a call depends on a live context handle, replay cannot be reduced to scalar/string argument copying
- visible handle bytes are weaker than truthful handle lineage

## Practical stop rules to preserve
### gRPC-like families
If the protobuf body already looks stable, ask before reopening payload semantics:
- was the same metadata/header set preserved?
- was the same deadline/timeout posture preserved?
- was the same authority/host routing assumption preserved?
- did call credentials live outside the serialized body?

### Windows RPC-like families
If opnum and arguments already look stable, ask before widening argument taxonomy:
- was the same binding-handle family preserved?
- was the same endpoint/transport assumption preserved?
- was the same authn/authz posture preserved?
- did the call depend on a live context handle whose lineage was not reproduced?

## KB-facing synthesis
This is not a claim that every RPC family works the same way.
It is a practical branch-memory rule:
- once one representative method/opnum contract is already externalized,
- the next truthful replay reduction may be **call-context truth** rather than more body decoding.

The useful compare label is:
- **body-identical but call-context-different**

That label is often a better explanation than generic schema doubt when:
- the same body times out in one run but not another
- the same arguments reach a different server path
- the same opnum fails under one binding family but not another
- the same apparent handle bytes fail because lineage/context ownership changed

## Files this note should support
- `topics/protocol-method-contract-to-minimal-replay-fixture-workflow-note.md`
- `topics/protocol-firmware-practical-subtree-guide.md`
- `index.md`
- one run report for this autosync pass
