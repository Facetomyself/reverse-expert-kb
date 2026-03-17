# iOS Traffic-Topology Relocation Workflow Note

Topic class: concrete workflow note
Ontology layers: mobile practical workflow, iOS observation-surface selection, traffic-visibility diagnosis
Maturity: practical
Related pages:
- topics/ios-packaging-jailbreak-and-runtime-gate-workflow-note.md
- topics/mobile-protected-runtime-subtree-guide.md
- topics/mobile-reversing-and-runtime-instrumentation.md
- topics/android-network-trust-and-pinning-localization-workflow-note.md
- topics/protocol-capture-failure-and-boundary-relocation-workflow-note.md
- topics/observation-distortion-and-misleading-evidence.md

## 1. When to use this note
Use this note when an iOS case is already clearly network- or request-relevant, but ordinary traffic capture still feels partial, misleading, or empty enough that later reasoning is not trustworthy.

Typical entry conditions:
- the target flow clearly performs meaningful network work, yet ordinary proxy capture misses the decisive requests
- you can reach the user-visible flow, but current capture only shows support traffic, telemetry, or a misleading subset
- there is no strong proof yet that certificate pinning is the real blocker
- VPN / WireGuard / full-tunnel / transparent MITM style observation is now plausible, but not yet framed as the main workflow step
- the current bottleneck is still **where to observe the traffic truthfully**, not yet request-field recovery or policy consequence localization

Use it for cases like:
- non-jailbroken iOS traffic capture where system-proxy tooling misses key requests
- app flows that appear to bypass, classify, or ignore ordinary HTTP proxy settings
- cases where proxy-only visibility suggests "no request" but the app clearly still succeeds remotely
- hybrid network cases where the wrong capture surface makes later trust/pinning conclusions too fragile

Do **not** use this note when:
- the first decisive problem is still packaging / resign / jailbreak / instrumentation drift broadly
- the request family is already visible and the real missing edge is now trust-path localization or request ownership
- the case has already narrowed to one response consumer, one callback/policy reducer, or one signature/preimage chain
- the true bottleneck is clearly protocol parser/state recovery rather than iOS observation topology

In those cases, route to the narrower note instead.

## 2. Core claim
A recurring iOS analyst mistake is to treat weak proxy capture as immediate proof of pinning, custom crypto, or missing local hooks.

In many practical iOS cases, the next useful move is simpler:

```text
decisive traffic exists
  -> current proxy-only surface is incomplete or misleading
  -> one compare pair proves the visibility problem is topological
  -> observation moves below app-visible proxy settings
  -> the real request family becomes legible
  -> only then do trust-path, ownership, and parameter questions become worth deepening
```

The central practical question is:

```text
Is the case really blocked by trust/pinning,
or am I still standing on the wrong traffic-observation surface?
```

This note exists because, in the iOS ladder, **topology** often has to be stabilized before broader runtime-gate or owner-localization work can be trusted.

## 3. The four boundaries to separate explicitly

### A. User-visible network trigger
This is the one action that should produce the target traffic.
Typical anchors:
- login submit
- one protected API action
- one challenge/verification step
- one content fetch or refresh step

What to capture:
- one target action only
- one expected request family only

Do not compare many unrelated screens or request families at once.

### B. Current ordinary-capture surface
This is the visibility you get from the usual proxy-based path.
Typical anchors:
- system HTTP proxy tools
- standard MITM setup
- request logs from the current proxy path

What to capture:
- what traffic is visible
- what important traffic appears absent
- whether the app still succeeds despite the missing visibility

This boundary matters because "not visible here" is not the same as "not happening."

### C. Relocated traffic surface
This is the candidate surface below or beside app-visible proxy settings.
Typical anchors:
- VPN / NE / full-tunnel capture
- WireGuard-style full-tunnel observation
- transparent MITM path on the analyst-controlled host
- any observation path that catches traffic the app does not voluntarily hand to an ordinary user-configured proxy

What to capture:
- whether the previously missing request family becomes visible here
- whether visibility improves without requiring an immediate deeper app-side bypass theory

### D. First proof-of-better-surface boundary
This is the first concrete proof that the relocation was the right move.
Typical anchors:
- the previously missing request family now appears
- headers / paths / methods now align with the user-visible action
- later trust-path or signing analysis now has a stable target request to follow
- earlier claims like "no request" or "wrong request" can now be corrected

This is the real end point of the workflow.
Until it is proved, topology relocation is still only a guess.

## 4. Default workflow

### Step 1: Freeze one representative iOS action
Pick one flow only.
Examples:
- launch -> login submit
- login -> first protected API call
- button tap -> one challenged request
- page refresh -> one content/API fetch

Avoid broad "capture the whole app" goals.

### Step 2: Write one visibility failure pair
Use a compact draft like:

```text
user-visible action:
  target action X

ordinary capture surface:
  proxy shows A/B traffic only

missing family:
  request family Y still absent

current outcome:
  app still succeeds / server still responds / feature still updates

leading diagnosis:
  likely topology mismatch before hard trust-path conclusion
```

This prevents premature pinning folklore.

### Step 3: Test whether the problem is topological before calling it trust
Useful questions:
- does the app still complete the action while the proxy view looks incomplete?
- does changing to VPN / full-tunnel / transparent MITM suddenly reveal the family?
- is there a clean local trust/pinning symptom, or only missing visibility?
- does the current proxy path show support traffic but miss the decisive action traffic?

Good provisional role labels:
- `target-action`
- `proxy-visible`
- `proxy-missing`
- `topology-relocated`
- `newly-visible-family`
- `later-trust-work`

