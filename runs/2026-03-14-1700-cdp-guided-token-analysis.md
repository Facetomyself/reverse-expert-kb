# Reverse Expert KB Run Report — 2026-03-14 17:00 Asia/Shanghai

## 1. Scope this run
This run deliberately followed the human correction to avoid growing the KB through more abstract taxonomy work.

Instead of adding another high-level browser synthesis page, the run focused on a **concrete browser request-shaping workflow**:
- how analysts can use CDP pause events and call-frame evaluation to invoke in-scope token / encrypt / decrypt functions at the right live breakpoint
- how to turn that tactic into a reusable methodology page for browser-side token-generation analysis

The practical theme of the run was:
- **CDP-guided, breakpoint-scoped function invocation as a practical reverse-engineering workflow for browser token/signature analysis**

## 2. New findings
- A high-value practical browser workflow is to stop at the right request-generation frame and use `Debugger.evaluateOnCallFrame` to call the target function while the page still provides the real closure state, constants, helper objects, and browser environment.
- This workflow is often more informative than prematurely porting obfuscated browser code into a standalone harness.
- The most useful breakpoint is often **not** inside the deepest crypto or transform function, but at the highest frame where:
  - the callable function is still in scope,
  - its required constants/helpers are also in scope,
  - and the live request/challenge state is still meaningful.
- The key recovery artifact in this workflow is a **call contract**, not just a recovered source listing:
  - request role
  - breakpoint location
  - frame identity
  - callable expression
  - argument shape
  - prerequisite state
  - output type
- Official Chrome wasm/debugging docs also reinforce a caution directly relevant to protected browser analysis:
  - debugger-visible execution may be perturbed (for example through wasm tier-down behavior), so analysts should compare debugger-visible and quieter runs when results drift.

## 3. Sources consulted
### Existing KB material
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- `topics/reese84-and-utmvc-workflow-note.md`
- `topics/browser-side-risk-control-and-captcha-workflows.md`
- `topics/browser-fingerprint-and-state-dependent-token-generation.md`
- `topics/browser-environment-reconstruction.md`
- `topics/browser-cdp-and-debugger-assisted-re.md`
- `runs/2026-03-14-1600-js-wasm-boundary-tracing.md`
- `sources/community-forums/2026-03-14-52pojie-kanxue-manual-curation.md`

### External sources used this run
- CN-SEC mirror of practitioner writeup: `https://cn-sec.com/archives/1702334.html`
  - topic: using CDP remote calls and paused-frame evaluation to invoke in-scope functions at a breakpoint
- Chrome DevTools docs: `https://developer.chrome.com/docs/devtools/wasm`
  - topic: debugger capabilities and observation caveats for wasm-backed browser execution
- Search-layer results also surfaced related practical signals around `__zp_stoken__`, `__zse_ck`, `acw_sc__v2`, and debugger/CDP workflows, but this run concentrated on the CDP call-frame methodology because it produced the clearest immediately-integrable practical guidance.

### Source artifact created
- `sources/browser-runtime/2026-03-14-cdp-callframe-token-analysis-notes.md`

## 4. Reflections / synthesis
This run materially improved the KB’s practical ratio.

Before this run, the browser subtree already had:
- structural browser CDP framing
- browser token-generation framing
- concrete target-family notes like Reese84 / ___utmvc

But it still lacked a standalone page for a very practical analyst move that appears repeatedly in real browser work:
- use the **live page as the harness**
- choose the best stack frame
- call the in-scope function directly
- record the frame-dependent call contract before attempting a full extraction

That shift matters because many browser targets are hard not because the transform itself is impossible, but because:
- closures are still live only at certain frames
- constants are initialized dynamically
- helper objects are scattered across wrappers
- request/challenge/session state still matters

So the real question is often not “how do I fully deobfuscate this today?”
It is:
- “At what frame can I already ask the browser page to do the work for me, while I learn what really matters?”

That is a much more practical, code-adjacent, target-solving orientation than abstract “debugger-assisted RE” alone.

## 5. Candidate topic pages to create or improve
### Created this run
- `topics/cdp-guided-token-generation-analysis.md`

### Improved this run
- `topics/browser-cdp-and-debugger-assisted-re.md`
- `topics/browser-fingerprint-and-state-dependent-token-generation.md`
- `topics/browser-side-risk-control-and-captcha-workflows.md`
- `index.md`

### Strong candidates for future creation/improvement
- `topics/network-runtime-correlation-in-browser-re.md`
- `topics/browser-request-role-mapping-and-value-attachment.md`
- `topics/browser-live-harness-externalization.md`
- `topics/site-family-notes-acw_sc_v2-and-related-cookie-workflows.md`
- `topics/site-family-notes-zse-ck-js-wasm-request-shaping.md`

## 6. Next-step research directions
- Deepen the browser subtree with additional **site/protection-family-specific notes**, especially around:
  - `acw_sc__v2`
  - `__zse_ck`
  - `__zp_stoken__`
- Add a practical note on **network-runtime correlation**, focused on how to move from one request to the right live frame quickly.
- Add a concrete page on **live-harness externalization**, centered on when a paused-frame workflow is stable enough to convert into a durable helper service or local harness.
- Continue preferring pages that contain:
  - breakpoint placement logic
  - hook points
  - frame-selection strategy
  - failure diagnosis
  - representative pseudocode/harness fragments
  - request-role mapping

## 7. Concrete scenario notes or actionable tactics added this run
- Added a concrete methodology page for using `Debugger.evaluateOnCallFrame` at a meaningful request-generation breakpoint.
- Added explicit guidance for choosing the **highest useful frame** rather than the deepest transform frame.
- Added the concept of a **call contract** as a practical recovery object.
- Added breakpoint suggestions for:
  - pre-dispatch request wrappers
  - response-driven refresh handlers
  - JS wrappers around wasm exports
  - cookie/storage write sites
- Added decision rules for when to stay in-browser versus externalize.
- Added representative pseudocode for:
  - paused-frame CDP evaluation
  - later-stage HTTP helper wrapping of live-page invocation
- Added concrete failure-mode diagnosis for:
  - frame drift
  - output rejection despite callable success
  - debugger-visible distortion
  - premature externalization

## Sync / preservation notes
- Local KB changes were integrated into canonical topic/source/index files rather than left as isolated notes.
- This run continued the KB pivot toward concrete, case-driven, workflow-backed browser reverse-engineering guidance.
