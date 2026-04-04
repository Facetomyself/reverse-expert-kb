# Ops Assistant 设计草案 v1

## 1. 目标

在**当前 OpenClaw 环境**内建设一个专门的运维助理，用于持续运维：

- 多台服务器
- 各服务器上部署的业务/项目
- 基础设施文档与实际运行态的一致性
- 关键异常告警
- 低风险自愈
- 运维留痕（本地 + GitHub 私有仓库）

---

## 2. 部署形态

### 2.1 运行位置
- 部署在**当前 OpenClaw 实例**中
- 不新起第二套 OpenClaw
- 复用当前已验证可用的：
  - workspace 文件能力
  - SSH/exec 能力
  - Telegram 渠道
  - cron / 定时执行能力

### 2.2 独立工作区策略
虽然共用当前 OpenClaw 实例，但逻辑上采用**独立工作区**：

- 根目录：`ops-assistant/`
- 与主业务/研究/日常文件分离
- `infra/` 仍是 SSH / 主机知识唯一真源
- `ops-assistant/` 作为：
  - 巡检计划层
  - 运维策略层
  - 报告留痕层
  - 告警层

### 2.3 与现有 `infra/` 的关系
- `infra/`：主机/项目知识的真源
- `ops-assistant/`：持续运维执行与留痕层

换句话说：
- 主机是谁、怎么连、文档在哪 → 看 `infra/`
- 什么时候检查、检查结果、告警、自愈、待处理漂移 → 看 `ops-assistant/`

---

## 3. 当前受管范围（v1）

基于当前 `infra/`，首批纳入：

### Tier 0 / 本机
- `oracle-open_claw`（当前 OpenClaw 所在主机）

### Tier 1 / 核心
- `oracle-proxy`
- `oracle-gateway`

### Tier 2 / 次核心
- `ali-cloud`

### Tier 3 / 特殊状态
- `oracle-mail`（退役/归档态，低频检查）
- `self-server`（不可达态，专项跟踪）

### 管理对象不仅是主机，还包括：
1. 主机可达性
2. SSH 基线
3. 关键 systemd 服务
4. Docker/compose 服务
5. 域名/反代/端口暴露
6. 部署中的业务项目
7. “未文档化项目 / 新增容器 / 新增服务 / 漂移配置”

---

## 4. 关键能力设计

## 4.1 巡检能力

### A. 主机层巡检
每台机器至少检查：
- reachability（SSH / TCP）
- uptime / load / memory / disk
- 关键端口监听
- 关键 systemd 服务状态
- Docker 容器状态
- 最近失败服务/容器

### B. 业务层巡检
对每台机器上的已知项目检查：
- 进程/容器是否存在
- 关键 endpoint 是否存活
- 域名访问是否通
- 证书是否临近过期
- 上次部署目录是否还存在
- 反代配置是否仍指向活服务

### C. 文档一致性巡检
这是本方案的重要增强能力。

需要发现：
- `infra/hosts/<host>/PROJECTS.md` 中记录了，但机器上已不存在
- 机器上有新的 compose 项目 / systemd 服务 / 暴露端口，但 `infra/` 未记录
- 某域名已指向主机，但主机上无对应服务
- 某项目目录、compose 文件、systemd unit 有变化，但文档未更新

### D. 漂移发现能力（重点）
运维 assistant 必须能发现：
- 漏归档项目
- 未登记容器
- 新开端口
- 新增域名/新反代
- 旧文档与当前运行态不一致
- “机器上还有东西，但 `infra/` 没记”

这部分是巡检的一等公民，不是附属功能。

---

## 4.2 告警能力

### 当前告警通道
- **Telegram**（唯一主告警通道）
- 使用独立 Telegram bot/account：`telegram:alerts`
- 当前已验证可向用户私聊 `5585354085` 主动推送

### 告警等级

#### P1 - Critical（立即推送）
- 主机不可达
- 核心业务服务中断
- 核心反代/入口不可用
- OpenClaw / Gateway / 关键代理服务异常
- 磁盘接近打满（如 > 90%）
- 证书极近过期（如 < 7 天）

#### P2 - Warning（即时或短延迟推送）
- 某业务容器退出
- 关键项目 healthcheck 失败
- 文档与运行态明显漂移
- 新发现未登记项目/端口/服务
- 重复失败的定时任务

