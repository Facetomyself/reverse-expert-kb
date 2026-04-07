# Qt signal-slot delivery notes

Date: 2026-04-07 18:21 Asia/Shanghai / 2026-04-07 10:21 UTC
Mode: external-research-driven
Branch: native practical workflows -> GUI message-pump / signal-slot first-consumer proof

## Why this branch
This run used the external slot on a thinner native GUI seam rather than returning to browser or malware work.

The practical question was not broad Qt GUI taxonomy.
It was how to preserve a more operational split between:
- signal/slot connection existence
- connection type / receiver-thread delivery rule
- actual queued/direct delivery in the run that matters
- the first behavior-changing consumer after delivery

That seam already existed in branch memory, but it was worth making more explicit and operator-facing.

## Search-layer observations
Explicit multi-source search was attempted with:
- `--source exa,tavily,grok`

Queries used:
1. `Qt signals slots queued connection direct connection thread affinity official docs`
2. `Qt connection types queued direct blockingqueued official documentation`
3. `Qt AutoConnection receiver thread affinity queued delivery official docs`

Observed source behavior:
- Exa returned usable hits
- Tavily returned usable hits
- Grok was invoked on all queries but failed or returned no usable results through the configured proxy/completions endpoint

## Primary source anchors
### Qt signals and slots docs
URL:
- https://doc.qt.io/qt-6/signalsandslots.html

Useful operator implications:
- signal emission and actual slot execution should not be flattened together
- queued delivery can defer the real consumer boundary relative to emission time
- connect-site visibility alone is weaker than a real delivery/consumer proof

### Qt ConnectionType docs
URL:
- https://doc.qt.io/qt-6/qt.html#ConnectionType-enum

Useful operator implications:
- `AutoConnection` depends on receiver thread affinity and may resolve differently than broad assumptions suggest
- direct vs queued vs blocking queued delivery are different proof objects
- delivery rule realism matters before narrating one slot as the first meaningful consumer

## Practical synthesis to preserve canonically
Useful ladder:

```text
signal/connection exists
  != connection type / thread-affinity delivery rule is what you think
  != queued or direct delivery actually happened in the run that matters
  != receiving slot was the first behavior-changing consumer
  != later GUI/state consequence truth
```

Specific operator-facing reminders:
- connect-site truth is weaker than delivery truth
- emitted signal truth is weaker than actual queued/direct delivery truth
- `AutoConnection` needs receiver-thread reality, not folklore
- delivery truth is still weaker than one first behavior-changing consumer and later GUI/state consequence

## Why this mattered to the KB
The native GUI branch already had the useful shorthand around `signal found != queued truth != first behavior-changing consumer`.
This run made that seam more operational so future Qt-heavy GUI work does not silently overread connect sites, emissions, or assumed delivery mode as already-good first-consumer proof.

## Candidate follow-ons
Possible later native GUI continuations if needed:
- a narrower note around event-filter vs signal-slot handoff truth when both are visible and the first behavior-changing consumer is still ambiguous
- a parent-page sync only if the new Qt delivery memory still feels too leaf-local
