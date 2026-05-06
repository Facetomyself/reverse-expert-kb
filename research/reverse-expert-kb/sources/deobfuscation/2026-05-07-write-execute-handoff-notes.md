# Source Notes — Write/Protect/Execute Handoff and First Consumer

Date: 2026-05-07 04:50 Asia/Shanghai
Search artifact: `sources/deobfuscation/2026-05-07-0450-write-execute-handoff-search-layer.txt`

## Scope

These notes support a practical deobfuscation / unpacking workflow for targets where decoded, generated, copied, or unpacked bytes become executable at runtime. The goal is not a generic packer tutorial. The durable proof object is the split between allocation/mapping, byte production, permission/cache readiness, first execution transfer, and first behavior-bearing consumer.

## Sources used

- Microsoft Learn, `VirtualProtect` — https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtualprotect
- Microsoft Learn, `FlushInstructionCache` — https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-flushinstructioncache
- Linux man-pages, `mprotect(2)` — https://man7.org/linux/man-pages/man2/mprotect.2.html
- Linux man-pages, `mmap(2)` — https://man7.org/linux/man-pages/man2/mmap.2.html
- Debray et al., `Reverse Engineering Self-Modifying Code: Unpacker Extraction` — https://www2.cs.arizona.edu/people/debray/Publications/unpacker-extraction.pdf
- Dliv3, `Thoughts about automated malware unpacking` — https://gist.github.com/Dliv3/6b995473190febd0bce75ee3aedb4fe1
- N4k0r, `Unpacking tips` — https://n4k0r.github.io/tips/unpacking/
- r0da, `Quick look around VMP 3.x - Part 1 : Unpacking` — https://whereisr0da.github.io/blog/posts/2021-01-05-vmp-1/

## High-signal facts

### Windows protection change is setup truth, not execution truth

Microsoft documents `VirtualProtect` as changing protection on committed pages, with page-range semantics that can cover every page containing the supplied byte range. The documentation also warns that when making a region executable, the caller bears responsibility for cache coherency via `FlushInstructionCache` where appropriate.

Reverse implication:
- `VirtualProtect(..., PAGE_EXECUTE*)` proves a page-protection transition request / success if the return value is checked.
- It does not prove that new bytes were written, that instruction cache coherence was handled, that control transferred there, or that the code became behaviorally relevant.

### Instruction-cache flush is a separate readiness boundary

Microsoft documents `FlushInstructionCache` as flushing the instruction cache for a specified process and notes that applications should call it when they generate or modify code in memory because CPUs may otherwise execute old cached instructions.

Reverse implication:
- cache flush visibility is stronger than a raw protection flip for generated/modified code readiness
- but cache flush still does not prove first execution or downstream consumer ownership
- lack of a visible flush is not always decisive across architectures/runtimes, but it is a useful coherence warning in compare pairs

### Linux `mmap` / `mprotect` split mapping from protection

`mmap(2)` creates a process mapping and takes initial `PROT_READ`, `PROT_WRITE`, and/or `PROT_EXEC` attributes. `mprotect(2)` changes protection over page-aligned ranges and can generate `SIGSEGV` if the process accesses memory contrary to protection. Linux explicitly permits `mprotect` on existing process-address-space regions, including changing existing code mappings to writable, with architecture caveats around `PROT_EXEC`, `PROT_READ`, and `PROT_WRITE` implications.

Reverse implication:
- mapping provenance, current protection, and CPU-access consequence are separate proof objects
- file-backed vs anonymous, shared vs private, and page-aligned range effects matter when deciding whether a dump corresponds to a durable code object
- an executable mapping can be a staging arena, JIT cache, trampoline slab, shellcode blob, or loader scratchpad; it is not automatically the payload consumer

### Unpacker literature treats first transfer into unpacked code as a phase boundary

Debray et al. frame self-modifying/unpacking traces as phases where a modifying/unpacker phase produces or alters code and a later transfer enters unpacked code. The paper's examples emphasize that some small self-modification phases are obfuscation-only before the main unpacker or payload phase.

Reverse implication:
- one write/execute transition can be an intermediate unpacker phase rather than the payload boundary
- the practical output should include a downstream ordinary-code anchor, not only “jumped into modified memory”

### Practitioner unpacking workflows monitor executable allocation/protection and execution breakpoints

Practitioner notes repeatedly use `VirtualAlloc` / `VirtualProtect` or executable mappings as reduction surfaces, then set breakpoints on execution of those regions to dump right before/at first execution. This is useful, but it still needs a proof ladder:
- allocated or protected executable region
- bytes actually written or decoded
- first transfer into region
- dump snapshot at the right time
- first stable import/string/object/consumer downstream

## Durable synthesis

The compact proof ladder worth preserving in the KB is:

```text
mapped/allocated != bytes-written != executable/cache-ready != transferred-to != decoded-as-code != first consumer/effect
```

This seam belongs in the deobfuscation / protected-runtime branch because it is the smaller middle layer between broad packed-stub/OEP work and ordinary post-unpack semantic recovery. It also connects to malware unpacking and runtime-evidence packaging, but the canonical proof object is not “malware payload exists”; it is the runtime-generated-code handoff boundary.
