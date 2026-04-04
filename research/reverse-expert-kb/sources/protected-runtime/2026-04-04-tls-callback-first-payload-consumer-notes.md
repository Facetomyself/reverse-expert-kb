# 2026-04-04 TLS callback -> first payload consumer notes

Date: 2026-04-04 13:21 Asia/Shanghai / 2026-04-04 05:21 UTC
Theme: keep TLS callback presence and replay separate from the first payload-bearing consumer.

## Why this note was retained
The broad packed-startup note already preserved the important stop rule that raw entry, startup-owned pre-entry truth, unpack transfer, and payload-bearing handoff can all be different objects.

What was still missing was a thinner continuation page for the specific Windows/native case where the remaining uncertainty is already clearly **TLS-callback-shaped**.

## Primary retained anchors
### 1. PE format / .tls / callback routines
Source:
- Microsoft Learn — PE Format
  - https://learn.microsoft.com/en-us/windows/win32/debug/pe-format

Retained points:
- PE images can contain a `.tls` section with initialization data
- PE/TLS support includes callback routines for per-thread initialization and termination
- the TLS directory includes callback-array style information (`AddressOfCallbacks` concept)

Operator consequence:
- static TLS presence is a real startup surface, but weaker than replay truth for one callback in one run

### 2. Visual Studio `/TLS`
Source:
- Microsoft Learn — `/TLS`
  - https://learn.microsoft.com/en-us/cpp/build/reference/tls?view=msvc-170

Retained points:
- tooling can display the fields of the TLS structure and the addresses of TLS callback functions
- if a program does not use TLS, the image will not contain a TLS structure

Operator consequence:
- callback-array inventory is useful, but still only structure truth

### 3. PE format detail / startup interpretation
Source:
- MSDN Magazine archive — Inside Windows: An In-Depth Look into the Win32 Portable Executable File Format, Part 2
  - https://learn.microsoft.com/en-us/archive/msdn-magazine/2002/march/inside-windows-an-in-depth-look-into-the-win32-portable-executable-file-format-part-2

Retained use:
- historical practical context for how PE/TLS startup structures are interpreted during startup analysis
- used conservatively as supporting startup-reading context, not as the sole basis for claims about modern loader behavior

## Search-layer trace
See:
- `sources/protected-runtime/2026-04-04-1321-tls-callback-search-layer.txt`

Observed degraded mode:
- Exa: returned results
- Tavily: returned results
- Grok: invoked but returned empty set
