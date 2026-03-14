# Manual Curation from 52pojie / Kanxue / Related Community Sources

Date: 2026-03-14
Source type: manually provided article collection
Curated by: user
Prepared for: reverse-expert-kb integration

## Provenance
This note records a manually provided community-curated article list spanning:
- 吾爱破解 (52pojie)
- 看雪论坛 (Kanxue)
- related Bilibili / blog / article references

Primary entry references:
- 52pojie forum: https://www.52pojie.cn/
- 52pojie Bilibili: https://space.bilibili.com/544451485?spm_id_from=333.337.0.0
- Kanxue forum: https://bbs.kanxue.com/
- 正己 2595 Bilibili: https://space.bilibili.com/337859280

This is a community-practice source cluster rather than a benchmark or formal academic source set.
Its value is high for:
- practice signals
- workflow patterns
- anti-analysis case studies
- instrumentation tactics
- applied JS/mobile/protocol/anti-tamper material

## Why this source cluster matters
The current KB already has strong structure from framework and synthesis pages.
This source cluster adds something different:
- dense practitioner case studies
- repeated real-target patterns
- tool-and-tactic realism
- anti-analysis and instrumentation details often underrepresented in papers
- high-signal examples for child-page expansion

## Top-level structure of the provided material
The supplied curation naturally clusters into these branches:

1. JS / Web reverse engineering
2. Mobile / Android / iOS reversing
3. Frida / instrumentation / anti-Frida / hook workflows
4. Obfuscation / JSVMP / OLLVM / VMP / flattening / deobfuscation
5. Protocol / traffic / signing / risk-control parameter analysis
6. Firmware- / runtime- / platform-like context and protection concerns
7. Practice-oriented tools, environments, and reverse-engineering workflow notes

## A. JS / Web reverse engineering cluster
Representative items from the provided list include:
- 某当网登录滑块逆向
- 某航司 Reese84 逆向分析-补环境篇
- 某美验证码及风控浅析
- 巧用 Chrome-CDP 远程调用 Debug 突破 JS 逆向
- 某 q 音乐 jsvmp 反编译
- 在 nodejs 环境中复用 webpack 代码
- boss 直聘 __zp_stoken__ 控制流平坦化逆向
- 某程 token jsvmp 算法分析
- 某盾无感验证码逆向
- 某验 3 AST 分析及实现
- 顶象滑块验证码纯算逆向分析
- 某手势验证码纯算逆向分析
- 深入浅出 JSVMP
- 某里新版 acw_sc__v2 算法分析
- 某 d 的 _fingerprint 参数生成 / vmp 套 vmp
- 雷池 WAF 滑块版本逆向分析
- 点选验证码识别通用解决方案
- Reese84 / ___utmvc 逆向流程分析
- 某老板直聘四层 switch 反混淆
- 某音 jsvmp AST 还原
- WebSocket 通信逆向实战
- 某乎 __zse_ck 参数 js + wasm 多重套娃
- wasm 转 C 调用实战 / 封装到 dll
- JavaScript AST 基础与环境配置
- Tbooking 验证码逆向分析
- 某雷云盘验证码逆向思路总结
- 给某讯滑块 JSVMP 写反编译器
- Web / JS 逆向基础：V8 / JS / AST
- 什么是 (JS)VMP
- cctv 视频解密，wasm vmp 分析

### Practice signals from this cluster
This cluster strongly reinforces several KB themes:
- JS/web RE often centers on runtime answerability and environment recreation
- AST manipulation is a major practical deobfuscation workflow
- JSVMP and control-flow flattening are recurring real-world protection patterns
- browser/CDP-assisted workflows matter as much as pure static reading
- captcha/risk-control analysis often combines protocol, runtime, and deobfuscation concerns
- wasm increasingly appears as a practical sub-branch of modern web reverse engineering

### Best KB mappings
This cluster maps most strongly to:
- `topics/runtime-behavior-recovery.md`
- `topics/obfuscation-deobfuscation-and-packed-binaries.md`
- `topics/anti-tamper-and-protected-runtime-analysis.md`
- `topics/protocol-state-and-message-recovery.md`

Potential future child pages suggested by this cluster:
- JS / browser runtime reversing
- JSVMP and AST-based devirtualization
- captcha / risk-control workflow patterns
- wasm-assisted web reverse engineering

