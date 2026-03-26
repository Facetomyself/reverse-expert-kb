# ISR / deferred worker first-consumer notes — 2026-03-26

Topic focus:
- Linux/firmware-flavored interrupt and deferred-work material used to sharpen the reverse-KB operator rule for ISR/deferred consequence proof

Purpose of this note:
- preserve the source-backed practical refinement that **interrupt visibility is not yet consequence ownership**
- strengthen the existing firmware/protocol branch around the smaller operator stop rule:
  - `armed != observed_irq != scheduled_deferred != consumed`

## Sources retained
- Linux kernel docs — generic IRQ
  - <https://www.kernel.org/doc/html/latest/core-api/genericirq.html>
- Linux kernel docs — workqueue
  - <https://docs.kernel.org/core-api/workqueue.html>
- Linux kernel docs — NAPI
  - <https://docs.kernel.org/networking/napi.html>
- Linux Kernel Labs — deferred work
  - <https://linux-kernel-labs.github.io/refs/heads/master/labs/deferred_work.html>
- linux-insides — softirq, tasklets, workqueues
  - <https://0xax.gitbook.io/linux-insides/summary/interrupts/linux-interrupts-9>
- search artifact:
  - `sources/firmware-protocol/2026-03-26-1516-isr-deferred-worker-search-layer.txt`

## Practical takeaways preserved

### 1. IRQ/top-half visibility is not the same thing as the first truthful consumer
The retained sources reinforce a recurring split:
- IRQ arrival / top-half acknowledgement may only establish that a condition became visible
- softirq/tasklet/NAPI/workqueue/threaded handler may own the first durable processing step
- the actual reverse-engineering target is the first downstream object or reduction that predicts later state, reply, wakeup, or retry behavior

So the branch should preserve:
- `armed != observed_irq != scheduled_deferred != consumed`

### 2. The first useful proof object is often a reduction, not the callback family name
The useful operator target is commonly one of:
- first completion/status bucket reduction
- first poll budget / completion accounting edge that changes ownership
- first deferred worker state write
- first reply/error selector
- first wakeup/queue insertion that predicts later visible behavior

This is stronger than:
- naming the ISR
- listing tasklets/workqueues
- proving that NAPI or a worker was scheduled at all

### 3. NAPI-like and workqueue-like cases need a smaller stop rule
The NAPI material is especially useful because it makes the handoff explicit:
- IRQ-side scheduling can happen in interrupt context
- later poll ownership and completion release happen elsewhere
- the real consequence may live in poll processing and completion accounting rather than in the top-half

That maps well onto firmware/embedded cases where:
- one interrupt line is easy to see
- the durable behavior only appears when a later consumer drains a ring, status word, or completion bucket

### 4. Workqueue/process-context execution changes what counts as evidence
The workqueue/deferred-work material reinforces that some deferred handlers run in process context and can sleep/block/use richer locking and I/O patterns.

Practical RE implication:
- if the interesting behavior requires allocations, waits, richer locking, or outbound reply assembly, the real first consumer may be later in a worker rather than in the atomic interrupt-side code
- this should bias hook placement toward the first durable queue node, worker argument package, or state/reply reduction rather than broader IRQ-family cataloging

## KB-facing synthesis
The firmware/protocol branch should keep these proof layers separate:
1. peripheral/descriptor/arm truth
2. interrupt arrival truth
3. deferred scheduling truth
4. first consumer/reduction truth
5. later externally visible effect truth

The practical rule added by this run is:
- stop broad ISR/deferred narration once one **first consumer** object is already good enough to predict later behavior
- do not keep widening callback/worker taxonomy after that point unless model realism specifically needs it

## Suggested wording to preserve canonically
- `armed != observed_irq != scheduled_deferred != consumed`
- top-half visibility is often only arrival truth, not behavior ownership
- the analyst should freeze the first completion/status reduction, reply/error selector, wakeup, or durable state write that survives callback scope and predicts later behavior better than the interrupt label itself
