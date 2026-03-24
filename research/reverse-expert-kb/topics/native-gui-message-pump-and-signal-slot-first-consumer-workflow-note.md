# Native GUI Message-Pump and Signal-Slot First-Consumer Workflow Note

Topic class: workflow note
Ontology layers: native baseline practical branch, runtime-evidence bridge, GUI/event-dispatch practical continuation
Maturity: emerging
Related pages:
- topics/native-practical-subtree-guide.md
- topics/native-binary-reversing-baseline.md
- topics/native-callback-registration-to-event-loop-consumer-workflow-note.md
- topics/native-interface-to-state-proof-workflow-note.md
- topics/runtime-behavior-recovery.md
- topics/causal-write-and-reverse-causality-localization-workflow-note.md

## 1. What this workflow note is for
This note covers a thinner native-desktop case that appears constantly in real work:
- Win32-style message pumps and window procedures are visible
- subclass chains or wrapper procedures are visible
- Qt-style event delivery, `event()` handling, signal emission, and slot fan-out are visible
- or macOS Cocoa event delivery, `NSApplication sendEvent:`, responder-chain routing, target/action dispatch, XPC proxy/object boundaries, or dispatch-source callbacks are visible
- but the investigation still stalls because the analyst has not proved which handler, slot, responder, exported-object method, or callback is the **first behavior-changing consumer**

This is not the broad problem of understanding all async structure in a native target.
It is the narrower GUI/framework problem of reducing:

```text
visible event plumbing
```

into:

```text
one concrete UI/event family -> one consumer -> one durable consequence
```

The goal is to stop treating “the window procedure” or “the signal emission site” as the answer.
In practice, the answer is usually one layer later:
- one `WM_*` branch that writes state, schedules work, or chooses policy
- one subclass procedure that intercepts the decisive message family
- one Qt slot or `event()` override that first changes behavior
- one queued connection or follow-on callback that turns a visible UI event into a real program consequence

## 2. When to use this note
Use this note when most of the following are true:
- the target is native desktop / infotainment / rich-client shaped rather than browser, mobile, or heavily protected-first
- a GUI or event framework is clearly involved
- `GetMessage` / `DispatchMessage`, `WndProc`, `CallWindowProc`, message maps, `event()`, `QObject::connect`, `emit`, or slot machinery are already visible
- broad callback/event-loop structure is no longer the main mystery
- the real bottleneck is proving which message/slot consumer first matters for the analyst’s target question

Typical triggers:
- “I found the WndProc, but there are too many `WM_*` branches.”
- “I found subclassing, but I still don’t know which window-specific consumer owns the behavior.”
- “I found the Qt signal and its connections, but there are several slots and only one really changes policy.”
- “The GUI action is obvious, but the first durable write or follow-on worker handoff is not.”

Do **not** use this note as the first stop when:
- semantic labels are still too slippery to trust at all
- several broad interface routes still compete and no representative route has been proved yet
- the problem is really service/daemon worker ownership rather than GUI dispatch
- the case is better described by a protected-runtime, mobile, protocol, or browser branch

## 3. Core claim
In GUI-heavy native work, the decisive proof usually is **not** “I located the event loop” or “I found the callback registration.”
It is:

```text
one event family
 -> one framework reduction boundary
 -> one first consequence-bearing consumer
 -> one observable downstream effect
```

For Win32, that usually means:
- distinguish the message pump from the real `WndProc` branch
- distinguish the class procedure from a later subclass procedure
- distinguish the presence of `CallWindowProc` from the specific per-window original-proc chain that preserves ownership

For Qt, that usually means:
- distinguish event arrival from signal emission
- distinguish signal emission from direct-vs-queued slot delivery
- distinguish a broad slot graph from the first slot that writes state, schedules work, or chooses one downstream action family

For macOS Cocoa / XPC / dispatch-heavy cases, that usually means:
- distinguish `NSApplication` / `sendEvent:` visibility from the first responder or target/action receiver that actually changes behavior
- distinguish XPC connection/proxy setup from the service-side exported-object method or the first stateful reducer behind it
- distinguish dispatch-source registration or callback delivery from the first parser/classifier/state reducer that turns queue delivery into app-local meaning

## 4. Why this narrower continuation matters
The broader note `topics/native-callback-registration-to-event-loop-consumer-workflow-note.md` already explains how to reduce callback and event-loop ownership in native targets.

This page is a **thinner continuation** for one especially common subfamily:
- desktop GUI message pumps
- Win32 subclass chains
- Qt event delivery and signal-slot graphs

