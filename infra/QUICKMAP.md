# QUICKMAP

| Host | SSH alias | Public IP | Tailnet IP | Lifecycle | Reachability | Doc |
|---|---|---:|---:|---|---|---|
| oracle-proxy | `oracle-proxy` | `158.178.236.241` | `-` | active | reachable | `hosts/oracle-proxy/HOST.md` |
| oracle-gateway | `oracle-gateway` | `129.150.61.78` | `100.116.171.76` | active | reachable | `hosts/oracle-gateway/HOST.md` |
| oracle-mail | `oracle-mail` | `140.83.52.216` | `100.116.13.44` | active | reachable | `hosts/oracle-mail/HOST.md` |
| ali-cloud | `ali-cloud` | `106.15.239.221` | `100.98.184.19` | active | reachable | `hosts/ali-cloud/HOST.md` |
| oracle-registry | `oracle-registry` | `140.245.33.114` | `100.96.23.110` | active | reachable | `hosts/oracle-registry/HOST.md` |
| oracle-reverse-dev | `oracle-reverse-dev` | `140.245.61.236` | `100.79.183.3` | active | reachable | `hosts/oracle-reverse-dev/HOST.md` |
| home | `home` | `-` | `100.73.71.81` | active | interactive-only | `hosts/home/HOST.md` |
| company | `company` | `-` | `100.110.20.68` | active | interactive-only | `hosts/company/HOST.md` |
| home-macmini | `home-macmini` | `-` | `100.105.248.53` | active | unstable-observe | `hosts/home-macmini/HOST.md` |
| home-nas | `home-nas` | `-` | `100.73.212.89` | active | reachable_over_tailnet | `hosts/home-nas/HOST.md` |

## Tailnet reference points
- `oracle-gateway` → `100.116.171.76`
- `oracle-mail` → `100.116.13.44`
- `ali-cloud` → `100.98.184.19`
- `oracle-registry` → `100.96.23.110`
- `oracle-reverse-dev` → `100.79.183.3`
- `oracle-open_claw` → `100.78.194.18`

## Notes
- Current Tailnet connectivity validation uses `oracle-gateway` as the primary reference point.
- Only semantic names are canonical in current infra docs; older transitional names have been removed from the active inventory.
