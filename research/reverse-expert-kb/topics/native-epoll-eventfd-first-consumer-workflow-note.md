# Native epoll / eventfd First Consumer Workflow Note

Topic class: workflow note
Ontology layers: native async ownership, Linux event loops, readiness vs delivery, first consumer proof
Maturity: emerging
Related pages:
- topics/native-practical-subtree-guide.md
- topics/native-callback-registration-to-event-loop-consumer-workflow-note.md
- topics/native-inotify-fanotify-first-event-consumer-workflow-note.md
Related source notes:
- sources/native-and-desktop/2026-04-06-native-epoll-eventfd-first-consumer-notes.md

## 1. What this note is for
Use this note when a native Linux case already plausibly depends on **`epoll` / `eventfd` / loop wakeup delivery**, but the investigation still lacks the first trustworthy consumer boundary that turns visible readiness or wakeup plumbing into actual behavior ownership.

Typical situations:
- `epoll_wait(...)`, `epoll_ctl(...)`, or `eventfd(...)` is visible, but the real missing step is which first loop-owned consumer actually gives the event behavioral meaning
- fd readiness, wakeup writes, or event-loop dispatch is visible, but the analysis still collapses registration, readiness, dequeue/delivery, and later handler consequence together
- a libuv/libevent/libev-style loop is visible, but loop wakeup machinery is being mistaken for the later callback/handler that actually owns the behavior

This note is for the narrower question:

```text
Which first epoll/eventfd-owned consumer actually owns the behavior that matters?
```

Not the broader question:

```text
Does this target use epoll, eventfd, or a Linux event loop at all?
```

## 2. When to use it
Use this note when most of the following are true:
- the broad native async problem has already narrowed specifically into Linux `epoll` / `eventfd` / loop wakeup handling
- one watched-fd family, wakeup fd, or loop-dispatch path is already visible
- the main uncertainty is whether **registration truth**, **readiness truth**, **delivery/re-arm truth**, **first loop-owned consumer truth**, or **later visible consequence truth** actually owns the claim you care about
- the next useful output is one smaller trustworthy chain such as:
  - `epoll_ctl(...)` registration -> `epoll_wait(...)` readiness -> first dispatcher/handler consumer -> visible consequence
  - `eventfd_write` / wakeup -> loop wakeup record -> first loop-owned pending-work consumer -> visible consequence
  - library watcher registration -> loop wakeup/readiness -> first callback dispatch -> visible consequence

Do **not** start here when:
- the real bottleneck is still broader native route choice rather than Linux event-loop delivery
- the case has already narrowed into a more specific family such as inotify/fanotify, timer queues, waits, or GUI/message-pump ownership
- the first loop-owned consumer is already proved and the real missing step is later business logic consequence outside the async seam

## 3. Core claim
A recurring native-Linux mistake is to stop too early at one of these milestones:
- “the fd was registered with `epoll_ctl(...)`”
- “`epoll_wait(...)` returned readiness”
- “`eventfd` woke the loop”
- “the loop framework uses epoll, so this path owns the behavior”

The smaller reusable target is:

```text
registered
  != ready / woken
  != delivered / re-armed truth
  != first loop-owned consumer proved
  != later visible consequence truth
```

## 4. Boundary objects to keep separate
### A. Registration truth
Visible objects:
- `epoll_ctl(EPOLL_CTL_ADD|MOD|DEL, ...)`
- `eventfd(...)` creation and loop integration
- watcher registration in libuv/libevent/libev-style code

This is weaker than proof that the relevant event actually became ready or drove later behavior.

### B. Readiness / wakeup truth
Useful objects:
- one `epoll_wait(...)` return set
- one `EPOLLIN` / `EPOLLOUT` / `EPOLLERR` / `EPOLLHUP` readiness report
- one `eventfd` readable/wakeup record

This is weaker than proof that the right handler or callback actually consumed it meaningfully.

