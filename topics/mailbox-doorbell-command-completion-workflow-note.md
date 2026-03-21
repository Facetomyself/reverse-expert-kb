# Mailbox / Doorbell Command Completion Workflow Note

Topic class: concrete workflow note
Ontology layers: practical workflow, firmware/protocol continuation, mailbox/command-queue proof
Maturity: practical
Related pages:
- topics/protocol-firmware-practical-subtree-guide.md
- topics/protocol-reply-emission-and-transport-handoff-workflow-note.md
- topics/descriptor-tail-kick-and-completion-chain-workflow-note.md
- topics/peripheral-mmio-effect-proof-workflow-note.md
- topics/isr-and-deferred-worker-consequence-proof-workflow-note.md
- topics/runtime-behavior-recovery.md

## 1. When to use this note
Use this note when a protocol / firmware case already has meaningful output-side visibility, but still stalls at a mailbox-style command publish / completion seam.

Typical entry conditions:
- one accepted command, reply object, or output-side handler path is already visible
- a mailbox, command queue, submission slot, or peer-facing buffer is already plausible
- some command ID, slot index, sequence tag, or tail pointer logic is already visible
- but the analyst still has not proved:
  - the first submit / doorbell / tail / owner edge that actually publishes the command to the peer
  - the first completion / ack / callback / waiter path that proves the peer consumed it
  - the first durable software consequence that reduces that completion into policy, wakeup, state, or reuse

Use it for cases like:
- host↔firmware mailboxes where a driver clearly prepares commands, but publication still hides behind one tail/doorbell write
- command queues where completion entries or ack messages exist, but request→completion linkage is still hand-wavy
- embedded control paths where descriptor/ring ideas are partly relevant, but command IDs and mailbox slots are more practical anchors than bulk DMA taxonomy
- reverse engineering targets where logs, debugfs, or callbacks already expose mailbox activity, yet the decisive publish and completion boundaries are still unclear

Do **not** use this note when the real bottleneck is earlier, such as:
- the command family itself is still not visible from a trustworthy surface
- the parser/state path is still the real missing edge on the receive side
- local acceptance or reply-object creation is still unproved

Do **not** use this note when the real bottleneck is later, such as:
- the publish edge is already proved and the next missing proof is now one narrower MMIO effect-bearing write
- the completion boundary is already good enough and the remaining gap is now a later ISR/deferred consequence reduction

In those cases, start with:
- `topics/protocol-capture-failure-and-boundary-relocation-workflow-note.md`
- `topics/protocol-parser-to-state-edge-localization-workflow-note.md`
- `topics/protocol-replay-precondition-and-state-gate-workflow-note.md`
- `topics/protocol-reply-emission-and-transport-handoff-workflow-note.md`
- `topics/descriptor-tail-kick-and-completion-chain-workflow-note.md`
- `topics/peripheral-mmio-effect-proof-workflow-note.md`
- `topics/isr-and-deferred-worker-consequence-proof-workflow-note.md`

## 2. Core claim
A recurring firmware / protocol bottleneck is not mailbox discovery.
It is **mailbox publication-and-completion proof**.

The useful analyst target is often:
- not the first command object you can label
- not the first mailbox register block you can name
- not the first interrupt you can observe
- not the broadest queue or slot taxonomy you can recover

It is the smaller chain that actually predicts behavior:
- one staged command becomes peer-visible through one tail / doorbell / submit / owner edge
- one completion, ack, or callback can be linked back to that specific publish edge
- one later waiter, worker, or state reduction proves the completion mattered

That chain is usually more useful than broader register narration.

## 3. Target pattern
The recurring target pattern is:

```text
accepted command path visible
  -> command object or slot staged locally
  -> one publish edge commits peer-visible ownership
  -> peer consumes and records one completion / ack / status change
  -> one software-side callback / waiter / worker reduces that into durable consequence
```

The key discipline is:
- separate **local command staging** from **peer-visible publication**
- separate **raw interrupt visibility** from **request-linked completion proof**
- separate **completion visibility** from **durable software consequence**

