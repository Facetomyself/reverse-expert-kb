# Browser Service Worker Fetch Consumer and Cache Ownership Workflow Note

Topic class: workflow note
Ontology layers: browser runtime, service worker lifecycle, fetch interception, cache/network ownership
Maturity: emerging
Related pages:
- topics/js-browser-runtime-reversing.md
- topics/browser-cdp-and-debugger-assisted-re.md
- topics/browser-environment-reconstruction.md
- topics/browser-fingerprint-and-state-dependent-token-generation.md
Related source notes:
- sources/browser/2026-04-05-service-worker-fetch-consumer-and-cache-ownership-notes.md

## 1. What this note is for
Use this note when a browser-side target already plausibly depends on a **service worker** for request interception, cache shaping, offline fallback, or token/state mediation, but the investigation still lacks the first trustworthy consumer boundary that turns visible registration or fetch visibility into real behavior ownership.

Typical situations:
- `navigator.serviceWorker.register(...)` is visible, but you still do not know whether the current page is controlled by the worker that matters
- a service worker script contains `fetch` handlers, cache logic, or token/header rewriting, but you still do not know which first branch actually owns the response/request outcome in the run that matters
- cache hits, network fallbacks, or stale-while-revalidate behavior are visible in DevTools, but the analysis still collapses lifecycle truth, controller truth, fetch-event truth, and consequence truth together

This note is for the narrower question:

```text
Which first service-worker-owned lifecycle or fetch-event consumer actually owns the browser-visible outcome?
```

Not the broader question:

```text
Does this target use a service worker at all?
```

## 2. When to use it
Use this note when most of the following are true:
- the broad browser-runtime problem has already narrowed specifically into service-worker registration, update, fetch interception, or cache ownership
- one service worker script, registration, or fetch handler is already visible
- the main uncertainty is whether **registration truth**, **active-controller truth**, **fetch-event consumer truth**, **cache/network branch truth**, or **later visible outcome truth** actually owns the claim you care about
- the next useful output is one smaller trustworthy chain such as:
  - registration -> active worker -> controlling page -> fetch event -> `respondWith` cache branch -> visible response
  - registration -> waiting worker -> `skipWaiting` / `clients.claim` transition -> first controlled request -> fetch handler -> token/header mutation -> visible request
  - active worker -> fetch event -> cache miss / network fallback -> `cache.put` / later reuse -> visible stale-vs-fresh behavior

Do **not** start here when:
- the real bottleneck is still broader browser environment reconstruction or debugger-visible value generation
- the target is mainly websocket/protocol framed-consumer work rather than service-worker interception
- service-worker visibility is already sufficient and the real missing edge is now protocol finalization, anti-bot token generation, or outer request acceptance

## 3. Core claim
A recurring browser-reversing mistake is to stop too early at one of these milestones:
- “the app registers a service worker”
- “the worker has a `fetch` listener”
- “DevTools shows a request came from service worker/cache”
- “the worker calls `cache.match()` or `fetch()` in the handler, therefore ownership is solved”

The smaller reusable target is:

```text
service worker registration exists
  != current page is controlled by the worker that matters
  != relevant fetch event reached the branch that matters
  != cache/network choice truth
  != later visible request/response consequence truth
```

## 4. Boundary objects to keep separate
### A. Registration truth
Visible objects:
- `navigator.serviceWorker.register(...)`
- service worker script URL / scope
- install / activate handlers

This is weaker than proof that the current run is actually controlled by the worker instance that matters.

### B. Active-controller truth
Useful questions:
- is the worker merely registered, or is it the current active controller for this page?
- is the worker still waiting?
- did `skipWaiting()` make it active?
- did `clients.claim()` actually move current pages under its control?

MDN / spec-oriented reminders:
- `skipWaiting()` can move a waiting worker to active
- that still does not automatically mean all current pages are immediately controlled
- `clients.claim()` is the narrower controlling-page boundary after activation

This matters because “worker active” is weaker than “worker currently owns the page/request path that matters.”

### C. Fetch-event consumer truth
The useful object is often not “a fetch listener exists” but one smaller branch in that handler:
- one URL/path predicate
- one method/mode/destination predicate
- one cache-first or network-first branch
- one token/header rewrite path
- one response-rewrite / redirect / fallback path

From MDN / service worker docs:
- the `fetch` event fires in the service worker global scope for network requests made by the controlled page
- `event.respondWith(...)` is the decisive interception boundary for supplying the response

This means “fetch event exists” is weaker than “this specific branch owned the result.”

