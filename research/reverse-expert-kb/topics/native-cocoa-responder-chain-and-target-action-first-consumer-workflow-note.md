# Native Cocoa Responder-Chain and Target-Action First-Consumer Workflow Note

Topic class: workflow note
Ontology layers: native baseline practical branch, GUI/event-dispatch continuation, macOS/AppKit responder-routing practical continuation
Maturity: practical
Related pages:
- topics/native-gui-message-pump-and-signal-slot-first-consumer-workflow-note.md
- topics/native-practical-subtree-guide.md
- topics/native-binary-reversing-baseline.md
- topics/native-callback-registration-to-event-loop-consumer-workflow-note.md
- topics/runtime-behavior-recovery.md
- topics/causal-write-and-reverse-causality-localization-workflow-note.md
Related source notes:
- sources/native/2026-04-19-cocoa-responder-chain-and-target-action-notes.md
- sources/native-and-desktop/2026-03-24-macos-event-delivery-boundary-notes.md

## 1. When to use this note
Use this note when a native/macOS/AppKit case is already narrow enough that broad Cocoa event delivery is no longer the real mystery, but the first behavior-changing consumer is still hidden inside responder-chain or target/action routing.

Typical entry conditions:
- `NSApplication`, `sendEvent:`, `NSWindow sendEvent:`, or the main event loop are already visible enough to trust as framework reduction
- one control, menu item, or keyboard-driven action family is already plausible
- `NSControl sendAction:to:`, `NSApplication sendAction:to:from:`, `targetForAction:`, selector names, or first-responder logic are visible enough to inspect
- the remaining lie is no longer “did the event reach AppKit at all?”
- the remaining lie is whether one selector actually resolved to one receiver that changed behavior, or whether the current view only forwarded / declined / left the action for a later responder

Use it for cases like:
- a custom `NSApplication sendEvent:` hook is easy to find, but it mostly forwards and the real behavior changes later
- a control or menu item uses target/action and the target may be `nil`
- several responders implement the same selector, and the current key-window / main-window / first-responder state decides which one really handles it
- the selector looks standard or semantically obvious, but it is unclear which concrete receiver first writes state, changes mode, or enqueues work
- one action receiver is visible, but it may still only forward to a later worker, coordinator, document object, or request path

Do **not** use this note when:
- the main uncertainty is still broad GUI/event plumbing rather than responder-chain or target/action resolution
- the case has already drifted into XPC proxy/exported-object ownership, dispatch-source callback ownership, or broader async delivery rather than AppKit control/action routing
- the first receiver is already known and the real remaining question is one later causal write, reducer, or compare-run divergence behind it

In those cases, use the broader native GUI note, a runtime-evidence note, or the Apple/XPC continuation instead.

## 2. Core claim
The practical stop rule for this seam is:

```text
NSEvent queued / sendEvent visible
  != control or menu item emitted action
  != explicit target or nil-target resolution truth
  != exact receiver on the current responder chain
  != first durable write / mode change / task enqueue
  != later visible consequence truth
```

Treat these as different proof objects until one is frozen:
- event-loop / `sendEvent:` truth
- control/menu action-emission truth
- explicit-target vs nil-target resolution truth
- exact receiver truth under the current responder-chain state
- first durable consumer truth
- later visible consequence truth

A smaller selector-shaped reminder worth preserving is:

```text
selector name visible
  != current responder chain will accept it
  != targetForAction / sendAction receiver truth
  != first behavior-changing consumer
```

The goal is not merely to prove that “the app uses target/action.”
It is to answer:

```text
Which smallest AppKit action boundary actually predicts the later behavior:
raw event routing, action emission, receiver resolution, or one first durable consumer?
```

## 3. The proof objects to separate explicitly

### A. Event-routing truth
This is where AppKit first becomes visible.
Typical anchors:
- `-[NSApplication nextEventMatchingMask:untilDate:inMode:dequeue:]`
- `-[NSApplication sendEvent:]`
- `-[NSWindow sendEvent:]`
- one obvious `NSEvent` family reaching a view or first responder

Useful reminder:
- this is framework reduction first
- it proves the event reached AppKit, not that the later action receiver already matters
- only stop here if `sendEvent:` itself suppresses, rewrites, retargets, or policy-gates the path

### B. Action-emission truth
This is where a control or menu item turns event-level traffic into an action message.
Typical anchors:
- `-[NSControl sendAction:to:]`
- `-[NSApplication sendAction:to:from:]`
- menu-item action emission
- a concrete selector/sender pair leaving one control path

Useful reminder:
- action emission is already more honest than raw `sendEvent:` visibility
- but it is still weaker than exact receiver truth
- this is often the best first runtime hook when `sendEvent:` is too early and selector names alone are too weak

### C. Resolution truth
This is where the receiver becomes either fixed or dynamically chosen.
Typical anchors:
- direct non-`nil` target
- `target == nil` with runtime resolution through responder-chain search
- `targetForAction:` returning one candidate receiver
- current key-window / main-window / first-responder / delegate state that constrains the search

