# iOS Background URLSession Relaunch to Result-Consumer Workflow Note

Topic class: workflow note
Ontology layers: iOS practical reversing, background networking, delegate relaunch, first result consumer
Maturity: practical
Related pages:
- topics/ios-practical-subtree-guide.md
- topics/mobile-reversing-and-runtime-instrumentation.md
- topics/ios-url-loading-interception-and-first-consumer-workflow-note.md
- topics/ios-swift-concurrency-continuation-to-policy-workflow-note.md
Related source notes:
- sources/ios/2026-06-12-ios-background-urlsession-relaunch-delegate-notes.md

## 1. What this note is for
Use this note when an iOS case has narrowed into **background `URLSession` transfer ownership**, but the analyst is still flattening task creation, system-owned transfer progress, relaunch callbacks, delegate drain, completion-handler calls, and later app behavior into one vague "background request happened" claim.

Typical situations:
- a background `URLSessionConfiguration.background(withIdentifier:)` or `NSURLSession` background configuration is visible
- upload/download tasks are created, but the first behavior-changing consumer only appears after app suspension, termination, or relaunch
- `application(_:handleEventsForBackgroundURLSession:completionHandler:)` is visible, but it is unclear whether this proves app-owned result consumption
- `urlSessionDidFinishEvents(forBackgroundURLSession:)` fires, but the later file move, parse/decrypt, database update, retry decision, notification, or next request is still unproved
- a compare pair lies because one run exercises foreground delegates while the other exercises background daemon/relaunch delivery

This note answers the narrower question:

```text
Which background-session relaunch/delegate/result-consumer boundary actually owns the behavior being claimed?
```

Not the broader question:

```text
Does this app use URLSession or background networking at all?
```

## 2. When to use it
Use this note when most of the following are true:
- one decisive request family is already known to be iOS/Foundation-owned rather than WebView-only or custom-native-only
- the session is background-shaped, or evidence differs when the app is suspended, terminated, relaunched, or run foreground-only
- the missing proof object is no longer generic URL-loading interception, trust evaluation, or request signing; it is the handoff from background transfer delivery into app-owned result behavior
- you can name at least one of: background session identifier, task creation site, app-delegate relaunch method, session delegate callback family, downloaded/uploaded file location, or post-transfer consumer

Do **not** start here when:
- the current blocker is still traffic topology, pinning/trust-path localization, or custom `URLProtocol` / `WKURLSchemeHandler` selection
- the transfer is already foreground-owned and the meaningful behavior is a normal delegate/completion/async-result reducer
- one background result consumer is already proved and the remaining work is downstream parsing, protocol semantics, malware staging, or request-signing preimage recovery

## 3. Core claim
A common iOS reverse-engineering mistake is to stop at one of these attractive but early facts:
- "the app created a background `URLSession` task"
- "the transfer completed while the app was not foregrounded"
- "`handleEventsForBackgroundURLSession` fired"
- "`urlSessionDidFinishEvents(forBackgroundURLSession:)` fired"
- "the downloaded file exists"

The smaller reusable ladder is:

```text
background task created
  != system/daemon accepted and progressed transfer
  != app relaunched for the same session identifier
  != queued delegate events delivered
  != app called the stored completion handler
  != app parsed/consumed the result or produced a durable effect
```

Keep the short branch-memory form visible:

```text
created != progressed != relaunched != delegate-drained != completion-called != result-consumed
```

## 4. Boundary objects to keep separate
### A. Background-session configuration truth
Freeze:
- `URLSessionConfiguration.background(withIdentifier:)` / `backgroundSessionConfigurationWithIdentifier:` identifier
- whether the current run uses that exact identifier
- delegate object and queue used for the background session
- `sessionSendsLaunchEvents` / equivalent launch-event posture when visible
- discretionary, cellular, expensive-network, power, or connectivity settings only if they decide whether no-progress/no-callback is meaningful

This is setup truth, not transfer-result truth.

### B. Task creation and system-transfer truth
Freeze:
- task type: upload, download, or data-like path
- request identity and file/body identity if relevant
- task identifier / original request / earliest resume point
- whether the system accepted the task and whether progress/completion occurred outside the foreground app

A task resume or progress callback is still weaker than proving the later app-owned consumer.

### C. App relaunch / reattachment truth
Freeze:
- `application(_:handleEventsForBackgroundURLSession:completionHandler:)`
- session identifier passed to the app delegate
- where the app stores the completion handler
- whether the app recreates/reattaches a `URLSession` with the same identifier

