# Source notes — Windows COM activation to method consumer proof (2026-05-19)

Scope: source-backed notes for a native Windows practical workflow seam where COM registration, activation, class factory resolution, object creation, interface acquisition, and first method-owned effect must remain separate proof objects.

## Search trace

Search artifact:
- `sources/native/2026-05-19-0450-com-activation-consumer-search-layer.json`

Search command used:

```bash
python3 /root/.openclaw/workspace/skills/search-layer/scripts/search.py \
  --queries \
    "Windows COM local server activation class factory reverse engineering CoCreateInstance DCOM registration" \
    "Microsoft COM activation registry class factory CoGetClassObject IClassFactory documentation" \
    "COM server reverse engineering CLSID AppID LocalServer32 class factory method invocation" \
  --mode deep \
  --intent exploratory \
  --num 5 \
  --source exa,tavily,grok
```

The search returned useful Microsoft Learn / Open Specifications material from Exa and Tavily. Grok was invoked but returned HTTP 502 Bad Gateway for all three query attempts.

## Source-backed facts useful to the workflow

### Registration is only location / launch metadata

Microsoft's COM registration documentation says that, after a COM class implements `IClassFactory` or `IClassFactory2` and has a CLSID, registry information lets COM create instances by telling the system where the DLL or EXE code is located and how it should be launched.

Source:
- Microsoft Learn, "Registering COM Servers" — https://learn.microsoft.com/en-us/windows/win32/com/registering-com-servers

Reverse-engineering implication:
- a CLSID / ProgID / `InprocServer32` / `LocalServer32` / AppID artifact is registration truth, not activation truth
- it can identify plausible code and launch posture, but it does not prove this client, this process instance, or this method invocation used it

### CLSID lookup and class objects are a separate boundary from object behavior

Microsoft's "COM Class Objects and CLSIDs" page separates the CLSID database / registry mapping from class objects. It describes a class object as an intermediate object that supports functions common to creating instances, usually via `IClassFactory::CreateInstance`.

Source:
- Microsoft Learn, "COM Class Objects and CLSIDs" — https://learn.microsoft.com/en-us/windows/win32/com/com-class-objects-and-clsids

Reverse-engineering implication:
- a recovered CLSID or interface family is not yet a concrete implementation, object instance, or behavior-owning method
- class-object / factory proof is a useful middle layer, but still not the first semantic consumer

### `CoGetClassObject` may locate and load code, but returns a class-object interface

The `CoGetClassObject` documentation says it provides a pointer to an interface on a class object associated with a CLSID and can locate / dynamically load the executable code required. It also describes the common pattern: get the class object, then call `CreateInstance`; `CoCreateInstance` encapsulates connecting to the class object, creating the instance, and releasing the class object for the single-object case.

Sources:
- Microsoft Learn, `CoGetClassObject` — https://learn.microsoft.com/en-us/windows/win32/api/combaseapi/nf-combaseapi-cogetclassobject
- Microsoft Learn, `CoCreateInstance` — https://learn.microsoft.com/en-us/windows/win32/api/combaseapi/nf-combaseapi-cocreateinstance

Reverse-engineering implication:
- a `CoGetClassObject` / `CoCreateInstance` call is activation / factory-acquisition / object-creation evidence, not automatically downstream method-consumer proof
- the class context (`CLSCTX_*`), CLSID, requested IID, apartment/thread posture, and return interface pointer matter before asserting which server and interface were actually reached

### Running EXE servers publish class objects via `CoRegisterClassObject`

Microsoft's "Registering a Running EXE Server" says an EXE server should call `CoRegisterClassObject` after launch. This registers the CLSID in the class table so the SCM can determine it does not need to launch the class again if the server is already running. If the server is not in the class table, the SCM checks registry values and launches the server for the CLSID.

Sources:
- Microsoft Learn, "Registering a Running EXE Server" — https://learn.microsoft.com/en-us/windows/win32/com/registering-a-running-exe-server
- Microsoft Learn, `CoRegisterClassObject` — https://learn.microsoft.com/en-us/windows/win32/api/combaseapi/nf-combaseapi-coregisterclassobject

Reverse-engineering implication:
- registration in the class table is runtime publication truth for a class object, distinct from install-time registry truth
- process-launch observation is still weaker than proving the class object was registered, selected, and used for the current client request

### `IClassFactory::CreateInstance` creates an uninitialized object and returns a requested interface pointer

The `IClassFactory::CreateInstance` documentation says the method creates an uninitialized object. The requested IID controls the interface pointer returned through `ppvObject`; unsupported interfaces should return `E_NOINTERFACE` and set the output pointer to null.

Source:
- Microsoft Learn, `IClassFactory::CreateInstance` — https://learn.microsoft.com/en-us/windows/win32/api/unknwn/nf-unknwn-iclassfactory-createinstance

Reverse-engineering implication:
- `CreateInstance` success is object/interface acquisition truth, not yet proof that the behavior-bearing method was called
- `QueryInterface`, aggregation, marshaling proxy/stub boundaries, and apartment delivery can still change which code or thread sees the later call

### DCOM activation makes CLSID/IID request and returned object references explicit

The MS-DCOM Activation section describes activation as creating or finding an existing object or class factory. At a rudimentary level the client sends a CLSID, one or more IIDs, and optionally initialization storage; activation returns object references to the client.

Source:
- Microsoft Open Specifications, `[MS-DCOM]: Activation` — https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-dcom/c767a336-608a-4005-a39d-0d5bc68d34b7

Reverse-engineering implication:
- remote/local activation evidence is still activation/object-reference truth
- method call ingress, parameter unmarshaling, authorization, handler dispatch, and first state/effect consumer remain separate proof objects

## Practical synthesis

The compact stop rule for COM-shaped native reversing is:

```text
registered != activated != factory-selected != object-created != interface-bound != method-entered != consumed/effected
```

Use this seam when CLSID/registry/AppID evidence, `CoCreateInstance`, `CoGetClassObject`, `CoRegisterClassObject`, `IClassFactory::CreateInstance`, `QueryInterface`, proxy/stub artifacts, or DCOM activation telemetry are visible, but the current analyst claim still needs to prove one behavior-owning method / handler / reducer / state write.
