# Source notes — macOS NotificationCenter / DistributedNotificationCenter observer-consumer proof

Date: 2026-06-11 04:50 Asia/Shanghai
Scope: external research pass for a native/macOS practical workflow note around Foundation notification producer/observer/delivery/consumer separation.
Search artifact: `sources/native/2026-06-11-0450-macos-notificationcenter-search-layer.json`

## Sources consulted

- Apple Developer Documentation, `NotificationCenter` / `NSNotificationCenter` and `addObserver` pages surfaced by Exa/Tavily search:
  - https://developer.apple.com/documentation/foundation/notificationcenter
  - https://developer.apple.com/documentation/foundation/notificationcenter?language=objc
  - https://developer.apple.com/documentation/foundation/notificationcenter/addobserver(_:selector:name:object:)
  - https://developer.apple.com/documentation/foundation/notificationcenter/addobserver(forname:object:queue:using:)
- Apple archived Cocoa Notifications guide:
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/Notifications/Articles/Notifications.html
  - https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/Notifications/Articles/Registering.html
- Apple Developer Documentation, `DistributedNotificationCenter` / suspension behavior pages surfaced by Exa/Tavily:
  - https://developer.apple.com/documentation/foundation/distributednotificationcenter?language=objc
  - https://developer.apple.com/documentation/foundation/distributednotificationcenter/suspensionbehavior
  - https://developer.apple.com/documentation/foundation/distributednotificationcenter/addobserver(_:selector:name:object:suspensionbehavior:)
- Apple Developer Documentation, `CFNotificationCenterAddObserver` surfaced by Exa search:
  - https://developer.apple.com/documentation/corefoundation/cfnotificationcenteraddobserver(_:_:_:_:_:_:)
- NSHipster, `NSNotification & NSNotificationCenter`:
  - https://nshipster.com/nsnotification-and-nsnotificationcenter/
- Community/debugging signal only, not canonical authority:
  - https://apple.stackexchange.com/questions/468925/how-to-debug-distributed-notification-center
  - Stack Overflow result about distributed-notification suspension when app inactive
- Implementation/context pointers surfaced by Exa, used only as lower-confidence code-shape context:
  - GNUstep `NSNotificationCenter.m`
  - Apportable `NSNotificationCenter.m`
  - iOS Runtime Headers `NSNotificationCenter.h`

## Extracted source-backed facts

### Notification payload and decoupling
Apple’s archived Notifications guide describes notification as a broadcast model through `NSNotificationCenter` where:
- the poster does not need to know observers
- observers register with the notification center
- an `NSNotification` contains a `name`, an `object`, and optional dictionary / `userInfo`
- notification delivery can also be delayed/coalesced through a notification queue

Operator implication:
- a producer-side post and an observer-side effect are separate proof objects
- name/object/userInfo strings in a binary are not enough to prove either post or consumption
- `userInfo` fields should be treated as payload evidence until observer-side reads or effects are visible

### Local observer matching
Apple’s registration guide states local registration uses `addObserver:selector:name:object:` with observer, selector, notification name, and object filters.
It also notes:
- name and object are optional filters
- specifying only object receives notifications containing that object
- specifying only name receives that notification whenever posted regardless of object
- an observer can register to receive more than one message for the same notification
- the order of multiple messages for the same notification cannot be determined
- observers can be removed with `removeObserver:` or `removeObserver:name:object:`

Operator implication:
- registration is only eligibility truth
- name-only matches are weaker than name+object matches
- duplicate/multiple observer paths mean a single notification can fan out to several selector/block entries
- observer lifetime/removal must be checked at post time

### Block observers and queue truth
Apple Developer Documentation / search snippets preserve `addObserver(forName:object:queue:using:)` as a block-observer API with an `OperationQueue?` argument where the block runs.
NSHipster adds practical context that block registration returns an observer object needed for removal, while selector registration uses an existing observer and selector.

Operator implication:
- block token identity/lifetime and queue selection are separate from name/object match truth
- queue-mediated delivery can break naive producer-call-stack reasoning
- nil queue / current-thread behavior should not be assumed equivalent to a specific OperationQueue without runtime proof

### Distributed notifications
Apple’s registration guide and `NSDistributedNotificationCenter` docs preserve a separate cross-process model:
- observers register on a distributed notification center
- `object` is an identifying string because arbitrary object pointers cannot cross process boundaries
- suspension behavior controls what happens while delivery is suspended
- `NSApplication` may automatically suspend delivery when not active
- options such as deliver-immediately and post-to-all-sessions can change delivery posture

Operator implication:
- a distributed notification post is not target-process consumption proof
- sender-side name/string/object visibility must be paired with target-side registration and delivery evidence
- inactive/suspended state, coalescing/drop behavior, and options can decide whether a target callback ever fires

## Practical synthesis

The practical seam is:

```text
notification name visible
  != producer posted this event
  != one live observer matched name/object filters
  != delivery occurred under queue/coalescing/suspension rules
  != selector/block entered with the received payload
  != observer-owned state/task/effect occurred
```

For distributed notifications:

```text
posted cross-process
  != object-string/session matched
  != not dropped/coalesced/suspended
  != target process observer entered
  != app-owned effect
```

The new KB page should therefore bias operators toward pairing producer hooks with observer hooks and stopping at the first durable observer-owned consumer, not at notification-name discovery.

## Useful hook/breakpoint surfaces

- `-[NSNotificationCenter postNotificationName:object:userInfo:]`
- `-[NSNotificationCenter postNotification:]`
- Swift `NotificationCenter.default.post(name:object:userInfo:)`
- `-[NSNotificationCenter addObserver:selector:name:object:]`
- `-[NSNotificationCenter addObserverForName:object:queue:usingBlock:]` / Swift block API
- `-[NSNotificationCenter removeObserver:]`
- `-[NSDistributedNotificationCenter addObserver:selector:name:object:suspensionBehavior:]`
- `-[NSDistributedNotificationCenter postNotificationName:object:userInfo:options:]`
- `CFNotificationCenterAddObserver(...)`
- `CFNotificationCenterPostNotification(...)`
- first observer selector/block entry and first state write / task enqueue after entry

## Search audit summary

- Search sources requested: `exa,tavily,grok`
- Search sources succeeded: `exa,tavily`
- Search sources failed: `grok` returned HTTP 502 through the configured completions proxy for all three queries
- Exa endpoint observed in search-layer output: `http://158.178.236.241:7860/search`
- Tavily endpoint observed in search-layer output: `http://proxy.zhangxuemin.work:9874/api/search`
- Grok endpoint observed in error: `http://proxy.zhangxuemin.work:8000/v1/chat/completions`
