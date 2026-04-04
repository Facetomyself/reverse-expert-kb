# 2026-04-04 native inotify/fanotify first-event-consumer notes

Date: 2026-04-04 23:21 Asia/Shanghai / 2026-04-04 15:21 UTC
Theme: keep watch registration, concrete event-record truth, and first event-owned consumer truth separate.

## Why this note was retained
The native practical branch already had broad callback/event-loop reduction plus several Windows-heavy async continuations.
What it still lacked was a thinner Linux-native filesystem-watch continuation for cases where one inotify/fanotify registration is visible but the remaining ambiguity is which first event record actually becomes behaviorally real.

## Primary doc-backed anchors
### 1. inotify(7)
Source:
- man7.org — inotify(7)
  - https://man7.org/linux/man-pages/man7/inotify.7.html

Retained points:
- inotify events are read from the inotify file descriptor as `struct inotify_event` records
- events carry masks, watch descriptors, and optional names
- watch registration is distinct from later event delivery

Operator consequence:
- `inotify_add_watch` visibility is weaker than one concrete event record and weaker still than first consumer truth

### 2. fanotify_init(2) / fanotify_mark(2)
Sources:
- man7.org — fanotify_init(2)
  - https://man7.org/linux/man-pages/man2/fanotify_init.2.html
- man7.org — fanotify_mark(2)
  - https://man7.org/linux/man-pages/man2/fanotify_mark.2.html

Retained points:
- fanotify creates a monitoring instance and marks filesystem objects for observation
- the monitoring instance and mark configuration are weaker than one event metadata record and one first consumer
- object scope and mask configuration matter for compare-honest interpretation

Operator consequence:
- watcher setup alone does not explain later behavior; event records and their first consumer do

## Practical synthesis retained
This continuation keeps the following smaller split visible:

```text
watch registration
  != relevant event record in the run that matters
  != first parsed/filtered event consumer
  != downstream effect ownership
```

The operator move is to ask:
- what first event-mask/path/object dispatcher actually becomes the first consequence-bearing consumer after inotify/fanotify registration?

## Search-layer trace
See:
- `sources/native/2026-04-04-2321-native-inotify-search-layer.txt`

Observed degraded mode:
- Exa: returned results
- Tavily: returned results
- Grok: invoked but returned empty set
