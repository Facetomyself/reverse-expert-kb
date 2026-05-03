# macOS ServiceManagement / launchd / XPC helper consumer notes — 2026-05-04

Source class: external research synthesis
Related topic: `topics/native-macos-servicemanagement-xpc-helper-consumer-workflow-note.md`
Search artifact: `sources/native/2026-05-04-0450-macos-service-management-xpc-search-layer.txt`

## Why this was selected

Recent KB growth covered Linux D-Bus, Linux AF_UNIX fd/credential passing, and Windows named-pipe impersonation. The native practical branch still had a thinner macOS service/helper seam: ServiceManagement-registered helpers, launchd domains, MachServices, XPC services, and service-side handler ownership. This is adjacent to the iOS XPC branch and malware launchd/Login Items persistence pages, but the operator proof object is different: a native macOS helper or daemon route where registration / launchd availability / Mach-service lookup can be overread as handler-owned behavior.

## Source-backed observations

### Apple ServiceManagement / SMAppService

Apple's current ServiceManagement documentation exposes `SMAppService` with service registration, unregistration, status inspection, and System Settings Login Items interaction. The search result snippets for Apple's package-installer migration page note that newer SMAppService packaging places helper executable launchd property lists in the helper executable bundle rather than relying only on shared locations such as `/Library/LaunchDaemons`, and that a sample registers a launch agent at install time.

Reverse implication:
- a helper plist or embedded launchd plist is registration metadata, not launch proof
- `SMAppService.status`, Login Items / Background Items state, or successful registration narrows launchd posture but does not prove one Mach-service connection or handler call
- the same label can be represented by legacy plist locations, bundled helper plists, installer-copied plists, and user-approval/system-settings state; freeze the winning registration path before interpreting runtime behavior

Sources:
- `SMAppService` — https://developer.apple.com/documentation/servicemanagement/smappservice
- `Updating your app package installer to use the new Service Management API` — https://developer.apple.com/documentation/ServiceManagement/updating-your-app-package-installer-to-use-the-new-service-management-api

### Apple launchd daemon / agent behavior

Apple's archived Daemons and Services guide separates launchd registration from actual daemon process lifetime. launchd loads launch-on-demand plist parameters, registers requested sockets/file descriptors, launches daemons when requests arrive, and can relaunch on demand after idle shutdown. It also distinguishes system-level daemons from per-user agents and notes that user agents are loaded for logged-in users.

Reverse implication:
- plist presence / label visibility is not equivalent to a running process
- system vs user / GUI session / process-domain scope is a first-class proof object
- launch-on-demand can make a port or service appear available while the daemon is not yet running
- request arrival, launch, process identity, and later handler execution must be separated

Sources:
- `Creating Launch Daemons and Agents` — https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingLaunchdJobs.html
- `launchd.plist(5)` — https://www.manpagez.com/man/5/launchd.plist/
- `launchctl(1)` — https://www.manpagez.com/man/1/launchctl/

### Apple XPC services / NSXPCConnection

Apple's archived XPC services guide frames XPC services as launchd-managed helpers that launch on demand, can be restarted after crashes, may be terminated when idle, and are generally private to the containing application. It separates `NSXPCConnection`, `NSXPCInterface`, `NSXPCListener`, and `NSXPCListenerEndpoint`; the NSXPC layer is an Objective-C remote-procedure-call mechanism where client proxy calls relay to corresponding service-side objects.

Reverse implication:
- client-side `NSXPCConnection` / proxy creation is only route truth
- launchd-managed lifecycle can make connection invalidation/restart a separate proof object
- `NSXPCInterface` / protocol recovery is contract-selection truth, not service-side method-entry truth
- listener acceptance, exported-object method entry, reply/error, and durable effect must stay separate

Source:
- `Creating XPC Services` — https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingXPCServices.html

### Privileged helper / SMJobBless lineage

