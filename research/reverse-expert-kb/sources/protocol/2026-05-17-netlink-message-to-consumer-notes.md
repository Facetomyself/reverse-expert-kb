# Netlink Message to Consumer Notes — 2026-05-17

## Search trace
- Search output: `sources/protocol/2026-05-17-0450-netlink-message-consumer-search-layer.json`
- Requested sources: `exa,tavily,grok`
- Succeeded sources: `exa,tavily`
- Failed sources: `grok` — configured completions proxy returned HTTP 502 Bad Gateway for all three query attempts.

## Source-backed anchors
- Linux kernel Netlink introduction frames modern Netlink as a socket-based request/reply and notification interface with fixed `nlmsghdr`, optional protocol headers such as `genlmsghdr`, and TLV attributes. It explicitly separates `do`, `dump`, and multicast notification exchange shapes.
- Generic Netlink uses `nlmsg_type` for the family ID and `genlmsghdr.cmd` for the family operation. This matters because a reverser who treats `nlmsg_type` as the operation in Generic Netlink can chase the wrong dispatch boundary.
- Kernel documentation recommends `NLM_F_REQUEST | NLM_F_ACK` for `do` calls and `NLM_F_REQUEST | NLM_F_ACK | NLM_F_DUMP` for dumps. `nlmsg_seq` is echoed in responses and is the matching key for request/reply correlation; asynchronous notifications normally use sequence 0.
- `NLMSG_ERROR` carries an operation return code; success ACK is represented as `error == 0`. Extended ACK TLVs can add diagnostic detail when enabled and present.
- `NLMSG_DONE` terminates dumps and may carry dump error / extended ACK material. A multipart dump is not complete merely because one response packet was observed.
- `nlmsg_pid` is a Netlink port ID, not a guaranteed process ID. The kernel is usually port ID 0, but user-space sockets can receive automatically assigned unique port IDs when a process has multiple Netlink sockets.
- Netlink is not reliable for kernel-to-user delivery. Kernel messages may be dropped under memory pressure or full receive queues, and user space must detect loss such as `ENOBUFS` and resynchronize.
- Kernel developer notes recommend separate command IDs for notifications versus replies, useful returned data on create/add operations, and dump inconsistency reporting through `NLM_F_DUMP_INTR` when iteration can skip or repeat objects.
- Kernel connector documentation shows a Netlink-based callback-registration model: a `cb_id` selects a registered callback, `cn_msg` carries `seq`/`ack`, multicast groups can be selected, and reliability still requires preparing for loss.

## Practical synthesis
Netlink-heavy cases are easy to overread because the same capture can expose socket calls, headers, attributes, ACKs, dumps, and multicast notifications. Those are not the same proof object.

The useful reverse-engineering split is:

```text
family/control discovered
  != operation/command selected
  != request accepted / ACKed
  != dump completed consistently
  != notification delivered to this socket
  != local callback/parser consumed it
  != state/effect owned by that consumer
```

This split is especially useful for Linux desktop/server agents, container/network managers, kernel-adjacent malware, and firmware Linux userlands where a visible `sendmsg(AF_NETLINK)` or `recvmsg(AF_NETLINK)` trace is often only a boundary clue rather than the behavior-owning consumer.

## Operator implications
- For Generic Netlink, freeze family ID resolution separately from command dispatch; `CTRL_CMD_GETFAMILY` / discovered family metadata is not the target operation.
- Treat `NLM_F_ACK` / `NLMSG_ERROR(error == 0)` as request acceptance, not downstream state change.
- Treat one dump response as incomplete until `NLMSG_DONE` and dump consistency are accounted for.
- Treat multicast notification visibility as weaker than subscription truth plus delivery to the current socket plus local callback/parser consumption.
- Treat `nlmsg_seq` and `nlmsg_pid` as correlation aids, not as complete ownership proof; port ID reuse, multiple sockets, async notifications, and sequence-0 notifications can break naive matching.
- When delivery loss is plausible, add a resynchronization check before using absence of notification as evidence that no state change occurred.

## Primary references
- https://docs.kernel.org/userspace-api/netlink/intro.html
- https://kernel.org/doc/html/latest/core-api/netlink.html
- https://man7.org/linux/man-pages/man7/netlink.7.html
- https://docs.kernel.org/driver-api/connector.html
