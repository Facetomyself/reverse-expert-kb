# Protocol Service-Contract Extraction and Method-Dispatch Workflow Note

Topic class: concrete workflow note
Ontology layers: practical workflow, protocol state/message recovery, contract-to-handler bridge
Maturity: practical
Related pages:
- topics/protocol-state-and-message-recovery.md
- topics/protocol-layer-peeling-and-contract-recovery-workflow-note.md
- topics/protocol-schema-externalization-and-replay-harness-workflow-note.md
- topics/protocol-parser-to-state-edge-localization-workflow-note.md
- topics/protocol-replay-precondition-and-state-gate-workflow-note.md
- topics/protocol-reply-emission-and-transport-handoff-workflow-note.md
- topics/protocol-firmware-practical-subtree-guide.md

## 1. When to use this note
Use this note when a protocol family already looks service-oriented or RPC-shaped, but the next bottleneck is still one level more concrete than broad layer peeling and one level earlier than replay-gate or parser-to-state work.

Typical entry conditions:
- one message family, framed payload family, or RPC-looking transport surface is already visible
- the analyst already suspects a service/method shell, interface roster, opcode table, or generated-stub boundary exists
- the main missing step is not broad schema shape alone, but tying one schema or request family to one callable contract surface
- the next useful output is one service shell, one representative method family, or one dispatch-bearing object that can organize later replay or trace work

Use it for cases like:
- gRPC or protobuf-backed services where the outer transport is already recognized and the useful next object is the registered service/method surface
- Windows RPC or proprietary RPC targets where interface structures, UUIDs, method tables, or dispatch arrays are more truthful than raw frames alone
- custom binary protocols where an opcode family clearly feeds one service-like dispatcher and the analyst needs one representative method path before widening analysis
- binaries that already expose registration, builder, or server-start code, but still do not yield a reusable contract object

Do **not** use this note when:
- the current object is still too layered and the real bottleneck is broad layer peeling or contract recovery
- the smallest trustworthy contract already exists and the real missing step is externalizing it into a schema or replay harness
- the service shell is already good enough and the missing edge is now the first state/reply/peripheral consequence
- replay is already structurally plausible and the real bottleneck is freshness, auth, session, or another narrow acceptance gate

In those cases, start with:
- `topics/protocol-layer-peeling-and-contract-recovery-workflow-note.md`
- `topics/protocol-schema-externalization-and-replay-harness-workflow-note.md`
- `topics/protocol-parser-to-state-edge-localization-workflow-note.md`
- `topics/protocol-replay-precondition-and-state-gate-workflow-note.md`

## 2. Core claim
A recurring protocol RE bottleneck appears after the analyst can already say:
- this family is service-oriented
- these messages probably belong to one RPC or dispatcher surface
- there is likely a method roster, registration path, or dispatch object somewhere

But the analyst still cannot yet answer:
- what is the first trustworthy service shell?
- which method slots or operations are actually exposed?
- which request/response family belongs to which slot, name, UUID, path, or opcode?

The useful next target is often not:
- another broad transport taxonomy
- a full IDL recreation
- a whole client reimplementation
- endless detached field renaming

It is:
- one service shell or interface object
- one representative method family
- one registration or dispatch anchor
- one explicit note about what still blocks live replay or consequence proof

## 3. Target pattern
The recurring pattern is:

```text
one protocol family is already visible enough to look service-oriented
  -> registration / builder / interface / dispatch surfaces exist
  -> one service shell can be externalized
  -> one representative method can be tied to one request/response family
  -> later schema, replay, or handler-consequence work becomes better targeted
```

The key discipline is:
- separate **message shape** from **service contract**
- separate **service contract extraction** from **handler consequence proof**
- stop after one representative method surface is good enough

## 4. What counts as a high-value contract-bearing object
Treat these as high-value targets:
- one registered service object
- one interface structure with stable identity such as UUID, service name, or endpoint path
- one dispatch table or method array
- one builder/register call that reveals what service becomes reachable
- one generated stub or skeleton class that ties method names to message types
- one opcode-to-handler table stable enough to act like a service roster

