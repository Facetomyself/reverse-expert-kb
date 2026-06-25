# home / HOST

## Identity
- Name: `home`
- Provider: home-tailnet
- Tailnet IPv4: `100.73.71.81`
- Current raw hostname: `DESKTOP-CAU8JMI`
- MagicDNS name: `home.tail646ee3.ts.net`
- OS: Windows

## Role
- Frequent home LAN entrypoint
- User-managed Windows workstation
- Tailnet member

## Access
- Reachable from the OpenClaw host over Tailnet as of 2026-03-26
- `tailscale ping` succeeded on 2026-03-26
- TCP `22` returned `connection refused` on 2026-03-26, so generic SSH access is not currently enabled

## Notes
- This is one of the user's manually added commonly used inner-network machines.
- Tailnet/MagicDNS naming is already semantic (`home`), even though the underlying Windows hostname is still generic.
- Per user decision on 2026-03-26, this Windows machine should stay as an interactive Tailnet-connected endpoint only, not a formal SSH-managed ops node.
