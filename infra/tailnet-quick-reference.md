# Tailnet Quick Reference

这份文档是给“直接调用”准备的，不是背景说明。

## Current core members

- `oracle-gateway` — public `129.150.61.78` / tailnet `100.116.171.76`
- `oracle-open_claw` — public `64.110.106.11` / tailnet `100.78.194.18`
- `ali-cloud` — public `106.15.239.221` / tailnet `100.98.184.19`
- `oracle-registry` — public `140.245.33.114` / tailnet `100.96.23.110`
- `oracle-new2` — public `140.245.61.236` / tailnet `100.79.183.3`
- `oracle-mail` — public `140.83.52.216` / tailnet `100.116.13.44`

## Preferred mental model

默认顺序：
1. 机器间互联 → 先想 Tailnet IP / 语义化 alias
2. 人工 SSH 登陆 → 先用本地 SSH alias
3. 公网域名 / 公网 IP → 仅在外部入口、服务暴露、DNS 排障时再想

## Common checks

### Show local tailnet identity
```bash
tailscale ip -4
tailscale status
```

### Quick connectivity checks to gateway
```bash
tailscale ping 100.116.171.76
ping -c 3 100.116.171.76
```

### Show all known tailnet peers from current host
```bash
tailscale status
```

## SSH shortcuts from this workspace host

### Login by semantic SSH alias
```bash
ssh oracle-gateway
ssh ali-cloud
ssh oracle-registry
ssh oracle-new2
ssh oracle-mail
```

### Run a quick remote command
```bash
ssh oracle-gateway 'hostname && tailscale ip -4'
ssh oracle-registry 'hostname && tailscale ip -4'
ssh ali-cloud 'hostname && tailscale ip -4'
```

## Machine-to-machine examples

### From one server, test reachability to gateway
```bash
tailscale ping 100.116.171.76
```

### From one server, hit ali-cloud over Tailnet
```bash
ping -c 3 100.98.184.19
curl http://100.98.184.19:10086
```

### From one server, SSH to another over Tailnet directly
(only when the remote sshd is listening normally and host firewall permits it)
```bash
ssh root@100.98.184.19
ssh ubuntu@100.96.23.110
ssh ubuntu@100.79.183.3
ssh root@100.116.13.44
```

## Current host-specific notes

### `oracle-gateway`
- canonical tailnet reference point for current validation
- small 1C1G box: keep workloads lean
- also runs Hysteria / Caddy

### `ali-cloud`
- Tailscale health warning: configured DNS servers not reachable
- tailnet membership itself is working

### `oracle-mail`
- Tailscale health warning: SELinux may interfere with Tailscale SSH
- tailnet membership itself is working

### `oracle-registry`
- semantic hostname is now `oracle-registry`
- prefer this name over the old generic `oracle-new1`

## When to use which identity

### Use SSH alias when:
- logging in from this OpenClaw workspace host
- you want existing local SSH config / key material / usernames

### Use Tailnet IP when:
- documenting machine-to-machine calls
- testing inter-host reachability
- describing future service mesh / internal routing
- bypassing public-path ambiguity

### Use public IP / public domain when:
- debugging external exposure
- checking ingress, DNS, TLS, Caddy, or firewall behavior
- testing from outside the Tailnet
