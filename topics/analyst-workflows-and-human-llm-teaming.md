# Analyst Workflows and Human–LLM Teaming in Reverse Engineering

## Why this topic matters
A reverse-engineering expert knowledge base should not only track what tools can recover from binaries. It also needs to capture **how experts actually work**:
- how they build and revise hypotheses
- how they sequence static and dynamic analysis
- how they externalize intermediate findings
- where they get blocked cognitively
- and how newer AI assistance changes, helps, or harms those workflows

This matters because expert reverse engineering is not only an output-generation problem. It is also a **sensemaking** and **workflow orchestration** problem.

## High-signal items collected so far

### 1. Votipka et al. (USENIX Security 2020): observational model of reverse-engineering process
Source:
- **An Observational Investigation of Reverse Engineers’ Processes**

Key points from the accessible abstract/page:
- semi-structured observational interview study of **16 reverse engineers**
- asks what questions reverse engineers pose, how they answer them, and how they decide what to do next
- distills a three-phase model:
  - **overview**
  - **sub-component scanning**
  - **focused experimentation**
- reports that analysts typically rely more on **static methods** in the first two phases and more on **dynamic methods** in the final phase
- experience matters in all phases, but differently
- paper proposes **five interaction-design guidelines** for reverse-engineering tools

Why it matters:
- this is one of the clearest anchors for modeling expert RE as a staged sensemaking process rather than a flat list of tactics
- strongly supports organizing the KB around analyst-support patterns, not just benchmark families

### 2. Mantovani et al. / malware-analyst workflow taxonomy (CCS 2021-era artifact)
Accessible signal from the fetched PDF metadata/table of contents indicates a substantial workflow study covering:
- malware analyst taxonomy
- analyst objectives and tiers
- malware analyst workflows
- prioritization
- main analysis process
- factors leading to workflow differences
- dynamic-analysis setup choices
- evasion handling
- usability recommendations

Even without a clean extracted body, the available structure is already useful.

Why it matters:
- shows that RE-adjacent expert practice has enough recurring structure to justify taxonomy-level documentation
- suggests this KB should explicitly track:
  - analyst goals
  - analyst tiers / experience bands
  - workflow branching conditions
  - environment and instrumentation setup decisions
  - anti-evasion coping strategies

### 3. Decompiling the Synergy (NDSS 2026): first systematic human–LLM teaming study in SRE
Source:
- **Decompiling the Synergy: An Empirical Study of Human–LLM Teaming in Software Reverse Engineering**

Key points from the NDSS paper page:
- claims to be the **first systematic investigation** of how LLMs team with analysts during software reverse engineering
- includes an online survey of **153 practitioners**
- includes a human study with **48 participants**:
  - **24 novices**
  - **24 experts**
- instruments over **109 hours** of SRE activity
- reports **18 findings** about benefits and harms
- key reported effects:
  - novice comprehension rate rises by about **98%**, roughly matching experts
  - experts gain comparatively little
  - known-algorithm functions are triaged up to **2.4× faster**
  - artifact recovery (**symbols, comments, types**) increases by at least **66%**
  - harms include hallucinations, unhelpful suggestions, and ineffective results

Why it matters:
- this is a major structural result for the KB
- suggests LLMs may be best understood as **gap-narrowing accelerators for lower-experience analysts**, not universal multipliers for experts
- also suggests expert workflows need explicit safeguards against overtrust, especially for plausible but wrong semantic suggestions

### 4. Cisco Talos (2025): practical MCP-mediated LLM sidekick model
Source:
- **Using LLMs as a reverse engineering sidekick**

Key practical points from the article:
- frames LLMs as workflow complements rather than replacements for malware analysts
- emphasizes using **MCP-style tool integration** with disassemblers/decompilers such as **IDA Pro** and **Ghidra**
- highlights practical constraints that materially affect RE usefulness:
  - context-window pressure
  - tool-use overhead and cost
  - model support for structured instructions/tool usage
  - privacy/confidentiality concerns for cloud models
  - latency and hardware limits for local models
- gives an explicit stack example:
  - MCP server + IDA Pro plugin
  - VSCode-based MCP client
  - local Ollama model and cloud Claude model

