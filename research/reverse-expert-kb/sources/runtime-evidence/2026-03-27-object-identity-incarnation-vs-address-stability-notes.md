# Runtime-Evidence Notes — Object Identity / Incarnation Truth vs Address Stability

Date: 2026-03-27 04:16 Asia/Shanghai / 2026-03-26 20:16 UTC
Branch: runtime-evidence practical workflows
Seam: watchpoint / query workflows where the same bytes or address range do not guarantee the same semantic object across the whole backward-search window

## Why this note exists
The runtime-evidence branch already preserved two useful reminders:
- watched-object choice matters
- query scope is part of truth selection, not just efficiency

What still needed a thinner practical continuation was a frequent failure mode in replay / reverse-watchpoint / TTD-memory-query work:
- the analyst has already shrunk to a narrow address range
- the returned writes are real
- but the queried bytes do not correspond to one stable semantic object across the whole window
- so the "first bad write" story quietly crosses allocation, copy, rebinding, slot reuse, or owner transfer boundaries

This note preserves the narrower operator rule:

```text
same address != same object != same consequence-bearing incarnation
```

## Conservative source-backed takeaways
### 1. TTD query surfaces are fundamentally address/time oriented, not automatic semantic-object identity recovery
Microsoft's TTD object-model documentation preserves that:
- `@$cursession.TTD.Memory(beginAddress, endAddress, ...)` returns memory access information for an address range
- these queries are computational and often expensive
- they are excellent once the analyst already knows the right range and time window

That is strong support for the workflow rule that a precise memory query is still not the same thing as a semantically correct watched object.
If the same address range hosts different incarnations over time, the query can be technically correct yet operationally misleading.

### 2. TTD itself exposes identity-preserving concepts because raw IDs/positions can drift
The current Microsoft Learn TTD object-model docs preserve two useful hints:
- `UniqueThreadId` is more trustworthy than raw OS thread ID because thread IDs can be reused over a process lifetime
- `PinObjectPosition(...)` exists as a first-class operation in the session object model

This does **not** prove a universal object-identity abstraction for all watchpoint problems.
But it does support the conservative workflow lesson that identity across a trace is a real analysis concern and should not be collapsed into raw numeric or address continuity by default.

### 3. Reallocation / relocation reminders support the practical failure mode even outside reversing-specific docs
Ordinary `realloc` behavior reminders are enough for the narrow practical point here:
- storage may stay in place or move
- old storage identity should not be overread once the meaningful object has moved or been replaced

For reverse workflows, the important consequence is not allocator theory.
It is that an address-oriented backward query can silently cross from:
- the current meaningful incarnation
into
- older related storage
without that older storage being the right answer to the operator's actual causal question.

### 4. Query-heavy workflows need an explicit identity anchor before narrating a first-bad-write story
A stronger workflow question is often:
- what proves I am still following the same semantic object?

Representative stronger anchors:
- one allocation/lifetime event
- one owner pointer or owning container slot
- one compare-aligned rebinding point
- one generation counter / epoch / reuse discriminator
- one copy / ownership-transfer boundary where the late consequence starts depending on the new incarnation rather than the old one

## Practical workflow rule preserved for the KB
When a watched object is defined by address range, slot, or pointer alone, explicitly ask:
1. Is the address stable?
2. Is the semantic object stable?
3. Is the consequence-bearing incarnation stable?

If the answer splits across those three, do **not** narrate a single continuous first-bad-write story by default.
Instead:
- stop at the first rebinding / copy / owner-transfer / reuse boundary
- freeze the stronger identity anchor there
- continue one more hop on the newer meaningful incarnation

## Case-shaped reminders
### A. realloc / growth / normalization pipelines
A late plaintext or normalized buffer may live at a different address than its earlier temporary/storage forms.
The earliest write to historically related storage may be true but still weaker than the first write to the incarnation that later consumers actually read.

### B. container slot reuse / pool allocator cases
The same slot or address may later host a different request/session/object.
A query over the slot can therefore produce real writes that belong to the wrong generation.

### C. owner transfer / rebinding cases
A callback result may first materialize in one helper-local object and then become operational only after being copied into a session, policy, queue, or request owner.
The operationally meaningful boundary may be the rebinding or owner-transfer write, not the earliest helper-local materialization.

## Operator shorthand worth preserving
```text
same address != same object != same consequence-bearing incarnation
```

## Sources used conservatively
- Microsoft Learn — TTD Memory Objects: <https://learn.microsoft.com/en-us/windows-hardware/drivers/debuggercmds/time-travel-debugging-memory-objects>
- Microsoft Learn — TTD Object Model: <https://learn.microsoft.com/en-us/windows-hardware/drivers/debuggercmds/time-travel-debugging-object-model>
- Microsoft WinDbg-Samples TTDQueries tutorial: <https://github.com/microsoft/WinDbg-Samples/blob/master/TTDQueries/tutorial-instructions.md>
- Stack Overflow — Force relocation with realloc: <https://stackoverflow.com/questions/49692405/force-relocation-with-realloc>

## Confidence and limits
Confidence: moderate for the workflow rule, conservative for low-level tool-specific semantics.

What this note does **not** claim:
- that TTD automatically solves semantic object identity for the analyst
- that every first-bad-write workflow should privilege the newest incarnation
- that realloc behavior alone explains all watchpoint drift cases

What it does claim conservatively:
- address-oriented query success is weaker than semantic-object continuity
- identity/incarnation drift is a real enough failure mode to preserve explicitly in runtime-evidence workflow guidance
- the KB should route analysts to freeze one stronger identity anchor before overreading query output in relocation/reuse-heavy cases
