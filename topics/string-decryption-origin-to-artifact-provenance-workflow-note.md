# String Decryption Origin to Artifact-Provenance Workflow Note

Topic class: concrete workflow note
Ontology layers: protected-runtime practice branch, deobfuscation workflow, artifact-provenance bridge
Maturity: structured-practical
Related pages:
- topics/obfuscation-deobfuscation-and-packed-binaries.md
- topics/decrypted-artifact-to-first-consumer-workflow-note.md
- topics/runtime-table-and-initialization-obligation-recovery-workflow-note.md
- topics/vm-trace-to-semantic-anchor-workflow-note.md
- topics/packed-stub-to-oep-and-first-real-module-workflow-note.md
- topics/malware-config-to-capability-bucket-workflow-note.md

## 1. Why this page exists
This page exists because the deobfuscation branch needs a smaller upstream stop rule before the existing `decrypted-artifact-to-first-consumer` workflow.

A common malware / protected-runtime state is:

```text
encoded strings are clearly present
  + a decoder candidate, stack-string builder, or emulator output is visible
  + tools can produce a tempting plaintext list
  -> but the analyst still cannot say which decoder callsite, origin bytes, key material, or construction site owns each recovered string
  -> and therefore cannot safely route one recovered artifact to the first behavior-bearing consumer
```

This is not the same as broad deobfuscation or artifact-consumer proof.
It is the narrower task of turning **string recovery output** into a provenance-preserving artifact that can survive later static cleanup, config extraction, request-builder proof, or IOC reporting.

## 2. Target pattern / scenario
Use this note when most of these are true:
- ordinary `strings` output is weak, sparse, or misleading
- encoded / encrypted / stack-built strings are visible or strongly suspected
- one or more decoder helpers, stack-build slices, or emulator-diff outputs exist
- automated tools or scripts can recover plaintext, but provenance is shallow
- the next useful object is not every string; it is one string family with origin, decoder, key/constant, decoded bytes, and consumer-ready metadata preserved

Representative cases:
- a stable decoder is called from many sites with encoded-string pointers or immediate arguments
- stack strings are built with MOV / copy sequences, then transformed locally
- per-string routines use similar arithmetic with changed constants or instruction forms
- layered string protection uses per-string RC4 keys plus shared AES / IV material
- runtime-only decoding means sandbox output sees only the subset exercised by the run

## 3. Core claim
Recovered plaintext is not automatically trustworthy reverse-engineering evidence.

Preserve this ladder:

```text
decoder candidate found
  != decoder callsite / slice selected
  != origin bytes or stack-built bytes reconstructed
  != key / IV / immediate constants paired to this artifact
  != decoded bytes materialized and validated
  != artifact provenance preserved
  != first behavior-bearing consumer proved
```

The practical goal is to create one provenance-preserving decoded artifact record:

```text
encoded origin -> decoder/slice -> key/constants -> decoded output -> storage/output address -> first-consumer candidate
```

Only after that should the case move to broader artifact-consumer proof.

## 4. What counts as artifact provenance
Minimum useful provenance for one decoded string family:
- **origin shape**: data-section bytes, stack-built bytes, heap/global construction, emulator memory diff, debugger dump, or tool output
- **origin locator**: address, stack offset, data object, callsite, or construction slice
- **decoder owner**: helper function, inlined loop, per-string routine, or emulated slice
- **input pairing**: arguments, length, key, IV, immediate constants, or candidate key source
- **materialization proof**: output address / buffer, before-after memory diff, return value, or database patch/comment
- **validation reason**: printable output, expected size, expected encoding, known config grammar, or cross-run consistency
- **consumer candidate**: the first callsite, parser, request builder, config reducer, import resolver, or capability path likely to use the output

Bad provenance:
- a flat plaintext list with no origin address
- a recovered IOC with no decoder or callsite tie-back
- an emulator output not tied to a concrete slice boundary
- a debugger dump that cannot be mapped back to the run path that produced it
- an in-place database patch that destroys original encrypted bytes without comments or sidecar notes

## 5. Practical workflow

### Step 1: classify the origin shape
Before decoding everything, label the string source:

```text
origin shape:
  static encoded bytes | stack-built bytes | runtime heap/global construction | emulator diff | debugger dump
```

Why this matters:
- static encoded bytes usually favor xref and argument extraction
- stack-built bytes require construction-site reconstruction before decode claims
- emulator diffs need slice boundaries and input state snapshots
- debugger dumps need run-path and timing provenance

### Step 2: choose one string family tied to one later question
Do not start with the whole plaintext list.
Choose one family likely to explain a later effect:
- C2 / URL / route strings
- registry / filesystem / service names
- dynamic import names
- command / task names
- config keys or mode strings
- credential / scanner dictionaries

Scratch note:

```text
later question:
  which request family / capability / config bucket does this string family explain?

string family:
  ...
```

### Step 3: freeze decoder identity separately from callsite truth
For stable helper cases:
- locate the candidate decoder
- enumerate xrefs / callers
- record which argument positions carry encoded bytes, lengths, keys, or output buffers

For inlined or per-string cases:
- record the local slice boundary
- preserve the construction / transformation block before trying to generalize

Do not collapse:

```text
decoder-like function exists
  != this callsite passes this encoded artifact
  != this invocation produced this decoded output
```

### Step 4: reconstruct origin bytes before trusting decoded bytes
For data-section bytes:
- record address and length source
- note whether the length is null-terminated, immediate, table-derived, or computed

For stack-built bytes:
- reconstruct all writes into the stack/object region
- preserve write order when it matters
- record whether the string is complete before the transform loop starts

For emulator-diff output:
- save before / after memory ranges
- note the instruction budget and stop condition
- label which output range changed into readable bytes

