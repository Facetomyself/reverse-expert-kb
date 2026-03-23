# Reverse KB Autosync Run Report — 2026-03-23 19:18 Asia/Shanghai

Mode: external-research-driven

## Summary
This run deliberately avoided another internal-only canonical sync. Recent autosync activity had already spent meaningful energy on branch wording, route memory, and canonical balance. To satisfy the anti-stagnation rule, this run performed a real external research pass on a thinner but still practical native branch: the GUI message-pump / Win32 subclass / Qt signal-slot first-consumer continuation.

The result was not a generic GUI summary. The run materially strengthened one practical native leaf with source-backed operator rules about:
- per-window subclass ownership truth
- safer subclass-chain reasoning via `SetWindowSubclass` / `DefSubclassProc`
- Qt direct vs queued delivery classification, including thread-affinity implications

## Branch-balance / direction review
### Why this branch was chosen
The native practical branch is now materially established, but some leaves still risk staying thinner in operator detail than the stronger browser/mobile/protected subtrees.

This GUI/event-dispatch continuation was chosen because it was:
- practical and recurring in real reversing
- underfed relative to denser native and protected-runtime leaves
- a good fit for an external-research-driven run that could produce concrete workflow value instead of more top-level wording or family-count sync

### Direction check
The KB’s intended direction remains practical, case-driven, and code-adjacent.
This run stayed aligned with that direction by improving:
- proof tactics
- stop rules
- ownership distinctions

It explicitly avoided:
- broad Win32 tutorialization
- broad Qt architecture explanation
- top-level wording-only maintenance without new practical signal

## Work completed
### KB changes
1. Added source note:
   - `sources/native-binary/2026-03-23-native-gui-subclass-and-qt-delivery-notes.md`

2. Materially strengthened practical leaf:
   - `topics/native-gui-message-pump-and-signal-slot-first-consumer-workflow-note.md`

### What changed in the leaf
The leaf now more clearly preserves these operator rules:
- Win32 subclass ownership is per window instance, not globally shared
- `SetWindowSubclass` / `DefSubclassProc` are useful live proof surfaces for reconstructing the actual subclass hop that owns a decisive `WM_*` family
- helper-based subclassing should not be treated as a cross-thread truth surface
- visible Qt signal emission does not itself prove queued delivery
- `DirectConnection`, `QueuedConnection`, and `AutoConnection` / thread-affinity implications should be classified before deciding where the first consequence-bearing consumer really lives

## Source-backed takeaways
### Win32 side
High-signal sources reinforced that:
- message loop / `WndProc` discovery is framework entry, not behavior proof
- subclassing changes ownership at the instance level
- the original procedure that matters is the one for the exact window being subclassed
- helper APIs preserve callback+ID / per-instance reference-data distinctions that matter in practical ownership recovery

### Qt side
High-signal sources reinforced that:
- many slots execute immediately on signal emission
- queued delivery is a special case that should be proved, not assumed
- cross-thread / thread-affinity facts are part of delivery classification and therefore part of consumer-proof workflow
- callback recovery improves the map, but still does not answer which slot first changes behavior in the current case

## Search audit
### Requested sources
- exa
- tavily
- grok

### Succeeded sources
- exa
- tavily
- grok

### Failed sources
- none

### Endpoints used
- Exa: `http://158.178.236.241:7860`
- Tavily: `http://proxy.zhangxuemin.work:9874/api`
- Grok: `http://proxy.zhangxuemin.work:8000/v1`

### Search execution details
Search was executed through:
- `skills/search-layer/scripts/search.py`
- explicit source selection: `--source exa,tavily,grok`

Queries:
1. `Win32 subclass CallWindowProc per-window original procedure reversing`
2. `Qt direct connection queued connection signal slot event loop reverse engineering`
3. `Win32 subclassing Raymond Chen per-window original wndproc SetWindowSubclass`

Raw search artifact:
- `sources/native-binary/2026-03-23-native-gui-subclass-signal-slot-search-layer.txt`

## Files changed this run
- `research/reverse-expert-kb/sources/native-binary/2026-03-23-native-gui-subclass-and-qt-delivery-notes.md`
- `research/reverse-expert-kb/topics/native-gui-message-pump-and-signal-slot-first-consumer-workflow-note.md`
- `research/reverse-expert-kb/runs/2026-03-23-1918-reverse-kb-autosync.md`
- `research/reverse-expert-kb/sources/native-binary/2026-03-23-native-gui-subclass-signal-slot-search-layer.txt`

## Commit / sync
If the working tree contains KB changes from this run only, commit them and run:
- `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`

## Overall assessment
This was a good anti-stagnation run.
It counted as a real external-research-driven pass, fed an under-denser practical branch, and improved operator value without reopening broad canonical-maintenance churn.