#### P3 - Info（默认不打扰，仅入报告）
- 常规巡检成功
- 低风险自愈成功
- 轻微资源波动
- 低优先级目录/项目变化

### 告警消息格式
建议统一为：
- 标题：`[P1][oracle-proxy] Tavily proxy unavailable`
- 摘要：发生了什么
- 检测时间
- 自动动作（如有）
- 下一步建议
- 报告链接/相对路径

---

## 4.3 自愈能力

### 原则
只允许**白名单低风险自愈**。

### 可自动执行（白名单）
- 重启指定容器
- `docker compose up -d` 拉起指定已知项目
- 重启指定 systemd 服务
- `nginx -t && systemctl reload nginx`（仅指定主机/场景）
- `openclaw gateway restart`
- 清理安全的临时缓存

### 不自动执行，需人工确认
- 修改业务配置
- 重建镜像
- 发布/回滚版本
- 修改反代
- 修改 cron/scheduler
- 修改数据库连接或 secrets 引用

### 默认禁止自动执行
- 防火墙调整
- SSH 配置调整
- 用户/权限/sudoers 变更
- 系统升级/重启
- 删除卷/数据库/关键目录
- 大范围批量 kill / prune

---

## 5. 权限设计（必须明确）

这是本方案的核心。

## 5.1 权限分层

### Level 1 — ReadOnlyInspect
允许：
- SSH 只读检查
- 查看日志
- 查看 systemd/docker 状态
- 网络与端口检查
- 检查目录、compose、unit 文件存在性
- 生成报告
- 发 Telegram 告警

这是默认权限层。

### Level 2 — SafeRemediate
在白名单范围内允许：
- 重启指定服务
- 重启指定容器
- 拉起指定 compose 项目
- 执行已批准的恢复脚本

要求：
- 每次动作有留痕
- 每次动作有前后状态检查
- 连续失败要停止升级，不可无限重试

### Level 3 — ChangeManaged
涉及配置变更，只能在明确审批后执行：
- 修改配置文件
- 调整反代/域名映射
- 增加/变更定时任务
- 改业务启动方式

### Level 4 — HumanOnly
这些动作只允许人工批准后单次执行，不纳入自动化：
- 防火墙 / SSH
- 用户权限
- 系统更新/重启
- 数据删除
- 重要迁移

## 5.2 主机/项目级授权模型
建议在后续增加一张授权表，例如：

```yaml
hosts:
  oracle-proxy:
    auto_actions:
      - restart:proxy-tavily-proxy-1
      - restart:tavily-scheduler
      - restart:camoufox
    ask_first:
      - edit:nginx
      - compose-rebuild:any
    forbidden:
      - firewall:any
      - sshd:any
```

这能把“能自动做什么”明确化。

---

## 6. 留痕与 GitHub 私有仓库

## 6.1 留痕原则
所有运维工作必须留痕，包括：
- 检查了什么
- 发现了什么
- 自动做了什么
- 是否修复成功
- 是否需要人工介入
- 哪些文档需要更新

## 6.2 留痕位置
建议：
- `ops-assistant/reports/YYYY-MM-DD/`
- `ops-assistant/alerts/`
- `ops-assistant/proposals/`
- 必要时同步更新 `infra/`

## 6.3 Git 留痕
建议单独建一个**私有 GitHub 仓库**，例如：
- `infra-ops-assistant`
- 或 `infra-ops-log`

### 为什么推荐单独私有仓库
- 你更容易查看运维变化
- 运维留痕和研究/杂项分开
- 适合后面做独立生命周期
- 权限、审计和回滚更清晰

### 推荐同步方式
- 本地目录：`ops-assistant/`
- 后续可以拆到独立 git repo，或先作为当前 workspace 中的 subtree / 子目录维护
- 每次巡检产出：
  - 仅在有变化时 commit
- commit 信息示例：
  - `ops(report): daily oracle fleet check 2026-03-17`
  - `ops(alert): record oracle-gateway registry-ui drift`
  - `ops(discovery): detect undocumented compose project on ali-cloud`

---

## 7. 巡检中“发现遗漏归档和修改项目”的设计

这是本方案必须支持的能力。

### 7.1 要发现什么

#### A. 未归档项目
例如：
- 主机上出现新的 compose 目录
- 新 systemd unit 指向未知项目目录
- 新暴露端口背后是未知服务
- 新域名反代到未登记服务

