# Windows WFP Callout Classify to Policy Consumer Notes - 2026-06-15

Source class: external research notes
Related topic: `topics/native-windows-wfp-callout-classify-to-policy-consumer-workflow-note.md`
Search artifact: `sources/native/2026-06-15-0450-windows-wfp-callout-search-layer.json`

## Why this source pass was useful

The native branch had good Windows telemetry (`ETW`) and file-system policy-driver (`minifilter`) seams, but not a network-filter counterpart for Windows Filtering Platform (WFP) callout drivers. WFP is common in firewall, VPN, EDR, AV, parental-control, network-inspection, and redirection components, and it creates the same evidence trap as minifilters: registration or callback entry is easy to see, but the actual allow/block/redirect/inject/logging consumer may be later and layer-dependent.

The useful practical seam is:

```text
callout registered != filter attached/matched != classifyFn entered != decision rights writable != async pended/cloned/absorbed != completed/reinjected/discarded != network/user-visible effect owned
```

## Source-backed facts to preserve

### Callout registration is only registration truth

Microsoft's callout registration material shows a callout driver registering one or more callouts with `FwpsCalloutRegister0(...)`, using an `FWPS_CALLOUT0` structure that contains a callout GUID plus `ClassifyFn`, `NotifyFn`, and `FlowDeleteFn` callbacks. A successful call gives a run-time callout identifier corresponding to the callout key.

Operator consequence:
- `FwpsCalloutRegister*` proves the driver registered callback functions with the filter engine.
- It does not prove that a user-mode management object was added, that a filter matched this traffic, or that this callout's `classifyFn` made a policy decision for the flow/packet under analysis.

Source:
- Microsoft Learn, `Registering Callouts with the Filter Engine` - https://learn.microsoft.com/en-us/windows-hardware/drivers/network/registering-callouts-with-the-filter-engine

### Filter / layer match gates classifyFn delivery

Microsoft's classify material states that the filter engine calls a callout's `classifyFn` when there is network data to process and all filtering conditions are true for a filter that specifies the callout as the action. The data supplied to `classifyFn` depends on the specific filtering layer: fixed values, metadata, raw data, filter information, and any flow context.

Operator consequence:
- A `classifyFn` hit is stronger than registration, but it still proves only that the filter/layer/condition path delivered this indication.
- The analyst must capture layer, direction, `inFixedValues`, `inMetaValues`, `layerData`, `filter`, and `flowContext` before interpreting the callback as outbound connect, inbound accept, stream inspection, packet inspection, redirection, or flow-state tracking.

Sources:
- Microsoft Learn, `Processing Classify Callouts` - https://learn.microsoft.com/en-us/windows-hardware/drivers/network/processing-classify-callouts
- Microsoft Learn, `FWPS_CALLOUT_CLASSIFY_FN0` - https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/fwpsk/nc-fwpsk-fwps_callout_classify_fn0

### `classifyOut` is a decision object, not a magic effect object

`FWPS_CLASSIFY_OUT0` contains `actionType`, `rights`, and `flags`. The action may be `FWP_ACTION_BLOCK`, `FWP_ACTION_CONTINUE`, `FWP_ACTION_PERMIT`, and related no-action variants. Write access to the action is controlled by `FWPS_RIGHT_ACTION_WRITE`; block actions can also use `FWPS_CLASSIFY_OUT_FLAG_ABSORB` for silent drop/packet-modification patterns.

Operator consequence:
- A function named `ClassifyFn` or a callback hit is weaker than a captured `classifyOut->actionType` write with the relevant rights/flags and layer semantics.
- `CONTINUE`, missing `FWPS_RIGHT_ACTION_WRITE`, higher-weight filter interaction, absorb-with-reinject patterns, or packet/stream clone paths can make a naive "blocked/permitted" claim wrong.

Source:
- Microsoft Learn, `FWPS_CLASSIFY_OUT0` - https://learn.microsoft.com/en-us/windows/win32/api/fwpstypes/ns-fwpstypes-fwps_classify_out0