This is reattachment truth. It does not prove any task result was parsed, persisted, surfaced, or used.

### D. Delegate-event delivery / drain truth
Freeze:
- relevant task delegate result callbacks such as completion/error, download-finished location, response, authentication, redirect, or metrics callbacks
- `urlSessionDidFinishEvents(forBackgroundURLSession:)` / `URLSessionDidFinishEventsForBackgroundURLSession:`
- whether all queued delegate events for that background session were delivered to the current delegate instance

Delegate drain means the queued messages reached the delegate. It is not equivalent to the app calling the stored app-delegate completion handler or consuming the downloaded/uploaded result.

### E. Completion-handler call truth
Freeze:
- the stored app-delegate completion handler
- the callsite that invokes it after delegate drain
- whether it is called once, too early, too late, or not at all
- whether the call is gated by task count, error state, database state, notification scheduling, or foreground/background state

This boundary matters because app snapshots, system scheduling, and later relaunch behavior can depend on it, while the behavior being reversed may still live after or before it.

### F. First result-consumer truth
Prefer one small app-owned consumer over broad network storytelling:
- file move from temporary download location
- parse/decrypt/decompress/import of the downloaded file
- database/cache/keychain update
- retry/backoff/next-request scheduling
- notification/UI model update
- request-signing/token-state update derived from the background result
- upload acknowledgement mapped into local state

Stop when one result consumer plus one later effect explains the claim. Do not keep widening into every delegate method.

## 5. Practical stop rules
- `background configuration visible != current session identifier owns this task`
- `task created/resumed != system accepted and progressed it`
- `transfer complete != app relaunched for the matching identifier`
- `handleEventsForBackgroundURLSession fired != task result consumed`
- `delegate callback fired != all queued background events drained`
- `urlSessionDidFinishEvents fired != stored app completion handler called`
- `completion handler called != downloaded file parsed or uploaded result acted on`
- `foreground delegate behavior != background relaunch behavior`
- `download file exists != durable app-owned state/effect`

## 6. Default workflow
### Step 1: freeze one session identifier and one task family
Record:

```text
identifier | config owner | delegate | task kind | request/file/body | task id | resume point | foreground/background state
```

If multiple identifiers exist, pick the one that predicts the behavior and leave the others as decoys until proven relevant.

### Step 2: prove system-transfer progress separately from app behavior
Look for the smallest proof that the task was accepted and progressed:
- task resume / state transition
- progress or completion delegate evidence
- downloaded temporary file location
- upload completion/error callback
- OS relaunch reason tied to the session identifier

Do not call this app-owned consumption yet.

### Step 3: prove relaunch and reattachment
Hook or inspect:
- app-delegate `handleEventsForBackgroundURLSession` method
- session identifier passed into that method
- storage of the completion handler
- recreation of the background session using the same identifier

If the identifier does not match, the current relaunch callback is not evidence for the task you care about.

### Step 4: prove delegate event drain
Separate individual task callbacks from session drain:
- task completion/error or download-finished callback
- response/auth/redirect/metrics callbacks if they change behavior
- `urlSessionDidFinishEvents(forBackgroundURLSession:)`

Event drain is a delivery boundary. It is often the right place to stop URLSession mechanics and hand off into app logic.

### Step 5: find the first result consumer
Continue exactly one hop into app-owned behavior:
- temp file -> file move/import/parser
- response/error -> retry scheduler
- upload completion -> state machine update
- downloaded payload -> decrypt/decompress/config import
- delegate drain -> stored completion handler -> notification/UI/cache effect

Once one consumer and effect are proved, stop widening the URLSession search.

## 7. Practical scenarios
### Scenario A: Background download completes after app termination
Wrong stop:
- "the task completed, so the app consumed the file"

Better stop:
- prove relaunch with the same identifier
- prove download-finished callback and temporary location
- prove one file move/import/parse/decrypt consumer
- only then claim app-owned downloaded-result behavior

### Scenario B: `handleEventsForBackgroundURLSession` fires but behavior is missing
Wrong stop:
- "relaunch happened, so the background path worked"

Better stop:
- check whether the app stored the completion handler
- recreate/reattach the session with the same identifier
- wait for `urlSessionDidFinishEvents`
- prove the stored completion handler call and then the result consumer

