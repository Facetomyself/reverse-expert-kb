# Reverse Expert Knowledge Base

This directory is for an hourly research-and-synthesis cron workflow focused on building a reverse-engineering expert knowledge base.

## Goal

Continuously collect, analyze, and organize high-signal knowledge about reverse engineering, while staying in the **research / note-taking / source-collection** stage.

The workflow should:
- search broadly across multiple sources
- avoid repeating the exact same findings every run
- reflect on what is newly learned vs already known
- write clean Markdown notes
- keep downloaded/source material organized

## Structure

- `index.md` — rolling high-level map of themes, open questions, and promising directions
- `runs/` — one Markdown report per hourly run
- `sources/` — downloaded/reference material grouped by source or topic
- `topics/` — topic-focused synthesis notes that mature over time

## Current stage

Research only. No implementation/building yet.

## Research focus

Construct a comprehensive line of thought for a "reverse engineering expert knowledge base", including but not limited to:
- static analysis
- dynamic analysis
- decompilation
- disassembly
- symbolic execution
- binary instrumentation
- unpacking and obfuscation analysis
- malware analysis overlaps
- Android/iOS reversing
- Windows/Linux/macOS reversing
- firmware / embedded reversing
- game anti-cheat / anti-tamper related reversing knowledge
- protocol reverse engineering
- tooling ecosystems
- workflows and knowledge organization methods
- datasets, benchmarks, corpora, and training material
- case-study driven expert heuristics

## Output rules

- Markdown only for notes/reports.
- Be incremental: prefer updating existing structure over creating scattered one-off notes.
- Keep source material organized under `sources/` by topic/source.
- In each run, clearly separate:
  - newly discovered information
  - deduplicated known information
  - reflections / synthesis
  - next research directions