### Step 4: Relocate to a lower or less classifiable observation surface
Prefer the smallest relocation that can falsify the current diagnosis.
Typical move:
- from ordinary proxy capture
- to VPN / WireGuard / transparent MITM capture on the analyst-controlled host

The point is not to collect more traffic randomly.
The point is to prove one better visibility boundary.

### Step 5: Stop once one decisive request family becomes trustworthy
The workflow succeeds when you can rewrite the case as:

```text
user-visible action
  -> proxy-only surface was incomplete
  -> relocated surface revealed request family Y
  -> request family Y now becomes the stable target for deeper work
```

At that point, hand off:
- to trust-path localization if TLS/pinning/native validation still matters
- to request ownership/signature analysis if the request is now visible enough
- to response-consumer or policy-consequence work if traffic visibility was the main blocker

Do not keep this page open after one request family becomes trustworthy.

## 5. Practical scenario patterns

### Scenario A: Proxy capture misses the interesting request, but the action still succeeds
Pattern:

```text
user action fires
  -> proxy shows only partial traffic
  -> app/server behavior proves the action still completed
  -> relocated VPN/full-tunnel surface reveals the real request family
```

Best move:
- classify this as topology failure first
- stop assuming "no request" or immediate pinning until the better surface is checked

### Scenario B: The proxy path shows some traffic, which creates false confidence
Pattern:

```text
ordinary proxy shows support APIs / telemetry
  -> analyst assumes visibility is complete
  -> decisive action request remains missing
  -> deeper conclusions are built on the wrong subset
```

Best move:
- treat partial visibility as dangerous, not reassuring
- prove whether the decisive family is absent only from this surface

### Scenario C: Non-jailbroken setup plus full-tunnel observation beats invasive proxy-only assumptions
Pattern:

```text
ordinary proxy setup stays blind
  -> app otherwise behaves normally
  -> full-tunnel or transparent MITM observation reveals the case without changing app logic much
```

Best move:
- prefer the surface that yields trustworthy traffic over the setup that merely feels more invasive or advanced

## 6. Breakpoint / hook placement guidance
Useful anchors include:
- one user-visible action boundary
- one ordinary proxy capture log boundary
- one relocated full-tunnel / transparent MITM visibility boundary
- the first newly visible request family that matches the target action
- the first later note/workflow that becomes possible because this family is now visible

If evidence is noisy, anchor on:
- one target action and one expected request family
- one missing-vs-visible contrast
- one proof request, not every request in the app

## 7. Failure patterns this note helps prevent

### 1. Treating missing proxy visibility as proof that no request exists
Proxy blindness is not absence.

### 2. Calling pinning too early
Many iOS cases are still unresolved topology problems when analysts start saying "SSL pinning" with too much confidence.

### 3. Building downstream request/signature theories on partial traffic
If the surface is wrong, deeper field reasoning is usually contaminated.

### 4. Mixing topology diagnosis with later trust-path diagnosis
First prove where the traffic becomes visible, then decide whether deeper native trust work is still needed.

## 8. Relationship to nearby pages
- `topics/ios-packaging-jailbreak-and-runtime-gate-workflow-note.md`
  - use when the case is still dominated by broader iOS setup/gate uncertainty; this traffic-topology note is the narrower entry when the gate-like problem is specifically "where is the truthful network surface?"
- `topics/android-network-trust-and-pinning-localization-workflow-note.md`
  - use after one trustworthy request family exists and the next bottleneck is stack/trust owner localization rather than visibility itself
- `topics/protocol-capture-failure-and-boundary-relocation-workflow-note.md`
  - use when the same visibility problem has become a broader protocol/transport boundary issue rather than an iOS-focused observation-topology problem
- `topics/observation-distortion-and-misleading-evidence.md`
  - use when the real issue is evidence trustworthiness under observation pressure more generally

## 9. Minimal operator checklist
Use this note best when you can answer these in writing:
- what single iOS action should produce the target traffic?
- what exactly is visible from the ordinary proxy surface?
- what important request family is still missing?
- what one relocated surface will test the topology hypothesis?
- what one newly visible request family would prove the relocation was correct?
- which narrower workflow note should take over after visibility is repaired?

If you cannot answer those, the case likely still needs broader iOS gate or orientation work first.

## 10. Source footprint / evidence quality note
This note is intentionally workflow-first.

It is grounded by:
- `topics/ios-packaging-jailbreak-and-runtime-gate-workflow-note.md`
- `topics/mobile-protected-runtime-subtree-guide.md`
- `topics/mobile-reversing-and-runtime-instrumentation.md`
- `topics/protocol-capture-failure-and-boundary-relocation-workflow-note.md`
- `sources/ios-runtime-and-sign-recovery/2026-03-17-sperm-ios-batch-1-notes.md`
- `runs/2026-03-17-1420-sperm-ios-batch-1.md`

The evidence base is sufficient because the claim is conservative:
- some iOS cases are blocked first by traffic-observation topology, not by deeper trust-path theory
- non-jailbroken/full-tunnel observation can be the decisive move
- a dedicated workflow note prevents this pattern from staying scattered across source notes and broader gate pages

## 11. Bottom line
When an iOS flow clearly performs meaningful network work but ordinary proxy capture stays incomplete, the next best move is often not deeper bypass theory.
It is to prove whether the current blindness is topological, relocate observation below app-visible proxy settings, and stop only when one decisive request family becomes trustworthy enough for the next stage of analysis.