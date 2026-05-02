# Source Notes — Windows Named Pipe Impersonation to Handler Consumer

Date: 2026-05-03 04:50 Asia/Shanghai
Search artifact: `sources/native/2026-05-03-0450-windows-named-pipe-impersonation-search-layer.txt`

## Source set

- Microsoft Learn, `ImpersonateNamedPipeClient` — https://learn.microsoft.com/en-us/windows/win32/api/namedpipeapi/nf-namedpipeapi-impersonatenamedpipeclient
- Microsoft Learn, `Impersonating a Named Pipe Client` — https://learn.microsoft.com/en-us/windows/win32/ipc/impersonating-a-named-pipe-client
- Microsoft Learn, `Named Pipe Server Using Overlapped I/O` — https://learn.microsoft.com/en-us/windows/win32/ipc/named-pipe-server-using-overlapped-i-o
- Microsoft Learn, `Named Pipe Security and Access Rights` — https://learn.microsoft.com/en-us/windows/win32/ipc/named-pipe-security-and-access-rights
- Microsoft Learn, `GetNamedPipeClientProcessId` — https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-getnamedpipeclientprocessid
- Google Project Zero, James Forshaw, `Windows Exploitation Tricks: Spoofing Named Pipe Client PID` — https://projectzero.google/2019/09/windows-exploitation-tricks-spoofing.html
- SpecterOps, `Exploring Impersonation through Named Pipe` — https://specterops.io/blog/2023/05/03/exploring-impersonation-through-the-named-pipe-filesystem-driver/

## Durable facts to preserve

### Named-pipe impersonation is message/thread scoped, not generic service truth

Microsoft documents `ImpersonateNamedPipeClient` as a server-end operation that changes the calling thread to impersonate the security context of the **last message read from the pipe**. The server should call `RevertToSelf` when done. Microsoft explicitly warns that failure must be checked: if impersonation fails, subsequent work remains in the server process security context, which is dangerous when that process is privileged.

Operator implication:
- a static call to `ImpersonateNamedPipeClient` is not enough
- prove the server pipe instance, the last read message, return-value branch, thread token, and `RevertToSelf` lifetime before attributing later file/registry/process access to the client identity

### Client SQOS and impersonation level decide what the server can actually do

Microsoft's concept page notes that impersonation level determines server capability while impersonating, and that clients can use `SECURITY_SQOS_PRESENT` when opening the client end to control the server's impersonation level.

Operator implication:
- token presence is not enough; freeze effective impersonation level
- `SecurityIdentification`-like evidence may support identity checks but not downstream privileged access on behalf of the client

### Pipe security descriptors gate who can connect or create instances

Microsoft's named-pipe security page states that a security descriptor can be supplied to `CreateNamedPipe`, controls access to both ends, and that `NULL` default DACLs grant full control to LocalSystem, administrators, creator owner, and read access to Everyone / anonymous. It also notes access checks for server-instance creation and client connections.

Operator implication:
- pipe name visibility is not connection proof
- DACL, remote-client flags, first-instance behavior, and actual client connection should be frozen before assuming a pipe path represents a live trust boundary

### Overlapped pipe servers split connect/read/write completion from handler truth

Microsoft's overlapped-I/O server example uses multiple pipe instances, each with state for connecting, reading, and writing. The documentation calls out that overlapped operations can complete immediately or later, and the server uses `GetOverlappedResult` plus state to decide the next operation.

Operator implication:
- a `ReadFile`/`ConnectNamedPipe` callsite is often only setup/progress truth
- the proof object is the completed operation associated with the correct pipe instance and state transition, not merely a pending `OVERLAPPED` structure

### PID/client-attribute checks are not durable identity proof by themselves

Project Zero documents that `GetNamedPipeClientProcessId` returns connection attributes set by the named pipe file-system driver, and analyzes historical spoofing routes around named-pipe client PID assumptions. The practical lesson is narrower than the exploit: treating client PID as a strong security identity is risky.

Operator implication:
- PID-based allow/deny branches should be treated as weak identity proof until cross-checked with token/SID/session/image evidence and the actual accepted pipe instance
- do not collapse `client PID observed` into `trusted client owned this request`

### Offensive writeups confirm the same boundary from the other side

SpecterOps and offensive tradecraft material frame named-pipe impersonation around a server thread impersonating the pipe client and then using/duplicating the resulting token. For KB purposes, the useful defensive/reversing lesson is not an exploit recipe; it is that connection forcing, pipe-server ownership, impersonation privilege, token capture, duplication, and later effect are separate objects.

Operator implication:
- when analyzing malware or service abuse, separate **pipe server created**, **privileged client connected**, **impersonation succeeded**, **token object captured/duplicated**, and **effect launched/performed**
- when analyzing benign services, separate **client connected**, **request read**, **server impersonated**, **authorization or resource access happened under that token**, and **server reverted**

## Practical ladder

```text
pipe name / instance visible
  != current client connection accepted
  != correct request bytes read on this pipe instance
  != client identity/token/impersonation level frozen
  != ImpersonateNamedPipeClient succeeded for the last read message
  != operation executed while impersonation lifetime was active
  != handler-owned state/effect proved
```

Compact branch memory:

```text
pipe != connected != read != impersonated != in-lifetime operation != consumed/effected
```

## Best immediate KB fit

Add a native workflow note for Windows named-pipe service/client-impersonation consumer proof. It should live next to:

- `native-service-dispatcher-to-worker-owned-consumer-workflow-note.md`
- `native-unix-domain-socket-fd-credential-first-consumer-workflow-note.md`
- `native-completion-port-and-thread-pool-first-consumer-workflow-note.md`
- `malware-service-servicemain-consumer-proof-workflow-note.md`
- `malware-wmi-*` / persistence proof notes when abuse rather than benign service routing is the question
