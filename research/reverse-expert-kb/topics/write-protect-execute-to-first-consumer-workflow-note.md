# Write / Protect / Execute to First Consumer Workflow Note

Topic class: concrete workflow note
Ontology layers: deobfuscation practice branch, protected-runtime overlap, unpacking / runtime-generated-code handoff
Maturity: structured-practical
Related pages:
- topics/obfuscation-deobfuscation-and-packed-binaries.md
- topics/anti-tamper-and-protected-runtime-analysis.md
- topics/protected-runtime-practical-subtree-guide.md
- topics/packed-stub-to-oep-and-first-real-module-workflow-note.md
- topics/runtime-table-and-initialization-obligation-recovery-workflow-note.md
- topics/decrypted-artifact-to-first-consumer-workflow-note.md
- topics/runtime-behavior-recovery.md
- topics/malware-packed-loader-to-first-payload-handoff-workflow-note.md

## 1. Why this page exists

This page exists because a common protected-runtime / unpacking false stop sits between two existing KB surfaces.

The KB already had:
- broad packed-stub -> OEP / first-real-module guidance
- artifact-to-first-consumer guidance once recovered material is readable
- runtime-table / initialization-obligation guidance when live state is truer than static dumps

What was still under-preserved was the narrower middle seam where a target creates, modifies, or decodes bytes at runtime and then makes them executable.

The tempting but weak conclusion is:

```text
VirtualAlloc/mmap/VirtualProtect/mprotect or RWX memory observed
  -> payload found
```

The stronger reverse-engineering question is:

```text
which exact mapping/range received which bytes,
when did it become executable/coherent,
which transfer first executed it,
was it decoded as stable code,
and which first ordinary consumer/effect proves this was not just loader churn?
```

## 2. Target pattern / scenario

Use this note when most of the following are true:
- a protected, packed, JIT-like, shellcode, or staged loader path allocates/maps memory, changes page protection, or writes into executable regions
- `VirtualAlloc`, `VirtualProtect`, `VirtualProtectEx`, `WriteProcessMemory`, `NtProtectVirtualMemory`, `mmap`, `mprotect`, `memcpy`, decoder loops, or instruction-cache flushes are visible
- the analyst can see bytes being produced or a region becoming executable, but cannot yet prove whether it is payload, another unpacker stage, a trampoline, a thunk slab, a JIT cache, or throwaway scratch
- first execution into the region is observable or can be breakpointed, but downstream ordinary-code ownership is still unclear

Representative cases:
- malware packers that decrypt/decompress into a newly executable region
- protectors that rewrite code pages, emit trampolines, or stage VM helpers in executable memory
- native applications with JIT / plugin / runtime-code-generation machinery where generated-code visibility is easier than consumer proof
- unpacking cases where the first transfer into new code is still too early to count as payload handoff

## 3. Core claim

Executable memory is a reduction surface, not a final proof object.

A practical proof ladder is:

```text
mapping / allocation selected
  != bytes written or decoded into that exact range
  != executable protection and cache/coherency readiness proved
  != control transferred into that range
  != bytes decoded as stable code at the executed snapshot
  != first ordinary consumer or behavior-bearing effect proved
```

Compact branch memory:

```text
mapped != written != executable/coherent != transferred != decoded != consumed/effected
```

This split prevents six common overreads:
1. **allocation overread** — a fresh or RWX region is not automatically unpacked payload
2. **write overread** — bytes written into a range may be transient, partial, encrypted, or overwritten later
3. **protection overread** — `PAGE_EXECUTE*` / `PROT_EXEC` readiness is not first execution
4. **cache/coherency overread** — generated/modified code readiness can involve instruction-cache semantics; visibility of a flush is useful but not consumer proof
5. **transfer overread** — a jump/call/return into new memory may enter another stub stage, thunk, or dispatcher
6. **disassembly overread** — code-shaped bytes are not final until one downstream ordinary consumer/effect is tied to the executed snapshot

## 4. First questions to answer

Before broadening, answer:

1. **Which later behavior do I care about?** Payload parser, config decode, request builder, policy reducer, child launch, plugin callback, or VM handler?
2. **Which exact range is the candidate?** Base, size, page alignment, module / anonymous / heap provenance, and current owner thread/process.
3. **Which operation first produced the bytes?** Copy, decompression, decryption, relocation/fixup, remote write, JIT compiler, or page rewrite.
4. **Which operation first made this exact range executable or coherent enough to execute?** Protection change, already-RWX allocation, cache flush, or architecture/runtime-specific publish step.
5. **Which transfer first entered the range, and what snapshot did it execute?** Call, jump, return, exception resume, callback, thread start, APC, or indirect dispatch.
6. **What first consumer proves the region is not just another stage?** Stable import/string use, parser/config read, request builder, policy state mutation, child launch, network send, persistence write, or ordinary downstream routine.

## 5. Practical workflow

### Step 1: select one candidate range, not every executable event

Start with one range that plausibly matters:
- new executable allocation
- write-then-execute page
- protection flip on a decoded buffer
- remote process region that later becomes a thread start / APC / callback target
- rewritten existing code page that later changes branch behavior

Record:

```text
range: base + size + page-rounded coverage
provenance: anonymous/file-backed/heap/module/remote/JIT cache
initial protection: RW, RX, RWX, guard/noaccess, copy-on-write
owner: process/thread/module/stub/helper if known
late behavior sought: <one concrete effect>
```

If the range is only selected because it is RWX but has no downstream hypothesis, it is a candidate surface only.

### Step 2: prove byte production into that range

