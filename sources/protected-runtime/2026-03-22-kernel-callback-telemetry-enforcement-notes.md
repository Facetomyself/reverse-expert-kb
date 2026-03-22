# 2026-03-22 kernel-callback telemetry -> enforcement consumer notes

## Scope
External-research-driven note collection for a thinner protected-runtime / anti-cheat-adjacent practical seam:
- kernel callback telemetry surfaces used by anti-cheat or security-sensitive drivers
- the analyst task of moving from callback registration to the first enforcement-relevant reducer or consumer
- emphasis on practical workflow structure, not broad anti-cheat taxonomy

## Search intent
Target gap:
- the KB already treated anti-cheat as a useful protected-runtime subdomain
- it still lacked one concrete operator page for callback-heavy kernel monitoring cases where registrations are visible but the first behavior-changing consumer is still unclear

Desired outcome:
- a practical workflow note focused on
  - callback family selection
  - telemetry-to-reducer mapping
  - first enforcement-relevant consumer
  - compare-run or downstream-effect proof

## Search audit
Mode: explicit multi-source via `search-layer`
Requested sources:
- exa
- tavily
- grok

Succeeded sources:
- exa
- tavily
- grok

Failed sources:
- none during the search-layer pass itself

Configured endpoints observed on this host:
- Exa: `http://158.178.236.241:7860`
- Tavily: `http://proxy.zhangxuemin.work:9874/api`
- Grok: `http://proxy.zhangxuemin.work:8000/v1`

## Search queries used
1. `kernel anti cheat callback telemetry enforcement consumer reverse engineering workflow`
2. `ObRegisterCallbacks PsSetCreateThreadNotifyRoutine anti cheat enforcement analysis`
3. `minifilter ETW anti cheat driver event pipeline enforcement reverse engineering`

## Sources actually used
### 1. Microsoft Learn — PsSetCreateThreadNotifyRoutine
URL:
- <https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/ntddk/nf-ntddk-pssetcreatethreadnotifyroutine>

Useful points:
- thread creation/deletion notification is an official kernel callback surface for highest-level/system-profiling style drivers
- the callback signature is small and event-oriented, which makes it a producer boundary rather than an explanation of later policy by itself
- the registration API documentation is strong grounding for distinguishing callback registration from later telemetry consumption

Why it mattered here:
- supports the workflow rule that registration alone is not yet enforcement understanding
- useful as a conservative official anchor for producer-side callback boundaries

### 2. SpecterOps — Understanding Telemetry: Kernel Callbacks
URL:
- <https://specterops.io/blog/2023/06/12/understanding-telemetry-kernel-callbacks/>

Useful points:
- surveys common Windows kernel callback surfaces including process/thread/image notifications and `ObRegisterCallbacks`
- explains the practical distinction between registration metadata, object types, operation types, and pre/post-operation callback paths
- makes clear that handle-oriented callbacks often modify or observe access rights rather than serving as a full standalone story about later enforcement
- gives a useful structural view of `CallbackList` / altitude / object-type insertion and of the `OpenProcess -> NtOpenProcess -> Obp*` callback path for handle creation

Why it mattered here:
- strongly supports a workflow that moves from callback registration and trigger site toward the first reducer or consumer that actually predicts later behavior
- helpful for distinguishing kernel telemetry production from the later policy state that matters to an analyst

### 3. s4dbrd — How Kernel Anti-Cheats Work
URL:
- <https://s4dbrd.github.io/posts/how-kernel-anti-cheats-work/>

Useful points:
- describes anti-cheat systems as three-component architectures: kernel driver, service, and game-side component
- explicitly highlights callback families such as process/thread/image notifications and object-handle callbacks as raw monitoring surfaces
- emphasizes that the meaningful operational story often continues through IOCTLs, service-owned logic, shared buffers, or later allow/deny policy paths rather than ending at callback registration
- keeps anti-cheat useful here as a protected-runtime case where privilege and observation topology matter as much as semantics

Why it mattered here:
- supports framing anti-cheat as a practical continuation of protected-runtime analysis rather than as a separate taxonomy island
- especially useful for the analyst move from raw callback telemetry to the first service-, policy-, or protection-relevant consumer

### 4. Fast and Furious: Outrunning Windows Kernel Notification Routines from User-Mode
URL:
- <https://pmc.ncbi.nlm.nih.gov/articles/PMC7338165/>

Useful points:
- explains the standard protected-process pattern of combining process-create notification with object callbacks that later filter handle rights
- shows that process visibility and callback establishment timing are distinct, and that races or setup windows can matter materially
- provides concrete BattlEye / EasyAntiCheat case references in the context of process-handle protection timing

Why it mattered here:
- reinforces the need to reason about callback setup, lifecycle timing, and later protection consumers rather than assuming registration means immediate complete protection
- useful for compare-run ideas involving early window, registration timing, and first stable downstream divergence

## Sources seen but used conservatively
- community and forum discussions surfaced during search-layer execution
  - directionally useful for confirming that analysts repeatedly stall on registration-heavy kernel monitoring surfaces
  - too uneven to use as primary structural support for the page

## Synthesis
A reusable operator gap emerged inside the protected-runtime branch:
- the KB already had watchdog/heartbeat reduction for repeated monitor loops
- it already had native callback-registration guidance for ordinary async/event-loop ownership
- but it did not yet have a protected-runtime-specific note for callback-heavy kernel telemetry where the hard part is not finding `PsSet*` / `ObRegisterCallbacks`, but proving which reducer, queue, service handoff, policy bucket, or handle-rights consumer actually matters first

The most reusable structure from the sources is:
1. choose one callback family
2. distinguish registration from actual trigger path
3. isolate the first telemetry reducer or policy carrier
4. prove one enforcement-relevant consumer and one later effect

That yields a practical continuation page rather than another broad anti-cheat summary.

## KB action taken
Created:
- `topics/kernel-callback-telemetry-to-enforcement-consumer-workflow-note.md`

Canonical sync needed after creation:
- `topics/protected-runtime-practical-subtree-guide.md`
- `topics/anti-tamper-and-protected-runtime-analysis.md`
- `index.md`
- run report

## Conservative limits
- did not treat anti-cheat architectures as interchangeable
- did not claim every callback leads directly to local deny/kill behavior
- did not overclaim undocumented internal anti-cheat implementation details from weak secondary sources
- treated official docs plus vendor/industry analysis plus an academic timing paper as enough grounding for a workflow note, not a full new branch split
