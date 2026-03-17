# Native Callback-Registration to Event-Loop Consumer Workflow Note

Topic class: workflow note
Ontology layers: workflow/sensemaking, runtime-evidence bridge, native baseline practical branch
Maturity: emerging
Related pages:
- topics/native-binary-reversing-baseline.md
- topics/native-interface-to-state-proof-workflow-note.md
- topics/runtime-behavior-recovery.md
- topics/record-replay-and-omniscient-debugging.md
- topics/causal-write-and-reverse-causality-localization-workflow-note.md

## 1. What this workflow note is for
This note covers a recurring native desktop/server reversing case:

- static structure is already readable enough to navigate
- registrations, callbacks, message handlers, reactor loops, or completion paths are visible
- the analyst can tell the subsystem is event-driven or async enough that direct call-graph reading is misleading
- but the investigation still stalls because no one has proved which callback family or loop consumer actually owns the first consequence-bearing behavior

This is not mainly the protected-target problem of reducing transformation churn.
It is not mainly the mobile problem of obtaining an observation foothold.
It is the native baseline problem of having **visible async structure with unclear behavioral ownership**.

The goal is to move from:

```text
many visible registrations, handlers, and dispatch helpers
```

to:

```text
one proved chain from registration or event source
through one queue/dispatch/selection boundary
into one consequence-bearing consumer and one downstream effect
```

## 2. When to use this note
Use this note when most of the following are true:
- the target behaves like a relatively ordinary native binary rather than a heavily environment-constrained mobile, firmware, or highly protected case
- a static map already exists, but direct caller/callee reading no longer explains real execution order
- callback tables, window procedures, observer lists, completions, timers, or event-loop helpers are already visible
- the current bottleneck is not “what code is related?” but “which asynchronous handoff actually matters first?”
- one narrow dynamic proof would collapse a lot of uncertainty

Do **not** use this as the primary guide when:
- interface routing itself is still unclear and `topics/native-interface-to-state-proof-workflow-note.md` is the better first step
- the main bottleneck is still semantic-anchor stabilization
- the target is really a protocol parser/state-gate or protected-runtime case in disguise
- packed/unpacked readiness is still unresolved

## 3. Core claim
In callback-heavy native work, the next best move is often **not** to keep reading more registration and dispatch code.
It is to separate registration from real delivery, choose one candidate callback family or loop consumer, and prove the first queue/dispatch/consumer edge that predicts a real downstream effect.

The key practical question is usually:

```text
Which posted task, dispatched event, completion delivery, or callback consumer
first changes later behavior in a way that makes the subsystem trustworthy?
```

## 4. The five boundaries to mark explicitly

### A. Event-source boundary
This is where the relevant activity becomes possible.
Typical anchors include:
- UI input or window messages
- socket or IPC readiness
- worker completion signals
- timer expiry or scheduled work wakeups
- observer/notification emissions
- parser or state-machine outputs that are later posted asynchronously

What to capture here:
- which event family actually matters for the target question
- which source gives the clearest later consequence if proved

### B. Registration / subscription boundary
This is where handlers become eligible to receive the event.
Typical anchors include:
- callback registration sites
- function-pointer or vtable assignment
- message-map setup
- observer-list insertion
- libuv/libevent/dispatch source registration
- thread-pool or completion-port association

What to capture here:
- which registration family is structurally relevant
- which parts are only plumbing versus which parts constrain later ownership

### C. Queue / dispatch-selection boundary
This is where the system decides which ready work actually gets delivered.
Typical anchors include:
- message pumps
- queue push/pop helpers
- epoll/select/kqueue reducers
- completion dequeue loops
- event-to-handler selectors
- timer wheels and delayed-task queues

What to capture here:
- the first place where visible registration becomes one concrete delivered task, callback, or handler selection

### D. Consequence-bearing consumer boundary
This is the first callback or handler that actually changes later behavior.
Typical anchors include:
- one state write or mode change
- one ownership transfer
- one queue insertion into a more specific worker or state machine
- one reply/action selection
- one persistent cache/session/object update
- one UI/service/policy transition

What to capture here:
- the narrowest consumer that predicts later behavior better than upstream registration labels alone

### E. Proof-of-effect boundary
This is where the analyst proves that the chosen consumer matters.
Typical anchors include:
- one observable output, reply, or IPC emission
- one follow-up callback or scheduled task
- one file/network/UI side effect
- one later state difference in a compare run
- one crash/guard/log family change tied to the consumer

What to capture here:
- one concrete downstream effect linked back to the chosen callback/consumer chain

## 5. Default workflow

### Step 1: choose one event family, not the whole framework
Do not start by mapping every message type or callback registration.
Choose one event family with:
- a clear external trigger or visible late effect
- one believable handler chain
- one downstream consequence you can observe

Good candidates usually have:
- the best later visibility
- the smallest number of competing consumer families
- the cleanest compare-run or hook opportunity

### Step 2: separate registration from delivery early
Label the local chain as:
- event source
- registration/subscription
- queue or dispatch selection
- consequence-bearing consumer
- effect

This prevents a common mistake: treating the first registration site as if it already explains behavior.