Treat these as useful but often too weak alone:
- “it uses protobuf” without any method or endpoint identity
- one decoded message blob with no attachment to a method shell
- guessed endpoint names with no registration or dispatch anchor
- large tables of handlers without one representative request/response family tied to them

## 5. Practical workflow

### Step 1: Freeze one representative family and one contract question
Pick one of these concrete questions only:
- which service object is being registered?
- which dispatch table owns this family?
- which method slot or endpoint path corresponds to this request family?
- which handler roster should organize later schema or replay work?

If you cannot ask one of those in a narrow way, you are still too early for this note.

### Step 2: Prefer registration and builder anchors before deep handler archaeology
Good early anchors include:
- service registration calls
- builder or server-start code
- interface-registration APIs
- generated service constructors
- endpoint-binding helpers
- dispatch-table installation paths

Strong rule:
- if the target explicitly registers the callable surface, extract that first
- do not start by individually chasing deep handlers if the service shell is still implicit
- do not stop at descriptor-bearing or reflection-visible service/method metadata alone when the live registration or bound dispatch surface is still unproved

Useful shorthand for this stage:
- described != registered != reachable

### Step 3: Externalize one service shell conservatively
Useful service-shell outputs include:
- service name and method roster
- interface UUID plus dispatch count
- endpoint path plus request/response type pairing
- opcode family plus slot count and slot-to-handler mapping

If names are weak, use stable structural labels:
- method index
- dispatch slot
- UUID
- path fragment
- opcode family

A good service shell is one that another analyst could use to target one representative method without rediscovering the whole registration path.

### Step 4: Tie one representative method to one message family
Do not stop at the shell alone.
For one representative method, tie together:
1. method identity
   - name, UUID slot, opcode, path, or dispatch index
2. request family
   - schema candidate, wrapper object, or serializer input
3. response family
   - if visible, even provisionally
4. registration or dispatch anchor
   - the place proving why this method belongs to this shell

This is the point where the contract becomes practical rather than merely structural.

### Step 5: Separate contract extraction from semantics and replay obligations
Keep these notes separate:
1. **service contract**
   - method roster, slot identity, interface shell, registration path
2. **message contract**
   - fields, schema, nesting, framing, serialization
3. **state / replay obligations**
   - auth, freshness, session phase, transport wrapping, pending-request ownership
4. **handler consequence**
   - state writes, reply selection, queue insertion, peripheral action

This separation matters because:
- you can recover one service shell before you know the fields well
- you can recover one method family before you know its state consequences
- you can know the method roster before live replay becomes acceptable

### Step 6: Build the smallest useful continuation artifact
A good first artifact is small:
- one service shell summary
- one method roster excerpt
- one dispatch-table slice
- one request/response pairing note
- one representative call fixture or harness target

Typical bad first artifacts:
- whole-client reimplementation
- speculative full IDL when only one method matters
- giant handler catalog with no representative method selected
- a perfect naming pass before one method can be exercised or traced cleanly

### Step 7: Hand off to the next narrower workflow
After one service shell and one representative method are anchored, ask what remains:
- if the method contract now needs externalized schema or serializer proof -> `protocol-schema-externalization-and-replay-harness-workflow-note`
- if the service shell is good enough and the next question is the first consequence-bearing handler edge -> `protocol-parser-to-state-edge-localization-workflow-note`
- if replay is now structurally plausible but still rejected -> `protocol-replay-precondition-and-state-gate-workflow-note`
- if accepted local handling exists but emitted output is still unclear -> `protocol-reply-emission-and-transport-handoff-workflow-note`

### Practical handoff rule
Stay on this note while the missing proof is still:
- where the service shell is registered or installed
- what the representative method roster looks like
- how one request/response family ties to one method slot or path

Leave this note once one representative method-bearing contract is already good enough and the real bottleneck becomes:
- schema externalization
- handler consequence proof
- replay acceptance
- emitted output proof

