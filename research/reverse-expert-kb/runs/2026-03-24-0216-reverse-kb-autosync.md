# Reverse KB autosync run — 2026-03-24 02:16 Asia/Shanghai

Mode: external-research-driven

## Scope this run
Performed a real external-research-driven maintenance pass on the native practical branch, explicitly avoiding another browser/mobile/protected dense-branch polish run.

This run targeted a thinner but practical seam:
- `topics/native-completion-port-and-thread-pool-first-consumer-workflow-note.md`

Goal:
- materially improve the KB itself, not just collect notes
- sharpen the native completion/thread-pool continuation with source-backed operator guidance around IOCP dequeue ownership and libuv worker→loop callback ownership
- preserve provenance in a dedicated source note and search trace

## Direction / branch-balance review
Current branch picture still favors avoiding overfeeding browser/mobile/protected subtrees.

Strong / easy-to-overfeed branches remain:
- browser anti-bot / captcha / request-signature workflows
- mobile protected-runtime / WebView / challenge-loop workflows
- protected-runtime practical reduction ladders

Now materially established and worth maintaining carefully:
- native practical workflows
- protocol / firmware practical workflows
- malware practical workflows
- iOS practical workflows

Why this branch was chosen:
- recent runs already gave real external passes to protected-runtime, protocol/firmware, and iOS
- native remains valuable as the default comparison branch for the KB but still benefits from practical deepening
- the completion/thread-pool note was a good underfed seam: specific enough for concrete improvement, but not yet so dense that another pass would be redundant

Balance judgment for this run:
- good use of an external-research slot in the rolling window
- avoided another internal-only canonical-sync pass
- produced a source-backed practical continuation page improvement rather than mere wording/index repair

## New findings
1. **IOCP dequeue truth has two separate ownership carriers**
   - `lpCompletionKey` often identifies handle family / queue family
   - `lpOverlapped` often leads back to the concrete request/session owner
   - this distinction is worth making explicit in the KB because it changes where the analyst should anchor proof

2. **IOCP ordering should not be overread from submit chronology**
   - Microsoft documents FIFO packet queueing but LIFO release of waiting threads plus concurrency-governed runnable worker limits
   - therefore the practical proof object is usually an owner identity chain, not naive chronological order

3. **Posted control packets must be separated from true I/O completions**
   - `PostQueuedCompletionStatus` means some dequeued packets are application-defined control-plane work, not real overlapped-I/O completion
   - queue traces can therefore mislead unless the packet family is classified first

4. **`GetQueuedCompletionStatus` failure can still carry a real dequeued failed-I/O packet**
   - FALSE + non-NULL `lpOverlapped` is a real failed completion, often important for retry/backoff/teardown ownership

5. **libuv exposes a concrete two-stage ownership split**
   - `work_cb` executes on a worker thread
   - completion is then routed back through `uv__work_done()` / `uv__queue_done()` into `after_work_cb` on the loop thread
   - for many practical reversing targets, the loop-thread `after_work_cb` is the real consequence-bearing consumer, not the worker-side function alone

6. **Cancellation / no-effect diagnosis in libuv-like systems often belongs in the loop-thread completion path**
   - useful for cases where the symptom is absence of later behavior rather than the work item never existing

## Sources consulted
- Microsoft Learn: I/O Completion Ports
  - https://learn.microsoft.com/en-us/windows/win32/fileio/i-o-completion-ports
- Microsoft Learn: `GetQueuedCompletionStatus`
  - https://learn.microsoft.com/en-us/windows/win32/api/ioapiset/nf-ioapiset-getqueuedcompletionstatus
- Microsoft Learn: thread-pool overview page requested during run, but the specific URL used returned 404 via `web_fetch`
- libuv guide: Threads / libuv work queue
  - https://docs.libuv.org/en/v1.x/guide/threads.html
- libuv source: `src/threadpool.c`
  - https://github.com/libuv/libuv/raw/refs/heads/v1.x/src/threadpool.c
- Search trace:
  - `sources/native-binary/2026-03-24-native-completion-threadpool-search-layer.txt`

## Reflections / synthesis
This run usefully tightened the KB’s native async branch in a way that is practical rather than taxonomic.

Before this run, the native completion/thread-pool note already had the right broad workflow shape, but it was still missing three source-backed practical reminders that matter in real work:
- IOCP dequeue-time ownership is often split between family identity (`completion key`) and concrete owner recovery (`OVERLAPPED*`)
- IOCP worker loops can mix posted control packets with true I/O completions
- libuv worker-thread completion is not necessarily the same thing as the first loop-thread consequence owner

These additions improve the branch because they help analysts avoid stopping at queue plumbing, helper wrappers, or worker-side computation when the first trustworthy behavior claim actually appears one layer later.

## Candidate topic pages to create or improve
Most immediate follow-ups:
- further improve `topics/native-completion-port-and-thread-pool-first-consumer-workflow-note.md` if more concrete Windows service/IOCP case material accumulates
- potentially add a narrower Windows service+IOCP/session-owner continuation only if several real cases justify it
- consider cross-linking runtime compare-run guidance to completion-order skepticism in multi-worker cases

Not recommended immediately:
- another top-level native index pass without new practical evidence
- another browser/mobile micro-variant expansion unless a branch gap is truly blocking

## Next-step research directions
- native Windows service + IOCP session ownership and failed-I/O policy branches
- native queue families where control packets, retry timers, and I/O completions share one worker loop
- additional event-loop frameworks where worker-side completion and consequence-bearing callback ownership split similarly to libuv
- branch-balance check next run should continue favoring thinner practical seams over already-dense browser/mobile leaves

## Concrete scenario notes or actionable tactics added this run
Added or strengthened the following operator guidance:
- for IOCP, distinguish dequeue-time family identity from concrete owner recovery
- do not infer ownership from packet chronology alone on multi-worker completion ports
- separate posted control packets from true I/O completions before tracing callback consequences
- treat FALSE `GetQueuedCompletionStatus` with non-NULL `lpOverlapped` as a potentially meaningful failed-I/O consumer path
- in libuv-like systems, jump quickly to loop-thread `after_work_cb` / completion delivery when the visible effect happens after worker computation
- inspect loop-thread cancellation/error delivery when the symptom is missing later behavior

## Files changed
- `topics/native-completion-port-and-thread-pool-first-consumer-workflow-note.md`
- `sources/native-binary/2026-03-24-native-completion-threadpool-notes.md`
- `sources/native-binary/2026-03-24-native-completion-threadpool-search-layer.txt`
- `runs/2026-03-24-0216-reverse-kb-autosync.md`

## Search audit
- Search sources requested: `exa,tavily,grok`
- Search sources succeeded: `exa,tavily,grok`
- Search sources failed: `none`
- Exa endpoint: `http://158.178.236.241:7860`
- Tavily endpoint: `http://proxy.zhangxuemin.work:9874/api`
- Grok endpoint: `http://proxy.zhangxuemin.work:8000/v1`

Notes:
- This run attempted explicit multi-source search as required.
- A later `web_fetch` on one Microsoft thread-pool overview URL returned 404, but that did not invalidate the search-layer pass or the other fetched sources.

## Commit / sync status
Pending at report write time.
