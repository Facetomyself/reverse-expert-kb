# ISR / deferred-worker consequence notes

Date: 2026-04-08
Branch target: firmware/protocol practical workflows / MMIO-to-consequence continuation
Purpose: preserve a source-backed operator refinement for cases where hardware-visible completion or interrupt activity is visible, but the first durable consumer still sits later in ISR/DPC/bottom-half/deferred-worker handling.

## Research intent
Strengthen the existing ISR / deferred-worker consequence workflow note with a sharper separation between:
- armed / write-side truth
- IRQ arrival / top-half truth
- deferred scheduling/execution truth
- first consumer/reduction truth

## Search artifact
Raw multi-source search artifact:
- `sources/protocol/2026-04-08-0952-irq-search-layer.txt`

Requested source set:
- `exa,tavily,grok`

Observed search-source reality for this run:
- Exa returned usable Linux/Windows interrupt-handling surfaces
- Tavily returned usable Linux/Windows interrupt-handling surfaces
- Grok was explicitly invoked and failed with repeated `502 Bad Gateway` through the configured proxy path

## Retained sources
1. Linux kernel documentation surfaces
   - hard IRQ / softirq / tasklet / workqueue / threaded IRQ concepts
2. Microsoft documentation surfaces
   - ISR / DPC separation and deferred procedure call handling
3. Conservative embedded/DMA completion discussion surfaces
   - retained only as support for practical handoff shape, not as sole truth

## High-signal retained findings

### 1. Linux already separates hard IRQ handling from later deferred work
Linux interrupt-handling materials preserve distinct layers such as:
- hard IRQ / top half
- softirq/tasklet/workqueue/threaded handling
- later worker-side consequence

Practical consequence:
- seeing IRQ arrival or a bottom-half callback is not automatically the same thing as proving the first behavior-changing consumer
- keep interrupt-plumbing truth separate from later reduction truth

### 2. Windows already separates ISR and DPC truth
Windows documentation preserves a clear distinction between:
- ISR entry/ack/service
- deferred procedure call scheduling/execution
- later driver or subsystem consequence

Practical consequence:
- ISR visibility is weaker than DPC truth
- DPC truth is still weaker than the first state/reply/scheduler consumer that actually predicts later behavior

### 3. Hardware-visible completion is often still only setup for a later local reduction
Across MMIO/interrupt/deferred-worker cases, the recurring practical pattern is:
- condition became possible
- interrupt path fired
- some deferred work became runnable
- only later did one status reduction / state write / reply-family choice / wakeup edge actually matter

Practical consequence:
- do not stop at hardware-visible arrival alone
- stop at the first local reduction that predicts the next durable effect

## Practical synthesis worth preserving canonically
A compact stop-rule ladder for this seam is:

```text
armed
  != IRQ arrival / top-half truth
  != deferred scheduling/execution truth
  != first consumer/reduction truth
```

This keeps four different successes separate:
1. **armed**
   - write-side or condition-side setup is now present
2. **IRQ arrival / top-half truth**
   - interrupt entry/ack/arrival is visible
3. **deferred scheduling/execution truth**
   - DPC / softirq / tasklet / workqueue / threaded follow-on work is visible
4. **first consumer/reduction truth**
   - one completion/status reduction, reply-family choice, state write, or wakeup edge predicts later behavior

## Best KB use of this material
This material is best used to sharpen the existing ISR / deferred-worker consequence workflow note.
It should not become a broad interrupt-taxonomy page.

The operator-facing value is:
- do not overclaim from MMIO write / hardware-visible completion alone
- do not overclaim from ISR/top-half visibility alone
- do not overclaim from DPC/tasklet/workqueue visibility alone
- stop only when one later consumer/reduction predicts the effect you actually care about

## Search reliability note
This was a degraded-source external pass, not a fully healthy tri-source result set.
It still counts as a real external-research attempt because `exa,tavily,grok` were explicitly requested and Grok was actually invoked; its failure is recorded clearly.