## 4. What counts as a publish edge
Treat these as high-value targets:
- first tail pointer write that makes a queued command visible
- first doorbell or submit register write reached only on successful runs
- first owner/valid bit transition that transfers command-slot ownership to the peer
- first mailbox slot advance or queue-tail commit that predicts later completion
- first write whose absence explains “command built but never consumed”

Treat these as useful but often one layer too early:
- command struct fill alone
- buffer copy into mailbox memory alone
- naming the register block alone
- broad queue layout recovery alone

## 5. What counts as completion proof
Treat these as high-value targets:
- first completion queue entry or ack object carrying the same command ID / slot / sequence tag
- first read-to-clear or status-clear action only reachable after peer consumption
- first tx_done, rx_callback, waiter wakeup, or completion object tied to the earlier submission
- first completion-head/tail movement that distinguishes successful from stalled runs
- first reusable slot/free-path transition caused by the completion path

Treat these as useful but weaker:
- interrupt visibility with no linked completion record
- generic worker entry with no command linkage
- broad logging that “something happened” without command/slot continuity

## 6. Practical workflow

### Step 1: Freeze one disciplined compare pair
Prefer one compare pair such as:
- same command family staged in both runs, but only one run writes the tail/doorbell register
- same command publish edge in both runs, but only one run reaches a completion/ack path
- same command ID visible in staging and completion in one run, but not the other
- same local handler path reached, but only one run frees/reuses the mailbox slot later

If you do not yet have a stable pair, you are still too early for this note.

### Step 2: Mark five boundaries explicitly
Before widening queue or interrupt taxonomy, mark these five boundaries:

1. **local-command boundary**
   - where one command object, slot, or reply-bearing buffer is clearly staged
2. **publish boundary**
   - where one tail / doorbell / owner / submit edge commits peer-visible ownership
3. **peer-consume boundary**
   - where the peer’s consumption is first inferable through status, ack, or completion evidence
4. **completion boundary**
   - where one completion entry, callback, or waiter path links back to the earlier command
5. **durable-consequence boundary**
   - where software reduces that completion into wakeup, slot reuse, result handoff, policy, or state

This prevents “we saw the mailbox register” from being mistaken for “we proved command publication.”

### Step 3: Prefer command continuity over full structure recovery
When documentation is partial or the target is proprietary, prioritize:
- command ID continuity
- slot index continuity
- sequence number continuity
- successful-vs-stalled doorbell/tail differences
- completion queue movement

These are often better anchors than perfect field maps.

### Step 4: Localize the smallest publish edge that predicts completion
After local command staging, ask:
- what single write or ownership transition only occurs when the peer later consumes the command?
- where does the mailbox stop being a local buffer and become a peer-visible commitment?
- which write best distinguishes “prepared” from “actually submitted”?
- is there a tail pointer, doorbell, submit register, owner bit, or valid bit that predicts later completion?

Useful local role labels:
- `cmd-stage`
- `slot-fill`
- `publish-tail`
- `doorbell`
- `owner-transfer`
- `peer-consume`
- `ack/completion`
- `waiter-wakeup`
- `slot-reuse`
- `durable-effect`

If a region cannot be given one of these roles, it may still be churn rather than leverage.

### Step 5: Prove completion with one downstream software reduction
Do not stop at “an interrupt fired.”

Prove the completion path by tying it to one downstream effect such as:
- a waiter or completion object is signaled only after the publish edge
- a reply/result is copied out only after one matching completion entry appears
- a slot or command ID is freed only when the completion callback runs
- a later worker/state update occurs only after the ack/completion path is reached
- one compare run builds the same command but never hits the completion-linked wakeup/reuse path

### Step 6: Hand the result to one next concrete task
Once the publish→completion chain is good enough, route the result into one next task only:
- narrower descriptor publish / completion proof if the channel is really ring-heavy
- narrower MMIO effect proof if the true remaining question is now one effect-bearing register write
- ISR/deferred consequence proof if completion is visible but durable state reduction is still missing
- replay/harness refinement if the command channel can now be exercised truthfully

Do not immediately widen into full queue/register documentation unless the next experiment truly needs it.

