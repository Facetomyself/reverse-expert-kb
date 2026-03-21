# Source Notes — Mailbox / doorbell command publish and completion workflow

Date: 2026-03-22
Purpose: support a practical protocol / firmware continuation note for the recurring case where an accepted command path is already visible, maybe even a reply object or command buffer is partly understood, but the analyst still has not proved the smaller mailbox-style chain that actually matters:

- command object is staged locally
- one mailbox tail / doorbell / submit write publishes it to the peer
- one interrupt, completion queue update, ack packet, or callback proves the peer consumed it
- one later software-side reduction turns that fact into durable consequence

## Scope
This note is intentionally narrower than generic DMA/ring/MMIO taxonomy.
It preserves the operator pattern that keeps recurring in firmware/driver work where the control path is command-oriented rather than bulk-data-oriented:

- a mailbox, command queue, or host↔firmware channel exists
- command IDs or slots are reused across request/completion pairs
- one tail/doorbell/interrupt boundary matters more than perfect structure recovery
- a later completion/ack path matters more than broad interrupt labeling

## External research performed
Explicit multi-source search was attempted through `search-layer` with:
- `--source exa,tavily,grok`

Queries used:
1. `firmware mailbox command completion acknowledgment workflow reverse engineering`
2. `embedded mailbox doorbell interrupt completion ring buffer workflow`
3. `command queue mailbox reply interrupt firmware driver completion workflow`

## Search audit
Search sources requested:
- exa
- tavily
- grok

Search sources succeeded:
- exa
- tavily
- grok

Search sources failed:
- none

Exa endpoint:
- `http://158.178.236.241:7860`

Tavily endpoint:
- `http://proxy.zhangxuemin.work:9874/api`

Grok endpoint:
- `http://proxy.zhangxuemin.work:8000/v1`

Degraded-mode note:
- not degraded for search execution
- some fetched pages remained truncated because of extractor limits, so claims below are intentionally conservative and only preserve the workflow-level shape that was directly visible

Audit artifact:
- `/tmp/reverse-kb-search-20260322-0016.txt` (ephemeral local capture)

## Supporting source signals

### 1. Linux mailbox framework cleanly separates send, ack, receive, and protocol ownership
Source:
- `https://docs.kernel.org/driver-api/mailbox.html`

High-signal findings:
- mailbox controller may know transmission completion through IRQ, polling, or not at all
- client drivers may operate in blocking or async mode
- mailbox usage naturally separates:
  - send request submission
  - tx-done / completion knowledge
  - rx callback handling of incoming/ack messages
- the protocol still lives above the common mailbox mechanism

Why it matters:
- this is a clean operator reminder that mailbox visibility is not one thing
- the useful proof points are often distinct:
  - publish/send edge
  - completion/ack knowledge
  - actual protocol-level callback consequence

### 2. AMD/Xilinx Generic Command Queue product guide gives an explicit doorbell + completion shape
Source:
- `https://xilinx.github.io/AVED/amd_v80_gen5x8_exdes_1_20231204/Generic+Command+Queue+IP+v2.0+-+Product+Guide.html`

High-signal findings:
- producer writes commands into submission queue entries
- producer writes the submission queue tail pointer to a doorbell register, which can trigger `irq_sq`
- consumer reads and processes submission entries
- consumer writes completion entries and then writes the completion queue tail pointer, which can trigger `irq_cq`
- reading specific tail/status registers clears the corresponding interrupt

Why it matters:
- this is almost a textbook practical chain for the analyst target:
  - staged command
  - doorbell publish
  - peer consumption
  - completion queue update
  - interrupt/clear behavior
- it also reinforces that interrupt clear/read behavior can be part of the proof chain, not just noise

### 3. NVMe documentation provides a portable analogy for command ID, submission tail, and completion head discipline
Source:
- `https://wiki.osdev.org/NVMe`

High-signal findings:
- driver prepares commands in submission queue memory and updates the tail doorbell register
- controller appends completion entries and signals completion queue availability via interrupt
- host processes completion entries and updates the completion head doorbell/register
- completion entries carry command identifier and queue/head context

