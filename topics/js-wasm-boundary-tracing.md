# JS↔Wasm Boundary Tracing Workflow Note

Topic class: concrete workflow note
Ontology layers: browser-runtime subdomain, mixed-execution recovery, request-shaping workflow
Maturity: structured-practical
Related pages:
- topics/js-wasm-mixed-runtime-re.md
- topics/browser-cdp-and-debugger-assisted-re.md
- topics/browser-environment-reconstruction.md
- topics/browser-fingerprint-and-state-dependent-token-generation.md
- topics/browser-side-risk-control-and-captcha-workflows.md
- topics/reese84-and-utmvc-workflow-note.md
- topics/protocol-state-and-message-recovery.md

## 1. Why this page exists
This page exists to push the KB toward a more practical level.

Mixed JS/Wasm targets are common enough in browser reverse engineering that analysts need something more actionable than:
- “wasm may hold protected logic”
- “trace the boundary”

They need a page that answers:
- where to hook first
- what breakpoint path usually pays off
- how to tell whether a returned integer is a result or a pointer
- when to stay in-browser versus externalize
- how to diagnose why a wasm harness diverges from browser behavior

This page is therefore a **workflow note**, not a general theory page.

## 2. Target pattern / scenario
### Representative scenario
A browser target has meaningful logic split between JavaScript orchestration and a wasm module.

Common practical shapes:
- browser-side token or signature generation where JS prepares state and wasm computes a protected transform
- challenge or anti-bot logic where wasm performs validation, scoring, or encoding
- protected content / media / crypto paths where JS owns orchestration and wasm owns the hot path
- mixed targets where JS looks noisy, but the decisive computation happens in a few exported wasm functions

### Analyst goal
The goal is usually not to decompile the whole module.
It is one of:
- identify which JS call site reaches the meaningful wasm export
- determine what values cross the JS↔Wasm boundary
- find where browser state enters the mixed path
- explain how a wasm-returned value becomes a request field, token, or decision
- decide whether the meaningful path can be externalized into a small harness

## 3. The first question to answer
Before stepping raw wasm, answer this:

**Which browser-visible event correlates with the meaningful wasm call?**

Usually start from one of these anchors:
- request carrying the token/field
- challenge transition
- decode/render event
- response handler that triggers a wasm-backed refresh

This keeps the work target-centered.

If you do not know the surrounding browser event yet, whole-module wasm analysis tends to waste time.

## 4. Concrete workflow: first pass

### Step 1: hook module creation
Start at the browser APIs that create the mixed runtime surface.

High-yield hook points:
- `WebAssembly.instantiate`
- `WebAssembly.instantiateStreaming`
- `WebAssembly.compile`
- `WebAssembly.Module`
- `WebAssembly.Instance`

Representative hook sketch:

```javascript
const _instantiate = WebAssembly.instantiate;
WebAssembly.instantiate = async function(bufferSource, importObject) {
  console.log('[wasm.instantiate]', {
    bytes: bufferSource?.byteLength,
    imports: importObject ? Object.keys(importObject) : []
  });

  const result = await _instantiate.apply(this, arguments);
  console.log('[wasm.exports]', Object.keys(result.instance.exports));
  return result;
};
```

What to record:
- when the module loads relative to the target workflow
- import namespace names
- export names and rough count
- whether multiple modules exist

Why this pays off:
- it anchors the module to a real workflow moment
- it gives the first stable surface for later breakpoint or wrapper placement

### Step 2: identify the JS wrapper that calls exports
After instantiation, look for the JS-side wrapper that actually invokes exported functions.

Do not jump into raw wasm first unless the wrapper is trivial and obvious.

Useful observation surfaces:
- breakpoint on the JS wrapper that caches `instance.exports`
- search for the instance object flowing into token/challenge/request code
- wrap calls at the JS call site rather than relying only on export names

Representative export-call wrapper sketch:

```javascript
function wrapExportCalls(exportsObj) {
  const wrapped = {};
  for (const [name, value] of Object.entries(exportsObj)) {
    if (typeof value === 'function') {
      wrapped[name] = new Proxy(value, {
        apply(target, thisArg, args) {
          console.log('[wasm.export.call]', name, args);
          const out = Reflect.apply(target, thisArg, args);
          console.log('[wasm.export.ret]', name, out);
          return out;
        }
      });
    } else {
      wrapped[name] = value;
    }
  }
  return wrapped;
}
```

Caveat:
- some targets hold references before you can replace them cleanly
- in that case, wrap the JS function that *uses* the export, not the export object itself

