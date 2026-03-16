# Run Report — 2026-03-16 14:00 — Document-start listener-first WebView pass

## 1. Scope this run
This run stayed inside the active hybrid WebView/mobile branch and deliberately avoided creating any new abstract parent page.

The practical target was a specific timing failure that still deserved tighter treatment:
- native emission is visible
- bridge exposure may also be visible
- but the decisive page-side consumer still misses the first useful message or callback because listener/port registration happened too late
- SPA-style route remounts or coarse `onPageFinished` reasoning make the case look like payload corruption instead of timing drift

Primary files reviewed before editing:
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- `topics/webview-native-response-handoff-and-page-consumption-workflow-note.md`
- recent run reports under `runs/`
- `sources/mobile-runtime-instrumentation/2026-03-16-webview-bridge-visibility-and-page-consumer-timing-notes.md`

## 2. New findings
### A. "Bridge visible" and "listener ready early enough" are different diagnosis questions
The most useful practical finding hardened this run is:

```text
bridge visible
  or native emission visible
  != first meaningful page listener / port / route-local consumer was ready in time
```

That distinction is more operationally useful than widening the hybrid taxonomy again.

### B. Document-start vs late-observer placement is a valuable compare-run axis
A concrete diagnosis pattern added this run:
- if an accepted-like run only works when page-side observation or message-listener coverage exists earlier than in the failed run,
- then late hook placement can create a false impression that payload shape or bridge choice is the problem

This is especially useful in hybrid cases where the first meaningful consumer exists before later route or callback setup is visible from coarse page-load anchors.

### C. `onPageFinished` is too coarse for some SPA-like hybrid cases
This run hardened the practical rule that WebView-level load completion is not the same thing as route-local consumer readiness.

Useful operator consequence:
- if route remounts occur after the last visible page-load event,
- then native emission can be correct while the first useful page-side consumer still does not exist yet

### D. Message-port paths can fail only on the first useful message
A valuable practical scenario normalized this run:

```text
port created
  -> port handed to page
  -> page listener attaches too late
  -> first meaningful message lost
  -> later traffic looks normal
```

That is a better explanation than immediately blaming malformed payloads.

## 3. Sources consulted
### Existing KB material
- `research/reverse-expert-kb/index.md`
- `topics/webview-native-response-handoff-and-page-consumption-workflow-note.md`
- recent run reports under `runs/`

### Existing source notes used this run
- `sources/mobile-runtime-instrumentation/2026-03-16-webview-bridge-visibility-and-page-consumer-timing-notes.md`

### Fresh external sources
- AndroidX WebKit release notes
  - <https://developer.android.com/jetpack/androidx/releases/webkit>
- Android `WebMessagePort` API reference
  - <https://developer.android.com/reference/android/webkit/WebMessagePort>
- Android Developers native-bridge security guidance
  - <https://developer.android.com/privacy-and-security/risks/insecure-webview-native-bridges>
- CommonsWare on HTML message channels
  - <https://commonsware.com/blog/2017/01/23/replacing-addjavascriptinterface-html-message-channels.html>
- recurrence/Q&A signals consulted conservatively:
  - <https://stackoverflow.com/questions/41753104/how-do-you-use-webmessageport-as-an-alternative-to-addjavascriptinterface>
  - <https://stackoverflow.com/questions/57692933/how-to-run-javascript-after-page-load-in-android-webview-for-single-page-appli>
  - <https://stackoverflow.com/questions/48986858/timing-of-evaluatejavascript-after-onpagefinished-in-webview-for-spa-navigati>

## 4. Reflections / synthesis
This run stayed aligned with the human correction.

The wrong move would have been:
- invent another hybrid timing framework page
- broaden the ontology
- restate existing structure without improving operator value

The better move was:
- strengthen one already-active workflow note
- add one compact source note centered on document-start/listener-first timing
- turn official WebView tooling signals into a practical compare-run tactic

A durable synthesis from this run is:

```text
if native emission looks correct,
do not ask only whether the bridge exists.

Also ask whether the meaningful page-side listener,
message port, or route-local consumer existed early enough
for the first useful emission to be received.
```

## 5. Candidate topic pages to create or improve
### Improved this run
- `topics/webview-native-response-handoff-and-page-consumption-workflow-note.md`
- `index.md`

### Created this run
- `sources/mobile-runtime-instrumentation/2026-03-16-document-start-listener-first-webview-notes.md`
- this run report

### Good next improvements
- `topics/webview-native-bridge-payload-recovery-workflow-note.md`
  - add one tiny scenario showing bridge payload recovery succeeding while the first useful return-path message is still missed by a late listener
- `topics/browser-request-finalization-backtrace-workflow-note.md`
  - add one short cross-link for cases where the first page-owned request appears only after listener-first timing is fixed
- `topics/webview-native-mixed-request-ownership-workflow-note.md`
  - add one sentence reminding analysts that ownership can be solved while listener timing remains the real bottleneck

## 6. Next-step research directions
1. Continue strengthening the hybrid WebView/mobile chain with tiny scenario patterns and compare-run templates instead of new abstract structure.
2. Look for stronger official or practitioner evidence on document-start injection and page-side listener ordering in modern AndroidX WebKit flows.
3. Add one miniature case around route-local callback replacement after SPA remount.
4. Keep favoring grounded observer-placement and request-effect diagnosis over generic communication overviews.

## 7. Concrete scenario notes or actionable tactics added this run
### Practical scenario normalized this run
**The bridge is visible and native emission is visible, but the app still fails because the first meaningful page-side listener, port, or route-local callback attached too late and missed the first useful message.**

### Concrete tactics added
- record `document-start observer present` separately from `bridge visible`
- record `listener/port registered` separately from `page load finished`
- treat `onPageFinished` as a coarse anchor, not proof of route-local readiness
- compare first useful native emission against first meaningful page consumer timing
- treat message-port first-message loss as a first-class diagnosis path before blaming payload semantics

## 8. Errors / sync notes
### Error status during research/edit pass
- `web_fetch` hit redirect-limit failures on several Android Developers pages.
- The run continued using search-layer result snippets, API/reference anchors, and direct fetch of the CommonsWare article where successful.

These did not block the KB edit pass.

### Local preservation status
Local KB progress preserved in:
- `topics/webview-native-response-handoff-and-page-consumption-workflow-note.md`
- `sources/mobile-runtime-instrumentation/2026-03-16-document-start-listener-first-webview-notes.md`
- `index.md`
- this run report

### Git / sync handling note
After this report:
1. stage only the touched reverse-expert-kb files
2. commit from `/root/.openclaw/workspace`
3. run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
4. if sync fails, preserve local progress and record the failure briefly
