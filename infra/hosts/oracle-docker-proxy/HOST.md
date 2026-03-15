# oracle-docker-proxy

## 1. Identity
- Host label: `oracle-docker-proxy`
- Static hostname: `Unknown`
- Provider: Likely Oracle Cloud (to be confirmed)
- Primary role: shared Docker/image/UI proxy host
- SSH alias: `Unknown`
- Main purpose: 根据 Cloudflare DNS 导出推测，这台机器承载多个面向容器镜像/代理/UI 的域名入口

## 2. System Baseline
- OS: Unknown
- Kernel: Unknown
- Architecture: Unknown
- CPU: Unknown
- Memory: Unknown
- Swap: Unknown
- Root disk: Unknown

## 3. Usage Pattern
- Host style: Unknown
- Change sensitivity: High (推测多个域名共用同一台主机)
- Operational preference: 先 SSH 核实主机身份、容器/服务分布、端口暴露，再补运维细节

## 4. Access Notes
- Main SSH alias: `Unknown`
- Expected user: `Unknown`
- SSH reachability: host is reachable on SSH, but current attempt with `root@129.150.61.78` failed with `Permission denied (publickey,password)`
- Discovery clue: Cloudflare DNS 中以下域名均指向 `129.150.61.78`
  - `backup.zhangxuemin.work`
  - `elastic.zhangxuemin.work`
  - `gcr.zhangxuemin.work`
  - `ghcr.zhangxuemin.work`
  - `hubcmd.zhangxuemin.work`
  - `hub.zhangxuemin.work`
  - `k8sgcr.zhangxuemin.work`
  - `mcr.zhangxuemin.work`
  - `nvcr.zhangxuemin.work`
  - `quay.zhangxuemin.work`
  - `ui.zhangxuemin.work`

## 5. High-Level Service Map
Not yet documented.

## 6. Machine-Level Infrastructure Notes
- Public IP candidate: `129.150.61.78`
- DNS annotation from export: `docker_proxy`
- This strongly suggests a shared reverse-proxy / registry-proxy / UI host, but exact runtime is not yet confirmed.

## 7. Documentation Scope
待补全：
- SSH 入口与主机基线
- 实际运行项目
- 端口与反代关系
- 数据路径与更新方式
- 这些域名之间的业务拆分
