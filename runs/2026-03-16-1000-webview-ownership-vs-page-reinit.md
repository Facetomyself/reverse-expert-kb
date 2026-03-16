# Run Report — 2026-03-16 10:00 — WebView ownership vs page reinit / page-consumption drift

## 1. Scope this run
This run stayed inside an existing concrete hybrid-app branch rather than creating another abstract topic page.

The practical target was the gap between three already-existing workflow notes:
- `topics/webview-native-mixed-request-ownership-workflow-note.md`
- `topics/webview-cookie-header-bootstrap-handoff-workflow-note.md`
- `topics/webview-native-response-handoff-and-page-consumption-workflow-note.md`

The specific problem addressed was:
- analysts can correctly prove native transport ownership
- they can correctly localize page-seeded cookie/header/bootstrap state entering native code
- but they may still keep deepening ownership or signing analysis even when the remaining divergence is actually page lifecycle timing, reload/reinit, stale bootstrap state, or later page-side consumption

Files reviewed at the start included:
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- the three hybrid workflow notes above
- `topics/browser-request-finalization-backtrace-workflow-note.md`
- `topics/mobile-protected-runtime-subtree-guide.md`
- `sources/mobile-runtime-instrumentation/2026-03-15-webview-native-mixed-request-ownership-notes.md`
- recent run reports under `runs/`

## 2. New findings
### A. Ownership can be solved while the case is still unsolved
The strongest practical finding this run is a hybrid diagnosis rule:

```text
intent owner known
  -> transport owner known
  -> first native consumer known
  -> case can still fail because page lifecycle / reload-reinit / native→page consequence is still wrong or mistimed
```

That is more useful than widening hybrid taxonomy again.
It turns an existing ownership note into a better mid-case operator aid.

### B. Chromium bridge behavior gives a real reason to keep lifecycle timing explicit
Fresh source review reinforced a practical lifecycle point that fits the KB’s recent direction well:
- Java bridge visibility is page-load-sensitive
- injected object changes are reflected only on the next page load
- frame/context structure matters

That does not mean every target literally hinges on `onPageFinished(...)`.
It does mean analysts should explicitly test whether the relevant page context, listener, route, or bridge visibility exists at the moment a native result is emitted or consumed.

### C. Cookie/bootstrap handoff and native→page return are often two halves of one real loop
A useful symmetry became clearer this run:

```text
page bootstrap / cookie / hidden state appears
  -> native reads or mirrors it
  -> native request path uses it
  -> native result comes back toward the page
  -> page must consume it at the right lifecycle moment
```

This is a better practical reading than treating those notes as unrelated micro-topics.

### D. Repeated reads or reinjections are ambiguous evidence
Repeated:
- `CookieManager.getCookie(...)` reads
- bootstrap/store reads
- `evaluateJavascript(...)` emissions

should not be over-read as proof that the cookie/token/bootstrap data itself is wrong.
They may instead indicate:
- reload/reinit loops
- route remounts
- wrong consumer-registration timing
- stale bootstrap snapshots

That failure family now deserves explicit treatment in the notes.

### E. Browser request-finalization can be the next hybrid boundary
Another useful connection hardened this run:
- sometimes the first meaningful page-owned request-finalization edge only becomes visible **after** native→page reinjection succeeds
- in those cases, browser-side request-finalization is the practical continuation of a mobile hybrid case, not a separate purely-browser topic

That is a structural/navigation improvement with real operator value.

## 3. Sources consulted
### Existing KB material
- `research/reverse-expert-kb/index.md`
- `topics/webview-native-mixed-request-ownership-workflow-note.md`
- `topics/webview-cookie-header-bootstrap-handoff-workflow-note.md`
- `topics/webview-native-response-handoff-and-page-consumption-workflow-note.md`
- `topics/browser-request-finalization-backtrace-workflow-note.md`
- `topics/mobile-protected-runtime-subtree-guide.md`
- `sources/mobile-runtime-instrumentation/2026-03-15-webview-native-mixed-request-ownership-notes.md`
- recent run reports under `runs/`

### Fresh external source checks
- Chromium Android WebView Java Bridge docs
  - <https://chromium.googlesource.com/chromium/src/+/master/android_webview/docs/java-bridge.md>
- TechYourChance WebView communication article
  - <https://www.techyourchance.com/communication-webview-javascript-android/>
- search-layer result set around:
  - `shouldInterceptRequest`
  - `evaluateJavascript`
  - `onPageFinished`
  - hybrid request interception / visibility

