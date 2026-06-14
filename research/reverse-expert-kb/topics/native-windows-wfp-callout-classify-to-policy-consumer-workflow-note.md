# Native Windows WFP Callout Classify to Policy Consumer Workflow Note

Topic class: workflow note
Ontology layers: native practical workflow, Windows network-filter driver evidence, kernel/user-mode policy handoff
Maturity: draft-practical
Related pages:
- topics/native-practical-subtree-guide.md
- topics/native-binary-reversing-baseline.md
- topics/native-etw-provider-session-consumer-workflow-note.md
- topics/native-windows-minifilter-callback-to-policy-consumer-workflow-note.md
- topics/malware-request-builder-to-send-boundary-workflow-note.md
- topics/malware-analysis-overlaps-and-analyst-goals.md
- sources/native/2026-06-15-windows-wfp-callout-policy-consumer-notes.md

## 1. When to use this note

Use this note when a Windows native target exposes Windows Filtering Platform (WFP) callout-driver surfaces and the current risk is overreading network-filter evidence.

Common entry signals:
- `FwpsCalloutRegister*`, `FwpsCalloutUnregister*`, `FWPS_CALLOUT*`, `classifyFn`, `notifyFn`, or `flowDeleteFn`
- `FwpmCalloutAdd*`, `FwpmFilterAdd*`, sublayer / provider / filter weight setup, or user-mode BFE management code
- `FWPS_CALLOUT_CLASSIFY_FN*`, `FWPS_INCOMING_VALUES*`, `FWPS_INCOMING_METADATA_VALUES*`, `FWPS_CLASSIFY_OUT*`, `FWP_ACTION_BLOCK`, `FWP_ACTION_PERMIT`, or `FWP_ACTION_CONTINUE`
- ALE layers such as `ALE_AUTH_CONNECT`, `ALE_AUTH_RECV_ACCEPT`, `ALE_FLOW_ESTABLISHED`, `ALE_CONNECT_REDIRECT`, or matching discard layers
- async classify functions such as `FwpsPendOperation*`, `FwpsCompleteOperation*`, packet/stream clone helpers, injection helpers, absorb flags, worker queues, or user-mode verdict services
- firewall, VPN, EDR, AV, DLP, parental-control, transparent proxy, redirection, or network-inspection components where it is unclear whether a callback only observed, pended, redirected, blocked, permitted, reinjected, logged, or handed off a decision

Do **not** use this note as a WFP programming tutorial. The reverse-engineering question is narrower:

> Which boundary is the first truthful proof object: callout registration, management-filter installation, filter/layer match, classify callback entry, decision write, async handoff, completion/reinjection/discard, or final network/policy effect?

## 2. Core split

Keep this ladder visible:

```text
callout registered in kernel
  != user-mode or kernel management object installed for the relevant layer/sublayer/filter
  != filter conditions matched this traffic and delivered classifyFn
  != layer/metadata/flow context selected the policy inputs actually used
  != classifyOut action/rights/flags were written as a decision
  != async pend/clone/absorb/user-mode handoff retained ownership correctly
  != completion, reauthorization, reinjection, or discard applied that decision
  != socket-visible / packet-visible / policy-owned effect proved
```

Compact stop rule:

```text
registered != filter-matched != classify-entered != decision-written != async-owned != completed/reinjected/discarded != effect-owned
```

The usual mistake is to collapse all of this into one sentence like "the WFP driver blocked the connection" or "the EDR saw the packet." A driver can register a callout that no relevant filter ever references, a filter can match a layer that is only flow tracking, `classifyFn` can return `CONTINUE`, a higher-weight filter or action-right state can constrain the decision, an absorbed packet can be reinjected later, and an ALE pended operation may not be decided until completion and reauthorization.

## 3. Proof objects

### 3.1 Callout-registration truth

What it proves:
- the kernel driver registered one or more callout structures with the filter engine
- `classifyFn`, `notifyFn`, and `flowDeleteFn` entry points and a runtime callout id may exist
- the driver has a possible callback surface for WFP indications

Useful evidence:
- `FwpsCalloutRegister0/1/2(...)` arguments, callout key, returned runtime id, and device object
- `FWPS_CALLOUT*` structure fields and per-callout GUIDs
- `notifyFn` add/delete events and `flowDeleteFn` cleanup ownership where relevant
- driver unload / unregister paths

What it does **not** prove:
- that `FwpmCalloutAdd*` / `FwpmFilterAdd*` installed a management object referencing the callout
- that the filter engine matched the target traffic
- that the callout was allowed to write a block/permit action

Stop when:
- you can name the callout key/runtime id and callbacks well enough that the next uncertainty is filter/layer attachment rather than generic driver presence.

### 3.2 Filter/layer/sublayer match truth

What it proves:
- a WFP management object and filter path may reference the callout at a concrete layer and sublayer
- filter conditions, weights, provider context, and layer semantics define when the callout can fire