### Step 5: pair key / IV / constants to this artifact
Key material is a separate proof object.

Examples:
- one global XOR constant
- per-string immediate arithmetic constants
- per-string RC4 key
- shared AES key / IV plus per-string wrapping layer
- key candidate selected by readability / expected-size validation

Do not collapse:

```text
key-like string found
  != correct key for this artifact
  != correct key for this run
  != key consumed by the later behavior of interest
```

### Step 6: materialize and validate plaintext conservatively
Validation can include:
- printable ASCII / UTF-16 output
- expected length
- expected URL / path / import / config grammar
- repeated decode consistency across callsites
- match with a known source-code family or public case only when provenance supports it

Treat validation as decode plausibility, not consumer proof.
A string can be correctly decoded and still be dead, decoy, unused in this branch, or only one candidate among many.

### Step 7: preserve output in a consumer-ready form
Good output record:

```yaml
string_id: family.local_index
origin_shape: stack-built bytes
origin_locator: function + stack range + construction block
encoded_bytes: ...
decoder_owner: function/slice
key_or_constants: ...
decoded_output: ...
output_locator: buffer/register/address/database comment
validation: printable + expected length + grammar
consumer_candidate: first parser/request/config/import-resolution site
confidence: high|medium|low
```

Use database comments, sidecar JSON/Markdown, labels, or scripts, but keep original bytes and provenance recoverable.

### Step 8: hand off to first-consumer proof
Once provenance is stable, move to:
- `topics/decrypted-artifact-to-first-consumer-workflow-note.md`

The next question becomes:

```text
which first ordinary consumer turns this decoded string family into behavior?
```

Not:

```text
how many more strings can I dump?
```

## 6. Common patterns

### A. Stable decoder with many callsites
Best proof object:
- decoder function + caller list + argument positions + decoded output sidecar

Tactics:
- use xrefs / HLIL / microcode / decompiler API to enumerate calls
- parse specific parameters rather than grep for all data bytes
- keep already-decoded address tracking so repeated strings do not inflate confidence

### B. Stack-built string plus local transform
Best proof object:
- construction slice + transform slice + emulated output

Tactics:
- recover all stack writes before the transform loop
- use bounded emulation when arithmetic variants make static replication brittle
- preserve slice start/stop and initial register/memory assumptions

### C. Layered per-string crypto
Best proof object:
- per-string encrypted array + per-string key + shared key/IV + validation checks

Tactics:
- separate array extraction, size extraction, key extraction, and shared-material extraction
- validate output with length/readability/grammar, but record that this is still decode plausibility
- avoid assuming a nearby key-looking string is the right key without testing

### D. Runtime-only decode near use
Best proof object:
- run-path-specific decoder invocation + output buffer + immediate next consumer candidate

Tactics:
- use debugger hooks or trace slices close to the use site
- compare exercised vs unexercised string families
- record trigger conditions so dynamic coverage is not overread as full inventory

## 7. Failure modes

### Failure mode 1: flat IOC list with no tie-back
Likely cause:
- tool output was treated as final evidence.

Next move:
- sample one high-value string and reconstruct origin -> decoder -> decoded-output provenance before using it in reporting or consumer proof.

### Failure mode 2: decoder found, but decoded output is incomplete
Likely cause:
- stack construction, length source, or per-string key pairing was not preserved.

Next move:
- move upstream to origin reconstruction and key/constant pairing before broad automation.

### Failure mode 3: dynamic run sees only a subset of strings
Likely cause:
- decode is near-use or branch-gated.

Next move:
- label coverage as run-path-specific; use xrefs, forced invocation, emulation, or alternate triggers to recover unexercised families.

### Failure mode 4: plaintext patched into the database, later analysis forgets it was decoded
Likely cause:
- convenience patching erased provenance.

Next move:
- keep comments / sidecar records with origin bytes, decoder, and callsite before propagating names or IOCs.

## 8. Handoff rules
Stay on this page while the missing object is:
- decoder/callsite truth
- origin-byte or stack-construction truth
- key/constant pairing truth
- decoded-output validation
- artifact provenance

Leave this page when:
- one string family has reliable provenance and the real bottleneck is its first behavior-bearing consumer
- the case is no longer string-specific and has become broader recovered-artifact or config-to-capability proof
- the remaining problem is ordinary route-to-state, protocol parser, request builder, or malware capability mapping

Likely next pages:
- `topics/decrypted-artifact-to-first-consumer-workflow-note.md`
- `topics/malware-config-to-capability-bucket-workflow-note.md`
- `topics/malware-request-builder-to-send-boundary-workflow-note.md`
- `topics/protocol-parser-to-state-edge-localization-workflow-note.md`
- `topics/native-interface-to-state-proof-workflow-note.md`

## 9. Source footprint / evidence note
This note is grounded in:
- `sources/deobfuscation/2026-04-27-string-decryption-origin-and-artifact-provenance-notes.md`
- Mandiant / FLARE FLOSS theory and blog material
- Tim Blazytko's Mirai / Binary Ninja string-decryption automation writeup
- 0ffset's Capstone / Unicorn stack-string emulation writeup
- Zscaler's Pikabot string-deobfuscation writeup

The evidence supports a conservative operator rule:
- decoded strings are valuable, but only provenance-preserving decoded strings are durable reverse-engineering evidence.

## 10. Topic summary
String decryption origin-to-artifact provenance is the upstream deobfuscation workflow that keeps decoder identity, callsite/slice truth, origin bytes, key/constant pairing, decoded output, and consumer-ready metadata separate.

It prevents a common failure: treating a flat plaintext string list as if it already proved current artifact ownership or later behavior.
