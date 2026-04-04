# Native Window Creation and Subclass First-Consumer Workflow Note

Topic class: workflow note
Ontology layers: workflow/sensemaking, runtime-evidence bridge, native baseline practical branch
Maturity: emerging
Related pages:
- topics/native-practical-subtree-guide.md
- topics/native-callback-registration-to-event-loop-consumer-workflow-note.md
- topics/native-gui-message-pump-to-consumer-workflow-note.md
- topics/runtime-behavior-recovery.md
Related source notes:
- sources/native/2026-04-04-native-window-creation-subclass-notes.md

## 1. What this workflow note is for
This note covers a recurring Win32-native GUI case where the analyst has already reduced the target into a window-creation path, but the remaining uncertainty is narrower than the broad callback/event-loop note and narrower than generic GUI message-pump tracing.

Typical symptoms:
- `RegisterClassEx*`, `CreateWindowEx*`, `WM_NCCREATE`, `WM_CREATE`, `SetWindowSubclass`, or `SetWindowLongPtr(...GWLP_WNDPROC...)` style ownership is visible
- the analyst keeps stopping at class registration or at the first visible window procedure rather than proving which per-instance callback/subclass chain first changes behavior
- one GUI path appears to “own” later behavior, but it is unclear whether the real owner is class-wide registration, instance creation, subclass installation, or one first instance-local consumer

The goal is to move from:

```text
one visible window class / WndProc / subclass hook family
```

to:

```text
one proved chain from class registration or instance creation
into one actual HWND-local procedure/subclass owner
into one first behavior-changing consumer
and one downstream effect
```

## 2. When to use this note
Use this note when most of the following are true:
- the target is native Windows GUI-heavy enough that Win32 window creation is already a plausible pivot
- broad callback/event-loop ownership is no longer the main bottleneck
- the remaining uncertainty is about per-window instance ownership, subclass layering, or first consumer truth after creation
- one narrow runtime proof against one HWND / one subclass path would collapse a lot of uncertainty

Common shapes include:
- `RegisterClassEx*` + `CreateWindowEx*` setup where later behavior is suspected to begin before normal user interaction
- control or helper window creation followed by immediate subclass installation
- GUI-heavy protectors or launchers that use hidden/utility windows and subclass chains
- mixed GUI/native apps where a later message consumer is easy to confuse with class registration or default processing

Do **not** use this as the primary note when:
- the broad async path is still unclear and generic callback registration is the better first stop
- the main uncertainty is ordinary message-pump routing after ownership is already clear
- the case is really about non-GUI waits/timers/APCs instead of window instance creation/subclass ownership

## 3. Core claim
In Win32 GUI ownership work, **class registration is weaker than instance creation truth**, instance creation is weaker than proving the actual WndProc/subclass chain that owns the instance, and that is weaker than proving the first instance-local consumer that changes behavior.

The wrong question is often:

```text
Where is RegisterClassEx / CreateWindowEx called?
```

The better question is:

```text
Which HWND-local procedure or subclass chain actually owns this instance,
and which first instance-local consumer changes later behavior?
```

## 4. Boundary objects to mark explicitly
### A. Class-registration truth
This is where the target defines a window class and one nominal window procedure.

What to capture here:
- class name / atom
- registered WndProc pointer
- one registration site

This is weaker than proving the instance that matters.

### B. Instance-creation truth
From Microsoft docs:
- `CreateWindowEx` sends `WM_NCCREATE`, `WM_NCCALCSIZE`, and `WM_CREATE` to the window being created before returning

What to capture here:
- one concrete HWND
- creation parameters / lpParam if visible
- one creation-time message sequence

### C. Subclass-ownership truth
Subclassing or WndProc replacement can make the class-registered WndProc weaker than the real consumer chain.

From Microsoft docs:
- `SetWindowSubclass` installs a subclass callback associated with a `(callback pointer, ID)` pair and reference data
- `DefSubclassProc` calls the next handler in the subclass chain and eventually the original window procedure
- the helper-based subclass APIs cannot subclass across threads

What to capture here:
- one subclass installation site
- one callback pointer + ID + refdata tuple
- one relation between subclass chain and original WndProc

### D. First behavior-changing consumer truth
This is the first instance-local callback or immediate downstream consumer that changes later behavior.
Typical anchors include:
- one state write during `WM_NCCREATE` / `WM_CREATE`
- one subclass callback that captures instance data
- one deferred post-create message consumer that becomes the real owner

### E. Proof-of-effect truth
This is where the analyst proves the chosen instance-local consumer matters.

## 5. Default workflow
### Step 1: choose one HWND family, not all window classes
Do not start by cataloging every registered class.
Pick one instance with:
- the clearest downstream effect
- one stable creation path
- one plausible subclass or WndProc owner

### Step 2: separate class registration from instance ownership
Write the local chain explicitly:
- class registration
- instance creation
- create-time message flow (`WM_NCCREATE` / `WM_CREATE`)
- subclass/WndProc ownership
- first consequence-bearing consumer
- effect

This prevents the classic mistake of treating registration as if it already explains behavior.

### Step 3: freeze the create-time message boundary
From Microsoft docs:
- `WM_NCCREATE` is sent prior to `WM_CREATE`
- `CreateWindowEx` returns only after the create-time message sequence has occurred

Practical stop rules:
- do not overread a class registration site as if it already owned one concrete HWND
- do not overread `CreateWindowEx` as if the original registered WndProc necessarily remains the active per-instance owner

### Step 4: preserve subclass-chain truth
If subclass helpers or WndProc replacement are present:
- prove which callback is in the active chain for the HWND you care about
- preserve the order: subclass callback -> next subclass -> original WndProc
- do not flatten `DefSubclassProc` use into proof that the visible callback is the first consequence-bearing owner

### Step 5: prove one instance-local consumer
Among candidate handlers, prefer the one that:
- consumes creation data or instance state
- predicts later behavior better than registration alone
- distinguishes class-wide structure from one per-window ownership path

### Step 6: use one narrow runtime move
Typical minimal proofs include:
- breakpoint/log on the `WM_NCCREATE` / `WM_CREATE` path plus the first instance data write
- breakpoint on `SetWindowSubclass` plus the first callback using its refdata
- compare one HWND that receives subclass installation versus another that does not, while observing one later effect

The aim is not full GUI tracing.
It is one proof that links class/instance setup to a behavior-changing per-instance consumer.

## 6. Practical stop rules this note preserves
- `registered class exists != one concrete HWND owner is proved`
- `CreateWindowEx reached != class-registered WndProc remains the real instance owner`
- `subclass installed != first behavior-changing consumer is known`
- `DefSubclassProc in chain != the current callback is the behavior-changing owner`

## 7. Sources
See: `sources/native/2026-04-04-native-window-creation-subclass-notes.md`

Primary references:
- https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-createwindowexa
- https://learn.microsoft.com/en-us/windows/win32/winmsg/wm-nccreate
- https://learn.microsoft.com/en-us/windows/win32/winmsg/wm-create
- https://learn.microsoft.com/en-us/windows/win32/api/commctrl/nf-commctrl-setwindowsubclass
- https://learn.microsoft.com/en-us/windows/win32/api/commctrl/nf-commctrl-defsubclassproc