## B. Mobile / Android / iOS reversing cluster
Representative items from the provided list include:
- 《安卓逆向这档事》模拟器环境搭建
- frida-java 源码阅读
- frida 笔记 / objection 用法 / hook so 方法大全
- 多篇 Android 逆向学习与 app 算法分析
- Unity / IL2Cpp / 存档解密 / 加固分析
- VMOS Pro 破解分析
- Frida 脚本持久化 / Xposed 模块 / 注入方案
- arm so 加载 / gojni 协议 / so 层动态调试
- libmsaoaidsec.so 反 Frida
- 安卓加壳 / 脱壳 / 加固原理
- iOS Wtoken / iOS 越狱检测 / iOS 逆向环境搭建
- 《挑战不用 macOS 逆向 iOS APP》系列
- Android 设备指纹 / 环境检测 / Warlock / Fireyer
- Binder 拦截 / eBPF / dlopen 限制 / linker / 签名校验 / so 加壳
- 某老牌反作弊产品分析
- frida 检测与绕过
- 某外卖 / 生鲜 / 金融 / 短视频等 app 风控与算法分析
- iOS 应用逆向攻防实战
- Pixel 6 安卓15 eBPF 环境
- [iOS逆向] Frida反检测绕过 + VIP解锁 + Theos 插件制作
- 从 App 启动流程看 Android 整体加固
- 整体加固 Demo 及加壳工具编写

### Practice signals from this cluster
This cluster strongly reinforces that:
- mobile RE is heavily workflow- and instrumentation-driven
- anti-Frida / anti-hook / environment detection are first-class real-world constraints
- Android reversing spans Java, ART, JNI, linker, Binder, ELF, eBPF, and whole-app protection layers
- iOS reversing is deeply tied to environment setup, jailbreak detection, resigning, and runtime checks
- Unity/IL2Cpp and mobile game protection are recurring practical subdomains
- app protocol/signature/risk-control analysis often blends protocol RE, runtime observation, and protected-runtime tactics

### Best KB mappings
This cluster maps most strongly to:
- `topics/mobile-reversing-and-runtime-instrumentation.md`
- `topics/runtime-behavior-recovery.md`
- `topics/anti-tamper-and-protected-runtime-analysis.md`
- `topics/obfuscation-deobfuscation-and-packed-binaries.md`
- `topics/notebook-and-memory-augmented-re.md` (for long-horizon applied workflows)

Potential future child pages suggested by this cluster:
- Android anti-Frida and anti-hook practice
- iOS environment control and detection bypass
- Unity / IL2Cpp reversing
- Android linker / Binder / eBPF-assisted reversing
- app signing / risk-control / protocol casework

## C. Kanxue practitioner cluster
Representative items from the provided list include:
- 指纹浏览器编译与开发
- 魔改 chromium / debugger / CDP 对抗检测
- 风控参数分析 / 设备风控 / 设备信息 SDK 分析
- VMP 样本分析 / Android ARM64 VMP / 手搓 VMP
- 安卓逆向核心流程
- trace 绕过 CRC / CRC 原理与绕过
- OLLVM / 字符串加密 / 反混淆 / microcode / 状态机视角
- IDA 插件 / MCP / 动态调试环境 / 反编译引擎模块
- Frida 自编译去特征 / 常见检测与绕过 / libmsaoaidsec.so 绕过
- Linker / SO 加密 / GNUHash / SO 加固 / SO 脱壳
- seccomp / ptrace / SVC tracehook / Zygisk / 注入 / 无痕 hook
- QBDI / Unicorn / dynamic binary instrumentation / VMLifter
- Swift / iOS 重签名检测 / iOS Frida trace
- BPF / sandbox 对抗 / protected SDK analysis
- AI + IDA Pro MCP / VMP 手动分析与 AI 还原

### Practice signals from this cluster
This cluster strongly reinforces:
- anti-analysis is a major practitioner axis, not a niche corner
- VMP / OLLVM / SO 加固 / hook 对抗 / trace 工具 是持续高频主题
- tool-building and workflow augmentation are central to expert practice
- dynamic instrumentation and lifting frameworks (QBDI, Unicorn, VMLifter, trace tools) are operationally important
- Chromium / CDP / debugger detection is a live browser-reversing topic
- AI-assisted RE is already entering community workflows

