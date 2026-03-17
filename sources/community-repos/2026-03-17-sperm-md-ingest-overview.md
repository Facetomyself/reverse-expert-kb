# Source Overview — 2026-03-17 — `Facetomyself/sperm` `md/` manual ingest

## Source
- Repository: <https://github.com/Facetomyself/sperm>
- Scoped path: <https://github.com/Facetomyself/sperm/tree/main/md>
- Acquisition mode: manual targeted ingest overview
- Snapshot method: shallow sparse clone of `md/`
- Total Markdown files observed: **173**

## Why this source matters
This repository looks less like one tightly-authored monograph and more like a **curated accumulation of practical reversing writeups**, especially around:
- Android app reversing
- Frida / hook / observation-surface practice
- JS / browser-side anti-bot and environment patching
- VM / OLLVM / mixed protected-runtime cases
- protocol and network-side app analysis
- smaller numbers of iOS and native-basics notes

That makes it useful as a **feeder source** for practical workflow extraction, even when individual articles vary in depth, style, or originality.

## Top-level shape
- Android / mobile-heavy material dominates the corpus
- strong overlap between instrumentation and Android practical reversing
- browser / JS anti-bot content is present and likely high-yield for the existing browser-runtime subtree
- protected-runtime / VM / obfuscation content is substantial enough to mine for concrete workflow notes
- protocol/network material exists but is comparatively smaller
- iOS material exists but is relatively sparse

## Preliminary bucket summary
## android-mobile (101)
- simpread-09 - How to use frida on a non-rooted device — LIEF Documentation.md
- simpread-2022 某安卓 Crackme 流程分析.md
- simpread-2024 腾讯游戏安全大赛 - 安卓赛道决赛 VM 分析与还原.md
- simpread-APP 渗透 _ 安服仔们又稳了! 过爱 _ 梆企业版初级反调的 Frida 检测（含脚本）.md
- simpread-APP 逆向工程技巧——反调试检测线程.md
- simpread-Android Hook 技术学习——常见的 Hook 技术方案总结.md
- simpread-Android 加固 little 总结.md
- simpread-App 逆向百例 _ 16 _ 某交友 App 花指令分析.md
- simpread-App 逆向百例 _ 18 _ 某 A 系防护 SO 跳转修复.md
- simpread-App 逆向百例 _ 19 _ 某 App Sign 完整分析.md
- simpread-Flutter Android APP 逆向系列 (一) _ Dawnnnnnn.md
- simpread-Frida + AndroidAsync 实现 RPC  - 奋飞安全.md
- simpread-Frida Android hook _ Sakura の blog.md
- simpread-Frida 工作原理学习（1）.md
- simpread-Frida 演示之某阅读 APP 解密分析.md
- simpread-M3U8 涉黄 APP 取证分析实战.md
- simpread-Protobuf 协议逆向解析 - APP 爬虫 .md
- simpread-[入门级] 移动安全逆向 hook 操作整理 v1.0.md
- simpread-[原创] 基于 trace 内存爆破标准算法 - Android 安全 - 看雪论坛 - 安全社区 _ 非营利性质技术交流社区.md
- simpread-[原创] 搜狗搜索 app so 加解密分析.md
- ... 另有 81 篇

