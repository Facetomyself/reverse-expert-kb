# 2026-03-22 — Runtime/init-obligation external notes

## Search framing
This note supports a protected-runtime / runtime-obligation KB pass focused on cases where:
- repaired static artifacts are under-initialized or misleading
- live/runtime state is truer than the static artifact
- replay/emulation is close-but-wrong
- the next practical target is one minimal init chain, runtime table family, or initialized-image boundary

Search was explicitly attempted via `search-layer --source exa,tavily,grok`.
Raw search artifact:
- `sources/protected-runtime/2026-03-22-runtime-init-obligation-search-layer.txt`

## Source 1: Emulating Android native libraries using unidbg
URL:
- https://bhamza.me/blogpost/2024/09/10/Emulating-Android-native-libraries-using-unidbg.html

Useful takeaways:
- unidbg is valuable precisely because it can replay JNI-shaped native logic while preserving some runtime expectations that static reimplementation loses.
- a recurring early failure mode is not “wrong algorithm” but missing runtime environment and dependency resolution (for example Android resolver / shared-library dependency setup).
- JNI-facing routines often appear callable before they are truthfully reproducible; the environment and initialization surface still matters.

KB-relevant synthesis:
- treat partial-emulation setup errors as a concrete example of init/context obligation debt, not just tool friction.
- in Android signing / protected native flows, “callable” is weaker than “truthfully initialized.”

## Source 2: Tapping into the potential of Memory Dump Emulation
URL:
- https://blahcat.github.io/2024-01-27-tapping-into-the-potential-of-memory-dump-emulation/

Useful takeaways:
- snapshot/dump-driven emulation can rebuild a workable execution environment from memory plus CPU state rather than from a pristine static image.
- the practical strength is that the dump captures a truthful already-initialized state boundary.
- the article emphasizes on-demand page materialization and faithful state restoration rather than broad static reconstruction first.

KB-relevant synthesis:
- when post-init memory is truer than the repaired binary, an initialized snapshot boundary may be the right recovery object.
- the key operator question becomes: what is the smallest truthful initialized image or state boundary worth standardizing and reusing?

## Source 3: Differential Computation Analysis: Hiding your White-Box Designs is Not Enough
URL:
- https://eprint.iacr.org/2015/753

Useful takeaways:
- white-box implementations can be attacked from dynamic traces without full structural reverse engineering.
- execution traces and memory-access behavior can expose key-dependent structure even when lookup tables are heavily obfuscated.
- the practical contribution is that runtime observation can outperform static table understanding when the latter is intentionally hostile.

KB-relevant synthesis:
- for table-heavy protected runtimes, runtime table/value/access recovery is a first-class artifact family, not a fallback after failed static cleanup.
- this supports treating “runtime-table extraction obligation” as a practical bridge page, especially when family recognition exists but offline replay still drifts.

## Source quality / limits
- The unidbg post is practitioner tutorial material, useful for concrete failure modes and setup/initialization intuition rather than universal claims.
- The memory-dump emulation post is also practitioner material, but strongly useful for the initialized-state boundary idea.
- The DCA paper is academically stronger, but it supports the runtime-trace/table-recovery direction at a higher level rather than offering the exact workflow language used by the KB.
- A Black Hat PDF candidate was fetched but `web_fetch` returned raw PDF bytes, so it was not used as a substantive source for this pass.

## Practical additions justified by these sources
These sources support strengthening the KB in four concrete ways:
1. distinguish “callable” from “truthfully initialized” in partial emulation / replay
2. treat initialized-image or snapshot boundaries as reusable recovery objects
3. elevate runtime-table extraction from ad hoc tactic to a named artifact-recovery family
4. bias toward one smallest missing init obligation rather than broad static repair when outputs are close-but-wrong
