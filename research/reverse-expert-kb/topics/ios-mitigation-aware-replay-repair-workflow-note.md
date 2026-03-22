# iOS Mitigation-Aware Replay-Repair Workflow Note

Topic class: concrete workflow note
Ontology layers: mobile practical workflow, iOS mitigation-aware continuation, replay-close reduction
Maturity: practical
Related pages:
- topics/ios-practical-subtree-guide.md
- topics/arm64e-pac-and-mitigation-aware-ios-reversing.md
- topics/ios-pac-shaped-callback-and-dispatch-failure-triage.md
- topics/ios-block-callback-landing-and-signature-recovery-workflow-note.md
- topics/runtime-table-and-initialization-obligation-recovery-workflow-note.md
- topics/ios-result-callback-to-policy-state-workflow-note.md

## 1. Why this page exists
This page exists for a narrower recurring iOS stall pattern that the KB had already hinted at but had not yet turned into a dedicated operator note.

The branch already had:
- a broad mitigation-aware continuation for modern iOS PAC / arm64e cases
- a narrower callback/dispatch triage note for deciding whether one authenticated boundary is wrong-family, wrong-context, lying-code-view, or replay-close
- a broader runtime-table / initialization-obligation page for close-but-wrong replay across several platform families

What was still missing was the narrower continuation for this very specific case:
- one owner or callback family is already plausible enough that broad owner search should probably stop
- the landing boundary is already trustworthy enough, or at least reduced enough, that the real bottleneck is no longer callback-family choice alone
- replay is **close enough** that the remaining failure smells like one authenticated-context, materialization, initialized-image, or object-provenance gap
- modern iOS PAC / arm64e / dyld-cache truth still affects whether the remaining explanation is trustworthy

That gap matters because these cases often drift into two bad loops:
- reopening broad owner search even though the path is already reduced enough
- rewriting broad replay logic when the real missing proof is one smaller runtime obligation near an authenticated boundary

This page keeps that middle ground practical.

## 2. When to use this page
Use this page when most of the following are true:
- the case is already clearly iOS-shaped and mitigation-aware enough that PAC / arm64e / dyld-cache truth matters
- one owner path, callback family, or dispatch family is already plausible enough that broad owner search no longer looks cheapest
- one replay path, black-box invocation path, or reduced call path is already structurally close
- the remaining failure happens near one callback, indirect boundary, object materialization edge, or initialized-runtime dependency
- the immediate question is no longer just “which family is this?” but “what smaller context/materialization/init gap still makes this replay untruthful?”

Representative entry conditions:
- a callback family now looks right and lands where expected, but replay still crashes or diverges on-device
- a reduced invocation reaches the right code family, but one late boundary still behaves as though the object, context, or pointer materialization is not truthful yet
- static and runtime views now agree enough to stop arguing about the family, yet replay remains close-but-wrong around a cache-backed or arm64e-shaped edge
- a private-framework or dyld-cache-backed path is already reduced enough that the remaining uncertainty is one narrower runtime obligation, not broad target selection

Do **not** use this page when:
- the code view is still too untrustworthy to say whether the family is even right
- callback/block landing truth is still the real bottleneck
- the case is still mostly about broad owner choice rather than replay-close repair
- the problem is already clearly a generic runtime-table/init-obligation case with no special iOS mitigation-aware pressure left

In those cases, stay with the broader or earlier page first.

## 3. Core claim
When a modern iOS case is already replay-close, the next best move is often **not** broader tracing and **not** broader replay rewriting.
It is to classify the remaining gap conservatively as one smaller replay-repair object.

The key question is usually:

```text
Is this path still failing because the family is actually wrong,
or because the family is plausible but one authenticated context,
object materialization, initialized image, or narrower runtime obligation is still missing?
```

A practical continuation rule is:

```text
iOS case already reduced and replay-close
  -> freeze one representative replay failure boundary
  -> preserve one truthful runtime landing and one compare pair
  -> classify the remaining gap as family / context / code-view / missing-obligation
  -> bias toward the smallest still-missing object/materialization/init proof
  -> hand off quickly into a narrower replay-repair or downstream consequence page
```

The point is not to diagnose PAC internals precisely.
The point is to keep replay-close iOS work from reopening the whole case.

## 4. The four replay-close failure classes to separate explicitly

### A. Not actually replay-close after all
The family may still be wrong.
Common signals:
- target and non-target actions hit the same reduced path with no meaningful behavioral separation
- the chosen replay target is easy to invoke but does not predict the later effect
- the apparent “last failing edge” does not own the consequence you care about

What to preserve:
- one reason the family had looked plausible
- one compare pair showing it may still be the wrong family

### B. Right family, wrong authenticated context
The family is plausible, but the pointer/context/object provenance is still not truthful enough.
Common signals:
- replay reaches the right code family but dies or diverges sharply at an indirect/callback boundary
- object shape looks plausible, but invocation still smells context-wrong rather than target-wrong
- the remaining instability is late and narrow enough that broad owner reopening feels wasteful