That narrower focus matters because GUI/event-framework cases have a recurring failure mode:
- analysts stop too early at framework labels like `WndProc`, `DefWindowProc`, `DispatchMessage`, `event()`, or `emit`
- but those labels still do not prove which handler actually changed later behavior

This note therefore biases toward:
- one message family, not whole-window cataloging
- one slot/consumer, not whole-signal graph inventory
- one durable state or follow-on task, not framework narration

## 5. Practical source-backed reminders
The current source pass supports several operator reminders.

### A. Win32 message pumps do not themselves explain behavior
Official Win32 material makes clear that the message loop, class registration, and `lpfnWndProc` association are framework structure, not by themselves the consequence-bearing answer.
The analyst still needs the specific handled `WM_*` path that predicts the target behavior.

### B. Subclass chains are ownership-sensitive per window instance
Microsoft guidance and Raymond Chen’s discussion both reinforce a practical reversing rule:
- when subclassing is present, the saved original procedure is window-instance specific
- treating some globally remembered “old WndProc” as the consumer truth is unsafe
- a real proof often depends on identifying **which exact window instance** and **which exact subclass hop** owns the decisive message family

This is highly relevant in reversing because subclass wrappers often look symmetrical in pseudocode while actually preserving different downstream ownership chains.

### C. Qt signals do not automatically imply deferred event-loop delivery
Qt documentation makes an important distinction:
- many slots run immediately on signal emission
- queued connections defer delivery until later

For reversing, this means:
- do not assume every visible signal implies a later queue boundary
- first classify whether the target signal/slot edge is immediate or queued
- only then decide whether the proof boundary is emission-time or later event-loop delivery

### D. Qt binary work benefits from callback recovery, but callback recovery is still not enough
QtRE’s reported value is exactly that it recovers large amounts of callback and semantic information from Qt binaries.
That is useful, but it still leaves the analyst with the narrower practical question:
- among the recovered callbacks/slots, which one first changes behavior in a way that matters for the case?

So callback recovery is a map improver, not the endpoint.

### E. Cocoa event-loop and responder-chain visibility are still only framework reduction unless they change ownership
Apple’s Cocoa architecture documentation makes a practical reversing distinction worth keeping explicit:
- `NSApplication` sets up the main event loop and receives events from the window server
- `sendEvent:` dispatches events onward, often into `NSWindow`, controls, target/action logic, and the responder chain
- `NSApplication sendEvent:` is therefore an early interception boundary, but not automatically the truthful consumer

For reversing, this means:
- do not stop at `sendEvent:` just because it is the first global app-side hook
- only treat it as the first real consumer if it suppresses, rewrites, retargets, or policy-gates later behavior
- otherwise continue until one responder, target/action receiver, exported-object method, or stateful reducer actually predicts the downstream effect

### F. XPC and dispatch-source setup are ownership reducers, not always the decisive consumer
Apple’s XPC and dispatch-source material also support a narrower stop rule:
- `NSXPCConnection`, proxy acquisition, listener setup, and dispatch-source registration reduce the search space
- but they often remain delivery scaffolding rather than the first consequence-bearing consumer

For reversing, this means:
- preserve the boundary between XPC connection/proxy setup and the service-side exported-object method that actually changes behavior
- preserve the boundary between dispatch-source registration/callback delivery and the first parser, classifier, or state reducer after callback entry

## 6. The four boundaries to mark explicitly

### A. Trigger family
Choose one event family only.
Typical examples:
- `WM_COMMAND`, `WM_NOTIFY`, `WM_TIMER`, `WM_PAINT`, `WM_SIZE`
- one custom control notification
- one mouse/keyboard event that gates a later action
- one Qt `QEvent` subtype
- one emitted signal such as `clicked()`, `finished()`, `valueChanged()`, or a target-specific signal

Capture:
- what external or internal trigger makes this family happen
- why this family is the smallest credible bridge to the later behavior you care about

### B. Framework reduction boundary
This is where the broad event framework becomes one concrete handler family.
Typical examples:
- `DispatchMessage` into one specific `WndProc`
- subclass interception before or after the original procedure
- one switch branch on `uMsg`
- one `event()` override selecting a narrower event case
- one `QObject::connect` edge that identifies the relevant receiver set
- one direct-vs-queued connection decision
- `NSApplication sendEvent:` into one `NSWindow`, control, target/action receiver, or responder-chain branch
- one XPC proxy call narrowing into a service-side exported-object method
- one dispatch-source delivery narrowing into one concrete callback family

Capture:
- where broad framework routing becomes a smaller candidate set
- whether ownership is class-wide, per-instance, or connection-specific

