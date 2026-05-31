# 2026-06-01 — Exception / guard / dynamic-unwind ownership notes

Scope: source-backed refinement for protected-runtime exception-owned control transfer, especially Windows x64 dynamic function tables and guard-page / VEH-style trap ownership.

Search artifact:
- `sources/protected-runtime/2026-06-01-0450-exception-guard-unwind-search-layer.json`

## Sources consulted
- Microsoft Learn, `RtlAddFunctionTable` — https://learn.microsoft.com/en-us/windows/win32/api/winnt/nf-winnt-rtladdfunctiontable
- Microsoft Learn, `RtlAddGrowableFunctionTable` — https://learn.microsoft.com/en-us/windows/win32/api/winnt/nf-winnt-rtladdgrowablefunctiontable
- Microsoft Learn, x64 exception handling — https://learn.microsoft.com/en-us/cpp/build/exception-handling-x64
- BenteVE, `SEH-VEH-hook-Page-Guard-Exception` — https://github.com/BenteVE/SEH-VEH-hook-Page-Guard-Exception
- Rasetsuu, `vmprotect-research` — https://github.com/Rasetsuu/vmprotect-research

## High-signal source facts

### Dynamic function tables are range-shaped ownership, not mere API presence
Microsoft documents `RtlAddFunctionTable` as adding a dynamic function table used on 64-bit Windows to unwind or walk stacks. Static image tables are normal, but dynamically generated code must provide function-table information at runtime. The parameters bind a table, entry count, and base address.

`RtlAddGrowableFunctionTable` is even more explicitly range-shaped: it informs the system of a dynamic function table representing a region of memory containing code, with `RangeBase`, `RangeEnd`, current entry count, and maximum entry count. Microsoft notes that the table is used for dispatching exceptions through runtime-generated code and for stack backtraces.

Operator implication:
- an observed call to the registration API is only **registration truth**
- the current exception PC must still be shown to fall within the installed range or table entry
- an unwind lookup / dispatch decision must still hit that table or callback-owned range
- a later resume or handler consequence must still be proved before the range becomes behavior ownership

Compact split:

```text
registered != covering this PC != lookup hit != resumed consequence
```

### x64 unwind metadata is a dispatcher input, not the behavior itself
Microsoft's x64 exception-handling documentation describes `RUNTIME_FUNCTION` entries as sorted table entries containing function start, function end, and unwind info address. `UNWIND_INFO` may include handler flags (`UNW_FLAG_EHANDLER`, `UNW_FLAG_UHANDLER`) and chained unwind info.

Operator implication:
- `.pdata` / `RUNTIME_FUNCTION` / `UNWIND_INFO` material can explain why a handler is reachable, but it does not by itself prove which handler action owns the behavior
- when generated or relocated code participates, static metadata alone can be close-but-wrong until runtime-installed function tables are correlated with the live PC
- handler data should be treated as one ownership candidate that still needs landing / lookup / resume proof

### Guard-page / VEH demos preserve the one-shot and re-arm hazard
The BenteVE guard-page VEH/SEH demo states that a `PAGE_GUARD` is added to the memory page containing the original function so a `STATUS_GUARD_PAGE_VIOLATION` can be caught. The handler can check whether the accessed address is the target function and change the instruction pointer in `ContextRecord` to the hook function. The demo also notes that when a guard-page violation is caught, the guard is removed and must be reapplied; unrelated accesses on the same page may require single-step handling to restore guard state.

Operator implication:
- `VirtualProtect(... PAGE_GUARD ...)` is setup truth, not dispatch proof
- one `STATUS_GUARD_PAGE_VIOLATION` is first-delivery truth, not repeated mechanism truth
- if the case depends on repeated use, re-arm / single-step / protection-restore evidence is required
- the first behavior-bearing object is usually the handler-side resume rewrite, not the guard bit itself

Compact split:

```text
guard configured != first fault != re-armed mechanism != resumed consequence
```

### VEH-based protected dispatch may be bytecode/control-flow architecture, not incidental anti-debug noise
The `vmprotect-research` repository summary describes VMProtect 3.5+ research where one dispatch model is VEH-based rather than page-fault based, with bytecode encryption, heap trampoline dispatch, and concrete trace analysis. Treat this as practitioner research rather than vendor documentation, but it is useful as a case-shape reminder: exception-owned transfer can be the protection architecture's dispatch surface, not only an anti-debug side effect.

Operator implication:
- do not classify every VEH hit as debugger resistance or crash noise
- ask whether exception delivery is carrying bytecode / dispatch state, a trampoline handoff, a resume target, or an ordinary anti-debug verdict
- stop once the smallest dispatch-owned state edge or resumed target is stable enough to continue; do not require a full devirtualizer if one proof object is enough

## Practical evidence row

For exception-owned Windows protected-runtime cases, capture:

```text
symptom | trigger family | registration/table site | installed range/base/end | current fault/exception PC | dispatcher landing | lookup/table hit | handler/context mutation | re-arm fact if guard/trap repeated | resumed target | downstream state/effect | handoff route
```

Use the row to prevent three common overclaims:
1. API presence is treated as range ownership.
2. range ownership is treated as lookup/resume truth.
3. one first fault is treated as sustained mechanism or behavior proof.

## Conservative synthesis

The KB's existing exception-owned workflow is directionally right. The source-backed refinement is to keep two middle proof objects first-class:

- **runtime-installed range ownership** for dynamic unwind/function-table cases
- **sustained trigger ownership** for guard/trap cases where one first exception is not enough

Both cases share the same final stop rule: leave the exception branch only after one resumed target, handler-side context mutation, state write, or other consequence-bearing edge predicts the next ordinary behavior.