## 7. Breakpoint / hook placement guidance
Useful anchors include:
- first command ID/slot assignment
- first slot-fill or command-copy helper
- first tail/doorbell/submit/owner write
- first completion queue append or ack parser path
- first callback, tx_done, completion waiter, or wakeup object
- first slot-free / head-advance / completion-consume path
- first later worker or policy/state effect used as proof boundary

If traces are noisy, anchor on:
- compare-run divergence around the tail/doorbell write
- command ID continuity rather than all register traffic
- completion queue movement rather than generic interrupt storms
- first waiter wakeup or slot reuse rather than every later worker

## 8. Failure patterns this note helps prevent

### 1. Mistaking command construction for submission
A filled mailbox buffer is not yet a peer-visible command.

### 2. Treating interrupt visibility as enough
An interrupt without request-linked completion is often still too weak.

### 3. Overfitting the whole register map before one chain is proved
One trustworthy publish→completion chain is usually more valuable than full mailbox taxonomy.

### 4. Losing command identity across the handoff
If you stop preserving command ID, slot, or sequence continuity, request→completion claims become soft quickly.

### 5. Staying too long in mailbox narration after the next bottleneck has shifted
Once the publish→completion chain is already good enough, move on to narrower MMIO effect, ISR/deferred consequence, or replay work.

## 9. Concrete scenario patterns

### Scenario A: Doorbell write is the real missing proof
Pattern:

```text
same command object is built in both runs
  -> only one run writes tail/doorbell
  -> only that run reaches completion/ack
```

Best move:
- anchor on the publish write, not more command-struct recovery

### Scenario B: Command ID continuity proves the chain
Pattern:

```text
local command ID assigned
  -> publish edge occurs
  -> later completion entry carries the same ID
  -> callback/wakeup frees that command slot
```

Best move:
- preserve the request→completion identity chain as the proof object

### Scenario C: Completion is visible but durable effect still hides later
Pattern:

```text
publish edge is known
  -> completion queue/ack is known
  -> durable state change still occurs only in a later worker
```

Best move:
- leave this note and continue into ISR/deferred consequence proof

## 10. Relationship to nearby pages
- `topics/protocol-reply-emission-and-transport-handoff-workflow-note.md`
  - use that when the missing proof is still where accepted local state becomes any committed outbound path at all
- `topics/descriptor-tail-kick-and-completion-chain-workflow-note.md`
  - use that when the channel is better understood as a broader descriptor/ring publish problem rather than a mailbox-style command continuation
- `topics/peripheral-mmio-effect-proof-workflow-note.md`
  - use that when the publish chain is already good enough and the remaining gap is now one narrower effect-bearing MMIO edge
- `topics/isr-and-deferred-worker-consequence-proof-workflow-note.md`
  - use that when completion visibility already exists and the missing proof is later durable consequence

## 11. Minimal operator checklist
Use this note best when you can answer these in writing:
- what is the one command family or compare pair?
- where is the local command-stage boundary?
- what is the first publish edge?
- what is the first request-linked completion or ack boundary?
- what later software consequence proves that completion mattered?
- what single next task becomes easier once this chain is known?

## 12. Source footprint / evidence quality note
This note is intentionally workflow-first.

It is grounded by:
- `sources/firmware-protocol/2026-03-22-mailbox-doorbell-command-completion-notes.md`
- `topics/protocol-reply-emission-and-transport-handoff-workflow-note.md`
- `topics/descriptor-tail-kick-and-completion-chain-workflow-note.md`
- `topics/peripheral-mmio-effect-proof-workflow-note.md`
- `topics/isr-and-deferred-worker-consequence-proof-workflow-note.md`

The evidence base here is sufficient for a practical continuation note because the point is not to claim one universal mailbox architecture.
The point is to preserve a recurring analyst move that the KB previously did not name explicitly.

## 13. Bottom line
When a firmware / protocol case already exposes local command staging and maybe even broad mailbox visibility, the next high-value move is often not more register cataloging.

It is to prove the smaller trustworthy chain between:
- command staging
- peer-visible publication
- request-linked completion/ack
- and the first durable software consequence.

That is the point where mailbox visibility becomes operational leverage.
