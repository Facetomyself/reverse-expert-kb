# Source Notes — D-Bus Service Activation and First Method Consumer

Date: 2026-04-28 04:50 Asia/Shanghai
Branch: native desktop/server practical workflows
Run artifact: `sources/native/2026-04-28-0450-dbus-service-activation-method-consumer-search-layer.txt`

## Scope

These notes support a practical native/Linux workflow seam:

```text
activatable D-Bus name visible
  != current owner / unique connection truth
  != service process activated and name acquired
  != object path / interface / member contract truth
  != method call delivered to the intended handler
  != first handler-owned consumer / side effect
```

The goal is not to teach D-Bus from scratch. The goal is to keep a reverser from overreading a `.service` file, bus name, introspection XML, or one `busctl call` as if it already proves the service-owned behavior path.

## Source-backed observations

### D-Bus tutorial / specification

Relevant source anchors:
- https://dbus.freedesktop.org/doc/dbus-tutorial.html
- https://dbus.freedesktop.org/doc/dbus-specification.html

Useful facts for reversing:
- D-Bus is message-oriented IPC, not a byte-stream protocol. Calls are routed through bus names, object paths, interfaces, members, and typed arguments.
- Object paths name native object instances exposed by the service, but the mapping from object path to native object / handler is binding-specific.
- Well-known bus names are lifecycle / routing names. Unique names identify a particular connection and are not reused during the bus daemon lifetime.
- Service activation means the bus can start an application when a message targets a well-known name that has no current owner and is activatable.
- Auto-start holds the original message while the service starts, waits for it to request the name, then delivers the message if activation succeeds.
- `.service` files map well-known names to executables. System-bus service files require a `User` key; search-path priority can decide which service file wins when multiple directories provide the same name.
- `SystemdService=` can delegate activation to systemd, so the D-Bus service file, systemd unit, and eventual process may be different proof objects.
- Activation may be mediated by policy / AppArmor before and after the process appears, so “activatable” is not the same as “call delivered.”

Practical implication:
- activation metadata proves eligibility, not handler execution. Keep bus-name ownership, process start, name acquisition, method delivery, and handler-side effect separate.

### `dbus-daemon(1)`

Relevant source anchor:
- https://dbus.freedesktop.org/doc/dbus-daemon.1.html

Useful facts:
- There are standard systemwide and per-login-session bus instances with different configuration files and policies.
- The daemon can be run with `--systemd-activation` to enable systemd-style service activation.
- System bus policy files are normally loaded from `/usr/share/dbus-1/system.d`; administrator overrides are in `/etc/dbus-1/system.d`.
- `SIGHUP` only partially reloads configuration; policy changes may apply, but some changes require restart.

Practical implication:
- do not treat a policy/config file view as current delivery truth without checking the bus instance and current owner/process state.

### `busctl(1)`

Relevant source anchors:
- https://man7.org/linux/man-pages/man1/busctl.1.html
- https://man.archlinux.org/man/busctl.1.en

Useful facts:
- `busctl list` distinguishes unique and well-known names and can show activatable peers.
- `busctl status SERVICE` shows process information and credentials for a service owner.
- `busctl monitor` and `busctl capture` observe messages; capture can produce pcapng for Wireshark-style inspection.
- `busctl tree` and `busctl introspect` recover object paths, interfaces, methods, properties, and signals.
- `busctl call` invokes a method with explicit service, object, interface, method, signature, and arguments.
- `--auto-start=` controls whether a call implicitly activates an activatable service.
- `--expect-reply=` changes whether the caller waits for reply / error truth.

Practical implication:
- good D-Bus reversing usually needs at least two proof surfaces: bus-level route/delivery evidence and service-side handler/effect evidence. Introspection is a contract hint; monitor/capture is delivery evidence; status/name-owner is current-owner evidence; handler breakpoint/log/watchpoint is consumer evidence.

## Durable KB split to preserve

```text
service file / activatable name found
  != bus instance and policy path selected
  != current owner / unique connection identified
  != activation request succeeded
  != name acquired by the process that matters
  != object path / interface / member contract selected
  != method call delivered to that owner
  != binding dispatch reached the native handler
  != first handler-owned consumer / side effect
```

## Operator tactics

- Start by deciding whether the relevant bus is system, user/session, container, or custom-addressed.
- List both acquired and activatable names; record the unique owner when present.
- If the service is activatable but not owned, trigger with `--auto-start=yes` or explicit `StartServiceByName`, then observe `NameOwnerChanged` / owner status.
- Treat `.service` / `SystemdService=` / unit aliases as launch-route hypotheses, not as handler proof.
- Use introspection / `tree` only to select a target object/interface/member and expected signature.
- Use `monitor` / `capture` / match rules to prove the actual method call and arguments were delivered.
- On the service side, break at binding dispatch surfaces or handler implementations, not only at bus connect / name request.
- Freeze the first behavior-bearing consumer: state write, policy reducer, worker enqueue, file/network/IPC action, or reply-producing branch.
