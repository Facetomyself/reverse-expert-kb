# iOS Request-Signing Finalization and Preimage-Routing Workflow Note

Topic class: concrete workflow note
Ontology layers: iOS practical workflow, request-shaping continuation, controlled-replay / preimage-routing bridge
Maturity: practical
Related pages:
- topics/ios-practical-subtree-guide.md
- topics/ios-chomper-owner-recovery-and-black-box-invocation-workflow-note.md
- topics/runtime-table-and-initialization-obligation-recovery-workflow-note.md
- topics/mobile-signature-location-and-preimage-recovery-workflow-note.md
- topics/ios-objc-swift-native-owner-localization-workflow-note.md
- topics/mobile-signing-and-parameter-generation-workflows.md
- topics/ios-result-callback-to-policy-state-workflow-note.md

## 1. When to use this note
Use this note when the case is already clearly iOS-shaped and the main uncertainty is no longer broad topology, setup, trust, or owner choice.

Typical entry conditions:
- one decisive request family is already visible enough to compare meaningfully
- one owner path is already plausible enough to target with hooks or controlled invocation
- the analyst can already reach a near-final request builder, signer, or native helper
- black-box invocation is partly working, or at least cheaper than more broad owner hunting
- the remaining question is which **next reduction** is cheapest:
  - finalize one truthful in-app call path
  - recover the preimage before final transform destroys structure
  - or stop reducing and keep one minimal black-box replay surface

Use it for cases like:
- an iOS signer/helper is callable, but outputs still drift and it is unclear whether the missing piece is upstream preimage state or one small init obligation
- `NSURLSession` / request-builder hooks already show the target family, but the field still changes faster than final-output capture can explain
- Chomper-assisted replay reaches the right function family, but the real missing proof is whether one ObjC/Swift wrapper adds the decisive canonicalization, header merge, nonce seed, or body-normalization step
- a native signing helper looks stable, but reproducing it outside the app may be more expensive than preserving one truthful in-app request-finalization surface

Do **not** use this note when:
- the request family is still not visible enough to trust the traffic picture
- trust-path or post-trust routing is still the earliest blocker
- the first consequence-bearing owner is still unclear
- the case has already narrowed into a generic cross-platform signing/preimage problem rather than an iOS-shaped continuation from one known owner/call path
- the real gap is no longer request shaping, but callback/result-to-policy consequence

## 2. Core claim
After iOS owner localization becomes good enough, analysts often over-rotate into one of two bad extremes:
- they keep broad replay/harness work going long after one truthful in-app callable path already exists, or
- they jump too early into generic signing-algorithm cleanup before proving where request finalization, canonicalization, and preimage capture are still cheapest on iOS

The practical iOS question is usually narrower:

```text
Do I need one more iOS-specific finalization boundary,
one earlier preimage capture point,
or should I stop reducing and preserve one truthful black-box request path?
```

That decision is valuable because many iOS signing cases are dominated less by the final crypto primitive than by one small family of boundary problems:
- Objective-C / Swift wrapper canonicalization before the native helper
- request/body/header normalization immediately before `NSMutableURLRequest` or task creation
- one nonce/timestamp/session seed pulled from local state or keychain-backed context (see also: `topics/ios-keychain-item-retrieval-to-request-signing-owner-workflow-note.md`)
- one init/runtime-table/image-local artifact needed to make a nearly-correct helper truthful
- one request family where in-app black-box replay is already cheaper than extracting a standalone signer

## 3. Practical routing rule
Once one owner path is already plausible, classify the current bottleneck into one of three continuations.

### A. Finalization-boundary problem
Choose this when:
- the same action reliably reaches one signer/helper family
- output drift correlates with request body/header/path differences
- one higher-level wrapper still appears to canonicalize or merge state before the final helper
- the missing proof is likely one request-builder or request-finalization boundary rather than the crypto core itself

Best next move:
- stay close to the request-construction boundary
- capture pre-final request material and the final attached field in the same run
- prove whether one ObjC / Swift wrapper contributes the decisive serialization, sort order, header merge, or body mutation

### B. Preimage-routing problem
Choose this when:
- the signer/helper boundary is already visible, but its inputs still look opaque or packed
- the final field changes faster than final-output-only capture can explain
- one or more upstream inputs appear session-, challenge-, or environment-scoped
- you need one earlier capture point before final hashing/encoding destroys explanatory structure

Best next move:
- move one hop earlier than the final helper
- log argument objects, intermediate buffers, and one representative state source in the same compare pair
- reduce the case into one stable input family versus one volatile/session-bound input family

### C. Truthful black-box path is already enough
Choose this when:
- the in-app callable path already emits valid or nearly-valid requests
- standalone signer extraction would cost more than preserving one controlled in-app request path
- the real next question is acceptance, callback consequence, or one narrower init obligation rather than signing internals

Best next move:
- stop broad signing reduction
- keep one minimal truthful invocation contract
- route onward into runtime-table/init-obligation repair or result-to-policy consequence proof as appropriate

## 4. Concrete workflow

### Step 1: anchor one decisive request family
For one representative request family, write down:
- endpoint / method / content type
- where the signed field lands: header, query, body member, cookie-like storage, or mixed
- whether body bytes, header ordering, or path normalization visibly affect the signed output
- whether the field only appears after login, challenge, warm-up, or one feature-specific state transition

Do not widen to multiple request families yet.
One truthful family is enough.