### Source-quality judgment
- strongest evidence this run came from the Chromium bridge documentation plus the already-existing KB workflow structure
- practical implementation material was useful because it reinforced concrete workflow points already becoming central in the KB: lifecycle timing, wrapper normalization, and cheap console-side confirmation
- raw search results were used mainly to confirm recurrence of the operator problem, not as strong normative evidence
- one `web_fetch` attempt to Android `WebViewClient` docs failed with redirect issues in this environment; that was recorded as a limitation, not forced into overconfident claims

## 4. Reflections / synthesis
This run matched the human’s correction well.

The wrong move would have been:
- inventing another hybrid communication framework page
- broadening taxonomy while a frontline workflow gap remained

The better move was:
- keep working inside an existing concrete branch
- strengthen the exact moment where real hybrid investigations often go wrong
- connect mobile hybrid ownership notes more explicitly to page lifecycle, native→page return, and browser request-finalization

A durable synthesis from this run is:

```text
ownership solved
  -> check page-seeded state freshness
  -> check native→page return timing
  -> check first meaningful page consumer / route mount / reload-reinit effects
  -> only then decide whether more signing or transport analysis is still justified
```

That is concrete enough to guide real cases and narrow enough to avoid re-abstracting the subtree.

## 5. Candidate topic pages to create or improve
### Improved this run
- `topics/webview-native-mixed-request-ownership-workflow-note.md`
- `topics/webview-cookie-header-bootstrap-handoff-workflow-note.md`
- `topics/browser-request-finalization-backtrace-workflow-note.md`
- `topics/mobile-protected-runtime-subtree-guide.md`
- `index.md`

### Created this run
- `sources/mobile-runtime-instrumentation/2026-03-16-webview-ownership-vs-page-reinit-notes.md`
- this run report

### Good next improvements
- improve `topics/webview-native-bridge-payload-recovery-workflow-note.md`
  - add one short explicit subsection on distinguishing structurally correct bridge payload capture from wrong lifecycle moment / wrong page consumer
- improve `topics/browser-request-finalization-backtrace-workflow-note.md`
  - add a dedicated miniature hybrid case example instead of only a short source-footprint note
- improve `topics/webview-native-response-handoff-and-page-consumption-workflow-note.md`
  - add one small compare-run template that explicitly records route mount / listener registration timing

## 6. Next-step research directions
1. Keep hardening existing hybrid notes around loop closure and lifecycle timing rather than creating new hybrid parent pages.
2. Look for stronger practitioner/community material on SPA route remounts, WebView reinjection loops, and delayed listener registration in hybrid mobile cases.
3. Improve the payload-recovery note so it clearly distinguishes bridge payload correctness from downstream consumer readiness.
4. Continue linking hybrid mobile notes to browser request-finalization only where there is a real boundary chain, not just topical overlap.

## 7. Concrete scenario notes or actionable tactics added this run
### Practical scenario normalized this run
**Native transport ownership is already proven, and page-seeded state is already localized, but behavior still diverges because the page is reloading, remounting, consuming stale bootstrap state, or missing the native result at the relevant lifecycle moment.**

### Concrete tactics added
- do not stop once intent owner and transport owner are known
- explicitly test whether the remaining divergence is page lifecycle timing rather than transport/signing failure
- compare when page state was seeded vs when native code consumed it
- treat repeated cookie/bootstrap reads and repeated native reinjection as ambiguous evidence that may indicate reload/reinit loops
- if the decisive page-owned request only becomes visible after native→page reinjection succeeds, route into browser request-finalization from that point rather than treating the case as “already solved”
- read cookie/bootstrap handoff and native→page return symmetrically when both halves are present in the same target loop

## 8. Errors / sync notes
### Error status
Minor external-tool limitation only:
- `web_fetch` against Android `WebViewClient` reference hit redirect limits in this environment
- no blocking failure occurred for the KB update itself

### Local preservation status
Local KB progress preserved in:
- `topics/webview-native-mixed-request-ownership-workflow-note.md`
- `topics/webview-cookie-header-bootstrap-handoff-workflow-note.md`
- `topics/browser-request-finalization-backtrace-workflow-note.md`
- `topics/mobile-protected-runtime-subtree-guide.md`
- `index.md`
- `sources/mobile-runtime-instrumentation/2026-03-16-webview-ownership-vs-page-reinit-notes.md`
- this run report

### Git / sync handling note
The workspace may contain unrelated modifications outside the KB subtree.
The post-run commit should therefore stage only the reverse-expert-kb files touched by this pass.

### Planned git / sync actions
After this report:
1. stage only the relevant reverse-expert-kb files updated this run
2. commit them from `/root/.openclaw/workspace`
3. run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
4. if sync fails, record the failure briefly while preserving local progress as success