### C. Delivery / re-arm truth
Typical smaller truths:
- edge-triggered vs level-triggered handling reality
- `EPOLLONESHOT` re-arm path
- drain-to-`EAGAIN` obligations
- wakeup fd read/clear behavior before later callbacks run

Do not flatten “readiness happened” into “the loop-side consumer is solved.”

### D. First loop-owned consumer truth
This is the first dispatcher/handler/callback path that gives the readiness or wakeup behavioral meaning.
Typical shapes:
- first `epoll_wait(...)` result dispatcher
- first per-fd handler callback
- first loop-owned pending-work reducer after wakeup fd consumption
- first library callback dispatch that turns readiness into state change

### E. Later visible consequence truth
This is where the analyst proves the event-loop-owned chain actually matters:
- one later state change, queued work execution, I/O action, request progression, or visible behavior depends on the consumer you froze
- one later effect only exists because the earlier loop-owned consumer actually ran

## 5. Practical stop rules this note preserves
- `fd registered != relevant readiness proved`
- `readiness returned != delivery/re-arm truth proved`
- `eventfd woke loop != first loop-owned consumer proved`
- `framework uses epoll != this callback/handler owned the behavior`
- `ready list visible != later visible consequence truth`

## 6. Default workflow
### Step 1: freeze one watched-fd family, one wakeup/readiness family, and one visible consequence
Do not widen into every watcher or loop phase.
Pick one high-leverage chain.

### Step 2: separate registration from readiness truth
Before explaining behavior, freeze:
- which fd or wakeup object was registered
- which readiness/wakeup instance belongs to the case that matters
- which event flags or wakeup record matter

### Step 3: freeze one delivery/re-arm boundary
Pick the smallest loop contract that matters:
- one edge-triggered drain boundary
- one `EPOLLONESHOT` re-arm boundary
- one wakeup-fd read/clear step

### Step 4: prove one first loop-owned consumer
Prefer the first dispatcher/handler/callback that best predicts later behavior.

### Step 5: stop once one smaller trustworthy chain exists
Examples:
- registration -> readiness -> first dispatcher callback -> visible effect
- `eventfd` wakeup -> wakeup consumer -> pending-work reducer -> visible effect
- watcher registration -> loop dispatch -> first callback consumer -> visible state change

## 7. Practical scenarios
### Scenario A: `epoll_ctl(...)` and `epoll_wait(...)` are visible
Wrong stop:
- “the loop uses epoll, so this path owns the behavior”

Better stop:
- freeze one readiness instance and one first dispatcher/handler consumer that actually changes behavior.

### Scenario B: `eventfd` wakeup is visible
Wrong stop:
- “the wakeup fd fired, so the later callback path is solved”

Better stop:
- keep wakeup truth separate from the first pending-work reducer or loop callback that actually consumes the wakeup meaningfully.

### Scenario C: edge-triggered / one-shot handling is visible
Wrong stop:
- “one readiness notification fired, so one callback execution is explained”

Better stop:
- preserve re-arm/drain truth separately before claiming consumer ownership.

## 8. Why this note exists in the native branch
The native subtree already had practical leaves for callback/event-loop ownership, IOCP/threadpool work, waits, timers, APCs, GUI/message pumps, and inotify/fanotify.
What it lacked was a Linux-specific continuation for **`epoll` / `eventfd` readiness and first loop-owned consumer ownership**.

This note fills that gap and preserves the smaller ladder:
- registration
- readiness / wakeup
- delivery / re-arm
- first loop-owned consumer
- later visible consequence

instead of collapsing everything into “the event loop woke up.”

## 9. Sources
See:
- `sources/native-and-desktop/2026-04-06-native-epoll-eventfd-first-consumer-notes.md`

Primary anchors retained:
- man7 `epoll(7)`, `epoll_wait(2)`, `epoll_ctl(2)`, `eventfd(2)`
- libuv / libevent / libev wakeup and event-loop documentation
- explicit `search-layer` multi-source attempt with `--source exa,tavily,grok`
