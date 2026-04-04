# 2026-04-04 Windows RPC binding auth-info / context lineage notes

Date: 2026-04-04 09:21 Asia/Shanghai / 2026-04-04 01:21 UTC
Theme: do not flatten opnum/arguments into the whole comparable call object when binding auth-info posture or context-handle lineage still decides behavior.

## Why this note was retained
The protocol branch already had a broader call-context truth continuation under minimal replay fixtures.
What was still missing was a narrower Windows RPC practical leaf that anchors the compare loop in concrete runtime objects a reverser can ask about:
- binding-handle auth info
- context-handle lineage

## Primary doc-backed anchors
### 1. RpcBindingSetAuthInfo
Source:
- Microsoft Learn — RpcBindingSetAuthInfo
  - https://learn.microsoft.com/en-us/windows/win32/api/rpcdce/nf-rpcdce-rpcbindingsetauthinfo

Retained points:
- sets a binding handle’s authentication and authorization information
- unless the client calls it, RPCs on that binding are not authenticated
- it must not be called on a binding while an RPC call on the same handle is in progress
- it takes a snapshot of credentials

Operator consequence:
- a visible call can still be non-comparable if one binding has auth configured and another does not
- handle posture matters apart from visible opnum/args

### 2. RpcBindingInqAuthInfo
Source:
- Microsoft Learn — RpcBindingInqAuthInfo
  - https://learn.microsoft.com/en-us/windows/win32/api/rpcdce/nf-rpcdce-rpcbindinginqauthinfo

Retained points:
- returns authentication and authorization information from a binding handle
- `RPC_BINDING_HAS_NO_AUTH` is a real return condition
- the runtime may upgrade the effective authentication level above the level originally requested

Operator consequence:
- “requested auth level matched” can still be weaker than “effective auth-info tuple matched”

### 3. Context handles
Source:
- Microsoft Learn — Context Handles
  - https://learn.microsoft.com/en-us/windows/win32/rpc/context-handles

Retained points:
- context handles let the server maintain per-client state across calls
- the client sees an opaque token, but the meaning is server-side
- copying visible token bytes is weaker than reproducing the right context lineage

Operator consequence:
- if a call depends on a live context handle, replay/compare cannot be reduced to scalar argument copying

## Search-layer trace
See:
- `sources/protocol/2026-04-04-0921-windows-rpc-authinfo-search-layer.txt`

Observed degraded mode:
- Exa: returned results
- Tavily: returned results
- Grok: invoked but returned empty set / proxy 502 errors surfaced by tool output
