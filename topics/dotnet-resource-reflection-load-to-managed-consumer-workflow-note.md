# .NET Resource / Reflection Load to Managed Consumer Workflow Note

Topic class: concrete workflow note
Ontology layers: deobfuscation practice, malware-analysis overlap, managed-runtime loader handoff
Maturity: practical
Related pages:
- topics/obfuscation-deobfuscation-and-packed-binaries.md
- topics/protected-runtime-practical-subtree-guide.md
- topics/decrypted-artifact-to-first-consumer-workflow-note.md
- topics/string-decryption-origin-to-artifact-provenance-workflow-note.md
- topics/packed-stub-to-oep-and-first-real-module-workflow-note.md
- topics/malware-packed-loader-to-first-payload-handoff-workflow-note.md
- topics/malware-config-to-capability-bucket-workflow-note.md

## 1. Why this page exists
Managed .NET malware and obfuscated managed packers create a recurring false proof:

```text
embedded resource / overlay / byte array visible
  or dumped DLL recovered
  or Assembly.Load hit
  == payload behavior proved
```

That is usually too broad. In .NET cases, the hidden payload path often crosses several distinct boundaries:

```text
resource / overlay / static byte array / bitmap carrier
  -> selected carrier path
  -> decode / decrypt / decompress routine
  -> decoded PE / CLR image bytes
  -> Assembly.Load / load-from-bytes boundary
  -> target type/member/delegate/static-constructor selection
  -> first managed consumer or downstream malware effect
```

The KB already has notes for packed-stub handoff, decrypted-artifact consumer proof, malware packed-loader handoff, and protected-runtime artifact provenance. This page fills the managed-runtime variant where the important handoff is not a native OEP but a CLR resource / reflection / delegate / `Assembly.Load(byte[])` chain.

## 2. When to use this note
Use this note when most of these are true:
- the target is a managed .NET assembly or a managed stage inside a malware chain
- resources, PE overlays, bitmap resources, manifest resources, static byte arrays, or resource-stream reads are visible
- a decode routine or unpacked bytes can be recovered, but the first behavior-bearing managed target is still unclear
- `Assembly.Load(...)`, reflection, `InvokeMember`, delegates/proxies, late binding, or static constructors are on the likely path
- the analyst needs to prove the first real payload-side managed consumer, not merely extract another hidden DLL

Do **not** use this as a generic .NET tooling checklist. Use it when the current uncertainty is the handoff from hidden managed bytes into one selected and behavior-bearing managed routine.

## 3. Core stop rule
Keep this split visible:

```text
resource/overlay visible != bytes decoded != assembly loaded != target selected/invoked != managed consumer/effect-owned
```

A resource name, bitmap blob, manifest stream, dumped DLL, or `Assembly.Load` breakpoint is useful evidence, but it answers a different question from “which managed routine owns the later config, request, persistence, or payload effect?”.

## 4. Practical workflow

### Step 1: classify the carrier, not just the blob
Start by naming the carrier type and the path that selects it:

```text
carrier:
  manifest resource / ResourceManager entry / GetManifestResourceStream / bitmap resource / PE overlay / static byte array / encoded string / file dropped by wrapper

selection path:
  entry point -> UI init / form constructor / static constructor / helper -> resource name or marker -> decode call
```

For resource-backed cases, distinguish:
- resource inventory truth
- runtime-selected resource truth
- resource stream / object materialized truth
- decoded byte-array truth

A bitmap-looking resource is not meaningful by itself; the useful proof starts when a path selects it and consumes bytes from it.

### Step 2: recover one decode contract
Freeze the smallest decode contract that produces candidate stage bytes:

```text
decode routine:
  input carrier + offset/length/marker + key/IV/constants + compression/encryption transform -> output bytes
```

Good evidence includes:
- marker strings or offsets used to split overlay/resource material
- key / IV / salt / XOR table / decompressor constants
- output length and hash
- `MZ`, CLR metadata, or a valid managed module after decode
- repeatability across a clean replay or runtime dump

Do not over-read a successful decoder as execution proof. It is still only decoded-stage truth.

### Step 3: prove the load boundary
Watch or instrument the managed loader boundary:

```text
Assembly.Load(byte[])
Assembly.Load(byte[], ...)
Assembly.LoadFrom / LoadFile if file-backed
AppDomain / AssemblyLoadContext variants when relevant
```

For the load event, record:
- caller method / stack
- byte-array identity or hash
- assembly identity, module name, metadata token/MVID when available
- load context or AppDomain / AssemblyLoadContext if it affects later reachability
- whether the bytes loaded are the same decoded bytes recovered offline

A load boundary proves the runtime accepted a stage. It still does not prove which member will execute.

### Step 4: resolve target selection separately
After load, locate the first target selection mechanism:

```text
assembly.GetTypes() / GetType(...)
GetMethod / InvokeMember / MethodInfo.Invoke
LateBinding / dynamic invoke
Delegate.CreateDelegate / proxy delegate field
static constructor side effect
entry-like exported method naming convention
```