### Step 2: locate the last iOS-shaped finalization boundary
Before chasing the crypto primitive, localize the last boundary where request semantics are still human-readable.
Typical boundaries:
- ObjC/Swift request-builder methods producing dictionaries, arrays, or JSON-like objects
- `NSMutableURLRequest` mutation helpers
- Foundation serializer / canonicalizer helpers
- Swift wrappers that derive path/body/header material before entering a native helper
- native helper entry where arguments are still recognizable even if the output is opaque

Useful question:

```text
What is the last boundary where I can still explain
why this request differs from the previous one?
```

If you still have an answer there, you are not yet forced into deeper static cleanup.

### Step 3: compare two near-identical runs
Build a compare pair that differs in exactly one meaningful dimension:
- same account / same device / same install recipe, but different body value
- same path and body, but different timestamp window
- same action twice across warm vs cold state
- same flow before and after one challenge / retry / re-auth event

Capture in one compare pair:
- pre-final request object or canonicalized body
- final attached signature/header/query field
- one likely seed source if already suspected (nonce provider, timestamp helper, keychain-backed token, session object)

This is usually more valuable than tracing ten extra helper layers.

### Step 4: decide whether the decisive gap is wrapper logic or helper inputs
#### Signs the missing piece is still a wrapper/finalization boundary
- the final helper is reached with different argument shapes than expected
- a body/header/path object mutates immediately before task creation
- request validity tracks header order, JSON compaction, percent-encoding, or merged metadata
- two near-identical runs reach the same helper but with differently normalized material

#### Signs the missing piece is upstream preimage/state
- helper arguments look stable in structure but not in values
- one argument changes with login/session/challenge state even when body/path stay fixed
- nonce/timestamp/device-state values dominate divergence
- final-output capture explains nothing without earlier state provenance

#### Signs a truthful black-box path is already enough
- the in-app path already returns accepted or almost-accepted traffic
- remaining failures are now freshness/init-side-condition shaped rather than request-shaping shaped
- the hard part has moved to callback consequence or later acceptance gate, not signature generation itself

### Step 5: pick the cheapest continuation
If wrapper/finalization dominates:
- keep working locally on iOS request builders and final mutation points
- prefer one more iOS-specific note or evidence slice over generic signing taxonomy
- preserve one exact finalization boundary in notes and scripts

If preimage/state dominates:
- continue into `topics/mobile-signature-location-and-preimage-recovery-workflow-note.md`
- carry forward the iOS-specific owner/finalization context so the generic signing page does not flatten the case into pure algorithm work

If truthful black-box invocation already dominates:
- continue into `topics/runtime-table-and-initialization-obligation-recovery-workflow-note.md` when outputs are close-but-wrong because one runtime artifact or init chain is still missing
- continue into `topics/ios-result-callback-to-policy-state-workflow-note.md` when truthful result material already exists and the real gap is now one behavior-changing consumer

## 5. Hook-placement heuristics that matter on iOS
Useful iOS-shaped boundaries to test before deeper static cleanup:
- request-builder methods that still expose `NSDictionary` / `NSArray` / `NSData` / `NSString` arguments with business meaning
- `NSMutableURLRequest` setters and request-finalization wrappers when the field may be attached late
- Swift wrappers that normalize body/path/header material before a native signer call
- native helper entry points when arguments are still structured enough to compare across runs
- keychain/session/token accessors when the suspected missing input is session-scoped rather than algorithmic

A practical reminder from the source pass and existing branch:
- if a request-dump tool already proves the final emitted request shape while a live owner path is callable, do not assume the next step is standalone signer extraction
- sometimes the operator win is preserving one truthful in-app call path and using earlier hooks only to explain drift, not to fully reimplement the signer

## 6. Failure patterns this note helps separate
### Failure pattern A: “I found the signer, so I’m done.”
Often false.
The real missing piece may still be one wrapper that canonicalizes body/path/header material before the signer sees it.

### Failure pattern B: “Final output capture should be enough.”
Often false.
If session/challenge/environment state enters earlier, final-output-only capture hides the reason divergence happens.

### Failure pattern C: “Near-correct output means wrong algorithm.”
Often false.
On iOS, near-correct outputs frequently mean one missing init artifact, request-finalization mutation, timestamp source, or session-bound seed rather than a wrong crypto family.

### Failure pattern D: “If black-box replay works, I still need full signer extraction.”
Not always.
If the analyst goal is request acceptance, downstream consequence proof, or narrow controlled experimentation, preserving one truthful black-box path may be the better stopping point.

## 7. Source-backed practical signals retained for this page
This run’s external research was intentionally conservative.
It did **not** try to infer one universal iOS signing recipe.
Instead it retained a smaller set of reusable operator signals:
- Chomper-style execution-assisted invocation is valuable once one owner path is already plausible, but it does not remove the need to localize one truthful finalization boundary
- request-dump / interception tooling is useful because it anchors the final emitted request shape even when standalone signer extraction is not yet worth doing
- Frida iOS guidance and interception material reinforce that many useful boundaries stay at ObjC/Swift/Foundation request-construction layers, not only inside low-level crypto helpers
- practitioner writeups repeatedly imply that useful progress often comes from recovering one earlier input/preimage family or preserving one truthful black-box call path, not from fully lifting every transform immediately

## 8. Practical handoff rule for the iOS branch
A compact iOS continuation ladder now worth preserving is:

```text
iOS owner plausible
  -> prove one last request-finalization boundary
  -> if needed, move one hop earlier to recover preimage/state
  -> if black-box path is already truthful enough, stop reducing and route onward
```

This means:
- leave broad owner-localization work once one owner is already good enough
- do not jump straight from owner proof into generic signing taxonomy if one narrower iOS finalization boundary is still the real gap
- do not stay in broad signing reduction if one truthful in-app call path is already enough for the case goal
