# Source Notes — 2026-03-16 — Result-Code / Enum-to-Policy Mapping in Mobile Targets

## Why this source note exists
This note supports a concrete mobile workflow page for a recurring practical bottleneck:
- the analyst already sees a parsed response, callback, or verdict object
- one or more ints / enums / result codes are visible
- but the first local reduction from those codes into allow / retry / degrade / challenge / block behavior is still unclear

This is not meant to become an abstract taxonomy of enums or protocol schemas.
It is meant to support a practical workflow for localizing:
- enum/result-code anchors
- packed-switch / sparse-switch / ordinal mapping sites
- normalization helpers that collapse many codes into fewer policy states
- first state writes or schedulers that make the mapping operational

## Search queries used
Search-layer (`search.py`, Grok source only on this host) was used with these exploratory queries:
- `Android reverse engineering enum result code mapping state machine challenge policy app`
- `Android reverse engineering switch enum result code callback state write mobile app`
- `protobuf enum result code mapping reverse engineering Android app challenge flow`

## Sources consulted

### 1. pbtk — Protobuf toolkit
URL: https://github.com/marin-m/pbtk
Type: tool / README / workflow reference

Most useful signals:
- supports extracting `.proto` structures from Android Java runtimes, including Lite/Nano/Micro variants and Proguarded paths
- ties generated message classes back to recovered `.proto` paths, which is operationally useful when one response object exposes enums or integer status fields but their later meaning is still unclear
- sample-driven workflow makes field and enum inspection easier by connecting captured payloads to a named schema
- explicitly notes that enum information can be surfaced while interacting with decoded message structures

Operational value for the KB:
- supports a workflow where enum/result-code localization often starts from recovered structure rather than raw bytes
- justifies a practical split between:
  - parsed object field visibility
  - enum/result-code mapping helper visibility
  - first policy-state consumer visibility

Caution:
- tool-centric source; useful for workflow grounding, not a universal statement about all mobile targets

### 2. SysDream — Reverse-engineering of protobuf-based applications
URL: https://sysdream.com/reverse-engineering-of-protobuf-based/
Type: older practitioner write-up

Most useful signals:
- shows how generated protobuf outputs may embed serialized descriptor metadata
- highlights `DescriptorPool::InternalAddGeneratedFile(...)` and descriptor recovery as a path from opaque blobs to named messages/fields
- reinforces that once structure is recovered, the analyst can stop reasoning from raw transport bytes alone

Operational value for the KB:
- supports the idea that enum/result-code work often improves dramatically once the field names or descriptor structure are recovered
- useful as provenance for the tactic: recover structure first, then localize the reduction from many fields/codes into a smaller local policy space

Caution:
- older and more descriptor-rich than some modern lite/micro Android cases

### 3. Arkadiy Tetelman — Reverse Engineering Protobuf Definitions From Compiled Binaries
URL: https://arkadiyt.com/2024/03/03/reverse-engineering-protobuf-definitiions-from-compiled-binaries/
Type: modern workflow / implementation note

Most useful signals:
- generated outputs often embed descriptor-like material that can be scanned using `.proto` strings and decoded back into source definitions
- practical scanning strategy depends on recognizing encoded descriptor boundaries and converting them back into readable schemas
- describes limits clearly: compiler choice, obfuscation, descriptor suppression, and field-order assumptions all matter

Operational value for the KB:
- strengthens the practical claim that enum/result-code localization is often easier after descriptor/schema recovery than before it
- helps justify conservative workflow guidance: when the code path is still opaque, use schema recovery as an accelerator, but do not assume it always works

### 4. Android/Dalvik bytecode references surfaced through search
Representative source surfaced by search-layer:
- Android Dalvik bytecode documentation on `packed-switch` / `sparse-switch` instruction forms

Most useful signal:
- Java/Kotlin enum or result-code branching commonly compiles down to switch-oriented bytecode shapes rather than preserving a clear high-level enum branch in decompiled output

