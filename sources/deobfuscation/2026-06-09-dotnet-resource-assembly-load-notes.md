# .NET resource / reflection loader notes — 2026-06-09

## Search posture
External-research-driven pass for a thinner deobfuscation / malware-loader seam: managed .NET resources, byte arrays, reflection loading, and first managed payload consumer proof.

Search artifact:
- `sources/deobfuscation/2026-06-09-0450-dotnet-resource-assembly-load-search-layer.json`

## Sources consulted
- Microsoft Learn, `System.Reflection.Assembly.Load` — https://learn.microsoft.com/en-us/dotnet/api/system.reflection.assembly.load
- Microsoft Learn, `System.Resources.ResourceManager` — https://learn.microsoft.com/en-us/dotnet/api/system.resources.resourcemanager
- Unit 42, `Uncovering .NET Malware Obfuscated by Encryption and Virtualization` — https://unit42.paloaltonetworks.com/malware-obfuscation-techniques/
- Unit 42, `Stealthy .NET Malware: Hiding Malicious Payloads as Bitmap Resources` — https://unit42.paloaltonetworks.com/malicious-payloads-as-bitmap-resources-hide-net-malware/
- cyber.wtf, `.NET Deobfuscation` — https://cyber.wtf/2025/04/07/dotnet-deobfuscation/
- dnlib / de4dot / ConfuserEx-related search results from Exa/Tavily as supporting ecosystem pointers.

## Practical extraction

### Managed loader proof objects
Microsoft’s `Assembly.Load` API documentation keeps the loader boundary concrete: the managed runtime can load an assembly by name or from a COFF-based image in a byte array. For reversing, this means that a decoded byte array is not yet payload execution; it is only a candidate loaded-image handoff until the load event and later invocation are proved.

`ResourceManager` / manifest-resource access similarly keeps resource visibility separate from runtime selection and use. A resource entry or bitmap-looking blob can be an embedded stage, a decoy, localization material, or a protected configuration object. The proof object changes only when the code path selects that resource, decodes/extracts bytes, validates assembly/file identity, and hands it to a loader or consumer.

### Unit 42 staged .NET malware patterns
Unit 42’s 2024 .NET obfuscation write-up highlights payload protection and delivery techniques including AES, code virtualization, staged payloads, PE overlay storage, and dynamic code loading / deobfuscation / execution via .NET reflection. Its useful RE lesson is not just “look for reflection”; the practical ladder is:

```text
carrier bytes / overlay / resource
  -> key/IV/marker or decode routine
  -> decoded stage bytes
  -> Assembly.Load / reflection handoff
  -> invoked method / entry bridge
  -> config/comms/persistence consumer
```

The 2025 bitmap-resource case is a sharper scenario: a benign-looking 32-bit .NET app contains bitmap resources; an initial resource is deobfuscated into `TL.dll`; reflection / late binding invokes a method in that loaded assembly; a second bitmap resource is unpacked into another assembly; a later byte-array resource becomes the final payload. This proves why `bitmap resource visible` and `TL.dll bytes recovered` are still weaker than `loaded assembly + selected method + invoked consumer + downstream payload effect`.

### cyber.wtf .NET deobfuscation patterns
The cyber.wtf deobfuscation article describes a textbook managed packer chain: a byte array is recovered, `Assembly.Load(...)` loads it, type lookup selects a target, and `InvokeMember(...)` starts execution. It also emphasizes that the assembly-loading part may be buried under control-flow flattening or call indirection, so the cheaper discriminant is often a runtime breakpoint/hook on `Assembly.Load` plus capture of the byte array, followed by a first invocation/consumer proof.

The same article’s delegate/proxy discussion is useful because it keeps invocation proof separate from load proof: a delegate field, type handle, resource stream, or proxy call can hide the real call target. A managed assembly being loaded is therefore only the middle of the story; the first behavior-bearing call target can be a reflection member, delegate target, static constructor side effect, or later ordinary method.

## Operator stop rule

Preserve this split:

```text
resource/overlay visible != bytes decoded != assembly loaded != target selected/invoked != managed consumer/effect-owned
```

When resource-backed .NET malware or obfuscated managed packers are under analysis, do not stop at a resource list, a dumped DLL, or an `Assembly.Load` hit unless the analyst’s actual question is only “is there a hidden managed stage?”. For behavior claims, the durable proof object is the selected target plus one first consumer/effect.

## Useful evidence table

```text
sample | carrier(resource/overlay/array) | selection path | decode routine | key/iv/marker | decoded hash/MZ/CLR | load API | load context | target selection | invocation API/delegate | first consumer/effect | confidence | next check
```