### Step 3: find the first real dispatch reduction
Look for the first place where many possible handlers become one delivered callback family.
Usually this is one of:
- message id or opcode selection
- queue pop plus callback pointer fetch
- completion dequeue and continuation dispatch
- event-loop reducer that routes one ready object to one handler family
- observer/filter logic that decides who actually receives the signal

If you cannot find a dispatch reduction, you are probably still reading framework plumbing rather than behaviorally relevant code.

### Step 4: choose the first consequence-bearing consumer
Among the delivered handlers, prefer the one that:
- writes durable or semi-durable state
- selects the next action family
- schedules specific follow-on work
- changes object ownership or lifecycle
- produces a visible output family

Do not choose the most central-looking framework callback if a smaller downstream consumer better predicts behavior.

### Step 5: prove it with one narrow runtime move
Typical minimal proofs include:
- breakpoint or log on one queue-pop or dispatch-selection helper
- watchpoint on one state field written by the chosen consumer
- compare run that toggles one triggering event or input condition
- hook on one follow-up task enqueue or visible emitter
- reverse-causality or record/replay step from a late visible effect back to one consumer

The aim is **not** maximal event tracing.
It is one proof that:
- this event family is real
- this dispatch path is the relevant one
- this consumer changes later behavior

### Step 6: rewrite the subsystem map after proof
Once proved, rewrite the working model as:

```text
event source -> registration family -> dispatch reduction -> consequence-bearing consumer -> effect
```

Only after that should you broaden into neighboring callbacks, sibling message types, or adjacent event families.

## 6. Common scenario patterns

### Pattern 1: GUI or window-message subsystem
Symptoms:
- many handlers or message-map entries are visible
- window procedures and wrapper helpers are readable
- static reading still does not reveal which event path changes mode or state first

Best move:
- choose one message family
- find the first reducer from generic message pump to one handler
- prove one state write or UI/service effect from that handler

### Pattern 2: Reactor or async I/O service
Symptoms:
- socket/event-loop plumbing is obvious
- many callbacks appear symmetrical
- registration sites are visible but later ownership is unclear

Best move:
- separate registration from readiness delivery
- localize one queue/dequeue or ready-list reduction
- prove one consumer that selects reply, session state, or downstream task family

### Pattern 3: Completion-based worker pipeline
Symptoms:
- thread pool, futures/promises, or completion callbacks are visible
- the direct caller chain breaks at posted work boundaries
- several continuations look plausible

Best move:
- choose one posted task or completion family
- prove the first continuation that mutates durable state or schedules the next meaningful stage
- ignore sibling continuations until one chain is grounded

### Pattern 4: Observer/signal-slot style notification graph
Symptoms:
- notifications are easy to find
- many subscribers receive the same event family
- static reading does not show which subscriber really changes behavior

Best move:
- treat emission as only the source boundary
- localize the first subscriber that changes policy, ownership, mode, or later output
- prove one downstream consequence from that subscriber rather than cataloging the whole observer graph

## 7. What this note adds to the native branch
The native branch now has a more realistic ordered progression:
- `topics/native-practical-subtree-guide.md` first when the case is clearly native-shaped but the current bottleneck still needs branch-level routing
- `topics/native-semantic-anchor-stabilization-workflow-note.md` first when code is readable but meanings are still too slippery
- `topics/native-interface-to-state-proof-workflow-note.md` second when several interface routes exist and one representative proof chain is needed
- `topics/native-plugin-loader-to-first-real-module-consumer-workflow-note.md` third when plugin/module loader structure is visible but the real loaded-module owner is still unclear
- `topics/native-callback-registration-to-event-loop-consumer-workflow-note.md` fourth when one route or loaded-module owner is already plausible but async registration/dispatch structure still hides the first consequence-bearing consumer

This page is therefore usually a **continuation note**, not the default first native practical stop.
Use it after semantic-anchor, interface-path, and when relevant loaded-module-owner work are solved enough that the remaining ambiguity really lives at queue, callback, completion, or event-loop boundaries.

## 8. Failure modes this note helps prevent
- treating registration sites as if they already prove ownership
- cataloging the whole event framework before proving one behavior-changing consumer
- over-tracing every callback instead of choosing one consequence target
- confusing event visibility with meaningful consumption
- stopping at framework dispatch helpers instead of the first consumer that changes behavior
- broadening to sibling handlers before one async chain is grounded

## 9. Compact operator checklist
- Pick one event family, not the whole framework.
- Separate source, registration, dispatch, consumer, and effect.
- Prefer the first consequence-bearing consumer over the prettiest dispatch helper.
- Use one narrow runtime proof, not maximal tracing.
- Rewrite the subsystem map only after one async chain is proved.

## 10. Topic summary
In native baseline reversing, async and callback-heavy targets often stall not because nothing is visible, but because visible registration and dispatch structure still do not reveal ownership.

The practical cure is to separate registration from delivery, choose one candidate callback or loop-consumer chain, localize the first consequence-bearing consumer, and prove one downstream effect.
That single proof usually turns a confusing event framework into a smaller, trustworthy working map.