Operational value for the KB:
- supports a concrete analyst reminder to look for:
  - `packed-switch`
  - `sparse-switch`
  - synthetic ordinal-mapping arrays
  - helper methods that translate raw codes before the switch
- useful because result-code / enum mapping frequently becomes easier in smali than in decompiler output

Limitation encountered:
- direct fetch of the Android doc hit redirect limits in this environment, so this note keeps the claim conservative and workflow-centered

### 5. Search-layer signal: Stack Overflow / JEB / practitioner material on enum-switch reconstruction
Representative surfaced URLs:
- Stack Overflow discussion on reverse engineering enum switches in Android APKs
- JEB Android analysis documentation

Most useful signal:
- reverse engineering of enum-heavy control flow often requires moving from decompiler output to bytecode/smali patterns to reconstruct switch ownership and branch meaning

Operational value for the KB:
- supports a practical page that tells analysts to stop trusting pretty-but-flattened decompiler control flow when enum/result-code ownership is the real bottleneck

Caution:
- these were weaker than the protobuf-structure sources and were mainly used as supporting workflow signal rather than primary evidence

## Practical synthesis taken from the source cluster
The strongest reusable model from this cluster is:

```text
parsed response / verdict object
  -> one or more result codes / enums / booleans become visible
  -> helper reduces raw values or sibling fields into fewer categories
  -> switch / ordinal map / branch selects policy bucket
  -> state write / scheduler / gate makes that bucket operational
  -> later allow / retry / degrade / challenge / block consequence appears
```

The important analyst lesson is:
- **visible result codes are not yet visible policy**
- the critical step is often a later reduction helper or switch boundary that collapses many low-level values into a much smaller set of business/risk states

## Concrete hook / breakpoint anchors suggested by the source cluster
These are workflow-oriented anchors, not universal internals:
- generated message / parsed model getters exposing candidate code fields
- normalization helpers that rename or collapse raw fields
- synthetic enum-switch arrays or ordinal helpers in decompiled Java/Kotlin output
- smali `packed-switch` / `sparse-switch` blocks when JADX output is too flattened
- state writes such as `setMode(...)`, `setChallengeRequired(...)`, `setRiskLevel(...)`, `updateState(...)`
- retry/backoff schedulers downstream from the mapping helper
- first request family or UI mode whose presence changes by mapping outcome

## Failure-pattern reminders supported by the source cluster
### 1. Parsed structure is visible, but behavior is still unexplained
Likely cause:
- analyst stopped at field visibility instead of following the reduction helper or switch boundary

### 2. Decompiled code looks simple, but branch ownership is still wrong
Likely cause:
- enum-switch lowering or synthetic ordinal mapping obscures the real control split
- smali-level switch reconstruction is needed

### 3. Retry/error paths are confused with trust/policy paths
Likely cause:
- several neighboring integers or enums are collapsed in the same region
- one helper classifies transient error, another classifies policy, and a third drives scheduling

### 4. Compare-runs show the same outer result code, but downstream behavior still differs
Likely cause:
- sibling fields, local context, or preexisting mode flags also participate in the reduction
- the decisive difference is the final policy bucket, not the raw visible code

## How this source note should influence KB structure
This cluster justifies a concrete page such as:
- `topics/result-code-and-enum-to-policy-mapping-workflow-note.md`

That page should emphasize:
- target pattern / scenario
- practical workflow
- where to place breakpoints/hooks
- when to move from decompiler output to smali switch reconstruction
- separation of raw result-code visibility from final policy-state consequence
- proof of consequence through state writes or later request changes

## Limits of current evidence
- the strongest accessible evidence this run was workflow/tooling oriented rather than target-specific public case studies
- direct Android bytecode documentation fetch hit redirect limits in this environment
- the present evidence is strong enough for a practical workflow note, but not for a universal theory of enum lowering across all toolchains

## Bottom line
The useful analyst object here is not merely a visible integer or enum field.
It is the concrete path from **result-code visibility to first behavior-changing policy bucket**.
That is often where Android/mobile reversing work regains traction once response parsing is no longer the main bottleneck.
