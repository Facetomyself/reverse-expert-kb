# Run Report — 2026-03-17 13:31 Asia/Shanghai — Manual ingest overview for `Facetomyself/sperm` `md/`

## Summary
This run manually triggered the reverse-KB workflow in **A mode**: full scan of the target repository subdirectory, with the goal of producing a **source archive overview and thematic inventory first**, without prematurely merging content into canonical topic pages.

The scoped source was:
- <https://github.com/Facetomyself/sperm/tree/main/md>

The run found **173 Markdown files** under `md/` and recorded them as a practical feeder source for later extraction.

## Scope this run
- manually inspect the target GitHub repository subdirectory
- enumerate the article corpus under `md/`
- characterize the collection at a theme/bucket level
- preserve provenance in a source note under `sources/`
- write a run report documenting the ingest decision
- avoid modifying canonical topic pages until a second-pass extraction selects high-signal material

## New findings
### 1. The source is large enough to justify staged ingest
The repository subdirectory contains **173 Markdown files**, which is too large for reliable one-shot canonicalization.

### 2. The corpus is strongly practical and mobile-weighted
The biggest visible cluster is Android/mobile practical reversing, with heavy overlap among:
- app-specific sign/parameter analysis
- Frida/hook practice
- anti-debug and anti-instrumentation handling
- traffic capture / interception / transport ownership
- mixed protected-runtime and obfuscation cases

### 3. Browser and anti-bot material is present enough to matter
The corpus also contains a meaningful browser/JS slice, including Cloudflare, browser environment patching, fingerprinting, AST, debugger resistance, and broader anti-bot automation material.

### 4. Protected-runtime mining looks especially promising
VM, OLLVM, flow-flattening, white-box AES, DFA, anti-debug, and mixed code-protection material appear frequently enough that this source could feed the KB’s protected-runtime/deobfuscation practical branch.

### 5. This source is better treated as a reservoir than a single voice
The repository reads like an accumulated article bank rather than one stable canonical source. That means later extraction should be selective and workflow-centered rather than wholesale.

## Sources consulted
- `research/reverse-expert-kb/README.md`
- `research/reverse-expert-kb/index.md`
- recent run report: `research/reverse-expert-kb/runs/2026-03-17-1233-native-practical-branch-sequencing-pass.md`
- external repository scanned this run:
  - <https://github.com/Facetomyself/sperm/tree/main/md>

## Reflections / synthesis
The right move here was **not** to immediately merge dozens of repo articles into the KB.

That would create two failure modes:
- source-noise inflation
- canonical-page drift driven by article titles rather than stable operator bottlenecks

Instead, this run converts the repo into a traceable staged source:
- full manifest preserved
- rough theme distribution captured
- likely high-yield follow-up candidates identified
- canonical topic edits deferred until a narrower extraction pass

## Candidate topic pages to create or improve
No canonical topic pages were edited this run.

Likely later targets after second-pass extraction include:
- browser-runtime subtree notes
- mobile protected-runtime practical notes
- network/protocol receive-path or transport-ownership notes
- deobfuscation/protected-runtime workflow notes
- selective iOS workflow pages if the source material turns out to be deeper than title-level suggests

## Next-step research directions
Recommended manual follow-up modes from this source:
1. **Android / protected-runtime pass** — prioritize VM, anti-debug, Frida-detection, sign/parameter recovery, transport ownership, and protection-specific writeups
2. **Browser / JS pass** — extract environment patching, anti-bot workflow, cookie/signature generation, AST deobfuscation, debugger resistance
3. **Protocol/network pass** — isolate protobuf/grpc/quic/app-protocol material
4. **iOS pass** — inspect the small but potentially dense iOS subset separately

## Concrete scenario notes or actionable tactics added this run
This run did not add a new canonical workflow note.
It did add a practical workflow rule for source handling:
- when a repo-sized article bank is large and heterogeneous, preserve it first as a staged source overview instead of forcing immediate canonical integration

## Files changed this run
- `research/reverse-expert-kb/sources/community-repos/2026-03-17-sperm-md-ingest-overview.md`
- `research/reverse-expert-kb/runs/2026-03-17-1331-sperm-md-manual-ingest-overview.md`

## Outcome
The reverse KB now has a traceable staged-ingest record for the `Facetomyself/sperm` repository’s `md/` corpus, ready for narrower second-pass extraction by subtheme.
