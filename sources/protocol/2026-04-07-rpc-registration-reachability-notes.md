# Windows RPC registration / reachability notes

Date: 2026-04-07 08:21 Asia/Shanghai / 2026-04-07 00:21 UTC
Mode: external-research-driven
Branch: protocol practical workflows -> service-contract extraction / registration / reachability

## Why this branch
This run used the external slot on a thinner protocol seam instead of returning to browser or malware work.

The practical question was not broad RPC taxonomy.
It was how to preserve a more operational split between:
- interface/service contract description
- server-side interface registration
- endpoint publication
- actual client reachability/binding truth

That seam already existed in the KB as branch memory, but it was worth making more explicit and operator-facing.

## Search-layer observations
Explicit multi-source search was attempted with:
- `--source exa,tavily,grok`

Queries used:
1. `Windows RPC endpoint mapper interface registration binding reachability official docs RpcServerRegisterIf RpcEpRegister`
2. `RPC interface registration endpoint mapper reachability official docs Windows`
3. `described registered reachable RPC endpoint mapper binding official docs`

Observed source behavior:
- Exa returned usable hits
- Tavily returned usable hits
- Grok was invoked on all queries but failed with repeated 502 errors through the configured proxy/completions endpoint

## Primary source anchors
### Microsoft Learn: RpcServerRegisterIf
URL:
- https://learn.microsoft.com/en-us/windows/win32/api/rpcdce/nf-rpcdce-rpcserverregisterif

Useful operator implications:
- interface registration is a server-side act distinct from endpoint publication and distinct again from later client binding success
- seeing interface-spec material or generated stubs is weaker than proving runtime server registration

### Microsoft Learn: RpcEpRegister
URL:
- https://learn.microsoft.com/en-us/windows/win32/api/rpcdce/nf-rpcdce-rpcepregister

Useful operator implications:
- endpoint registration/publishing is its own proof object
- server registration alone is weaker than endpoint-mapper-visible reachability
- published endpoint visibility is still weaker than a successful client binding/dispatch path in the run that matters

### Endpoint mapper docs
Attempted:
- `https://learn.microsoft.com/en-us/windows/win32/rpc/the-endpoint-mapper`

Result:
- fetch path returned 404 through the current fetch route
- non-blocking; the two API docs already grounded the practical split conservatively

## Practical synthesis to preserve canonically
Useful ladder:

```text
interface described
  != server registered
  != endpoint published
  != client reachable/bindable
  != meaningful method dispatch or later consequence
```

Specific operator-facing reminders:
- IDL/stub/proxy visibility is weaker than runtime server registration truth
- `RpcServerRegisterIf`-class registration is weaker than endpoint-mapper publication truth
- endpoint publication is weaker than actual client reachability in the run that matters
- successful reachability/binding is still weaker than one dispatched method or later consequence that answers the analyst’s real question

## Why this mattered to the KB
The protocol branch already had the useful branch-memory shorthand `described != registered != reachable`.
This run made that split more operational for Windows RPC-shaped work so future service-contract and replay work does not silently overread stubs, registration, or endpoint visibility as already-good client reality.

## Candidate follow-ons
Possible later protocol continuations if needed:
- a narrower note around client binding-handle posture vs call-context truth when registration/reachability is already good enough but replay still lies
- a parent-page sync only if the new RPC registration/reachability memory still feels too leaf-local