### D. Cache/network ownership truth
Typical smaller truths:
- one `cache.match()` hit actually satisfied the request
- one network fallback actually produced the visible response
- one `cache.put()` or later cache update created the stale/fresh behavior seen later
- one stale-while-revalidate style path returned cached data first while a later background update changed future behavior

Do not flatten “cache APIs are present” into “the visible outcome was cache-owned.”

### E. Later visible outcome truth
This is where the analyst proves the service-worker-owned path actually matters:
- one page/request really ran under the active controller that matters
- one `fetch` event branch actually produced or mutated the visible request/response
- one later cached/not-cached/fallback/rewritten outcome depends on the service-worker path you froze

## 5. Practical stop rules this note preserves
- `worker registration exists != current page is controlled by that worker`
- `worker active != controlling current page/request path`
- `fetch listener exists != relevant fetch-event consumer proved`
- `cache API visible != cache branch owned the visible outcome`
- `network fallback visible != later cache update / reuse truth proved`
- `skipWaiting visible != clients.claim / current-control truth`
- `request seen in DevTools != first service-worker-owned consumer proved`

## 6. Default workflow
### Step 1: freeze one worker, one controlled scope, and one visible outcome
Do not widen into every worker or every request.
Pick one high-leverage chain:
- one request clearly marked as service-worker-influenced
- one stale-vs-fresh cache case
- one token/header rewrite case
- one update/claim transition case

### Step 2: separate registration from current-controller truth
Before explaining behavior, freeze:
- worker script and scope
- whether the worker is waiting, active, or controlling the page that matters
- whether `skipWaiting()` / `clients.claim()` actually changed current control

### Step 3: freeze one fetch-event branch
Pick the smallest branch that matters:
- one request URL/mode/destination gate
- one `respondWith(...)` path
- one `cache.match()` / `fetch()` / fallback branch
- one header/token mutation path

### Step 4: preserve cache/network choice truth
If the interesting behavior is cache-shaped, preserve:
- one cache-hit truth object
- one network-fallback truth object
- one stale-then-refresh or later `cache.put()` / update truth object

Do not overread “cache code exists” into “this response was cache-owned.”

### Step 5: prove one first service-worker-owned consumer
Among candidate proofs, prefer the one that best predicts visible behavior:
- controlling worker -> relevant fetch event -> `respondWith` cache hit -> visible response
- controlling worker -> relevant fetch event -> network fallback -> rewrite/mutation -> visible request/response
- waiting -> `skipWaiting` / `clients.claim` -> first controlled fetch -> visible change in request/response ownership

### Step 6: stop once one smaller trustworthy chain exists
Examples:
- registration -> active controller -> page controlled -> fetch branch -> cache hit -> visible response
- active worker -> fetch event -> network branch -> token/header mutation -> visible request
- waiting worker -> `skipWaiting` / `clients.claim` -> first controlled request -> changed response ownership

## 7. Practical scenarios
### Scenario A: worker clearly registered, but current page still uses old behavior
Wrong stop:
- “the new worker exists, so the new cache/request logic owns this page now”

Better stop:
- freeze whether the current page is actually controlled, and whether `skipWaiting()` / `clients.claim()` changed that yet

### Scenario B: `fetch` listener exists with cache logic
Wrong stop:
- “the worker handles fetch, so the visible response came from cache logic”

Better stop:
- prove one `respondWith` branch and whether the visible response came from cache hit, network fallback, or later update path

### Scenario C: stale-while-revalidate style behavior confuses ownership
Wrong stop:
- “the response is cached, therefore cache fully explains current and later behavior”

Better stop:
- preserve the split between current cached response, background refresh/update, and later future-request behavior

### Scenario D: service-worker update path seems to change anti-bot or token behavior
Wrong stop:
- “`skipWaiting()` is present, so the new token behavior already owns the current run”

Better stop:
- prove activation and current control (`clients.claim()` / controlled page) before narrating token/request changes as owned by the new worker

## 8. Why this note exists in the browser branch
The browser subtree is already strong on CDP/debugger workflows, risk-control/captcha families, environment reconstruction, and mixed-runtime analysis.
What it lacked was a thinner practical continuation for service-worker-owned request/cache behavior.

This note fills that gap and preserves the smaller ladder:
- registration
- active/current control
- fetch-event branch
- cache/network ownership
- later visible outcome

instead of collapsing everything into “a service worker exists.”

## 9. Sources
See:
- `sources/browser/2026-04-05-service-worker-fetch-consumer-and-cache-ownership-notes.md`

Primary anchors retained:
- MDN service worker lifecycle and fetch-event docs
- W3C service worker spec
- explicit `search-layer` multi-source attempt with `--source exa,tavily,grok`
- practical update/control and caching references (MDN / web.dev / Workbox-oriented material)
