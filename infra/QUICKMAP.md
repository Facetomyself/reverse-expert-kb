# Infrastructure Quick Map

这是 SSH / 远程主机任务的第一眼速查表。

## Hosts

| name | ssh alias | public IP | tailnet IP | lifecycle | reachability | docs |
|---|---|---:|---:|---|---|---|
| oracle-proxy | `oracle-proxy` | `158.178.236.241` | - | active | reachable | `hosts/oracle-proxy/HOST.md` |
| oracle-docker-proxy | `oracle-gateway` | `129.150.61.78` | `100.116.171.76` | active | reachable | `hosts/oracle-docker-proxy/HOST.md` |
| ali-cloud | `ali-cloud` | `106.15.239.221` | `100.98.184.19` | active | reachable | `hosts/ali-cloud/HOST.md` |
| oracle-mail | `oracle-mail` | `140.83.52.216` | `100.116.13.44` | active | reachable | `hosts/oracle-mail/HOST.md` |
| oracle-new1 | `oracle-registry` | `140.245.33.114` | `100.96.23.110` | active | reachable | `hosts/oracle-new1/HOST.md` |
| oracle-new2 | `oracle-new2` | `140.245.61.236` | `100.79.183.3` | active | reachable | `hosts/oracle-new2/HOST.md` |
| self-server | `self-server` | `211.144.221.229` | - | unknown | unreachable_from_openclaw | not fully documented yet |
| oracle-open_claw | `oracle-open_claw` | `64.110.106.11` | `100.78.194.18` | active | local | local machine; not a remote audit target |

## Tailnet quick use

已确认接入同一 Tailnet 的核心机器：
- `oracle-gateway` → `100.116.171.76`
- `oracle-open_claw` → `100.78.194.18`
- `ali-cloud` → `100.98.184.19`
- `oracle-registry` → `100.96.23.110`
- `oracle-new2` → `100.79.183.3`
- `oracle-mail` → `100.116.13.44`

最常用的心智模型：
- 机器间互联优先记 **Tailnet IP / 语义化 alias**
- 公网入口、域名、服务暴露再回各主机文档看
- 当前 Tailnet 连通性验证都以 `oracle-gateway` 为基准参考点

See also:
- `tailnet-quick-reference.md` — copy/paste oriented Tailnet / SSH command cheatsheet

## Recommended read order

1. `inventory.yaml`
2. `host-status.yaml`
3. `hosts/<host>/HOST.md`
4. Then as needed:
   - `hosts/<host>/NETWORK.md`
   - `hosts/<host>/PROJECTS.md`
   - `hosts/<host>/projects/*.md`
   - `hosts/<host>/CHANGELOG.md`
   - `OVERVIEW.md`

## Notes

- `infra/` is the source of truth for SSH / remote-host operations knowledge.
- After any meaningful edit, commit in the `infra/` repo.
- `infra/.git/hooks/post-commit` is expected to auto-push to the private GitHub repo.
- If auto-push fails, run `bin/sync-infra.sh` manually.
