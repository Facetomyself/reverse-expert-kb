# Inotify / fanotify record-shaping vs first consumer notes

Date: 2026-04-08
Branch target: native practical workflows / Linux watcher seam
Purpose: preserve a source-backed operator refinement for watcher-heavy cases where inotify/fanotify returns real records, but returned-record semantics are still weaker than the first event-owned consumer that predicts later behavior.

## Research intent
Strengthen the existing native inotify/fanotify workflow note with a sharper separation between:
- watch registration truth
- returned event-record truth
- record-shaping semantics (coalescing / rename-cookie pairing / overflow / permission framing)
- first event-owned consumer truth

## Search artifact
Raw multi-source search artifact:
- `sources/native/2026-04-08-1356-inotify-search-layer.txt`

Requested source set:
- `exa,tavily,grok`

Observed search-source reality for this run:
- Exa returned usable man7/Linux watcher surfaces
- Tavily returned usable man7/Linux watcher surfaces
- Grok was explicitly invoked and failed with repeated `502 Bad Gateway` through the configured proxy path

## Retained sources
1. man7 / Linux inotify documentation surfaces
   - event coalescing, rename-cookie pairing, queue overflow, returned-record semantics
2. man7 / Linux fanotify documentation surfaces
   - metadata records, permission events, response/allow-deny handling
3. Conservative kernel-list discussion surfaces retained only as support for operator framing

## High-signal retained findings

### 1. Returned inotify records may already be shaped by coalescing and pairing semantics
The Linux inotify documentation already preserves distinctions around:
- watch registration
- event occurrence
- returned record delivery
- coalescing of successive unread identical events
- rename-cookie pairing
- queue-overflow effects

Practical consequence:
- one returned record is weaker than full operation history
- returned-record truth is still weaker than the first event-owned consumer that matters

### 2. fanotify permission events are weaker than permission-decision ownership
The Linux fanotify documentation already separates:
- metadata arrival
- permission event type
- later response/allow-deny decision handling

Practical consequence:
- metadata arrival is weaker than proving which code actually owns the allow/deny decision
- do not stop at permission-event visibility when the later decision consumer is still the real question

### 3. Watcher APIs report from the boundary outward, not from the behavior-bearing consumer backward
Watcher APIs naturally expose boundary-side records first.

Practical consequence:
- the returned record is often a reduction boundary, not yet the first truthful owner of the later effect
- keep watcher setup, returned-record truth, and event-owned consumer truth separate

## Practical synthesis worth preserving canonically
A compact stop-rule ladder for this seam is:

```text
watch registration
  != returned event record
  != coalesced/paired/overflow-shaped or permission-shaped watcher surface
  != first event-owned consumer
```

This keeps four different successes separate:
1. **watch registration**
   - the watcher exists and is pointed at the relevant object family
2. **returned event record**
   - one watcher record was actually delivered
3. **record-shaping watcher surface**
   - coalescing, cookie pairing, overflow, or permission framing now constrains what the record means
4. **first event-owned consumer**
   - one parser/router/decision owner predicts later behavior

## Best KB use of this material
This material is best used to sharpen the existing native inotify/fanotify workflow note.
It should not become a broad filesystem-notification page.

The operator-facing value is:
- do not overclaim from watch registration alone
- do not overclaim from a returned event record alone
- keep record-shaping semantics visible as part of truth selection
- stop only when one first event-owned consumer is frozen

## Search reliability note
This was a degraded-source external pass, not a fully healthy tri-source result set.
It still counts as a real external-research attempt because `exa,tavily,grok` were explicitly requested and Grok was actually invoked; its failure is recorded clearly.