### Best KB mappings
This cluster maps most strongly to:
- `topics/anti-tamper-and-protected-runtime-analysis.md`
- `topics/obfuscation-deobfuscation-and-packed-binaries.md`
- `topics/runtime-behavior-recovery.md`
- `topics/analyst-workflows-and-human-llm-teaming.md`
- `topics/decompilation-and-code-reconstruction.md`

Potential future child pages suggested by this cluster:
- DBI / trace-guided reverse engineering
- anti-debug / anti-instrumentation practice taxonomy
- browser / CDP / debugger-detection reversing
- AI-assisted deobfuscation and lifting workflows

## D. High-value recurring motifs across the entire manually curated list
Across 52pojie and Kanxue, several motifs recur with striking frequency:

### 1. Runtime evidence beats static elegance in many practical targets
Repeated examples involve:
- Frida
- tracing
- CDP
- live hook strategies
- environment recreation
- dynamic bypass and observation

This strongly reinforces:
- `topics/runtime-behavior-recovery.md`
- `topics/mobile-reversing-and-runtime-instrumentation.md`

### 2. Protected runtimes are a mainstream reality
Repeated examples involve:
- anti-Frida
- anti-debug
- CRC / integrity checks
- hook detection
- sandbox / environment detection
- signing / jailbreak / root checks
- SO / VMP / OLLVM protection

This strongly reinforces:
- `topics/anti-tamper-and-protected-runtime-analysis.md`
- `topics/obfuscation-deobfuscation-and-packed-binaries.md`

### 3. Deobfuscation is often workflowed through AST / traces / microcode / tool augmentation
Repeated examples involve:
- AST transforms
- JSVMP devirtualization
- OLLVM flattening recovery
- microcode-based reasoning
- trace-guided lifting

This strongly reinforces:
- `topics/obfuscation-deobfuscation-and-packed-binaries.md`
- `topics/decompilation-and-code-reconstruction.md`

### 4. Protocol and risk-control analysis are central applied tasks
Repeated examples involve:
- signing parameters
- captcha flows
- traffic / jce / websocket / app protocol analysis
- device fingerprint and environment checks

This strongly reinforces:
- `topics/protocol-state-and-message-recovery.md`
- `topics/firmware-and-protocol-context-recovery.md` (where environment context matters)

### 5. Community sources are especially valuable for child-page expansion candidates
This source cluster is likely to be most useful for future child pages rather than only for parent-page justification.

## Suggested integration actions
Based on the current KB structure, this manual source cluster should be used in three ways.

### 1. As a practitioner-source backbone
Use it to deepen the practice-oriented sections of:
- runtime behavior recovery
- mobile reversing and instrumentation
- anti-tamper / protected-runtime analysis
- obfuscation / deobfuscation / packed binaries
- protocol state and message recovery

### 2. As pressure for future child pages
It strongly suggests the following child pages are worth creating later:
- JS / browser runtime reversing
- JSVMP and AST devirtualization
- anti-Frida and anti-instrumentation practice
- Android linker / Binder / eBPF reversing
- DBI / trace-guided reverse engineering
- Unity / IL2Cpp practice notes
- risk-control and fingerprint protocol analysis

### 3. As a contrastive evidence source
These sources should not replace formal papers or benchmark pages.
Instead they should complement them by adding:
- operational realism
- workflow details
- tool friction
- real anti-analysis conditions
- practice-derived heuristics

## Caveats
This source cluster is valuable, but it is not homogeneous.

Caveats include:
- uneven rigor and reproducibility
- variable depth and writing quality
- domain-specific bias toward popular Chinese practice targets
- occasional overlap with offensive scraping / bypass casework that should be framed carefully inside the KB
- duplicate links and partially overlapping topic boundaries in the supplied list

Therefore, this cluster should be treated as:
- high-value practitioner evidence
- high-value topic-expansion fuel
- not as a benchmark or canonical ground-truth layer by itself

## Bottom line
This manually curated 52pojie / Kanxue source cluster substantially increases the KB’s practice realism.

Its strongest contribution is not broad theory, but repeated concrete evidence that expert reverse engineering in the wild is heavily shaped by:
- runtime observation
- anti-analysis pressure
- deobfuscation workflows
- mobile instrumentation
- protocol and risk-control analysis
- tool-assisted, long-horizon reasoning

That makes it one of the most valuable practitioner-source clusters currently available to this KB.