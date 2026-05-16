# Protocol Netlink Message to Consumer Workflow Note

Topic class: concrete workflow note
Ontology layers: protocol / firmware practical workflow, Linux Netlink ownership, ACK/dump/notification truth, first local consumer proof
Maturity: practical
Related pages:
- topics/protocol-firmware-practical-subtree-guide.md
- topics/protocol-ingress-ownership-and-receive-path-workflow-note.md
- topics/protocol-parser-to-state-edge-localization-workflow-note.md
- topics/protocol-replay-precondition-and-state-gate-workflow-note.md
- topics/native-dbus-service-activation-to-method-consumer-workflow-note.md
- topics/native-inotify-fanotify-first-event-consumer-workflow-note.md
Related source notes:
- sources/protocol/2026-05-17-netlink-message-to-consumer-notes.md

## 1. Why this note exists
This note exists for Linux Netlink-shaped cases where:
- `socket(AF_NETLINK, ...)`, `sendmsg(...)`, `recvmsg(...)`, libnl/libmnl, rtnetlink, Generic Netlink, connector, audit, uevent, or netfilter Netlink paths are already visible
- the operator can see headers or attributes, but cannot yet prove which request, dump, notification, callback, parser, or state consumer owns the behavior
- a visible ACK, port ID, sequence number, multicast event, or family name is being overread as a complete behavior claim

The mistake this note prevents is:

```text
Netlink traffic visible == kernel/user-space state transition proved
```

The smaller truthful ladder is:

```text
family/control discovered
  != operation/command selected
  != request accepted / ACKed
  != dump completed consistently
  != notification delivered to this socket
  != local callback/parser consumed it
  != state/effect owned by that consumer
```

## 2. When to use this note
Use this note when most of these are true:
- the target is Linux user space, kernel-adjacent userland, embedded Linux firmware, network/configuration software, container/runtime plumbing, or kernel-adjacent malware
- Netlink traffic or APIs are already visible enough that the remaining question is not “does communication exist?”
- behavior differs across runs because of ACK handling, sequence matching, dump completion, multicast subscription, socket identity, dropped notification, or local dispatch
- the next useful artifact is one proved request/reply/notification-to-consumer chain, not a broad inventory of Netlink families

Do **not** use this note when:
- the protocol family is still unknown at the socket/framing level; use boundary relocation or layer peeling first
- the main issue is a higher-level RPC/service contract that only happens to use Netlink as one internal transport
- the path has already reached a specific parser/state edge; use parser-to-state or replay-precondition notes next

## 3. Core claim
Netlink analysis should keep six proof objects separate:
1. **family / control discovery truth** — which classic family or Generic Netlink family is being addressed
2. **operation / command truth** — which `nlmsg_type`, `genlmsghdr.cmd`, connector `cb_id`, or family operation is selected
3. **request acceptance truth** — whether an ACK / `NLMSG_ERROR(error == 0)` or error response corresponds to the request
4. **dump / stream completeness truth** — whether multipart dump traversal reached `NLMSG_DONE` and avoided inconsistency/loss
5. **notification delivery truth** — whether the current socket subscribed to and received the relevant multicast/unicast event
6. **consumer / effect truth** — which local callback, parser, handler, cache update, policy reducer, or state write actually uses the message

## 4. Source-backed anchors
Conservative anchors from Linux kernel documentation and man pages:
- Netlink uses sockets, a fixed `nlmsghdr`, protocol-specific headers such as `genlmsghdr`, and TLV attributes.
- Generic Netlink uses `nlmsg_type` as the family ID and `genlmsghdr.cmd` as the operation; Classic Netlink families may encode operation differently.
- Common exchange shapes are `do`, `dump`, and multicast notification.
- `NLM_F_ACK` causes acknowledgements; success ACK is an `NLMSG_ERROR` payload with `error == 0`.
- `nlmsg_seq` is echoed for request/reply matching; async notifications normally use sequence 0.
- `nlmsg_pid` is a Netlink port ID, not a guaranteed process ID; one process can have multiple Netlink sockets.
- Multipart replies end with `NLMSG_DONE`; dump inconsistency may be reported with flags such as `NLM_F_DUMP_INTR`.
- Kernel-to-user Netlink delivery can lose messages under memory pressure or full receive queues, so absence of a notification is not always absence of state change.

Operator consequence:
- an ACK proves acceptance/processing status for the request boundary, not necessarily downstream effect ownership
- a multicast event proves delivery only after subscription and socket identity are pinned, and still needs local consumer proof
- a dump proves a snapshot only when completion and consistency are accounted for

## 5. Boundary objects to keep separate
### A. Socket and family truth
Freeze:
- Netlink protocol (`NETLINK_ROUTE`, `NETLINK_GENERIC`, `NETLINK_AUDIT`, connector, etc.)
- classic family versus Generic Netlink
- resolved Generic Netlink family ID and family name, if applicable
- whether the trace is control-plane discovery (`CTRL_CMD_GETFAMILY`) rather than the target operation

