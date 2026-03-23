# 2026-03-23 kernel callback local-vs-handoff consumer notes

## Scope
Source-backed continuation for the protected-runtime workflow note:
- narrow the operator question after callback registration is already known
- distinguish two practical callback-to-consumer shapes
  - local rights-bearing consumer inside callback context
  - emitted-record / queue / IOCTL / service handoff consumer outside callback context
- keep the result useful for reverse-engineering workflow selection, not bypass instruction writing

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

Search trace:
- `/tmp/reverse-kb-2026-03-23-1616-search.txt`

## Search queries used
1. `Windows kernel callback object callbacks telemetry enforcement consumer anti-cheat rights filter queue handoff`
2. `ObRegisterCallbacks access mask downgrade telemetry queue service handoff reverse engineering`
3. `process image thread notify callbacks anti-cheat telemetry reducer enforcement consumer reverse engineering`

## Sources actually used
### 1. Microsoft Learn — ObRegisterCallbacks
URL:
- <https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/wdm/nf-wdm-obregistercallbacks>

Useful points:
- official boundary for process/thread/desktop handle-operation callbacks
- confirms the registration object and the supported callback family without overclaiming undocumented internals
- useful as the clean anchor for cases where analysts already know they are on the `ObRegisterCallbacks` path

Why it mattered here:
- supports naming a specific local-rights-filter subcase without pretending every callback family behaves the same way
- keeps the workflow note grounded when talking about handle create/duplicate paths and pre/post-operation callback structure

### 2. XPN — Windows Anti-Debug Techniques: OpenProcess Filtering
URL:
- <https://blog.xpnsec.com/anti-debug-openprocess/>

Useful points:
- shows the practical operator shape where a pre-operation callback on the process handle path rewrites or filters requested access
- makes the key workflow distinction that the consequence-bearing object can already be the downgraded rights result itself, not necessarily a later service or queue object
- useful for treating `requested access -> filtered/granted access` as a minimal proof object

Why it mattered here:
- directly supports adding a named "local rights-bearing consumer" subcase to the workflow page
- improves the page’s stop rule: if the reduced rights object already explains attach/open failure, do not keep hunting for a larger downstream narrative without evidence

### 3. Fast and Furious: Outrunning Windows Kernel Notification Routines from User-Mode
URL:
- <https://pmc.ncbi.nlm.nih.gov/articles/PMC7338165/>

Useful points:
- explains the standard sequence where a driver first learns about a process and then relies on callback-based handle filtering for later access control
- shows that protection setup timing and effect timing are not identical
- gives strong support for early-window vs settled-state compare logic in callback-heavy protected-process cases

Why it mattered here:
- strengthens the proof advice for timing-sensitive callback cases
- supports the practical compare pair `early-window handle acquisition vs settled-state handle acquisition`

### 4. s4dbrd — How Kernel Anti-Cheats Work: A Deep Dive into Modern Game Protection
URL:
- <https://s4dbrd.github.io/posts/how-kernel-anti-cheats-work/>

Useful points:
- describes the recurring three-component architecture: kernel driver, usermode service, and game-side/injected component
- explicitly places IOCTLs, named pipes, and shared-memory sections after kernel-side event collection in the broader protection stack
- useful not as a vendor-specific fact source, but as a practical architectural reminder that callback telemetry often becomes meaningful only after a later handoff or policy consumer

Why it mattered here:
- supports adding a named "callback produces one emitted record, real consumer lives outside callback context" subcase
- helps route analysts toward queue/shared-buffer/IOCTL/service consumers when callback bodies stay short and telemetry-heavy

## Synthesis
This pass tightened one practical ambiguity in the protected-runtime callback page.

The previous page already said:
- do not stop at registration metadata
- find the first carrier or consumer that survives callback scope

What it did not say sharply enough was that two different operator shapes recur:

### Shape A — local rights-bearing consumer
Typical path:
- handle create / duplicate request
- pre-operation callback executes
- desired or granted access is rewritten
- the resulting downgraded rights object already explains the symptom

Why this matters:
- analysts can waste time looking for a larger queue/service story when the first meaningful consumer is already the rewritten access mask or granted-rights result
- the smallest useful proof becomes `requested access vs resulting granted access`, not a whole architecture map

### Shape B — emitted-record / handoff consumer
Typical path:
- process/thread/image/object callback fires
- callback or reducer produces a compact record, flag, or bucket
- queue/shared-memory/IOCTL/service handoff occurs
- later component owns score/deny/degrade/kick behavior

Why this matters:
- analysts can overread callback-local helpers when the callback is only the producer
- once one emitted record or reducer write is isolated, the right next question is who first consumes that object downstream

## KB action taken
Extended:
- `topics/kernel-callback-telemetry-to-enforcement-consumer-workflow-note.md`

Nature of extension:
- added named Subcase A / Subcase B treatment under first telemetry carrier identification
- added narrower proof advice for rights-filter cases vs handoff cases
- updated source-footprint section to reflect this continuation pass

## Conservative limits
- did not claim a specific anti-cheat vendor queue or IOCTL format without direct stronger evidence
- did not treat XPN’s OpenProcess filtering write-up as representative of every callback-heavy protected-runtime target
- used the architecture article only for broad stack shape, not for undocumented internals of a particular vendor
- kept the result workflow-centered and case-selection-centered rather than exploit-centered
