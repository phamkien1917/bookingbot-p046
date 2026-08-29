---
name: ponytail
description: Enforce radical simplicity, YAGNI, standard library first, deletion before addition, minimal abstractions, and smallest correct changes while preserving correctness.
---

# Ponytail — Radical Simplicity

Operate with extreme discipline around simplicity, pragmatism, and minimalism in code.

## Core Principles

1. **YAGNI (You Aren't Gonna Need It):** Build only what is needed for the immediate task. Never add speculative features, unused configurations, or future-proofing abstractions.
2. **Smallest Correct Change:** Solve problems with the minimum number of modified lines and files.
3. **Deletion Before Addition:** Remove dead code, redundant helpers, and obsolete logic before adding new code.
4. **Standard Library / Native First:** Prefer language built-ins and standard libraries over new third-party packages.
5. **Existing Dependencies First:** Reuse packages already in `requirements.txt` / `package.json` before introducing new dependencies.
6. **No Premature Abstraction:** Do not create layers of wrappers, generic factories, or speculative interfaces for one-off operations. Direct, readable code beats clever indirection.
7. **Correctness Invariant:** Simplicity never excuses broken functionality, skipped edge cases, or bypassed security.

## Workflow

1. Understand the exact problem.
2. Check if existing utilities or stdlib functions already solve it.
3. Write the most direct, readable, minimal fix.
4. Clean up any obsolete code created by the change.
5. Validate thoroughly.
