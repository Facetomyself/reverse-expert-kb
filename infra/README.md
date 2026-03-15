# Infrastructure Knowledge Base

这不是单纯的机器清单，而是面向日常运维、排障、接手和复盘的基础设施手册。

## 目标

每台机器的文档要回答四类问题：

1. **这台机器是什么**：系统、网络、用途、入口
2. **这台机器跑了什么**：项目、端口、容器、依赖关系
3. **我该怎么运维**：检查、重启、日志、数据、健康检查
4. **出问题怎么排**：常见故障、判断路径、修复动作

## 目录结构

```text
infra/
  README.md
  conventions.md
  inventory.yaml
  hosts/
    oracle-proxy/
      HOST.md
      NETWORK.md
      PROJECTS.md
      CHANGELOG.md
      projects/
        tavily-proxy.md
        tavily-key-generator.md
        grok-register.md
        grok2api.md
        cliproxy.md
```

## 设计原则

- **以主机为主视角**：先按机器组织，再细化到项目
- **项目文档写到可复制运维**：不要只写概念，要写命令
- **敏感信息尽量不直接写死**：写位置、写来源、写取用方式
- **把项目关系写清楚**：谁依赖谁、谁给谁喂数据、谁对外提供入口
- **把踩坑点沉淀进去**：不要把关键经验只留在聊天记录里

## 文档等级

- `HOST.md`：机器身份、系统基线、用途
- `NETWORK.md`：公网 IP、域名、端口、暴露方式
- `PROJECTS.md`：项目导航页和优先级
- `projects/*.md`：每个项目的详细运维手册
- `CHANGELOG.md`：这台机器的重要变更记录

## 敏感信息规则

文档里可以写：
- 主机名
- 公网 IP / 域名
- 路径
- 容器名 / 服务名
- 端口
- 部署方式
- 常用运维命令
- 数据位置

文档里尽量不直接写：
- 密码
- token 全值
- 私钥
- API key 全值

推荐写法：
- `Admin password: see credential store`
- `Token configured in ~/.openclaw/credentials/...`

## 当前覆盖

- `oracle-proxy`：已建立较完整文档
- `oracle-docker-proxy`：已建立较完整文档
- `ali-cloud`：已建立第一、二轮文档
- `oracle-mail`：已建立首轮文档并标记为退役
- `self-server`：已确认当前不可达
- `oracle-open_claw`：已明确是本机，不作为下一台远程主机

另见：
- `infra/OVERVIEW.md` — 全局运维地图 / 状态总览
- `infra/host-status.yaml` — 结构化主机状态表
- `infra/dns-reconciliation.md` — DNS / 主机 / 服务对账
- `infra/dns-cleanup-plan.md` — DNS 清理执行计划
- `infra/dns-first-wave.md` — 第一波 DNS 变更清单