Why it matters:
- adds a practitioner-oriented complement to the NDSS human-study result
- clarifies that human–LLM teaming quality depends heavily on the **automation interface**, not just the model
- supports a subtopic on **automation interfaces shaped by analyst interaction needs**

### 5. Brown et al. / Frontiers 2026: immersive sensemaking synthesis for binary RE
Source:
- **Immersive sensemaking for binary reverse engineering: a survey and synthesis**

Key points from the accessible article text:
- frames binary RE as a cognitively demanding, uncertainty-heavy task unlikely to be fully automated
- synthesizes RE cognition, cognitive systems engineering, and immersive analytics
- argues that useful support should target three broad themes:
  - **enhancing abductive iteration**
  - **augmenting working memory**
  - **supporting information organization**
- treats immersion/embodiment not as aesthetics but as mechanisms for externalizing thought and stabilizing reasoning

Why it matters:
- broadens the workflow topic beyond LLMs
- gives a stronger conceptual vocabulary for describing expert RE as:
  - abductive
  - memory-limited
  - representation-sensitive
  - organizationally fragile

## Cross-cutting synthesis

### A. Reverse engineering is a staged sensemaking process
The workflow literature so far points to a recurring pattern:
- establish orientation / overview
- narrow to likely-relevant subcomponents
- run more focused experimentation
- continually revise the mental model as evidence accumulates

This means tools should not only maximize raw recovery quality. They should support **phase transitions** in analyst reasoning.

### B. Externalization is central
Several strands point the same way:
- observational RE studies care about questions, evidence, and decisions
- immersive-sensemaking work emphasizes working-memory relief and information organization
- practical LLM workflows rely on persistent tool context and artifact manipulation

A likely expert pattern is that good reversing depends on externalizing:
- hypotheses
- naming guesses
- intermediate semantic anchors
- uncertainty boundaries
- evidence trails

This suggests the KB should eventually track notebook/memory-augmented workflows explicitly.

### C. LLM value is uneven across experience levels
The NDSS 2026 result is especially important here.

Current evidence suggests:
- novices may gain large comprehension and triage benefits
- experts may gain less on average
- artifact recovery improves, but trust calibration becomes more important
- hallucinations and irrelevant suggestions remain serious workflow hazards

So the right model is not “LLMs make everyone better equally.”
A better framing is:
- **novices:** scaffolding, explanation, faster triage, artifact bootstrap
- **experts:** selective acceleration, metadata drafting, candidate hypothesis generation, but with persistent verification burden

### D. Interface and orchestration matter as much as model quality
The Talos article makes this concrete.

In practice, usefulness depends on:
- how the model accesses disassembler state
- how much context can be retained without truncation or runaway cost
- whether tool use is reliable and structured
- whether sensitive samples can be analyzed locally
- how well the analyst can control, inspect, and reject model suggestions

This reinforces that the KB should distinguish:
- **model capability claims**
- **workflow integration patterns**
- **trust and verification burdens**

### E. Analyst-support research deserves first-class status in the KB
A stable top-level family is emerging:
- observational studies of reverse engineers
- workflow/sensemaking models
- human–LLM teaming
- notebook/memory-augmented analysis flows
- visualization / immersive-analysis support
- automation interfaces shaped by analyst interaction needs

This is not peripheral to expert reversing. It is part of the core subject.

## Open questions
- What are the five tool-design guidelines from Votipka et al., in exact form?
- Which workflow models generalize across malware, firmware, vulnerability research, and protected-binary analysis?
- How should the KB represent expert-vs-novice differences without flattening them into one continuum?
- What kinds of LLM assistance are actually net-positive for experts: renaming, summarization, type suggestions, algorithm labeling, search, note synthesis, or conversational planning?
- Which failure modes are most workflow-damaging: hallucinated semantics, overconfident renaming, context loss, tool misuse, or privacy constraints?
- Are there strong papers on RE notebooks, evidence trails, or persistent analyst memory systems beyond general sensemaking literature?
- Which evaluation metrics best reflect analyst-support value: comprehension rate, time-to-triage, correction burden, trust calibration, or downstream bug-finding yield?
