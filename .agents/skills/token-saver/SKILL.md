---
name: token-saver
description: Aggressively reduce unnecessary context, repeated reads, repository scanning, memory loading, verbose tool use, and token consumption while preserving correctness.
---

# Token Saver — Context Minimization

## Core Principle

Use the smallest sufficient context. Every additional piece of context must justify its token cost.

## Search-First Workflow

TASK
→ SEARCH
→ LOCATE
→ TARGETED READ
→ EDIT
→ TARGETED TEST
→ UPDATE STATE
→ STOP

## Repository Discipline

Never scan the entire repository by default. Search by:
- filename
- symbol
- function
- class
- route
- component
- config key
- error string

Read only relevant sections. Expand outward only when required.

## Memory Discipline

Historical memory is expensive context. Default: DO NOT retrieve broad memory.
Use historical memory only when:
- current task depends on a previous decision
- information is not already present
- the memory fragment is directly relevant
- it materially affects correctness

Never retrieve all memory merely "for context".

## Conversation Discipline

Prefer:
1. Current user request
2. Working state (`.agents/context/WORKING_STATE.md`)
3. Recent relevant messages
4. Specific historical context only when needed

Do not preserve greetings, repeated explanations, obsolete plans, or abandoned exploration.

## Reread Prevention

Do not reread unchanged files unless:
- exact implementation detail is required
- summary is insufficient
- file changed
- new evidence requires reinspection

## Large Files & Logs

- Search first, then read only the target line range.
- For logs: search exact error string → surrounding lines → stack frame → failing function. Do not ingest full logs.

## Tests & Stop Condition

- Prefer: single targeted test → affected module tests → broader suite only if required.
- **Stop condition:** Once sufficient evidence exists to take the next correct action, STOP SEARCHING.
