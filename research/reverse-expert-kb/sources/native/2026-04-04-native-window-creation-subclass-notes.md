# 2026-04-04 native window creation / subclass first-consumer notes

Date: 2026-04-04 19:21 Asia/Shanghai / 2026-04-04 11:21 UTC
Theme: keep class registration, instance creation, subclass-chain ownership, and first instance-local consumer truth separate.

## Why this note was retained
The native practical branch already had:
- broad callback/event-loop reduction
- GUI message-pump continuation
- IOCP/timer/APC/wait-object continuations

What it still lacked was the thinner Win32 GUI creation/subclass continuation for cases where one window class and one creation path are already visible but the remaining ambiguity is which HWND-local procedure/subclass owner first changes behavior.

## Primary doc-backed anchors
### 1. CreateWindowEx
Source:
- Microsoft Learn — CreateWindowExA function
  - https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-createwindowexa

Retained points:
- sends `WM_NCCREATE`, `WM_NCCALCSIZE`, and `WM_CREATE` to the window being created before returning
- creates one concrete window instance (HWND), not just class metadata

Operator consequence:
- class-registration truth is weaker than one proved instance-creation path
- create-time message flow is a real ownership boundary

### 2. WM_NCCREATE / WM_CREATE
Sources:
- Microsoft Learn — WM_NCCREATE
  - https://learn.microsoft.com/en-us/windows/win32/winmsg/wm-nccreate
- Microsoft Learn — WM_CREATE
  - https://learn.microsoft.com/en-us/windows/win32/winmsg/wm-create

Retained points:
- `WM_NCCREATE` is sent before `WM_CREATE`
- creation data flows through `CREATESTRUCT` / creation parameters at this stage
- returning failure from create-time handlers affects whether creation succeeds

Operator consequence:
- create-time message handling can own important per-instance state before later ordinary GUI traffic exists

### 3. SetWindowSubclass / DefSubclassProc
Sources:
- Microsoft Learn — SetWindowSubclass
  - https://learn.microsoft.com/en-us/windows/win32/api/commctrl/nf-commctrl-setwindowsubclass
- Microsoft Learn — DefSubclassProc
  - https://learn.microsoft.com/en-us/windows/win32/api/commctrl/nf-commctrl-defsubclassproc

Retained points:
- subclass callbacks are identified by callback pointer + ID pair and can hold reference data
- `DefSubclassProc` passes processing to the next handler in the subclass chain and eventually the original WndProc
- helper-based subclassing cannot be used across threads

Operator consequence:
- the visible class WndProc can be weaker than the real active per-HWND subclass chain
- subclass installation truth is weaker than first consequence-bearing callback truth

## Search-layer trace
See:
- `sources/native/2026-04-04-1921-native-window-subclass-search-layer.txt`

Observed degraded mode:
- Exa: returned results
- Tavily: returned results
- Grok: invoked but returned empty set
