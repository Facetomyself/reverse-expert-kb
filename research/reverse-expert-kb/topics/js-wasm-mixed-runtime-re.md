# JS / WASM Mixed Runtime Reverse Engineering

Topic class: topic synthesis
Ontology layers: browser-runtime subdomain, mixed-execution recovery, protected-code overlap
Maturity: structured
Related pages:
- topics/js-browser-runtime-reversing.md
- topics/jsvmp-and-ast-based-devirtualization.md
- topics/browser-environment-reconstruction.md
- topics/runtime-behavior-recovery.md
- topics/decompilation-and-code-reconstruction.md
- topics/obfuscation-deobfuscation-and-packed-binaries.md
- topics/community-practice-signal-map.md

## 1. Topic identity

### What this topic studies
This topic studies reverse engineering of browser-side targets whose meaningful logic is split across JavaScript and WebAssembly execution layers.

It covers:
- JS ↔ wasm interaction boundaries
- wasm-backed parameter/signature generation
- mixed static/dynamic recovery workflows
- browser-side wasm protection and virtualization overlap
- lifting, translation, or externalization of wasm logic for analysis
- how analysts reconnect wasm-executed semantics back to browser-visible behavior

### Why this topic matters
Modern browser targets increasingly place critical logic partly or primarily in wasm modules.
That changes the analyst’s job.

Instead of only understanding JavaScript, the analyst may need to recover:
- where JS hands off to wasm
- what values cross the boundary
- how wasm execution contributes to token generation, crypto, challenge logic, or protected computation
- whether the wasm layer is merely an optimization, or the true semantic center of the target

This topic matters because mixed JS/wasm targets are neither ordinary browser JS reversing nor ordinary native binary reversing.
They form a mixed-execution subdomain with its own workflow shape.

### Ontology role
This page mainly belongs to:
- **browser-runtime subdomain**
- **mixed-execution recovery**
- **protected-code overlap**

It is a browser-runtime page because the logic lives inside browser execution contexts.
It is a mixed-execution page because semantics are split across JS and wasm layers.
It overlaps protected-code analysis because wasm is often used alongside obfuscation, virtualization, or execution-hiding strategies.

### Page class
- topic synthesis page

### Maturity status
- structured

## 2. Core framing

### Core claim
JS/wasm mixed runtime reversing should be treated as a distinct workflow family where analysts recover semantics across language and execution boundaries rather than within a single code surface.

The key analyst question is often not:
- what does this wasm blob do in isolation?

It is:
- what role does wasm play in the end-to-end browser-side workflow?
- which values, control transfers, or semantic responsibilities cross between JS and wasm?
- where should analysis stay in-browser, and where should wasm be lifted, traced, or externalized?

### What this topic is not
This topic is **not**:
- generic wasm introduction material
- native-only reverse engineering
- browser JS reversing without wasm involvement
- a claim that all wasm usage is protection-driven

It is about analyst-centered recovery of meaning across JS/wasm execution boundaries in browser-side targets.

### Key distinctions
Several distinctions should remain explicit.

#### 1. wasm as implementation detail vs wasm as semantic center
Sometimes wasm is a performance helper. Sometimes it contains the real protected algorithm.

#### 2. Boundary tracing vs whole-module understanding
The fastest path may be to understand boundary values and call responsibilities rather than fully lifting the entire wasm module immediately.

#### 3. Mixed-runtime recovery vs pure decompilation
Even if wasm can be translated or lifted, the real problem often remains understanding how browser JS and wasm cooperate.

#### 4. wasm use vs virtualization/protection intent
Wasm may be used for performance, portability, or protection. Analysts need to distinguish those roles.

#### 5. Browser-side wasm vs native-binary semantics
Wasm may resemble low-level code in some ways, but it still lives inside browser-driven workflows, browser state, and browser-side request logic.

## 3. What this topic depends on
This topic depends on several other KB concepts.

- **JS / browser runtime reversing**
  - because mixed JS/wasm logic is one branch of browser runtime analysis
- **Runtime behavior recovery**
  - because tracing boundary values and execution effects is often essential
- **Browser environment reconstruction**
  - because extracted or externalized wasm analysis often still depends on browser-side assumptions and inputs