Why it matters:
- even though NVMe is not a generic firmware mailbox, it reinforces a recurring operator truth:
  - local command fill is not yet publish
  - command ID continuity is often the easiest way to prove request→completion linkage
  - completion queue handling often proves more than raw interrupt visibility

### 4. Samsung NPU reversing material shows mailbox controls in a real firmware/driver case
Source:
- `https://blog.impalabs.com/2103_reversing-samsung-npu.html`

High-signal findings:
- the driver explicitly initializes interface/mailbox structures during device bring-up
- logs/debug surfaces help reveal firmware/driver interaction boundaries
- the NPU environment combines firmware loading, interface opening, and mailbox-mediated communication

Why it matters:
- this grounds the workflow in a realistic RE setting rather than only abstract controller docs
- mailbox control surfaces often become visible in logs/debugfs/driver init long before the full command protocol is understood

### 5. Existing KB notes already covered nearby seams but not this narrower continuation
From existing KB pages:
- `topics/protocol-reply-emission-and-transport-handoff-workflow-note.md`
- `topics/descriptor-tail-kick-and-completion-chain-workflow-note.md`
- `topics/peripheral-mmio-effect-proof-workflow-note.md`
- `topics/isr-and-deferred-worker-consequence-proof-workflow-note.md`

Why it matters:
- the KB already knew how to talk about:
  - accepted local output becoming one outbound handoff
  - generic descriptor publish / completion chains
  - narrower MMIO effect proof
  - later ISR/deferred consequence proof
- what was still missing was the mailbox/doorbell-specific continuation where command publish and ack/completion linkage are the real practical bottleneck

## Distilled practical pattern
A useful chain to preserve is:

```text
accepted command path or reply object visible
  -> one command slot / mailbox buffer / queue entry is staged
  -> one tail / doorbell / submit / kick edge publishes it to peer-visible ownership
  -> peer writes one completion / ack / status / callback trigger
  -> one software-side callback, waiter, or worker reduces that fact into durable consequence
```

## Operator heuristics to preserve
- Do not confuse command-buffer fill with command publication.
- Tail/doorbell/submit/owner writes are often more useful than perfect field recovery.
- Command IDs, slot numbers, and sequence tags are often the cheapest trustworthy request→completion linkage.
- An interrupt alone is weaker proof than a completion entry or ack object tied back to one earlier publish edge.
- Read-to-clear or status-clear behavior can be part of the proof chain, not just cleanup noise.
- Mailbox cases often sit between broad reply-emission work and broader descriptor/MMIO taxonomy; do not widen too early.
- If the command appears accepted locally but no durable effect follows, suspect:
  - unpublished tail/doorbell state
  - pending-slot ownership
  - completion queue not drained
  - ack callback path not reached
  - interrupt/status clear semantics hiding the real completion boundary

## Candidate canonical KB mapping
Most directly supports:
- `topics/mailbox-doorbell-command-completion-workflow-note.md`

Also strengthens:
- `topics/protocol-firmware-practical-subtree-guide.md`
- `topics/protocol-reply-emission-and-transport-handoff-workflow-note.md`
- `topics/descriptor-tail-kick-and-completion-chain-workflow-note.md`
- `topics/peripheral-mmio-effect-proof-workflow-note.md`
- `topics/isr-and-deferred-worker-consequence-proof-workflow-note.md`

## Limits / conservative claims
This run does **not** claim:
- one universal mailbox register map
- that all command queues are literally DMA rings
- that every completion is interrupt-driven
- that Linux mailbox API structure directly matches every proprietary firmware implementation

This run **does** claim conservatively:
- mailbox/doorbell command channels repeatedly expose a practical seam between local command staging and peer-visible publication
- command ID / slot continuity is often a strong RE anchor for request→completion linkage
- a dedicated workflow note is justified because this seam is narrower and more operator-useful than burying it inside generic output-handoff or generic MMIO notes

## Bottom line
The recurring analyst miss is not failure to find the mailbox.
It is failure to preserve the smaller trustworthy chain inside it:

- where the command becomes published
- how the peer’s completion or ack is linked back to that publication
- and where software finally reduces that completion into durable consequence

That is the operator pattern this source note exists to preserve.
