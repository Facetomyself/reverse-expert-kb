# Reverse Expert KB Run Report — 2026-03-14 16:00 Asia/Shanghai

## 1. Scope this run
This run focused on correcting the KB’s drift toward abstract browser/wasm synthesis by adding a **concrete mixed-runtime workflow page** for analysts working on browser targets split across JavaScript and WebAssembly.

The practical target for the run was:
- identifying how to trace a meaningful JS↔Wasm boundary in real browser reverse-engineering work
- turning existing mixed-runtime browser notes into a more actionable workflow with hooks, breakpoints, memory interpretation, compare-run tactics, and externalization decision rules

## 2. New findings
- The highest-leverage first move on many browser JS/Wasm targets is **boundary-first tracing**, not whole-module wasm recovery.
- Useful first hooks cluster around a small set of browser APIs:
  - `WebAssembly.instantiate`
  - `WebAssembly.instantiateStreaming`
  - JS wrappers around exported functions
  - imported JS callbacks invoked from wasm
- For practical analyst work, the most valuable questions are often:
  - which export is called right before the target request/challenge event?
  - what arguments cross into wasm at that moment?
  - is the returned integer an actual result or a pointer/handle into linear memory?
- Chrome DevTools wasm support reinforces a concrete workflow lesson:
  - raw wasm debugging and memory inspection are real tools,
  - but on protected browser targets they are often most effective **after** boundary narrowing, not before.
- Chrome’s own docs/blog also reinforce an evidence-trust caveat relevant to this KB:
  - debug mode can tier wasm down / perturb execution characteristics,
  - so mixed-runtime targets can suffer the same “observation changes the target” problem already documented elsewhere in the browser subtree.

## 3. Sources consulted
### Existing KB material
- `README.md`
- `index.md`
- `topics/js-wasm-mixed-runtime-re.md`
- `topics/browser-cdp-and-debugger-assisted-re.md`
- `topics/browser-side-risk-control-and-captcha-workflows.md`
- `topics/browser-fingerprint-and-state-dependent-token-generation.md`
- `topics/reese84-and-utmvc-workflow-note.md`

### New external sources used this run
- Chrome DevTools docs: `https://developer.chrome.com/docs/devtools/wasm`
- Chrome DevTools blog: `https://developer.chrome.com/blog/wasm-debugging-2020`
- RingZer0 training page: `https://ringzer0.training/webassembly-security-from-reversing-to-vulnerability-research/`

### Source artifact created
- `sources/browser-runtime/2026-03-14-js-wasm-boundary-tracing-notes.md`

## 4. Reflections / synthesis
This run’s most important correction is structural but practical: the KB now has a page for what an analyst actually does when wasm is present in a browser target.

Previously, the browser/wasm branch had good high-level framing but was still vulnerable to the failure mode the human explicitly called out: too much ontology, not enough scenario guidance.

The new workflow note improves that by centering:
- target pattern / scenario
- analyst goal
- first hook points
- breakpoint placement
- memory/pointer interpretation
- compare-run strategy
- minimal harness decision rules
- failure-mode diagnosis

A particularly useful synthesis point is that **raw wasm debugging is not the default first move** in many browser reversing tasks. The better first move is often to anchor analysis to a request or challenge event, trace the JS wrapper into wasm, and only then decide whether deeper wasm inspection is worth it.

That is exactly the kind of practical method bias the KB needs more of.

## 5. Candidate topic pages to create or improve
### Created this run
- `topics/js-wasm-boundary-tracing.md`

### Improved this run
- `topics/js-wasm-mixed-runtime-re.md`
- `topics/browser-cdp-and-debugger-assisted-re.md`
- `index.md`

### Strong candidates for future creation/improvement
- `topics/wasm-externalization-and-harnessing.md`
- `topics/browser-wasm-protection-patterns.md`
- `topics/js-wasm-memory-object-and-pointer-recovery.md`
- `topics/cdp-guided-token-generation-analysis.md`

## 6. Next-step research directions
- Do a follow-up practical page on **wasm externalization and harnessing**, with explicit rules for import reconstruction and browser-state assumptions.
- Add a more target-grounded note on **JS/Wasm token-generation paths** where request fields are assembled partly in JS and partly in linear memory.
- Deepen the browser subtree’s practical guidance on **pointer/offset interpretation** in wasm-backed browser targets.
- Look for stronger practitioner or conference material on real browser protection using wasm, especially target families where wasm is used for anti-bot or protected transform logic.

## 7. Concrete scenario notes or actionable tactics added this run
- Added hook sketches for `WebAssembly.instantiate` and export-call tracing.
- Added import-callback wrapping as a practical way to see wasm→JS dependencies.
- Added heuristics for deciding whether a numeric return is likely a result versus a pointer/offset/handle.
- Added a compare-run template for correlating exports with request/challenge timing.
- Added decision rules for when to stay in-browser versus externalize a minimal harness.
- Added failure-mode diagnosis for diverging harness behavior and raw-wasm-overfocus.

## Sync / preservation notes
- Local KB progress was preserved in canonical topic/source/run files.
- This run favored KB integration over isolated note accumulation, in line with the new practical-first direction.