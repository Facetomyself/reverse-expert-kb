# JS↔Wasm Boundary Tracing — Source Notes (2026-03-14)

## Scope
This note supports a concrete KB shift away from abstract wasm discussion and toward **practical browser analyst workflows** for mixed JS/Wasm targets.

Focus:
- how analysts find the meaningful JS↔Wasm call boundary
- where to place breakpoints/hooks first
- when DevTools raw wasm support is enough versus when boundary tracing is higher leverage
- what failure modes appear when analysts externalize or over-focus on whole-module decompilation too early

## Sources consulted

### Chrome DevTools docs
- https://developer.chrome.com/docs/devtools/wasm
- https://developer.chrome.com/blog/wasm-debugging-2020

Key signals:
- DevTools can expose original source / call stack / scope when DWARF is available.
- Without good debug info, analysts often drop to raw wasm debugging/disassembly.
- Memory inspection is explicitly important for wasm-backed debugging.
- DevTools-open sessions tier wasm down for debugability, which changes performance behavior and can perturb timing-sensitive targets.
- Path-mapping friction between build/runtime machines is a real source of analyst confusion when debugging real wasm builds.

Practical KB relevance:
- good wasm debugging support exists, but it is not a replacement for target-centered workflow selection.
- for protected browser targets, the analyst often benefits more from finding the **JS-side import/export boundary and value flow** than from trying to understand a whole raw wasm body immediately.

### RingZer0 training page
- https://ringzer0.training/webassembly-security-from-reversing-to-vulnerability-research/

Key signals:
- real-world wasm security analysis includes CFG/callgraph reconstruction, dynamic analysis, taint tracking, DBI, de-obfuscation, decompilation, and real-life module analysis.
- wasm reversing is broad enough to justify dedicated workflow notes, not only abstract mentions.

Practical KB relevance:
- confirms that wasm analysis is not only a compiler/debugger curiosity; dynamic tracing and graph recovery are normal parts of the problem.
- supports a workflow that begins with bounded, high-payoff dynamic tracing rather than immediate whole-module recovery.

## Practical synthesis points

### 1. Boundary-first is often the right first move
In browser targets, the highest-leverage first question is often:
- what JS callback, request builder, challenge handler, or wrapper hands control to wasm?

That is usually more actionable than:
- what does every function in the module do?

### 2. High-value hooks cluster around a few browser APIs
Likely first hooks:
- `WebAssembly.instantiate`
- `WebAssembly.instantiateStreaming`
- `WebAssembly.compile`
- `WebAssembly.Module`
- `WebAssembly.Instance`
- JS wrapper calls into exported wasm functions
- imported JS functions invoked back from wasm

Why it matters:
- these surfaces reveal module bytes, import object shape, export names, and boundary argument values.
- even when names are poor, repeated call shapes and temporal correlation with network/challenge events help narrow the real path.

### 3. Raw wasm stepping is often useful later, not first
When DWARF or names are missing, raw wasm debugging can still help, but it is usually most efficient after the analyst has already identified:
- which export matters
- what values enter it
- what request/challenge stage it serves

### 4. Memory inspection matters, but only in context
Inspecting linear memory is useful when:
- JS passes pointers/offsets into wasm
- a returned integer is actually an offset/handle
- strings/buffers are staged in memory before browser-visible encoding or request attachment

The memory view is most useful when coupled to boundary capture, not used in isolation.

### 5. Debugger presence can perturb mixed-runtime targets too
Chrome’s wasm debugging support notes that debug mode can change optimization/tiering behavior.

KB implication:
- mixed JS/Wasm targets can have the same evidence-trust problem as other protected browser targets.
- analysts should compare quieter runs versus debugger-assisted runs before over-trusting timing or performance-sensitive observations.

## Practical hook sketch ideas worth preserving

### Hook module creation / import shape
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

Usefulness:
- captures when the real module is loaded
- records import namespaces / export names
- gives an early anchor for later breakpoint placement

### Wrap exported functions after instantiation
```javascript
function wrapExports(instance) {
  for (const [name, value] of Object.entries(instance.exports)) {
    if (typeof value === 'function') {
      instance.exports[name] = new Proxy(value, {
        apply(target, thisArg, args) {
          console.log('[wasm.export.call]', name, args);
          const out = Reflect.apply(target, thisArg, args);
          console.log('[wasm.export.ret]', name, out);
          return out;
        }
      });
    }
  }
}
```

Usefulness:
- helps identify which export is called right before token emission, challenge update, or decode path
- especially effective when combined with network/runtime correlation

Caveat:
- some instance exports may be non-writable or wrapped awkwardly depending on how the target retains references.
- sometimes it is better to wrap the JS call site instead of mutating `instance.exports` directly.

### Watch imported JS callbacks
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

Usefulness:
- reveals when wasm calls back into JS for string handling, environment access, crypto helpers, or browser integration
- often clarifies whether wasm is the semantic center or just a helper

## Failure modes to capture in KB

### Failure mode 1: export names exist, but none obviously map to the target behavior
Likely meaning:
- meaningful logic is behind generic names or table-indirect dispatch
- the real signal is timing/call frequency and argument shape, not names

Next move:
- correlate export calls with network emission or UI/challenge transitions
- inspect imported JS callbacks and memory writes around those moments

### Failure mode 2: returned integers seem meaningless
Likely meaning:
- return value is a pointer/offset/handle into linear memory
- semantics live in memory or later JS-side decoding

Next move:
- inspect memory around returned offsets
- trace the immediate JS consumer of that return value

### Failure mode 3: externalized module behaves differently from in-browser execution
Likely meaning:
- missing import behavior
- missing browser-state assumptions
- hidden JS-side pre/post processing
- challenge or request sequencing still matters upstream/downstream

Next move:
- diff importObject contents
- compare boundary argument values in-browser vs harness
- externalize only one meaningful path, not the whole page runtime

### Failure mode 4: DevTools/raw stepping produces confusing or unstable observations
Likely meaning:
- wrong abstraction level too early
- debugger/tiering effects perturb timing
- the target is protection-sensitive or stateful

Next move:
- return to boundary-first tracing
- use shorter breakpoint windows around request finalization or challenge transitions
- compare quieter runs

## KB direction supported by this source cluster
This cluster strongly supports creating a **concrete workflow page** rather than another abstract wasm taxonomy page.

The most valuable addition is a page centered on:
- analyst goal
- likely hook points
- breakpoint placement
- compare-run plan
- memory/pointer interpretation workflow
- externalization decision rules
- failure diagnosis

That is more useful than a generic “wasm in browser reversing” expansion.