### C. First consequence-bearing consumer
This is the first handler/slot that predicts later behavior better than the framework labels do.
Typical examples:
- one `WM_COMMAND` branch updating mode or object state
- one subclass procedure swallowing or rewriting a message before forwarding
- one slot that schedules a worker, emits a narrower downstream signal, or stores durable UI/business state
- one handler that bridges from GUI semantics into service/business logic
- one responder-chain or target/action receiver that performs the first durable write or policy choice
- one service-side XPC exported-object method that owns the first real behavior change
- one parser/classifier/state reducer immediately after a dispatch-source callback

Capture:
- one exact function or slot
- the one write, branch, enqueue, or ownership transfer that makes it matter

### D. Proof-of-effect boundary
This is where the case stops being framework interpretation and becomes proved behavior.
Typical examples:
- one visible UI transition
- one worker/task enqueue
- one IPC or request-builder invocation
- one later policy/state change
- one compare-run difference when the triggering message or slot is suppressed or altered

Capture:
- one concrete downstream effect linked back to the chosen consumer

## 7. Default workflow

### Step 1: choose one event family with a visible late effect
Good candidates are event families that can be linked to:
- a specific button/menu action
- one state-mode change
- one follow-on request, task, or object creation
- one visible accept/reject/enable/disable path

Bad candidates are event families chosen only because they are common or central-looking.

### Step 2: separate framework entry from real ownership
For Win32, label separately:
- message pump
- class `WndProc`
- subclass proc(s)
- original-proc forwarding boundary
- one `WM_*` branch that may actually matter

For Qt, label separately:
- event arrival
- event handler or signal emission site
- connect graph edge(s)
- direct vs queued delivery
- slot(s) that may actually matter

For macOS, label separately:
- event-source or action family
- `NSApplication` / `sendEvent:` visibility
- `NSWindow`, control, or responder-chain reduction
- target/action receiver or exported-object method candidate set
- dispatch-source callback delivery vs the first stateful reducer after callback entry

### Step 3: prove per-instance or per-connection ownership before generalizing
This is especially important when:
- the same subclass proc is attached to several controls
- several windows share a class procedure but differ by user data / properties / attached subclass data
- several Qt receivers connect to the same signal
- Cocoa responder-chain candidates or target/action receivers share selector names but not behavioral ownership
- pseudocode makes several slots or callbacks look equivalent even though one is the only policy-changing consumer

A practical rule:
- in GUI work, never assume framework symmetry implies behavioral symmetry

### Step 4: pick the first consumer that changes behavior, not the prettiest framework hook
Prefer the handler/slot that:
- writes durable state
- selects the next action family
- emits a narrower downstream signal that clearly matters
- queues a worker or request path
- suppresses, rewrites, or forwards the event in a behavior-changing way

Preserve three narrower stop rules before generalizing:
- **Win32:** do not flatten shared subclass wrappers into one owner; recover the exact `HWND` plus live subclass hop, and when helper-based subclassing is in play preserve the callback + subclass-ID pair and instance-local reference data rather than stopping at “this window class is subclassed”
- **Qt:** do not flatten `AutoConnection` into generic “queued” proof; first determine receiver thread affinity and whether the slot is delivered directly at emit time or later through queued delivery
- **Cocoa:** do not stop at `NSApplication sendEvent:` unless that method itself suppresses, rewrites, retargets, or policy-gates the path; otherwise continue into one `NSWindow`, responder-chain receiver, target/action consumer, or later exported-object method that actually changes behavior

### Step 5: use one narrow runtime proof
Minimal proofs that work well here:
- breakpoint/log on one `WM_*` branch rather than the whole `WndProc`
- breakpoint on `SetWindowLongPtr` / `SetWindowSubclass` or `CallWindowProc` to recover the live subclass chain
- compare-run with one message family altered or one control action avoided
- hook/log one Qt slot and one downstream state write
- distinguish direct vs queued slot delivery by checking whether the consumer runs before control returns to the outer loop

### Step 6: rewrite the map in consumer-first form
Once proved, rewrite the subsystem like this:

```text
trigger family
 -> framework reduction boundary
 -> first consequence-bearing consumer
 -> downstream effect
```

Do not keep the final map at the level of:
- “the app uses WndProc”
- “the control is subclassed”
- “Qt signals/slots are involved”

Those are only framework facts.

## 8. Common scenario patterns

### Pattern 1: Win32 command routing through a crowded `WndProc`
Symptoms:
- `WndProc` is easy to find
- many `WM_*` branches exist
- the target behavior is tied to one command/control action

