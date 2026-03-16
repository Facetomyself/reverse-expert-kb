# Run Report — 2026-03-16 09:00 — WebView native→page response handoff hardening

## 1. Scope this run
This run deliberately stayed inside an existing concrete hybrid-app workflow branch instead of expanding the KB with another abstract parent page.

The practical target was:
- `topics/webview-native-response-handoff-and-page-consumption-workflow-note.md`

The reason for choosing it was straightforward:
- the KB already had hybrid ownership diagnosis and page→native bridge-payload recovery
- it also already had a native→page return-path note
- but that note still benefited from a tighter, more operator-useful hardening pass around lifecycle timing, callback-wrapper interpretation, and cheap page-consumption confirmation surfaces

Files reviewed at the start included:
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- `topics/webview-native-response-handoff-and-page-consumption-workflow-note.md`
- `topics/webview-native-bridge-payload-recovery-workflow-note.md`
- `topics/mobile-protected-runtime-subtree-guide.md`
- `sources/mobile-runtime-instrumentation/2026-03-15-webview-native-response-handoff-notes.md`
- recent run reports under `runs/`

## 2. New findings
### A. The note needed lifecycle-aware failure diagnosis, not a new taxonomy page
The strongest gap was not missing classification.
It was a missing practical question:

```text
if the native payload looks right, is the problem actually wrong data,
or is it wrong lifecycle timing / reload-reinit / missing listener registration?
```

That is a concrete investigation question analysts hit in real hybrid cases.
It is more valuable than another broad communication taxonomy.

### B. `evaluateJavascript(...)` remains a strong anchor, but timing needs more explicit treatment
Fresh source refreshes reinforced a practical pattern:
- native→page emission via `evaluateJavascript(...)` is often easy to recognize and hook
- but apparently “correct” emissions can still fail to advance behavior because the page-side consumer is not yet registered, the route is not mounted, or the page is reloading/reinitializing

This means the workflow note now needs to push analysts to test:
- payload correctness
- first meaningful consumer
- lifecycle moment

rather than assuming payload corruption first.

### C. JSON-wrapped callback returns are a real compare-run pitfall
Fresh implementation material again showed that callback-return material can be JSON-wrapped at the transport boundary.

That matters practically because analysts can otherwise:
- diff transport wrappers instead of semantic payloads
- over-read quoted strings / wrapper objects as meaningful changes
- misclassify an issue as token drift when it is mostly callback-format noise

The workflow note now calls this out explicitly.

### D. `WebChromeClient.onConsoleMessage(...)` is worth naming as a cheap secondary observation surface
This is not a full tracing method, but it is useful in exactly the kinds of cases this page is about:
- native emission is visible
- deep JS instrumentation is unstable or expensive
- the analyst needs quick evidence that the page actually received and acted on the emission

That makes console capture a practical corroboration surface, not just developer convenience.

### E. Reload / reinit loops deserve first-class mention in failure diagnosis
A recurring hybrid failure shape is:
- the same injection or callback pattern is visible repeatedly
- the analyst interprets this as token/path failure
- but the stronger explanation is that the page is reloading, remounting, or losing state before the decisive consumer path stabilizes

That now belongs explicitly in the note’s failure section.

## 3. Sources consulted
### Existing KB material
- `research/reverse-expert-kb/index.md`
- `topics/webview-native-response-handoff-and-page-consumption-workflow-note.md`
- `topics/webview-native-bridge-payload-recovery-workflow-note.md`
- `topics/mobile-protected-runtime-subtree-guide.md`
- `sources/mobile-runtime-instrumentation/2026-03-15-webview-native-response-handoff-notes.md`
- recent browser/mobile workflow pages for structural fit

### Fresh external source checks
- Android Developers `WebView` API reference
  - <https://developer.android.com/reference/android/webkit/WebView>
- Android Developers `WebMessagePort` API reference
  - <https://developer.android.com/reference/android/webkit/WebMessagePort>
- Android Developers insecure WebView native bridges guidance
  - <https://developer.android.com/privacy-and-security/risks/insecure-webview-native-bridges>
- Android Developers WebView / JavaScript debugging guidance
  - <https://developer.android.com/develop/ui/views/layout/webapps/debugging>
  - <https://developer.android.com/develop/ui/views/layout/webapps/debug-javascript-console-logs>
- OWASP MASTG WebView bridge testing page
  - <https://mas.owasp.org/MASTG/tests/android/MASVS-PLATFORM/MASTG-TEST-0033/>
- TechYourChance practical WebView communication article
  - <https://www.techyourchance.com/communication-webview-javascript-android/>
