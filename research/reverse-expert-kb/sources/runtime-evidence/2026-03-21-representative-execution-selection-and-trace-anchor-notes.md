# Representative execution selection and trace-anchor triage notes

Date: 2026-03-21
Topic: runtime evidence / record-replay / omniscient debugging
Purpose: source-backed practical notes for deciding which execution window to record and where to anchor first triage inside a replayable trace

## Why this note exists
The runtime-evidence branch already had broad material on record/replay and reverse-causality, but it was lighter on a practical question analysts hit early:

- when record/replay looks attractive, which execution should you actually capture?
- once you have a trace, where should first triage begin so the replay pays off instead of becoming another huge archive?

The sources below converge on the same operational rule:
- bound the recording around one representative effect or effect family
- prefer one trustworthy anchor family for first triage
- treat capture strategy as part of analysis design, not just a tooling choice

## Sources consulted

### Microsoft Learn — Time Travel Debugging Overview
URL:
- https://learn.microsoft.com/en-us/windows-hardware/drivers/debuggercmds/time-travel-debugging-overview

Useful signals:
- TTD traces can become very large quickly; recording only as much execution as needed is explicitly encouraged.
- `.run` and `.idx` files form a replay substrate, with indexing as a separate practical cost.
- TTD is framed as most useful when the path to failure matters more than the final state alone.
- Timelines and queryable events matter because raw possession of a trace is not enough.

Practical extraction:
- trace-size pressure is not a storage footnote; it should shape the analyst’s capture window
- the first question is often not “can I record?” but “what is the shortest representative execution that still contains the decisive effect?”

### Google Cloud / Mandiant blog — .NET hollowing case study with TTD
URL:
- https://cloud.google.com/blog/topics/threat-intelligence/time-travel-debugging-using-net-process-hollowing

Useful signals:
- the case study does not start with broad trace wandering; it starts by choosing a behavioral family (process hollowing) and then searching around process creation plus remote-memory-write APIs.
- the article explicitly recommends adapting searches to the API family relevant to the target technique.
- TTD is presented as valuable because it allows analysts to jump directly to key execution events instead of redoing setup.

Practical extraction:
- first triage should anchor on one effect family, not the whole execution narrative
- good anchors are often effect-adjacent APIs, writes, module loads, exceptions, child-process events, or state transitions already suggested by prior evidence
- replay becomes efficient when the initial query/anchor is narrow enough to partition the trace

### Binary Ninja docs — rr-backed Linux time-travel debugging
URL:
- https://docs.binary.ninja/guide/debugger/gdbrsp-ttd.html

Useful signals:
- rr replay is exposed through familiar reverse-debugger workflows rather than a separate analysis world.
- practical setup assumes one recorded trace per target run and then debugging within that trace.

Practical extraction:
- on Linux/rr-style workflows, the practical unit is still “one chosen recorded run” rather than generic omniscience over everything
- this reinforces the need to decide which run deserves preservation before deep analysis starts

### PANDA manual
URL:
- https://github.com/panda-re/panda/blob/dev/panda/docs/manual.md

Useful signals:
- PANDA documentation explicitly describes the most effective workflow as collecting a recording of a piece of execution of interest and then analyzing it repeatedly.
- record/replay is tied to plugins and targeted analyses, not blind full-history browsing.

Practical extraction:
- “piece of execution of interest” is the key phrase: execution capture should be scoped around one bounded question
- whole-system replay still benefits from selecting one narrow region-of-interest before custom analysis begins

## Lower-confidence / partial-use signals

### O’Callahan rr paper URL via USENIX fetch
URL:
- https://www.usenix.org/system/files/conference/atc17/atc17-o_callahan.pdf

Status:
- direct fetch returned raw PDF bytes rather than usable extracted text in this environment

Usefulness:
- confirms the paper endpoint exists, but not used as a quote-bearing source in this note

### MIT LL / omniscient debugging PDF landing
URL:
- https://www.ll.mit.edu/media/6101

Status:
- redirected to PDF; extraction degraded to raw bytes in this environment

Usefulness:
- not used as a quote-bearing source in this note

## Working synthesis
A practical replay workflow usually benefits from separating two design choices that are easy to blur together:

1. **execution selection**
   - choose the smallest execution window that still contains a representative version of the effect you care about
2. **anchor selection**
   - choose the first stable event family that partitions the trace into a tractable search space

This matters because “record everything and inspect later” often fails twice:
- recording cost and index cost grow unnecessarily
- first triage has no obvious anchor, so the trace becomes another large evidence dump

## Candidate anchor families
Useful first-triage anchors often include:
- first child-process creation relevant to the case
- first remote-memory-write or suspicious allocation family
- module load for the component likely to own the consequence
- exception family or error path near a failure effect
- first decrypted-buffer consumer when decryption is already known
- request-finalization or send boundary when one network effect is the target
- callback or queue-consumer edge when the effect is asynchronous
- one late state write or enum/policy reduction when a visible verdict/result already exists

## Operational rule for the KB
The runtime-evidence branch should preserve this practical distinction:
- broad replay/tooling pages explain why execution history helps
- a narrower workflow note should tell the analyst how to choose one representative execution and one anchor family before broad reverse-causality work starts

That narrower note is what this source pass supports.