### Scenario C: Foreground run and background run diverge
Wrong stop:
- "same request means same consumer"

Better stop:
- compare foreground delegate/completion delivery with background relaunch/delegate-drain delivery
- preserve task identifier, session identifier, app state, and result file identity
- find the first reducer/parser/state update that differs after delegate delivery

### Scenario D: Background upload acts like a durable queue
Wrong stop:
- "upload task created means upload-owned state changed"

Better stop:
- prove task acceptance/progress, completion/error delivery, and app relaunch if needed
- then prove the local state transition that marks the queued item uploaded, retries it, deletes it, or schedules the next request

### Scenario E: No callback arrives
Wrong stop:
- "target suppressed the request"

Better stop:
- first rule out identifier mismatch, no reattached session, `sessionSendsLaunchEvents` posture, foreground-only delegate assumptions, and task not accepted/progressed
- only then widen into target-side gating or trust/policy logic

## 8. Hook / breakpoint plan
Start narrow:
- `+[NSURLSessionConfiguration backgroundSessionConfigurationWithIdentifier:]`
- `URLSessionConfiguration.background(withIdentifier:)`
- `-[NSURLSession downloadTaskWithRequest:]`, upload task creation, task `resume`
- `application:handleEventsForBackgroundURLSession:completionHandler:` / Swift equivalent
- storage and invocation of the app-delegate completion handler
- recreation of a `URLSession` with the same identifier
- `URLSession:downloadTask:didFinishDownloadingToURL:`
- `URLSession:task:didCompleteWithError:`
- `URLSessionDidFinishEventsForBackgroundURLSession:` / `urlSessionDidFinishEvents(forBackgroundURLSession:)`
- first file move, parse/decrypt/import, retry/state update, notification, or next-request enqueue after delegate delivery

For Swift-heavy cases, expect the delegate result to cross into `async` / `Task` / `AsyncStream` / MainActor state. If callback/delegate truth is already good enough and the remaining liar is continuation or stream consumption, hand off to the Swift-concurrency or `AsyncStream` notes rather than widening background-session hooks.

## 9. Evidence table
Use a compact table per task:

```text
session_id | task_id | task_kind | request/body/file | app_state | accepted/progressed | relaunch_id | delegate_callbacks | did_finish_events | completion_handler_called | first_result_consumer | later_effect | false_stop_ruled_out
```

## 10. Hand-off rules
- If the real blocker is whether the request family reaches Foundation URL loading at all, hand off to traffic topology or trust-path localization.
- If the real blocker is `URLProtocol`, session-local `protocolClasses`, or `WKURLSchemeHandler`, hand off to URL-loading interception.
- If the result consumer enters Swift `async` / continuation / stream logic, hand off after delegate delivery to the Swift-concurrency or `AsyncStream` notes.
- If the downloaded/uploaded material is a protocol payload, hand off after first app-owned result availability to protocol/message recovery.
- If the downloaded material is a stage, config, or payload, hand off after first app-owned import/execute/decode consumer to staged malware or protected-runtime artifact-provenance notes.

## 11. Source-backed cues
- Apple documents `application(_:handleEventsForBackgroundURLSession:completionHandler:)` as the app-delegate method used when background URL session events need to be handled after the app is relaunched; it provides a session identifier and completion handler rather than direct result-consumer proof.
- Apple documents `urlSessionDidFinishEvents(forBackgroundURLSession:)` as the delegate callback indicating all messages enqueued for a background session have been delivered.
- Apple's background-download guidance keeps relaunch/event handling separate from ordinary foreground request flow; once relaunched, queued events are delivered to the app's delegate path.
- `sessionSendsLaunchEvents` is configuration-shaped evidence: launch delivery can be disabled, so missing relaunch callbacks can be setup/configuration truth rather than proof that the target never transferred.
- Developer forum and issue traces reinforce the practical implementation shape: save the app-delegate completion handler, recreate the background session with the same identifier, let delegate events drain, then call the stored completion handler. Treat those as implementation cues, not a substitute for target-local proof.

## 12. What this adds to the KB
The iOS branch already had URL-loading interception, trust-path localization, Swift continuation, and result-to-policy notes. This page fills a narrower background-transfer seam where the false proof is:

```text
created/resumed background URLSession task or relaunch callback == app-owned result behavior
```

The durable operator rule is smaller:

```text
created != progressed != relaunched != delegate-drained != completion-called != result-consumed
```
