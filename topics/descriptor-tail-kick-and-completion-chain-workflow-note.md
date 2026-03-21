# Descriptor-Tail Kick and Completion-Chain Workflow Note

Topic class: concrete workflow note
Ontology layers: practical workflow, protocol/firmware context bridge, transport-to-hardware consequence bridge
Maturity: practical
Related pages:
- topics/protocol-firmware-practical-subtree-guide.md
- topics/protocol-reply-emission-and-transport-handoff-workflow-note.md
- topics/peripheral-mmio-effect-proof-workflow-note.md
- topics/isr-and-deferred-worker-consequence-proof-workflow-note.md
- topics/firmware-and-protocol-context-recovery.md
- topics/protocol-state-and-message-recovery.md
- topics/runtime-behavior-recovery.md

## 1. When to use this note
Use this note when a protocol / firmware case is already far enough along that:
- one request/reply family or service command is isolated
- local acceptance and some reply-building logic are already visible
- serializer, queue, descriptor, ring, or mailbox structures are already suspected
- but the analysis still stalls because the first **commit-to-device** edge is smeared across:
  - descriptor preparation
  - producer/consumer index updates
  - doorbell / notify / enable writes
  - later completion interrupt or deferred-worker handling

Typical cases:
- virtqueue, DMA ring, mailbox, or descriptor-driven devices where reply-object creation is visible but the useful proof is the first tail/kick/notify edge
- firmware where queue fill helpers are visible, but the decisive effect is not the buffer fill alone and not the later ISR alone
- embedded services where output-side proof needs one concrete chain from accepted protocol state -> descriptor-visible commit -> completion-driven durable consequence
- rehosting or harness work where the model is "close" but still misses exactly when software hands ownership to hardware and when completion returns ownership to software

Do **not** use this note when the real bottleneck is earlier:
- the message family is still unclear
- replay is still failing because local acceptance/preconditions are unproved
- there is no credible queue/ring/descriptor candidate yet
- the first hardware-facing write itself is still totally unknown and there is no output-side chain yet

In those cases start with:
- `topics/protocol-replay-precondition-and-state-gate-workflow-note.md`
- `topics/protocol-reply-emission-and-transport-handoff-workflow-note.md`
- `topics/peripheral-mmio-effect-proof-workflow-note.md`

## 2. Core claim
A recurring late-stage protocol / firmware bottleneck is that analysts stop at the wrong boundary.

They stop at one of these too early:
- local reply-object creation
- a serializer/helper that only prepares a descriptor
- seeing a ring structure in memory
- the first MMIO write without proving what it commits
- the first interrupt without proving what it completes

The more useful target is usually a **descriptor-tail kick and completion chain**:

```text
accepted protocol path
  -> descriptor or ring entry becomes materially valid
  -> producer/tail/doorbell/notify edge commits hardware-visible ownership
  -> device progresses / DMA consumes / transmit launches
  -> completion interrupt or deferred worker reduces that fact into durable software consequence
```

That chain is often the smallest trustworthy proof object for output-side and hardware-side cases.

## 3. Why this note exists
The KB already had good adjacent notes for:
- reply-emission / transport handoff
- peripheral/MMIO effect proof
- ISR/deferred-worker consequence proof

What was still implicit was the specific seam where those three notes often meet in descriptor-driven systems:
- **buffer fill is not yet commit**
- **tail/producer/notify is often the first hardware-visible commit**
- **completion interrupt/workqueue is often the first durable software-side proof that the earlier kick really mattered**

This note preserves that seam as one reusable operator move instead of forcing analysts to rediscover it across driver, firmware, and DMA-heavy targets.

## 4. Target pattern
The recurring target pattern is:

```text
request or command family visible
  -> local reply/build path visible
  -> one descriptor/ring/mailbox object becomes populated
  -> one tail/producer/doorbell/notify/enable edge commits it
  -> one completion/ISR/deferred path proves downstream consequence
```

The key discipline is:
- separate **descriptor preparation** from **descriptor commit**
- separate **hardware-visible kick** from **later durable software consequence**
- prove one narrow chain instead of cataloging every ring field or ISR branch

## 5. What counts as the commit edge
Treat these as high-value candidates:
- producer index / tail pointer / head advance that differs across a representative compare pair
- doorbell / notify / queue-enable / transmit-poll-demand write that only occurs on successful output runs
- ownership-bit or valid-bit transition that changes a descriptor from prepared to consumable
- final length / address / flags write immediately followed by tail advance or notify
- mailbox enqueue or slot publish step that makes the object visible to hardware/peer logic

Treat these as useful but often one layer too early:
- internal reply object construction
- buffer allocation alone
- descriptor field writes that occur in both successful and stalled runs before publish/kick
- broad ring-structure labeling without one proved publish edge

## 6. What counts as the completion side of the chain
Treat these as strong downstream proof surfaces:
- ISR entry or completion callback only reachable after the publish/kick edge
- status writeback, used-index advance, descriptor reclaim, or completion bit set
- deferred worker / bottom-half / tasklet / workqueue callback that performs one durable state write or wakeup
- reply-visible send-complete, queue-drain, retry release, or scheduler wake that only happens when the earlier kick succeeded

Treat these as useful but often one layer too early:
- broad interrupt-mask setup
- generic polling loops without one state reduction
- merely seeing a completion register read with no proven later consequence

## 7. Practical workflow

### Step 1: Freeze one compare pair around publish vs no-publish
Good pairs include:
- same accepted request where one run reaches producer-tail update and later completion, while the other builds the descriptor but never publishes it
- same command family where one run performs doorbell/notify and later emits or completes, while the other stalls earlier
- same descriptor fill sequence under two states where only one side advances used/completion state later

