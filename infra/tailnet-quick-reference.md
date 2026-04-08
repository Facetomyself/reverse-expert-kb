# Tailnet Quick Reference

## Current canonical node names
- `oracle-gateway` — public `129.150.61.78` / tailnet `100.116.171.76`
- `oracle-mail` — public `140.83.52.216` / tailnet `100.116.13.44`
- `ali-cloud` — public `106.15.239.221` / tailnet `100.98.184.19`
- `oracle-registry` — public `140.245.33.114` / tailnet `100.96.23.110`
- `oracle-reverse-dev` — public `140.245.61.236` / tailnet `100.79.183.3`
- `oracle-open_claw` — local host / tailnet `100.78.194.18`
- `home-nas` — tailnet `100.73.212.89`

## Common SSH entrypoints
```bash
ssh oracle-gateway
ssh oracle-mail
ssh ali-cloud
ssh oracle-registry
ssh oracle-reverse-dev
ssh home-nas
```

## Quick connectivity checks
```bash
ssh oracle-gateway 'hostname && tailscale ip -4'
ssh oracle-registry 'hostname && tailscale ip -4'
ssh oracle-reverse-dev 'hostname && tailscale ip -4'
```

## Guidance
- Use only semantic canonical names in current operations.
- Do not rely on older transitional host names in new docs or automation.
- `oracle-gateway` remains the main Tailnet connectivity reference point.
