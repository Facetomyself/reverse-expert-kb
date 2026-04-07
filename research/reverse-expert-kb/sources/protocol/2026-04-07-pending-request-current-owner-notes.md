# Pending-request current-owner / late-completion notes

Date: 2026-04-07 14:21 Asia/Shanghai / 2026-04-07 06:21 UTC
Mode: external-research-driven
Branch: protocol practical workflows -> pending-request generation / epoch / slot-reuse realism

## Why this branch
This run used the external slot on a thinner protocol seam rather than returning to browser or malware work.

The practical question was not broad async protocol taxonomy.
It was how to preserve a more operational split between:
- visible request/key/tag/user_data correlation
- request still being the current live owner
- timeout/cancel/retire/epoch-shift truth
- late completion still belonging to the current path

That seam already existed in the KB as branch memory, but it was worth making more explicit and operator-facing.

## Search-layer observations
Explicit multi-source search was attempted with:
- `--source exa,tavily,grok`

Queries used:
1. `gRPC completion queue tag Next official docs outstanding call completion ownership`
2. `io_uring user_data completion stale reused request ownership official docs`
3. `late reply timeout cleanup outstanding request ownership async completion official docs`

Observed source behavior:
- Exa returned usable hits
- Tavily returned usable hits
- Grok was invoked on all queries but failed with repeated 502 errors through the configured proxy/completions endpoint

## Primary source anchors
### gRPC C++ async docs
URL:
- https://grpc.io/docs/languages/cpp/async/

Useful operator implications:
- completion-queue events/tags are not the same as a still-current logical request owner
- outstanding async operation lifetime and completion delivery need to be kept distinct from superficial tag matching

### io_uring docs / man page
URLs:
- https://man7.org/linux/man-pages/man7/io_uring.7.html
- https://docs.kernel.org/io_uring/io_uring.html (fetch path returned 404 through current route; non-blocking)

Useful operator implications:
- visible completion/user_data is weaker than proving the completion still belongs to the currently live request/context
- queue/completion visibility and current-owner realism are distinct proof objects, especially when timeout/cancel/reuse is in play

## Practical synthesis to preserve canonically
Useful ladder:

```text
visible correlation token matches
  != request is still the current live owner
  != timeout/cancel/retire/epoch shift left ownership unchanged
  != late completion still belongs to the same meaningful path
  != later consequence truth
```

Specific operator-facing reminders:
- tags / user_data / IDs are weaker than current-owner proof
- timeout/cancel cleanup is weaker than proving a later completion still belongs to the same live request
- epoch/generation/slot reuse realism matters even when outer correlation looks good
- completion visibility is still weaker than one later consequence that answers the analyst’s real question

## Why this mattered to the KB
The protocol branch already had a strong pending-request generation / slot-reuse note.
This run made the late-completion/current-owner split more operational so future async protocol work does not silently overread superficial token matches as already-good current-path truth.

## Candidate follow-ons
Possible later protocol continuations if needed:
- a narrower timeout/cancel cleanup continuation when current-owner realism is still the main liar after request correlation is already good enough
- a parent-page sync only if the new late-completion/current-owner memory still feels too leaf-local
