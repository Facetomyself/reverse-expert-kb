# Source Notes — 2026-03-17 — `sperm/md` Browser / JS anti-bot batch 3

## Source set
Primary repository reservoir:
- <https://github.com/Facetomyself/sperm/tree/main/md>

Articles closely reviewed in this batch:
- `simpread-人均瑞数系列，瑞数 4 代 JS 逆向分析.md`
- `simpread-人均瑞数系列，瑞数 5 代 JS 逆向分析.md`
- `simpread-某瑞数 5 代 cookie 和 url 后缀补环境代码.md`
- `simpread-Canvas 指纹隐藏实战.md`
- `simpread-【网页逆向】chan 妈妈滑块 ast 反混淆.md`
- `simpread-JS 逆向 _ 某行业大佬对坑风控的一些经验总结.md`

## Why these articles were grouped together
This batch coheres around one practical branch:
- **real browser anti-bot work often becomes protection-family-specific, and the winning move is to model the family’s generated artifacts, state sources, and validation layers rather than treating it as generic “JS reverse”**

The subthemes are:
- family-specific analysis for 瑞数/Botgate 4.x and 5.x
- cookie and URL-suffix generation as consequence-bearing artifacts
- `$_ts` / localStorage / fingerprint-derived state dependencies
- canvas-fingerprint hiding and detector-aware spoofing
- slider/captcha reconstruction as data-path recovery, not UI playacting
- broader risk-control layering: proxy, client environment, behavior

## Strong recurring ideas

### 1. Protection families are best modeled by their artifact pipeline
The 瑞数 articles are strongest when they stop being “huge VM code walkthroughs” and instead become:
- initial challenge page / external JS / self-executing bootstrap
- VM payload extraction
- `$_ts` state acquisition and mutation
- cookie generation
- URL suffix generation
- optional fingerprint augmentation via localStorage- or browser-state-derived values

This is excellent KB framing.
It says: learn the family by learning the **artifact pipeline** it emits.

### 2. Consequence-bearing browser artifacts are often cookies and rewritten request URLs
The 瑞数 material reinforces a browser equivalent of the KB’s existing boundary logic:
- the decisive artifacts are not “the whole codebase”
- they are the generated cookie, the request suffix, the sign param, or the rewritten open/send path.

This is highly reusable.
If you can localize where those artifacts are generated and which state they depend on, the family becomes tractable.

### 3. `$_ts`-style state objects are often not static lookups but indirection tables with dynamic remapping
Both 瑞数 generations repeatedly reinforce a subtle but important lesson:
- the apparent state object is not just a bag of final constants
- some keys name methods which compute the actual values later
- mappings may be dynamically reassigned
- position and index relationships inside initialization blocks matter

That means browser protected-runtime work sometimes needs an **index-remapping / state-indirection recovery** phase before direct replay is reliable.

### 4. Browser fingerprint-dependent artifacts are not just “extra checks”; they can alter the artifact length and shape
The 瑞数 5 material is especially useful here:
- localStorage / canvas / network-info / other collected values can conditionally lengthen or change the 128-bit/array-like source material used downstream
- therefore fingerprint state is sometimes not merely a binary pass/fail gate, but a contributor to the actual generated artifact.

This is very KB-worthy because it separates:
- artifact validation
- artifact construction

Some fingerprint surfaces participate directly in construction.

### 5. Canvas hiding is detector-aware spoofing, not arbitrary noise injection
The canvas-fingerprint article is valuable because it goes beyond naive random-noise plugins.
Its durable lesson is:
- random noise alone is easy to detect
- detectors inspect prototype fidelity, `toString`, `length`, `name`, stable readout, and known-pixel behavior
- therefore useful spoofing must be **selective, session-stable, and detector-aware**.

This pairs well with batch 1’s runtime-shape reconstruction theme.
Spoofing must preserve believable behavior surfaces, not only alter pixels.

### 6. Slider/captcha work is often a data-path problem, not a human-interaction problem
The slider article is strongest where it reduces the challenge into:
- AST deobfuscation / decrypt-function collapse
- path/position extraction
- coordinate normalization/scaling
- AES or other straightforward envelope encryption

This is a useful corrective to a common failure mode:
- the UI looks “human-interaction-heavy,”
- but the real operator task is often just recovering the data path that encodes the interaction result.

### 7. Risk control is layered: proxy, client environment, then behavior
The broader risk-control experience summary is not highly technical, but it contributes a useful workflow guardrail:
- first layer: proxy / IP / network reputation
- second layer: client environment cleanliness
- third layer: behavior modeling

This is worth preserving because it helps avoid over-investing in JS details when the real gate may still be lower or earlier.

## Concrete operator takeaways worth preserving

### A. Family-artifact-pipeline workflow
Reusable sequence:
1. identify the challenge family and its generation/version markers
2. map the emitted artifact pipeline:
   - bootstrap page / JS loader
   - VM or packed payload load
   - state-object acquisition (`$_ts`-like)
   - cookie generation
   - URL suffix or sign generation
   - later XHR/open/send rewriting
3. localize the smallest stage that owns the artifact you need

### B. State-indirection recovery workflow for browser protected families
Reusable sequence:
1. do not treat family state objects as final constants too early
2. identify which keys are value slots vs method indirections
3. recover dynamic remapping or index-position relationships
4. only then freeze a replay model or external reimplementation

### C. Artifact-construction-vs-validation distinction
Reusable rule:
- some client-state/fingerprint surfaces merely validate the client
- others directly change the generated cookie/suffix/sign payload
- determine which is happening before deciding whether the surface can be stubbed or must be faithfully reproduced

### D. Detector-aware spoofing workflow for canvas/fingerprint surfaces
Reusable sequence:
1. identify the probe family (canvas, WebGL, audio, etc.)
2. check whether the detector inspects:
   - output stability
   - known-pixel behavior
   - prototype/`toString`/`length`/`name`
   - repeated-read consistency
3. apply session-stable and probe-aware perturbation only where needed
4. preserve believable native-surface metadata while altering the fingerprint outcome

### E. Slider/captcha data-path recovery workflow
Reusable sequence:
1. reduce the obfuscated client code to the decrypt/export core
2. locate where UI movement is normalized into data (`distance`, `t`, path list, scaled coordinates)
3. isolate the final envelope transform/encryption
4. treat the challenge as a data serialization problem unless evidence proves strong server-side behavior modeling

### F. Layered risk-control triage rule
Reusable sequence:
1. rule out network/proxy reputation issues first
2. then rule out client-environment/fingerprint incoherence
3. only then over-invest in behavior simulation and path realism

## Candidate KB implications
This batch strongly supports or suggests improvements to:
- browser-runtime and anti-bot subtree notes
- family-specific protection case-note branches
- `topics/runtime-behavior-recovery.md`

Potential future child-note opportunities:
- family-artifact-pipeline notes for browser protection families
- state-indirection recovery for browser challenge VMs / packed families
- detector-aware fingerprint spoofing note
- slider/captcha data-path recovery note
- layered risk-control triage note

## Confidence / quality note
This is one of the strongest browser batches so far because it adds **family-specific structure**.

The major durable lesson is:
- when a browser protection family is mature, do not fight it as generic JS.
- learn its emitted artifacts, its state object, and its validation layers.

Once that structure is clear, even large VM-like codebases become much less mystical.