Useful evidence:
- `FwpmCalloutAdd*`, `FwpmSubLayerAdd*`, `FwpmFilterAdd*`, provider/context ids, filter ids, weights, and conditions
- layer id: ALE connect, receive/accept, flow-established, stream, transport, packet, redirect, or discard
- process/app-id, address/port, protocol, interface, compartment, direction, and condition fields
- BFE enumeration from `netsh wfp`, ETW, debugger state, or user-mode management code

What it does **not** prove:
- that this specific network event satisfied the conditions
- that a classify callback entered
- that the layer's semantics match the analyst's claim: connect authorization, inbound accept, flow tracking, redirect, stream inspection, packet modification, or logging-after-discard

Stop when:
- the relevant layer, filter id, callout key, conditions, weight/order, and expected event class are frozen for one representative traffic event.

### 3.3 Classify-entry / input-selection truth

What it proves:
- the filter engine delivered one classify indication to the callout because the layer/filter path matched
- the callback received a specific set of fixed values, metadata, raw/layer data, filter info, and flow context

Useful evidence:
- breakpoint at `classifyFn` with `inFixedValues`, `inMetaValues`, `layerData`, `filter`, `flowContext`, and `classifyOut`
- layer-specific decode of local/remote tuple, process id / app id, protocol, interface, compartment, direction, and token/app-container fields when present
- `layerData` kind: `NET_BUFFER_LIST`, stream packet, null metadata-only indication, redirect record, or layer-specific structure
- flow context lookup or association for stateful decisions

What it does **not** prove:
- that the callback wrote a permit/block/continue decision
- that the input fields used by policy were trustworthy or complete
- that later async completion/reinjection/discard occurred

Stop when:
- one classify entry is tied to one event/layer and the policy input slice that the target actually uses.

### 3.4 Decision-write truth

What it proves:
- the callout suggested an action or declined to decide through `classifyOut->actionType`, `rights`, and `flags`
- the callback's immediate verdict can now be separated from mere callback entry

Useful evidence:
- `FWPS_CLASSIFY_OUT*` before/after: `actionType`, `rights`, `flags`, `filterId`
- writes to `FWP_ACTION_BLOCK`, `FWP_ACTION_PERMIT`, `FWP_ACTION_CONTINUE`, `FWP_ACTION_NONE`, or no write
- `FWPS_RIGHT_ACTION_WRITE` state and whether the code clears action-write rights
- `FWPS_CLASSIFY_OUT_FLAG_ABSORB` when packet modification, silent drop, or reinjection patterns are possible
- local rule/cache decision that feeds the action write

What it does **not** prove:
- that a later layer, reauthorization, reinjection, socket result, or policy consumer behaved as inferred
- that an async path is complete
- that a block/permitted result is visible to user mode or the remote peer

Stop when:
- the immediate action, rights, flags, and local decision source are captured for the representative classify call.

### 3.5 Async ownership truth

What it proves:
- the callout did not finish all decision work synchronously; it retained or transformed the proof object through a layer-specific async mechanism
- the next truthful owner may be a worker queue, user-mode service, cloned packet, stream buffer, or reauthorization state table

Useful evidence:
- ALE: `FwpsPendOperation*`, operation handle/state key, `FwpsCompleteOperation*`, reauthorization classify, `FWP_CONDITION_FLAG_IS_REAUTHORIZE`
- packet: block+absorb, referenced/cloned `NET_BUFFER_LIST`, clone id, worker queue, injection/discard path
- stream: clone/need-more-data state, stream injection helper, ordered-delivery constraints, per-flow pending state
- user-mode / service handoff: ALPC/RPC/named-pipe/IOCTL/shared queue, request id, verdict reply, timeout, disconnect, fail-open/fail-closed branch
- flow context lifetime: associate, lookup, delete, and `flowDeleteFn` cleanup

What it does **not** prove:
- that completion used the intended decision
- that a cloned packet was reinjected rather than discarded, or vice versa
- that a pended ALE operation's reauthorization returned the verdict expected by the first callback

Stop when:
- the async-owned object, correlation key, owner service/worker, timeout policy, and completion route are frozen.

### 3.6 Completion / reinjection / discard truth

What it proves:
- the async path resolved into a layer-specific finalization: ALE completion and reauthorization, packet reinjection/discard, stream injection/drop, redirect application, or flow-state update
- the network stack had a concrete next action for this event

Useful evidence:
- `FwpsCompleteOperation*` status and reauthorization callback with the stored decision
- injection helper call, completion callback, injected clone identity, or discard branch
- redirect target applied and later connect/flow event reflecting the redirected tuple
- flow delete cleanup and state retirement
- socket API status, packet trace, ETW/WFP event, firewall log, or remote-visible effect

What it does **not** prove:
- that a policy alert/log/quarantine/UI/report consumer ran
- that similar flows were handled the same way
- that the same component owns malware/EDR behavior beyond this network event

Stop when:
- the final WFP/network disposition is paired with one socket-visible, packet-visible, or policy-owned effect.

## 4. Breakpoint / hook plan

Prefer one representative event over global WFP inventory.

