# Protocol Windows RPC Binding Auth-Info and Context Lineage Workflow Note

Topic class: concrete workflow note
Ontology layers: protocol / firmware practical workflow, Windows RPC call comparability, binding auth-info truth, context-handle lineage truth
Maturity: practical
Related pages:
- topics/protocol-firmware-practical-subtree-guide.md
- topics/protocol-method-contract-to-minimal-replay-fixture-workflow-note.md
- topics/protocol-replay-precondition-and-state-gate-workflow-note.md
- topics/protocol-pending-request-generation-epoch-and-slot-reuse-workflow-note.md
Related source notes:
- sources/protocol/2026-04-04-windows-rpc-binding-authinfo-context-lineage-notes.md

## 1. Why this note exists
This note exists for the narrower Windows RPC case where:
- interface/opnum and argument bundle are already good enough to name
- a representative call is already visible or replayable enough to compare
- but one run still behaves differently because the *binding handle’s auth-info posture* or the *context-handle lineage* is different

The operator mistake this note tries to prevent is:

```text
same opnum + same visible arguments == same comparable RPC call
```

The smaller truthful ladder is:

```text
same opnum/arguments
  != same binding-handle auth-info truth
  != same authenticated call posture
  != same live context-handle lineage
  != same server-side comparability
```

## 2. When to use this note
Use this note when most of these are true:
- the family is already clearly Windows RPC-shaped
- one representative method/opnum is already isolated
- broad payload/argument semantics are no longer the cheapest explanation
- replay or compare pairs still diverge with auth failures, invalid handle behavior, wrong-path behavior, or inexplicable acceptance drift
- the likely missing edge is no longer “what is the message?” but “what made this a comparable call on this binding?”

Do **not** use this note when:
- the interface/opnum is still uncertain
- the message/argument bundle is still too speculative to compare honestly
- the real bottleneck is broader acceptance gating unrelated to binding/auth/context posture

## 3. Core claim
For Windows RPC-like families, one truthful call object can require more than opnum plus visible arguments.

Two narrower proof objects matter:
1. **binding auth-info truth** — what authn/authz/authentication-level posture is actually attached to the binding handle used for the call
2. **context-handle lineage truth** — whether the apparent handle/token passed by the client still names a live server-side context in the correct lineage

## 4. Conservative doc-backed anchors
From Microsoft Learn:
- `RpcBindingSetAuthInfo` sets a binding handle’s authentication and authorization information
- unless a client calls `RpcBindingSetAuthInfo`, remote procedure calls on that binding are not authenticated
- `RpcBindingInqAuthInfo` returns the authentication and authorization information associated with a binding handle
- the authentication level returned by `RpcBindingInqAuthInfo` may differ from the level originally requested because the runtime can upgrade to the next higher supported level
- context handles represent server-maintained context for a client; the client sees an opaque token, but the meaning is server-side and lineage-dependent

Operator consequence:
- comparing only opnum + scalar arguments can be weaker than comparing one full call object that also preserves binding auth-info posture and context lineage truth

## 5. Boundary objects to keep separate
### A. Method/opnum truth
You already know what call family you are studying.
Keep this frozen.

### B. Binding auth-info truth
Freeze, if possible:
- principal-name expectation
- authentication level
- authentication service
- authorization service
- whether the binding has auth at all

Useful anchors:
- `RpcBindingSetAuthInfo`
- `RpcBindingInqAuthInfo`

### C. Context-handle lineage truth
If the call uses a context handle, treat the visible token as weaker than the lineage.
Questions that matter:
- where was the context originally established?
- is the server-side state still live?
- is the token being reused across reconnect/epoch/session changes?

### D. Effect/comparability truth
Only after B and C are frozen should you overread accept/reject differences as payload truth.

## 6. Default workflow
### Step 1: Freeze one representative call pair
Pick one pair:
- a working call
- a failing or differently behaving call

Hold opnum and broad arguments constant as much as possible.

### Step 2: Ask whether the binding is even comparably authenticated
Cheap discriminants:
- was auth set on the binding at all?
- does `RpcBindingInqAuthInfo` show auth info on the working binding but not the failing one?
- did the runtime upgrade the requested authn level?

Practical stop rule:
- do not treat “same requested auth level” as the same as “same effective auth level” if the runtime upgraded it.

### Step 3: Freeze the binding auth-info tuple
For the representative call, record:
- principal-name expectation
- authn level
- authn service
- authz service
- whether credentials are bound to the handle

The goal is not exhaustive security modeling.
The goal is one compare-honest tuple.

### Step 4: Ask whether a context handle is part of the true call object
If the call depends on a context handle:
- do not reduce it to copied bytes
- treat it as an opaque reference to server-side state
- freeze the creation/open step that produced it, if possible

### Step 5: Build the smaller compare label
If body/opnum/arguments still match, prefer this narrower label:

```text
same opnum/args, different binding auth-info or context lineage
```

This is often better than reopening broad argument taxonomy.

## 7. Practical failure patterns this note prevents
- “same opnum, same args, so auth can’t be the reason”
- “I copied the context-handle value, so the call should be equivalent”
- “requested authn level matched, so effective call posture matched”
- “binding exists, therefore it is comparably authenticated”

## 8. Sources
See: `sources/protocol/2026-04-04-windows-rpc-binding-authinfo-context-lineage-notes.md`

Primary references:
- https://learn.microsoft.com/en-us/windows/win32/api/rpcdce/nf-rpcdce-rpcbindingsetauthinfo
- https://learn.microsoft.com/en-us/windows/win32/api/rpcdce/nf-rpcdce-rpcbindinginqauthinfo
- https://learn.microsoft.com/en-us/windows/win32/rpc/context-handles