- search-layer result set around `evaluateJavascript`, `postWebMessage`, lifecycle timing, and console debugging

### Source-quality judgment
- strongest evidence this run came from official Android API / debugging references plus the already-existing KB structure
- OWASP MASTG stayed useful for bridge terminology and canonical object-bridge examples
- tutorial-style material was weaker than official docs, but useful because it exposed practical details directly relevant to workflow hardening: JSON-wrapped callback returns, `onPageFinished(...)` timing habits, and `WebChromeClient.onConsoleMessage(...)`
- Stack Overflow style results were treated as supporting practitioner evidence only, not primary proof

## 4. Reflections / synthesis
This run fit the human’s correction well.

The wrong move would have been:
- inventing a new hybrid WebView taxonomy page
- widening the branch while leaving a near-frontline workflow note only half-practical

The better move was:
- strengthen an existing note analysts could plausibly use mid-case
- make the note more diagnosis-oriented where real investigations commonly stall
- update the subtree guide and index so navigation reflects the hardened practical reading

A durable practical normalization from this run is:

```text
native result visible
  -> outbound native emission visible
  -> test lifecycle timing / wrapper normalization / reload-reinit effects
  -> localize first meaningful page consumer
  -> then route into request-finalization or another bridge round trip
```

That is exactly the kind of grounded tactic the KB needed more of.

## 5. Candidate topic pages to create or improve
### Improved this run
- `topics/webview-native-response-handoff-and-page-consumption-workflow-note.md`
- `topics/mobile-protected-runtime-subtree-guide.md`
- `index.md`

### Created this run
- `sources/mobile-runtime-instrumentation/2026-03-16-webview-native-response-handoff-hardening-notes.md`
- this run report

### Good next improvements
- improve `topics/webview-native-mixed-request-ownership-workflow-note.md`
  - add one short explicit subsection on when ownership appears native, but the decisive failure is still page reinit / page-side delayed consumption
- improve `topics/browser-request-finalization-backtrace-workflow-note.md`
  - add one cross-link sentence for hybrid cases where page request assembly only becomes visible after native reinjection succeeds
- improve `topics/webview-cookie-header-bootstrap-handoff-workflow-note.md`
  - make page reload/bootstrap refresh vs explicit callback return even more symmetric with the native→page note

## 6. Next-step research directions
1. Continue hardening existing hybrid/mobile workflow notes where the remaining gap is a missing diagnosis step rather than a missing category.
2. Look for more high-signal practitioner material around page-mount timing, SPA route reinitialization, and repeated WebView reinjection behavior in hybrid apps.
3. Strengthen the bridge between hybrid return-path notes and browser-side request-finalization notes, especially for cases where a native result only becomes meaningful after page-owned request helpers run.
4. Keep preferring concrete branch hardening over creating new abstract “communication framework” pages.

## 7. Concrete scenario notes or actionable tactics added this run
### Practical scenario normalized this run
**Native code visibly computes or retrieves the right result and visibly emits it back toward the page, but page behavior still does not advance in a stable way.**

### Concrete tactics added
- do not assume token corruption first when the outbound native emission looks right
- explicitly test three explanations separately:
  - wrong payload
  - wrong consumer
  - wrong lifecycle moment
- normalize callback-wrapper structure before compare-run diffing when using `evaluateJavascript(..., ValueCallback)`-style evidence
- use `WebChromeClient.onConsoleMessage(...)`-style console visibility as a cheap confirmation surface when deep JS instrumentation is unstable
- treat repeated reinjection / callback visibility without progress as a hint to inspect reload, remount, or bootstrap-state reset rather than only deeper token logic
- when page-side consumer localization succeeds, decide explicitly whether the next bottleneck is:
  - browser request finalization
  - another native round trip
  - or still a page-state / delayed-consumer issue

## 8. Errors / sync notes
### Error status
No major tooling failure occurred during the research/update phase.

### Local preservation status
Local KB progress preserved in:
- `topics/webview-native-response-handoff-and-page-consumption-workflow-note.md`
- `topics/mobile-protected-runtime-subtree-guide.md`
- `index.md`
- `sources/mobile-runtime-instrumentation/2026-03-16-webview-native-response-handoff-hardening-notes.md`
- this run report

### Git / sync handling note
The workspace already contained unrelated modifications outside the KB subtree.
To avoid mixing maintenance work, the commit after this run should stage only the KB files touched by this pass.

### Planned git / sync actions
After this report:
1. stage only the relevant reverse-expert-kb files updated this run
2. commit them from `/root/.openclaw/workspace`
3. run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
4. if sync fails, keep local preservation as success and record the failure briefly
