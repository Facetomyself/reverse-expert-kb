# iOS XPC lifecycle / reconnection notes

Date: 2026-04-07 12:21 Asia/Shanghai / 2026-04-07 04:21 UTC
Mode: external-research-driven
Branch: iOS practical workflows -> XPC proxy / service-consumer lifecycle realism

## Why this branch
This run used the external slot on a thinner iOS service-handoff seam rather than returning to browser or malware work.

The practical question was not broad XPC taxonomy.
It was how to preserve a more operational split between:
- client-side connection/proxy truth
- listener acceptance / exported-object method entry truth
- interruption vs invalidation truth
- reconnection truth
- later same-service or later consumer consequence truth

That seam already existed in the KB as branch memory, but it was worth making more explicit and operator-facing.

## Search-layer observations
Explicit multi-source search was attempted with:
- `--source exa,tavily,grok`

Queries used:
1. `NSXPCConnection interruption invalidation resume reconnect exported object official docs`
2. `Apple NSXPCConnection interruption invalidation exported object official documentation`
3. `NSXPCListener interruption invalidation connection service consumer Apple docs`

Observed source behavior:
- Exa returned usable hits
- Tavily returned usable hits
- Grok was invoked on all queries but failed with repeated 502 errors through the configured proxy/completions endpoint

## Primary source anchors
### Apple: NSXPCConnection
URL:
- https://developer.apple.com/documentation/foundation/nsxpcconnection

Useful operator implications:
- connection establishment/proxy setup is distinct from exported-object method entry and distinct again from later successful consequence
- interruption and invalidation are worth separating as different lifecycle events
- a later healthy-looking proxy/connection is weaker than proving the same meaningful method path ran again

### Apple: NSXPCListener / NSXPCListenerDelegate
URLs:
- https://developer.apple.com/documentation/foundation/nsxpclistener
- https://developer.apple.com/documentation/foundation/nsxpclistenerdelegate

Useful operator implications:
- listener acceptance is its own proof object
- accepted connection truth is weaker than one exported-object method entry
- service-side consumer proof should not stop at listener/lifecycle infrastructure alone

## Practical synthesis to preserve canonically
Useful ladder:

```text
client connection/proxy exists
  != listener accepted connection
  != exported-object method entry
  != interruption/invalidation/reconnection truth for this path
  != later same-service consequence or later consumer truth
```

Specific operator-facing reminders:
- interruption is weaker than invalidation as an end-of-life boundary
- a reconnected proxy/connection is weaker than proving the same meaningful method path ran again
- listener acceptance is weaker than exported-object method entry
- method entry is still weaker than one later consequence that answers the analyst’s real question

## Why this mattered to the KB
The iOS branch already had a good XPC service-handoff continuation.
This run made the lifecycle split more operational so future iOS XPC work does not silently overread client proxy visibility, connection health, or reconnection as already-good same-request or same-service consequence truth.

## Candidate follow-ons
Possible later iOS continuations if needed:
- a narrower XPC reply/error/reconnect compare continuation when service method entry is already good enough but same-request completion truth still lies
- a parent-page sync only if the new lifecycle memory still feels too leaf-local