### B. Operation / command truth
Freeze:
- `nlmsg_type`
- `nlmsg_flags`
- `genlmsghdr.cmd`, connector `cb_id`, or family-specific message type
- attribute IDs and lengths that select the actual request path

Practical stop rule:
- do not treat “family resolved” as “operation selected.”

### C. Request/ACK truth
Freeze:
- outbound `nlmsg_seq`
- whether `NLM_F_ACK` was requested
- matching response sequence
- `NLMSG_ERROR` error code and extended ACK TLVs when present

Practical stop rule:
- do not treat `error == 0` ACK as proof of later state/effect consumption.

### D. Dump completeness truth
For dump-shaped exchanges, freeze:
- initial dump request and flags
- all multipart chunks observed in the current receive loop
- `NLMSG_DONE`
- inconsistency/loss indicators and any resync path

Practical stop rule:
- one `recvmsg(...)` with objects is not the dump; the dump is the completed multipart exchange plus consistency posture.

### E. Notification delivery truth
For multicast/asynchronous paths, freeze:
- group subscription / membership change
- destination port ID / group
- notification command distinct from reply command, if the family separates them
- sequence behavior, often `nlmsg_seq == 0` for async notifications
- receive queue loss / `ENOBUFS` / resync handling

Practical stop rule:
- a kernel-side notification send site is weaker than delivery to this socket, and delivery is weaker than local callback/parser consumption.

### F. Consumer / effect truth
Only after the right message is tied to the right local owner should the analyst claim behavior.
Freeze the first:
- callback dispatch
- parser branch
- cache/state update
- policy decision
- user-visible or kernel-visible effect

## 6. Default workflow
### Step 1: Classify the exchange shape
Label the current slice as one of:
- `do` request/reply
- `dump` request/multipart reply
- multicast/asynchronous notification
- connector callback/message genealogy

This prevents mixing ACK, dump, and notification evidence into one claim.

### Step 2: Separate control discovery from target operation
For Generic Netlink, first ask:
- is this only `CTRL_CMD_GETFAMILY` or family/multicast-group discovery?
- where does the target family command begin?

Freeze family resolution, then move to command proof.

### Step 3: Correlate by sequence and port ID conservatively
Use `nlmsg_seq` and port ID as correlation aids, but record the caveats:
- async notifications may use sequence 0
- port ID is a socket identity, not always process ID
- multiple sockets in one process can break naive PID-shaped assumptions

### Step 4: Decide what the ACK actually proves
If `NLM_F_ACK` / `NLMSG_ERROR` is visible:
- map it back to the original request header
- preserve success versus errno versus extended ACK detail
- stop at acceptance unless a later consumer/effect is observed

### Step 5: Finish dumps before interpreting object absence
If the path is dump-shaped:
- require `NLMSG_DONE` or an explicit reason the dump ended
- check for inconsistency/loss flags or receive errors
- avoid interpreting missing objects before resync if loss is plausible

### Step 6: Prove notification subscription and delivery before consumer claims
For multicast/uevent/audit/connector-like paths:
- prove group membership or subscription path
- prove delivery to the socket under analysis
- then step into the local dispatcher/parser/callback

### Step 7: Stop at the first behavior-owning consumer
Once a handler updates a cache, selects a policy branch, mutates state, or triggers a durable effect, stop broad Netlink narration and hand off one grounded chain:

```text
request/notification object -> local consumer -> state/effect
```

## 7. Cheap discriminants
- Does the request set `NLM_F_ACK`, and does the ACK sequence match the request?
- Is the visible packet a control-family lookup or the target family command?
- Is this a dump, and has `NLMSG_DONE` been observed?
- Is the message a notification with sequence 0 rather than a reply?
- Which socket owns the port ID, and are there multiple Netlink sockets in the process?
- Was the multicast group joined before the event under analysis?
- Is there any receive-side loss or resync signal before relying on absence of events?
- Which callback/parser consumes the message first?

## 8. Practical failure patterns this note prevents
- “`sendmsg(AF_NETLINK)` happened, so the kernel accepted the change.”
- “The ACK succeeded, so the downstream state definitely changed.”
- “The family ID was resolved, so I know the command path.”
- “One dump packet lacked the object, so the object was absent.”
- “`nlmsg_pid` equals PID, so this process identity is proved.”
- “A multicast send site fired, so this user-space listener consumed it.”
- “No notification arrived, so no state transition happened.”

## 9. Useful outputs
- one request/reply correlation table keyed by sequence and port ID
- one dump-completion proof with `NLMSG_DONE` / inconsistency posture
- one multicast subscription-to-callback chain
- one local parser/callback-to-state/effect chain
- one replayability judgment that says whether the comparable object is the body, the family command plus attributes, the ACKed request, the completed dump, or the notification-consumer chain

## 10. Sources
See: `sources/protocol/2026-05-17-netlink-message-to-consumer-notes.md`

Primary references:
- https://docs.kernel.org/userspace-api/netlink/intro.html
- https://kernel.org/doc/html/latest/core-api/netlink.html
- https://man7.org/linux/man-pages/man7/netlink.7.html
- https://docs.kernel.org/driver-api/connector.html