1. Registration and management attachment:
   - `FwpsCalloutRegister*`, `FwpmCalloutAdd*`, `FwpmSubLayerAdd*`, `FwpmFilterAdd*`, filter id / callout key / layer / conditions / weight.
2. Classify delivery:
   - selected `classifyFn`; capture layer, direction, tuple, process/app identity, metadata, `filter`, `flowContext`, and `layerData` kind.
3. Input reducer:
   - field normalization, process/app lookup, rule/cache lookup, flow-context lookup, redirect target selection, packet/stream parser entry.
4. Immediate decision:
   - `classifyOut->rights`, `actionType`, `flags`, action-write clearing, absorb flag, and local result.
5. Async handoff if present:
   - `FwpsPendOperation*`, clone/reference/absorb, worker queue, user-mode request, timeout/fallback, flow-context state.
6. Completion/effect:
   - `FwpsCompleteOperation*`, reauthorization classify, injection/discard, redirect application, socket return, packet trace, WFP/ETW log, and first policy/log/alert consumer.

## 5. False-stop checklist

Before claiming "the WFP driver blocked/allowed/redirected this traffic," rule out:

- **Registration false stop**: `FwpsCalloutRegister*` is visible, but no management callout/filter references it for this traffic.
- **Filter-match false stop**: a filter exists, but layer, direction, weight, condition, app-id, interface, or provider-context mismatch prevents this event from reaching it.
- **Layer-semantics false stop**: the hit is flow-established, discard logging, redirect, stream, or packet inspection, not the authorization point the claim needs.
- **Callback-entry false stop**: `classifyFn` entered, but it only logs, associates flow context, or returns/continues without action-write ownership.
- **Decision-rights false stop**: `classifyOut->rights` did not allow the claimed write, or the code only vetoed/continued under higher-weight filter constraints.
- **Absorb/reinject false stop**: `BLOCK|ABSORB` was used for packet modification, but the clone was later reinjected.
- **Async false stop**: an operation was pended or packet cloned, but no correlated completion, reauthorization, injection, or discard path is proved.
- **User-mode-verdict false stop**: a request was sent to a service, but the reply, timeout, fail-open/fail-closed branch, or correlation key is missing.
- **Effect false stop**: WFP disposition is captured, but socket status, packet trace, alert/log, redirect consequence, or first downstream consumer is still inferred.

## 6. Evidence table shape

For one representative network event, record:

```text
driver / provider:
callout key / runtime id:
filter id / sublayer / weight:
layer / direction:
traffic tuple:
process / app id / token fields:
conditions matched:
classifyFn entry:
metadata / flow context:
layerData kind:
policy inputs selected:
local rule/cache id:
rights before action:
actionType / flags after action:
action-write cleared:
async mechanism:
pend / clone / absorb / redirect id:
worker or user-mode handoff:
verdict / timeout / fallback:
completion / reauthorization:
reinjection / discard / redirect applied:
socket-visible / packet-visible result:
first downstream consumer/effect:
false stops ruled out:
```

## 7. Hand-off rules

- If the decisive proof object moves to a user-mode service over ALPC, RPC, named pipe, COM, IOCTL, or shared memory, preserve the WFP request/correlation id and hand off to the relevant native IPC or service-worker note.
- If the WFP component only emits telemetry, hand off to ETW / runtime-evidence pages instead of narrating enforcement.
- If the same seam appears in EDR, AV, firewall, VPN, malware, or C2 traffic analysis, use this page to freeze network-filter proof, then hand off to malware comms, detection-rule, reporting, or policy-effect pages.
- If the case is packet/stream modification rather than authorization, treat clone/absorb/injection as the primary proof object and avoid claiming allow/block until final stack-visible behavior is captured.
- If the target uses WFP redirection, keep original tuple, redirect target, reauthorization, and later socket/flow consumer separate before attributing behavior to a proxy, VPN, or security product.

## 8. Sources / provenance

- `sources/native/2026-06-15-windows-wfp-callout-policy-consumer-notes.md`
- `sources/native/2026-06-15-0450-windows-wfp-callout-search-layer.json`
- Microsoft Learn, `Registering Callouts with the Filter Engine` - https://learn.microsoft.com/en-us/windows-hardware/drivers/network/registering-callouts-with-the-filter-engine
- Microsoft Learn, `Processing Classify Callouts` - https://learn.microsoft.com/en-us/windows-hardware/drivers/network/processing-classify-callouts
- Microsoft Learn, `Processing Classify Callouts Asynchronously` - https://learn.microsoft.com/en-us/windows-hardware/drivers/network/processing-classify-callouts-asynchronously
- Microsoft Learn, `FWPS_CALLOUT_CLASSIFY_FN0` - https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/fwpsk/nc-fwpsk-fwps_callout_classify_fn0
- Microsoft Learn, `FWPS_CLASSIFY_OUT0` - https://learn.microsoft.com/en-us/windows/win32/api/fwpstypes/ns-fwpstypes-fwps_classify_out0
- Microsoft Learn, `ALE Layers` - https://learn.microsoft.com/en-us/windows/win32/fwp/ale-layers
