# Native waitable timer / registered-wait notes

Date: 2026-04-07 10:21 Asia/Shanghai / 2026-04-07 02:21 UTC
Mode: external-research-driven
Branch: native practical workflows -> wait object / threadpool wait / waitable timer delivery

## Why this branch
This run used the external slot on a thinner native practical seam rather than returning to browser or malware.

The practical question was not broad Windows synchronization taxonomy.
It was how to preserve a more operational split between:
- object armed/registered truth
- signaled or timer-fired truth
- registered-wait / threadpool-wait / APC callback delivery truth
- later consequence-bearing consumer truth

That seam already existed partly across the native wait and timer notes, but the branch still benefited from a sharper operator-facing split grounded in docs.

## Search-layer observations
Explicit multi-source search was attempted with:
- `--source exa,tavily,grok`

Queries used:
1. `CreateWaitableTimer SetWaitableTimer RegisterWaitForSingleObject SetThreadpoolWait official docs callback race cancellation Windows`
2. `Windows waitable timer register wait threadpool wait official docs callback delivery cancellation`
3. `SetWaitableTimer APC completion routine waitable timer vs wait object official docs Windows`

Observed source behavior:
- Exa returned usable hits
- Tavily returned usable hits
- Grok was invoked on all queries but failed with repeated 502 errors through the configured proxy/completions endpoint

## Primary source anchors
### Waitable timer objects / using waitable timer objects
URLs:
- https://learn.microsoft.com/en-us/windows/win32/sync/waitable-timer-objects
- https://learn.microsoft.com/en-us/windows/win32/sync/using-waitable-timer-objects

Useful operator implications:
- timer object creation/arming is distinct from later signaled/fired truth
- APC completion routine delivery depends on alertable-wait semantics and should not be flattened into ordinary object-signaled truth
- timer signal visibility is still weaker than the later callback/consumer that gives it behavioral meaning

### RegisterWaitForSingleObject
URL:
- https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-registerwaitforsingleobject

Useful operator implications:
- wait registration is distinct from callback delivery
- registration/cancellation races matter for truthful callback claims
- object signal truth is still weaker than actual registered-wait callback truth

### SetThreadpoolWait
URL:
- https://learn.microsoft.com/en-us/windows/win32/api/threadpoolapiset/nf-threadpoolapiset-setthreadpoolwait

Useful operator implications:
- threadpool-wait association is distinct from callback delivery
- waiter association and later callback dispatch are different proof objects
- later consequence should still not be collapsed into raw wait association truth

## Practical synthesis to preserve canonically
Useful ladder:

```text
armed / registered
  != object signaled or timer fired
  != APC / registered-wait / threadpool-wait callback delivered
  != later consequence-bearing consumer
```

Specific operator-facing reminders:
- waitable timer armed truth is weaker than actual timer-fire truth
- timer-fire/object-signal truth is weaker than APC or registered-wait callback delivery truth
- registered-wait or threadpool-wait registration is weaker than actual callback delivery truth
- callback delivery is still weaker than one later consumer or effect that answers the analyst’s real question

## Why this mattered to the KB
The native branch already had wait-object and timer continuations, but the shared branch memory around waitable timers, registered waits, threadpool waits, and APC-style completion was still easy to flatten.

This run sharpened the practical operator split so future native async work does not silently overread registration, signal, or timer-fire visibility as already-good callback/consumer truth.

## Candidate follow-ons
Possible later native continuations if needed:
- a narrower APC-vs-registered-wait compare continuation when queueing/delivery realism still lies after wait/timer truth is already good enough
- a parent-page sync only if the new waitable-timer/registered-wait memory still feels too leaf-local
