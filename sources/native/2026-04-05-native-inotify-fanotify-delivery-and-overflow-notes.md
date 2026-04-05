# Source notes — native inotify/fanotify delivery, pairing, and overflow realism

Date: 2026-04-05 12:27 Asia/Shanghai / 2026-04-05 04:27 UTC
Topic: native inotify/fanotify first event consumer realism
Author: Reverse Claw

## Why this pass happened
Recent autosync runs had already strengthened malware/Linux persistence, protocol request-lifetime realism, protected-runtime next-state recovery, and runtime-evidence object-identity stop rules.
This hour needed a real external-research-driven pass on a different practical seam.

The existing Linux-native filesystem-watch note was the right target:
- it already existed canonically
- it was practical and underfed relative to heavier branches
- it still benefited from sharper source-backed reminders about event delivery semantics rather than only registration or broad event-loop ownership

## Practical question
What delivery-side details matter most when deciding whether one inotify/fanotify event has really reached the first consequence-bearing consumer?

## Retained high-signal points
### 1. Inotify returned records are not always a one-to-one underlying operation history
From `inotify(7)` and supporting search results:
- successive identical unread events may be coalesced into a single returned record
- the queue is ordered
- rename-related `IN_MOVED_FROM` / `IN_MOVED_TO` records are connected by a shared cookie

Retained operator consequence:
- one returned record is weaker than one full underlying operation history
- if rename handling matters, preserve cookie-paired consumer logic rather than stopping at one lone move-related record
- adapter/library bug reports around rename association and nonadjacent associated events are useful reminders that consumer truth can live above raw event receipt

### 2. Overflow is not merely observability noise
From `inotify(7)`:
- event queues can overflow and emit `IN_Q_OVERFLOW`

Retained operator consequence:
- overflow may be part of the behavior story, not just a logging nuisance
- if the target explicitly handles overflow, rebuilds caches, or degrades behavior after overflow, that handling path may itself be the first consequence-bearing consumer worth proving

### 3. Fanotify permission cases have a distinct consumer boundary
From `fanotify(7)` and related references:
- permission events are requests to userspace to decide whether access is granted
- fanotify object identity and payload shape can vary depending on report flags (`FD`, `FID`, `DIR_FID`, `NAME`, etc.)

Retained operator consequence:
- metadata arrival is weaker than the first allow/deny response path
- object identity may not always be one simple path string, so the first useful consumer can sit at the permission-response or identity-resolution boundary instead of at raw event receipt

### 4. Library and adapter issues are useful, but mainly as delivery-shaping reminders
Search results surfaced watcher library issues around:
- rename association not being adjacent in the read buffer
- duplicate creation reporting
- path association/reporting fixes

Retained operator consequence:
- these are useful because they show how easily analysts can overread raw event visibility
- they should be treated as delivery-shaping reminders, not as kernel-manpage replacements
- the KB should preserve the stop rule that the first trustworthy consumer may be parser/association logic above raw FD reads

## Conservative synthesis used in KB
Useful branch rule preserved:

```text
watch registration
  != relevant event occurred
  != returned event record fully explains history
  != first event-owned consumer proved
```

Additional branch memory preserved:
- coalescing can compress visible inotify history
- rename cookies matter when pairing move semantics
- overflow can be behavior-bearing
- fanotify permission flows have a stricter first-consumer boundary at the allow/deny response path

## Sources consulted
### Normative/local
- local `man 7 inotify`
- local `man 7 fanotify`

### Explicit multi-source search attempt
All searches were run via explicit `search-layer` source selection:
- `python3 /root/.openclaw/workspace/skills/search-layer/scripts/search.py --source exa,tavily,grok ...`

Search themes used:
- inotify coalescing, rename cookies, overflow, first consumer semantics
- fanotify permission events, report flags, overflow, and first listener/decision semantics

### Representative surfaced materials
- `inotify(7)` references via man7.org / Debian manpages
- `fanotify(7)` / `fanotify_init(2)` / `fanotify_mark(2)` references via man7.org / Debian manpages
- watcher/adapter issue material around inotify rename association and delivery quirks
- Red Hat support writeup illustrating blocking permission-event response behavior in fanotify

## Search audit material for run report
Requested sources:
- Exa
- Tavily
- Grok

Observed outcome across this source pass:
- Exa: succeeded with usable hits on both queries
- Tavily: succeeded with usable hits on both queries
- Grok: invoked and failed with HTTP 502 Bad Gateway on both queries

Endpoints / execution paths used:
- Exa endpoint: via `python3 /root/.openclaw/workspace/skills/search-layer/scripts/search.py --source exa,tavily,grok`
- Tavily endpoint: via `python3 /root/.openclaw/workspace/skills/search-layer/scripts/search.py --source exa,tavily,grok`
- Grok endpoint: via `python3 /root/.openclaw/workspace/skills/search-layer/scripts/search.py --source exa,tavily,grok`

## What this changed in KB terms
This pass did not justify a new Linux watcher sibling page.
The correct move was to strengthen the existing inotify/fanotify first-event-consumer note with sharper delivery-side realism:
- inotify coalescing
- rename cookie pairing
- queue overflow
- fanotify permission-response boundary

The durable operator value is keeping registration, record receipt, event-history interpretation, and first consumer truth separate.