Tie the final executed bytes to their producer:
- `memcpy` / `memmove` / decoder loop write range
- decompressor output pointer
- decrypt loop key/constants and output span
- `WriteProcessMemory` / cross-process write
- JIT codegen buffer publication
- self-modifying writes into existing code pages

Watch for:
- partial writes followed by later fixups
- multiple generations reusing the same range
- copied headers/imports that are not the final executed body
- guard/fault-driven or exception-driven writes that happen after the first dump
- compare-run drift where randomization changes base but not code family

Stop rule:

```text
same address != same generation != same executed bytes
```

### Step 3: separate executable readiness from execution

Freeze the readiness boundary:
- Windows: `VirtualProtect` / `VirtualProtectEx` / lower `NtProtectVirtualMemory` return value and new protection
- Linux/Unix: `mmap` initial `PROT_EXEC`, `mprotect` transition, or platform-specific W^X policy behavior
- cache/coherency: `FlushInstructionCache`, explicit builtins, runtime publish barriers, or architecture/runtime-specific cache sync where visible

Treat readiness as setup truth.

Good note:

```text
range 0x...-0x... became RX after bytes [hash/len] were written;
no first execution yet; next breakpoint is execute-on-range.
```

Bad note:

```text
VirtualProtect RX => payload is running.
```

### Step 4: catch first transfer into the range

Use the lowest-noise surface available:
- hardware/software execute breakpoint on the candidate range
- DBI / emulator block callback for first basic block in range
- thread-start / APC / callback target breakpoint when the range is entered through an async mechanism
- exception/VEH/SEH or signal-resume breakpoint when execution is fault-owned
- compare-run trace slice from protection change to first in-range block

Record:
- source instruction / return site / callback family
- target address and generation number
- register/stack state at entry
- whether target is direct payload, trampoline, thunk, dispatcher, or another stub
- whether this is first entry for the generation or a later re-entry

Stop rule:

```text
transferred-to != payload-handoff
```

A first in-range block can still be a trampoline, loader continuation, import fixer, VM dispatcher, exception landing pad, or cache warmup helper.

### Step 5: decode and snapshot the executed generation

Snapshot the region at the moment that matters:
- before first execution if the goal is original emitted bytes
- at first execution if late fixups may complete just before transfer
- after first basic-block family if self-modifying code patches the next block lazily
- after import/relocation repair if static reopening needs a coherent image

Preserve:
- base, size, hash, protection, generation count
- adjacent ranges if direct branches leave the page
- relocation/import/table context if the range depends on external state
- execution trace into/out of the region

Do not trust one linear disassembly if the code is still being patched under execution. Prefer a trace-backed basic-block set plus a later static reopen when stable.

### Step 6: prove the first ordinary consumer/effect

Only call the handoff useful when one downstream object becomes behaviorally relevant:
- config parser consumes decoded data
- request builder uses generated routine output
- policy reducer changes state
- import/object/module family becomes stable and ordinary
- child/thread/callback launch is owned by the generated code
- network/file/registry/device/hardware effect is tied to this executed generation
- a dump reopens statically and reconnects to stable xrefs, strings, or function families

Good stop condition:

```text
range generation G entered at 0x...
  -> first ordinary call family at 0x...
  -> decoded config field consumed by parser/request builder
  -> dump snapshot S reopens with stable downstream xrefs
```

Weak stop condition:

```text
RX memory executed once.
```

## 6. Common failure modes

### RWX inventory collapse

A process may have several executable dynamic regions: JIT caches, trampolines, injected hooks, TLS/startup thunks, exception machinery, or unused staging buffers. Inventory helps route work; it does not name the payload.

### Stale dump collapse

Dumping after allocation or first protection flip may freeze encrypted, incomplete, pre-fixup, or wrong-generation bytes. Prefer generation-aware snapshots tied to first transfer and consumer evidence.

### Same-address generation collapse

Packers and runtimes may reuse one region repeatedly. Treat each produce/protect/execute cycle as a possible new generation until hashes, write windows, and first consumers prove otherwise.

### Transfer-only collapse

A jump into generated memory is often just the next loader stage. Require one ordinary downstream consumer before naming the region as payload or final target.

### Cache/coherency blind spot

When generated code behaves inconsistently across architecture, emulator, or live target, check whether the observed path depends on instruction-cache flush / publish-barrier behavior rather than assuming the dump or transfer proof is wrong.

## 7. Evidence package

A good handoff package includes:
- candidate range and provenance
- byte producer and final write window
- protection/cache readiness event
- first transfer into range
- generation hash/snapshot and trace slice
- first ordinary consumer/effect
- dump/reopen instructions if static follow-up is expected
- known unresolved ambiguity: additional stages, lazy patching, missing cache flush, anti-debug topology, or remote-process ownership

## 8. Source-backed anchors

- Microsoft `VirtualProtect` documents page-protection changes and notes that executable generated code requires cache coherency responsibility via `FlushInstructionCache`.
- Microsoft `FlushInstructionCache` documents explicit instruction-cache flushing for modified/generated code.
- Linux `mmap(2)` and `mprotect(2)` separate mapping creation from page-protection changes, with explicit `PROT_EXEC` / `PROT_WRITE` / `PROT_READ` semantics and architecture caveats.
- Self-modifying-code unpacker literature treats modification/unpacking phases and later transfer into unpacked code as distinct phases.
- Practitioner unpacking workflows use executable allocation/protection and execute breakpoints as useful reduction surfaces, but the KB keeps them below consumer proof rather than treating them as final payload identification.