Apple's SMJobBless sample describes embedding a privileged helper tool in an app, securely installing it, associating it with the invoking application, relying on code signatures to ensure the expected helper, prompting for authorization on first use, and isolating privileged code in a separate process instead of running the whole app elevated.

Reverse implication:
- helper availability is tied to code-signing / requirement / authorization / launchd setup, not just a binary name
- proof should preserve caller identity / code requirement / entitlement or audit-token check when the helper does privileged work
- authorization success or helper installation is weaker than one privileged operation executed by the expected helper method

Source:
- Apple SMJobBless sample ReadMe — https://developer.apple.com/library/archive/samplecode/SMJobBless/Listings/ReadMe_txt.html

### MachServices and XPC abuse writeups

HackTricks summarizes the common macOS local-service route as client process -> `NSXPCConnection` or `xpc_connection_create_mach_service()` -> launchd Mach service -> daemon receives XPC message -> daemon should verify identity/entitlements -> privileged operation. It also emphasizes that LaunchDaemon/LaunchAgent plists with `MachServices` register named Mach ports, and that client verification should rely on stronger identity material than PID alone. Treat this as practitioner/security context, not as an authoritative API spec.

Tencent Xuanwu's CVE-2020-9971 writeup is useful for reverse workflow because it distinguishes application-bundle XPC services from LaunchDaemon/LaunchAgent Mach services and introduces launchd process domains as a namespace for process-scoped XPC service information. Its exploit details are not needed here; the durable RE lesson is that domain/scope ownership and launchd registration can be the real proof object before handler behavior.

Reverse implication:
- Mach service name visibility is endpoint metadata, not an accepted connection
- launchd domain / system-vs-user-vs-process scope matters before attributing the helper
- audit token / entitlements / code signature checks are separate from listener acceptance and method dispatch
- security writeups should be used to sharpen proof boundaries, not to turn the KB page into an exploitation recipe

Sources:
- HackTricks, `macOS XPC Mach Services Abuse` — https://hacktricks.wiki/en/macos-hardening/macos-security-and-privilege-escalation/macos-proces-abuse/macos-xpc-mach-services-abuse.html
- Tencent Xuanwu Lab, `CVE-2020-9971 Abusing XPC Service mechanism to elevate privilege in macOS/iOS` — https://xlab.tencent.com/en/2021/01/11/cve-2020-9971-abusing-xpc-service-to-elevate-privilege/

## Durable synthesis

The practical macOS helper split to preserve is:

```text
registration/plist visible
  != launchd domain and enablement state frozen
  != Mach service / XPC endpoint currently published
  != expected helper process launched under expected identity
  != client identity / entitlement / code requirement accepted
  != listener / connection accepted
  != exported method or xpc handler entered
  != reply/error/lifecycle state interpreted
  != service-owned durable effect consumed
```

Compact branch memory:

```text
registered != domain-live != endpoint-published != launched-identity != accepted-client != method-entered != replied/lifecycle != consumed/effected
```

## Operator tactics to preserve

- Start by choosing one label / service identifier / Mach service / client selector, not every helper in the app bundle.
- Freeze domain: system LaunchDaemon, user LaunchAgent, GUI session, process-scoped XPC service, bundled app XPC service, or ServiceManagement registered helper.
- Treat `Label`, `MachServices`, `Program` / `ProgramArguments`, `BundleProgram`, `SMAppService.status`, Login Items state, and `launchctl print` output as setup or routing evidence until one runtime connection is tied to them.
- Prove the launched helper's path, bundle, code signature, effective user/session, and launch reason before attributing privileged or user-scoped effects.
- For NSXPC, keep proxy route, listener acceptance, exported interface, exported object method, reply/error, interruption/invalidation, and later state/effect separate.
- If trust is part of the behavior, capture audit-token / entitlement / code requirement checks as their own boundary; PID/name clues are weak reductions.
- Stop only after one helper-owned state write, filesystem/database operation, policy reducer, child launch, privileged operation, reply-owned state change, or downstream effect is tied to the accepted request.