### Step 3: correlate export calls with a target moment
Now compare export-call timing against one concrete event:
- request finalization
- token attachment
- challenge update
- decode/render stage

A minimal compare sheet is often enough:

```text
run A: cold load, no interaction
  export f12 called 1x during init
  export f37 called right before request /verify
  request carries token T1

run B: warm retry
  export f12 skipped
  export f37 called again with changed arg[2]
  request carries token T2

run C: altered browser state
  export f37 still called, but returned handle differs
  downstream token missing or malformed
```

This immediately tells you:
- which export is probably meaningful
- whether the call is init-only or request-coupled
- whether state changes appear before or after the wasm boundary

## 5. Where to place breakpoints / hooks

### A. Instantiation boundary
Use when:
- the page is large and you need to narrow the mixed-runtime surface
- multiple modules may exist

What to inspect:
- import object shape
- export list
- module byte length
- whether the module is loaded early or lazily on challenge/request paths

### B. JS wrapper around exported calls
Use when:
- you need the fastest route to meaningful boundary arguments
- raw wasm is still too opaque

What to inspect:
- arguments passed into the export
- calling stack leading into the wrapper
- immediate consumer of the return value

### C. Imported JS callbacks invoked from wasm
Use when:
- wasm appears to call back into JS for environment access, string processing, or browser integration
- you need to know whether wasm is the semantic center or only a helper

Representative import-wrapper sketch:

```javascript
function wrapImports(importObject) {
  for (const ns of Object.keys(importObject || {})) {
    for (const key of Object.keys(importObject[ns] || {})) {
      if (typeof importObject[ns][key] === 'function') {
        const original = importObject[ns][key];
        importObject[ns][key] = function(...args) {
          console.log('[wasm->js import callback]', `${ns}.${key}`, args);
          return original.apply(this, args);
        };
      }
    }
  }
  return importObject;
}
```

What to inspect:
- browser or environment reads
- string/byte conversion helpers
- crypto helpers
- callback timing relative to request/challenge events

### D. Immediate JS consumer of the return value
Use when:
- the export returns an integer, array, or object whose meaning is unclear
- you suspect pointer/offset semantics

What to inspect:
- whether the return is treated as a pointer/handle
- whether JS reads from wasm memory next
- whether the return only becomes meaningful after JS-side formatting/encoding

## 6. How to interpret common boundary shapes

### Shape 1: simple numeric args, simple numeric return
Possible meanings:
- true arithmetic result
- status code
- pointer/offset into linear memory
- table index / handle

Do not assume it is “the token” just because it changes.

### Shape 2: JS writes bytes into memory, then calls export
Possible meanings:
- JS is staging string/buffer input for wasm processing
- the meaningful preimage is visible before the export call

Likely next move:
- capture the preimage bytes or string before the write
- then inspect how the export output is consumed

### Shape 3: wasm returns a pointer-like integer, then JS decodes bytes
Possible meanings:
- wasm produced the real result in linear memory
- JS performs only final formatting

Likely next move:
- inspect memory around the returned offset
- capture JS-side decode path

### Shape 4: wasm frequently calls back into JS imports
Possible meanings:
- wasm relies heavily on browser/runtime helpers
- the module may be less self-contained than it first appears

Likely next move:
- treat imports as part of the semantic path, not just plumbing

## 7. Memory inspection workflow
Linear memory inspection matters most when a boundary value is really an address-like handle.

Typical cases:
- strings staged into memory before an export call
- result bytes written into memory and decoded by JS after return
- structs or buffers assembled across JS and wasm layers

Practical workflow:
1. capture boundary args/return
2. identify whether one number behaves like an offset
3. inspect memory around that address
4. compare with immediate JS-side decoding/encoding code
5. reconnect the bytes to the request field or challenge artifact you care about

A useful heuristic:
If the return value is numerically small/stable but the downstream token/string is complex, the real semantics probably live in memory or JS-side formatting rather than in the return scalar itself.

## 8. Compare-run methodology
Do not trust one run.

### Minimum useful compare axes
Change one dimension at a time:
- cold load vs warm load
- first request vs retry
- no interaction vs post-challenge interaction
- normal browser state vs reduced/altered state
- in-browser execution vs minimal harness execution

### What to record
For each run, record:
- which exports were called
- argument count / rough shape
- whether imports were called back
- what returned values looked like
- whether a request token / field changed downstream
- whether memory-backed decoding changed

### Why this matters
Mixed-runtime targets often fool analysts because:
- the same export is used in multiple roles
- one export is init-only and another is request-coupled
- browser state changes alter boundary inputs without changing code structure
- externalization strips away critical JS-side staging logic

