# Source notes — Android Binder / ContentProvider first consumer ownership

Date: 2026-04-05 22:29 Asia/Shanghai / 2026-04-05 14:29 UTC
Topic: Android Binder / ContentProvider first consumer ownership
Author: Reverse Claw

## Why this pass happened
Recent runs had already strengthened multiple thinner branches across browser service workers, mobile/WebView bridges, native/runtime evidence, firmware/protocol trust, and iOS URL-loading interception.
This hour needed a real external-research-driven pass on another underfed seam.

The Android/mobile subtree referenced Binder/provider families, but it lacked a canonical workflow note centered on **first consumer ownership** across Binder and `ContentProvider` IPC.
That made it a good target: practical, Android-specific, and distinct enough from WebView and network ownership notes to justify a new workflow page.

## Practical question
What smaller truth objects matter once Binder/provider presence is already obvious, but the investigation still lacks the first trustworthy consumer that actually owns the IPC consequence?

## Retained high-signal points
### 1. Presence and current call are different truths
Android docs and AIDL/Binder references are useful because they preserve the distinction between:
- interface/provider registration or metadata
- current client call via proxy or `ContentResolver`
- actual server/provider-side consumer

Retained operator consequence:
- visible AIDL/Stub/Proxy or provider authority is weaker than the current client path that uses it
- client-side proxy or resolver visibility is weaker than server/provider consumer truth

### 2. Selection/marshaling is often the narrower missing reducer
Binder/AIDL and provider docs are useful because they highlight explicit selectors:
- transact codes / `onTransact(...)`
- provider URI matching
- `call(method, arg, extras)` method/extras routing
- `Bundle` / Parcel fields that decide later handling

Retained operator consequence:
- one selector is often the right next reducer before broader downstream tracing
- “IPC happened” is weaker than “this exact route/selector owned the later behavior”

### 3. First consumer truth usually lives at `onTransact(...)`, implementation dispatch, or provider operation methods
Docs and practical Binder/provider material converge on the same operational rule:
- the first server/provider method that interprets the transaction is the useful proof object
- not just the existence of a Proxy/Stub or authority

Retained operator consequence:
- `onTransact(...)` / first implementation method / provider method should be frozen before widening into business logic
- this is the correct practical target for a reverser who already knows the family but not the owner

### 4. ContentProvider `call(...)` deserves equal status with CRUD paths
Provider docs are useful because they preserve a seam analysts often underweight:
- many apps carry important provider behavior through `call(...)`, method names, and extras rather than `query`/`insert`/`update`/`delete`

Retained operator consequence:
- do not overfit every provider case into CRUD-only mental models
- if the visible path is `call(...)`, method/extras routing can be the real first consumer selector

## Conservative synthesis used in KB
Useful branch rule preserved:

```text
interface/provider exists
  != current client call uses it
  != relevant transact / provider selection truth
  != first Binder/provider consumer proved
  != later visible consequence truth
```

Additional branch memory preserved:
- authority/URI/method/extras should be preserved as selection truth objects
- `call(...)` should be treated as a first-class provider seam
- proxy visibility and Binder traffic should not silently replace first server/provider consumer proof

## Sources consulted
### Explicit multi-source search attempt
All searches were run via explicit `search-layer` source selection:
- `python3 /root/.openclaw/workspace/skills/search-layer/scripts/search.py --source exa,tavily,grok ...`

Search themes used:
- `ContentProvider` and `ContentResolver` operation/call semantics
- Binder / AIDL `onTransact(...)`, Stub/Proxy, and first consumer ownership
- provider authority/method/extras routing

### Representative surfaced materials
- Android `ContentProvider` docs
- Android `ContentResolver` docs
- Android AIDL / Binder docs and references
- Binder / IPC practical references around `onTransact(...)`
- provider `call(...)` and authority routing discussions

## Search audit material for run report
Requested sources:
- Exa
- Tavily
- Grok

Observed outcome across this source pass:
- Exa: succeeded with usable hits on all three queries
- Tavily: succeeded with usable hits on all three queries
- Grok: invoked and failed with HTTP 502 Bad Gateway on all three queries

Endpoints / execution paths used:
- Exa endpoint: via `python3 /root/.openclaw/workspace/skills/search-layer/scripts/search.py --source exa,tavily,grok`
- Tavily endpoint: via `python3 /root/.openclaw/workspace/skills/search-layer/scripts/search.py --source exa,tavily,grok`
- Grok endpoint: via `python3 /root/.openclaw/workspace/skills/search-layer/scripts/search.py --source exa,tavily,grok`

## What this changed in KB terms
This pass justified a new canonical Android/mobile workflow note.
The subtree was missing a practical continuation for Binder / `ContentProvider` first-consumer ownership.

The durable operator value is keeping these truths separate:
- interface/provider presence
- current client call
- selection/marshaling
- first consumer
- later visible consequence