Useful reminder:
- direct target and nil-target resolution are different proof objects
- `nil` target is not broadcast truth; it is current-chain search truth
- focus changes, panel activation, and first-responder drift can change the winner without changing the selector string

### D. Exact receiver truth
This is the first object that actually receives the selector in the run that matters.
Typical anchors:
- one concrete document controller, window controller, view, responder, or delegate object
- one object returned by `targetForAction:` that later receives `sendAction`
- one responder-chain hop that accepts the selector when earlier candidates decline or forward

Useful reminder:
- exact receiver truth is stronger than selector visibility
- but it is still weaker than consumer truth if the receiver mostly forwards or only performs trivial adaptation
- do not stop at the first object that merely *can* respond if the first durable state/task/policy change lives one hop later

### E. First durable consumer truth
This is the boundary that closes the target/action question.
Typical anchors:
- one state write or mode switch
- one document/model mutation
- one task enqueue, request build, or worker handoff
- one durable policy choice or enable/disable path

Useful reminder:
- this is the first receiver that actually predicts later behavior better than framework labels do
- once this boundary is frozen, the AppKit-routing question is solved and later work should hand off downstream instead of staying inside responder folklore

## 4. Practical source-backed reminders

### A. `sendEvent:` is the earliest AppKit hook, not automatically the truthful consumer
Apple’s event-architecture and main-event-loop material makes the delivery ladder explicit:
- the app object fetches the event
- converts it to `NSEvent`
- dispatches it with `sendEvent:`
- usually forwards toward the window, then the relevant view or first responder

For reversing, that means:
- treat `sendEvent:` as framework reduction by default
- only keep it as the answer if it changes routing or policy itself
- otherwise keep reducing into action emission and receiver resolution

### B. `NSControl sendAction:to:` is the practical handoff from raw input to app-specific command
Apple’s AppKit material preserves that controls use `sendAction:to:` and that this asks `NSApplication` / `NSApp` to deliver the action.

For reversing, that means:
- control-click or key event truth is weaker than action-emission truth
- `sendAction:to:from:` is often the smallest honest hook for freezing selector, target, and sender together
- when the case is control-driven, this boundary is usually more valuable than another earlier `sendEvent:` hook

### C. Nil-target routing follows a prescribed search order
Apple’s target/action documentation preserves the practical nil-target order:
- key-window first responder and successors
- key window, then key-window delegate
- main-window first responder and successors if needed
- main window, then main-window delegate
- application object, then app delegate

For reversing, that means:
- `target == nil` should be read as “current responder-chain search,” not “any object with the selector”
- key vs main window state and first responder state are evidence objects, not background noise
- if compare pairs differ in focus or panel activation, the receiver may drift even with the same selector and sender

### D. Untargeted actions and event messages do not follow the same proof model
Apple’s retained `NSResponder` material keeps two different routing styles explicit:
- events travel through AppKit event dispatch toward the relevant responder path
- untargeted actions search the larger action-message responder chain

For reversing, that means:
- do not flatten one event-path hook into proof of later action ownership
- do not assume the same receiver that sees the event must be the action receiver
- keep event-routing truth and action-routing truth separate until one durable consumer is frozen

### E. `targetForAction:` is often the best runtime recovery surface for ambiguous nil-target cases
Apple’s retained `NSResponder` material preserves that `targetForAction:` can find the recipient of an untargeted action without actually sending it.

For reversing, that means:
- if many responders share the same selector, hook or log `targetForAction:` and `sendAction:to:from:` together
- preserve `selector + sender + resolved target + key/main-window state + first-responder state`
- that bundle is usually a stronger artifact than raw class-name guesses from the binary alone

### F. Exact receiver truth is still weaker than first durable consumer truth
Apple’s target/action material makes clear that action methods receive the sender and may query it for details.
That is useful, but it also means the first receiver can still be adaptation or coordination glue.

For reversing, that means:
- do not freeze the map at the first object that receives the selector if it only validates, forwards, or chooses a later worker/document path
- keep going until one receiver writes durable state, changes mode, or enqueues the next meaningful work item

## 5. Default workflow

### Step 1: choose one event/action family with a visible late effect
Good candidates:
- one button or menu action tied to a visible mode change
- one keyboard-driven command tied to document/model mutation
- one control action tied to a request, worker enqueue, or later policy branch

Bad candidates:
- generic app-global events chosen only because `sendEvent:` is easy to hook
- selectors chosen only because they look semantically pretty but have no visible later effect

### Step 2: separate event routing from action emission
Write the smallest honest chain first:

```text
one NSEvent family
  -> one `sendEvent:` / window / responder reduction boundary
  -> one action-emission boundary (`sendAction...`) if the case is command-shaped
```

If you cannot distinguish those two layers yet, you are still too early to reason about target/action ownership.