## browser-web-js (31)
- simpread-2025 第三届 - JS 逆向 & 验证码比赛 (混淆）第二题 纯算首发.md
- simpread-Canvas 指纹隐藏实战.md
- simpread-JS 逆向 _ 某行业大佬对坑风控的一些经验总结.md
- simpread-JS 逆向系列 22 - 彻底解决前端无限 debugger.md
- simpread-Js Ast 一部曲：高完整度还原某 V5 的加密.md
- simpread-Js Ast 二部曲：某 V5 “绝对不可逆加密” 一探究竟.md
- simpread-Python 爬虫进阶必备 _ Js 逆向之补环境到底是在补什么？.md
- simpread-[原创]（随笔）有风控 & 无风控 App 对抗深入浅出.md
- simpread-[验证码识别] 易盾空间推理验证码识别详细流程.md
- simpread-ast 自动扣 webpack 脚本实战_渔滒的博客 - CSDN 博客.md
- simpread-cloudflare 五秒盾 js 逆向分析.md
- simpread-curl_cffi 突破 Cloudflare 验证.md
- simpread-js 破解之补浏览器环境的两种监控方式.md
- simpread-js 逆向 --jsl mfw.md
- simpread-js 逆向) 某音 cookie 中的__ac_signature.md
- simpread-js 逆向之模拟浏览器环境 _ 范昌锐的博客.md
- simpread-【网页逆向】chan 妈妈滑块 ast 反混淆.md
- simpread-【验证码识别专栏】人均通杀点选验证码！Yolov5 + 孪生神经网络 or 图像分类 = 高精模型.md
- simpread-人均瑞数系列，瑞数 4 代 JS 逆向分析.md
- simpread-人均瑞数系列，瑞数 5 代 JS 逆向分析.md
- ... 另有 11 篇

