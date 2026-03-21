# Source Notes — 2026-03-21 — Schema externalization / replay-harness generation for protocol recovery

## Source set
Search mode and policy:
- explicit multi-source search via `search-layer` with `--source exa,tavily,grok`
- queries centered on protocol reverse engineering, schema extraction, service-contract recovery, and replay-harness generation

Primary retained sources reviewed:
- <https://netzob.org/>
- <https://people.eecs.berkeley.edu/~dawnsong/bitblaze/protocol.html>
- <https://arkadiyt.com/2024/03/03/reverse-engineering-protobuf-definitiions-from-compiled-binaries/>
- <https://github.com/marin-m/pbtk>
- <https://github.com/mildsunrise/protobuf-inspector>
- supportive search-only signals from FieldHunter / BinPRE / DynPRE / FUBOToRP style results

Existing KB materials consulted for fit:
- `topics/protocol-layer-peeling-and-contract-recovery-workflow-note.md`
- `topics/protocol-content-pipeline-recovery-workflow-note.md`
- `topics/protocol-firmware-practical-subtree-guide.md`
- `topics/protocol-state-and-message-recovery.md`

## Why this source cluster was chosen
The protocol / firmware branch already had strong practical coverage for:
- capture-failure diagnosis
- socket/plaintext boundary relocation
- layer peeling into a smaller trustworthy contract
- content-pipeline continuation
- receive ownership, parser/state consequence, replay gating, and output handoff

But there was still a thinner practical gap between:
- **recovering one smaller contract**, and
- **replaying or automating against that contract outside the target**.

This source cluster helps answer a narrower operator question:
- once one protobuf/TLV/RPC-like contract is partly visible, how do you externalize it into one schema or service-contract artifact and one replay/fuzz harness target without pretending you already understand the whole protocol?

## Strong recurring ideas

### 1. Automatic PRE work is valuable mainly when it yields a reusable interaction object
The Berkeley/BitBlaze material frames protocol reverse engineering as useful because it enables:
- protocol analyzers
- application dialogue replay
- monitoring / filtering
- behavioral understanding

That is important because it keeps the operator goal practical:
- the useful stopping point is often not “perfect protocol inference”
- it is one externalized object that can drive replay, comparison, simulation, or fuzzing

### 2. Netzob is strong evidence for the message-format -> grammar -> simulation chain
Netzob’s own framing is unusually aligned with the KB’s practical bias:
- infer message vocabulary / format
- infer grammar / state machine
- use the model for simulation / traffic generation / fuzzing

This is valuable not because the tool must be used literally in every case, but because it validates a durable workflow shape:
- **format recovery should hand off into a reusable simulator/replay target, not remain trapped as analyst-private notes**

### 3. Embedded descriptor metadata can short-circuit blind schema reconstruction
Arkadiy Tetelman’s protobuf descriptor-recovery write-up is high-signal because it shows a very concrete shortcut:
- generated binaries often retain descriptor-like metadata
- searching for `.proto` names and valid `FileDescriptor`-shaped byte regions can recover full source-like `.proto` definitions
- once that exists, the analyst no longer needs to guess field layout from isolated blobs alone

Practical consequence:
- if one payload family is protobuf-shaped, do not stay stuck in blind wire-format interpretation longer than necessary
- check whether the target binary or generated output already contains descriptor-bearing artifacts that can be externalized directly

### 4. Unknown-message inspection is good enough to bootstrap a provisional schema
`protobuf-inspector` is useful because it embraces the intermediate state:
- unknown protobuf blobs can still be parsed structurally without a definition
- field names are missing, but nesting, scalar/repeated shape, and wire-type hints are already useful
- iterative field definition refines the parse until the parser no longer has to guess

Practical consequence:
- one provisional schema can be built iteratively from stable shape, not from business-name certainty
- this matches the KB’s “names are commentary, shape is truth” bias

### 5. PBTK adds the missing operator bridge from recovered schema to endpoint manipulation
PBTK is especially valuable because it is not just a parser aid:
- it extracts protobuf structures from APKs / binaries into readable `.proto`
- it supports editing, replaying, and fuzzing protobuf-backed endpoints
- it treats extracted schema as a live manipulation surface rather than dead documentation

That makes it the clearest practical bridge in this run’s source set between:
- **contract recovery**, and
- **harness generation / replay experimentation**.

### 6. Service-contract externalization is often more valuable than exhaustive semantics
Across the sources, a strong rule emerges:
- if you can externalize one message family, method shell, or schema candidate well enough to serialize, deserialize, mutate, and resend it,
- that is often more useful than spending another long pass inventing perfect field names or full state taxonomy first.

### 7. Harness construction should stay representative, not premature-general
A useful anti-drift lesson from this source set:
- the first good harness should normally cover one representative message family or service path
- not a whole client reimplementation
- not a broad protocol emulator
- not speculative support for every field and branch

The right first output is usually:
- one schema/service artifact
- one serializer/deserializer proof
- one replay/edit/fuzz harness target
- one clear note about remaining gates or state assumptions

## Concrete operator takeaways worth preserving

### A. Externalization-first decision rule
When one protocol object is already peeled enough to inspect, ask:
1. can I externalize this as one schema, descriptor, message model, or service/method shell?
2. can that artifact drive serialization/deserialization outside the target?
3. can I mutate or replay one representative family with it?

If yes, stop broad layer-peeling and produce the artifact.

### B. Descriptor-shortcut rule for protobuf-shaped targets
For protobuf-shaped families:
1. search binaries, generated code, or resources for embedded descriptors / `.proto` strings / reflection metadata
2. if descriptors exist, recover them before doing more blind blob inference
3. only fall back to iterative unknown-message reconstruction when the descriptor path is absent or incomplete

### C. Provisional-schema workflow
When the descriptor path is unavailable:
1. gather one representative blob family
2. inspect unknown messages structurally
3. preserve field numbers, wire types, nesting, optional/repeated behavior, and compare-run shape
4. write a provisional schema with intentionally generic names if needed
5. keep refining until round-trip parsing is stable enough for replay

### D. Harness-minimum workflow
A minimal good handoff looks like:
1. one externalized schema or service-contract artifact
2. one serializer/deserializer round-trip proof
3. one replay/edit/fuzz surface for a representative request or response family
4. one note about remaining replay gates, auth obligations, or session/state assumptions

### E. Stop-rule against taxonomy drift
Once one representative contract can be externalized and exercised outside the target:
- stop broad contract narration
- stop renaming fields for style
- stop pretending the branch still needs generic “protocol structure” discussion
- move into replay-gate, send-boundary, or artifact-automation follow-up instead

## Candidate KB implications
This batch strongly supports a missing practical rung in the protocol / firmware subtree:
- a workflow note between `protocol-layer-peeling-and-contract-recovery` and `protocol-replay-precondition-and-state-gate`
- focused on **schema / service-contract externalization and minimal replay-harness generation**

Likely parent-page implications:
- protocol branch memory should explicitly remember that one smaller trustworthy contract is sometimes only truly useful once it is externalized into a reusable artifact
- firmware/protocol parent framing should mention that some cases stall not on visibility or parser discovery, but on failing to convert a recovered contract into an external tool/harness surface

## Confidence / quality note
This source set is strong because it does not merely restate old PRE taxonomy.
It supports a specific operator bridge the KB was still thin on:
- from visible layered contract
- to externalized schema/service artifact
- to one representative replay/fuzz harness target
- with conservative stop rules and without overclaiming full protocol understanding.
