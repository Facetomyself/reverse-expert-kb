# 2026-03-25 — Native loader/import-resolution practical notes

Topic focus: delay-load helpers, forwarded exports / API-set style indirection, and the first real caller-side consumer after import resolution

## Why this note exists
The native loader/provider branch already covered visible plugin/module loading well enough, but it still benefited from a thinner Windows-heavy continuation:
- `GetProcAddress` / delay-thunk visibility can look like the answer
- forwarded exports, API-set indirection, or delay-load hooks can make that feel even more conclusive
- but the real proof object is often still one hop later: the first retained caller-side consumer that stores, reuses, dispatches through, or policy-gates the resolved target

That matters because native cases can otherwise stall in a fake-finish state:
- resolution mechanics are understood
- but behavior ownership is not yet proved

## Conservative source-backed reminders
### 1. Delay-load helper visibility is a resolution boundary, not automatically an ownership boundary
Microsoft’s delay-load helper documentation makes the mechanics explicit:
- helper checks whether the target DLL is already loaded
- helper may call `LoadLibrary`
- helper may call `GetProcAddress`
- helper stores the resolved address into the delay-load IAT slot and returns to the thunk

Practical RE implication:
- seeing `__delayLoadHelper2`, `ResolveDelayLoadedAPI`, or a patched thunk proves an import-resolution event
- it does **not** by itself prove which caller-side feature, provider path, or later behavior actually matters

### 2. Hookable delay-load paths weaken naive “the helper is the owner” reasoning
The same Microsoft material shows pre-load, pre-GetProcAddress, and failure hooks can alter normal behavior.

Practical RE implication:
- the resolved target may come from alternate DLL selection, hook substitution, or failure handling
- the stable proof object is often the caller-side retained function pointer / table slot / provider object that survives resolution, not the helper frame itself

### 3. Delay-loaded phantom or gated DLLs reinforce the need for caller-side consequence proof
Hexacorn’s phantom-DLL write-up is useful operationally because it shows delay-import presence can remain condition-gated and never become live on ordinary systems.

Practical RE implication:
- delay-import metadata and even reachable helper code can still overstate behavioral relevance
- analyst should prove the narrowing gate and one later caller-side consumer before claiming the delayed path owns the target behavior

### 4. Forwarded-export / API-set style answers are still weaker than first consumer proof
GetProcAddress docs and forwarded-export discussions are enough to preserve a conservative workflow reminder:
- resolved name lookup may land on a forwarded target or API-set mediated implementation
- this improves target-family truth
- but the behaviorally useful proof often remains one later host-side use: retained pointer, table patch, provider install, or later call site

Practical RE implication:
- “which real implementation name/address did this resolution produce?” and “which resolved edge first changes behavior?” are adjacent but distinct questions

## Practical operator rule added
Use this thinner native stop rule when the case already narrowed into Windows loader/import indirection:

```text
loader/import helper visible
  -> module / export / forwarder family becomes plausible
  -> resolved address or thunk patch becomes visible
  -> prove the first retained caller-side consumer of that resolved target
  -> only then widen into sibling imports, fallback DLLs, or async delivery
```

## Concrete scenario shapes worth preserving
### A. Delay-load thunk patched, but later behavior still unclear
- prove the first caller-side state slot, vtable-like table, or dispatch entry that stores/reuses the resolved address
- do not stop at helper success alone

### B. Forwarded export resolves cleanly, but several wrappers still compete
- treat forwarder truth as implementation-family reduction
- prove one later real caller or retained dispatch table entry that makes the path behaviorally relevant

### C. Phantom / optional DLL appears in metadata
- prove the gate that makes the path live in the current run
- then prove one later consumer before claiming real ownership

## Likely KB consequence
The loader/provider branch should preserve a narrower distinction between:
- **resolution truth**: which DLL/export/forwarder family was actually chosen
- **consumer truth**: which caller-side retained use first makes that resolved edge behaviorally relevant

That distinction is small, practical, and especially useful for Windows-native cases built around delay imports, runtime import lookups, API-set indirection, or forwarded-export ambiguity.
