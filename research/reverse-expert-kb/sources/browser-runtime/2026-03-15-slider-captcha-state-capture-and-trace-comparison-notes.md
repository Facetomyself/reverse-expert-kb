# Slider / Canvas Challenge State-Capture and Trace-Comparison Notes

Date: 2026-03-15
Topic cluster: browser-runtime, slider/canvas captcha workflow, challenge-state capture, trace-comparison tactics

## Scope
These notes were collected to support a **concrete workflow page** for slider/canvas-style challenge analysis.
The goal is not to restate abstract captcha taxonomy, but to capture practical recurring analyst leverage points:
- where challenge state is still structured
- where movement / answer traces are assembled
- where challenge success becomes app-consumable state
- how to compare accepted vs failed runs without overcommitting to one product’s internals

## Sources consulted

### 1. GeeTest official overview
- URL: https://docs.geetest.com/BehaviorVerification/overview/overview
- Why used:
  - confirms GeeTest v4’s framing around behavioral analysis, environmental detection, and multiple challenge types including slide puzzle
  - confirms product-level anti-reverse-engineering and environment-detection claims
  - useful as vendor grounding for why lifecycle timing, environment assumptions, and challenge-type branching matter
- Practical takeaways:
  - slider/canvas workflows should be modeled as more than visual puzzle solving
  - environment and behavioral collection are part of the analyst object
  - challenge type may vary by risk signals, so one visible puzzle path is not the whole family

### 2. `gravilk/geetest-v4-slide-documented`
- URL: https://github.com/gravilk/geetest-v4-slide-documented
- Why used:
  - readable practitioner/open-source signal around one concrete GeeTest v4 slide-solving workflow
  - shows a real practitioner path of documenting, partially deobfuscating, and anchoring around the image/challenge object rather than only discussing high-level theory
- Practical takeaways:
  - one recurring pattern is to treat puzzle assets and challenge metadata as analyst-visible structure before deeper packing/encryption paths
  - challenge solving work may involve image-position logic, asset hashing / indexing, or challenge-specific offsets
  - even when the internal script evolves, the workflow lesson survives: find stable challenge artifacts before over-expanding bundle deobfuscation
- Caution:
  - the repo is time-bounded and version-sensitive; do **not** treat exact internals as stable invariants

### 3. Castle blog: Binance custom slider solver analysis
- URL: https://blog.castle.io/what-a-binance-captcha-solver-tells-us-about-todays-bot-threats
- Why used:
  - offers a readable breakdown of a real custom slider family from a defender’s perspective
  - unusually useful because it explicitly describes the workflow chain:
    - challenge trigger / precheck
    - challenge fetch
    - image path
    - submit request carrying encrypted data
    - decrypted payload containing movement coordinates, fingerprinting data, and challenge-specific inputs
    - final token verification request
- Practical takeaways:
  - slider challenge solving often lives inside a broader workflow:
    - trigger edge
    - challenge asset fetch
    - movement/answer trace generation
    - packed submission
    - token issuance
    - final token redemption
  - the highest-leverage browser or app boundary is often the last readable trace object **before** it is encrypted or flattened into a submission blob
  - accepted-vs-failed comparisons should include:
    - challenge metadata
    - movement trace shape
    - fingerprint / browser context sibling fields
    - token redemption path
  - one product may use two anti-bot layers: one for challenge flow, one earlier for risk classification; this matters because analysts may over-focus on the visible slider while missing a prior gating layer

## Cross-source synthesis

### 1. A slider/canvas target is rarely just an image problem
Across vendor docs, practitioner material, and the Binance case, the durable practical model is:

```text
challenge trigger
  -> challenge asset / metadata fetch
  -> user or synthetic interaction trace
  -> local answer / trajectory object
  -> pack / encrypt / submit boundary
  -> success token or validate object
  -> final redemption request
```

This is better than either:
- “find the gap position,” or
- “find the encrypted parameter.”

### 2. The last structured trace object is a high-value anchor
A repeated leverage point is the last place where a movement trace, puzzle offset, or answer object still exists as structured data.
After that point, the path usually becomes much harder:
- encrypted blob
- flattened string
- packed request payload
- opaque callback/transport object

This suggests a practical breakpoint policy:
- do not start from the final opaque request if you can move one or two frames earlier to a readable trajectory/answer object

### 3. Token success is not the final truth surface
The Binance case makes a useful distinction:
- one request submits the challenge solution and receives a token
- a later request redeems that token

This means the workflow should separate:
- local challenge success
- token issuance
- backend acceptance

That same separation generalizes to other slider/canvas families.

### 4. Compare-run value is highest at bounded workflow edges
Promising compare axes:
- accepted vs failed challenge attempt
- immediate submit vs delayed submit
- one browser environment vs another
- visible challenge path vs escalated or alternate challenge path
- minimal observation vs heavy instrumentation

Useful compare boundaries:
- challenge trigger edge
- asset/metadata fetch response
- last readable answer / movement object
- packed submit request
- token/result object
- final redemption request

## Candidate durable workflow sections justified by the sources
A future practical page should likely include:
- target pattern / scenario
- analyst goal
- concrete workflow
- where to place breakpoints/hooks
- likely failure modes
- environment assumptions
- representative code/pseudocode/harness fragments
- compare-run recording template

## Why this source cluster is KB-worthy
This cluster justifies a **workflow note**, not another abstract anti-bot page, because it gives repeated evidence for concrete analyst actions:
- locate the challenge start edge
- capture challenge metadata and assets
- localize the movement/answer-object assembly path
- step backward from encrypted submission blobs to structured preimages
- separate token issuance from final backend acceptance
- compare runs at the same lifecycle boundaries

## Limitations / evidence note
- Open-source and practitioner material here is version-sensitive and should not be treated as algorithmically stable.
- The Castle post is defender analysis, not official protocol documentation.
- The vendor docs describe product capabilities and high-level integration, not undocumented internals.
- Therefore the KB page built from these notes should stay conservative and workflow-first.
