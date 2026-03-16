# Run Report — 2026-03-16 12:00 — WebView bootstrap freshness vs page-consumer timing

## 1. Scope this run
This run stayed deliberately inside the recently active hybrid WebView/mobile branch instead of creating any new abstract topic page.

The concrete target was a recurring practical confusion that still remained under-explained across recent notes:
- page-seeded cookie/header/bootstrap state is localized correctly
- native code appears to consume it correctly
- native transport or native result also looks broadly correct
- but the case still fails because either:
  - native code consumed a stale bootstrap snapshot, or
  - the later page-side consumer was not ready when native→page reinjection happened

The goal this run was to tighten that exact diagnosis boundary and connect it more explicitly to browser request-finalization, because in some hybrid cases the first meaningful page-owned request only appears after lifecycle-correct reinjection.

Primary files reviewed before editing:
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- `topics/webview-cookie-header-bootstrap-handoff-workflow-note.md`
- `topics/webview-native-response-handoff-and-page-consumption-workflow-note.md`
- `topics/browser-request-finalization-backtrace-workflow-note.md`
- `topics/webview-native-bridge-payload-recovery-workflow-note.md`
- `topics/mobile-protected-runtime-subtree-guide.md`
- recent run reports under `runs/`
- `sources/mobile-runtime-instrumentation/2026-03-15-webview-cookie-header-bootstrap-handoff-notes.md`

## 2. New findings
### A. Correct page-seeded handoff is still not enough
The strongest practical finding reinforced this run is:

```text
correct page-seeded cookie/bootstrap handoff
  -> correct native read
  -> seemingly correct native request/result
  -> case can still fail because the page-side consumer was late, remounted, or reading different bootstrap state
```

That is more useful than widening the hybrid taxonomy again.

### B. Stale bootstrap handoff and late page-consumer timing are easy to confuse
A useful operator split hardened this run:
- **stale handoff** = native code read the wrong or older page-seeded snapshot
- **late page consumption** = native use was fine, but the later page listener/route/store was not ready when native→page reinjection happened

Those two failure families can look similar if the analyst only watches repeated cookie reads or repeated reinjections.

### C. Browser request-finalization can be a downstream hybrid boundary, not a separate topic
A more explicit chain emerged:

```text
page-seeded bootstrap/cookie state
  -> native consumption
  -> native result / updated session state
  -> lifecycle-correct native→page reinjection
  -> first meaningful page-owned request-finalization edge
```

This means some browser request-finalization cases are really the continuation of a mobile hybrid diagnosis path.

### D. Compact compare-run structure is high-value here
The most actionable addition this run was not a new framework page but a compact compare-run template that records:
- page bootstrap seeded time
- first native read time
- native result return time
- page listener/route/store readiness time
- first meaningful page-owned effect time

That gives analysts a better chance of separating stale state from wrong lifecycle moment.

## 3. Sources consulted
### Existing KB material
- `research/reverse-expert-kb/index.md`
- `topics/webview-cookie-header-bootstrap-handoff-workflow-note.md`
- `topics/webview-native-response-handoff-and-page-consumption-workflow-note.md`
- `topics/browser-request-finalization-backtrace-workflow-note.md`
- `topics/webview-native-bridge-payload-recovery-workflow-note.md`
- `topics/mobile-protected-runtime-subtree-guide.md`
- recent run reports under `runs/`

### Existing source notes used this run
- `sources/mobile-runtime-instrumentation/2026-03-15-webview-cookie-header-bootstrap-handoff-notes.md`
- `sources/mobile-runtime-instrumentation/2026-03-16-webview-lifecycle-ready-page-consumer-notes.md`
- `sources/mobile-runtime-instrumentation/2026-03-16-webview-ownership-vs-page-reinit-notes.md`

### Fresh external sources
No new external source cluster was needed for this pass.
This run primarily consolidated already-grounded recent material into a tighter, more actionable workflow chain.

## 4. Reflections / synthesis
This run stayed aligned with the human’s correction.

The wrong move would have been:
- inventing another “hybrid state synchronization framework” page
- broadening the ontology
- repeating structure instead of improving operator value

The better move was:
- tighten an existing concrete workflow note
- add a direct compare-run template
- strengthen the connection between hybrid mobile reinjection timing and browser request-finalization

A durable synthesis from this run is:

```text
when cookie/bootstrap handoff looks correct,
do not stop there.

also verify:
  snapshot freshness at native read time
  native return timing
  page listener / route / store readiness
  first page-owned request-finalization edge after reinjection
```

That is grounded, cumulative, and much more useful than another abstract page.

## 5. Candidate topic pages to create or improve
### Improved this run
- `topics/webview-cookie-header-bootstrap-handoff-workflow-note.md`
- `topics/browser-request-finalization-backtrace-workflow-note.md`
- `topics/mobile-protected-runtime-subtree-guide.md`
- `index.md`

### Created this run
- this run report

### Good next improvements
- improve `topics/webview-native-response-handoff-and-page-consumption-workflow-note.md`
  - add one even shorter checklist for listener registration vs store readiness vs route remount
- improve `topics/webview-native-bridge-payload-recovery-workflow-note.md`
  - add one miniature example showing a structurally correct bridge payload that still fails because later page consumption was mistimed
- improve `topics/webview-cookie-header-bootstrap-handoff-workflow-note.md`
  - add one tiny scenario example where repeated `CookieManager.getCookie(...)` reads are actually evidence of a reload/reseed loop

## 6. Next-step research directions
1. Keep strengthening the hybrid WebView/mobile loop-closure branch through practical compare-run templates, not new parent pages.
2. Look for stronger practitioner evidence on stale bootstrap snapshots versus route-remount timing in hybrid mobile targets.
3. Continue hardening the bridge between mobile reinjection timing and browser request-finalization where real downstream request edges exist.
4. Prefer adding miniature case patterns and scratch templates over new abstract structure.

## 7. Concrete scenario notes or actionable tactics added this run
### Practical scenario normalized this run
**Page-seeded cookie/bootstrap state enters native code correctly, but the target still fails because either the native read used a stale snapshot or the later page-side consumer was not ready when the native result came back.**

### Concrete tactics added
- compare page bootstrap seed time against the first native read time
- compare native result return time against page listener / route / store readiness time
- do not treat repeated cookie/bootstrap reads as automatic proof that the state itself is wrong
- do not treat visible native reinjection as automatic proof that the page meaningfully consumed it
- if the first page-owned request appears only after successful reinjection, treat browser request-finalization as the next real boundary in the same hybrid case

## 8. Errors / sync notes
### Error status
No blocking research or sync-preparation errors during the KB edit pass itself.

### Local preservation status
Local KB progress preserved in:
- `topics/webview-cookie-header-bootstrap-handoff-workflow-note.md`
- `topics/browser-request-finalization-backtrace-workflow-note.md`
- `topics/mobile-protected-runtime-subtree-guide.md`
- `index.md`
- this run report

### Git / sync handling note
After this report:
1. stage only the touched reverse-expert-kb files
2. commit from `/root/.openclaw/workspace`
3. run `/root/.openclaw/workspace/scripts/sync-reverse-expert-kb.sh`
4. if sync fails, preserve local progress and record the failure briefly
