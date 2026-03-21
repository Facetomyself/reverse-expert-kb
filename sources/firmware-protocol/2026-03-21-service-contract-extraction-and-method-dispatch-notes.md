# Source Notes — 2026-03-21 — Service-contract extraction / method-dispatch recovery for protocol and RPC reversing

## Source set
Search mode and policy:
- explicit multi-source search via `search-layer` with `--source exa,tavily,grok`
- queries centered on RPC reverse engineering, service-contract extraction, method-dispatch recovery, and schema/harness workflow bridging

Primary retained sources reviewed:
- <https://github.com/marin-m/pbtk>
- <https://labs.ioactive.com/2021/07/breaking-protocol-buffers-reverse.html>
- <https://blog.xpnsec.com/analysing-rpc-with-ghidra-neo4j>
- <https://specterops.io/blog/2023/10/18/uncovering-rpc-servers-through-windows-api-analysis/>
- supportive search-only signals from RpcView, protobuf reverse-engineering discussions, and protocol-inference papers

Existing KB materials consulted for fit:
- `topics/protocol-layer-peeling-and-contract-recovery-workflow-note.md`
- `topics/protocol-schema-externalization-and-replay-harness-workflow-note.md`
- `topics/protocol-firmware-practical-subtree-guide.md`
- `topics/protocol-state-and-message-recovery.md`

## Why this source cluster was chosen
The protocol / firmware branch already had practical notes for:
- boundary relocation
- socket-boundary truth selection
- layer peeling into one smaller trustworthy contract
- schema externalization into a replay/edit/fuzz surface
- replay gating and output handoff

But there was still a thinner practical gap around a recurring middle-stage problem:
- the analyst can already tell the family is RPC-like, protobuf-backed, or service-oriented
- yet the useful object is not merely the message shape
- it is the service shell, dispatch table, method roster, or registration path that turns parser knowledge into a callable or traceable contract

This source cluster supports a concrete operator continuation:
- extract one service contract and one method-dispatch surface before widening into replay-gate or whole-client reimplementation work

## Strong recurring ideas

### 1. Registration and dispatch structures are often the fastest route to the real callable contract
The IOActive gRPC write-up is valuable because it emphasizes practical anchor points like:
- service registration calls
- generated service classes
- method implementations attached to those classes
- transport setup that tells you which outer shell matters and which parts are just framework boilerplate

Practical implication:
- in RPC-shaped binaries, the useful next object is often not raw frame archaeology
- it is the first registration or service-constructor path that names the callable surface and narrows the search to real handlers

### 2. RPC server internals often expose stable enumeration pivots even when high-level IDL is absent
The XPN RPC analysis is high-signal because it treats Windows RPC reversing as a structured traversal problem:
- locate the runtime server root
- enumerate registered interfaces
- extract dispatch tables and interpreter metadata
- then reduce from interfaces to routines that matter

Practical implication:
- when full source schema or IDL is missing, interface dictionaries, dispatch tables, server info objects, and method arrays can still externalize a usable contract shell
- that shell is enough to organize later handler proof or harness targeting

### 3. API-wrapper analysis is often enough to recover contract-bearing structures even without a purpose-built RPC tool
The SpecterOps walkthrough is useful here not because it is an RPC-enumeration clone, but because it reinforces a durable technique:
- start from public wrappers or exported setup APIs
- follow argument normalization and runtime registration calls
- identify the concrete structures passed to the subsystem that owns the callable contract

Practical implication:
- contract extraction can begin from ordinary API-analysis discipline, not only specialized protocol tooling
- that matters for mixed or proprietary RPC families where no mature enumerator exists

### 4. Protobuf extraction becomes much more valuable once it is tied to endpoint or method identity
PBTK is again important here because it does not stop at `.proto` recovery.
It also treats schema as something that should connect to:
- concrete endpoints
- samples
- serialization/deserialization
- replay and fuzz workflows

Practical implication:
- a recovered message schema is stronger when attached to one service path, method name, opcode family, or dispatch slot
- otherwise it risks remaining a detached parser aid rather than a usable interaction contract

### 5. The right first output is usually one service shell plus one representative method family
Across the sources, a strong anti-drift rule appears:
- do not jump from “I found a dispatch table” to “I should reconstruct the whole client stack”
- do not jump from “I recovered protobuf messages” to “I already understand the service semantics”

A better first stopping point is:
- one service shell or method roster
- one representative request/response family
- one registration/dispatch anchor
- one note on remaining auth/session/transport obligations

### 6. Contract extraction and handler proof should stay separate
A repeated lesson from this source batch:
- service registration and method rosters tell you what can be called
- they do not by themselves prove what state consequences each method has
- dispatch recovery and handler consequence proof are adjacent but distinct jobs

Practical implication:
- the KB should keep service-contract extraction separate from parser-to-state or consequence localization
- otherwise analysts either overclaim semantics too early or stay stuck cataloging call surfaces without choosing one representative method

## Concrete operator takeaways worth preserving

### A. Registration-first rule for RPC-shaped targets
When a target looks gRPC / Windows RPC / generated-stub / service-oriented:
1. search first for registration, builder, or server-start anchors
2. enumerate service objects, interface structures, or dispatch tables
3. externalize one service shell and one representative method family
4. only then decide whether the next bottleneck is schema recovery, handler consequence, replay gating, or transport handoff

### B. Dispatch-table rule when names are sparse but structure is stable
If symbolic names are weak or stripped:
1. recover interface arrays, dispatch counts, or method tables
2. label slots conservatively by index, UUID, opcode, or transport path
3. attach one representative request/response family to one slot
4. use that smaller contract to choose the next trace or replay target

### C. Service-shell-plus-schema rule
A recovered schema should ideally be tied to one of:
- method name
- endpoint path
- opcode family
- dispatch slot
- registration object

That attachment makes the contract operational rather than merely descriptive.

### D. Representative-method stop rule
A strong first result is usually:
- one service shell
- one representative method
- one request/response or input/output family
- one dispatch/registration anchor
- one explicit note about remaining state/auth/output obligations

That is usually enough to hand off into:
- schema externalization / replay harness work
- parser-to-state consequence proof
- replay-precondition / state-gate localization

## Candidate KB implications
This source batch supports a concrete practical leaf in the protocol / firmware branch:
- a workflow note after broad layer peeling, but before replay-gate or state-consequence work
- focused on service-contract extraction and method-dispatch recovery for RPC-shaped or service-oriented protocol families

This note should help analysts decide when to:
- stop broad “it looks RPC-like” narration
- stop detached schema-only polishing
- turn one registration/dispatch surface into one reusable contract-bearing object

## Confidence / quality note
This source set is strong for:
- registration/dispatch-first heuristics
- practical separation between service-shell extraction and later handler/state proof
- tying protobuf/schema work to a callable method surface

It is intentionally conservative about universality:
- not every protocol family exposes a clean dispatch table
- not every service shell yields replay success without later state/auth work
- not every recovered method roster implies complete semantics
