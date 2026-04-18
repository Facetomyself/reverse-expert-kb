# 2026-04-19 Cocoa responder-chain and target-action first-consumer notes

Date: 2026-04-19
Branch: native practical workflows
Seam: macOS/AppKit cases where `NSApplication sendEvent:`, `NSControl sendAction:to:`, `NSApplication sendAction:to:from:`, selector names, and responder-chain activity are all visible, but the first behavior-changing consumer is still ambiguous
Related canonical pages:
- `topics/native-gui-message-pump-and-signal-slot-first-consumer-workflow-note.md`
- `topics/native-cocoa-responder-chain-and-target-action-first-consumer-workflow-note.md`
- `topics/native-practical-subtree-guide.md`
- `topics/native-binary-reversing-baseline.md`

## Research intent
Tighten the native/macOS GUI branch around a thinner liar that was already visible in branch memory but still lacked a dedicated workflow note:
- event-loop / `sendEvent:` visibility
- control or menu action emission truth
- explicit-target vs nil-target resolution truth
- exact responder / receiver truth under the current key/main-window and first-responder state
- first durable write / mode change / task-enqueue consumer truth

The goal is not a broad Cocoa tutorial page.
The goal is a reusable stop rule for reverse work when analysts can already see AppKit event plumbing and selector names but still risk flattening them into a fake “found the consumer” story.

## Search artifact
Raw multi-source search artifact:
- `sources/native/2026-04-19-0450-cocoa-responder-target-action-search-layer.txt`

Requested source set:
- `exa,tavily,grok`

Observed search-source reality for this run:
- Exa returned usable Apple Developer and Apple archive surfaces for `NSResponder`, `sendEvent:`, `sendAction`, target/action, and event-loop material
- Tavily returned usable Apple Developer results and snippets around the same AppKit surfaces
- Grok was explicitly invoked and failed with repeated `502 Bad Gateway` errors through the configured proxy path

## Retained sources
1. Apple Developer archive — `Target-Action`
   - <https://developer.apple.com/library/archive/documentation/General/Conceptual/CocoaEncyclopedia/Target-Action/Target-Action.html>
2. Apple Developer archive — `Event Architecture`
   - <https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/EventOverview/EventArchitecture/EventArchitecture.html>
3. Apple Developer archive — `Main event loop`
   - <https://developer.apple.com/library/archive/documentation/General/Devpedia-CocoaApp-MOSX/MainEventLoop.html>
4. Legacy AppKit reference mirror — `NSResponder`
   - <https://preterhuman.net/macstuff/techpubs/macosx/System/Library/Frameworks/AppKit.framework/Versions/C/Resources/English.lproj/Documentation/Reference/ObjC_classic/Classes/NSResponder.html>
5. Legacy AppKit reference mirror — `NSControl`
   - <https://preterhuman.net/macstuff/techpubs/macosx/System/Library/Frameworks/AppKit.framework/Versions/C/Resources/English.lproj/Documentation/Reference/ObjC_classic/Classes/NSControl.html>
6. Search-layer surfaced Apple Developer entries/snippets for:
   - `NSResponder`
   - `NSApplication sendEvent(_:)`
   - `NSApplication sendAction(_:to:from:)`
   - `NSControl sendAction(_:to:)`

Practical note on evidence quality:
- modern Apple documentation pages were surfaced reliably by search, but direct text extraction was thin for several pages
- retained exact wording in this note therefore leans mainly on Apple archive/classic reference material plus the search-result snippets from official Apple pages
- claims below are kept conservative to match that evidence quality

## High-signal retained findings

### 1. Main-event-loop and `sendEvent:` visibility are framework reduction first
Apple’s event-architecture and main-event-loop documentation preserves the broad delivery ladder:
- the app object pulls the next event from the queue
- converts it into an `NSEvent`
- dispatches it with `sendEvent:`
- usually forwards toward the relevant `NSWindow`
- then toward the view or first responder that should handle it

Practical consequence:
- `NSApplication`, `run`, `nextEventMatchingMask:...`, and `sendEvent:` are strong reduction boundaries
- but they are still weaker than one actual action-emission or behavior-changing receiver
- `sendEvent:` should only be treated as the truthful first consumer if it itself suppresses, rewrites, retargets, or policy-gates the path

### 2. `NSControl sendAction:to:` is the action-emission boundary, not yet the final owner
Apple’s AppKit material preserves that `NSControl` handles user events, then uses `sendAction:to:` to send an action message to the control’s target, and that this method asks `NSApplication` / `NSApp` to perform the delivery.