What to preserve:
- one reason the family still looks right
- one reason the context/pointer/object provenance still is not trusted

### C. Lying code-view still contaminates replay claims
The replay path is close, but the supporting code view is still not truthful enough.
Common signals:
- dyld-cache-backed truth, extracted-image truth, and runtime landing are still not lined up cleanly
- decluttered PAC/auth cleanup helped readability but may now be hiding the exact edge you need to classify
- replay arguments are being justified from the prettiest pseudocode rather than the strongest runtime anchor

What to preserve:
- which code view supported the replay claim
- what makes that view still suspect
- what runtime anchor disagrees or remains unaccounted for

### D. Missing narrower runtime obligation
The family is probably right and the code view may already be good enough, but one smaller obligation is still missing.
Common signals:
- replay is structurally close and broad owner arguments no longer improve the explanation
- the remaining gap smells like one object materialization, table/image dependency, registration side effect, or init/context obligation
- the same path becomes plausible only after one narrower setup/materialization edge is preserved from the live run

What to preserve:
- the smallest still-missing obligation hypothesis
- why it is cheaper to test than reopening broad owner or callback-family work

## 5. Truth surfaces to trust first

### A. Runtime landing beats pretty replay pseudocode
If replay reasoning says one boundary should work but the runtime landing or crash/no-crash pair disagrees, prefer the runtime anchor.
Useful anchors:
- one landing address or callee family
- one crash vs no-crash compare pair at the same boundary
- one live path vs reduced replay path comparison
- one object materialization edge before the failing dispatch

### B. Cache-truthful system code beats stale extracted views
If the path crosses system/private framework code, treat the dyld shared cache / build / slide reality as primary.
If those relationships are still fuzzy, stronger replay-repair claims should pause.

### C. Decluttered views are routing aids, not proof
PAC/auth cleanup can help you see the route.
It is not a license to forget the raw auth-bearing edge.
For replay repair, preserve both:
- the decluttered route view
- the raw sequence needed to classify the remaining failure

## 6. Default workflow

### Step 1: freeze one representative replay failure boundary
Pick one only:
- one callback invoke that fails only in replay
- one indirect branch or tail-call handoff that diverges in reduced execution
- one object/callback materialization edge after which replay becomes unstable
- one cache-backed call family whose live landing is known but replay remains late-failing

Do not widen into many neighboring helper edges.

### Step 2: write a replay-close draft before deeper tracing
Use a compact draft like this:

```text
candidate family:
  owner / callback / dispatch family X

why this still looks replay-close:
  one successful earlier boundary + one late failing edge

current best failure class:
  not-really-replay-close | wrong-context | lying-code-view | missing-obligation

runtime anchor:
  one observed landing / crash pair / compare pair

later effect of interest:
  one callback consequence / state change / request / policy edge
```

This draft can be wrong.
Its job is to stop uncontrolled replay broadening.

### Step 3: prove replay-close before proving missing obligation
Ask first:
- does this path predict the later effect better than sibling paths do?
- is the late-failing edge actually downstream of the effect you care about?

Only after that ask:
- if the family is plausible, what smaller object/context/materialization/init proof is still missing?

This order matters.
Otherwise you can spend hours diagnosing context problems on the wrong family.

### Step 4: classify the missing object of trust
Force the remaining gap into one small class first:
- authenticated pointer/context mismatch
- object materialization/provenance gap
- initialized-image/table/runtime dependency gap
- registration / callback-installation side effect gap
- code-view/truth-surface mismatch still contaminating replay claims

Minimal success condition:
- future-you can answer what specific thing is still untrusted, not only that “replay still fails.”

### Step 5: use one narrow compare pair
Good compare pairs include:
- live path vs reduced replay path
- no-crash invoke vs crash invoke at the same callback/dispatch edge
- target action vs nearby non-target action at the same reduced boundary
- object present-but-untruthful vs object materialized-through-live-path

What you want to learn:
- is the family-specific landing stable?
- does the same object/context pair survive both conditions?
- is the remaining drift better explained by wrong family, wrong context, or one missing obligation?

### Step 6: stop at the first useful replay-repair classification
The workflow succeeds once you can rewrite the case as one of these:

```text
this was not actually replay-close; the family still needs correction
```

```text
the family is plausible, but the authenticated context / object provenance is still not truthful
```

```text
the supporting code view was still misleading; replay claims must stay runtime-first
```

```text
the path is replay-close and the remaining gap is one narrower runtime obligation
```

At that point, leave this page.

## 7. Practical scenario patterns

### Scenario A: callback landing is now trustworthy, but replay still dies late
Pattern:

```text
callback family looks right
  -> landing now appears stable
  -> direct/reduced replay still crashes or diverges late
```

Best move:
- do not reopen broad owner search immediately
- first separate wrong-context from missing-obligation
- preserve one live object materialization edge before replay broadening

### Scenario B: extracted view suggests the replay should work, runtime says otherwise
Pattern:

