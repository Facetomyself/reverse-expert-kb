# Noise control

## Naming policy
- Use only canonical semantic host names in active ops-assistant inventory and automation.
- `oracle-gateway` is the canonical name for the gateway host.
- `oracle-registry` is the canonical name for the registry front-door host.
- `oracle-reverse-dev` is the canonical name for the reverse-development utility host.
- Do not keep probing or documenting older transitional names as active identities.

## Known exceptions
- `self-server`: known-unreachable-from-openclaw
- `home`: windows-tailnet-endpoint-not-an-ssh-ops-node
- `company`: windows-tailnet-endpoint-not-an-ssh-ops-node
- `home-macmini`: intermittently-online-tailnet-node
- `oracle-mail`: archived-mail-stack-host
