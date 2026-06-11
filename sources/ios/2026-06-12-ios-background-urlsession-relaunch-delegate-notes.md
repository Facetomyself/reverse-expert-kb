# 2026-06-12 — iOS Background URLSession Relaunch / Delegate / Completion Notes

## Scope
Source-backed notes for a practical iOS reversing seam: background `URLSession` transfers where task creation, daemon-owned transfer progress, app relaunch, delegate-event drain, completion-handler call, and later app-owned effect are easy to flatten into one vague "background request happened" claim.

## Sources consulted
- Apple Developer Documentation, `UIApplicationDelegate.application(_:handleEventsForBackgroundURLSession:completionHandler:)` — https://developer.apple.com/documentation/UIKit/UIApplicationDelegate/application%28_:handleEventsForBackgroundURLSession:completionHandler:%29
- Apple Developer Documentation, `URLSessionDelegate.urlSessionDidFinishEvents(forBackgroundURLSession:)` — https://developer.apple.com/documentation/foundation/urlsessiondelegate/urlsessiondidfinishevents(forbackgroundurlsession:)
- Apple Developer Documentation, `Downloading files in the background` — https://developer.apple.com/documentation/foundation/downloading-files-in-the-background
- Apple Developer Documentation mirror, `URLSessionConfiguration.sessionSendsLaunchEvents` — https://apple-docs.everest.mt/docs/foundation/urlsessionconfiguration/sessionsendslaunchevents/
- Apple Developer Forums, `handleEventsForBackgroundURLSession...` thread — https://developer.apple.com/forums/thread/69825
- Apple Developer Forums, `NSURLSession background download...` thread — https://developer.apple.com/forums/thread/71401
- Stack Overflow, `handleEventsForBackgroundURLSession never get called...` — https://stackoverflow.com/questions/27933082/handleeventsforbackgroundurlsession-never-get-called-ios7-background-transfer
- Cloudinary iOS issue, `Hook for receiving background URLSession events queued for app...` — https://github.com/cloudinary/cloudinary_ios/issues/327

## Source-backed reminders
- Apple's background-transfer model separates request/task creation from later app relaunch. A background session can continue transfer work while the app is suspended or terminated, and iOS may relaunch the app to deliver queued events.
- `application(_:handleEventsForBackgroundURLSession:completionHandler:)` is app-delegate relaunch/reattachment truth. It provides a session identifier and a completion handler that the app must retain and call after the session's queued events have been delivered.
- `urlSessionDidFinishEvents(forBackgroundURLSession:)` is delegate-drain truth: the URL session tells the delegate that all messages enqueued for the background session have been delivered. That is still weaker than proving the app called the stored completion handler, updated state, parsed a file, or triggered the behavior being analyzed.
- `sessionSendsLaunchEvents` changes whether launch events are delivered for a background session. Identifier/configuration truth therefore matters before treating missing relaunch callbacks as evidence against transfer completion.
- Background sessions use delegate-style delivery rather than simple closure/completion-handler ownership in many practical cases. Reversing only callsites that create data/download/upload tasks can miss the later consumer that runs after relaunch.
- Developer-forum and issue traces show common implementation confusion: recreate the background session with the same identifier after relaunch, store the app-delegate completion handler, wait for session delegate event drain, then call the stored handler. These traces are useful as implementation-shape evidence, not as normative authority beyond Apple docs.

## Practical proof ladder
```text
background task created
  != system/daemon accepted and progressed transfer
  != app relaunched for the same session identifier
  != queued delegate events delivered
  != app called the stored completion handler
  != app parsed/consumed the result or produced a durable effect
```

## Operator cues
- Preserve the background-session identifier. It is the bridge between setup-time `URLSessionConfiguration.background(withIdentifier:)`, relaunch callback, recreated session, and delegate event delivery.
- Treat `handleEventsForBackgroundURLSession` as reattachment/launch-event evidence, not as task-result consumption proof.
- Treat `urlSessionDidFinishEvents(forBackgroundURLSession:)` as "events delivered to delegate" evidence, not as UI state, parser state, request-signing state, or downloaded-file use.
- If `sessionSendsLaunchEvents` is false or the wrong identifier/configuration is recreated, a no-callback run may be configuration-shaped rather than target-behavior-shaped.
- For uploads/downloads, separate transfer availability from app-owned file move, parse/decrypt, database update, retry decision, notification display, or next request.

## KB integration target
Add a new iOS practical workflow note and route it from the iOS subtree guide and mobile parent page. Keep it adjacent to, but narrower than, generic URL-loading interception and Swift-concurrency continuation notes.