Best move:
- choose one `WM_COMMAND` / `WM_NOTIFY` family
- identify the exact control/command discriminator
- prove the first branch that writes state or schedules later work

### Pattern 2: Subclassed control where the real logic is not in the original class proc
Symptoms:
- `SetWindowLongPtr`, `SetWindowSubclass`, or wrapper helpers are visible
- pseudocode suggests forwarding through `CallWindowProc` / `DefSubclassProc`
- behavior depends on one specific control instance

Best move:
- recover the live subclass chain for that instance
- prove which hop intercepts or transforms the decisive message
- only then widen into sibling controls

### Pattern 3: Qt signal with many plausible receivers
Symptoms:
- a signal emission point is visible
- many `connect` edges or receiver methods exist
- callback recovery gives a graph but not ownership

Best move:
- classify direct vs queued delivery first
- include receiver thread affinity or `AutoConnection` behavior in that classification when visible
- choose one receiver that changes policy, state, or downstream action
- prove one consumer-to-effect edge instead of cataloging every receiver

### Pattern 4: GUI action that really matters only after a later queued continuation
Symptoms:
- the visible slot looks trivial
- the real consequence happens later in a worker/task/request path
- direct call-graph reading breaks after a queued handoff

Best move:
- still treat the GUI consumer as the first proof boundary
- then hand off to runtime-evidence or reverse-causality work once one enqueue/state edge is already grounded

### Pattern 5: Cocoa event seen early in `sendEvent:` but actually consumed later in responder or target/action routing
Symptoms:
- a custom `NSApplication` subclass or `sendEvent:` hook is easy to find
- the event family is obvious, but `sendEvent:` mostly forwards normal processing
- the first durable consequence appears only after responder-chain or control-action routing

Best move:
- treat `sendEvent:` as framework reduction unless it actually suppresses or rewrites behavior
- preserve the later responder or target/action receiver as the first truthful consumer if that is where state, policy, or task ownership changes

### Pattern 6: XPC or dispatch-source cases where the visible callback is still only delivery proof
Symptoms:
- `NSXPCConnection`, proxy calls, listeners, or dispatch-source registration are visible
- callback delivery is easy to hook
- the real question is still which exported-object method or post-callback reducer changes behavior

Best move:
- separate connection/registration from actual consumer ownership
- prove one exported-object method, parser, classifier, or state reducer that first predicts later behavior
- do not freeze the map at “XPC exists” or “dispatch source fires”

## 9. Handoff rule
Leave this note once the main uncertainty is no longer “which GUI message/slot consumer first matters?”

Common next steps:
- move to `topics/causal-write-and-reverse-causality-localization-workflow-note.md` when one GUI consumer is already known and the remaining bottleneck is the first decisive write/reducer behind a later effect
- move to `topics/runtime-behavior-recovery.md` when broader observability or compare-run design becomes the real need
- move back outward to `topics/native-callback-registration-to-event-loop-consumer-workflow-note.md` when the case stops being specifically GUI-shaped and becomes a broader async-ownership problem again

## 10. Failure modes this note helps prevent
- stopping at `WndProc`, `DispatchMessage`, `DefWindowProc`, or `event()` as if framework labels proved ownership
- assuming subclass chains are globally interchangeable rather than instance-specific
- assuming all Qt signal/slot edges are queued when many are immediate
- treating `NSApplication sendEvent:` or XPC proxy visibility as if it automatically proves consumer ownership
- treating callback recovery as sufficient proof of consequence
- cataloging whole GUI frameworks before grounding one consumer-to-effect chain

## 11. Compact operator checklist
- Pick one message or signal family only.
- Separate framework entry from per-instance or per-connection ownership.
- In Win32 subclass cases, preserve the exact per-window original-proc chain before generalizing from shared wrappers.
- Distinguish direct slot delivery from queued delivery.
- In Qt `AutoConnection` cases, decide whether the truthful consumer boundary is slot-immediate or receiver-loop-delivered.
- In Cocoa cases, treat `sendEvent:` as framework reduction unless it actually suppresses, rewrites, retargets, or policy-gates behavior.
- In XPC/dispatch-source cases, separate connection or registration visibility from the first exported-object method or post-callback state reducer that really changes behavior.
- Prefer the first behavior-changing consumer over framework landmarks.
- Prove one downstream effect before expanding the map.

## 12. Topic summary
GUI-heavy native reversing often stalls not because event plumbing is invisible, but because visible event plumbing is mistaken for behavioral ownership.

The practical cure is to choose one message or signal family, reduce the framework boundary into one per-instance or per-connection consumer, and prove the first downstream effect that makes that consumer behaviorally real.
