# Pending-request timeout and late-reply lifecycle notes

Date: 2026-03-23
Scope: practical notes for protocol / RPC / message-queue / firmware-adjacent cases where a reply or completion looks structurally plausible, but arrives after the outstanding request owner has timed out, been cleaned up, or otherwise lost ownership.

## Why this source batch matters
The KB already had a narrow practical note for pending-request ownership and async-reply consumption.
What still needed sharpening was a recurring operator mistake:
- seeing a structurally plausible late reply
- confirming that parser-visible fields and even correlation material still look reasonable
- then blaming parser incompleteness or crypto mismatch
- when the real gate is that the pending owner has already been retired and the runtime now treats the reply as stale, late, or unknown

This batch does not justify a whole new branch.
It does justify making the existing pending-request workflow note more practical around owner lifetime, timeout cleanup, and late-reply discard behavior.

## Retained sources

### 1. RabbitMQ RPC tutorial
URL: https://www.rabbitmq.com/tutorials/tutorial-six-java

Retained points:
- the client creates a callback queue and gives each request a unique `correlationId`
- when a response arrives, the client checks whether the `correlationId` matches the outstanding request it is waiting for
- unknown correlation values are intentionally treated as ignorable rather than as successful replies

Operator value:
- strong minimal model for why a structurally plausible reply can still be irrelevant if it no longer belongs to one live outstanding request

### 2. Spring AMQP request/reply documentation
URL: https://docs.spring.io/spring-amqp/reference/amqp/request-reply.html

Retained points:
- request/reply operations have a reply timeout
- `replyTimedOut` exists so implementations can clean up retained state on timeout
- failed deliveries include late replies and messages received without a correlation header
- the framework explicitly treats late replies as a distinct failure/cleanup class rather than as ordinary successful replies

Operator value:
- clean source-backed example that late replies after timeout belong in an ownership-lifecycle bucket
- useful for RE cases where the question is no longer “can this parse?” but “does a live request owner still exist to consume it?”

### 3. Microsoft Learn - [MS-RPCE]: Connection Time-Out
URL: https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-rpce/678e4235-0a3b-4b81-99fb-86ae3ac357f3

Retained points:
- higher-level protocols can instruct the runtime to monitor connection state so recovery action can occur if the client crashes or loses connectivity
- a common recovery action is context-handle rundown
- timeout/expiry handling is therefore not merely transport absence; it can retire state that later affects whether work remains meaningful

Operator value:
- useful conservative support for the idea that timeout/loss events can invalidate runtime-owned request context
- especially relevant in RPC-shaped cases where a late arrival is no longer attached to a still-live logical operation

### 4. RabbitMQ Java client / discussion snippets surfaced by multi-source search
URLs surfaced by search layer:
- https://github.com/rabbitmq/rabbitmq-java-client/blob/master/src/main/java/com/rabbitmq/client/RpcClient.java
- https://stackoverflow.com/questions/29789329/fixed-reply-queue-times-out-after-second-message
- https://stackoverflow.com/questions/56615866/rabbitmq-rpc-and-correlation-id-matching

Retained points:
- real implementations and user reports surface the exact shape we care about: outstanding-request maps, timeout cleanup, and warnings/errors when a reply arrives but no longer matches a live outstanding request
- the repeated wording pattern is effectively “no outstanding request for correlation ID” / “reply received after timeout”

Operator value:
- these are useful corroborating examples of the failure shape, even though the KB should phrase the conclusion conservatively and avoid framework-specific overclaiming

## Cross-source synthesis
A durable workflow lesson emerges:

```text
request family already known
  -> plausible reply/completion arrives
  -> runtime had already timed out, canceled, or cleaned up the owner
  -> reply is routed into stale/unknown/late handling instead of wakeup/consume
  -> the true next task is owner-lifecycle proof, not broader parser speculation
```

High-value lifecycle questions suggested by this batch:
- where is the outstanding owner inserted?
- where is timeout/cancel cleanup performed?
- what late/unknown-reply branch is taken if the owner is gone?
- is there a generation/epoch/channel reuse boundary where the same visible token is no longer sufficient?

## What this batch does *not* justify
Do not overclaim from this source set.
It does **not** prove that every ignored reply is a timeout artifact.
Other gates still exist:
- freshness / nonce / replay-window checks
- auth / MAC / session binding
- wrong serializer or wrong transport wrapper
- reply never actually emitted

The narrower justified claim is:
- late replies after timeout/cleanup are common enough, practical enough, and source-backed enough that the pending-request workflow note should explicitly tell analysts to check owner lifetime before blaming parser or crypto incompleteness

## KB action justified by this batch
This batch is strong enough to justify:
- extending `topics/protocol-pending-request-correlation-and-async-reply-workflow-note.md`
  - with explicit timeout/cancel cleanup as a local role
  - with a dedicated lifecycle-check step
  - with a concrete late-reply-after-timeout scenario
- surfacing that note more clearly from the protocol/firmware subtree guide and index