A recurring failure mode is staying too long in service-shell cataloging after one representative method is already sufficient:
- more UUID inventory
- more dispatch-slot counting
- more service-family relabeling
when the real bottleneck has already shifted into schema, consequence, or acceptance.

## 6. Breakpoint / hook placement guidance
Useful anchors for this stage:
- registration APIs and service builders
- interface dictionaries and runtime server roots
- dispatch tables and method arrays
- generated stub/skeleton classes
- endpoint-binding code
- serializer constructors attached to one method family
- handler-entry trampolines that still preserve slot identity

If traces are noisy, anchor on:
- the first registration site proving the callable shell exists
- one representative slot only
- one service object plus one request family
- one dispatch table rather than all handlers at once

## 7. Failure patterns this note helps prevent

### 1. Treating message schemas as sufficient when the callable shell is still unknown
A schema without method identity is often hard to replay, fuzz, or even trace correctly.

### 2. Treating dispatch inventory as semantic understanding
A method roster tells you what surfaces exist, not what they do.

### 3. Jumping from service discovery to whole-client reimplementation
That usually overgrows the evidence and delays the next real proof step.

### 4. Mixing handler consequence proof into contract extraction too early
First recover one service shell and one representative method.
Then localize one consequence edge.

## 8. Concrete scenario patterns

### Scenario A: gRPC binary with obvious builder/setup code
Pattern:

```text
HTTP2 transport already recognized
  -> RegisterService / builder path is visible
  -> service object and method family can be named
  -> one request/response family can be attached to one method
```

Best move:
- recover the service shell first
- then decide whether the next missing proof is schema externalization or handler consequence

### Scenario B: Windows RPC interface with sparse names but stable runtime structures
Pattern:

```text
interface structures and dispatch tables are visible
  -> UUID and slot counts are stable
  -> method names may be weak
  -> one slot can still be used as the representative contract anchor
```

Best move:
- externalize one interface shell and one representative slot by index/UUID
- do not wait for perfect names before continuing

### Scenario C: Custom opcode dispatcher acting like a private RPC shell
Pattern:

```text
one parser already reduces frames to opcode families
  -> a method-like dispatch table exists
  -> one request family consistently lands on one slot
```

Best move:
- treat the dispatcher as the service shell
- tie one opcode family to one request/response contract
- leave broader consequence work for the next note

## 9. What good output looks like
A strong result from this workflow usually contains:
- one service shell or interface summary
- one representative method family
- one registration or dispatch anchor
- one request/response pairing or message-family attachment
- one short list of remaining schema, replay, or handler-proof obligations

That is enough.
The goal is not a full IDL or client rebuild.
It is one reusable contract-bearing object.

## 10. Relationship to the broader protocol branch
This note usually sits:
- after `protocol-layer-peeling-and-contract-recovery-workflow-note`
- alongside or just before `protocol-schema-externalization-and-replay-harness-workflow-note`
- before common narrower continuations like parser/state consequence, replay gating, or output handoff

In ladder form:

```text
see the right boundary
  -> peel to one smaller trustworthy contract
  -> recover one service shell / representative method surface
  -> externalize schema or harness as needed
  -> only then debug handler consequence, acceptance, or output
```

## 11. Sources and confidence
Primary source notes for this page:
- `sources/firmware-protocol/2026-03-21-service-contract-extraction-and-method-dispatch-notes.md`
- `sources/firmware-protocol/2026-03-21-schema-externalization-and-replay-harness-notes.md`

This note is grounded in:
- gRPC registration and service-implementation anchors from the IOActive write-up
- Windows RPC interface / dispatch extraction practice from XPN and RpcView-style traversal
- API-wrapper-to-structure recovery discipline reinforced by the SpecterOps walkthrough
- schema-to-endpoint / replay bridge practice from `pbtk`
- the additional registration-vs-reachability stop rule captured in `sources/protocol/2026-03-27-service-contract-registration-vs-reachability-notes.md`

Confidence note:
- strong for the workflow shape and stop rules
- intentionally conservative about naming quality and framework universality
- does not claim that one recovered service shell alone proves semantics or replay success