## 9. When raw wasm stepping is worth it
Raw wasm stepping is useful once you already know one of these:
- the export that matters
- the call window that matters
- the pointer/memory region that matters

It is usually lower leverage as a first move on protected browser targets.

Use it when:
- one export is clearly tied to the target field or challenge stage
- you need to understand an internal transform stage, not just the boundary role
- debug info or naming makes the function tractable
- memory inspection already narrowed the relevant region

## 10. Externalization decision rules

### Stay in-browser first if
- you still do not know which import callbacks matter
- the meaningful path is tightly coupled to browser-state collection
- request/challenge sequencing is still unclear
- the JS-side wrapper is still doing significant staging or decoding

### Consider a minimal harness when
- one meaningful export path has been isolated
- required import behavior is enumerable
- boundary arguments are stable enough to capture
- the browser-side pre/post processing can be named and reproduced

### Prefer minimal externalization
Aim for a harness for **one meaningful path**, not a whole-page clone.

Representative harness sketch:

```javascript
async function runMeaningfulPath({ wasmBytes, imports, capturedArgs }) {
  const { instance } = await WebAssembly.instantiate(wasmBytes, imports);
  const out = instance.exports.targetFn(...capturedArgs);
  return { out, memory: instance.exports.memory };
}
```

Then separately reproduce only the JS pre/post stages you have actually observed.

## 11. Failure modes and what they usually mean

### Failure mode 1: export names exist, but none clearly match the target behavior
Likely causes:
- generic/minified names
- table-indirect dispatch
- meaningful signal is call timing, not naming

Next move:
- correlate export calls with request or challenge transitions
- inspect imports and return consumers

### Failure mode 2: export returns an integer that seems meaningless
Likely causes:
- pointer/offset semantics
- handle/table index semantics
- result only becomes meaningful after JS-side decode

Next move:
- inspect memory around the return value
- trace immediate JS consumer

### Failure mode 3: minimal harness “works” mechanically but output diverges from browser behavior
Likely causes:
- missing import semantics
- missing browser-state inputs
- missing JS-side pre/post processing
- hidden request/challenge context

Next move:
- diff import object contents
- compare boundary args in-browser vs harness
- reduce harness scope to one verified path

### Failure mode 4: raw wasm stepping is too noisy or misleading
Likely causes:
- wrong abstraction level too early
- debugger/tiering effects
- protection-sensitive or stateful target behavior

Next move:
- return to JS wrapper / boundary tracing
- shorten breakpoint windows around the target event
- compare quieter runs

## 12. Practical analyst checklist

### Phase A: anchor the path
- [ ] identify the request/challenge/render event that matters
- [ ] identify when the wasm module is instantiated
- [ ] record imports and exports

### Phase B: locate the meaningful boundary
- [ ] wrap or breakpoint JS calls into exports
- [ ] correlate calls with the target event
- [ ] inspect immediate return-value consumer

### Phase C: classify the boundary
- [ ] determine whether args are preimage/state/buffer inputs
- [ ] determine whether return is a result or pointer/handle
- [ ] inspect import callbacks from wasm to JS

### Phase D: compare runs
- [ ] compare cold/warm behavior
- [ ] compare retry/no-retry behavior
- [ ] compare normal vs altered browser state
- [ ] compare in-browser vs harness behavior

### Phase E: choose the next move
- [ ] stay at boundary level
- [ ] inspect raw wasm internals
- [ ] inspect memory regions
- [ ] externalize one minimal path

## 13. What this page adds to the KB
This page adds grounded material the KB explicitly needs more of:
- concrete hook points
- breakpoint placement strategy
- pointer/memory interpretation heuristics
- compare-run methodology
- minimal harness guidance
- failure diagnosis tied to real mixed-runtime workflows

It is intentionally more useful for an analyst-in-progress than another abstract wasm taxonomy page.

## 14. Source footprint / evidence note
This workflow note is grounded by:
- Chrome DevTools wasm debugging docs and blog posts for realistic browser observation surfaces, memory inspection, and debug/tiering caveats
- wasm security/reversing training material showing dynamic analysis, graph recovery, de-obfuscation, and real-life module analysis as normal parts of wasm RE
- existing KB browser-runtime synthesis and practitioner clustering around wasm-backed browser targets

## 15. Topic summary
JS↔Wasm boundary tracing is a practical workflow for browser targets where the meaningful computation is split across JavaScript and WebAssembly.

It matters because the fastest route is often not whole-module recovery, but correctly locating the boundary, capturing what crosses it, understanding how memory and JS-side staging shape the result, and only then deciding whether deeper wasm analysis or externalization is worth the cost.