### Step 3: freeze direct-target vs nil-target truth
Ask explicitly:
- is the target non-`nil` and fixed?
- or is the receiver resolved dynamically through the current responder chain?
- what were the key window, main window, and first responder in the run that matters?
- which delegate objects were eligible?

If the target is `nil`, do not skip this step.
That is usually the real liar.

### Step 4: recover the exact receiver before narrating ownership
Prefer one concrete artifact bundle:
- selector
- sender
- resolved target / receiver
- key-window / main-window state
- first responder

Minimal practical probes that work well here:
- breakpoint/log `-[NSApplication sendAction:to:from:]`
- breakpoint/log `targetForAction:` in nil-target cases
- compare runs with focus/window state intentionally changed
- breakpoint on the first receiver plus one downstream state write or enqueue

### Step 5: stop at the first durable consumer, then hand off
Rewrite the chain as:

```text
event family
  -> action emission
  -> receiver resolution
  -> first durable consumer
  -> downstream effect
```

Once that is stable, leave this note.
If the consumer only enqueues later work, route downstream to runtime-evidence, reverse-causality, or a broader async-delivery note.

## 6. Practical scenario patterns

### Pattern 1: `sendEvent:` is easy to hook, but the real work begins at `sendAction`
Symptoms:
- a custom `NSApplication` subclass or global hook is obvious
- `sendEvent:` mostly forwards normal behavior
- the interesting change only happens once a control or menu emits an action

Best move:
- treat `sendEvent:` as framework reduction
- freeze the first `sendAction:to:from:` boundary
- then recover the real receiver and first durable consumer

### Pattern 2: Nil-target menu or control action with several plausible receivers
Symptoms:
- target is `nil`
- many responders implement the selector or a selector with the same semantic name
- visible receiver candidates include views, window controllers, documents, delegates, or the app object

Best move:
- recover `targetForAction:` / `sendAction` resolution under the real key/main-window state
- preserve first-responder truth explicitly
- stop only when one concrete receiver actually changes behavior

### Pattern 3: Same selector name, different receiver depending on focus drift
Symptoms:
- compare pairs show the same selector but later behavior differs
- one run involves a different active panel/window or different first responder
- the selector may be standard (`cut:`, `copy:`, `paste:`, `saveDocument:`) or app-specific

Best move:
- freeze key-window, main-window, and first-responder state in both runs
- do not narrate “same selector == same receiver” by default
- prove the actual receiver before reopening deeper logic

### Pattern 4: First receiver exists, but the durable consumer is one hop later
Symptoms:
- the resolved target is easy to recover
- that object mainly validates input, forwards to a controller/document, or chooses a later worker/request path
- the real consequence happens after one narrow handoff

Best move:
- keep the resolved receiver as receiver truth
- continue until one write, mode change, or enqueue makes the action behaviorally real
- then hand off downstream instead of widening responder-chain narration again

## 7. Handoff rule
Leave this note once the main uncertainty is no longer “which AppKit action receiver first matters?”

Common next steps:
- move to `topics/causal-write-and-reverse-causality-localization-workflow-note.md` when one AppKit consumer is already known and the remaining gap is the first decisive write/reducer behind a later effect
- move to `topics/runtime-behavior-recovery.md` when the real need becomes broader compare-run design, observability, or runtime evidence strategy
- move back outward to `topics/native-gui-message-pump-and-signal-slot-first-consumer-workflow-note.md` when the case broadens back into mixed GUI/event-framework routing rather than specific responder-chain resolution
- move back outward to `topics/native-callback-registration-to-event-loop-consumer-workflow-note.md` when the case is no longer really AppKit action-routing shaped and instead becomes a broader async-delivery problem

## 8. Failure modes this note helps prevent
- stopping at `sendEvent:` because it is global and early
- treating `target == nil` as vague class-level folklore instead of current responder-chain search
- assuming selector-name visibility proves receiver truth
- forgetting that key-window / main-window / first-responder state can change the winning receiver
- confusing sender visibility with consumer truth
- stopping at the first receiver that merely forwards or validates instead of the first receiver that changes behavior

## 9. Compact operator checklist
- Pick one event or action family only.
- Separate event-routing truth from action-emission truth.
- Decide whether the target is explicit or dynamically resolved.
- In nil-target cases, freeze key-window, main-window, first-responder, and delegate state.
- Prefer `sendAction:to:from:` / `targetForAction:` over selector-name guessing when receiver ownership is still ambiguous.
- Treat selector visibility as candidate-set truth first, not consumer truth.
- Stop at the first durable write, mode change, task enqueue, or policy choice.
- Hand off downstream once the AppKit routing question is solved.

## 10. Topic summary
AppKit target/action cases are easy to overread from global hooks, pretty selector names, or vague responder-chain lore.

The practical cure is to keep five boundaries separate:
- event routing
- action emission
- target resolution
- exact receiver truth
- first durable consumer truth

That keeps `sendEvent:` visibility, selector names, and nil-target folklore from impersonating real behavior ownership.