```text
decluttered/static view looks straightforward
  -> replay feels structurally correct
  -> runtime landing or crash pair does not agree
```

Best move:
- downgrade the pseudocode from proof to routing aid
- classify this first as a possible lying-code-view problem

### Scenario C: private-framework path is plausible, but object provenance is still weak
Pattern:

```text
system/private framework callback family seems right
  -> replay reaches it
  -> final invocation/materialization still is not truthful enough
```

Best move:
- freeze the cache/build/image relationship and one object provenance edge
- do not let “it reaches the right family” become proof that the replay object is already truthful

### Scenario D: replay is almost right, and the missing gap looks smaller than broad re-analysis
Pattern:

```text
owner/family already plausible
  -> most setup seems sufficient
  -> one late edge still fails consistently
```

Best move:
- treat the case as replay-close until proven otherwise
- bias toward one missing object/materialization/init obligation instead of widening back out

## 8. Breakpoint / hook placement guidance
Useful anchors include:
- one live callback registration or installation site
- one actual invocation landing site
- one state/object materialization edge before the failing boundary
- one later effect that proves whether the boundary mattered
- one compare pair separating crash from no-crash or live from replay

If the path is noisy, prefer:
- one replay boundary over many sibling callbacks
- one runtime landing over many static guesses
- one object provenance question over many local helper hooks
- one downstream effect over many nearby wrapper names

## 9. Common mistakes this page prevents

### 1. Reopening broad owner search even though the case is already replay-close
This often wastes the strongest evidence the case already produced.

### 2. Treating every replay-close arm64e failure as pure PAC proof
That overclaims far beyond what operator evidence usually supports.

### 3. Treating clean pseudocode as replay proof
Decluttering helps routing; it does not prove the live boundary is truthful.

### 4. Rewriting broad replay logic instead of isolating one missing obligation
Close-but-wrong often means one smaller missing object/context/init proof.

### 5. Hooking every nearby callback instead of freezing one replay boundary
This turns a narrow repair problem back into exploratory noise.

## 10. Relationship to nearby pages
- `topics/arm64e-pac-and-mitigation-aware-ios-reversing.md`
  - use first when the case is broadly mitigation-aware and the immediate problem is still code-view truth, PAC-era confidence calibration, or deciding whether the case is even replay-close
- `topics/ios-pac-shaped-callback-and-dispatch-failure-triage.md`
  - use first when one authenticated boundary is already frozen but the current job is still classifying the failure as wrong-family, wrong-context, lying-code-view, or replay-close
- `topics/ios-block-callback-landing-and-signature-recovery-workflow-note.md`
  - use first when the callback/block landing itself is still not truthful enough to support replay claims
- `topics/runtime-table-and-initialization-obligation-recovery-workflow-note.md`
  - use next when this page classifies the case as truly replay-close and the remaining gap is one narrower runtime artifact or init obligation
- `topics/ios-result-callback-to-policy-state-workflow-note.md`
  - use next when replay succeeds well enough and the remaining gap is the first behavior-changing local consumer or policy state

## 11. Minimal operator checklist
Use this note best when you can answer these in writing:
- what exact replay boundary am I freezing?
- what later effect makes this replay path worth caring about?
- is my best current explanation still wrong-family, wrong-context, lying-code-view, or missing-obligation?
- what one runtime landing or compare pair do I trust most?
- what smaller object/materialization/init proof is still untrusted?
- what narrower page should take over once this classification is done?

If you cannot answer those, the case probably still needs broader mitigation-aware routing, callback-landing proof, or owner reduction first.

## 12. Source footprint / evidence quality note
This note is intentionally narrow and conservative.

It is grounded by:
- `topics/arm64e-pac-and-mitigation-aware-ios-reversing.md`
- `topics/ios-pac-shaped-callback-and-dispatch-failure-triage.md`
- `topics/ios-block-callback-landing-and-signature-recovery-workflow-note.md`
- `topics/runtime-table-and-initialization-obligation-recovery-workflow-note.md`
- `topics/ios-practical-subtree-guide.md`
- `sources/mobile-runtime-instrumentation/2026-03-22-ios-pac-replay-repair-notes.md`
- Apple pointer-authentication documentation
- `ipsw` dyld shared cache documentation
- current practitioner dyld shared cache reversing material
- cautious PAC background from Project Zero and USENIX work

The evidence base is sufficient for this workflow note because the claims are limited to:
- replay-close arm64e cases are easy to misclassify
- truthful runtime landing and cache-truthful code views matter more than prettier replay pseudocode
- one small replay-repair classification workflow is more useful than broader theory or broader tracing

## 13. Bottom line
When a modern iOS case is already replay-close near a PAC-shaped or cache-backed boundary, the next best move is usually not to reopen the whole case.
Freeze one replay failure boundary, classify it conservatively, prove one runtime landing with one compare pair, and then reduce the remaining gap into one smaller context/materialization/init repair target.
That keeps mitigation-aware replay confusion from swallowing the rest of the investigation.
