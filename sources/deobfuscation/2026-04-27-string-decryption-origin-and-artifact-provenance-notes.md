# String Decryption Origin and Artifact-Provenance Notes — 2026-04-27

## Scope
External-research notes for a thinner deobfuscation seam: when a sample clearly has encoded / encrypted strings, the next proof object is not merely “strings recovered.” The analyst still has to preserve decoder identity, argument / origin truth, construction site truth, decoded-bytes truth, and later consumer truth as separate objects.

## Source anchors

### Mandiant / FLARE FLOSS theory and blog
Sources:
- https://raw.githubusercontent.com/mandiant/flare-floss/master/doc/theory.md
- https://cloud.google.com/blog/topics/threat-intelligence/automatically-extracting-obfuscated-strings/

Relevant points:
- String obfuscation is often used instead of full packing so sensitive resources such as domains, filenames, registry keys, dynamic imports, and other IOCs are hidden without making the whole binary look packed.
- FLOSS models the work as several separate stages: identify possible decoding routines, collect xrefs / arguments, emulate decoder functions with captured state, diff emulator memory before/after, and extract readable strings from the diff.
- The blog explicitly distinguishes strings decoded during initialization from strings decoded immediately before use.
- Traditional manual approaches are either debugger-driven forcing / dumping at decode sites or reimplementation of the decoder; both require locating the decoder and the relevant inputs first.
- Stackstrings / manually constructed strings are a separate source-shape from ordinary encoded data-section bytes.

Operator implication:
- `decoder suspected != callsite arguments recovered != decoded bytes materialized != string origin understood != consumer proved`.
- A decoded string list is useful triage, but weak provenance if the analyst cannot map a string back to its decoder callsite, construction site, or first behavior-bearing consumer.

### Tim Blazytko / synthesis.to — Binary Ninja Mirai string-decryption automation
Source:
- https://synthesis.to/2021/06/30/automating_string_decryption.html

Relevant points:
- The workflow starts by noticing repeated encoded strings passed as parameters to one function.
- Manual analysis reduces the function to a `strlen` / allocation / copy / XOR loop, then identifies the XOR key.
- Automation uses Binary Ninja HLIL to walk callers of the target function, identify call instructions, parse specific parameters, and decrypt bytes until a null terminator while tracking already-decrypted addresses.
- The practical payoff is not just a string list: decoded default credentials make the surrounding scanner logic understandable.

Operator implication:
- When callsite structure is stable, parameter-to-decoder mapping can be a stronger provenance object than generic binary-wide string recovery.
- Decoding in-place in the database should still preserve original address / callsite notes; otherwise later static understanding may overread the plain text as if it were originally present.

### 0ffset Training Solutions — Capstone / Unicorn stack-string emulation
Source:
- https://www.0ffset.net/reverse-engineering/capstone-resolving-stack-strings/

Relevant points:
- The hard case is not only “find encrypted bytes”; stack strings may be built dynamically before decryption.
- Polymorphic per-string routines can change constants, instruction forms, and arithmetic shapes, making direct static pattern replication brittle.
- The writeup uses Capstone for finding / slicing and Unicorn for raw instruction emulation, explicitly because higher-level OS context is not needed for that local byte transformation.
- The Emotet example explains why dynamic sandbox observation may see only a few C2s while many more are available through emulating the deobfuscation functions.

Operator implication:
- `data-section encrypted bytes != stack-built bytes != emulated decoded output`.
- For stack-built or polymorphic string routines, preserve construction site and slice boundary before trusting decoded output as complete.
- Emulation can be the cheapest bridge when static algebra keeps changing but the local instruction slice is bounded.

### Zscaler ThreatLabz — Pikabot string deobfuscation
Source:
- https://www.zscaler.com/blogs/security-research/automating-pikabot-s-string-deobfuscation

Relevant points:
- Pikabot decrypts strings only when required, not all at once.
- The string path includes stack-pushed encrypted arrays, per-string RC4 keys, Base64 normalization, AES-CBC, and a sample-level AES key / IV.
- The extraction workflow distinguishes AES key / IV extraction, encrypted-array extraction, array-size extraction, and RC4-key extraction.
- The RC4 key extraction approach changed after naive “near initialization” extraction produced false keys; the final approach tested candidate strings and validated output size / readability, then marked keys as consumed to limit false positives.

Operator implication:
- `key material found != correct key for this string != encrypted array reconstructed != decoded string valid != current-use consumer proved`.
- Validation checks such as expected size and printable output are useful but only prove decode plausibility; they do not by themselves prove the decoded string drives the later behavior of interest.

## Durable synthesis
The thinner workflow seam worth preserving is:

```text
decoder candidate found
  != decoder callsite / slice selected
  != origin bytes or stack-built bytes reconstructed
  != key / IV / immediate constants paired to this artifact
  != decoded bytes materialized and validated
  != artifact provenance preserved
  != first behavior-bearing consumer proved
```

The KB already had a page for `decrypted artifact -> first consumer`. This run adds the missing upstream stop rule: before consumer proof, string recovery itself needs provenance discipline. Otherwise plain-text artifacts become seductive but ambiguous evidence.

## Practical tactics to preserve
- Classify each recovered string by origin shape: static data bytes, stack-built bytes, runtime heap/global construction, emulator memory diff, or debugger dump.
- Keep decoder identity separate from argument / key / construction-site truth.
- Prefer callsite-argument extraction when the decoder is stable and heavily referenced.
- Prefer bounded emulation when per-string arithmetic or stack construction makes static reimplementation brittle.
- Treat printable/expected-size output as decode-plausibility proof, not consumer proof.
- Preserve original address, callsite, stack offset, key/IV source, and decoded-output address so the next analyst can tie the string to a first ordinary consumer instead of only a flat IOC list.