- **Decompilation and code reconstruction**
  - because lifting or translating wasm is often part of the workflow
- **Obfuscation and protected-code analysis**
  - because wasm may hide or harden the most important client-side logic

Without those dependencies, the topic becomes either too compiler-centric or too browser-generic.

## 4. What this topic enables
Strong understanding of this topic enables:
- better identification of whether meaningful logic lives in JS, wasm, or the boundary between them
- more disciplined choice among breakpointing, tracing, lifting, translating, or harnessing wasm modules
- clearer analysis of browser-side crypto, token, and challenge workflows that depend on wasm execution
- stronger integration of browser-runtime work with code-reconstruction techniques

In workflow terms, this topic helps the analyst decide:
- should I follow JS call paths, instrument boundary values, or lift wasm logic directly?
- what minimum understanding is enough to reconnect wasm computation to the browser-side behavior I care about?
- when is partial boundary understanding sufficient, and when is whole-module analysis necessary?

## 5. High-signal sources and findings

### A. Practitioner community sources show repeated mixed JS/wasm targets
Source cluster:
- `sources/community-forums/2026-03-14-52pojie-kanxue-manual-curation.md`
- `topics/community-practice-signal-map.md`

Representative recurring signals include:
- wasm 转 C 调用实战
- wasm 转 C 调用与封装至 dll 案例
- 某乎 __zse_ck 参数 js 与 wasm 多重套娃
- cctv 视频解密，wasm vmp 分析
- broader browser-side parameter and protection cases where wasm appears as part of the protected path

Why it matters:
- this confirms mixed JS/wasm targets are not rare curiosities
- they are a repeated practical pattern in browser-side reversing

### B. wasm often appears where browser-side logic becomes most security- or protection-sensitive
Practitioner patterns suggest wasm commonly appears in contexts such as:
- token or signature generation
- protected algorithm execution
- browser-side crypto or content handling
- mixed virtualization / protection paths

Why it matters:
- this supports treating wasm not just as a technical implementation detail, but as a meaningful branch of browser-side protected execution

### C. Translation and externalization are practical analyst moves
The supplied source cluster includes wasm-to-C / DLL-oriented workflows.

Why it matters:
- analysts do not always stop at in-browser inspection
- practical workflows often attempt to externalize, translate, or wrap wasm logic for more controlled analysis

### D. Boundary reasoning is often the highest-leverage first move
Synthesis from the browser subtree suggests:
- the fastest gain often comes from understanding JS↔wasm boundaries, input/output values, and where browser state enters the computation
- full wasm lifting may be unnecessary for the next analyst decision

Why it matters:
- this strongly matches the KB’s “next trustworthy object” framing

## 6. Emerging internal structure of the topic
A stable internal decomposition is emerging.

### 1. JS↔wasm boundary analysis
Includes:
- call boundaries
- argument/value transfer
- return-path semantics
- state handoff between JS and wasm

### 2. In-browser mixed-runtime observation
Includes:
- breakpoints around boundary calls
- value tracing
- browser-side execution correlation
- identifying which side owns which semantics

### 3. wasm lifting / translation / externalization
Includes:
- wasm-to-C workflows
- harnessing or wrapping wasm
- extracting modules for more controlled analysis

### 4. Protected or virtualized mixed-runtime targets
Includes:
- wasm-backed protected logic
- wasm in VMP-like or deobfuscation-sensitive workflows
- mixed JS/wasm anti-analysis overlap

### 5. Applied browser workflow integration
Includes:
- parameter generation
- challenge logic
- content decryption or protected media logic
- browser-side crypto or verification paths

## 7. Analyst workflow implications
This topic matters especially during:

### Orientation
The analyst first needs to determine:
- where does the meaningful logic actually live?
- is wasm the core algorithmic layer, or only a helper invoked from JS?
- what browser-visible behavior is explained by the boundary between layers?

### Hypothesis formation
Analysts often form hypotheses such as:
- the key token is computed inside wasm but staged from JS-side state
- this wasm module holds the protected core while JS provides orchestration and browser context
- the visible browser-side control flow is only a shell around a more important wasm computation

