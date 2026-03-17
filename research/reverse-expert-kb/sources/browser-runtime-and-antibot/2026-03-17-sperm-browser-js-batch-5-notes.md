# Source Notes — 2026-03-17 — `sperm/md` Browser / JS anti-bot batch 5

## Source set
Primary repository reservoir:
- <https://github.com/Facetomyself/sperm/tree/main/md>

Articles closely reviewed in this batch:
- `simpread-2025 第三届 - JS 逆向 & 验证码比赛 (混淆）第二题 纯算首发.md`
- `simpread-[验证码识别] 易盾空间推理验证码识别详细流程.md`
- `simpread-【验证码识别专栏】人均通杀点选验证码！Yolov5 + 孪生神经网络 or 图像分类 = 高精模型.md`
- `simpread-修改 6 字节打开微信内置浏览器的 F12 - SeeFlowerX.md`
- `simpread-某小程序平台桌面版开启 js 调试.md`

One intended automation article path did not resolve in this batch, but the remaining sources were sufficient for a coherent extraction.

## Why these articles were grouped together
This batch coheres around one practical branch:
- **many browser-side challenges that look like “human interaction” are better solved by restoring observability and then reducing the task into artifact generation, prompt interpretation, or model-friendly image reasoning pipelines**

The subthemes are:
- slider/captcha “纯算” recovery via instruction/log analysis
- point-and-click captcha solving as object detection + prompt reasoning + optional color/orientation classification
- Siamese or classifier augmentation when prompt/reference matching is visual rather than textual
- restoring debugging/devtools visibility in embedded or desktop browser shells (WeChat/xweb/miniprogram contexts)
- opening a code/debug plane before brute-forcing business logic

## Strong recurring ideas

### 1. Many slider/captcha challenges are still artifact-generation problems at heart
The 2025 competition article is useful because it shows that a seemingly interaction-heavy problem can collapse into:
- recover stack/instruction semantics from logging or instrumentation
- identify array/word transforms and index flows
- map them into a deterministic arithmetic / lookup pipeline
- generate the final answer directly

This strongly reinforces an earlier browser-branch lesson:
- **UI appearance does not guarantee UI-level difficulty; often the real task is still data-path recovery**.

### 2. Captcha solving should often be split into three layers: acquisition, perception, reasoning
The 易盾 article is valuable because it explicitly decomposes the problem:
- acquire challenge images + prompts at scale
- build perception models (detection/classification/orientation/color)
- perform prompt reasoning on top of those outputs

That is a much better KB framing than “train a model to solve captcha.”
It turns the work into a modular pipeline.

### 3. Prompt reasoning is often simpler than the image model once the ontology is made explicit
The 易盾 writeup contributes a subtle but high-value lesson:
- once object classes, orientation, and optional color are normalized,
- prompt parsing becomes a constrained symbolic reasoning problem,
- not a vague NLP problem.

This means many point-click captchas can be reduced to:
- ontology design
- dataset labeling
- detection/classification
- deterministic prompt-to-target matching

### 4. The best model stack depends on whether the prompt references textual labels, object classes, or visual similarity
The point-click article is useful because it distinguishes at least two major regimes:
- yolo + OCR/classifier when the prompt can be grounded to named/textual targets
- yolo + Siamese when the prompt itself is image-like and the task is visual similarity matching

This is strong operator guidance because it is a **topology selection rule for the perception stack**.

### 5. Browser challenges become much easier once you restore a true debugging plane
The WeChat/xweb/miniprogram articles are valuable because they show a different but complementary move:
- before over-instrumenting bundles externally,
- restore DevTools / inspectability / JS step-debugging in the production-like runtime itself,
- then debug the actual executing page or mini-program.

This is highly compatible with the branch’s existing emphasis on observability-first workflows.

### 6. Embedded browser shells often hide the debug plane behind a small gate, not a deep impossibility
Both embedded-browser debug articles reinforce this useful practical rule:
- the inability to F12/inspect may come from a small explicit gate (one return, one flag, one `isInspectable` property) rather than some deeply inaccessible runtime
- patching that gate can re-open the whole observation surface

This should likely become a reusable workflow note later.

### 7. “Model-first” and “debug-first” approaches are complementary, not opposed
A nice synthesis from this batch:
- for some captchas, deterministic code/path recovery yields a pure solver
- for others, model pipelines do the perception work and reasoning closes the loop
- in both cases, improved observability/debugging lowers the problem cost substantially

That makes the browser branch richer without making it incoherent.

## Concrete operator takeaways worth preserving

### A. Captcha pipeline decomposition workflow
Reusable sequence:
1. separate the challenge into acquisition, perception, and reasoning
2. determine whether the decisive part is deterministic code-path recovery or visual perception
3. build only the minimum perception stack needed for the challenge ontology
4. keep reasoning symbolic/deterministic whenever possible

### B. Perception-stack topology selection rule
Reusable sequence:
1. if the target can be grounded to text or named labels, prefer detection + OCR/classifier
2. if the target is defined by image similarity/reference examples, prefer detection + Siamese/embedding comparison
3. add color/orientation classifiers only when the prompt truly requires them
4. do not overbuild a monolithic model when modular pipelines are enough

### C. Prompt-ontology normalization workflow
Reusable sequence:
1. collect prompts and perform frequency/category analysis
2. normalize object classes, orientation, color, and special equivalence cases
3. convert prompt matching into a deterministic rule engine once the ontology is explicit
4. keep the rule engine separate from the visual model outputs

### D. Embedded-browser debug-plane restoration workflow
Reusable sequence:
1. identify whether the runtime blocks DevTools/inspectability via a narrow gate
2. locate the gate by strings, properties, or small return-value checks
3. patch/override the gate to reopen inspection or JS debugging
4. debug the real production-like runtime rather than relying only on unpacked/rehosted artifacts

### E. Debug-first reduction rule for browser challenges
Reusable rule:
- when a browser-side challenge seems too opaque, first ask whether the actual missing piece is a debugging plane
- if you can restore inspectability/DevTools in the executing shell, do that before overcommitting to external deobfuscation or model work

## Candidate KB implications
This batch strongly supports or suggests improvements to:
- browser-runtime and anti-bot subtree notes
- captcha/slider practical workflow branches
- environment observability and embedded-browser debugging notes

Potential future child-note opportunities:
- captcha pipeline decomposition note (acquisition/perception/reasoning)
- perception-stack topology selection note
- embedded-browser debug-plane restoration note
- prompt-ontology normalization note for point-click captchas

## Confidence / quality note
This is a strong late browser batch because it widens the branch without making it fuzzy.
Its best contribution is the operator framing that many captcha/browser challenges are solved either by:
- restoring observability and reducing them into deterministic artifact pipelines,
- or building the smallest viable perception + reasoning stack.

Both are workflow-centered and KB-friendly.