Record the selection predicate, not only the final method name:
- name string or decrypted name
- first type matching condition
- metadata token / method handle
- delegate field assignment site
- static constructor or type-initializer trigger
- reflection binding flags / argument array

If the method name is obfuscated, the predicate can be more trustworthy than the name.

### Step 5: stop only at one first managed consumer/effect
The useful milestone is one first consumer that makes the loaded stage behaviorally meaningful:

```text
loaded assembly
  -> selected target
  -> invocation / delegate / static-constructor entry
  -> first config parser / request builder / persistence helper / next-stage loader / final payload launch
```

Good stop points include:
- a config decode routine entered from the loaded stage
- a first request-builder or transport wrapper call owned by the loaded stage
- a persistence or file-write path owned by the loaded stage
- a next `Assembly.Load`, process launch, DLL load, or native handoff with caller ownership preserved
- a static-constructor side effect that writes durable state or schedules the next stage

If the first consumer is just another loader, hand off to the malware packed-loader or staged-execution notes with the new stage identity preserved.

## 5. Evidence table
Use this compact table during case work:

```text
sample | carrier | resource/offset/marker | decode routine | key/IV/constants | decoded hash/type | load API/context | loaded assembly identity | target selection | invocation mechanism | first managed consumer/effect | confidence | next check
```

This table forces the analyst to separate carrier, decode, load, invocation, and effect. That is the whole point of the note.

## 6. Breakpoint / hook plan

### Minimal dynamic plan
1. Break on `System.Reflection.Assembly.Load(byte[])` and related overloads.
2. Dump the byte array, hash it, and validate whether it is a managed PE / CLR image.
3. Capture the managed call stack and caller method.
4. Break on `MethodInfo.Invoke`, `Type.InvokeMember`, `Delegate.DynamicInvoke`, and suspicious `Delegate.CreateDelegate` paths if reflection/proxy invocation hides the target.
5. Once a target is selected, trace one hop into the loaded assembly and mark the first config/comms/persistence/next-loader consumer.

### Static-assisted plan
1. Enumerate resources and manifest-resource streams.
2. Search for resource names, marker strings, `GetManifestResourceStream`, `ResourceManager`, `Assembly.Load`, `InvokeMember`, `GetTypes`, and delegate-construction patterns.
3. Recover the decode routine and replay it offline only far enough to validate byte identity.
4. Reopen dumped managed stages in dnSpyEx / ILSpy and cross-check with runtime target selection.
5. Avoid broad deobfuscation until one selected target path says which subset matters.

## 7. Case-shaped reminders

### Bitmap-resource staged loader
A bitmap or resource entry can be a carrier for an embedded managed stage. The stronger proof ladder is:

```text
bitmap resource selected
  -> bytes decoded / cut to stage length
  -> CLR assembly loaded
  -> reflection / late binding invokes one method
  -> that method selects the next resource or final payload path
```

Do not claim the bitmap itself “executes”; the selected method and its first consumer own the behavior.

### Reflection-loaded packer stage
A common managed packer shape is:

```text
byte-array recovery helper
  -> Assembly.Load(bytes)
  -> type lookup / first matching type
  -> InvokeMember / MethodInfo.Invoke
  -> payload-side method
```

When the type lookup is predicate-based rather than name-based, preserve the predicate. It may be the most stable artifact after renaming obfuscation.

### Delegate / proxy indirection
A delegate field or proxy class can hide the real call target after the stage has loaded. Treat delegate construction / assignment as target-selection evidence and delegate invocation as delivery evidence; neither is automatically the first behavior consumer.

## 8. Handoff rules
- If decoded bytes are readable but unused, hand off to `decrypted-artifact-to-first-consumer-workflow-note.md`.
- If the loaded managed stage is just another packed layer, hand off to `malware-packed-loader-to-first-payload-handoff-workflow-note.md` or `packed-stub-to-oep-and-first-real-module-workflow-note.md` with the managed-stage identity preserved.
- If the first consumer is config selection, hand off to `malware-config-to-capability-bucket-workflow-note.md`.
- If the first consumer is network request construction, hand off to `malware-first-request-family-and-comms-proof-workflow-note.md` or `malware-request-builder-to-send-boundary-workflow-note.md`.
- If the main blocker is string/key provenance before the stage can even be decoded, hand off to `string-decryption-origin-to-artifact-provenance-workflow-note.md`.

## 9. Source-backed cues
- Microsoft’s `Assembly.Load` API keeps the managed load boundary concrete: loading bytes is a runtime acceptance event, not automatically method execution.
- Microsoft’s `ResourceManager` / resource APIs keep resource access separate from resource selection and use.
- Unit 42’s staged .NET malware examples show overlay/resource/bitmap carriers, AES/decode logic, reflection loading, and multiple managed stages before final payload behavior.
- The cyber.wtf .NET deobfuscation walkthrough shows the practical breakpoint target: capture `Assembly.Load(...)` byte arrays, then resolve the reflection/delegate invocation that starts execution.

## 10. Compact branch-memory line
Preserve this line in parent pages:

```text
resource/overlay visible != bytes decoded != assembly loaded != target selected/invoked != managed consumer/effect-owned
```
