# Loader image-repair and startup-handoff notes — 2026-03-25

Topic class: retained source note
Branch: protected-runtime / packed-startup overlap / Windows loader-side tamper repair
Purpose: preserve a practical stop rule for cases where early image tampering is visible, but loader-side remap/repair may make the tampered view weaker than the later execution truth

## Why this note exists
This run targeted a thinner but practical protected-runtime seam:
- not generic anti-debugging
- not broad process hollowing taxonomy
- not another top-level wording sync

The useful operator question here is narrower:

```text
main-image headers or IAT page appear modified early
  + tampering / hollowing / hook-like activity is visible
  + the analyst can easily overread that modified view as enduring execution truth
  -> ask whether the loader itself detects the tampering and remaps/repairs the main image before entry
  -> keep "tampered view truth" separate from "post-repair execution truth"
  -> do not stop at evidence of early mutation alone
```

This is practically relevant because an analyst can otherwise:
- overclaim an early IAT/header patch as the final payload handoff
- overclaim one modified main-image view as the object that still owns later behavior
- miss that the useful boundary is actually the first consumer after the loader’s repair/remap decision

## External search performed
This run explicitly attempted multi-source search through:
- `search-layer --source exa,tavily,grok`

Queries:
1. `Windows module tampering protection NtQueryVirtualMemory ProcessImageSection NtMapViewOfSection reverse engineering`
2. `loader remaps main image IAT page tampering protection process hollowing reverse engineering`
3. `module tampering protection main image headers IAT remap loader before entry point`

Saved raw artifact:
- `sources/protected-runtime/2026-03-25-protected-runtime-loader-image-repair-search-layer-1720.txt`

## Search audit for this note
Requested sources:
- exa
- tavily
- grok

Succeeded:
- exa
- tavily

Failed:
- grok

Endpoints on this host:
- Exa: `http://158.178.236.241:7860`
- Tavily: `http://proxy.zhangxuemin.work:9874/api`
- Grok: `http://proxy.zhangxuemin.work:8000/v1`

Degraded-source note:
- Grok invocation failed with `502 Bad Gateway`
- Exa and Tavily returned enough usable material to continue conservatively
- this note therefore comes from a real external-research-driven run under a degraded source set, not from KB-only maintenance and not from Grok-only mode

## Conservatively retained source-backed cues
Primary retained source:
- Yarden Shafir, *Understanding a New Mitigation: Module Tampering Protection* — Windows Internals / Winsider

Retained cues from that source:
- the mitigation protects against **early modifications of the process main image**, specifically including header / IAT-page tampering and process-hollowing-like situations
- before the entry point is called, the loader can check whether the main image headers or IAT page were modified from their original mapping
- the described implementation uses `NtQueryVirtualMemory` with `MemoryWorkingSetExInformation`, then `NtQueryInformationProcess(ProcessImageSection)`, then `NtMapViewOfSection`
- if tampering is detected, the loader can remap the main image section and continue using the fresh/remapped section rather than the tampered copy

Why this matters for the KB:
- a visible early modified view is not automatically the view that still owns later execution
- in some loader-side repair cases, the correct handoff object is not "the first mutated page" but the first stable post-repair consumer

## Practical stop rule preserved
For Windows/native packed or protected startup cases, preserve this split:

1. **early tampered-view truth**
   - headers, IAT, or main-image pages appear modified
   - may indicate hook, hollowing, or other early startup mutation
2. **loader repair/remap truth**
   - loader-side logic may detect the tampering and remap/repair the main image before entry
   - this can invalidate the naive assumption that the first tampered page still governs later behavior
3. **post-repair execution truth**
   - the first payload-bearing or consequence-bearing consumer after the loader’s repair/remap decision is often the stronger anchor for later analysis

Compact operator reminder:
- do **not** equate “I saw the main image or IAT modified” with “that modified copy still owns the first real handoff”
- ask whether the loader may have switched execution onto a repaired/remapped view before the ordinary payload/consumer region becomes meaningful
- in those cases, treat the first stable post-repair module/object/consumer anchor as stronger than the earlier mutation artifact alone

## How this should affect packed-startup analysis
This note sharpens the existing packed-startup workflow in one specific way.

Existing branch memory already preserved:
- raw PE entry
- raw post-unpack transfer
- payload-bearing post-startup handoff

This note adds a narrower Windows loader-side caution:
- between visible startup tampering and later payload-bearing handoff, there may also be a **loader image-repair / remap boundary**
- therefore a tampered header/IAT view can be **evidence of attack or protection interaction** without yet being the best reusable ownership anchor for later behavior

Practical consequence:
- if the startup region shows header/IAT mutation, `NtQueryVirtualMemory(MemoryWorkingSetExInformation)`, `ProcessImageSection`, or `NtMapViewOfSection`-style repair/remap evidence, rename the current result as only **tampered-view proof** until one later post-repair consumer anchor is found
- do not stop at the tampered page if the loader is plausibly replacing or bypassing it before ordinary code takes over

## Suggested canonical wording memory
Useful compact memory line:
- in Windows/native protected startup, keep **tampered-view truth**, **loader repair/remap truth**, and **payload-bearing post-startup handoff truth** separate; a modified IAT/header page can be real evidence yet still be weaker than the first stable post-repair consumer as the later execution anchor

## Sources
- https://windows-internals.com/understanding-a-new-mitigation-module-tampering-protection/
