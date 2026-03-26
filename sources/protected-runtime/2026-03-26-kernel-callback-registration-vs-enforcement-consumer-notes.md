# Kernel callback registration vs enforcement-consumer notes

Date: 2026-03-26
Branch: protected-runtime practical subtree
Focus: kernel callback telemetry -> enforcement-consumer reduction

## Why this note exists
This note preserves a narrower protected-runtime stop rule for callback-heavy kernel telemetry cases:
- visible callback registration is often earlier than behavioral ownership
- the first practical consumer may instead be a rights-bearing object, reducer bucket, queue node, shared record, IOCTL payload, or later service/game policy worker
- registration, callback firing, emitted telemetry carrier, and enforcement-relevant consumer should not collapse into one vague "callback did it" story

## Search context
Explicit external search attempted through `search-layer --source exa,tavily,grok`.

Queries:
1. `ObRegisterCallbacks handle access mask downgrade first consumer anti cheat reverse engineering`
2. `PsSetCreateProcessNotifyRoutine later service consumer telemetry anti cheat driver reverse engineering`
3. `kernel callback telemetry queue IOCTL policy consumer anti cheat protected runtime`

Search artifact:
- `sources/protected-runtime/2026-03-26-1416-kernel-callback-telemetry-search-layer.txt`

Observed source-set reality for this run:
- Tavily returned usable results
- Exa proxy returned `402 Payment Required` but search-layer output still retained Exa-labelled result rows
- Grok was invoked and failed with repeated `502 Bad Gateway`

## Conservative retained sources
- Microsoft Learn — `ObRegisterCallbacks`
  - registration semantics for process/thread/desktop handle operations
  - useful mainly to freeze that registration itself is a setup surface, not automatic proof of later behavioral ownership
- Microsoft Learn — `PsSetCreateProcessNotifyRoutineEx`
  - process-create callback executes at process creation/deletion time and is called in a specific context
  - useful for separating registration / callback execution timing from later persistent telemetry carriers or policy consumers
- Adrian / s4dbrd — `How Kernel Anti-Cheats Work`
  - practical architectural reminder that kernel driver, usermode service, and game-injected/usermode components often split collection from later policy/reporting
  - IOCTLs, shared memory, and service-owned logic are recurring downstream carriers/consumers rather than callback registration being the whole story
- Adrian / s4dbrd — `Reversing BEDaisy.sys`
  - concrete case framing that real anti-cheat drivers register kernel-facing surfaces yet remain operationally meaningful through larger minifilter / service / protected-runtime architecture rather than one callback label alone

## Retained findings
### 1. Registration is a setup fact, not automatically the first enforcement fact
The docs are strongest for preserving a basic but important rule:
- `ObRegisterCallbacks` proves that a driver registered callback routines for certain object operations
- `PsSetCreateProcessNotifyRoutineEx` proves the driver asked to be called on process-create/delete transitions

But those APIs mainly freeze:
- callback family
- registration existence
- some execution-time constraints

They do **not** by themselves freeze:
- the first rights-bearing consequence object
- the first telemetry record that survives callback scope
- the first usermode/service/game consumer that makes the telemetry matter

### 2. In handle-rights cases, the rewritten rights-bearing object may itself be the first consumer
A practical subcase is worth preserving sharply:
- if an `ObRegisterCallbacks` pre-operation path directly rewrites desired/granted access masks
- and the analyst’s visible symptom is already explained by the downgraded handle rights
- then the rights-bearing object is often the first enforcement-relevant consumer

That is a narrower and more practical stop rule than staying at callback-registration naming.

Useful split:
- registration surface
- callback firing surface
- rights rewrite object
- later symptom (`OpenProcess`, `ReadProcessMemory`, handle duplication, etc. denied or degraded)

### 3. In anti-cheat architectures, telemetry often becomes meaningful only after queue / IOCTL / service handoff
The architectural writeup is useful not as authoritative vendor truth, but as a cross-check that modern kernel anti-cheat systems commonly split:
- kernel collection / interception
- usermode service communication
- later policy or reporting logic

For KB purposes, the recurring practical consequence is:
- callback execution may still be only the producer
- the first behaviorally important consumer may be one emitted IOCTL/shared-memory record, one reducer bucket, or one service/game worker that decides deny/degrade/report behavior

### 4. Process-create callbacks should not be overread as full policy ownership
`PsSetCreateProcessNotifyRoutineEx` is useful because it preserves timing/context reality:
- process-create callbacks run at creation/deletion transitions
- they may establish state, telemetry, or setup obligations
- but later policy ownership may still live in another callback family, another reducer, or a later driver/usermode consumer

This matters in startup-window cases where the analyst can see callback setup clearly but the protected behavior only becomes predictable after a later object-callback, IOCTL, or service-owned policy transition.

## Practical stop rule preserved
Prefer the smaller ladder:

```text
callback family visible
  -> separate registration from actual callback firing
  -> ask what first object survives callback scope
  -> if rights are already rewritten locally, stop at that rights-bearing object
  -> otherwise follow the first queue / record / IOCTL / shared-state carrier
  -> freeze one later enforcement-relevant consumer only after that carrier becomes behaviorally predictive
```

Equivalent short form:

```text
registered != fired != emitted != enforced
```

And in many handle-filter cases:

```text
registration != rights consequence
```

## Concrete operator questions to retain
1. Is this callback family only registered, or do I also have evidence of a real trigger path?
2. Does the callback itself already rewrite the consequence-bearing object (for example granted access rights)?
3. What first object survives beyond callback scope: flag, score, queue node, ring entry, IOCTL payload, shared record, service message?
4. Does later deny/degrade behavior correlate better with callback firing, with emitted telemetry, or with one downstream consumer?
5. Is the current case really immediate local rights filtering, or is it producer -> handoff -> later policy?

## Why this matters for the KB
Without this note, callback-heavy protected-runtime cases drift into two bad operator habits:
- stopping at callback registration labels as if that already explains protected behavior
- overexpanding into callback inventory instead of freezing one rights object or one first downstream consumer

This note keeps the branch practical by preserving a case-driven distinction between:
- registration facts
- callback execution facts
- rights/telemetry carriers
- enforcement consumers
