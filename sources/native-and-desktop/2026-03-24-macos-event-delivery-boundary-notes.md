# 2026-03-24 macOS event-delivery boundary notes

Date: 2026-03-24 07:16 Asia/Shanghai
Branch: native desktop practical subtree
Theme: macOS Cocoa / NSApplication / responder-chain / XPC / dispatch delivery boundary

## Why this note exists
This source pass was chosen as an anti-stagnation run on an underfed native-desktop seam.
Recent runs had already spent meaningful attention on iOS and Win32/Qt GUI ownership.
The practical gap left open inside native desktop was macOS event delivery, especially the analyst stop rule for when `NSApplication`, responder-chain routing, XPC proxy/object boundaries, or dispatch-source callbacks are visible but the first behavior-changing consumer is still not honestly proved.

## Search mode
Explicit multi-source search was attempted through `search-layer` with:
- `--source exa,tavily,grok`

Queries:
1. `macOS NSXPC XPC Mach service reverse engineering first consumer practical`
2. `Cocoa NSApplication sendEvent target action reverse engineering first meaningful consumer`
3. `macOS dispatch source runloop callback reverse engineering queued delivery practical`

Raw search artifact:
- `sources/native-and-desktop/2026-03-24-macos-event-delivery-search-layer.txt`

## Search-source result snapshot
Requested:
- exa
- tavily
- grok

Succeeded with retained results:
- exa
- tavily
- grok

Observed degradation:
- Grok emitted JSON-parse errors during the run, but still returned retained results for Apple dispatch/run-loop material.
- This should be treated as degraded-but-usable Grok participation rather than clean success.

Endpoints used on this host:
- Exa: `http://158.178.236.241:7860`
- Tavily: `http://proxy.zhangxuemin.work:9874/api`
- Grok: `http://proxy.zhangxuemin.work:8000/v1`

## Sources retained conservatively
Primary sources:
- Apple Cocoa Fundamentals / Core Application Architecture
- Apple Creating XPC Services
- Apple DispatchSourceProtocol / dispatch source docs
- CocoaDev note on overriding `NSApplication sendEvent:`

Supporting context sources:
- Mandiant introductory Cocoa reverse-engineering note
- SIMBL armchair Cocoa reverse-engineering guide
- practical XPC reversing / interception notes from security blogs (used conservatively, not as sole authority)

## Practical findings worth keeping

### 1. `NSApplication` visibility is still only framework reduction
Apple’s Cocoa architecture documentation makes the main event-loop shape clear:
- `NSApplicationMain` builds the singleton app object
- the main run loop receives events from a window-server-backed event source
- `run` repeatedly obtains the next event
- `sendEvent:` dispatches the event onward, usually toward an `NSWindow`, then deeper into responder-chain handling

Practical reversing implication:
- finding `NSApplication`, `run`, `nextEventMatchingMask:untilDate:inMode:dequeue:`, or `sendEvent:` is not yet consumer proof
- those landmarks are the Cocoa equivalent of framework reduction, not the final ownership answer

### 2. `sendEvent:` is an early interception boundary, not automatically the truthful consumer
The Cocoa material and long-lived CocoaDev guidance line up on one useful operator rule:
- `NSApplication sendEvent:` is the earliest app-side place where the program sees the event
- but in ordinary cases it still forwards normal processing onward
- the truthful consumer boundary often lives later in `NSWindow`, the first responder, a control action, or a target/action-resolver edge

Practical stop rule:
- do not stop at `sendEvent:` just because it is a pretty global hook
- only treat it as the first real consumer if it actually suppresses, rewrites, retargets, or policy-gates later behavior

### 3. Target/action and responder-chain routing should not be flattened into “GUI event handled”
Cocoa architecture material explicitly preserves that:
- events reach a window
- controls may emit action messages
- action dispatch may travel through target/action logic and the responder chain

Practical reversing implication:
- the first truthful consumer is often not raw event receipt but the first responder or target/action receiver that performs a durable write, mode change, task enqueue, or policy choice
- a visible selector name alone is still not enough if the responder-chain candidate set remains open

### 4. XPC proxy/object visibility is not yet behavior ownership
Apple’s XPC service documentation keeps a useful separation intact:
- the connection object and proxy shape provide the RPC surface
- the service-side exported object actually receives the method call
- the service may be relaunched on demand and may hold minimal state

Practical reversing implication:
- `NSXPCConnection` setup, proxy acquisition, or listener creation is still only ownership reduction
- the first behavior-changing consumer usually lives at the exported object method, reply block, or the next stateful reducer behind that method
- do not confuse the connection scaffold with the decisive service-side policy point

### 5. Dispatch-source visibility is not the same as first meaningful consequence
Apple dispatch-source documentation and run-loop/dispatch references support a smaller operator rule:
- a dispatch source makes an event family eligible for handling on a target queue
- that callback boundary is often only the delivery point
- the meaningful consumer may live one stage later in the parser, classifier, state reducer, or request builder invoked by that callback

Practical reversing implication:
- preserve the difference between event-source readiness, queue-delivered callback execution, and the first stateful reducer after callback entry
- do not stop at `dispatch_source_create` or the event handler registration when the callback itself is still only plumbing

## Practical operator rule to carry into the KB
For macOS desktop/event-heavy cases, preserve four boundaries explicitly:
1. event family (`NSEvent`, action, XPC message, dispatch-source readiness)
2. framework reduction (`NSApplication` / `sendEvent:` / responder-chain routing / XPC connection-to-exported-object / dispatch-source callback delivery)
3. first consequence-bearing consumer (first responder / target-action receiver / exported-object method / first stateful reducer after dispatch callback)
4. proof-of-effect boundary (UI change, task enqueue, reply emission, policy/state update)

## Concrete scenarios worth remembering
- If `sendEvent:` only forwards, it is framework reduction, not the truthful consumer.
- If a control action resolves through the responder chain, the real consumer may be the first receiver that changes state, not the control or selector name alone.
- If `NSXPCConnection` and proxy calls are visible, the decisive consumer is usually service-side exported-object logic or the first stateful reducer behind it.
- If a dispatch source fires on a queue, the callback is often only delivery proof; the next parser/classifier/reducer may be the first behavior-bearing consumer.

## KB-targeted takeaway
The macOS desktop branch should remember one stop rule that parallels the Win32/Qt refinement:
- do not stop at `NSApplication sendEvent:`, responder-chain visibility, XPC proxy setup, or dispatch-source registration as if those alone prove ownership
- classify whether they are merely framework reduction or the first actual behavior-changing consumer
- then preserve the earliest consumer that really predicts later behavior