### Focused experimentation
Progress often depends on:
- tracing values at JS↔wasm boundaries
- correlating browser events and network requests with wasm invocations
- deciding when to translate/lift wasm versus when to keep analysis inside the browser
- externalizing only the meaningful computation path instead of the whole page logic

### Long-horizon analysis
Analysts need to preserve:
- which values cross the JS/wasm boundary
- what parts of the wasm module were actually relevant
- how extracted or translated wasm behavior compares to in-browser behavior
- what assumptions still depend on browser runtime state

### Mistakes this topic helps prevent
A strong mixed-runtime model helps avoid:
- overanalyzing the entire wasm module when only one boundary path matters
- treating wasm as native code with no browser-context dependence
- ignoring JS orchestration when wasm appears to hold the core algorithm
- externalizing wasm too early without preserving the browser-side assumptions it depends on

## 8. Evaluation dimensions
The most important evaluation dimensions for this topic are:

### Boundary clarity
Can the analyst explain what crosses between JS and wasm and why it matters?

### Externalization payoff
Does lifting or wrapping wasm make the protected logic easier to inspect or test?

### Semantic recovery quality
Does the workflow recover meaningful understanding of the mixed execution path?

### Browser-context preservation
Are the browser-side assumptions needed for wasm execution still visible and controlled?

### Workflow payoff
Does the mixed-runtime analysis reduce time-to-answer on real browser-side protected targets?

Among these, the especially central dimensions are:
- boundary clarity
- externalization payoff
- browser-context preservation
- workflow payoff

## 9. Cross-links to related topics

### Closely related pages
- `topics/js-browser-runtime-reversing.md`
  - because mixed JS/wasm analysis is one of the main child branches of browser runtime reversing
- `topics/browser-environment-reconstruction.md`
  - because wasm externalization often still depends on reconstructed browser-side state or APIs
- `topics/runtime-behavior-recovery.md`
  - because live boundary observation is often the fastest route to understanding
- `topics/decompilation-and-code-reconstruction.md`
  - because wasm lifting or translation is one form of code reconstruction inside this workflow
- `topics/obfuscation-deobfuscation-and-packed-binaries.md`
  - because wasm often overlaps with protected or obfuscated browser-side logic
- `topics/jsvmp-and-ast-based-devirtualization.md`
  - because mixed JS/wasm targets may combine virtualization in JS with protected execution in wasm

### Depends on framework pages
- `topics/expert-re-overall-framework.md`
- `topics/global-map-and-ontology.md`

### Often confused with
- pure wasm compiler analysis
- native binary reversing without browser context
- browser JS reversing without mixed execution concerns

## 10. Open questions
- Which child page deserves priority next: JS↔wasm boundary tracing, wasm externalization workflows, or wasm-backed browser protection patterns?
- How should the KB represent the difference between performance-oriented wasm and protection-oriented wasm?
- What evaluation patterns best capture mixed-runtime RE payoff in browser targets?
- How much browser-state preservation is required for externalized wasm analysis to remain trustworthy?

## 11. Suggested next expansions
This topic may later split into several child pages:
- `topics/js-wasm-boundary-tracing.md`
- `topics/wasm-externalization-and-harnessing.md`
- `topics/browser-wasm-protection-patterns.md`

## 12. Source footprint / evidence quality note
Current evidence quality is strong on practitioner signal and lighter on formal literature.

Strengths:
- clearly justified by repeated mixed JS/wasm cases in the manually curated community cluster
- strong overlap with browser runtime, environment reconstruction, and protected-code analysis
- fills an important mixed-execution gap in the browser subtree

Limitations:
- still depends more on clustered practitioner evidence than on a dedicated formal literature pass
- boundary-tracing and wasm-protection subpatterns deserve deeper normalization later

Overall assessment:
- this page is already useful as a structured child page and well justified by the current practitioner source base, but it should be deepened before being treated as mature

## 13. Topic summary
JS / wasm mixed runtime reverse engineering gives the KB an explicit home for browser-side targets whose semantics are split across JavaScript and WebAssembly.

It matters because many real browser-side protected workflows are best understood not by studying JS or wasm alone, but by recovering the mixed execution path, the boundary values that cross it, and the browser-side assumptions that make the whole system run.