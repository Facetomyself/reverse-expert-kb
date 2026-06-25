# OpenAi (migrated, not running)

- Host: `oracle-proxy`
- Path: `/root/OpenAi`
- Source: migrated from the current OpenClaw host on `2026-03-16`
- Current state: **migrated only; not running**
- Service status: **not part of active production / service map**

## What this is

这是一个从当前 OpenClaw 主机迁移到 `oracle-proxy` 的项目目录副本，目的是把文件转移到该机器保存。

它目前的语义是：
- 已迁移
- 本地源目录已删除
- 没有在 `oracle-proxy` 上启动
- 不应被视为线上服务、守护进程、容器项目或反代后端

## Operational rule

看到 `/root/OpenAi` 时，默认结论应为：
- **这是迁移材料，不是运行中的服务**

除非有明确证据证明它已被启用，例如：
- `ps` / `pgrep` 看到相关进程
- `docker ps` 看到相关容器
- `ss -ltnp` 看到相关监听端口
- `systemctl` 看到对应 service
- 反代配置明确把流量导向该项目

没有这些证据时，不要把它写进运行态服务地图。

## Verification checklist

如果以后需要确认它是否仍然只是“存放未运行”，优先检查：

```bash
ssh oracle-proxy
cd /root/OpenAi
ps aux | grep -i openai
pgrep -af 'python|node|uvicorn|gunicorn|pm2' | grep -i /root/OpenAi || true
docker ps --format '{{.Names}}\t{{.Image}}' | grep -i openai || true
ss -ltnp
systemctl --type=service --all | grep -i openai || true
```

## If enabling in the future

如果未来要把这个目录真正启用为服务，先补这些文档再上线：
- 在 `PROJECTS.md` 中把状态从 `migrated-not-running` 改成真实状态
- 新建或更新对应项目运维文档
- 记录所用运行方式：裸进程 / systemd / docker / compose / 反代
- 在 `CHANGELOG.md` 中写明启用时间和验证结果

## Change history

- 2026-03-16: migrated from the current OpenClaw host to `oracle-proxy:/root/OpenAi`
- 2026-03-16: explicitly documented as **not running** after migration