Practical consequence:
- control hit / mouse-down truth is weaker than action-emission truth
- action-emission truth is weaker than exact receiver truth
- `-[NSApplication sendAction:to:from:]` is often the smallest practical place to freeze selector, target, and sender together before broader receiver guessing

### 3. Nil target is a search problem, not a broadcast fact
Apple’s target/action documentation preserves the key practical rule:
- when a control or cell target is `nil`, the application resolves the receiver at runtime instead of delivering to one pre-fixed object
- the prescribed order starts with the first responder in the key window, walks the responder chain to the window and its delegate, then may fall back to the main window and finally the application object and its delegate

Practical consequence:
- `target == nil` is not “any matching class could handle this”
- the receiver depends on current key-window, main-window, first-responder, and delegate state
- selector-name visibility alone is weaker than current resolution truth

### 4. The responder chain for action messages is larger than one window-local path
The retained `NSResponder` material preserves that action messages do not follow the same narrow path as ordinary event messages.
For untargeted actions, the full practical chain includes:
- key-window first responder and its successors
- key window
- key-window delegate
- main-window first responder and its successors
- main window
- main-window delegate
- `NSApp`
- app delegate

Practical consequence:
- the first receiver can move when focus, key/main-window state, or delegate composition changes
- identical selectors implemented in several responders are not equivalent proofs
- compare pairs that change focus or window ordering can silently change the receiver without changing the selector string at all

### 5. `sendAction` direct-target truth and nil-target truth are different proof objects
The retained `NSResponder` documentation also preserves a smaller but important split:
- if the target is not `nil`, the action is sent directly to that object
- if the target is `nil`, `sendAction:to:from:` searches for an object that implements the action method
- `targetForAction:` can be used to recover the recipient of an untargeted action without actually sending the message

Practical consequence:
- do not narrate an action path until you know whether the case is direct-targeted or dynamically resolved
- in nil-target cases, `targetForAction:` / `sendAction:to:from:` is often the most honest recovery surface
- in direct-target cases, target identity is still weaker than first durable consumer truth if the receiver mostly forwards or delegates again

### 6. Selector visibility is still weaker than behavior ownership
Apple’s target/action and responder documentation keeps one final practical distinction intact:
- the action method name defines a command shape
- the sender is passed so the receiver can query details
- the receiver that matters is the one that actually changes state, mode, policy, or downstream work

Practical consequence:
- one visible selector such as `saveDocument:`, `cut:`, or an app-specific action name is still only candidate-set truth
- the truthful consumer is the first receiver that performs a durable write, chooses a later route, or enqueues real work
- sender visibility is useful, but `sender` is not automatically the consumer

## Practical synthesis worth preserving canonically
A compact stop-rule ladder for this seam is:

```text
NSEvent queued / sendEvent visible
  != control or menu item emitted action
  != explicit target or nil-target resolution truth
  != exact receiver on the current responder chain
  != first durable write / mode change / task enqueue
  != later visible consequence truth
```

A smaller action-shaped memory worth preserving is:

```text
selector name visible
  != current responder chain will accept it
  != targetForAction / sendAction receiver truth
  != first behavior-changing consumer
```

That keeps five different wins separate:
1. **framework routing truth**
   - the event reached AppKit and a concrete `sendEvent:` / window / view boundary is real
2. **action-emission truth**
   - a control or menu item actually formed and emitted the action message
3. **resolution truth**
   - the receiver is either explicit or dynamically resolved through the current responder chain
4. **receiver truth**
   - one exact object on the current path actually received the selector
5. **consumer truth**
   - one receiver performed the first durable write, mode change, task enqueue, or policy choice that predicts later behavior

## Best KB use of this material
This material is best used as a dedicated thinner continuation under the native GUI workflow note.
It should not become a broad Cocoa architecture or AppKit tutorial page.

The operator-facing value is:
- do not stop at `sendEvent:` by default
- do not treat `target == nil` as vague receiver folklore; recover the current resolution path
- use `sendAction:to:from:` / `targetForAction:` as practical recovery surfaces when selector visibility alone is too weak
- freeze key-window / main-window / first-responder state before narrating receiver ownership
- stop only once one receiver actually changes behavior rather than merely receiving or forwarding the selector

## Search reliability note
This was a degraded-source external pass, not a fully healthy tri-source result set.
It still counts as a real external-research attempt because `exa,tavily,grok` were explicitly requested and Grok was actually invoked; its failure is recorded clearly.
