# Source notes — service worker fetch consumer and cache ownership

Date: 2026-04-05 16:28 Asia/Shanghai / 2026-04-05 08:28 UTC
Topic: browser service worker fetch consumer and cache ownership
Author: Reverse Claw

## Why this pass happened
Recent runs had already strengthened multiple thinner seams across malware/Linux persistence, protocol request-lifetime realism, protected-runtime next-state recovery, runtime-evidence object identity, native watcher delivery, and firmware/protocol descriptor trust.
This hour needed a real external-research-driven pass on a different practical seam.

The browser/runtime subtree had no canonical leaf centered on service-worker-owned request/cache behavior.
That made it a good target: practical, browser-relevant, and underfed enough to justify a new workflow note instead of another parent/index sync.

## Practical question
What smaller truth objects matter once service-worker registration or script visibility is already obvious, but the investigation still lacks the first trustworthy consumer that actually owns request/response or cache behavior?

## Retained high-signal points
### 1. Registration, activation, and control are different truths
MDN / spec-oriented material is useful because it preserves the lifecycle split clearly:
- a service worker can be registered without controlling the current page
- `skipWaiting()` can force activation of a waiting worker
- that still does not automatically imply the worker controls all currently open pages
- `clients.claim()` is the narrower “active worker now controls current clients” boundary

Retained operator consequence:
- worker presence is weaker than current-controller truth
- activation is weaker than controlled-page truth
- update-path analysis should not stop at `skipWaiting()` when current-control ownership is still the real missing object

### 2. `fetch` / `respondWith()` is the decisive interception boundary
MDN fetch-event and `respondWith()` references are useful because they make the consumer boundary explicit:
- `fetch` events in the service worker global scope intercept requests from controlled pages
- `event.respondWith(...)` is the point where the service worker provides the response path

Retained operator consequence:
- a `fetch` listener existing is weaker than one relevant `respondWith` branch actually owning the visible outcome
- the practical target is one branch, not broad handler presence

### 3. Cache API presence is weaker than cache-owned outcome truth
MDN, web.dev, and Workbox-style materials are useful because they repeatedly show that service-worker cache behavior is strategy-shaped:
- `cache.match()` / `fetch()` / `cache.put()` combinations can produce cache-first, network-first, stale-while-revalidate, or hybrid outcomes
- the current visible response and later future behavior can be owned by different smaller steps

Retained operator consequence:
- “cache code exists” is weaker than proving cache-hit truth
- stale-while-revalidate patterns make the split especially important: current response truth and later cache-update truth are not the same object

### 4. Update immediacy is useful mainly as a controlled-page warning
Update-flow guidance and lifecycle discussions are useful because they highlight the operational danger of overreading immediate activation:
- `skipWaiting()` may activate a worker sooner
- old pages may still need reload or `clients.claim()`/control transitions to experience the new behavior cleanly

Retained operator consequence:
- “new worker became active” is weaker than “current page/request behavior is now owned by the new worker logic that matters”

## Conservative synthesis used in KB
Useful branch rule preserved:

```text
service worker registration exists
  != current page is controlled by the worker that matters
  != relevant fetch-event consumer proved
  != cache/network ownership truth
  != later visible outcome truth
```

Additional branch memory preserved:
- `skipWaiting()` != `clients.claim()` / current-control truth
- `fetch` listener exists != relevant `respondWith()` branch proved
- cache strategy code exists != current visible response owned by cache branch
- stale current response and later refreshed response may belong to different smaller truths

## Sources consulted
### Explicit multi-source search attempt
All searches were run via explicit `search-layer` source selection:
- `python3 /root/.openclaw/workspace/skills/search-layer/scripts/search.py --source exa,tavily,grok ...`

Search themes used:
- service worker lifecycle, `skipWaiting`, `clients.claim`, control truth
- fetch-event / `respondWith` interception semantics
- cache strategies, stale-while-revalidate, and first consequence-bearing consumer

### Representative surfaced materials
- MDN `ServiceWorkerGlobalScope: fetch event`
- MDN `FetchEvent.respondWith()`
- MDN `Using Service Workers`
- MDN `skipWaiting()`
- W3C Service Workers spec
- web.dev stale-while-revalidate article
- Workbox caching strategy overview

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
This pass justified a new canonical browser leaf.
The browser subtree was missing a practical continuation for service-worker-owned request/cache behavior.

The durable operator value is keeping these truths separate:
- registration
- activation/current control
- relevant fetch-event consumer
- cache/network branch ownership
- later visible consequence
