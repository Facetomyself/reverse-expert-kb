# Run Report — 2026-03-16 11:00 — WebView lifecycle-ready page-consumer pass

## 1. Scope this run
This run deliberately avoided creating another abstract topic page.

Instead, it tightened an existing concrete hybrid-app branch around one recurring practical failure:
- analysts recover the page→native handoff payload correctly
- analysts may even recover the native result correctly
- but the case still fails because the native→page return lands before the relevant page listener, route, or state consumer is ready

The main goal was to make the KB more actionable for this real mid-case diagnosis problem by improving existing workflow notes and navigation rather than expanding taxonomy.

Primary files reviewed before editing:
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- `topics/webview-native-bridge-payload-recovery-workflow-note.md`
- `topics/webview-native-response-handoff-and-page-consumption-workflow-note.md`
- `topics/mobile-response-consumer-localization-workflow-note.md`
- `topics/browser-request-finalization-backtrace-workflow-note.md`
- `topics/mobile-protected-runtime-subtree-guide.md`
- recent run reports under `runs/`

## 2. New findings
### A. Correct page→native payload is not enough
The most useful finding this run is a sharper operator rule for hybrid cases:

```text
correct page→native payload
  -> correct native consumer
  -> correct native result
  -> case can still fail because page listener / route / store consumer was not ready yet
```

That is materially better than widening the bridge taxonomy again.

### B. Lifecycle timing should be recorded as a first-class compare-run boundary
The practical compare-run structure that emerged is:

```text
native result produced at:
page listener registered at:
route mounted or remounted at:
reload / reinit observed at:
first meaningful page consumer fired at:
first request-driving effect at:
```

This is the concrete improvement added to the KB’s hybrid workflow branch.

### C. Official WebView material supports the lifecycle-readiness concern
The strongest external grounding this run came from official WebView bridge/reference material and Chromium bridge docs.
The conservative but useful takeaway is:
- bridge visibility and outbound emission are real but insufficient proof points
- page/frame/load timing still matters
- message-channel and callback-string return paths both have registration-order failure modes

### D. SPA/remount style drift belongs in hybrid diagnosis, not only frontend debugging
A useful structural synthesis this run:
- route remount / reload / page-state reset should now be treated as a hybrid reverse-engineering diagnosis problem when native→page return is visible but effect is missing
- this belongs inside the existing hybrid WebView workflow notes, not in a generic frontend note

## 3. Sources consulted
### Existing KB material
- `research/reverse-expert-kb/index.md`
- `topics/webview-native-bridge-payload-recovery-workflow-note.md`
- `topics/webview-native-response-handoff-and-page-consumption-workflow-note.md`
- `topics/mobile-response-consumer-localization-workflow-note.md`
- `topics/browser-request-finalization-backtrace-workflow-note.md`
- `topics/mobile-protected-runtime-subtree-guide.md`
- recent run reports under `runs/`

### Fresh external sources
- Chromium Android WebView Java Bridge docs
  - <https://chromium.googlesource.com/chromium/src/+/master/android_webview/docs/java-bridge.md>
- Android WebView reference
  - <https://developer.android.com/reference/android/webkit/WebView>
- AndroidX `WebViewCompat` reference
  - <https://developer.android.com/reference/androidx/webkit/WebViewCompat>
- Android native bridge risk note
  - <https://developer.android.com/privacy-and-security/risks/insecure-webview-native-bridges>
- TechYourChance WebView communication article
  - <https://www.techyourchance.com/communication-webview-javascript-android>
- InAppWebView communication docs
  - <https://inappwebview.dev/docs/webview/javascript/communication>
- React Native WebView SPA navigation issue
  - <https://github.com/react-native-webview/react-native-webview/issues/2667>
- StackOverflow recurrence signal on interface visibility / page update behavior
  - <https://stackoverflow.com/questions/79495428/android-webview-javascript-interface-being-removed-on-webforms-partial-postback>
- 42Gears note on `evaluateJavascript(...)` timing
  - <https://techblogs.42gears.com/inject-javascript-to-android-webview>

## 4. Reflections / synthesis
This run stayed aligned with the human’s correction.

The wrong move would have been:
- invent a new “hybrid lifecycle framework” page
- add another abstract parent layer
- widen ontology without improving frontline operator use

The better move was:
- strengthen two existing workflow notes
- add one source note with traceable provenance
- improve subtree/index navigation so the diagnosis is easier to find in context

A durable synthesis from this run is:

```text
if page→native payload looks correct
and native result looks correct
but behavior still diverges,
check lifecycle-ready page consumption before going deeper into payload decoding
```

That is narrow, practical, and cumulative.

## 5. Candidate topic pages to create or improve
### Improved this run
- `topics/webview-native-bridge-payload-recovery-workflow-note.md`
- `topics/webview-native-response-handoff-and-page-consumption-workflow-note.md`
- `topics/mobile-protected-runtime-subtree-guide.md`
- `index.md`

### Created this run
- `sources/mobile-runtime-instrumentation/2026-03-16-webview-lifecycle-ready-page-consumer-notes.md`
- this run report

### Good next improvements
- improve `topics/webview-cookie-header-bootstrap-handoff-workflow-note.md`
  - add one compact compare-run subsection distinguishing stale bootstrap handoff from later page-consumer timing failure
- improve `topics/browser-request-finalization-backtrace-workflow-note.md`
  - add a tiny hybrid case example where request-finalization only becomes visible after lifecycle-correct reinjection
- improve `topics/webview-native-response-handoff-and-page-consumption-workflow-note.md`
  - add one short scratch template for route-mount / listener-registration logging during compare runs

## 6. Next-step research directions
1. Keep tightening the hybrid WebView branch around concrete failure diagnosis instead of creating new parent pages.
2. Look for stronger practitioner evidence around WebView route remount, delayed listener registration, and message-channel ordering in hybrid mobile targets.
3. Extend the same lifecycle-ready diagnosis rule into cookie/bootstrap handoff notes where appropriate.
4. Keep linking hybrid native→page return to browser request-finalization only when there is a real downstream boundary chain.

## 7. Concrete scenario notes or actionable tactics added this run
### Practical scenario normalized this run
**The bridge payload and native result are both correct, but the hybrid case still fails because the page-side listener, route, or store consumer was not ready when the result returned.**

### Concrete tactics added
- compare accepted and failed runs at both the page→native handoff and later native→page return boundary
- record listener registration time, route mount/remount time, reload/reinit time, and first meaningful consumer time
- treat visible `evaluateJavascript(...)` or `postWebMessage(...)` output as proof of emission, not proof of successful consumption
- keep lifecycle timing as a first-class hypothesis before blaming payload corruption
- route from bridge-payload recovery into native→page return / page-consumer diagnosis when payload shape is already explained but behavior still diverges

## 8. Errors / sync notes
### Error status
No blocking research errors this run.

### Local preservation status
Local KB progress preserved in:
- `topics/webview-native-bridge-payload-recovery-workflow-note.md`
- `topics/webview-native-response-handoff-and-page-consumption-workflow-note.md`
- `topics/mobile-protected-runtime-subtree-guide.md`
- `index.md`
- `sources/mobile-runtime-instrumentation/2026-03-16-webview-lifecycle-ready-page-consumer-notes.md`
- this run report

### Git / sync handling note
After writing this report:
1. stage only the touched reverse-expert-kb files
2. commit from `/root/.openclaw/workspace`
3. run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
4. if sync fails, preserve local progress and record the failure briefly