### Asynchronous classify changes the proof object

Microsoft's asynchronous classify guidance separates immediate permit/block/continue from cases where the callout forwards fields, metadata, or packets to another component such as a user-mode application. The mechanism differs by layer:

- asynchronous ALE classify uses `FwpsPendOperation0(...)` and completes with `FwpsCompleteOperation0(...)`
- packet classify typically blocks with `FWPS_CLASSIFY_OUT_FLAG_ABSORB`, references/clones packets, then completes by reinjecting a cloned/modified packet or silently discarding it
- stream layers use stream clone/injection helpers and ordered-delivery constraints
- ALE connect completion triggers a reauthorization classify where the decision should be returned
- ALE flow-established layers do not support asynchronous processing

Operator consequence:
- An async handoff is a separate evidence boundary. The held operation/clone, user-mode or worker decision, reauthorization, reinjection/discard, and later socket-visible result must be correlated.
- A packet absorbed for modification is not automatically a durable block; it may be reinjected. A pended ALE operation is not decided until completion and reauthorization are observed.

Source:
- Microsoft Learn, `Processing Classify Callouts Asynchronously` - https://learn.microsoft.com/en-us/windows-hardware/drivers/network/processing-classify-callouts-asynchronously

### ALE layers decide what event is actually being authorized

Microsoft's ALE layer reference separates resource assignment, listen, receive/accept, connect, flow-established, endpoint closure, and redirect layers. For example, `ALE_AUTH_CONNECT` matches TCP `connect()` and first outbound UDP packets to a unique remote address/port tuple; `ALE_AUTH_RECV_ACCEPT` matches TCP `accept()` and first inbound UDP packets from a unique remote tuple; `ALE_FLOW_ESTABLISHED` is flow-state tracking and should not return block/permit.

Operator consequence:
- A WFP hit must be interpreted through its layer and direction. A flow-established callback is not the same proof object as an outbound connect authorization; an ALE discard layer is often logging after a drop rather than the original decision owner.
- Redirect layers are address/port mutation seams and should be separated from permit/block or packet-modification claims.

Source:
- Microsoft Learn, `ALE Layers` - https://learn.microsoft.com/en-us/windows/win32/fwp/ale-layers

### Public case material confirms EDR/network-inspection shape but is secondary

Search surfaced Quarkslab's Defender network-inspection driver write-up and public WFP callout examples. These are useful as implementation-shape cues: WFP is used in real network inspection/security products, callouts are attached at layers/sub-layers with conditions, and Defender-like drivers may inspect connection establishment / traffic paths. They should not replace Microsoft API docs as normative semantics.

Sources:
- Quarkslab, `Guided tour inside WinDefender’s network inspection driver` - https://blog.quarkslab.com/guided-tour-inside-windefenders-network-inspection-driver.html
- GitHub, `0mWindyBug/WFPCalloutReserach` - https://github.com/0mWindyBug/WFPCalloutReserach
- Pavel Yosifovich, `Introduction to the Windows Filtering Platform` - https://scorpiosoftware.net/2022/12/25/introduction-to-the-windows-filtering-platform

## Practical synthesis

For reversing, the most useful table is one row per representative network event:

```text
provider/driver:
callout key / runtime id:
filter id / sublayer / weight:
layer:
direction:
process / app id / token fields:
local/remote tuple:
metadata / flow context:
layerData kind:
classifyFn hit:
rights before write:
actionType / flags after write:
async path:
pend / clone / absorb id:
worker or user-mode handoff:
reply / verdict / timeout:
completion / reauthorization:
reinjection / discard:
socket-visible or packet-visible result:
first policy/log/alert/consumer:
false stops ruled out:
```

The source-backed branch memory to add is:

```text
registered != filter-matched != classify-entered != decision-written != async-owned != completed/reinjected/discarded != effect-owned
```
