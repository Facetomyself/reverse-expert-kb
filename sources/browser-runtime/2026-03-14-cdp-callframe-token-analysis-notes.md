# CDP Call-Frame Token Analysis Notes

Date: 2026-03-14
Topic: browser runtime / CDP-assisted token analysis / practical breakpoint workflows

## Provenance
This note captures two source inputs used to deepen the browser-runtime subtree with more concrete, code-adjacent workflow guidance.

### Source 1
- Title: 前端加密对抗Part2-通过CDP远程调用Debug断点函数
- URL: https://cn-sec.com/archives/1702334.html
- Original link mentioned in article: https://www.t00ls.com/articles-69054.html
- Access path: fetched via `web_fetch`
- Source type: practitioner writeup / applied workflow note

### Source 2
- Title: Debug C/C++ WebAssembly
- URL: https://developer.chrome.com/docs/devtools/wasm
- Access path: fetched via `web_fetch`
- Source type: official tooling documentation

## Why these sources matter
The KB already had browser CDP/debugger pages, but they still leaned too much toward structural framing.
These sources add a more practical, repeatable workflow pattern:
- stop execution at a value-generation edge
- capture the relevant call frame
- directly evaluate in-scope functions with controlled input
- use the live page state as the execution harness instead of prematurely porting everything out

That is highly relevant to browser token / signature / request-shaping analysis.

## Practical findings from the practitioner writeup
The practitioner article describes a concrete workflow built around Chrome DevTools Protocol events and call-frame evaluation.

### Core tactic
When execution is paused at a breakpoint near an encrypt/decrypt/token-generation function, the analyst can use CDP to evaluate expressions directly inside the paused call frame.

Key protocol ideas highlighted:
- `Debugger.paused` provides paused call-frame information
- `Debugger.evaluateOnCallFrame` can evaluate an expression in the lexical scope of that paused frame

This produces a practical analyst capability:
- instead of fully lifting or rewriting the algorithm immediately,
- call the in-scope target function directly while the page has already established the right closure state, constants, wrappers, and browser environment.

### Practical use case described
The source shows a workflow where request and response bodies are encrypted, and the analyst:
1. finds a call site near the in-scope encrypt/decrypt functions,
2. pauses execution there,
3. identifies the callable function and its expected arguments,
4. remotely triggers evaluation through CDP,
5. wraps that capability behind a small HTTP helper service,
6. plugs that service into a proxy workflow for request encryption / response decryption.

### Important practical lesson
The useful recovery object is often not “the whole deobfuscated algorithm.”
It is:
- the breakpoint location,
- the callable function name/expression,
- the required in-scope constants / helper objects,
- and the conditions under which that call remains valid.

This aligns strongly with the KB’s shift toward concrete workflow notes.

## Practical findings from Chrome’s wasm docs
The Chrome docs are not about anti-bot targets directly, but they reinforce several workflow lessons relevant to protected browser reversing.

### Tooling capabilities explicitly supported
While paused, DevTools can support:
- source-level stepping
- call stack inspection
- scope/variable inspection
- memory inspection for wasm-backed objects

### Operational caution
Chrome explicitly notes that when DevTools is open, wasm execution may be tiered down / run differently to improve debugability.

For KB purposes, this matters because it reinforces a general anti-analysis caveat:
- debugger-visible execution is highly useful,
- but the analyst must still compare debugger-visible behavior against less intrusive runs when targets are timing-sensitive or debugger-sensitive.

## Synthesis for KB integration
These sources jointly support a practical methodology page centered on:
- network-to-breakpoint anchoring
- paused-frame evaluation as an analyst tool
- staying in-browser longer before externalization
- recording breakpoint validity conditions
- using call-frame evaluation for parameter path recovery, not only whole-algorithm extraction

## Concrete tactic candidates to add into canonical topic pages
- breakpoint on final request-builder or token-attachment site
- inspect call stack upward for the nearest frame where the desired function and constants coexist
- prefer `Debugger.evaluateOnCallFrame` over premature code porting when closures or dynamic constants still matter
- record a small “call contract”:
  - expression used
  - expected argument format
  - required frame identity
  - request/challenge state required before invocation
- treat proxy integration as a later-stage validation harness, not the first analytical move
- compare behavior with DevTools/CDP visible vs quieter execution when results drift

## Evidence quality note
- The practitioner writeup is valuable for method realism and concrete workflow shape.
- The official Chrome docs are valuable for grounding debugger/wasm capabilities and observation caveats.
- Together they are sufficient to justify a concrete browser workflow page focused on CDP-guided token generation analysis.