## obfuscation-protected-runtime (38)
- simpread-2024 腾讯游戏安全大赛 - 安卓赛道决赛 VM 分析与还原.md
- simpread-2025 第三届 - JS 逆向 & 验证码比赛 (混淆）第二题 纯算首发.md
- simpread-App 逆向百例 _ 16 _ 某交友 App 花指令分析.md
- simpread-DFA 还原白盒 AES 密钥.md
- simpread-Js Ast 一部曲：高完整度还原某 V5 的加密.md
- simpread-Js Ast 二部曲：某 V5 “绝对不可逆加密” 一探究竟.md
- simpread-SM4-DFA 攻击.md
- simpread-VM 逆向，一篇就够了.md
- simpread-VM 逆向，一篇就够了（下）.md
- simpread-elf 修复的杂糅分析笔记.md
- simpread-k 手花指令分析理解.md
- simpread-x-zse-96 安卓端纯算, 魔改 AES.md
- simpread-x-zse-96,android 端, 伪 dex 加固, so 加固, 白盒 AES, 字符串加密.md
- simpread-xx 度灰 app 加密算法分析还原 - 『移动安全区』  - 吾爱破解 - LCG - LSG _ 安卓破解 _ 病毒分析 _ www.52pojie.cn.md
- simpread-【iOS 逆向】iOS 某大厂 vmp 参数还原.md
- simpread-【iOS 逆向】某音乐 sign 分析 - 过 ollvm 与花指令.md
- simpread-【网页逆向】chan 妈妈滑块 ast 反混淆.md
- simpread-一文搞懂花指令的原理、识别与去除.md
- simpread-使用 Unidbg 模拟执行去除 OLLVM-BR 混淆.md
- simpread-初探 android crc 检测及绕过.md
- ... 另有 18 篇

## instrumentation-observation (37)
- simpread-09 - How to use frida on a non-rooted device — LIEF Documentation.md
- simpread-APP 渗透 _ 安服仔们又稳了! 过爱 _ 梆企业版初级反调的 Frida 检测（含脚本）.md
- simpread-APP 逆向工程技巧——反调试检测线程.md
- simpread-Android Hook 技术学习——常见的 Hook 技术方案总结.md
- simpread-Frida + AndroidAsync 实现 RPC  - 奋飞安全.md
- simpread-Frida Android hook _ Sakura の blog.md
- simpread-Frida 工作原理学习（1）.md
- simpread-Frida 演示之某阅读 APP 解密分析.md
- simpread-JS 逆向系列 22 - 彻底解决前端无限 debugger.md
- simpread-[入门级] 移动安全逆向 hook 操作整理 v1.0.md
- simpread-[原创] 基于 trace 内存爆破标准算法 - Android 安全 - 看雪论坛 - 安全社区 _ 非营利性质技术交流社区.md
- simpread-[原创] 记一次 unicorn 半自动化逆向——还原某东 sign 算法.md
- simpread-[原创][分享]fridaserver 去特征检测以及编译.md
- simpread-frida _ 凡墙总是门-so.md
- simpread-frida 免 root hook.md
- simpread-frida 检测.md
- simpread-frida 的配置与使用 (从 0 到 hook tb签名算法） - 早苗の魔导典.md
- simpread-iphone8p 到手，10 分钟搞定越狱 + frida 环境.md
- simpread-【APP 逆向百例】某当劳 Frida 检测.md
- simpread-【安卓逆向】安居客反调试与参数分析.md
- ... 另有 17 篇

## protocol-network (14)
- simpread-M3U8 涉黄 APP 取证分析实战.md
- simpread-Protobuf 协议逆向解析 - APP 爬虫 .md
- simpread-分析 okhttp3-retrofit2 - 截流某音通信数据.md
- simpread-好库推荐 _ 两个解决 ja3 检测的 Python 库，强烈推荐.md
- simpread-某某 App protobuf 协议逆向分析.md
- simpread-某某网站 JS 逆向及 tls 指纹绕过分析.md
- simpread-某电子书阅读器加密协议分析.md
- simpread-某车联网 App 通讯协议加密分析 (三) Trace Block.md
- simpread-深度剖析 ja3 指纹及突破.md
- simpread-猿人学 - app 逆向比赛第四题 grpc 题解.md
- simpread-猿人学 2022 逆向比赛第七题 quic.md
- simpread-现代 Web 自动化核心：从 CDP 协议到高级反检测策略.md
- simpread-突破 tls_ja3 新轮子.md
- simpread-逆向某短视频 App 搜索协议：破解加密通信，还原真实数据！.md

## mobile-ios (8)
- simpread-iphone8p 到手，10 分钟搞定越狱 + frida 环境.md
- simpread-【iOS 逆向】iOS 某大厂 vmp 参数还原.md
- simpread-【iOS 逆向】某音乐 sign 分析 - 过 ollvm 与花指令.md
- simpread-【iOS-Flutter 逆向】__ 岛之踩坑记录篇.md
- simpread-在非越狱 iOS 上实现全流量抓包.md
- simpread-某手 sig3-ios 算法 Chomper 黑盒调用.md
- simpread-某红书 Shield 算法 Chomper 黑盒调用.md
- simpread-移动安全之 IOS 逆向越狱环境准备 (上).md

## asm-native-basics (6)
- simpread-arm 中的多寄存器寻址和与堆栈寻址.md
- simpread-arm 中的溢出和进位.md
- simpread-arm 汇编学习（一） _ Sakura の blog.md
- simpread-一文弄懂 arm 中立即数.md
- simpread-在静态分析、计算 arm64 汇编时提速.md
- simpread-字节对齐.md

## uncategorized (20)
- simpread-BYD 分析 _ Notion Blog.md
- simpread-IO 重定位简单实现和对抗.md
- simpread-Proxy 代理（二次修改）.md
- simpread-Tiny 去花小记 (上）.md
- simpread-Tiny 去花小记 (下）.md
- simpread-VX 小程序逆向分析.md
- simpread-X-Argus 逆向分析.md
- simpread-getByte 算法分析与还原 - SeeFlowerX.md
- simpread-tiktok 系列文章 - device_register（2）.md
- simpread-一文掌握 IDA Pro MCP 逆向分析利器.md
- simpread-某乎请求头签名算法分析.md
- simpread-某招聘网站 202312 月新版 token 生成分析.md
- simpread-某盾设备指纹算法分析.md
- simpread-某蜂窝 zzzghostsigh 补环境 + 纯算.md
- simpread-某黑盒样本案例分析.md
- simpread-浅谈某短视频的 sig4 纯算思路.md
- simpread-浅谈设备指纹技术和应用.md
- simpread-猿人学第五题 - 双向认证分享.md
- simpread-用 Scrapy 爬取 5 秒盾站点，结果万万没想到，速度可以这么快！.md
- simpread-聊聊大厂设备指纹获取和对抗 & 设备指纹看着一篇就够了!.md

## High-signal candidates for later deep extraction
These are not yet canonicalized; they are just likely-good follow-up candidates for a second pass:
- simpread-2024 腾讯游戏安全大赛 - 安卓赛道决赛 VM 分析与还原.md
- simpread-VM 逆向，一篇就够了.md
- simpread-VM 逆向，一篇就够了（下）.md
- simpread-从 trace 到二进制插桩到 Frida.md
- simpread-分享一个 Android 通用 svc 跟踪以及 hook 方案——Frida-Seccomp.md
- simpread-当 Xiaomi 12 遇到 eBPF.md
- simpread-现代 Web 自动化核心：从 CDP 协议到高级反检测策略.md
- simpread-cloudflare 五秒盾 js 逆向分析.md
- simpread-curl_cffi 突破 Cloudflare 验证.md
- simpread-Python 爬虫进阶必备 _ Js 逆向之补环境到底是在补什么？.md
- simpread-Protobuf 协议逆向解析 - APP 爬虫 .md
- simpread-某某 App protobuf 协议逆向分析.md
- simpread-猿人学 2022 逆向比赛第七题 quic.md
- simpread-【iOS 逆向】iOS 某大厂 vmp 参数还原.md
- simpread-在非越狱 iOS 上实现全流量抓包.md

## Ingest recommendation
This source should be treated as a **batch source reservoir**, not blindly merged into canonical topic pages.

Recommended next passes:
1. extract and summarize the strongest Android/protected-runtime workflow articles first
2. separately mine browser/JS anti-bot and environment-patching articles into browser subtree source notes
3. treat generic setup/basics posts as supporting background rather than canonical KB drivers
4. prefer creating compact source-note bundles by subtheme instead of one note per article unless an article is unusually strong

## Full observed file manifest
- simpread-09 - How to use frida on a non-rooted device — LIEF Documentation.md
- simpread-2022 某安卓 Crackme 流程分析.md
- simpread-2024 腾讯游戏安全大赛 - 安卓赛道决赛 VM 分析与还原.md
- simpread-2025 第三届 - JS 逆向 & 验证码比赛 (混淆）第二题 纯算首发.md
- simpread-APP 渗透 _ 安服仔们又稳了! 过爱 _ 梆企业版初级反调的 Frida 检测（含脚本）.md
- simpread-APP 逆向工程技巧——反调试检测线程.md
- simpread-Android Hook 技术学习——常见的 Hook 技术方案总结.md
- simpread-Android 加固 little 总结.md
- simpread-App 逆向百例 _ 16 _ 某交友 App 花指令分析.md
- simpread-App 逆向百例 _ 18 _ 某 A 系防护 SO 跳转修复.md
- simpread-App 逆向百例 _ 19 _ 某 App Sign 完整分析.md
- simpread-BYD 分析 _ Notion Blog.md
- simpread-Canvas 指纹隐藏实战.md
- simpread-DFA 还原白盒 AES 密钥.md
- simpread-Flutter Android APP 逆向系列 (一) _ Dawnnnnnn.md
- simpread-Frida + AndroidAsync 实现 RPC  - 奋飞安全.md
- simpread-Frida Android hook _ Sakura の blog.md
- simpread-Frida 工作原理学习（1）.md
- simpread-Frida 演示之某阅读 APP 解密分析.md
- simpread-IO 重定位简单实现和对抗.md
- simpread-JS 逆向 _ 某行业大佬对坑风控的一些经验总结.md
- simpread-JS 逆向系列 22 - 彻底解决前端无限 debugger.md
- simpread-Js Ast 一部曲：高完整度还原某 V5 的加密.md
- simpread-Js Ast 二部曲：某 V5 “绝对不可逆加密” 一探究竟.md
- simpread-M3U8 涉黄 APP 取证分析实战.md
- simpread-Protobuf 协议逆向解析 - APP 爬虫 .md
- simpread-Proxy 代理（二次修改）.md
- simpread-Python 爬虫进阶必备 _ Js 逆向之补环境到底是在补什么？.md
- simpread-SM4-DFA 攻击.md
- simpread-Tiny 去花小记 (上）.md
- simpread-Tiny 去花小记 (下）.md
- simpread-VM 逆向，一篇就够了.md
- simpread-VM 逆向，一篇就够了（下）.md
- simpread-VX 小程序逆向分析.md
- simpread-X-Argus 逆向分析.md
- simpread-[入门级] 移动安全逆向 hook 操作整理 v1.0.md
- simpread-[原创] 基于 trace 内存爆破标准算法 - Android 安全 - 看雪论坛 - 安全社区 _ 非营利性质技术交流社区.md
- simpread-[原创] 搜狗搜索 app so 加解密分析.md
- simpread-[原创] 某 app 加固逆向分析 - Android 安全 - 看雪 - 安全社区 _ 安全招聘 _ kanxue.com.md
- simpread-[原创] 记一次 unicorn 半自动化逆向——还原某东 sign 算法.md
- simpread-[原创][分享]fridaserver 去特征检测以及编译.md
- simpread-[原创]android 抓包学习的整理和归纳.md
- simpread-[原创]（随笔）有风控 & 无风控 App 对抗深入浅出.md
- simpread-[验证码识别] 易盾空间推理验证码识别详细流程.md
- simpread-android 安全启动验证链.md
- simpread-app 逆向 平头哥实战（某农产品 app）.md
- simpread-arm 中的多寄存器寻址和与堆栈寻址.md
- simpread-arm 中的溢出和进位.md
- simpread-arm 汇编学习（一） _ Sakura の blog.md
- simpread-ast 自动扣 webpack 脚本实战_渔滒的博客 - CSDN 博客.md
- simpread-b 站 app 漫展抢票 _ oacia = oacia の BbBlog~ = DEVIL or SWEET.md
- simpread-cloudflare 五秒盾 js 逆向分析.md
- simpread-curl_cffi 突破 Cloudflare 验证.md
- simpread-elf 修复的杂糅分析笔记.md
- simpread-frida _ 凡墙总是门-so.md
- simpread-frida 免 root hook.md
- simpread-frida 检测.md
- simpread-frida 的配置与使用 (从 0 到 hook tb签名算法） - 早苗の魔导典.md
- simpread-getByte 算法分析与还原 - SeeFlowerX.md
- simpread-iphone8p 到手，10 分钟搞定越狱 + frida 环境.md
- simpread-iptables 在 Android 抓包中的妙用.md
- simpread-js 破解之补浏览器环境的两种监控方式.md
- simpread-js 逆向 --jsl mfw.md
- simpread-js 逆向) 某音 cookie 中的__ac_signature.md
- simpread-js 逆向之模拟浏览器环境 _ 范昌锐的博客.md
- simpread-k 手花指令分析理解.md
- simpread-sign 参数分析.md
- simpread-tiktok 系列文章 - device_register（2）.md
- simpread-unidbg 算法还原术 · 某民宿 app 篇 · 上卷.md
- simpread-unidbg 算法还原术 · 某民宿 app 篇 · 下卷.md
- simpread-unidbg 算法还原术 · 某民宿 app 篇 · 中卷.md
- simpread-unidbg 调用 sgmain 的 doCommandNative 函数生成某酷 encryptR_client 参数.md
- simpread-x-zse-96 安卓端纯算, 魔改 AES.md
- simpread-x-zse-96,android 端, 伪 dex 加固, so 加固, 白盒 AES, 字符串加密.md
- simpread-xx 度灰 app 加密算法分析还原 - 『移动安全区』  - 吾爱破解 - LCG - LSG _ 安卓破解 _ 病毒分析 _ www.52pojie.cn.md
- simpread-《安卓逆向这档事》番外实战篇 3 - 拨云见日之浅谈 Flutter 逆向.md
- simpread-【2021 春节】安卓中级题逆向总结.md
- simpread-【APP 逆向百例】某品会 app 逆向分析.md
- simpread-【APP 逆向百例】某当劳 Frida 检测.md
- simpread-【APP 逆向百例】某瓣 app 逆向分析.md
- simpread-【APP 逆向百例】某蜂窝逆向分析.md
- simpread-【Fireyer】一款 Android 平台环境检测应用 _ iofomo _ Open-source organization.md
- simpread-【iOS 逆向】iOS 某大厂 vmp 参数还原.md
- simpread-【iOS 逆向】某音乐 sign 分析 - 过 ollvm 与花指令.md
- simpread-【iOS-Flutter 逆向】__ 岛之踩坑记录篇.md
- simpread-【安卓逆向】安居客反调试与参数分析.md
- simpread-【网页逆向】chan 妈妈滑块 ast 反混淆.md
- simpread-【转载】Unidbg Hook 大全 - SeeFlowerX.md
- simpread-【验证码识别专栏】人均通杀点选验证码！Yolov5 + 孪生神经网络 or 图像分类 = 高精模型.md
- simpread-一文弄懂 arm 中立即数.md
- simpread-一文掌握 IDA Pro MCP 逆向分析利器.md
- simpread-一文搞懂花指令的原理、识别与去除.md
- simpread-人均瑞数系列，瑞数 4 代 JS 逆向分析.md
- simpread-人均瑞数系列，瑞数 5 代 JS 逆向分析.md
- simpread-从 trace 到二进制插桩到 Frida.md
- simpread-使用 Unidbg 模拟执行去除 OLLVM-BR 混淆.md
- simpread-使用 Xposed 进行微信小程序 API 的 hook _ AshenOne.md
- simpread-修改 6 字节打开微信内置浏览器的 F12 - SeeFlowerX.md
- simpread-分享一个 Android 通用 svc 跟踪以及 hook 方案——Frida-Seccomp.md
- simpread-分析 okhttp3-retrofit2 - 截流某音通信数据.md
- simpread-初探 android crc 检测及绕过.md
- simpread-在静态分析、计算 arm64 汇编时提速.md
- simpread-在非越狱 iOS 上实现全流量抓包.md
- simpread-多种姿势花样使用 Frida 注入 _ AshenOne.md
- simpread-大猿搜题 sign so 加密参数分析｜unidbg.md
- simpread-好库推荐 _ 两个解决 ja3 检测的 Python 库，强烈推荐.md
- simpread-如何在 vmp 中找到查表 aes 的密钥.md
- simpread-如何实现 Android App 的抓包防护？又该如何绕过？一文看懂攻防博弈 __ CYRUS STUDIO.md
- simpread-字节对齐.md
- simpread-字节系, ali 系, ks,pdd 最新抓包方案.md
- simpread-安卓 Svc 穿透获取设备信息 - 简书.md
- simpread-安卓上基于透明代理对特定 APP 抓包 - SeeFlowerX.md
- simpread-对 APP 逆向抓包的实践.md
- simpread-对 Flutter 开发的某 App 逆向分析.md
- simpread-对旅行 APP 的检测以及参数计算分析【Simplesign 篇】.md
- simpread-广东的 vmp 大致分析.md
- simpread-当 Xiaomi 12 遇到 eBPF.md
- simpread-快手花指令实战分析.md
- simpread-所有无限 debugger 的原理与绕过.md
- simpread-手把手教你用 Chrome 断点调试 Frida 脚本，JS 调试不再是黑盒.md
- simpread-抖音抓包.md
- simpread-控制流平坦化反混淆（春节红包活动 Android 高级题） - 『移动安全区』  - 吾爱破解 - LCG - LSG _ 安卓破解 _ 病毒分析 _ www.52pojie.cn.md
- simpread-携程抓包.md
- simpread-新版 a+1 站 ollvm 算法分析.md
- simpread-某 A 系电商 App doCommandNative 浅析.md
- simpread-某 A 系电商 App x-sign 签名分析.md
- simpread-某乎请求头签名算法分析.md
- simpread-某买菜 app 加密浅析及 excel 初体验.md
- simpread-某咖啡 app 加密参数分析进阶版.md
- simpread-某小程序平台桌面版开启 js 调试.md
- simpread-某手 sig3-ios 算法 Chomper 黑盒调用.md
- simpread-某手抓包问题分析.md
- simpread-某招聘网站 202312 月新版 token 生成分析.md
- simpread-某某 App protobuf 协议逆向分析.md
- simpread-某某网站 JS 逆向及 tls 指纹绕过分析.md
- simpread-某查线路 app 设备检测逆向分析.md
- simpread-某瑞数 5 代 cookie 和 url 后缀补环境代码.md
- simpread-某电子书阅读器加密协议分析.md
- simpread-某盾设备指纹算法分析.md
- simpread-某红书 Shield 算法 Chomper 黑盒调用.md
- simpread-某蜂窝 zzzghostsigh 补环境 + 纯算.md
- simpread-某车联网 App 通讯协议加密分析 (三) Trace Block.md
- simpread-某音乐 app ollvm 算法分析.md
- simpread-某风控 SDK 逆向分析 _ AshenOne.md
- simpread-某黑盒样本案例分析.md
- simpread-注入 frida-gadget 绕过 Frida 检测.md
- simpread-浅析 APP 代理检测对抗 - 先知社区.md
- simpread-浅谈某短视频的 sig4 纯算思路.md
- simpread-浅谈设备指纹技术和应用.md
- simpread-深度剖析 ja3 指纹及突破.md
- simpread-渣浪的 S 参数分析.md
- simpread-爬虫之 - 某生鲜 APP 加密参数逆向分析.md
- simpread-猿人学 - app 逆向比赛第四题 grpc 题解.md
- simpread-猿人学 2022 逆向比赛第七题 quic.md
- simpread-猿人学安卓逆向抓取比赛 - 第六题算法分析还原.md
- simpread-猿人学第五题 - 双向认证分享.md
- simpread-现代 Web 自动化核心：从 CDP 协议到高级反检测策略.md
- simpread-用 Scrapy 爬取 5 秒盾站点，结果万万没想到，速度可以这么快！.md
- simpread-监控、定位 JavaScript 操作 cookie - 『脱壳破解区』  - 吾爱破解 - LCG - LSG _ 安卓破解 _ 病毒分析 _ www.52pojie.cn.md
- simpread-移动安全之 IOS 逆向越狱环境准备 (上).md
- simpread-突破 tls_ja3 新轮子.md
- simpread-绕过 libxxxxsec.so 对 Frida hook Java 层的检测.md
- simpread-聊聊大厂设备指纹获取和对抗 & 设备指纹看着一篇就够了!.md
- simpread-记一次 tiktok 抓包过程.md
- simpread-记一次汽车 app 白盒 aes 还原过程.md
- simpread-过某加固 Frida 检测.md
- simpread-还原某里 226 控制流混淆的思路 - 『脱壳破解区』  - 吾爱破解 - LCG - LSG _ 安卓破解 _ 病毒分析 _ www.52pojie.cn.md
- simpread-逆向分析反调试 + ollvm 混淆的 Crackme.md
- simpread-逆向某物 App 登录接口：抓包分析 + Frida Hook 还原加密算法.md
- simpread-逆向某物 App 登录接口：还原 newSign 算法全流程.md
- simpread-逆向某短视频 App 搜索协议：破解加密通信，还原真实数据！.md
- simpread-隐藏 Root - Zygisk 版面具 Magisk 过银行 App 等 Root 检测，Shamiko 模块的妙用 - 哔哩哔哩.md
- simpread-非 root 环境下 frida 的两种使用方式 · nszdhd1's blog.md