#### B. 已归档但已漂移
例如：
- `infra/PROJECTS.md` 里写着项目在跑，实际已停
- compose 文件已改，但文档未更新
- 项目路径、端口、域名变了
- 原先反代的后端已经不是同一个服务

#### C. 遗漏修改
例如：
- 新增 env 文件 / compose override
- 新增容器名、service 名
- 新增 systemd timer / cron
- 新增端口监听

### 7.2 如何发现
巡检时做这些对账：

1. **文档 → 运行态对账**
   - `infra/hosts/<host>/PROJECTS.md`
   - `infra/hosts/<host>/NETWORK.md`
   - 与 Docker / systemd / listening ports / reverse proxy 配置对比

2. **运行态 → 文档反查**
   - 找到所有 compose 项目、容器、unit、监听端口
   - 检查是否都能映射回 `infra/` 文档

3. **域名 → 后端对账**
   - 域名指向主机
   - 主机是否真有对应服务
   - 是否已记录

4. **目录发现**
   - 扫描常见部署目录，如：
     - `/opt`
     - `/srv`
     - `/root`
     - `/home/*`
   - 寻找 `docker-compose.yml` / `.env` / `compose.yaml` / systemd unit 线索

### 7.3 结果分级
- `documented`：已记录且一致
- `undocumented`：发现了但未记录
- `drifted`：已记录但与当前不一致
- `retired-candidate`：疑似已停用但文档仍现役

---

## 8. 目录结构建议

```text
ops-assistant/
  README.md
  docs/
    ops-assistant-design-v1.md
    alert-policy.md
    permission-model.md
    cron-plan.md
  inventory/
    managed-hosts.yaml
    service-owners.yaml
    drift-rules.yaml
  checks/
    host_health.py
    docker_inventory.py
    systemd_inventory.py
    reverse_proxy_inventory.py
    drift_scan.py
  runbooks/
    service-restart-whitelist.md
    incident-handling.md
    host-unreachable.md
    undocumented-project-triage.md
  reports/
    2026-03-17/
      oracle-proxy.md
      oracle-gateway.md
      fleet-summary.md
  alerts/
    telegram-templates.md
  state/
    last-check.json
    fingerprints.json
    known-services.json
  proposals/
    undocumented-projects-2026-03-17.md
```

---

## 9. 后台运行策略

## 9.1 周期建议

### 高频（5~15 分钟）
检查：
- 主机 reachability
- 核心服务是否在线
- 关键入口是否可访问

### 中频（每小时）
检查：
- docker / systemd
- 磁盘 / 内存 / 负载
- 关键业务 endpoint

### 低频（每日 / 每周）
检查：
- 文档漂移
- 未归档项目发现
- 证书有效期
- 变更汇总

## 9.2 后台运行方式
建议使用 OpenClaw cron / 定时工作流。

---

## 10. 初始实施顺序（推荐）

### Phase 1 — 设计落盘
- 建立 `ops-assistant/` 工作区
- 确定权限模型
- 确定告警等级
- 确定 Telegram 为唯一告警渠道

### Phase 2 — 清单与对账
- 建 `managed-hosts.yaml`
- 从 `infra/` 生成首版受管主机清单
- 建 `drift-rules.yaml`

### Phase 3 — 巡检 MVP
优先实现：
- reachability
- docker/systemd inventory
- listening ports
- undocumented project discovery
- Telegram P1/P2 告警

### Phase 4 — 自愈 MVP
先只允许：
- 白名单容器/服务重启
- Gateway restart
- 单次恢复尝试

### Phase 5 — GitHub 私有仓库留痕
- 将 `ops-assistant/` 同步到私有仓库
- 建立标准 commit 规范

---

## 11. 推荐决定（直接可执行）

### 我建议你采用：
1. 当前 OpenClaw 实例内运行
2. 独立 `ops-assistant/` 工作区
3. `infra/` 作为主机知识真源
4. Telegram 作为首个也是唯一告警渠道
5. 严格权限分层
6. 自动巡检 + 白名单自愈 + 全量留痕
7. 后续同步到私有 GitHub 仓库

### 不建议当前就做：
- 告警邮件
- 全自动高风险修复
- 第二套独立 OpenClaw 实例
- 无边界 SSH root 自动运维

---

## 12. 下一步建议

下一步最值得直接落地的是：

1. `managed-hosts.yaml`
2. `permission-model.md`
3. `alert-policy.md`
4. `cron-plan.md`
5. 首版巡检脚本框架

