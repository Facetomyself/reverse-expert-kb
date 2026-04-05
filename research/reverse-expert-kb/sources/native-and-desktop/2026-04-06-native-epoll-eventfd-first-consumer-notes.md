# Source notes — native epoll / eventfd first consumer ownership

Date: 2026-04-06 03:33 Asia/Shanghai / 2026-04-05 19:33 UTC
Topic: native epoll / eventfd first consumer ownership
Author: Reverse Claw

## Why this pass happened
Recent runs had alternated properly between external and internal maintenance while strengthening Android IPC and firmware/protocol USB ownership.
This hour needed a fresh external-research-driven pass on another thinner practical branch.

The native subtree already had good coverage for broad callback/event-loop work, IOCP/threadpool, waits, timers, APCs, GUI pumps, and inotify/fanotify.
It lacked a Linux-specific workflow note centered on **`epoll` / `eventfd` readiness and first loop-owned consumer ownership**.
That made it a good target: practical, bounded, and distinct from both Windows-heavy async leaves and broader callback-plumbing notes.

## Practical question
What smaller truth objects matter once `epoll`/`eventfd` plumbing is already obvious, but the investigation still lacks the first trustworthy loop-owned consumer that actually owns the later behavior?

## Retained high-signal points
### 1. Registration and readiness are different truths
man7 `epoll(7)` / `epoll_wait(2)` / `epoll_ctl(2)` material is useful because it preserves:
- registration / watch-set truth
- returned readiness truth
- follow-on delivery/handling obligations

Retained operator consequence:
- visible `epoll_ctl(...)` registration is weaker than relevant readiness truth
- returned readiness is weaker than the first loop-owned consumer that actually interprets it

### 2. Readiness and delivery/re-arm are different truths
`epoll(7)` guidance around edge-triggered usage, drain-to-`EAGAIN`, and one-shot behavior is useful because it preserves a smaller operational split:
- ready-list visibility
- delivery/re-arm/drain reality
- later handler consequence

Retained operator consequence:
- do not collapse one returned event into solved callback/consumer ownership
- `EPOLLONESHOT`, edge-triggered drains, and wakeup-fd clear/read behavior can still be the narrower missing proof object

### 3. eventfd wakeup truth is weaker than first pending-work consumer truth
`eventfd(2)` plus libuv/libevent/libev wakeup references are useful because they preserve:
- wakeup object creation / use
- loop wakeup readability
- later callback or pending-work reducer that actually gives the wakeup meaning

Retained operator consequence:
- visible wakeup writes or readable wakeup fd are weaker than the first loop-owned consumer that turns that wakeup into later behavior

### 4. Loop-framework use is weaker than loop-owned consumer proof
libuv/libevent/libev documentation and practical references are useful because they preserve that loop wakeup and loop callback phases are not the same proof object.

Retained operator consequence:
- “this target uses epoll/libuv/libevent” is weaker than “this dispatcher/handler/callback first owned the behavior that matters”

## Conservative synthesis used in KB
Useful branch rule preserved:

```text
registered
  != ready / woken
  != delivered / re-armed truth
  != first loop-owned consumer proved
  != later visible consequence truth
```

Additional branch memory preserved:
- registration should stay separate from readiness
- readiness should stay separate from re-arm/drain truth
- wakeup-fd visibility should stay separate from first callback/pending-work consumer proof
- loop-framework identity should stay separate from later behavior ownership

## Sources consulted
### Explicit multi-source search attempt
All searches were run via explicit `search-layer` source selection:
- `python3 /root/.openclaw/workspace/skills/search-layer/scripts/search.py --source exa,tavily,grok ...`

Search themes used:
- Linux `epoll` / `eventfd` readiness and first-consumer semantics
- edge-triggered / one-shot / re-arm ownership
- libuv/libevent/libev loop wakeup and callback ownership

### Representative surfaced materials
- man7 `epoll(7)`
- man7 `epoll_wait(2)`
- man7 `epoll_ctl(2)`
- man7 `eventfd(2)`
- libuv event-loop docs
- libevent/libev wakeup-loop references
- practical discussions around edge-triggered / one-shot handling semantics

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
This pass justified a new canonical native workflow note.
The subtree was missing a Linux-specific continuation for `epoll` / `eventfd` readiness and first loop-owned consumer ownership.

The durable operator value is keeping these truths separate:
- registration
- readiness / wakeup
- delivery / re-arm
- first loop-owned consumer
- later visible consequence