Record only:
- request family
- already-known acceptance boundary
- candidate descriptor/ring object
- candidate publish/kick edge
- later completion-side difference

### Step 2: Mark six boundaries explicitly
Before expanding ring taxonomy, mark:
1. **acceptance boundary** — request is locally accepted
2. **descriptor-preparation boundary** — object fields are being filled
3. **publish boundary candidate** — owner/valid/tail/producer/doorbell change
4. **hardware-progress boundary** — DMA/read/consume/transmit appears possible or observable
5. **completion boundary** — interrupt/status/used-index/completion callback becomes reachable
6. **durable consequence boundary** — later state write, wakeup, reply-visible completion, or policy/scheduler change

This prevents "we found the ring" from being mistaken for "we proved the chain".

### Step 3: Prefer the first publish edge over complete descriptor semantics
When there are many descriptor fields, prioritize the first edge that changes ownership or visibility:
- tail increment
- producer index write
- doorbell/notify write
- valid/owner bit change
- queue-enable after fill

A perfect descriptor layout is often less valuable than one proved publish edge.

### Step 4: Tie the publish edge to one downstream completion fact
Do not stop at "this looks like a tail pointer".

Prove the candidate with one downstream fact such as:
- only runs with that edge reach ISR/completion/deferred handling
- only runs with that edge show used-index/status writeback
- only runs with that edge later emit the reply or wake the waiting consumer
- the first divergence between successful and stalled runs is publish/kick, not earlier descriptor fill

### Step 5: Reduce the completion side to one durable consequence
After finding ISR or deferred logic, ask:
- where does completion become one durable state transition?
- where is the first descriptor reclaim, reply-complete bit, pending-slot release, or wakeup?
- which one reduction actually predicts later observable behavior?

Useful local role labels:
- `reply-build`
- `descriptor-fill`
- `publish`
- `doorbell`
- `hardware-progress`
- `completion`
- `reclaim`
- `wake/reply-complete`

### Step 6: Hand the chain back to one next task
Once one chain is proved, route it into only one next task:
- rehosting model refinement for ring/doorbell/completion realism
- narrower serializer or framing recovery
- completion-side scheduler / wakeup modeling
- one representative harness experiment around publish timing or completion conditions

Do not widen immediately into full driver taxonomy.

## 8. Common failure patterns this note prevents

### 1. Treating descriptor fill as transmit proof
Filled descriptors are often not yet consumable until one ownership/tail/notify edge occurs.

### 2. Treating one MMIO write as sufficient without publish semantics
A register write matters more when it is shown to publish or kick the prepared object, not merely when it touches the same block.

### 3. Treating ISR visibility as enough without tying it back to publish
A later interrupt is useful only when linked to the earlier publish edge and one durable consequence.

### 4. Over-modeling ring fields before one compare pair is stable
Representative publish-vs-no-publish pairs are usually more valuable than a full inferred ring schema.

### 5. Smearing transport, MMIO, and completion into one blob
This note preserves a cleaner chain:
- prepare
- publish/kick
- complete
- reduce consequence

## 9. Concrete scenario patterns

### Scenario A: Reply built, but tail advance is the real commit
Pattern:

```text
request accepted
  -> output buffer filled
  -> descriptor fields written
  -> only one run advances producer/tail
  -> only that run later completes or emits
```

Best move:
- anchor on the first producer/tail change, not reply-object construction.

### Scenario B: Doorbell write matters more than descriptor semantics
Pattern:

```text
descriptor looks valid in both runs
  -> only one run performs notify/doorbell write
  -> later used-index or interrupt appears only there
```

Best move:
- treat notify as the decisive publish edge.

### Scenario C: MMIO write exists, but completion worker holds the durable proof
Pattern:

```text
publish edge exists
  -> interrupt fires
  -> durable consequence only appears in deferred worker
```

Best move:
- keep the earlier publish edge, but use the worker’s first reclaim/wakeup/state reduction as proof-of-consequence.

## 10. Relationship to nearby pages
- `topics/protocol-reply-emission-and-transport-handoff-workflow-note.md`
  - use that when the output-side problem is still proving the first committed outbound path in general
- `topics/peripheral-mmio-effect-proof-workflow-note.md`
  - use that when the first hardware-facing effect is still the main unknown and descriptor-publish structure is not yet stabilized
- `topics/isr-and-deferred-worker-consequence-proof-workflow-note.md`
  - use that when publish/kick is already good enough and the remaining uncertainty is later inside completion/deferred consequence proof

This note is the seam between them when one case specifically needs:
- descriptor/ring publish proof
- and one linked completion-side consequence

## 11. Evidence footprint / source quality note
This note is intentionally workflow-first and conservative.

It is supported by:
- existing KB protocol/firmware workflow notes on output handoff, MMIO effect proof, and ISR/deferred consequence proof
- search results and practitioner material that repeatedly expose the same operator shape around MMIO, DMA rings, and completion-driven reduction
- a modern virtio/MMIO/DMA/interrupt construction write-up that clearly illustrates the split between descriptor/state-machine preparation and later completion-driven progression
- supporting firmware fuzzing/emulation literature surfaced in this run, even though direct `web_fetch` extraction for some PDFs was degraded and therefore used conservatively

## 12. Bottom line
When a protocol / firmware case already has acceptance proof and visible output-side objects, the next useful question is often not "what does every descriptor field mean?"

It is:
- where does the descriptor or queue become **published to hardware**?
- what is the first **kick/notify/tail/owner** edge that commits that fact?
- what later **completion/ISR/deferred** reduction proves that the earlier publish really changed behavior?

That gives one compact operator chain worth preserving:
- build
- publish
- complete
- reduce

In descriptor-driven systems, that chain is often the smallest trustworthy bridge from protocol acceptance to durable hardware- and software-side consequence.
