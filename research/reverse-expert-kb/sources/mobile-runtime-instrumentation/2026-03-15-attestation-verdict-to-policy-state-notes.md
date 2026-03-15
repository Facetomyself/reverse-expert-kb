# Source Notes — 2026-03-15 — Attestation Verdict to Policy-State Transition

## Why this source note exists
This note was collected to support a concrete mobile workflow page on a recurring practical gap:
- the app already reaches a device-integrity / app-attestation / verdict path
- the analyst can often identify the API family or server verification stage
- but the first local consumer that turns a verdict into a retry, block, downgrade, challenge, or allow path is still unclear

The goal here is not to build an abstract attestation taxonomy.
It is to support a practical workflow for localizing:
- verdict arrival
- verdict decoding / normalization
- result-code / enum / boolean mapping
- first policy-state write or request scheduler that actually changes behavior

## Search queries used
Search-layer (`search.py`, Grok source only on this host) was used with these exploratory queries:
- `Android Play Integrity verdict reverse engineering app policy state transition callback device verdict`
- `Android attestation verdict callback state machine reverse engineering risk mode challenge app`
- `Android Play Integrity response handling app decision point retry challenge reverse engineering`

## Search results that were most useful
### 1. Android Developers — verdicts / Play Integrity API
Search-layer surfaced Google Android Developers material on Play Integrity verdicts and recent verdict labeling changes.

Operational value for the KB:
- reinforces that the app typically does **not** operate directly on a raw trust concept; it receives or derives labeled verdict categories / fields that then need local interpretation
- supports the practical distinction between:
  - verdict object / decoded payload
  - local mapping into app policy categories
  - later branch consequences
- useful as background for a workflow note, but not enough by itself to tell the analyst where to hook inside a real app

Limitation encountered:
- direct `web_fetch` on some `developer.android.com` Play Integrity pages hit redirect limits in this environment
- because of that, this run kept the synthesis conservative and workflow-centered instead of over-quoting docs that were not fully fetched locally

### 2. Android Developers — error / retry concepts around Play Integrity
Search-layer also surfaced Play Integrity error/retry references.

Operational value for the KB:
- suggests a practical split between:
  - verdict quality / trust classification
  - transient request failure / retryable error handling
- this matters because analysts can otherwise misread a retry scheduler as a trust-policy branch or vice versa
- supports adding explicit guidance to separate:
  - allow / degrade / block policy mapping
  - retry / backoff / fallback scheduling

### 3. Guardsquare — bypassing Key Attestation API with remote devices
URL:
- `https://www.guardsquare.com/blog/bypassing-key-attestation-api`

Most useful points:
- hardware-backed or remote attestation systems are often embedded in a broader server-side monitoring and abuse context, not just one local API return value
- the practical effect for reverse engineers is that a visible attestation API call does not automatically reveal the decisive branch
- the article is more security/abuse-focused than reversing-focused, but it strengthens a conservative workflow claim:
  - verdict presence is not equivalent to policy consequence
  - later local interpretation or server-side monitoring may still determine what actually changes

Usage in KB:
- used as supporting evidence for why a workflow page should focus on first meaningful consequence instead of only API-hook visibility

### 4. Approov — limitations of Google Play Integrity API
URL:
- `https://approov.io/blog/limitations-of-google-play-integrity-api-ex-safetynet`

Most useful points:
- practical description of the common app/server interaction pattern:
  - app invokes Play Integrity
  - Google returns encrypted verdict material
  - app forwards for verification
  - server decides defensive action
- useful reminder that local analysts may be dealing with one of several shapes:
  - local handling of request token acquisition
  - local handling of verified verdict result returned from own backend
  - local branch on policy category rather than on raw attestation fields
- also highlights that implementation often includes both verdict logic and retry/error handling, which can be confused in practice

Caveat:
- this is a vendor comparison blog, not neutral platform documentation
- useful mainly for operational framing, not for detailed internal claims

## Practical synthesis taken from the source cluster
The source cluster was most helpful when converted into a concrete analyst model:

```text
attestation request / token acquisition
  -> remote verification or local decode boundary
  -> verdict object / labels / booleans / enums
  -> app policy mapping or result-code normalization
  -> state write / feature gate / retry scheduler / challenge trigger
  -> later request acceptance, downgrade, block, or extra verification
```

The strongest reusable insight is:
- **the decisive reversing object is usually not the attestation API call itself**
- the more useful target is often the first local mapping from verdict material into:
  - policy state
  - gate decision
  - retry/fallback state
  - challenge / degraded-mode trigger

## Concrete hook / breakpoint anchors suggested by the source cluster
These are workflow-oriented anchors, not guaranteed universal internals:
- verdict or token callback boundary
- backend verification response parser / decoder boundary
- result-code or enum mapping helper
- controller / repository / manager state write
- feature gate decision point
- retry / fallback scheduler boundary
- first downstream request family whose presence changes after a verdict path fires

## Failure-pattern reminders supported by the source cluster
### 1. Seeing the API call is not enough
If the attestation request hook fires, the decisive logic may still live later in:
- backend verification response handling
- policy mapping helpers
- state repositories
- retry/fallback logic

### 2. Retry logic can look like trust logic
An app may:
- retry because of transient attestation/service errors
- downgrade because of policy verdicts
- trigger challenge or limited mode because of verified trust classification

These should not be collapsed into one branch.

### 3. Verdict labels are not the final behavior
Even when verdict categories are recoverable, the app may still map them into local business states such as:
- allow
- soft deny
- reduced privilege
- force login refresh
- force device bind
- trigger captcha / challenge
- schedule delayed retry

## How this source note should influence KB structure
This cluster argues for a concrete page such as:
- `topics/attestation-verdict-to-policy-state-workflow-note.md`

That page should emphasize:
- target pattern / scenario
- practical workflow
- breakpoint placement
- likely failure modes
- separation of verdict mapping from retry/fallback logic
- proof of consequence via state or request changes

## Limits of current evidence
- direct Android-developer page extraction was partially blocked by redirect behavior in this environment
- many strong public materials are implementation or security oriented rather than reverse-engineering oriented
- the present evidence is strong enough for a practical workflow note, but not for an authoritative deep taxonomy of Play Integrity internals

## Bottom line
The useful analyst object here is not “Play Integrity” in the abstract.
It is the concrete path from **verdict material to first behavior-changing policy state**.
That is where practical reverse-engineering work usually regains traction in attestation-heavy Android targets.
