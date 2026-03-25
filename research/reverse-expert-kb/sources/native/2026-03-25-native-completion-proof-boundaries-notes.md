# Native completion / thread-pool proof-boundaries notes — 2026-03-25

Context:
- external-research-driven autosync pass for the native practical branch
- target leaf: `topics/native-completion-port-and-thread-pool-first-consumer-workflow-note.md`
- raw search trace: `2026-03-25-native-completion-proof-boundaries-search-layer-1216.txt`

## Search / source-set status
Requested through `search-layer`:
- exa
- tavily
- grok

Observed usable result set:
- Exa: succeeded
- Tavily: succeeded
- Grok: failed (`502 Bad Gateway` during invocation)

This note keeps only conservative claims grounded mainly in Microsoft documentation plus one Raymond Chen practical explanation.

## Primary retained sources
- Microsoft Learn — `GetQueuedCompletionStatus`
- Microsoft Learn — `PostQueuedCompletionStatus`
- Microsoft Learn — `CreateThreadpoolIo`
- Raymond Chen, *The mental model for StartThreadpoolIo*

## Retained practical cues
### 1. Posted control packets are not the same thing as I/O-owned completion packets
`PostQueuedCompletionStatus` is explicitly allowed to post a packet whose returned values are simply the values supplied by the caller.
Microsoft also states that the system does **not** validate those values, and `lpOverlapped` need not point to a real `OVERLAPPED`.

Practical consequence for the KB:
- a worker loop reaching `GetQueuedCompletionStatus` does not by itself prove an I/O-owned request completed
- first separate **posted control-plane packet truth** from **real I/O-owned packet truth** before claiming request/session ownership

### 2. `completion key` and `OVERLAPPED*` are different ownership carriers
`GetQueuedCompletionStatus` returns both:
- a per-file completion key associated through `CreateIoCompletionPort`
- the `OVERLAPPED*` used when the completed I/O operation was started

Practical consequence for the KB:
- the completion key often narrows handle family / queue family / control family
- the `OVERLAPPED*` more often leads back to the concrete embedded request/session owner
- do not flatten them into one ownership claim

### 3. `GetQueuedCompletionStatus(FALSE)` with non-NULL `lpOverlapped` can still mean a completion was dequeued
Microsoft documents that failure cases split meaningfully:
- timeout -> no packet dequeued, `lpOverlapped == NULL`
- failed I/O completion -> packet dequeued, return is FALSE, but `lpOverlapped != NULL`

Practical consequence for the KB:
- do not treat every FALSE return as “nothing happened”
- failed completions can still own retry / degrade / fallback behavior

### 4. `CreateThreadpoolIo` is not callback-delivery proof by itself
Microsoft states:
- call `StartThreadpoolIo` to begin receiving overlapped I/O completion callbacks
- under `FILE_SKIP_COMPLETION_PORT_ON_SUCCESS`, if an async operation returns immediately with success, the callback is not called and notifications must be canceled

Raymond Chen’s practical clarification is sharper:
- `StartThreadpoolIo` is conceptually **per I/O operation**, not “once per handle forever”
- if no completion will arrive after all, call `CancelThreadpoolIo`

Practical consequence for the KB:
- do not flatten thread-pool I/O object creation into callback truth
- do not diagnose a missing callback as dead code until per-operation `StartThreadpoolIo` discipline and success-skip notification mode have been checked

## Canonical KB direction added by this run
The native completion-driven branch should preserve one extra operator split:
- **queue/dequeue visibility**
- **posted control-packet vs real I/O-owned packet truth**
- **completion-key family identity vs `OVERLAPPED*` owner recovery**
- **per-operation thread-pool expectation setup (`StartThreadpoolIo`)**
- **callback absence caused by immediate-success skip mode vs genuinely missing consumer**

That split is useful because it changes real debugging behavior:
- it prevents fake ownership claims based on worker-loop visibility alone
- it prevents premature “consumer never runs” claims in `TP_IO` cases
- it gives a smaller stop rule before widening into scheduler folklore or queue taxonomy
